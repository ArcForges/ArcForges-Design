# 02 — Microsoft MXC integration

Status: V2 design adopted; composed native behavior awaits P1 qualification. Owners: `AFV2-MXC-01` through `AFV2-MXC-04`. Evidence: [V-MXC-01–07 and A-MXC-01/02](../verification/platform-capabilities.md), [source research](../research/mxc-research.md), [source pins](../research/mxc-sources.json), and [native experiment protocol](../verification/mxc-experiments.md).

ArcForges uses official stable MXC for contained execution and security policy. ArcForges owns Sandbox persistence, Run identity, authorization, terminal sessions, host budgets, resource enforcement/readback, and recovery. Local CLI and Center requests enter the same Sandbox Core. No remote request can select an unvalidated backend, pass an arbitrary host executor, or bypass local policy.

## 1. Supported implementation profiles

Initial dependency pin: `Microsoft.Mxc.Sdk` **1.0.1** and official native artifacts from **v1.0.1**, with exact Windows JSON schema **1.0.0**. The package version is not the schema version. A dependency upgrade requires reviewed source/package pins and reruns of affected profile experiments. Floating `main`, development JSON, experimental launch flags, private FFI entrypoints, and privately patched MXC builds are outside these profiles. **V-MXC-01/02/07.**

| Profile ID | Official execution surface | Terminal mode | Required resource boundary | Admission state |
|---|---|---|---|---|
| `windows-process-executor-v1` | Unchanged official `wxc-exec.exe`, stable exact JSON, explicit `processcontainer`; native BaseContainer/PSEC with native denied-path support | C# Native AOT RunSupervisor owns ConPTY; executor inherits it; separate pipes are also an explicit mode | ArcForges Windows parent Job established before worker/executor execution; MXC owns its inner Job | Design adopted/source supported; full combination UNPROVEN under A-MXC-01 / F-MXC-01. |
| `linux-bubblewrap-sdk-v1` | `.NET Microsoft.Mxc.Sdk.V1.MxcContainer`, explicit `Containment.Bubblewrap` | `SpawnWithPty` or explicitly selected `Spawn` pipes | RunSupervisor starts in an already configured delegated cgroup v2/systemd boundary | Design adopted/source supported; full combination UNPROVEN under A-MXC-02 / F-MXC-02. |

Windows uses the official executor adjunct because stable .NET V1 does not expose ProcessContainer PTY/inherited-console creation or `fallback.allowDaclMutation`. The unchanged executor's inherited-console behavior is used by Microsoft's published stable Node adapter; ArcForges does not ship Node.js or copy that adapter. Direct stable .NET ProcessContainer pipes cannot be substituted for the default Windows profile because the same policy-authoring gap remains. **V-MXC-02.**

No automatic fallback to IsolationSession, AppContainer tiers, WSLc, Windows Sandbox, LXC, MicroVM, Hyperlight, host execution, plain pipes, shared host networking, or weaker resource control is permitted. A future stable .NET release may replace the executor adjunct only through an explicit profile revision and the combination gate. A labeled pipes-only development build is not full V2 terminal delivery.

## 2. Capability negotiation and admission

Discovery returns structured capabilities for the installed profile, rather than a single `mxcAvailable` boolean. The response includes profile revision, managed/native versions, artifact identity, architecture, OS build/kernel, native backend/tier, discovered network modes, terminal modes, resource-controller availability, probe time, and qualification evidence identifier. Represent each capability as `supported`, `unsupported`, or `unproven`; do not convert an unrun test to support.

For every Start request, the core validates the complete combination of terminal mode, filesystem policy, network policy, environment, resource requirements and recovery policy. Discovery is advisory; request validation and execution can still fail on a changed host. Persist the selected immutable Sandbox configuration revision, compiled policy hash, actual profile and owner identity with the Run before executing user code. **V-MXC-02/03/04.**

