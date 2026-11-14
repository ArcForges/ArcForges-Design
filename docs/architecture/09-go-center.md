# Go Center and remote management

Status: V2 target design. The existing Go identity, enrollment and channel are reusable implementations; the Sandbox/Run APIs and Dashboard described here are not yet delivered. Implementation owners: `AFV2-CENTER-01` through `AFV2-CENTER-03`, with contracts from `AFV2-API-01` and migration qualification from `AFV2-MIG-01`.

## 1. Responsibility and composition

The Center authenticates people and nodes, registers devices, authorizes remote management, routes typed requests and provides bounded status delivery. The Node's Sandbox Core is the sole authority for local execution, isolation, resource policy, filesystem access and Run state. The Center has no host-shell endpoint, scheduler, task-dependency graph, automatic execution retry or AI-specific command interpretation.

The same Go binary serves self-hosted and official-hosted installations. PostgreSQL is the business store. The official deployment retains its existing Cloudflare Worker/Container ingress; the Worker performs platform transport duties and consumes route/budget tables generated from Go registrations. It makes no subscription, authorization or Sandbox policy decision. A self-hosted Center can run behind the operator's TLS reverse proxy without Cloudflare, Neon or an official account.

Blazor WebAssembly serves the management UI as static assets. It calls the Center, never a private Node port. Existing Center-owned sign-in, passkey, session, device and enrollment pages remain usable for headless/self-hosted enrollment. Recovery/account deletion/export are unregistered gaps at the audited baseline, with required V2 completion owned by `AFV2-ID-01` (`R-CTR-004`); they are not reusable finished pages. There is no second ASP.NET business server.

| Component | Authoritative state | Must not own |
|---|---|---|
| Sandbox Core | Sandbox configuration, grants, Runs, resource policy, local data and durable command outcome | Subscription or official-server availability |
| Go Center | Accounts, device enrollment, credentials, remote command routing receipts, hosted entitlements, commerce and audit | Executable Run lifecycle or authoritative local resource limits |
| Channel hub | Current proved connections, bounded in-flight calls, live telemetry subscriptions | Durable work queue or disconnected command delivery |
| PostgreSQL | Center state, audit and content-free routing receipts | Command output, environment values or a copy of Sandbox files |
| Blazor | Current view, unsent forms, short-lived opaque cursors | Authorization decisions, signing keys or persistent bearer secrets |
| Worker | Route admission, transport framing, bounded forwarding and platform lifecycle | Business retries, contract conversion or business persistence |

The existing implementation's singleton fenced hub lease is retained for the initial V2 release. One database has one active channel owner. A standby must not accept Node channels while another owner holds the lease. Horizontal routing/sharding is outside the V2 delivery plan; the release must state the measured connection/call capacity of this deployment model.

## 2. Trust and request path

1. The browser obtains a same-origin cookie session and CSRF value through the existing strict browser session contract. Every unsafe browser request validates CSRF and exact origin. Native Node tokens are never accepted as browser account sessions.
2. Center ingress checks registered route, framing, size/deadline and session. Unknown routes are denied. The operation table checks account state, target ownership, required operation scope, rate/concurrency limits, audit admission and hosted entitlement.
3. The Center resolves the exact live enrollment, current channel generation and declared V2 capabilities. An unknown, foreign or revoked Node returns the same `not_found` shape. A disconnected Node returns `node_offline` without queuing work.
4. The Center sends a signed typed request bound to the configured Center audience, account, enrollment, Node, method, request digest, caller, expiry and command identity. The authenticated channel is an additional boundary; it does not replace message binding or local policy checks.
5. The Node verifies the Center/enrollment and request, checks the current local remote grant, invokes the same Sandbox Core operation as the CLI and returns a signed result. A valid Center signature never grants broader filesystem, network, resource or execution authority than local policy.
6. Center verifies the result's channel/operation/method/digest binding and forwards the typed response. Browser success follows the Node's committed result; an HTTP 200 or a written WebSocket frame is not execution success.

Ordinary Cloud operators can administer service health and billing without an automatic right to read Run output, import files or execute programs on a user's Node. Access to those operations requires the same account and locally granted remote authority as any other caller.

## 3. Enrollment and channel lifecycle

Reuse the implemented browser loopback/PKCE flow and device-code flow. Keep one-use code semantics, Node key proof, strict refresh-token rotation, credential-family revocation, step-up on enrollment approval, origin/audience binding and prevention of cross-account Node reuse. Device-code polling is a sign-in mechanism for a generic CLI, not a mobile product dependency.

