# Sandbox filesystem and persistent data

Status: current V2 design. Owned storage and import/export are delivered by AFV2-FILE-01; safe deletion and interruption recovery by AFV2-FILE-02; existing-store migration by AFV2-DATA-01. Backend feasibility is qualified by AFV2-MXC-01 through AFV2-MXC-04. A Sandbox's data lifetime is independent of any one Run or MXC instance.

## 1. Data ownership and layout

The owner configures one absolute ArcForges data root before creating Sandboxes. A Node records the root's native object identity and owner when accepting it. Configuration validates that it is a real private directory, not a symlink/reparse redirect, filesystem root, another Sandbox subtree, a public temporary directory or a protected installation/credential path. It must not overlap another configured root. Existing directory permissions are checked, not inferred from a prior `CreateDirectory` result. A root move is an offline migration operation after Runs have stopped, not a live string replacement.

The host-managed layout is:

| Path relative to data root | Owner and purpose | Workload visibility |
|---|---|---|
| `store/` | Node database, backup metadata and migration state | Denied |
| `control/` | Supervisor endpoints, request/config files, Run ownership records and deletion journals | Denied; no ancestor grant may include it |
| `credentials/` or the selected external secret store | Node enrollment/identity data | Denied; never copied into Sandbox HOME |
| `sandboxes/<sandbox-id>/home/` | Persistent application home | Writable grant |
| `sandboxes/<sandbox-id>/config/` | Persistent conventional configuration | Writable grant |
| `sandboxes/<sandbox-id>/cache/` | Persistent conventional cache, treated as ordinary Sandbox data | Writable grant; no cache-type analysis |
| `sandboxes/<sandbox-id>/tmp/` | Persistent Sandbox temporary area, with optional per-Run subdirectories | Writable grant; retention is explicit |
| `sandboxes/<sandbox-id>/work/` | Default working directory | Writable grant |
| `sandboxes/<sandbox-id>/data/` | User's persistent Sandbox files | Writable grant |
| `sandboxes/<sandbox-id>/logs/` | Captured Run output and metadata written by the trusted owner | Ungranted by default; workload writes its own logs elsewhere |
| `staging/` | Bounded Node-owned import/export staging | Denied |
| `deleting/` | Private quarantine of exact owned Sandbox roots being removed | Denied |

The Node creates each Sandbox root with an exclusive create operation, private permissions/ACLs, a native identity record and a random ownership marker held outside workload authority. Sandbox IDs are opaque generated identifiers, not path components supplied by a remote caller. Names are display metadata and never substitute for IDs or filesystem identity.

Permissions enumerate writable child directories individually. Do not grant the data root, `sandboxes/`, the full Sandbox root, the user's real HOME or any broad ancestor as a convenience. A broad parent grant could expose controls/logs or other Sandboxes. The selected backend must actually deny or withhold those paths; setting environment variables alone is not isolation.

The old `StorePaths.CreatePrivateDirectory` only creates new Linux directories with 0700 and leaves existing ones unchanged, so V2 must add validation rather than treating it as proof of ownership: [source](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Store/StorePaths.cs).

## 2. What is collected, denied and explicitly outside the guarantee

ArcForges supplies conventional locations for programs that honor HOME/config/cache/temp variables. It does not transparently rewrite every arbitrary path that an application chooses. The profile's actual filesystem policy defines the guarantee.

| Access | V2 rule |
|---|---|
| Writes under the explicitly granted owned child directories | Allowed and retained with the Sandbox |
| Writes under an explicit external writable grant | Allowed only within that grant; remain external user data, excluded from Sandbox deletion and size total |
| Reads of admitted executable/runtime/system dependencies | Allowed via the profile's explicit read grants/default system prerequisites; no implied write authority |
| Writes to ungranted host paths | Denied by the selected backend; required denial is tested, not assumed |
| Access to Node database, credentials, control directory or other Sandbox roots | Denied even if a caller asks for a broad grant that would include them |
| Program ignores HOME/XDG/TMP and uses a hard-coded host path | Its operation fails unless that path is explicitly authorized; no redirect promise |
| Network downloads saved to a granted directory | Ordinary Sandbox data; network authorization is separate |
| Host services, external daemons or already-running brokers contacted by the workload | Their effects are not automatically owned Sandbox writes; admission/network/IPC policy must not advertise such external effects as confined |