| Condition | Required response |
|---|---|
| MXC, official executor, native library, required controller or helper missing | Fail admission with the concrete dependency/capability reason; no workload started. |
| Requested feature is unsupported by the profile | `UnsupportedCombination` naming profile, feature and failed requirement. |
| Relevant native combination has not been qualified | Mark unproven; P1 experiment route only. Do not advertise normal product support. |
| Windows probe chooses fallback tier or native deny is unavailable | Reject; do not auto-run host prep or ask the workload to proceed with relaxed security. |
| Linux requests host/public ingress or available IPv6 connectivity unsupported by stable Bubblewrap | Reject the unsupported request; retain the user's intended policy unchanged. |
| Policy/native launch changes after preparation | Fail launch and reconcile all created resources; do not retry through another backend. |
| Resource settings cannot be installed and read back before launch | Fail admission/launch; do not run with a merely desired limit. |

Windows uses the exact request in `wxc-exec --probe --config <private-file>` to inspect native tier and capability diagnostics before the launch attempt. `MxcContainer.Probe` can supplement general discovery but cannot author the full fallback prohibition in typed 1.0.1. The profile always includes a deny for its existing private control directory and `fallback.allowDaclMutation=false`. In stable source, every AppContainer DACL tier needs consent, and AppContainer BFS needs it for nonempty denies. This provides request-level rejection on a changed host as well as preflight detection. This source-derived property must be demonstrated with the shipped official binary; it is not a new MXC tier-selector API. **V-MXC-02/03; A-MXC-01.**

## 3. Ownership and launch ordering

`RunSupervisor` is a trusted local execution owner separate from the transient CLI/Web client and the restartable Node request handler. It owns exactly one Run's native/terminal handles and an authenticated control endpoint. Node can restart without destroying that owner. Persistence of Sandbox data does not depend on persistence of an MXC container.

| Resource | Owner and lifetime |
|---|---|
| Sandbox directory/configuration | Sandbox Core; persists across Runs and service restarts. |
| Run journal, compiled request, policy hash | Core plus authenticated supervisor; prepared before launch, retained with bounded diagnostic policy. |
| Outer Job/cgroup identity and enforcement handles | ArcForges resource owner; a surviving supervisor/durable manager retains ownership across Node restart. Never only a client handle or PID. |
| Windows official executor process and ConPTY | RunSupervisor; survive client detach; close only during verified finalization. |
| Linux `MxcProcess` / `MxcPtyProcess` | RunSupervisor; disposal kills the native tree and is not a detach operation. |
| MXC internal Job, PSEC, namespace/firewall/proxy resources | Official MXC runtime; do not close, duplicate, inject into, or reimplement private handles. |
| Terminal output draining/replay | RunSupervisor; continues when no clients are attached. |
| Account/Center connection | Node remote-management layer; losing it does not own or stop a local Run. |

### Required sequence

1. Authorize the local principal, resolve Sandbox revision and executable/arguments, reserve budget, validate storage ownership and capability combination, and journal `Prepared` with operation/Run identities.
2. Create the outer resource scope and apply/read back required limits. Establish a trusted per-Run supervisor with a durable control endpoint. On Windows start the worker suspended, assign the valid Job chain, install retained non-inheritable ownership handles, and only then resume. On Linux use the delegated service/cgroup launch path that places the worker in the configured scope before its executable begins.
3. The supervisor acknowledges its host-boot/start/owner-generation identity and exact resource membership over authenticated local IPC. The creating Node may release its duplicate ownership handle only after the supervisor owns the boundary. Parent death at every intermediate stage must fail closed without an unowned workload.
4. Create terminal or pipe endpoints and begin the output-drain owner. Invoke only the selected official executor/SDK through the compiled request. No post-Spawn PID attachment is allowed as the primary resource guarantee.
5. Record supervised execution active and the observed payload-start certainty. Monitor native completion, the supervisor deadline, resource readback, terminal flow, and requested Stop independently of client cancellation.
6. After native/executor exit, finalize MXC and verify the outer workload subtree is empty. If trusted supervisor processes inhabit the accounting scope, compare exact identities and require that only the documented controller members remain; a nonzero aggregate is not silently called empty. Helpers and every untrusted descendant must be gone. Release remaining controller members/scope after final records are safely committed.

The Windows outer Jobs have no UI limits and no breakaway. BaseContainer's inner Job is owned by MXC and created before payload resume. Inherited ancestor Jobs from service launch must also be inspected; a service wrapper can otherwise invalidate the proposed hierarchy. P1 must demonstrate memory/CPU enforcement and accounting with the entire hierarchy, not just `AssignProcessToJobObject` returning success. **V-MXC-03.**

