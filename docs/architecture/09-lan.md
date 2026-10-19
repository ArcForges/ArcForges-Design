# 09 — LAN: discovery, pairing, placement and transfer

Decision: [AD-0008](../decisions/AD-0008-lan-trust-and-placement.md). Contracts: `arcforges.peer.v1` ([contracts](../contracts/proto/arcforges/peer/v1/peer.proto)).

## 1. Listener and identity

- The listener is TCP `0.0.0.0:47820` (configurable; IPv6 dual-stack where available). Kestrel HTTPS uses TLS 1.3 only and requires a client certificate. TLS 1.3 is available on every supported platform: Windows 11, whose Schannel supports TLS 1.3 (Windows 10 does not, V-N06; [AD-0002](../decisions/AD-0002-platform-scope.md)), and Linux with OpenSSL. It is enabled when the user turns on LAN features. The TLS layer accepts any well-formed client certificate. A gRPC interceptor then limits unpaired identities to `PeerHandshakeService.Hello` and `PairingService`, and every other service requires a pinned (paired) identity (AD-0008 §4). WSL2 mirrored networking exposes the guest on the LAN (L-12), but guest nodes do **not** open a LAN listener by default: their LAN presence is through the host node.
- **Node key:** ECDSA P-256. On Windows it is stored as a CNG key with export disabled, in the user profile. On Linux it is a 0600 PKCS#8 file in the data root. The self-signed certificate SAN contains `URI:arcforges:node:<node_id>`.
- **Account certificates** (cloud-issued, for trust between nodes of one account without pairing) are accepted future work (roadmap RM-01). Release 1 uses the self-signed node certificate only, and LAN features need no account.

## 2. Discovery

| Mechanism | Detail |
|---|---|
| DNS-SD | Service `_arcforges._tcp.local`, instance `<node name>`. TXT records: `id` (node ID, base32), `v` (protocol range, for example `1-1`), `fp` (first 16 hex digits of the certificate SHA-256), `tls=1`. The `acct` record (a per-account hash, policy `lan.advertise_account_hint`) is reserved for account hints (roadmap RM-01) and is not advertised in release 1. Advertising is limited to networks the user marks as trusted: Windows Private-category networks, and on Linux the interfaces the user selects. Windows registers and browses with `DnsServiceRegister`/`DnsServiceBrowse` (V-T04). Linux uses the in-process responder and browser (RFC 6762/6763 subset: PTR, SRV, TXT, A, AAAA; probing; announcements; TTL 120 s). |
| Manual | `PeerService.AddPeerAddress(host, port)` |
| Account hints | Deferred (roadmap RM-01): `NodeEnrollmentService.GetLanHints` is reserved and not served in release 1 |
| Advertisement control | Policy `lan.advertise` (default true while LAN features are on) |

Discovered peers appear as `DISCOVERED` (untrusted) and are never used until paired (R-LAN-001).

## 3. Pairing

### 3.1 Same account (deferred)

Account-based trust between nodes of one account (`PAIRED (ACCOUNT)`) is accepted future work (roadmap RM-01). In release 1 every peer, including another machine of the same user, is trusted through local confirmation (§3.2).

### 3.2 Local confirmation (any two nodes)

1. A user starts pairing on node A for discovered peer B (`PeerService.BeginPairing`). B shows an incoming request to its user, which can be accepted or rejected.
2. A opens a TLS connection to B using self-signed certificates, unverified for now.
3. The commitment exchange (`peer.v1.PairingService`, all over that TLS session):
   1. A sends `commit = SHA-256(nonce_A ‖ fp_A)`.
   2. B sends `nonce_B` and `fp_B`. A checks that `fp_B` equals the certificate B presented in this TLS session.
   3. A reveals `nonce_A` and `fp_A`. B verifies the commitment, and checks that `fp_A` equals the client certificate A presented.
4. Both compute `SAS = uint32(HMAC-SHA-256(nonce_A ‖ nonce_B, fp_A ‖ fp_B ‖ "arcforges-pairing-v1")[0..4]) mod 1,000,000`, shown as six digits.
   - **Why it defeats a man in the middle.** An attacker presents its own certificates to each side, so the two sides use different fingerprints and compute different digits.
   - **Why the commitment matters.** It stops the attacker from choosing a nonce after seeing the other, so it cannot search for colliding digits.
   - **No exporter.** None is used, because .NET 10 does not expose one (V-N05).
5. Both users confirm the digits match (`ConfirmPairing`). Each node pins the other's certificate fingerprint, and the peer becomes `PAIRED (PINNED)`.
6. Mismatch, rejection or a 120 s timeout aborts the pairing. Five failed attempts per peer per hour block it (R-LAN-002).

### 3.3 Revocation

`PeerService.RemovePeer` unpins locally and notifies the peer when it is reachable; **Block** also refuses the identity in future. Trust is per peer and local: revoking a node in the cloud (`FleetService.RevokeNode`) ends only its cloud access and changes no LAN pin. A lost or stolen machine must therefore be removed or blocked on every peer that paired with it (D-15); the web revoke dialog says so. Account-wide LAN revocation arrives only with account-based trust (roadmap RM-01).

