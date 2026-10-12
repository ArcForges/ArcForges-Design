# 11 — Security and privacy

## 1. Origins and permissions (local)

The node classifies every API call by **origin**. The connection's client kind is verified, and process ancestry is checked against registered agent roots ([08](08-ai-integration.md) §3).

| Origin | Determined by |
|---|---|
| `HUMAN` | Desktop connections; CLI processes **not** descended from a registered agent root and attached to an interactive terminal |
| `AGENT` | MCP adapter connections; hook handler; CLI processes descended from an agent root or carrying `ARCFORGES_SESSION` |
| `SCRIPT` | CLI not under an agent root and without a terminal (CI, scheduled scripts) |
| `REMOTE` | Signed relay commands (§3) |
| `PEER` | LAN peers (mTLS identity) |
| `GUEST` / `HOST` | Guest link counterparts |

Default permission matrix (policy `permissions`, editable only by `HUMAN`). The key is A = allow, P = approval required (an approval request is raised and the call returns `PENDING_APPROVAL` with an approval ID), D = deny, R = remote policy decides (AD-0009 §5).

| Operation | HUMAN | SCRIPT | AGENT | REMOTE | PEER |
|---|---|---|---|---|---|
| Submit task (own) | A | A | A (subject to `agent.allowed_command_patterns`, default all) | R (high) | A (per peer policy) |
| Read tasks, records, resources | A | A | A (own session's tasks in detail; others as summary) | R (low) | status only |
| Cancel own task | A | A | A | R (medium) | A (own remote attempts) |
| Cancel others' tasks | A | P | P | R (medium) | D |
| Change priority, pause or resume pool | A | A | P | R (low/medium) | D |
| Change policy | A | P | P | R (high) | D |
| Plan cleanup | A | A | A | R (medium) | D |
| Execute cleanup | A | P | P (A for low-risk only if `cleanup.agent_execute=LOW_RISK_ONLY`) | R (high) | D |
| Adopt process | A | D | D | D | D |
| Integrations, pairing, account sign-in | A (interactive) | D | D | D | D |
| Node stop, update, rollback | A | A | D | R (high) | D |
| Apply remedy | per remedy class | per remedy class | P | R | D |

**Approvers** must be `HUMAN` (Desktop, interactive CLI), or `REMOTE` with step-up and the node policy `remote.allow_approvals=true` (R-SEC-002).

## 2. Local IPC

- **Windows.**
  - The named pipe uses `PIPE_REJECT_REMOTE_CLIENTS`. Its DACL grants `GENERIC_READ | GENERIC_WRITE` to the node user's SID only, explicitly denies `NT AUTHORITY\NETWORK`, and allows SYSTEM.
  - The node also verifies `GetNamedPipeClientProcessId` → token user SID equals its own (DesktopPlatform LocalRpc peer-identity provider; AD-0013).
- **Linux.**
  - The socket directory is mode `0700`, owned by the user.
  - Every connection checks `SO_PEERCRED` uid = node uid.
  - Guest nodes additionally accept only the bridge (uid match) and the link token.
- **Bound to the user.** Any same-user process can reach the node, as with any user-level service. Malware running as the user is out of scope, and the node never extends the user's privileges (R-SEC-001).

## 3. Keys and secrets inventory

| Key / secret | Holder | Protection | Rotation |
|---|---|---|---|
| Node key (ECDSA P-256) | Each node | Windows CNG non-exportable user key; Linux 0600 file | On demand (re-pair); on compromise, revoke |
| Node credential (refresh token, scope `node`) | Each node | OS secret store (AD-0011 §4) | 90-day sliding; revocable |
| Relay token HMAC key | Cloud (Worker + container secrets) | Platform secrets | 90 days, two active `kid`s |
| Relay command signing key (Ed25519) | Cloud container | Platform secret | Yearly; public key distributed by enrollment and releases |
| Entitlement token key (Ed25519) | Cloud container | Platform secret | Yearly; 2 active keys |
| Node Issuing CA (P-256 intermediate) | Cloud container | Platform secret. Root is offline (human custody). | Intermediate yearly |
| Release signing (Ed25519 manifest key, Authenticode certificate, GPG apt key) | Release engineering | Offline / HSM / signing service (human prerequisite) | Per policy |
| Google service accounts (Play Developer API, FCM) | Cloud container | Platform secrets, least privilege | Yearly |
| Paddle webhook secret | Cloud container | Platform secret | On rotation in Paddle |
| Loopback cache-proxy bearer | Each node | Memory plus 0600 file | Every node start |
| MCP HTTP bearer (optional) | Each node | 0600 file | Every node start |

Secrets are never logged. Records and exports apply secret-name redaction ([04](04-execution.md) §2). Output text is scanned for credential-shaped tokens (high-entropy strings after `token=`, `Bearer `, `ghp_`, `sk-`, `AKIA` and similar) **only for exports and support bundles**, and these are masked (R-SEC-003).

## 4. Threat model

| ID | Boundary | Threat | Mitigation | Test |
|---|---|---|---|---|
| T-01 | B1 | Another local user connects to the node | Pipe DACL and peer SID; socket 0700 and SO_PEERCRED | Real Windows ACL check; Linux second-uid test (deferred where unavailable) |
| T-02 | B1 | Agent changes policy to remove limits | Permission matrix: AGENT policy changes need approval | Unit and closed-loop |
| T-03 | B1 | Batch-file argument injection | [04](04-execution.md) §2 refusal | Unit (CVE-class corpus) |
| T-04 | B1 | Cleanup deletes user data through symlinks or junctions | Reparse points never followed; validation re-check before acting; quarantine | Real tests with junctions and symlinks |
| T-05 | B1 | Managed task rewrites the ArcForges installation | Read-only app directories ([AD-0007](../decisions/AD-0007-ai-integration.md) §8) | Real test |
| T-06 | B2 | Fake guest link | Bridge launched by host user; uid check; link token | Unit |
| T-07 | B3 | Rogue LAN node | Discovery ≠ trust; mTLS with pinned or account certificates | Closed-loop |
| T-08 | B3 | MITM during local pairing | Commitment-based SAS bound to the TLS exporter | Unit (protocol), closed-loop |
| T-09 | B3 | Peer exfiltrates source | Per-peer `data_out` policy; default status-only | Closed-loop |
| T-10 | B3 | Cache poisoning through a writable LAN cache | `cache_write` off by default, explicit per trusted peer; documented risk | Policy tests |
| T-11 | B4 | Forged remote command | Ed25519 signature, expiry and target checks, then local remote-control policy | Unit, closed-loop |
| T-12 | B4 | Stolen relay token | 15-minute lifetime; scope; device revocation stops refresh | Unit |
| T-13 | B5 | Account takeover | Passkeys, step-up for medium and high risk, session revocation (reused) | Reused tests plus new step-up gates |
| T-14 | B6 | Spoofed Paddle or RTDN webhook | HMAC raw-body / Pub/Sub OIDC verification; inbox dedup | Closed-loop with fixtures |
| T-15 | B6 | Play token replay to another account | Token-to-account uniqueness; `obfuscatedAccountId` check | Unit |
| T-16 | Cloud | Cost amplification (alarm loops, viewer floods) | Quotas, DO wake guard, kill switches | Closed-loop |
| T-17 | Supply chain | Tampered update | Signed manifest + Authenticode; digest checks; rollback | Real update tests with test keys |
| T-18 | B1 | Escaped processes evade cancellation | Ancestry scan; report and terminate | Real Windows WMI test |

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

- **Deletion.** Account deletion (reused flow with grace) revokes every node and phone. Nodes receive the notice through the relay or the next enrollment call, and offer local wipe (`arcforges node wipe`, HUMAN only). Exports: account data export through the reused `DataService`, and node records export through `ExportRecords` (R-OPS-004).
- **Telemetry.** Off by default. Opt-in sends daily anonymous counters only (R-OPS-003).
- **Support bundles.** Generated locally: node logs, capability report, policies, recent findings and redacted records, all with the redactions of §3. The user reviews the file list before an optional upload (R-OPS-005).

## 6. Supply chain

- Signed release artifacts (AD-0012 §3).
- Dependency admission and provenance practices are reused from the existing repositories (locked restores, reviewed dependency admission records, licence boundaries).
- An SBOM (CycloneDX JSON) is generated per release from the locked dependency graph and published with the manifest.
- No `postinstall`-style scripts run during install. The MSI and `.deb` install only files and registrations.