Resource ownership must survive Node termination, and its identity must be recoverable by a new Node through the same supervisor or authenticated durable owner. A name/PID supplied by a stored row is insufficient. On supervisor loss, retained parent ownership and OS cleanup policy terminate the Run and independently confirm cleanup. If exact ownership cannot be established, quarantine the unresolved Run and its data; do not attach to a guessed process. The final implementation of handle duplication, names, ACLs and service-manager ownership is accepted only with the crash experiments. **A-MXC-01/02.**

## 4. Windows executor protocol

The executor path is fixed by the protected installation manifest for the selected architecture. Validate signature, version and hash at install/update, and resolve the executable by full path. Never discover it from the user's PATH or an inherited `MXC_BIN_DIR`/native-library override. Launch it without a host shell.

The core writes exact schema 1.0.0 JSON, not a serialized typed `ContainerRequest`. The minimum profile constraints are:

- Explicit `containment: "processcontainer"`, unique Run-scoped container identity, explicit command/cwd/env, and one-shot lifecycle cleanup.
- Explicit read-only/read-write/deny lists; the existing private Run control directory is always denied and is outside every workload grant. Native denied-path support is mandatory.
- `fallback.allowDaclMutation: false`. No `--experimental`, learning mode that permits denied access, elevated host preparation, or testing tier overrides.
- `processContainer.leastPrivilege` is omitted/false: this is an LPAC-specific option that native BaseContainer rejects, not a generic switch to strengthen this profile. An explicit request requiring it is an unsupported combination.
- Explicit directional network policy; no accidental capability broadening. Required CLI UI restrictions remain enforced by the native policy.
- Explicit per-request telemetry disabled by default for this stable pin, and a supervisor-owned deadline with truthful stop attribution.

Store the JSON in an owner-restricted per-Run control directory, separate from all Sandbox writable data and host-import/export locations. Create a new file atomically, reject symlink/reparse traversal and preexisting collisions, enforce maximum UTF-8 size, flush before launch, and bind it to the Run/policy hash. Its ACL must allow only the intended trusted service/supervisor identity; the untrusted restricted payload must not read or mutate it. Do not grant a parent directory that exposes it. Preserve the file until both admission probe and actual launch have consumed it; bounded cleanup removes it after the run no longer needs it. Record policy hashes/redacted structure in ordinary logs, not secret environment values.

Pass `--config` and the absolute private file path as two correctly encoded executor arguments. Base64 JSON in argv is not used because it exposes configuration to command-line observation. Configuration is not sent through stdin; stdin belongs to the workload. The source's separate `--log-file` diagnostics are not a substitute for a documented authenticated control protocol.

Use a real JSON serializer with the pinned exact schema, not string templates. The trusted executor/supervisor environment is a separate allowlist from the payload environment; strip user-controlled MXC loader, binary-location and testing overrides before any SDK or helper discovery. Launch from a protected working location so native-library search cannot consume writable development artifacts.

User executable and arguments are validated and serialized into the request's command line with tested Windows quoting; NUL and invalid environment keys are rejected, case-insensitive duplicate Windows environment names are resolved deterministically or rejected. Shell execution requires an explicit chosen shell executable and script/arguments. Policy paths and executable argv are separate fields; no interpolation through `cmd`, PowerShell, or a host command template occurs.

The supervisor uses documented ConPTY creation and resize with concurrent pumping, then launches the official executor inside that pseudoconsole. This startup attribute is applied to ArcForges's trusted executor launch; it is not passed through an imaginary SDK method. The executor's official ProcessContainer launch inherits its terminal. Ordinary pipe mode is separately identified in the Run and never advertised as a terminal. **V-MXC-02; MXCS-09/10/24 in the source catalogue.**

## 5. Linux SDK protocol

Use the selected public `.NET V1` surface after the RunSupervisor is inside its resource scope:

- Explicit `new Containment.Bubblewrap()`; `ContainerRequest` carries command, working directory, exact environment, filesystem and network policy.
- Pipe mode uses `MxcContainer.Spawn`/`SpawnAsync` and `MxcProcess` streams. Terminal mode uses `MxcContainer.SpawnWithPty` and `SpawnWithPtyOptions.Size`.
- Consume terminal `Input` and `Output` before starting the dedicated lifetime wait. For pipes, take every stream the supervisor will own before `WaitAsync`, then drain stdout/stderr concurrently.
- Keep the lifetime wait/deadline owner independent of a client/RPC cancellation token. `Kill` and final `Dispose` are deliberate lifecycle operations.
- Treat required native/helper versions, namespace availability and cgroup controllers as admission facts. Missing network dependencies fail explicitly; there is no host-network retry.