## 4. Peer policy and status

`PeerPolicy`:
- `allow_place_to`, `accept_from`;
- `cache_read`, `cache_write`;
- `max_cpu_share` and `max_mem_share` (fractions of the peer's managed budget offered to us, set by that peer);
- `allowed_toolchains[]`, `allowed_command_patterns[]`;
- `require_approval`;
- `data_out` = `{source, outputs, logs}`.

The default for a new pairing is status only. `PeerStatusService.WatchStatus` streams the peer's capabilities, toolchains, enforcement state, budget summary and queue length (D0/D1 data) (R-LAN-004).

**What placement rights mean** (added 2026-10-19; [11](11-security-privacy.md) §1, T-27). A paired peer allowed to place work here executes code as the local user, with that user's access. `allowed_command_patterns` and `allowed_toolchains` are filters on the argument vector, which are guardrails: they restrict which commands are started, not what the started programs do. Placement therefore stays opt-in per peer ([AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) §5).

## 5. Placement

### 5.1 Scoring

For each task with `placement=ANY` (or naming a node), the origin computes for each candidate `c` (local, and peers whose policy allows):

```
eligible(c) = constraints met (os, arch, toolchains, labels) ∧ policy allows ∧ peer reachable ∧ compatible protocol
score(c) = est_start_delay(c) + est_duration(c) + transfer_seconds(c) − warmth_bonus(c)      (all terms in seconds)
  est_start_delay: from the candidate's offer (queue ETA)
  est_duration: the candidate's own DURATION p50 for this command fingerprint when it holds an ACTIVE fact (exchanged in the offer);
                otherwise the origin's p50 scaled by the candidate's CPU class (relative benchmark score exchanged at pairing)
  transfer_seconds: (input bytes the candidate lacks) / measured LAN throughput (EWMA of past transfers, default 50 MB/s)
  cache_warmth: share of the task's cache bindings for which the candidate holds a matching compat_key cache with hits in the last 7 days
  warmth_bonus: w_c · cache_warmth(c) only when est_duration is borrowed from another node; 0 when it is the candidate's own fact,
                because that fact already reflects the candidate's cache state (no double counting)
defaults: w_c = 60 s (so a fully warm cache is worth one minute); cache_warmth is in [0, 1]
choose argmin(score); local wins ties.
```

Placement is re-evaluated only before start. Running attempts never migrate (R-LAN-005).

### 5.2 Protocol (`peer.v1.PlacementService`)

1. `RequestOffer` takes a task summary (sanitized per `data_out`), demand, requirements, input byte estimate and priority. It returns an `Offer` (`offer_id`, `accept_by` 30 s, queue ETA, reservation, `missing_toolchains[]`, `cache_warmth`). The executor reserves budget for the offer's lifetime.
2. `AcceptOffer(offer_id, attempt_ref, task_spec, input_manifest_digest)` creates a **remote attempt** with a lease (5 min).
3. Input transfer (§6). The executor starts the attempt automatically when inputs are complete and its admission grants the reservation.
4. `WatchRemoteAttempt(remote_attempt_id, cursor)` streams states, output chunks, segments, sample summaries and the final result. The origin mirrors them into its task record.
5. `RenewAttemptLease` every 60 s. `CancelRemoteAttempt` cancels. `ReleaseRemoteAttempt` frees the remote workspace when retention ends.
6. Output return (§6). The origin applies declared outputs inside the declared output paths only, comparing each file with its base recorded at submission. Files changed locally are handled per `output_conflict`: `STAGE` (default), `SKIP_EXISTING`, `FAIL`, or `OVERWRITE` for HUMAN or SCRIPT callers only. Returned outputs never delete local files.

**Environment on the executor.** `inherit=CALLER` becomes `inherit=NODE` on the executor, because origin paths are not portable. Explicit `set` entries are transferred. Path-like values that point inside the origin workspace are rewritten to the remote workspace root, and the record shows each rewrite.

## 6. Transfer (`peer.v1.TransferService`)

- **Input manifest:**
  - git workspaces: `git ls-files -s` (tracked) plus `git ls-files --others --exclude-standard` (untracked, not ignored), restricted to declared `inputs.include` and `inputs.exclude` globs;
  - other workspaces: a walk with globs.

  Each entry is `{path, mode, size, sha256}`. Digests come from the `file_digest_cache` (path, size, mtime, file ID → digest). The manifest itself is content-addressed.
- **Output bases.** At submission the origin also records, for every path matched by `declared_outputs`, its current digest or "absent". These are the bases for conflict detection when outputs return.
- **Executor pull:**
  1. The executor calls `PutManifest` on itself.
  2. It computes what is missing against its CAS and the remote workspace's current manifest.
  3. It pulls blobs from the origin with `DownloadBlob` (server stream, 4 MiB chunks, SHA-256 verified per blob, resumable by offset).
  4. It leases a **workspace slot** for the attempt: `work/remote/<origin_node>/<origin_workspace>/<slot>/` (R-LAN-011).
     - A free slot is reused and brought to the new manifest incrementally. Files absent from the manifest are deleted inside that slot only.
     - If every slot of the origin workspace is leased, a new slot is created, up to `lan.max_workspace_slots` (default 2). Beyond that, the remote attempt stays `RESERVED` until a slot frees, and the offer's ETA includes the wait.
     - A slot belongs to exactly one remote attempt, from materialization until its outputs have been pulled or the attempt is released. Concurrent attempts from the same origin workspace therefore never share a writable directory.
     - Materialization copies from the CAS, or block-clones where the file system supports it (Windows ReFS/Dev Drive `FSCTL_DUPLICATE_EXTENTS_TO_FILE`, Linux `FICLONE`). It never hardlinks, because builds that write in place would corrupt the stored blob and every workspace sharing it.
- **Outputs** return in reverse: the executor builds a manifest of the declared outputs, and the origin pulls the blobs into `staging/transfer/`. While the attempt runs remotely, the task holds no keys at the origin. To apply the outputs, the origin takes, exclusively, the keys of the output paths and the tool keys the task's adapter emits, for example `tool:dotnet:<w>` for a placed .NET build ([03](03-resource-control.md) §4). Directory keys alone would not exclude a local build that holds a tool key, so no local managed task writes or reads those outputs meanwhile. For each file it compares the current local digest with the base recorded at submission:
  - **unchanged** (or absent both times): atomic replace, through a temporary file and a rename;
  - **changed locally**, per `output_conflict`:
    - `STAGE` (default) writes the returned file to `out/<workspace>/<task>/<attempt>/conflicts/<path>`, keeps the local file and raises `OUTPUT_CONFLICT`;
    - `SKIP_EXISTING` keeps the local file;
    - `FAIL` applies nothing if any file conflicts;
    - `OVERWRITE` replaces it, and only HUMAN or SCRIPT callers may choose it.

  Returned outputs never delete local files. The attempt result records the applied, conflicted and skipped counts and the staging path (`AttemptResult.outputs`).
- **Limits:** a manifest has at most 2 million entries; a single transfer at most 100 GiB. Both are configurable. All traffic stays on the peer connection and never routes through the cloud (R-LAN-006).

## 7. Failure, ownership and versions

| Event | Behaviour |
|---|---|
| Origin disconnects | The remote attempt continues. The origin re-watches from its cursor when it reconnects. |
| Origin silent beyond the lease | The executor applies `lease_expiry_action`: `FINISH_AND_RETAIN` (default; results kept 7 days) or `CANCEL` |
| Executor unreachable beyond the lease | The origin marks the attempt `LOST` (`effect=UNKNOWN`) and retries elsewhere only if the task is retryable (R-LAN-007) |
| Executor preempts (local policy or pressure) | `PREEMPTED`; retryable tasks are re-placed |
| Origin cancels | `CancelRemoteAttempt`; the executor runs the cancellation sequence ([04](04-execution.md) §6) |
| Protocol mismatch | Handshake `Hello` exchanges `{min, max, features}`; incompatible peers are shown `INCOMPATIBLE` with the versions needed (R-LAN-009) |

**Ownership.** The task stays owned by the origin and the attempt by the executor ([AD-0004](../decisions/AD-0004-contracts-and-state.md)). The executor's local user can always see, pause or cancel remote attempts on their machine (R-LAN-008).

## 8. No subscription gating

LAN discovery, pairing, placement and cache sharing are free and need no account, entitlement or cloud connection ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2). Per-peer policy ([AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) §5) alone decides what each paired peer may do.