The V2 channel uses a separate protocol version and signature-domain strings. It does not reinterpret `relay.v1` task enums as Sandbox operations. Capability negotiation states the protocol/cohort, OS/backend, supported operations and terminal/resource restrictions. It reports proof status for the complete admitted backend/profile combination: individual MXC and OS features do not establish that their composition works. Unknown mandatory capabilities fail with `upgrade_required`; unsupported or unproven combinations disable the affected operation with a precise reason and no weaker fallback. Platform capabilities, including ingress limitations, are independent of hosted/self-hosted subscription mode. The final V2 runtime serves no old Task/Fleet file routing endpoint.

| Channel condition | Center behavior | Node behavior |
|---|---|---|
| Enrollment accepted, remote grant disabled | Registry may show the device; channel may expose only the approved availability summary | No Sandbox detail or control is admitted |
| Token and Node proof valid | Accept one channel per enrollment and replace an older connection under a new generation | Start heartbeat/reconnect loop; do not start a Run |
| Heartbeat deadline or transport lost | Mark status stale/offline; settle delivered mutations conservatively | Continue local Runs under local policy; reconnect with jitter |
| Center entitlement expires | Refuse further hosted remote calls and close hosted channel after the documented recheck interval | Keep local execution and local CLI available |
| Credential or device revoked | Fence new requests, close channel and invalidate pending stream grants | Discard remote session credentials; preserve local data and Runs |
| Node local remote grant revoked | Refuse affected operations; close affected subscriptions | Revoke immediately in Core; no server acknowledgement is needed |
| Center restart or lease loss | Close owned channels, fence routing, recover uncertain receipts before serving | Reconnect and publish a fresh snapshot; no replay of terminal input |

Reuse the current bounded challenge, heartbeat, send queue, frame rate, in-flight count and lease mechanisms. Their release values are implementation limits, not paid quotas. Expose accepted limits in negotiation; test the configured upper bounds and deny excessive settings. Retain fail-closed behavior when signing-key freshness cannot be established. No credentials, commands, file contents or terminal bytes enter transport logs.

## 4. Public management operations

The core contract namespace is `arcforges.sandbox.v2`. Services are `NodeService`, `SandboxService`, `RunService`, `ResourceService` and `DataService`; cloud device registration is `arcforges.management.v2`. Local and remote calls have the same Core request validation and result semantics. The remote envelope identifies a Node/enrollment and admits only the explicitly registered remote methods; it is not a generic method-name/JSON/host-command tunneling API.

| Service/action group | Remote permission | Local policy and result |
|---|---|---|
| Node list/inspect, last-seen and enrollment revocation | Account device management; essential security remains available after subscription lapse | Registry data only; live resource/Sandbox detail additionally needs a local view grant |
| Sandbox list/inspect | `view` | Redacted configuration, revision, data usage and supported operations; no secret values |
| Sandbox create | `configure` through a local `provision` grant | Request carries `provision_grant_id` and immutable template revision; its complete configuration must equal or narrow the local creation template; no arbitrary Node-wide creation authority |
| Sandbox configure | `configure` through a Sandbox-scoped grant | Root and host mounts remain within the local envelope; `meta.expected_rev` prevents lost updates; configuration never expands remote authority |
| Sandbox deletion plan/execute | `delete` plus a fresh operation-bound approval | Core refuses active Runs or unsafe ownership; plan binds revision/object identity; delayed or changed plans are refused |
| Run start | `run` | Exact executable/arguments within an existing authorized Sandbox; admission uses current resource and isolation policy |
| Run inspect/list/log read | `view` / `logs` | Stable Run ID, outcome, cursor bounds, redaction and explicit truncation/gap markers |
| Run stop | `stop` | Targets one owned Run and its managed descendants; Core defines graceful timeout and escalation; does not terminate unrelated host processes |
| Resource observation | `view` | Timestamped CPU/memory/pressure samples plus requested, effective and verified limits; unavailable values are not zero |
| Resource policy changes | `resources` | Restricted to locally authorized ceilings and current revision; Core handles rejection or partial backend application |
| Data import/export and size | `data` | Only Sandbox-relative owned paths; bounded streams and byte limits; no generic host file edit/search API |
| Operation reconciliation | Original operation's read permission | Query by `command_id`; does not execute, retry or invent a replacement command |