The first supported profiles expose owned directories at their actual absolute host paths. The stable typed V1 path-grant API compiles Linux binds as source path to the same target path; it does not provide user-authored source-to-different-target aliases. Windows ProcessContainer authorization likewise provides no general path rewrite. See the pinned [MXC research](../research/mxc-research.md). Do not promise `/work` remount aliases or Windows known-folder virtualization. The backend compiles grants; the public API describes read/write authority, not raw bubblewrap arguments or Windows ACL recipes.

On Linux, set HOME, XDG_CONFIG_HOME, XDG_CACHE_HOME, XDG_DATA_HOME and TMPDIR to the admitted private directories; set TMP/TEMP where appropriate. On Windows, set HOME, USERPROFILE, APPDATA, LOCALAPPDATA, TEMP and TMP to the corresponding admitted directories when the backend/application honors them. Some programs query OS known-folder APIs rather than environment variables. Such programs may need explicit allowed paths or may fail; the Design does not label environment changes as transparent filesystem redirection.

All final environment values come from the validated start snapshot. Do not inherit the entire Node environment. Start with a minimal platform allowlist for executable resolution and terminal locale, then Sandbox values and explicitly allowed per-Run overrides. Protect ownership/control/backend variables against override. Secrets are explicit values authorized for the workload and excluded from receipts/logs; no Node/Center token is inherited. Command-line arguments themselves may contain secrets and therefore are not general telemetry fields.

## 3. Filesystem grants

Each `HostGrant` carries the canonical host path, same-path backend presentation, writable flag and Node-resolved native identity. The containing Sandbox configuration revision and owner authorization bind the complete grant set; private implementation records may assign grant identities for reconciliation. Paths are resolved on the target Node, never on Center. The owner reviews the actual canonical target and access mode. A remote action cannot create a host-wide writable grant by embedding a new path in `RunService.Start`.

Grant creation/configuration is an explicit Sandbox configuration mutation using `expected_revision`. Validate the complete resulting configuration atomically. Reject overlapping grants that weaken a denied/control boundary, mixed identities after canonicalization, unsupported remapping, link traversal into another target, unsupported filesystems and mount targets that hide required controls. Record the granted source identity, not merely the current path spelling. At each Start, reopen/recheck the grant target and refuse if identity or access changed.

A running Run uses an immutable grant/profile snapshot. Path, network, profile and identity changes require no nonterminal Run; this prevents an existing process from retaining a grant the user believes revoked. Ordinary non-access metadata changes apply to later Runs. Live resource changes use the separate versioned resource-policy operation. An access-revocation workflow explicitly stops and drains affected Runs before committing the new configuration. No hot path-grant or network-policy mutation is promised by the initial profiles.

External grants are never adopted as owned data. `SandboxService.Inspect` and `DataService.GetUsage` show owned data and external granted paths separately. Export includes owned selected data only unless the owner explicitly requests an external-file copy as a separate import. Delete unmounts/detaches grants after Runs end; it does not recursively visit or erase their sources.

## 4. Size observation

`DataService.GetUsage` returns the current timestamped `Usage` summary: owned logical bytes, observed allocated bytes where supported, regular-file count, partial flag and excluded external roots. An incomplete scan is not zero usage. Scan by opened owned root and no-follow traversal; stay on allowed volume/device boundaries. Symbolic links/reparse points contribute their own entry cost only and are not followed. Hard-linked content is counted under a documented convention (logical bytes per directory entry; allocated-byte deduplication is optional only within a single scan and must be labeled).

Use a bounded asynchronous internal scan with cancellation and entry/byte/time limits. The Node retains its scan progress privately; `GetUsage` returns the latest partial or complete aggregate without holding a request open for a whole large tree. `DataService.ListEntries` separately provides bounded, paginated entry metadata. Scans do not monopolize the Node writer or terminal control slots. No classification of compiler caches, hit rates, dependency caches, CAS deduplication or general disk garbage is implemented. The space view is an observation of this Sandbox's owned data.

## 5. Import