## 9. WSL guests are not LAN peers

The host–guest link uses the `wsl.exe` bridge and `peer.v1.GuestLinkService` over a byte stream ([03](03-resource-control.md) §6). A guest appears in the UI as part of its host machine.

- **Discovery.** The host lists WSL2 distributions (`wsl.exe --list --verbose`). For each running one, it checks for the guest binary at `~/.local/share/arcforges/app/current/arcforges` or `/usr/bin/arcforges`, using `wsl.exe -d <distro> --exec test -x <path>`.
- **Trust.**
  - **The bridge.** The host launches the bridge as the same Windows user. The guest node accepts the bridge only from its own uid (`SO_PEERCRED`).
  - **First link (trust on first use).** The host generates a 32-byte link token, stored in the Windows Credential Manager (under `--test-mode` without the OS secret-store opt-in, in the isolated test backend: [02](02-node-service.md) §4), and sends it with its node ID. The guest pins that host node ID and the token's hash (`host_link`).
  - **Later links** must present the same host and token. A link from a different host is refused and recorded (`ResourceService.GetHostLink`). The user accepts the new host inside the guest with `arcforges guests trust-host <host-node-id>` (`TrustHost`, HUMAN and interactive only); its next link is then pinned as on first use.
- **No pairing.** Guests are never paired as LAN peers.
