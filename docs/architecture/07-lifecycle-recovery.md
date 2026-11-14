# Sandbox and Run lifecycle, ownership and recovery

Status: current V2 design. AFV2-CORE-01 through AFV2-CORE-03 establish the model/owner; AFV2-REC-01 qualifies interruption recovery; AFV2-DATA-01 migrates existing state. Native backend ownership and terminal behavior depend on AFV2-MXC-01 through AFV2-MXC-04. This chapter uses the canonical Sandbox/Run state names; transport connectivity and terminal attachment are separate states.

## 1. Persistent Sandbox and ephemeral Run

A Sandbox is persistent configuration plus an owned data root, grants, resource policy, profile selection and monotonically increasing revision. It is not a live MXC container. Creating it does not require starting a payload. Multiple Runs may execute within it only when the configured concurrency/resource policy permits; they share the explicitly described persistent directories and may affect each other's application files. ArcForges does not promise application-level serialization inside shared writable data.

A Run is one immutable start snapshot and one managed foreground root with descendants under a single execution owner. Run ID is never reused. Restart is a new Run ID referencing the same Sandbox, not a reset of the prior terminal record. A Sandbox can retain data after any number of completed, failed or lost Runs.

The local Node and optional Center refer to these same identities. Remote connectivity cannot change the lifetime of a local Run. Disabling remote control prevents future remote mutations and closes authorized remote output subscriptions; it does not implicitly stop local programs. Terminal input/resize is local-only in the initial V2 surface.

## 2. Sandbox states

| State | Meaning | Allowed operations |
|---|---|---|
| CREATING | Durable create intent exists; owned-root setup not finalized | Inspect, inspect operation; no Start or delete effect |
| READY | Valid configuration and owned-root identity; no unresolved Sandbox-wide recovery block | Inspect, configure via revision CAS, Start within policy, data operations subject to Run/in-use rules |
| DELETING | A deletion operation holds the mutation lease | Inspect, inspect/resume/cancel only as allowed by deletion phase; no Start/configure/import |
| DELETED | Confirmed owned-root deletion and retained tombstone | Inspect retained receipt/tombstone; repeated identical delete succeeds idempotently |
| ERROR | A definite nonexecuting setup/configuration failure | Inspect and explicit repair/retry; no Start until successful revalidation |
| RECOVERY_REQUIRED | Ownership or a possible filesystem effect is unresolved | Inspect/export only when independently safe, explicit reconciliation; no Start or destructive delete |

Configuration changes use a single-writer lease and `expected_revision` while the Sandbox remains READY. Read validation and write commit are bound to the same revision. The successful change increments the revision once. A running Run retains its snapshot; path, network, profile and identity changes require no nonterminal Runs. An immediate revocation workflow must stop and drain affected Runs before committing the new configuration. A configuration conflict returns the current revision and no effect.

Create uses exclusive native directory creation and a durable intent. A crash before any effect can return ERROR/failed operation; a partially created owned root is reconciled from exact identity and marker. Do not erase an unknown preexisting directory because its path matches the requested ID. A successful root is finalized READY only after permissions, required child directories and metadata commit are complete.

## 3. Run states and observable outcome

| State | Entry evidence | Exit rule |
|---|---|---|
| STARTING | Durable Start receipt/reservation and immutable snapshot; launch ownership allocated | To RUNNING after trusted owner/backend admission; to FAILED only on definite no-payload launch rejection with cleanup confirmed; to STOPPING when stop wins the race; to RECOVERY_REQUIRED on uncertain ownership/effect |
| RUNNING | Trusted owner is active in the qualified resource boundary and the backend has begun the execution lifecycle | To STOPPING on authorized stop/pressure policy; to DRAINING on root/executor completion or owner finalization |
| STOPPING | Durable stop intent, reason and deadline recorded | To DRAINING after graceful/forced termination is requested and root ends; RECOVERY_REQUIRED if ownership cannot be controlled/reconciled |
| DRAINING | Root/executor has ended or forced cleanup began; managed descendants/handles are still being checked | To EXITED only after trusted final record and independent empty-scope proof; to RECOVERY_REQUIRED if cleanup remains unclear |
| EXITED | The Run's execution lifetime is terminal and no managed payload descendants remain in the known scope | Immutable outcome; only retained-output/receipt queries and retention work |
| FAILED | Definite pre-start/launch failure with no remaining managed payload effect or ownership | Immutable failure receipt; new Start requires a new operation and Run ID |
| RECOVERY_REQUIRED | Possible execution/cleanup effect or resource ownership cannot be proven | Inspect and bounded reconciliation/explicit stop by verified identity; never unconditional PID killing or automatic restart |

