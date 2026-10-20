# 11 — Security and privacy

## 1. Origins and permissions (local)

The node classifies every API call by **origin**. The connection's client kind is verified, and process ancestry is checked against registered agent roots ([08](08-ai-integration.md) §3).

| Origin | Determined by |
|---|---|
| `HUMAN` | Desktop connections; CLI processes **not** descended from a registered agent root and attached to an interactive terminal (the console or pty is checked by the CLI and reported in the hello; spoofable, see below) |
| `AGENT` | MCP adapter connections; hook handler; CLI processes descended from an agent root or carrying `ARCFORGES_SESSION` |
| `SCRIPT` | CLI not under an agent root and without a terminal (CI, scheduled scripts) |
| `REMOTE` | Signed relay commands (§3) |
| `PEER` | LAN peers (mTLS identity) |
| `GUEST` / `HOST` | Guest link counterparts |

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
  - Guest nodes additionally accept only the bridge (uid match) and the link token.
- **Bound to the user.** Any same-user process can reach the node, as with any user-level service. Malware running as the user is out of scope, and the node never extends the user's privileges (R-SEC-001).

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md)):* a tiered threat scope keeps the statement above as its unconfined row, in force now, and adds confined and STRONG-backend rows that apply only when their roadmap rows are promoted ([17](17-delegated-execution.md) §4.1).

## 3. Keys and secrets inventory

| Key / secret | Holder | Protection | Rotation |
|---|---|---|---|
| Node key (ECDSA P-256) | Each node | Windows CNG non-exportable user key; Linux 0600 file | On demand (re-pair); on compromise, revoke |
| Node credential (refresh token, scope `node`) | Each node | OS secret store (AD-0011 §4) | 90-day sliding; revocable |
| Node data key (AES-256; seals task secrets, [04](04-execution.md) §2) | Each node | OS secret store (AD-0011 §4) | A new version when the current key is missing or the backend changed; values sealed under a lost key are unavailable (`STATE/secrets_unavailable`, L-26) |
| Relay token HMAC key | Cloud (Worker + container secrets) | Platform secrets | 90 days, two active `kid`s |
| Command signing key (ECDSA P-256, ES256) | Cloud container | Platform secret | Yearly; public key distributed by enrollment and releases |
| Entitlement token key (ECDSA P-256, ES256) | Cloud container | Platform secret | Yearly; 2 active keys |
| Node Issuing CA (P-256 intermediate) | Deferred with account-based LAN trust (roadmap RM-01); not created in release 1 | — | — |
| Release signing (ES256 manifest key, Authenticode certificate, GPG apt key) | Release engineering | Offline / HSM / signing service (human prerequisite) | Per policy |
| Google service accounts (Play Developer API, FCM) | Cloud container | Platform secrets, least privilege | Yearly |
| Paddle webhook secret | Cloud container | Platform secret | On rotation in Paddle |
| Compiler-cache store tokens (the sccache store; the ccache HTTP fallback) | Per attempt | Node memory; passed in the attempt's environment | Issued at attempt start, revoked at its end |
| MCP HTTP bearer | Reserved for the local HTTP transport (roadmap RM-05); not created in release 1 | — | — |

**Same-user qualifier** (added 2026-10-19; T-25). The OS secret stores, and the Linux 0600-file fallback, protect the node's secrets from other users, not from processes of the signed-in user. Any same-user process, managed tasks included, can read the node credential and the node data key, and so the task secrets sealed under it; a running task's environment holds its secret values in clear ([04](04-execution.md) §2–3). The release coverage statement says: "Unsandboxed managed processes can read every credential the signed-in user can read. ArcForges does not read or record them." ([product definition](../product/product-definition.md) §9).

**Command signing key** (added 2026-10-19; T-11). The node verifies every remote command with this key, then applies its local remote-control policy ([AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md) §5). A compromised cloud command key can therefore issue any command the node's local remote-control policy permits; that policy, not the signature, bounds the exposure.

Secrets are never logged. Records and exports apply secret-name redaction ([04](04-execution.md) §2). Output text is scanned for credential-shaped tokens (high-entropy strings after `token=`, `Bearer `, `ghp_`, `sk-`, `AKIA` and similar) **only for exports and support bundles**, and these are masked (R-SEC-003).

## 4. Threat model

