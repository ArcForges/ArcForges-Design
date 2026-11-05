# 11 — Security and privacy

**Amended 2026-10-28 (target; AF-CTR-03 to AF-CTR-07) by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §7, §10, §11.** Boundary B4 (node ↔ cloud) becomes node ↔ center: the node's outbound connection with its node credential carries center-routed calls whose caller identity and origin the center verified; central authorization never bypasses node policy. A third credential kind, the agent grant, gives AI clients origin AGENT; it never yields HUMAN power and never approves its own requests. What passes through the center and what it keeps is the table of AD-0021 §10: task specifications, output and file contents only transiently, never persisted. Routed calls stay signed end to end (T-11; AD-0021 §10): the center signs, the node verifies signature, target and expiry before its policy decides. Boundary B3 (node ↔ node) and data class D4's LAN peers are out of current delivery.

## 1. Origins and permissions (local)

The node classifies every API call by **origin**. The connection's client kind is verified, and process ancestry is checked against registered agent roots ([08](08-ai-integration.md) §3).

| Origin | Determined by |
|---|---|
| `HUMAN` | Desktop connections; CLI processes **not** descended from a registered agent root and attached to an interactive terminal (the console or pty is checked by the CLI and reported in the hello; spoofable, see below) |
| `AGENT` | MCP adapter connections; hook handler; CLI processes descended from an agent root or carrying `ARCFORGES_SESSION` |
| `SCRIPT` | CLI not under an agent root and without a terminal (CI, scheduled scripts) |
| `REMOTE` | Signed relay commands (§3). AF-CTR-05 target: center-routed calls, signed by the center and verified by the node, with the center caller the center verified ("Center-routed callers" below) |
| `PEER` | LAN peers (mTLS identity) |
| `GUEST` / `HOST` | Retired 2026-10-21 by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) (formerly the guest link counterparts); never assigned |

**Origins are guardrails, not a security boundary** ([AD-0007](../decisions/AD-0007-ai-integration.md) §8). Every local client runs as the same user as the node, so a determined same-user process can present itself as another origin. Documented bypasses:
- **Looking interactive.** A process can allocate a pseudo-terminal (or console) so that the CLI reports an interactive terminal.
- **Escaping ancestry.** A process can be re-parented, for example through a detached launcher or a scheduled task, so that it no longer descends from a registered agent root.
- **Direct writes.** A same-user process can edit the node store and `node.json` directly. The node detects such edits (tamper finding `ENFORCEMENT_DEGRADED`) but cannot prevent them.

The matrix therefore protects against accidental and casual misuse by AI clients, and the tests cover what holds: classification of the supported clients, approval routing and audit (R-AI-009).

**Same-user limits beyond origins** (bypass catalogue, added 2026-10-19). Release 1 confines no workload: managed processes, the AI clients and the node run as the same user. The following are documented bypasses, never claimed impossible:
- **Container tampering (T-22).** Same-user code can change the limits of ArcForges' containers or end other attempts. Named jobs and the ack event carry the default security descriptor, so other processes of the user can open them (V-W11), and Linux attempt units and their cgroups belong to the user's own user manager (V-L01, V-L05). Every resource guarantee is therefore ENFORCED against accidental and over-privileged workloads, and a GUARDRAIL against workloads that target ArcForges' objects ([03](03-resource-control.md) §5).
- **Leaving the container (T-23).** Work launched outside the recorded ancestry, through WMI, a broker, a service, a scheduled task or a spoofed parent, never joins the attempt's container (V-W01, V-W10). The ancestry scan detects only descendants whose recorded ancestry passes through a job member, so such work is not detected and appears as `UNMANAGED` ([03](03-resource-control.md) §9; A-W04).
- **Routing out of a client sandbox (T-24).** Commands routed through ArcForges (MCP `run`, hook rewrites) gain resource control and records, but run outside the client's own sandbox. The client's own process, with its hooks, its MCP servers and, for Claude Code, its file tools, keeps the user's full access (V-A03, V-A06; A-A03; [AD-0007](../decisions/AD-0007-ai-integration.md) §4). The per-client wording is the routing rows of the [product definition](../product/product-definition.md) §9.
- **Same-user secret reach (T-25).** The OS secret stores protect the node's secrets from other users, not from the user's own processes (§3).
- **Privileged changes without ArcForges elevating (T-26).** ArcForges never elevates ([AD-0005](../decisions/AD-0005-resource-enforcement.md), Process model), but an unconfined workload can obtain a privileged change through the OS. The channel catalogue:
  - **Linux system bus:** requests that polkit authorizes are not stopped by no-new-privileges, and distribution rules can authorize package installs for active administrator-group users without a prompt (V-L08).
  - **Windows sudo:** it elevates only through UAC, and Microsoft warns that it can be a potential escalation-of-privilege vector in some configurations; the inline mode is one (V-W09).
  - **UAC on administrator accounts:** on an administrator account without Administrator protection, UAC is not a security boundary; unconfined workloads may obtain administrator rights silently (V-W07, V-W08).

  The host's own account type and Administrator protection state are D2 host posture (§5): only the doctor's HUMAN-only host-posture check reports them ([07](07-records-diagnosis-memory.md) §2.4), never the release coverage statement or the MCP adapter.
- **Paired peers (T-27).** A paired peer with placement rights executes code as the local user. Per-peer command patterns are argument-vector filters, which are guardrails ([09](09-lan.md) §4).