`RUNNING` is not a fabricated proof that an arbitrary payload's first instruction executed. Record `payload_started` separately as `unknown`, `no` or `confirmed`, using only trusted backend/native observation. Some official executor surfaces cannot distinguish all startup stages; preserve unknown. No terminal text, PID existence alone or guessed delay can certify payload execution.

Terminal outcome fields are independent of the state:

- `exit_source`: payload, official_executor, supervisor or unknown.
- Raw observed exit code/signal, absent if not observed; never invent zero.
- `payload_started`: unknown/no/confirmed.
- `termination_reason`: natural_exit, user_stop, pressure, shutdown, owner_failure, host_reboot, backend_failure or another catalogued reason.
- Operation effect certainty and cleanup certainty, with source/time and bounded detail.
- Accepted/started/root-ended/drained timestamps where actually observed, output cursor bounds and final resource counters.

A payload that runs and exits nonzero is EXITED with that observed exit; it is not a FAILED launch. A user-stopped Run is EXITED with `termination_reason=user_stop`, not a separate STOPPED state. A wrapper exit code may be presented only with `exit_source=official_executor`; do not label it a payload exit if the published protocol cannot prove that. Unknown effect remains unknown even after processes are gone: termination does not undo files or network side effects already performed.

## 4. Durable RunSupervisor

One trusted RunSupervisor owns the official SDK/executor handles, PTY master or pipe handles, output capture, resource-scope lifetime and durable completion record. It is launched from the signed/admitted installation, with a fixed helper role, a private per-Run control file and capability-bound local channel. The control file and endpoint live outside every workload grant. The owner enters the qualified resource boundary before invoking the backend; user code must never run in a pre-admission gap.

The Node records Run ID, Sandbox ID/revision, snapshot digest, Node installation identity, host boot identity, supervisor PID and native process creation identity, endpoint/channel generation, resource-scope identity, backend/profile version and a reference to protected handshake material. PIDs alone are never authority. The supervisor's handle inheritance is explicitly restricted; workload processes receive neither Node credentials nor control/job handles that could extend authority.

The supervisor's control API contains only that Run's bounded lifecycle, input, resize, state and output operations. It cannot create another Run or execute arbitrary host commands. Its handshake binds the expected Run, snapshot, boot/process identity and generation; a remote account cannot connect directly to it. A stale Node reconnect, replayed stop or different request digest is refused or resolved from the durable receipt.

MXC native handles need not be reopenable after a Node restart because the live supervisor retains them. This design does **not** claim recovery of an SDK handle after the owner itself dies. If the official API cannot reopen state, preserve that limitation and use the outer ownership boundary to terminate/reconcile remaining work. [MXC research](../research/mxc-research.md) pins official surface and required experiments.

## 5. Exact backend completion semantics

The stable one-shot ProcessContainer candidate observes its root process and, when finalizing, terminates the internal process Job before cleaning up security/proxy state. Therefore background descendants do not have an independent promise to survive root exit. Long-running CLI services must keep their foreground root alive; CLI detach merely disconnects the client while the owner/root continue.

The stable native implementation's bounded wait-for-empty can warn and continue after five seconds. That makes executor exit insufficient evidence that every descendant has drained. ArcForges must obtain independent empty readback from its verified outer resource boundary. On Windows query the exact owned outer scope and exclude only the known trusted supervisor/guardian identities from the payload-empty test; those helpers remain separately accounted. On Linux observe the exact cgroup/service generation and verify that only permitted trusted owner processes remain, then stop/release the owner and confirm full scope emptiness as required by the profile.

Do not accidentally call a scope nonempty forever because the supervisor itself is still waiting to report completion; do not exclude every process whose name resembles the supervisor. Exclusions use held native identities. A PID that was reused, a scope path that changed identity or a same-named foreign Job is not a match.