The initial import contract transfers one regular file: `DataService.BeginImport` authorizes the destination and reserves staging space, `WriteImport` transfers bounded contiguous chunks, and `CommitImport` performs the guarded effect with a recorded operation ID. `CloseTransfer` releases a completed/cancelled transfer when doing so is safe. Local CLI sources are local to the initiating CLI; a remote-target command and Web upload carry bytes, never a server-side instruction to read an arbitrary host path. Do not treat remote path strings as trusted file handles.

`BeginImport` identifies Sandbox ID, expected Sandbox revision through request metadata, destination relative path, declared length, SHA-256 digest and explicit `overwrite` (false by default). Overwrite requires the currently observed `expected_file_version`; a pathname alone does not authorize replacement. Reject absolute paths, `..`, reserved control names, platform-invalid components and case-fold collisions. The initial contract does not unpack archives or create links/devices/sockets. An archive is an ordinary file until a user explicitly runs a program to unpack it inside the Sandbox.

Before transferring, verify Sandbox state and the exact owned destination root; active Runs may read/write imported paths, so the initial release performs mutating import only while no nonterminal Run exists in that Sandbox. If live import is later admitted, it needs an explicit conflict/visibility contract, not a bypass of this rule.

Reserve bounded disk capacity; stream to a private staging directory that the workload cannot access. Verify declared length and digest, reject excess data before committing, flush content and durable intent, and move the staged file within the same owned filesystem using the platform's guarded operation. Writes use the transfer's verified contiguous offset; an identical replay is accepted, and conflicting replay is refused. A client that transfers several files coordinates a sequence of independent per-file transfers and receipts; there is no filesystem-wide atomic transaction. It must show completed, refused and uncertain items separately. A retry with the same operation ID resolves the same durable receipt and cannot overwrite a different target.

For overwrite, recheck the native target identity/version immediately before effect; a changed target returns `CONFLICT/identity_changed`, leaving the existing file intact. An unknown post-effect result is reconciled from the held identities/journal; it is never blindly repeated. Partial unused staging is safe to remove only when its ownership and worker termination are confirmed.

## 6. Export

`DataService.BeginExport` selects one regular file by owned-root-relative path and optional observed file-version token, under an expected Sandbox revision and local transfer-size limit. The initial release requires no nonterminal Run and no conflicting file mutation. The Node produces a private immutable transfer snapshot, verifies its length/digest and exposes it through bounded `ReadExport` chunks; `CloseTransfer` releases it. A client exporting several files coordinates separate transfers. Live export and whole-directory snapshot consistency are outside this initial contract.

Create the export snapshot by opening the source without following links/reparse points, retaining its identity and verifying unchanged identity/size/stamp at the end of the copy. A concurrent host-side change fails the snapshot rather than returning a mislabeled digest. Do not expose Node controls, Node secrets, external mount contents or paths outside the selection. Browser download authorization is short-lived and bound to account/device/Sandbox/operation; no public reusable URL or unbounded retained cloud copy is created. Local export checks the destination and uses explicit replace behavior; it never silently overwrites a host path.

Exports may include application secrets stored in the selected user data. The UI clearly identifies the selection before authorization and transport is encrypted. Audit records contain IDs, counts, sizes, digests and outcomes, not file contents. Exclude stdin/credential material from automatic support logs.

## 7. Safe whole-Sandbox deletion

Deletion has a `SandboxService.PlanDelete` preview and a bounded `SandboxService.Delete` effect operation. The plan names the exact Sandbox revision, owned root identity, active/reconciling Runs, external grants that will be detached, owned-data size estimate, and any protection/error that prevents deletion. It never asks the user to approve an opaque arbitrary host command. `Delete` consumes the unexpired plan ID with its operation ID; destructive remote deletion additionally requires the configured remote-delete permission and a fresh owner action.

The mutation sequence is:

1. Under the Node single writer and common admission lock, confirm the plan revision, root identity and expiry. If any Run is STARTING, RUNNING, STOPPING, DRAINING or RECOVERY_REQUIRED, or a transfer/effect still holds managed use, return `STATE/managed_use` without changing the Sandbox state. Otherwise transition to DELETING and refuse new Starts/configuration/imports. Delete does not auto-kill a Run as an undocumented side effect.
2. Verify every prior Run resource scope is empty of workload descendants and no supervisor/effect worker still owns a data handle requiring protection. A root-process exit or executor exit alone is insufficient.
3. Reopen the private parent and root by native identity, verify owner marker and exact ownership. Refuse changed identity, root links/reparse points, foreign mounts/volumes, protected descendants or ambiguous origin. Lexical path-prefix checking is not sufficient.
4. Persist the delete intent before destructive effects. Detach recorded external grants without traversing their targets. Move the exact owned root into private deletion quarantine using a native guarded operation supported and qualified on that platform. If the guard cannot exclude unsafe movement, refuse before the effect.
5. Delete only entries reachable beneath the held quarantined root using no-follow traversal and bounded batches. Do not cross mount points or follow hard-link targets. Recheck ownership and type at the effect boundary; record progress/errors durably.
6. When the actual owned root is gone and all worker handles are released, finalize the Sandbox tombstone and retained audit receipt. The tombstone permits idempotent replay without recreating the Sandbox. Free database metadata only according to the specified retention policy.

A bounded recoverable deletion failure leaves DELETING with durable progress and a typed reason; uncertain ownership or possible effect moves the Sandbox to RECOVERY_REQUIRED. Use the shared error catalog (`CONFLICT/identity_changed`, `STATE/managed_use`, `VALIDATION/path_rejected`, `AUTHORIZATION/permission_denied`, `RESOURCE/disk_space` or `EXECUTION/outcome_unknown`) with a bounded specific detail. The user can inspect and resume reconciliation safely. An operation cancelled after destructive progress cannot truthfully restore the old READY state; it reports partial effect and continues only through explicit safe resume. Before the quarantine effect, cancellation can return to READY after confirming no effect and releasing the deletion lock. Data is not declared deleted until the effect is confirmed.

There is no automatic recursive `Directory.Delete(dataRoot)` path. An attacker-created link/reparse swap, stale path or same-user mutation cannot authorize deletion of another Sandbox or host directory. The required boundary is owned private Sandbox data with native identity and exclusion; arbitrary hostile host-tree cleanup is outside this product.

## 8. Reuse and existing-data migration

The historical file-effects implementation already contains substantial native identity, staging, full-durability journal and worker-exit mechanisms; its delivery evidence is catalogued in the [runtime audit](../research/runtime-audit.md). Extract relevant primitives after reviewing their assumptions; remove the old Center-routed general workspace editor/searcher and Agent-owned cleanup policy. Existing creation records are evidence, not permission:

- [FileCreationOwnership](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Files/FileCreationOwnership.cs)
- [AttemptTempProvenance](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Execution/AttemptTempProvenance.cs)
- [WorkspacePath native traversal](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Platform/WorkspacePath.cs)
- [FileMutationJournal](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Files/FileMutationJournal.cs)
- [Current store migration history](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Store/Migrations/StoreMigration.cs)

AFV2-DATA-01 preserves immutable schema steps 1–15, freezes old writes, reconciles unresolved file workers/journals/holds, makes a durable backup, appends V2 tables and later contracts away retired active tables with a higher minimum reader version. Do not automatically convert registered host workspaces or cache roots into Sandbox-owned roots. Legacy data can be explicitly imported by copy, preserving source files. Unresolved effects block destructive migration, not read-only inventory/export.

## 9. Native acceptance

Test on designated native Windows/Linux hosts using disposable roots and known foreign sentinels. Required positive cases are persistent state across repeated Runs, correct program conventional directories, successful bounded import/export, accurate partial size scans, normal owned-root deletion and recovery from each durable deletion phase. Required negatives include unauthorized host writes, symlink/reparse/`..` traversal, case collision, root/ancestor swap, external mount traversal, changed target during import, active/background descendants, PID reuse, disk full, lost worker acknowledgment and cancellation after a possible effect.

Assertions must inspect the actual foreign sentinels and ownership identities after operations. A refusal proves refusal only; it does not prove the positive deletion path. No indefinite probes or invented guarantees are added beyond these defined acceptance boundaries. If a required native guard is unavailable, the operation fails safely and its positive acceptance remains open in the Plan.