The stable SDK accepts a command string; Bubblewrap executes it through a contained `sh -c`. An executable-plus-argv request therefore needs a tested POSIX serializer, such as an `exec` command with each argument safely quoted. It must not concatenate raw caller input into shell syntax. An explicitly requested shell script remains allowed as a workload. The host never evaluates the workload command as part of supervisor creation. **V-MXC-04/05.**

Filesystem grants present the same absolute host paths; no `/work` or synthetic-home alias is assumed. Direct only cooperative application state through explicit HOME/XDG/temp paths. A small list of intentional runtime variables is distinct from host service environment inheritance. Policy and resources are validated together with terminal mode, including the additional network namespace/helper tree. **V-MXC-04/05.**

## 6. Terminal, Stop, pause, and exit contract

Attach creates a client session over the supervisor's existing terminal; Detach removes that session only. At most one authorized writer lease controls input and resize at a time; read-only observers never gain control through output parsing. Terminal bytes are opaque untrusted data. Dimension validation follows the SDK range of 1–32767 for both rows and columns; client abuse/backpressure limits are enforced before native calls. Output is always drained into bounded recording/replay with explicit gaps when data is dropped. **V-MXC-06.**

`Ctrl+C` is a terminal input operation with platform/application semantics, not universal proof of process-tree termination. A Stop request records intent and an absolute monotonic escalation deadline, performs a negotiated graceful interrupt where supported, and then uses native tree kill/outer-boundary enforcement. A raw-mode TUI may receive ETX as input. Closing input requests EOF only; closing the terminal is not the graceful-stop API. Pause/resume is unsupported in these initial profiles because no stable public generic MXC operation establishes the necessary tree, terminal and deadline semantics.

The Run model records at least `exit_source={payload,official_executor,supervisor,unknown}`, raw code if observed, `payload_started={unknown,confirmed,no}`, effect certainty, and `stop_reason`. The Windows profile normally observes executor provenance; do not label it payload provenance without independent evidence. Native launch failure, application nonzero exit, timeout, forced stop, owner loss and cleanup failure remain distinguishable observations where evidence permits, otherwise uncertainty is explicit. An error-shaped stderr line must never set a trusted status. `RUNNING` means the supervisor is actively owning an execution attempt; it does not promise payload entrypoint confirmation.

A root exit ends the one-shot execution and MXC terminates leftover children. Long-running services therefore retain their root/foreground process. The record may retain the observed exit while the Run is cleaning; it becomes terminal only after all workload descendants and helpers are gone and required records/ownership changes are durable. MXC's internal five-second Job drain warning is not sufficient cleanup proof. Cleanup failure retains a bounded error and the unresolved resource/data ownership so a later recovery operation can finish safely. **V-MXC-06.**

## 7. Upgrade, qualification, and failure decisions

The admitted profile is a tuple of stable package/runtime, protected distribution, OS/architecture, backend/tier, policy capabilities, resource composition and terminal mode. A profile upgrade does not migrate an active Run's native handles. Drain or retain its installed version until existing owners finish; new Runs use the newly qualified revision. Never delete the installed native unit while a live supervisor depends on it.

P1 requires `MXC-AOT-01`, `MXC-WIN-01` through `MXC-WIN-06`, and `MXC-LNX-01` through `MXC-LNX-05` as applicable. The [protocol](../verification/mxc-experiments.md) supplies evidence and bounded negative cases. `AFV2-MXC-04` accepts a profile only when the same native environment satisfies the mandatory terminal/filesystem/network/resources/recovery combination. All are currently **NOT_RUN / UNPROVEN**.

If the unchanged official executor cannot support the required composition, record a stable upstream capability blocker. The Plan then requires a supported stable remedy or an explicit product decision; it does not implement a private fork, quietly drop the terminal requirement, relax limits, or mark a pipes demonstration as full acceptance. Preserve currently necessary execution/resource assets until this gate proves their replacement.