The precise generated names and wire fields live in the V2 API specification. This table defines required authorization and routing behavior and must be checked against that catalogue, not maintained as an independent list of implemented methods.

Local grants default off. An enrollment can display the locally approved policy to the user and request a local enablement action. Only a local authenticated owner may create or edit a grant, authorize a host path, change the data root or expand a resource ceiling. V2 exposes typed remote grant revocation; re-enabling or editing a grant uses the local CLI. Remote configuration/resource actions may narrow settings within their existing grant but cannot restore revoked authority. Grants bind the Center's configured audience and exact enrollment, so signing in to another Center does not inherit permissions.

Creation authority must exist before a Sandbox does. A locally created grant with `scope_kind=provision` has no Sandbox ID and instead contains a complete immutable `creation_template` and `template_revision`. Remote `SandboxService.Create` names that grant and revision; Core checks the requested configuration is equal to or narrower than the template, including mounts, network permissions and resource ceilings. It atomically records the created Sandbox and its derived Sandbox-scoped grant, limited to the parent authority. A regular `scope_kind=sandbox` grant requires an existing Sandbox ID. Only local `NodeService.SetRemoteGrant` may create or widen either grant type. A remote caller cannot mint a provisioning grant, substitute a broader template, or gain control of other Sandboxes through a creation request. Template replacement/revocation invalidates subsequent use of the old revision; replay of an already completed command only returns its existing result under current read authorization.

## 5. Idempotency and uncertain outcomes

Every mutation carries a nonzero `command_id`. A command is bound to `(account, enrollment, protocol, method, command_id)` and a canonical intent digest. Canonical intent includes target IDs, configuration revision and payload fields that change the effect; it excludes transport correlation, deadlines, step-up evidence and reissued signatures. Signed transport digests separately cover the exact transmitted bytes. The API contract defines the canonical digest bytes and C#/Go golden vectors.

Center admission reserves the command in PostgreSQL before it can be delivered. The Node keeps the durable Core receipt and resulting IDs. A matching replay returns or reconciles the original effect; a different intent with the same identity is `command_id_reused`. Account ownership and current permission are rechecked before a replay reveals an old result. Expired authorization is never refreshed by replaying a command.

| Routing state | Evidence | Permitted recovery |
|---|---|---|
| `ACCEPTED` | Durable admission; delivery may not yet be known | Treat as possibly delivered after a crash |
| `NOT_DELIVERED` | Transport proves no delivery in this or any prior attempt | Caller may explicitly retry the same command under fresh authorization |
| `SUCCEEDED` / `FAILED` / `REJECTED` | Verified Node result with terminal outcome | Return/query the same result; never execute a new effect |
| `UNKNOWN` | May have reached Node; no verified terminal result | Query `NodeService.GetOperation(command_id)`; preserve identity and show uncertainty |
| `EXPIRED` | Delivery or replay validity ended | Refuse execution; explain whether earlier effect remains unknown |

The browser never automatically retries a mutation after timeout, disconnect, reload or an unknown effect. It preserves the command identity for reconciliation. Explicit retry is limited to a proven `NOT_DELIVERED` or the contract's same-command recovery path; it never silently replaces the command ID. A state read can be retried with bounded backoff. This command protocol is transport reliability, not the cancelled Task/Attempt automatic-retry system.

Receipt retention and tombstones prevent a deleted record from making a previously executed command look new. Node deletion or re-enrollment changes the enrollment epoch and invalidates old authority. Run identifiers and command histories are not transplanted into a different Sandbox or device. Details and migrations are in [Cloud store](../data/cloud-store.md).

## 6. Status, resources and log delivery

The initial Dashboard uses bounded unary reads and capped long polls over the existing binary gRPC-Web/Connect infrastructure. Nodes retain their one outbound channel. Do not introduce an unbounded viewer relay or a second stateful WebSocket hub solely for charts. A Run can outlive every RPC deadline.

Each Node boot/channel snapshot has an epoch and monotonically increasing sequence. A response includes `observed_at`, `received_at`, epoch, sequence and freshness. Center forwards requested detail while the viewer is authorized; it does not permanently collect all filesystem paths or Run output. Registry last-seen data may be persisted; cached live summaries remain bounded and explicitly stale after disconnect.

Pagination and output cursors are opaque, target-bound, versioned and length-bounded. Log cursors also bind Run/output epoch and byte position. A stale cursor returns `cursor_expired` with an available starting point; deleted or evicted data returns an explicit gap. No offset is silently reset to zero. Each read declares maximum bytes and wait duration; Core and Center both cap them. Cancellation of a read releases a call slot and does not stop its Run.