Default permission matrix (policy `permissions`, editable only by `HUMAN`).
- **Key.** A = allow; P = approval required (an approval request is raised and the call fails with `AUTHORIZATION/approval_required`, carrying the approval ID); D = deny.
- **REMOTE column.** It names the `fleet.v1.NodeCommandBody` kind and its risk class. The cloud requires step-up for medium and high, and the node's remote-control policy decides last (AD-0009 §5). Anything without a command kind is denied remotely. The RPC annotations carry the same class (`REMOTE=…`; [contracts](../contracts/README.md)).
  *Amended 2026-11-05 (AF-CTR-05 target; Plan decisions Q6 and PB-1):* the command kinds of the REMOTE column below stay as history for the unserved `SendNodeCommand`. The six center-routed task methods are REMOTE rows of their own, without command kinds, in the table "Center-routed operations" below, which also records the center's `mobile.limited` and step-up rules for them; "anything without a command kind is denied remotely" holds for every other operation. The step-up sentence above holds for the routed methods of medium and high class. For them the node's center-routed policy decides last, not its remote-control policy ("Center-routed callers" below).

| Operation | HUMAN | SCRIPT | AGENT | REMOTE (command kind, class) | PEER |
|---|---|---|---|---|---|
| Submit task (own) | A | A | A (subject to `agent.allowed_command_patterns`, default all) | `run_task` (high) | A (per peer policy) |
| Read tasks, records, resources | A | A | A (own session's tasks in detail; others as summary) | Only the status summaries the node publishes: `refresh` (low); detail per privacy policy | status only |
| Read an output tail | A | A | A (own session) | `read_output_tail` (low; privacy policy `remote_output_tail`, default off) | D |
| Cancel own task | A | A | A | `cancel_task` (medium) | A (own remote attempts) |
| Cancel others' tasks | A | P | P | `cancel_task` (medium) | D |
| Change a task's priority | A | A | P | `set_priority` (medium) | D |
| Pause or resume a pool | A | A | P | `pause_queue`, `resume_queue` (low) | D |
| Change parallelism | A | P | P (A when lowering its own session's limit) | `set_parallelism` (high) | D |
| Change other policy, create or delete pools | A | P | P | D | D |
| Decide an approval | A | D | D | `decide_approval` (high; node policy `remote.allow_approvals`) | D |
| Plan cleanup | A | A | A | D | D |
| Execute cleanup | A | P | P (A for low-risk only if `cleanup.agent_execute=LOW_RISK_ONLY`) | D | D |
| Adopt or terminate a process | A | P (terminate) / D (adopt) | P (terminate) / D (adopt) | D | D |
| Integrations, pairing, account sign-in | A (interactive) | D | D | D | D |
| Stop the node, apply an update | A | A | D | `stop_node`, `apply_update` (high) | D |
| Roll back an update | A (interactive) | D | D | D | D |
| Apply remedy | per remedy class | per remedy class | P | D | D |

**Approvers** must be `HUMAN` (Desktop, interactive CLI), or `REMOTE` through `decide_approval` with step-up and the node policy `remote.allow_approvals=true`. Every privileged or remote action is audited (R-SEC-002).

**Operation names** (added 2026-10-23, AF-SEC-01). The policy `permissions` overrides and `ExplainPermission` name operations by these keys. Rows marked *annotation* are not in the matrix above; their defaults come from the RPC annotations of the contract. *Fixed* operations cannot be overridden.

| Operation | Matrix row | HUMAN | SCRIPT | AGENT | Fixed |
|---|---|---|---|---|---|
| `task.submit` | Submit task (own) | A | A | A | |
| `task.read` | Read tasks, records, resources | A | A | A | |
| `task.read_output` | Read an output tail | A | A | A | |
| `task.cancel_own` | Cancel own task | A | A | A | |
| `task.cancel_others` | Cancel others' tasks | A | P | P | |
| `task.set_priority` | Change a task's priority | A | A | P | |
| `task.pause` | Pause a running task (*annotation*: `PauseTask`) | A | A | P | |
| `task.purge` | Purge a task record (*annotation*: `PurgeTaskRecord`) | A | D | D | |
| `task.retry` | Retry a finished task (*annotation*: `RetryTask`) | A | A | A (P for a `SIDE_EFFECTING` or `UNKNOWN` task) | |
| `pool.pause` | Pause or resume a pool | A | A | P | |
| `parallelism.change` | Change parallelism | A | P | P | |
| `parallelism.lower_own_session` | Change parallelism: lowering the caller's own session's limit | A | P | A | |
| `policy.change` | Change other policy, create or delete pools | A | P | P | |
| `policy.retry_safety` | `retry_safety` rules (HUMAN-edited, AD-0006 §4) | A | D | D | yes |
| `policy.permissions` | The `permissions` overrides (HUMAN-edited) | A | D | D | yes |
| `policy.center_routed` | The center-routed policy, its cross-node relay opt-in `relayed_from` included (HUMAN-edited; AF-CTR-05 target, Plan decision PB-2) | A | D | D | yes |
| `approval.decide` | Decide an approval | A | D | D | yes |
| `cleanup.plan` | Plan cleanup | A | A | A | |
| `cleanup.execute` | Execute cleanup | A | P | P | |
| `process.adopt` | Adopt or terminate a process: adopt | A | D | D | |
| `process.terminate` | Adopt or terminate a process: terminate (also cancelling an `ADOPTED` task) | A | P | P | |
| `integration.change` | Integrations, pairing, account sign-in | A | D | D | yes |
| `account.sign_in.read` | Read the node's sign-in flow (*annotation*: `AccountService.GetSignInFlow`; added 2026-11-05, AF-CTR-04, ArcForges #69) | A | A | D | yes |
| `node.stop` | Stop the node | A | A | D | |
| `node.update` | Apply an update | A | A | D | |
| `node.rollback` | Roll back an update | A | D | D | yes |
| `node.settings` | Change node settings (*annotation*: `UpdateNodeSettings`) | A | P | D | |
| `node.rename` | Rename the node (*annotation*: `RenameNode`) | A | A | D | |
| `notifications.mark_read` | Mark notifications read (*annotation*: `MarkNotificationsRead`) | A | D | D | |

Overrides for `REMOTE` can only narrow (deny); remote enforcement is AF-CTR-05's (AF-CLD-05 is superseded, [AD-0021](../decisions/AD-0021-central-access-go-center.md)).

**Center-routed operations** (AF-CTR-05 target, not built; added 2026-11-05 by the Plan decisions Q6 and PB-1). The six routed task methods of `FleetService` are REMOTE rows without command kinds. The center applies its columns to an account session before it routes the call; the node applies its own column when the verified call arrives, after the checks of T-11 and before any effect:

| Routed method | Node operation | Class | Center: `mobile.limited` session | Center: account session | Node default for a center-routed caller |
|---|---|---|---|---|---|
| `SubmitNodeTask` | `task.submit` | high | `Upgrade` (never reached) | step-up evidence on every call, class `fleet.submitNodeTask`, target the node ID | A, within the caller's cells ("Center-routed callers" below) |
| `GetNodeTask`, `ListNodeTasks`, `WaitNodeTask` | `task.read` | low | `Allowed` | no step-up | A: detail for the caller's own tasks, the others as summaries; command lines as below |
| `ReadNodeTaskOutput` | `task.read_output` | low | `Allowed` | no step-up | A for the caller's own tasks; the others only with privacy `remote_output_tail` (default off) |
| `CancelNodeTask` | `task.cancel_own`, `task.cancel_others` | medium | `Upgrade` (never reached) | step-up evidence on every call, class `fleet.cancelNodeTask`, target the node ID | own tasks A; others' tasks P (a local HUMAN decides) |
| `CancelNodeTask` of an `ADOPTED` task | `process.terminate` | (D) | as `CancelNodeTask`: the center does not know the task's kind | as `CancelNodeTask` | D, fixed for REMOTE (MR-08, the Plan maintenance record `maintenance/2026-10-25-mr08-permission.md`, carried into AF-CTR-05's acceptance): no policy, confirmation or approval reaches it, and the adopted process keeps running |

- **Step-up (PB-1).** A `mobile.limited` session never reaches `SubmitNodeTask` or `CancelNodeTask`: it must first upgrade to an account session by a step-up, as T-19 requires of a phone paired through a node credential. An account session needs step-up evidence for them, the medium and high routed methods, under the center's existing rule: one proved, unconsumed challenge of the caller's session for the operation's class and target, at most five minutes old, consumed by the call. Evidence is needed per delivery (review finding N-3): a resend with the same `command_id` after the first delivery consumed its evidence first meets `AUTHENTICATION/step_up_required`, and with fresh evidence it is routed again, where the node's command deduplication replays the recorded outcome without a second effect. The center does not answer such a resend from its receipt alone, because it stores no routed response (Plan CTR5-RTE-03). The reads stay open to both session kinds.
- **The relayed half of a row.** The `mobile.limited` and step-up rules of a row apply to its account-session half only. A node-relayed caller (below) carries none, because a node credential cannot step up (today's row check refuses such rules on a row with node scopes, Cloud `access.go`). Its bound is the confinement below and the target node's policy, and the center admits it only to these six methods, `ListNodes` and `GetNode`. Every one of these calls, the reads `ListNodes` and `GetNode` included, needs a valid relay assertion (below; Plan confirmation point C-N6), so a bearer token alone reads nothing of the account's nodes.

**Center-routed callers** (AF-CTR-05 target, not built; added 2026-11-05 by the Plan decisions Q1 as amended by PB-2, Q7 and PN-8; [AD-0021](../decisions/AD-0021-central-access-go-center.md) §7 as amended). A center-routed call reaches the node with origin `REMOTE` and a center caller that the center verified and signed into the call. The node decides it by its center-routed policy, never by the HUMAN cells:
- **Account session** (Web, Android; HUMAN at the center): the last column of the table above.
- **Node-relayed caller from the target node itself** (the CLI, through its node's local endpoint): the narrower of the last column and the cells of the local origin that the relay assertion states (HUMAN, SCRIPT, or AGENT with `agents.allowed_command_patterns`). That origin is the target's own classification only under two conditions, which are checked, not assumed: the center verified the call's relay assertion (below) against the key of the bearer credential's installation, and the relaying node that the signed call header states is the target itself. A call that fails either check is refused before policy. Even then the origin is a classification with §1's documented bypasses, and a same-user process that holds the node key (T-25) can claim any origin.
- **Node-relayed caller from another node:** refused by default, `AUTHORIZATION/permission_denied` with `state.reason` `relay_own_node_only`, because the policy's `relayed_from` defaults to `own_node`. Only a local HUMAN of the target opts in (`relayed_from` = `account`; the fixed operation `policy.center_routed` of "Operation names" above). After the opt-in, the claimed local origin is advisory, because the target cannot verify what another node classified: a claimed HUMAN or SCRIPT origin gets the SCRIPT cells, never more, and a claimed AGENT origin is refused (`state.reason` `relayed_agent_own_node_only`) until the agent grants of AF-CTR-07 exist. MCP adapter and hook clients are AGENT, so behind the local endpoint they reach only their own node. The relaying node also refuses to forward an AGENT caller to another node, with the same reason (review finding N-9), so an honest node never sends such a call; the target's refusal stays the bound.
- **Relay assertion** (Plan addendum D0-B1, refining PB-2 item 4). A call that a node relays for a local caller carries a relay assertion: a signature by the relaying node's key under the domain string `"ArcForges relay-origin v1\n"` (§3) over canonical bytes that name the SHA-256 of the canonical center URL, the relaying node ID and installation ID, the local caller's origin class (HUMAN, SCRIPT or AGENT) and local identity (its local session ID), the routed method, the request SHA-256, the target node ID (zero for `ListNodes`), the command ID (zero for a read), a relay nonce, and an expiry at most 120 s after issue. The request SHA-256 is the digest of the exact node.v1 request bytes that the routed request carries, the `request_sha256` of the call header (Plan CTR5-SIG-01); for `ListNodes` and `GetNode`, which carry no node.v1 request, it covers their request fields as C2 fixes them, the assertion excluded. The relay nonce is one that the center sent on the relaying node's open channel (Plan confirmation point C-N2): one nonce per call, used once, and void when that connection closes or is replaced. Relaying therefore needs an open channel of the relaying node, for a cross-node relay too. Contracts part C2 fixes the byte layout and the nonce frames. Before it serves or routes the call, the center checks:
  - the signature, against the key registered for the bearer credential's installation;
  - that the assertion's node and installation are that credential's enrolled node and installation;
  - that it has not expired and its nonce is unused, and then spends the nonce;
  - that its request digest, method, target and command ID equal those of the routed request, and that the routed request's `caller` (relaying node and local origin) equals the assertion's (Plan confirmation point C-N1).

  Otherwise it refuses the call `AUTHENTICATION/unauthenticated` with a closed reason, `request_mismatch` for any differing field ([errors](../contracts/errors.md)), and routes nothing. The center fills the call header's center caller (relaying node, local origin and local identity) only from the verified assertion, never from the request's `caller` field, and signs it, the assertion's SHA-256 included, into the header; the target checks that the relaying node is the one the center states. A bearer token alone therefore never yields a HUMAN, SCRIPT or AGENT origin, or any relayed call.
- **Remote-control policy** (review finding N-4). `RemoteControlPolicy` (`remote.enabled`, `max_risk`, `allow_approvals`) governs only the unserved command kinds of `SendNodeCommand`; it neither enables nor disables routed calls. The center-routed policy has its own off switch, `enabled`: it defaults to true while the node is signed in with its cloud link on (Plan Q7(a)), and only a local HUMAN changes it (`policy.center_routed`). While it is false, every routed call is refused before any effect (`AUTHORIZATION/permission_denied`, `state.reason` `center_routed_disabled`); turning the cloud link off (`SetCloudLink`) closes the channel.
- **Approvals.** A routed caller never decides an approval (`decide_approval` is not routed). A P verdict answers `AUTHORIZATION/approval_required` with the approval ID, and a local HUMAN decides it (Approvers above).
- **Command lines (PN-8).** Routed `GetNodeTask`, `ListNodeTasks` and `WaitNodeTask` return a task's specification (argv, working directory, environment) only for the caller's own tasks, those whose owner carries the same center caller (the same account session, or the same relaying node and local origin). For other tasks they return summaries without the specification, unless the privacy policy `remote_command_lines` is true (default false), which adds argv and the working directory, with environment names only. Secret values are never returned to a remote caller: secret-shaped names are stored as presence only (R-EXE-017), and sealed values never leave the node.
- **Record.** Every routed call the node verifies, and every one it refuses at verification, is recorded in the node store's `routed_call_log` ([node store](../data/node-store.md), "Schema step 2").
- **Exposure.** A leaked node token without the node key relays nothing and reads nothing of the account's nodes: every relayed call, `ListNodes` and `GetNode` included, without a valid relay assertion is refused before it is served or routed, and the channel needs the hello proof (§3). A token together with the node key (a same-user process, T-19, T-25) can relay as the node: to its own node with any claimed origin, within that origin's cells; to another node of the account only where that node's local HUMAN opted in to cross-node relay, and there with no more than the SCRIPT cells, never as AGENT.

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md), amended 2026-10-19; [18](18-application-workload-control.md) §7.5, §9):* an application origin and an application client kind (two enum values) carry callers of the cooperative resource API; their classification depends on the connection's client kind being verified against the peer (AF-SEC-01; §1's documented bypasses apply). The proposed rows, additive to the matrix above, take effect with RM-09 stage 1 (cooperative rows), RM-18 (per-application entries and placement) and EX-26 (the interactive mode):