The final transition to EXITED and permission to delete Sandbox data require this independent drain evidence. If native drain cannot be confirmed within the bounded cleanup deadline, persist RECOVERY_REQUIRED with the scope/identity/evidence, retain the data and expose the error. A warning message or normal executor return cannot close this acceptance.

## 6. Start and stop races

The Node serializes product mutations while platform work is asynchronous. A Start operation first validates authorization/revision/profile/capacity, records its immutable snapshot and reservation, then launches the trusted owner. The owner acknowledges the exact snapshot before invoking the backend. Each result carries the operation/Run/generation identity so a late completion cannot overwrite newer stop or recovery state.

If Stop arrives in STARTING, persist stop intent immediately and prevent the owner from starting user code when it has not crossed the admitted start boundary. If backend startup is already in progress, the owner continues observing actual launch and stops any created payload within the same recorded resource scope. A timeout does not mean no process exists. Do not release resource reservation or delete start metadata until no-effect or drained ownership is established.

Stop is idempotent by operation ID and Run ID. Repeating the same request returns its progress/result. Reusing an ID with different reason/policy is a conflict. A request against an already EXITED/FAILED Run returns the terminal state without starting another process. Multiple authorized stop requests converge on the earliest durable stop intent; a stricter explicit force escalation can shorten the remaining grace if policy permits, with its own audit record.

Graceful stop uses the selected profile's proven signaling mechanism and a bounded policy grace. Terminal Ctrl+C is ordinary terminal input; explicit Stop is a management operation. When grace expires, terminate the verified whole Run payload scope using the supported backend/outer-owner mechanism and enter DRAINING. Do not broadcast signals to an unverified host process group or enumerate arbitrary ancestry as an isolation fallback. Windows Job freeze remains unsupported unless separately proven; Linux frozen scopes must be thawed where required for supported termination paths.

## 7. Node restart and reconnect

On Node restart, acquire the same per-user/data-root singleton, open the store, check integrity after an unclean stop, and compare boot identity before reaching READY. Recover each unfinished Run independently:

| Observed evidence | Action |
|---|---|
| Same boot; authenticated live supervisor; snapshot/Run/scope identity matches | Rebind the control generation, read actual state/limits/output cursors, reconcile durable pending operations, resume monitoring; do not start a new payload |
| Same boot; durable trusted final record and independent scope-empty evidence | Commit terminal outcome and release reservation; recover receipt idempotently |
| Same boot; owner absent but scope still contains verified payload descendants | Enter STOPPING/DRAINING and terminate only the proven owned scope according to fail-closed owner-loss policy; terminal attachment is unavailable |
| Same boot; ownership or possible launch cannot be proved | RECOVERY_REQUIRED, retain reservation conservatively and refuse delete; no PID-only cleanup |
| Boot changed | Original OS processes cannot have survived; record host_reboot interruption with unknown raw exit if no final record, retain persistent data, and do not restart automatically |
| Store/config migration is unresolved | Keep mutations blocked for the affected object; expose the exact migration/reconciliation error |

Rebind authenticates both Node and owner. The new Node generation invalidates stale control connections but not the Run's terminal identity. Terminal writer leases are invalidated on Node rebind and require reacquisition by the authenticated local owner; read-only viewers reconnect by cursor and see a GAP if their offset is outside retention. No terminal control token is sent through Center as a reusable host capability.

A brief Node outage leaves supervisors running under their last accepted resource and filesystem policies. They retain their hard limits and bounded output behavior. The Node Resource Manager cannot adapt global budgets while absent; this limitation is visible in health metadata. Supervisors do not remove limits or invent cloud authorization when disconnected.

## 8. Owner crash, connection loss and host shutdown

The supervisor process lifetime is an independent failure boundary. The qualified Windows topology uses kill-on-close ownership and the outer scope to contain all descendants; all duplicate query/control handles must be accounted so a leftover Node handle does not accidentally defeat the expected last-handle cleanup. When the Node detects owner death, it explicitly reconciles/terminates the owned outer scope before releasing such handles. If both Node and owner die, the native topology must still provide the profile's bounded cleanup; this is a P1/P2 real-host test, not an assumed Job property of an unspecified handle graph.