The Node never waits for a browser to consume output before draining a managed process's terminal/stdio. A bounded local spool and ring policy governs disk use and records truncation. Slow viewers receive gap markers or disconnects without changing Run lifetime. Details are fetched only on demand. Log rendering treats text as untrusted data: no HTML interpretation, external link auto-navigation or terminal escape execution in the ordinary log view.

TTY ownership stays in Sandbox Core. V2 terminal attach, detach and input are local CLI operations only. The Dashboard's scope is launch, stop, status and log viewing. The Center allowlist excludes terminal attachment/input methods; no browser terminal interface, grant or alternate execution path is created.

## 7. Offline, revoke and failure behavior

Center/database/provider outage must have no path to the local process supervisor's stop decision. Local runs and local resource pressure response continue. A Node does not start disconnected remote commands when it reconnects. A lost Center reply to a Run start leaves a reconciliable operation, never a second Run on reconnect.

Subscription failure is confined to the official remote service. Account sign-in, security remediation, device revocation, billing status and cancellation remain accessible. Self-hosted operation makes no request to an official subscription service. Center maintenance/abuse limits may refuse traffic in either mode and must say `operator_limit` or `overloaded`, not pretend that a self-hosted user needs a paid plan.

HTTP/protocol failures preserve the common error category, retry/effect classification and correlation identity. Required reasons include `node_offline`, `node_unreachable`, `permission_denied`, `remote_disabled`, `upgrade_required`, `revision_conflict`, `command_id_reused`, `operation_unknown`, `cursor_expired`, `resource_unavailable` and `overloaded`. Error details contain no unauthorized target names, secret values or payload bytes. Unknown OS outcomes remain unknown until Core reconciles them.

## 8. Implementation and deletion sequence

1. `AFV2-API-01`: publish the new contract cohort and C#/Go compatibility vectors. Keep prior artifacts resolvable.
2. `AFV2-MIG-01`: inventory deployed schema/artifact identities; qualify fresh/schema-10/schema-11 paths, backup/restore and finite rollback boundaries. The current `RequireCTR06SecurityBridge` hard stop must be resolved through a reviewed V2 successor; it is not a flag to bypass.
3. `AFV2-CENTER-01`: adapt identity, registry and channel capability negotiation; create V2 data grants/receipts while preserving account and key identity. Keep product surfaces dark.
4. `AFV2-CENTER-02`: register and implement the typed remote mutations and queries, local grant checks and uncertain-outcome reconciliation against real Sandbox Core.
5. `AFV2-CENTER-03`: implement bounded status/resource/log delivery and revoke/backpressure/failure behavior.
6. After all consumers have moved, remove Go `fleetapi` task/file/workspace routing, old routed-method enums from active composition, mobile pairing/auth routes, product MCP/AI seams and the C# Center/D1/proof-runtime composition. Keep historical migration inputs and immutable public artifacts as evidence; they are not executable legacy services.

Retain reusable Go `identity`, `session`, `device`, `entitlement`, `access`, `ingress`, `platform`, `store`, `observe`, `quota` and cryptographic/channel primitives. Refactor domain vocabulary rather than rebuilding their guarantees. Do not delete `DesktopPlatform` ContentSandbox or independent product contracts merely because their names include sandbox or AI.

## 9. Acceptance

Real native Windows and Linux Nodes must be controlled through an actual Go Center backed by real PostgreSQL. Exercise both self-hosted and official-mode policy with fixture plan data clearly identified as fixtures. Browser integration is explicit local acceptance, not new hosted browser CI.

Required scenarios: local start with no Center/account; wrong account and revoked grant denied; correct Sandbox start and stop with descendant cleanup; duplicate command before/after each persistence/send boundary; Center crash after delivery; Node crash during admission; lease takeover; signing-key rotation; schema upgrade/rollback and role fencing; stale/evicted log cursor; slow output viewer; session/entitlement expiry mid-read; grant revocation; offline local continuation; unsupported backend operation; resource requested/effective mismatch; malformed/oversized frames; and real Web-to-Center-to-Node operation on both OSes. Missing external provider or hosted evidence remains separately `NOT PROVEN` and is owned by the hosting acceptance task; it does not masquerade as an executed test.

Source baseline and evidence limitations: [Cloud/Web/Contracts audit](../research/cloud-audit.md).