| Operation | HUMAN | SCRIPT | AGENT | APPLICATION (new) | REMOTE | PEER |
|---|---|---|---|---|---|---|
| Write a per-application entry; set its placement; set maximums, ceilings, designations, minimum identity strengths; adopt | A | D | D | D | D (view only) | D |
| Launch an application whose profile asks for owner placement | A | runs in managed placement or is refused | runs in managed placement or is refused | D | `run_task` (high), always managed placement | D |
| Request, watch, renew, release its **own** grants; declare activity | A | A | A (own session; MCP leg) | A, clamped by the derived identity's policy | D | D |
| Submit **own** tasks | A | A | A | A, only to pools the owner assigned; priority clamped to the class ceiling | `run_task` (high) | per peer policy |
| Pause pools, change other policy, decide approvals, clean up, stop the node | as above | as above | as above | **D** | as above | as above |
| Interactive mode, leased | A | — | — | effects through an owner designation only | a leased toggle (medium, step-up); never freezes | D |
| Stop a controlled application gracefully | A | P | P | own tasks only | `cancel_task` (medium, step-up), with "unsaved work may be lost" | D |

Every HUMAN-only row stays a GUARDRAIL against same-user code that presents itself as HUMAN or drives the ArcForges Desktop, as this section already says. A remote client may narrow within bounds a local HUMAN authored, for example by revoking a cooperative grant (a `revoke_grant` command kind, medium, with step-up). Every remote change of an owner maximum or placement is denied; remote adoption approval is refused; no remote freeze of an interactive application; terminating a process stays REMOTE D. The new remote command kinds are additive within `v1` at promotion; none is reserved now.