| ID | Boundary | Threat | Mitigation | Test |
|---|---|---|---|---|
| T-01 | B1 | Another local user connects to the node | Pipe DACL and peer SID; socket 0700 and SO_PEERCRED | Real Windows ACL check; Linux second-uid test (deferred where unavailable) |
| T-02 | B1 | Agent changes policy to remove limits | Guardrail: AGENT policy changes through the API need approval. Direct same-user edits of the store or `node.json` are detected (tamper finding), not prevented (§1). | Unit and closed-loop (API path); tamper-finding test |
| T-03 | B1 | Batch-file argument injection | [04](04-execution.md) §2 refusal | Unit (CVE-class corpus) |
| T-04 | B1 | Cleanup deletes user data through symlinks or junctions | Reparse points never followed; validation re-check before acting; quarantine | Real tests with junctions and symlinks |
| T-05 | B1 | Managed task rewrites the ArcForges installation | Guardrail: read-only version directories with digest checks at startup, and optional Linux unit hardening (`ReadOnlyPaths=`, [AD-0007](../decisions/AD-0007-ai-integration.md) §8), read back after start and reported as applied or not applied, never as workload isolation (amended 2026-10-19). Same-user bypass is documented. | Real test of the read-only attribute, digest check and finding; Linux hardening read-back test, applied where supported and reported as not applied otherwise (A-L04) |
| T-06 | B2 | Fake guest link | Bridge launched by host user; uid check; link token | Unit |
| T-07 | B3 | Rogue LAN node | Discovery ≠ trust. TLS accepts any well-formed client certificate. A gRPC interceptor limits unpaired identities to `Hello` and `Pairing`, and blocked identities reach nothing ([AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) §4). | Closed-loop: an unpaired peer reaches only Hello and Pairing; a blocked peer reaches nothing |
| T-08 | B3 | MITM during local pairing | Commitment-based SAS over both certificate fingerprints. Each side checks that the fingerprints equal the certificates presented in the TLS session (no exporter, V-N05). | Unit (protocol), closed-loop with an interposed relay |
| T-09 | B3 | Peer exfiltrates source | Per-peer `data_out` policy; default status-only | Closed-loop |
| T-10 | B3 | Cache poisoning through a writable LAN cache | `cache_write` off by default, explicit per trusted peer; documented risk | Policy tests |
| T-11 | B4 | Forged remote command | ES256 signature, expiry and target checks, then local remote-control policy. Stated exposure (amended 2026-10-19): a compromised cloud command key can issue any command the node's local remote-control policy permits (§3) | Unit, closed-loop |
| T-12 | B4 | Stolen relay token | 15-minute lifetime; scope; device revocation stops refresh | Unit |
| T-13 | B5 | Account takeover | Passkeys, step-up for medium and high risk, session revocation (reused contracts; endpoints built by AF-ID-01) | Closed-loop tests of the identity endpoints, including the step-up gates |
| T-14 | B6 | Spoofed Paddle or RTDN webhook | HMAC raw-body / Pub/Sub OIDC verification; inbox dedup | Closed-loop with fixtures |
| T-15 | B6 | Play token replay to another account | Token-to-account uniqueness; `obfuscatedAccountId` check | Unit |
| T-16 | Cloud | Cost amplification (alarm loops, viewer floods) | Quotas, DO wake guard, kill switches | Closed-loop |
| T-17 | Supply chain | Tampered update | Signed manifest + Authenticode; digest checks; rollback | Real update tests with test keys |
| T-18 | B1 | Escaped processes evade cancellation: descendants outside the job whose recorded ancestry passes through a job member (amended 2026-10-19; launches outside the recorded ancestry are T-23) | Ancestry scan; report and terminate | Real test: such a descendant is detected and terminated (previously "Real Windows WMI test", which is now T-23's test) |
| T-19 | B5 | Stolen node credential used to gain account access (for example from the Linux 0600-file fallback, or read by any same-user process, T-25) | A node credential can create and confirm a phone pairing, but the phone then holds only a `mobile.limited` session. Medium- and high-risk commands, billing and account settings need a step-up on the phone (passkey or e-mail code) ([AD-0011](../decisions/AD-0011-identity-and-login.md) §3). | Closed-loop: a phone paired through a node credential cannot run medium or high commands or reach billing before step-up |
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
| Audit events | Cloud | — | 1 year |
| Commerce references (Paddle or Play IDs, states) | Cloud | — | 7 years (billing records) |
| Support cases | Cloud | — | 2 years |
| Support bundles | R2 (consented upload) | — | 30 days |
| Push registrations | Cloud | — | Until unregistered or invalid |
| Host posture: the account type and the Administrator protection state (D2; added 2026-10-19) | Node, read by the doctor's host-posture check ([07](07-records-diagnosis-memory.md) §2.4) | Never. Returned only to local callers of HUMAN origin: not to AGENT or SCRIPT callers, not through the MCP adapter, the relay or `GetReleaseScope`; left out of support bundles unless the owner includes it | Latest only |

- **Deletion.** Account deletion (the reused contract's flow with a grace period, built by AF-ID-02) revokes every node and phone. Nodes receive the notice through the relay or the next enrollment call, and offer local wipe (`arcforges node wipe`, HUMAN only). Exports: account data export through the reused `DataService`, and node records export through `ExportRecords` (R-OPS-004).
- **Telemetry.** Off by default. Opt-in sends daily anonymous counters only (R-OPS-003).
- **Support bundles.** Generated locally: node logs, capability report, policies, recent findings and redacted records, all with the redactions of §3. Host-posture values are left out unless the owner includes them. The user reviews the file list before an optional upload (R-OPS-005).

## 6. Supply chain

- Signed release artifacts (AD-0012 §3).
- Dependency admission and provenance practices are reused from the existing repositories (locked restores, reviewed dependency admission records, licence boundaries).
- An SBOM (CycloneDX JSON) is generated per release from the locked dependency graph and published with the manifest.
- No `postinstall`-style scripts run during ArcForges' own install. The setup program, `install.sh` and the `.deb` install only files and registrations. This covers ArcForges' own installer only, not software that managed tasks install (scoped 2026-10-19).