On Linux, the supported user-service/cgroup topology binds owner death to full-group cleanup, with explicit service restart policy that does **not** rerun the payload. Record the actual main process/start generation and cgroup identity. User-manager restart/reexec and lost D-Bus connection must be tested separately from Node restart. A missing controller or service cannot be replaced by a plain child process.

Center loss only affects remote state freshness and remote output subscriptions. Existing Runs continue under local policy. There is no remote input/resize lease in the initial V2 surface. The owner keeps the terminal master open; local attachment and stop remain available. Subscription expiry denies future official-hosted remote management according to entitlement policy and never becomes a local Run stop trigger.

Host shutdown/reboot stops the operating-system processes. After boot, preserve Sandbox files and show interrupted Runs; automatic restart is outside the initial product scope. A user can explicitly start a service again. Output/operation records that were durably flushed are recoverable; data still in a process or filesystem buffer is not promised crash-safe.

## 9. Durable records and retention

The Node's transactional store is authoritative for object state, revisions, operation receipts, resource reservations, remote action audit and completion history. A bounded per-Run control record owned by the trusted supervisor captures launch/finalization facts needed while the Node is unavailable. Atomic replace plus appropriate flush/directory durability is used for owner records. Include version, Run ID, boot/process identity, snapshot digest, observed state, exit provenance, terminal offsets and resource counters; omit credentials, stdin and payload contents.

The Node accepts an owner record only after validating its ownership/provenance, identities and monotonic generation. An untrusted workload cannot author a completion record through stdout or its writable data directories. The Node commits the corresponding receipt/state once. The owner may then release resources after payload drain and record durability; final records remain until Node acknowledgment/retention makes deletion safe.

Keep records for Starting/Stopping/Draining/RECOVERY_REQUIRED Runs while effects remain unresolved even if normal history retention would expire. Old receipt deletion must not let the same Start operation execute again; maintain a bounded tombstone or reject expired command IDs under the API's replay policy. Logs may rotate independently, producing explicit cursor gaps. No cleanup of retained records may traverse external mounts or infer that an unknown owner is gone from timeout alone.

## 10. Migration from Task/Attempt

The existing runtime has proven recovery participants, boot identity, per-process creation identity, durable launch/exit records and holder acknowledgment. Reuse these patterns, not the old object state machine:

- [Recovery participants](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Recovery.cs)
- [Existing execution-platform ownership contract](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform/ExecutionPlatform.cs)
- [Windows holder/job implementation](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform.Windows/WindowsExecutionPlatform.cs)
- [Linux service ownership](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform.Linux/LinuxExecutionPlatform.cs)

At cutover, stop old admission, drain or explicitly stop old attempts, settle file-worker/journal holds, take a backup and append the V2 migration. Legacy historical attempts are exported as legacy executions; they are not relabeled isolated Sandbox Runs. Remove old Task/Attempt supervisor/helper routes and old live schema after the replacement and compatibility gates, without a permanent dual runtime. Preserve released migration bytes and shared packages used by independent products.

## 11. Recovery acceptance

AFV2-REC-01 must exercise crashes at every durable handoff: before Start receipt, after reservation/before owner, after owner/before backend, during backend startup, during active terminal input/output, between stop intent and signal, during forced termination, after root exit/before drain, after final record/before Node commit, and during delete/import effects. Tests inspect actual owned processes/scopes and foreign sentinels rather than only database state.

Additional required cases are Node restart with a live owner and unchanged payload PID identity; owner crash with Node alive; simultaneous Node/owner termination; native user-manager reconnect; PID/scope name reuse; unknown exit provenance; backend root exit with background descendants; drained versus still-populated scope; Center disconnect and subscription expiry; host reboot model plus an appropriately authorized real reboot/restart qualification in the Plan; and no automatic rerun of an arbitrary side-effecting CLI.

Injected process crashes and local fake clocks may test deterministic state logic where the task permits them. They do not prove kernel Job/cgroup cleanup or PTY lifetime. Those combinations require designated native hosts. A missing required proof leaves the corresponding profile/acceptance open; no failed cleanup is relabeled successful merely to remove the old runtime.