## 2. Local IPC

- **Windows.**
  - The named pipe uses `PIPE_REJECT_REMOTE_CLIENTS`. Its DACL grants `GENERIC_READ | GENERIC_WRITE` to the node user's SID only, explicitly denies `NT AUTHORITY\NETWORK`, and allows SYSTEM.
  - The node also verifies `GetNamedPipeClientProcessId` → token user SID equals its own (DesktopPlatform LocalRpc peer-identity provider; AD-0013).
- **Linux.**
  - The socket directory is mode `0700`, owned by the user.
  - Every connection checks `SO_PEERCRED` uid = node uid.
  - *Superseded 2026-10-21 by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) (kept as history):* "Guest nodes additionally accept only the bridge (uid match) and the link token." There are no guest nodes.
- **Bound to the user.** Any same-user process can reach the node, as with any user-level service. Malware running as the user is out of scope, and the node never extends the user's privileges (R-SEC-001).

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md)):* a tiered threat scope keeps the statement above as its unconfined row, in force now, and adds confined and STRONG-backend rows that apply only when their roadmap rows are promoted ([17](17-delegated-execution.md) §4.1).

## 3. Keys and secrets inventory

| Key / secret | Holder | Protection | Rotation |
|---|---|---|---|
| Node key (ECDSA P-256) | Each node | Windows CNG non-exportable user key; Linux owner-only (0600) PKCS#8 file; under `--test-mode` a file-backed key on both systems (ArcForges #63) | A new key for every sign-in after the credential ended: the key is deleted when its credential ends (sign-out, revocation, expiry) and on a center change, and the center refuses a key an installation holds or held (AF-CTR-04); on compromise, revoke the node's device |
| Node credential (refresh token, scope `node`) | Each node | OS secret store (AD-0011 §4), bound to the node ID and the full center URL, and used only while that center is the configured one (ArcForges #63) | Strict rotation at every refresh (the node refreshes at two thirds of the access lifetime, 60 minutes by default); the refresh token's idle limit is 90 days, within the family's absolute end of 365 days by default, which a refresh never extends (center policy keys, Cloud #130); revocable (sign-out, the device's revocation) |
| Node data key (AES-256; seals task secrets, [04](04-execution.md) §2) | Each node | OS secret store (AD-0011 §4) | A new version when the current key is missing or the backend changed; values sealed under a lost key are unavailable (`STATE/secrets_unavailable`, L-26) |
| Relay token HMAC key | Cloud (Worker + container secrets) | Platform secrets | 90 days, two active `kid`s |
| Command signing key (ECDSA P-256, ES256) | Cloud container | Platform secret | Yearly; public key distributed by enrollment and releases |
| Entitlement token key (ECDSA P-256, ES256) | Cloud container | Platform secret | Yearly; 2 active keys |
| Node Issuing CA (P-256 intermediate) | Deferred with account-based LAN trust (roadmap RM-01); not created in release 1 | — | — |
| Release signing (ES256 manifest key, Authenticode certificate, GPG apt key) | Release engineering | Offline / HSM / signing service (human prerequisite) | Per policy |
| Google service accounts (Play Developer API, FCM) | Cloud container | Platform secrets, least privilege | Yearly |
| Paddle webhook secret | Cloud container | Platform secret | On rotation in Paddle |
| Transactional e-mail credential (a Postmark Server token, or the SMTP user name and password of an IAM user allowed `ses:SendRawEmail`) | Cloud container, only while a provider is configured (the Worker passes the named provider's variables) | Platform secret, from GitHub environment secrets; the acceptance names are `MAIL_POSTMARK_TOKEN_ACCEPTANCE`, `MAIL_SMTP_USERNAME_ACCEPTANCE` and `MAIL_SMTP_PASSWORD_ACCEPTANCE` (none is created: e-mail is disabled in every environment); production naming is decided at AF-PROD-01 | At the provider; a changed value restarts the center before its next request |
| Compiler-cache store tokens (the sccache store; the ccache HTTP fallback) | Per attempt | Node memory; passed in the attempt's environment | Issued at attempt start, revoked at its end |
| MCP HTTP bearer | Reserved for the local HTTP transport (roadmap RM-05); not created in release 1 | — | — |

**Same-user qualifier** (added 2026-10-19; T-25). The OS secret stores, and the Linux 0600-file fallback, protect the node's secrets from other users, not from processes of the signed-in user. Any same-user process, managed tasks included, can read the node credential and the node data key, and so the task secrets sealed under it; a running task's environment holds its secret values in clear ([04](04-execution.md) §2–3). The release coverage statement says: "Unsandboxed managed processes can read every credential the signed-in user can read. ArcForges does not read or record them." ([product definition](../product/product-definition.md) §9).

**Transactional e-mail credential** (added 2026-11-03; AF-CTR-03, Cloud #127). A Postmark sender signature or domain belongs to the Postmark account, not to a Server: a token of the acceptance Server can send as any confirmed sender of the same account, a production domain included. One Server per environment separates streams, statistics, suppression lists and tokens, not senders; isolating the production sender needs a separate Postmark account (or accepting that exposure), which the owner decides at H-19 and AF-PROD-01. The token lets the center send any mail as the product's signed domain, and the Container's egress is open (`enableInternet`, which the database connection needs), so whether mail leaves instead through an outbound handler that fixes the destination is decided again before the production environment gets a provider. No production e-mail secret exists before AF-PROD-01 chooses between a separate GitHub environment with a reviewer and a suffix convention inside the one shared environment.

**Command signing key** (added 2026-10-19; T-11). The node verifies every remote command with this key, then applies its local remote-control policy ([AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md) §5). A compromised cloud command key can therefore issue any command the node's local remote-control policy permits; that policy, not the signature, bounds the exposure.
*Amended 2026-11-05 (AF-CTR-05 target; Plan confirmation point C-N5, CTR5-SEC-18):* for the center-routed methods the bound is the node's center-routed policy (§1, "Center-routed callers"), not its remote-control policy, which governs only the unserved command kinds. A compromised command key can sign any center caller into a call header, an account session included, so it can issue any routed call that the center-routed policy admits for that caller; by default that includes submissions. What limits it is the node's own policy (its `enabled` switch, its permission overrides, which may only narrow REMOTE), the key's retirement runbook, and the nodes dropping a retired key at their next refresh.

**Signature domain strings** (AF-CTR-05 target, not built; added 2026-11-05 by the Plan decision PB-3). Every new signature by the center's command key or by a node key (AF-CTR-04 onwards) signs a fixed ASCII domain string of its own followed by its fields, so that no signature can be presented as another kind (Contracts `fleet.proto`, "Node key proof": "Other signatures of the node key use a different leading domain string"). Signatures are ES256 in IEEE P1363 form, 64 bytes, low-S.

| Signature | Key | Signed bytes |
|---|---|---|
| Node key proof (delivered, AF-CTR-04) | Node key | `"ArcForges node-key-proof v1\n"` (28 bytes), then the purpose, the audience digest, the node ID and the binding |
| Routed call | Center command key | `"ArcForges relay-call v1\n"` (24 bytes), then the exact call header bytes |
| Routed result | Node key | `"ArcForges relay-result v1\n"` (26 bytes), then the exact result header bytes |
| Channel hello proof | Node key | `"ArcForges relay-hello v1\n"` (25 bytes), then the center's nonce, the connection ID, the SHA-256 of the canonical center URL, the node ID and the installation ID |
| Relay assertion (Plan addendum D0-B1) | Node key of the relaying node | `"ArcForges relay-origin v1\n"` (26 bytes), then the canonical assertion fields (§1, "Relay assertion") |

The headers are never a bare `SignedBlob` payload signature: a signature over the header bytes without the domain string is refused. Contracts part C2 fixes the field order and lengths and adds Go and C# golden vectors that include the prefixes; header digests and signatures cover the exact transmitted bytes ([AD-0021](../decisions/AD-0021-central-access-go-center.md) §10).

**Named exceptions** (review finding N-7). Two legacy signatures predate the rule and are bare `SignedBlob` payloads: `NodeCommand` by the command key and `NodeCommandResult` by a node key (Contracts `fleet.proto`, carried by the `command` and `command_result` members of `relay.proto`). They belong to the unserved `SendNodeCommand`. AF-CTR-05 nodes and centers neither produce nor accept them, and the task that first serves `SendNodeCommand` must replace them with domain-separated signatures before it does; none is planned, because AF-CLD-05 is superseded.

**Channel proof of possession** (AF-CTR-05 target, not built; added 2026-11-05 by the Plan decision PB-4; its binding stated by the Plan addendum D0-B2). The node channel is admitted on the node's access token, but the token alone never makes a connection the node's. After the upgrade, the center sends a challenge on this WebSocket connection only: a nonce of at least 16 random bytes, and the connection ID. The nonce is accepted once and only on this connection, and it is void at the 10 s hello deadline or when the connection closes. The node's `NodeHello` carries the channel hello proof above, and the center checks:
- that the node ID and installation ID the hello names equal the enrolled node and the installation of the bearer credential that opened this connection, or it closes the connection 4403;
- the signature, against the key registered for that credential's installation, never against a key the hello names;
- that the signed nonce and connection ID are this connection's own.

Only then does it register the connection as the node's and close an older connection of the same node (4409, replaced), and it sends no call on a connection before that. A token thief without the node key therefore neither displaces the live channel nor receives a routed call, and the key of another installation, enrolled in any account, proves nothing for this credential. Residual risks: the binding is to the WebSocket connection, not to TLS, because TLS ends at the Worker, so no TLS channel binding is claimed; and a same-user process that can read the Linux 0600 key file, or use the Windows user key, can still prove possession (T-25).

Secrets are never logged. Records and exports apply secret-name redaction ([04](04-execution.md) §2). Output text is scanned for credential-shaped tokens (high-entropy strings after `token=`, `Bearer `, `ghp_`, `sk-`, `AKIA` and similar) **only for exports and support bundles**, and these are masked (R-SEC-003).

## 4. Threat model

| ID | Boundary | Threat | Mitigation | Test |
|---|---|---|---|---|
| T-01 | B1 | Another local user connects to the node | Pipe DACL and peer SID; socket 0700 and SO_PEERCRED | Real Windows ACL check; Linux second-uid test (deferred where unavailable) |
| T-02 | B1 | Agent changes policy to remove limits | Guardrail: AGENT policy changes through the API need approval. Direct same-user edits of the store or `node.json` are detected (tamper finding), not prevented (§1). | Unit and closed-loop (API path); tamper-finding test |
| T-03 | B1 | Batch-file argument injection | [04](04-execution.md) §2 refusal | Unit (CVE-class corpus) |
| T-04 | B1 | Cleanup deletes user data through symlinks or junctions | Reparse points never followed; validation re-check before acting; quarantine | Real tests with junctions and symlinks |
| T-05 | B1 | Managed task rewrites the ArcForges installation | Guardrail: read-only version directories with digest checks at startup, and optional Linux unit hardening (`ReadOnlyPaths=`, [AD-0007](../decisions/AD-0007-ai-integration.md) §8), read back after start and reported as applied or not applied, never as workload isolation (amended 2026-10-19). Same-user bypass is documented. | Real test of the read-only attribute, digest check and finding; Linux hardening read-back test, applied where supported and reported as not applied otherwise (A-L04) |
| T-06 | B2 | Fake guest link (*retired 2026-10-21 by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md): B2 and the guest link do not exist; not applicable*) | Bridge launched by host user; uid check; link token | Unit |
| T-07 | B3 | Rogue LAN node | Discovery ≠ trust. TLS accepts any well-formed client certificate. A gRPC interceptor limits unpaired identities to `Hello` and `Pairing`, and blocked identities reach nothing ([AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) §4). | Closed-loop: an unpaired peer reaches only Hello and Pairing; a blocked peer reaches nothing |
| T-08 | B3 | MITM during local pairing | Commitment-based SAS over both certificate fingerprints. Each side checks that the fingerprints equal the certificates presented in the TLS session (no exporter, V-N05). | Unit (protocol), closed-loop with an interposed relay |
| T-09 | B3 | Peer exfiltrates source | Per-peer `data_out` policy; default status-only | Closed-loop |
| T-10 | B3 | Cache poisoning through a writable LAN cache | `cache_write` off by default, explicit per trusted peer; documented risk | Policy tests |
| T-11 | B4 | Forged remote command | ES256 signature, expiry and target checks, then local remote-control policy. Stated exposure (amended 2026-10-19): a compromised cloud command key can issue any command the node's local remote-control policy permits (§3); for the AF-CTR-05 routed methods, any call the node's center-routed policy admits (amended 2026-11-05, C-N5, CTR5-SEC-18; §3). AF-CTR-05 target (amended 2026-11-05, Plan decisions PB-3 and PB-4): each signature kind signs its own domain string; a channel becomes the node's only after a node-key proof, by the key of the bearer credential's installation, over this connection's one-use nonce, before any replacement or call; and a relayed call needs a relay assertion by the relaying node's key, which the center verifies before routing (§1, §3; Plan addendum D0-B1, D0-B2) | Unit, closed-loop; golden vectors with the domain strings, a signature over the bare header refused; `TestATokenWithoutTheNodeKeyCannotReplaceTheChannel`, `TestAHelloSignedByAnotherInstallationsKeyIsRefused` (an enrolled key of another account with a stolen token), `ATokenWithoutTheNodeKeyCannotRelay` (center) and `ARelayedCallWithoutAValidAssertionIsRefused` |
| T-12 | B4 | Stolen relay token | 15-minute lifetime; scope; device revocation stops refresh | Unit |
| T-13 | B5 | Account takeover | Passkeys, step-up for medium and high risk, session revocation (reused contracts; endpoints built by AF-CTR-03, which superseded AF-ID-01) | Closed-loop tests of the identity endpoints, including the step-up gates |
| T-14 | B6 | Spoofed Paddle or RTDN webhook | HMAC raw-body / Pub/Sub OIDC verification; inbox dedup | Closed-loop with fixtures |
| T-15 | B6 | Play token replay to another account | Token-to-account uniqueness; `obfuscatedAccountId` check | Unit |
| T-16 | Cloud | Cost amplification (alarm loops, viewer floods) | Quotas, DO wake guard, kill switches | Closed-loop |
| T-17 | Supply chain | Tampered update | Signed manifest + Authenticode; digest checks; rollback | Real update tests with test keys |
| T-18 | B1 | Escaped processes evade cancellation: descendants outside the job whose recorded ancestry passes through a job member (amended 2026-10-19; launches outside the recorded ancestry are T-23) | Ancestry scan; report and terminate | Real test: such a descendant is detected and terminated (previously "Real Windows WMI test", which is now T-23's test) |
| T-19 | B5 | Stolen node credential used to gain account access (for example from the Linux 0600-file fallback, or read by any same-user process, T-25) | A node credential can create and confirm a phone pairing, but the phone then holds only a `mobile.limited` session. Medium- and high-risk commands, billing and account settings need a step-up on the phone (passkey or e-mail code) ([AD-0011](../decisions/AD-0011-identity-and-login.md) §3). AF-CTR-05 target (amended 2026-11-05, Plan decisions PB-1 and PB-2): a `mobile.limited` session never reaches routed `SubmitNodeTask` or `CancelNodeTask`, an account session needs step-up evidence for them, and the node token alone relays nothing, because a relayed call needs a relay assertion by the node key (Plan addendum D0-B1). A token together with the node key (T-25) relays for its own node, and to another node only where that node's local HUMAN opted in, with no more than the SCRIPT cells (§1, "Center-routed callers") | Closed-loop: a phone paired through a node credential cannot run medium or high commands or reach billing before step-up; AF-CTR-05: a `mobile.limited` session cannot submit or cancel a routed task, a token without the node key cannot relay, and a cross-node relay is refused by default |
| T-20 | B3 | Lost or stolen paired machine (its node key and credentials are protected from other users only, T-25) | Trust is per peer: the user removes or blocks the machine on every peer that paired with it (D-15). Cloud revocation ends only cloud access ([09](09-lan.md) §3.3). | Closed-loop: a removed or blocked peer reaches nothing; a cloud-revoked node keeps no cloud access |
| T-21 | B1 | Local users and sccache on loopback TCP. (a) Another local user connects to an attempt's sccache server on a loopback port without authentication (Windows, or a client older than 0.9.0 on Linux) and submits a compile request that runs as the attempt's user. (b) While the node is down, another local user takes the cache store's port and answers cache reads with poisoned entries. | (a) The server exists only for its attempt, on a port from a per-user range outside the ephemeral ranges. Every second, the holder (Windows) or the node (Linux) checks the listener's owning process, and stops an attempt that uses sccache when a process outside it listens there (`ENDPOINT_TAKEN`). Supported versions on Linux use a Unix socket in a directory only the user can open. (b) The store needs a per-attempt token for every request; the node binds its port exclusively on Windows and rebinds it at once when it restarts, and if another process holds it, the node stops the attempts that use sccache. Remaining: a foreign listener that appears between two checks, a wrapper script that sets its own port, and a process that takes the store's port while the node is down, which receives reads and tokens and could answer with poisoned entries. Machines shared with untrusted local users should not use sccache; the toolchain page says so whenever sccache is installed. | Closed-loop on Linux (socket permissions) and on both platforms (port-ownership checks, the rebind, and an attempt without sccache surviving a collision); exposure documented |
| T-22 | B0, B1 | Container tampering: same-user code changes the limits of ArcForges' containers or ends sibling attempts (added 2026-10-19) | Documented bypass (§1); every resource guarantee carries the same-user qualifier ([03](03-resource-control.md) §5) | Release-scope text in AF-AI-01's fixture |
| T-23 | B1 | Leaving the container outside the recorded ancestry: work launched through WMI, a broker, a service, a scheduled task or a spoofed parent (added 2026-10-19; amends T-18) | Documented gap (§1); the ancestry scan detects only descendants whose recorded ancestry passes through a job member ([03](03-resource-control.md) §9) | AF-SEC-01: the real Windows WMI test shows that the scan reports nothing, and the gap is documented in §1 (A-W04). AF-AI-01: the release coverage statement states the gap among the documented bypasses T-22 … T-27 |
| T-24 | B11 | Routing out of a client sandbox: MCP `run` or a hook rewrite moves a command out of the client's OS sandbox; the client's own process, with its hooks, its MCP servers and, for Claude Code, its file tools, stays outside every ArcForges boundary (added 2026-10-19) | Stated per client in the integration consent diff and in the routing rows of `GetReleaseScope`, which D-14, `arcforges coverage` and the MCP `session_coverage` tool show ([AD-0007](../decisions/AD-0007-ai-integration.md) §4) | Fixture checks in AF-AI-01, AF-AI-02 and AF-MCP-01 (A-A03) |
| T-25 | B1, B5 | Same-user secret reach: the data key's OS-store entry, sealed task secrets in running environments, the Linux 0600 fallback (added 2026-10-19; amends T-19 and T-20) | The same-user qualifier (§3; [04](04-execution.md) §2) and the release-scope credential sentence | Release-scope text |
| T-26 | B1 | Privileged changes without ArcForges elevating: polkit-authorized system-bus requests on Linux; Windows sudo in some configurations, such as the inline mode; UAC is not a security boundary on an administrator account without Administrator protection (added 2026-10-19) | The system bus and the other channels in the channel catalogue (§1); the generic UAC sentence in the release coverage statement; the host's account type and Administrator protection state reported by the doctor's HUMAN-only host-posture check ([07](07-records-diagnosis-memory.md) §2.4), never through the release coverage statement or MCP | Catalogue review; release-scope text (AF-AI-01); the doctor check on a standard and an administrator account, with the values withheld from AGENT, SCRIPT and MCP callers (AF-DIAG-01; A-W05) |
| T-27 | B3 | A paired peer with placement rights executes code as the local user; per-peer command patterns are argument-vector filters, which are guardrails (added 2026-10-19) | Stated; placement stays opt-in per peer ([AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) §5; [09](09-lan.md) §4) | Release-scope text |

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md)):* threat rows T-28 … T-42, which apply only when their roadmap rows are promoted, are proposed in [17](17-delegated-execution.md) §4.4; none is in force, and none enters this table before its row is promoted.

## 5. Privacy

| Data | Location | Leaves the node | Retention |
|---|---|---|---|
| Task records, timelines, samples | Node | Summaries (D1) to the relay only with remote access on; detail (D2) only on explicit viewer request where privacy policy allows (default **deny** for command lines and output) | 14 days logs / 90 days records (policy) |
| Operational memory | Node | Never | TTL 30 days unobserved |
| Agent session metadata | Node | Summary counts with remote view | 90 days |
| Account profile, auth identities | Cloud D1 | — | Until account deletion (+30-day grace) |
| Sessions | Cloud | — | 90 days after expiry |
| Devices and nodes | Cloud | — | Until revoked + 30 days |
| Node status cache | DO storage | — | Until node revoked or 30 days stale |
| Remote commands | Cloud | — | 90 days |
| Account command receipts (results hold the display name, locale and time zone, a credential summary and a device view) | Cloud | — | 90 days; purged with the account |
| Sign-in flows and rate-limit buckets (unsalted digests of e-mail addresses and client prefixes) | Cloud | — | 7 days (flows); one window (buckets) |
| Audit events | Cloud | — | 1 year |
| Commerce references (Paddle or Play IDs, states) | Cloud | — | 7 years (billing records) |
| Support cases | Cloud | — | 2 years |
| Support bundles | R2 (consented upload) | — | 30 days |
| Push registrations | Cloud | — | Until unregistered or invalid |
| Host posture: the account type and the Administrator protection state (D2; added 2026-10-19) | Node, read by the doctor's host-posture check ([07](07-records-diagnosis-memory.md) §2.4) | Never. Returned only to local callers of HUMAN origin: not to AGENT or SCRIPT callers, not through the MCP adapter, the relay or `GetReleaseScope`; left out of support bundles unless the owner includes it | Latest only |

- **Deletion.** Account deletion (the reused contract's flow with a grace period, built by AF-ID-02) revokes every node, phone and browser. Nodes receive the notice through the relay or the next enrollment call, and offer local wipe (`arcforges node wipe`, HUMAN only). Exports: account data export through the reused `DataService`, and node records export through `ExportRecords` (R-OPS-004).
- **Telemetry.** Off by default. Opt-in sends daily anonymous counters only (R-OPS-003).
- **Support bundles.** Generated locally: node logs, capability report, policies, recent findings and redacted records, all with the redactions of §3. Host-posture values are left out unless the owner includes them. The user reviews the file list before an optional upload (R-OPS-005).

## 6. Supply chain

- Signed release artifacts (AD-0012 §3).
- Dependency admission and provenance practices are reused from the existing repositories (locked restores, reviewed dependency admission records, licence boundaries).
- An SBOM (CycloneDX JSON) is generated per release from the locked dependency graph and published with the manifest.
- No `postinstall`-style scripts run during ArcForges' own install. The setup program, `install.sh` and the `.deb` install only files and registrations. This covers ArcForges' own installer only, not software that managed tasks install (scoped 2026-10-19).
