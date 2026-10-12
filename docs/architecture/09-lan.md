# 09 — LAN: discovery, pairing, placement and transfer

Decision: [AD-0008](../decisions/AD-0008-lan-trust-and-placement.md). Contracts: `arcforges.peer.v1` ([contracts](../contracts/proto/arcforges/peer/v1/peer.proto)).

## 1. Listener and identity

- The listener is TCP `0.0.0.0:47820` (configurable; IPv6 dual-stack where available). Kestrel HTTPS uses TLS 1.3 only and requires a client certificate. It is enabled when the user turns on LAN features. WSL2 mirrored networking exposes the guest on the LAN (L-12), but guest nodes do **not** open a LAN listener by default: their LAN presence is through the host node.
- **Node key:** ECDSA P-256. On Windows it is stored as a CNG key with export disabled, in the user profile. On Linux it is a 0600 PKCS#8 file in the data root. The self-signed certificate SAN contains `URI:arcforges:node:<node_id>`.
- **Account certificate (Pro, signed in):**
  1. The node submits a CSR to `NodeEnrollmentService.IssueNodeCertificate`.
  2. The cloud's **ArcForges Node Issuing CA** returns a 30-day certificate with SAN `URI:arcforges:node:<node_id>` and `URI:arcforges:account:<account_id>`.
  3. The node renews at 2/3 of its lifetime.

  Revoked node IDs arrive with every entitlement token refresh (≤24 h) and every relay connection.

## 2. Discovery

| Mechanism | Detail |
|---|---|
| DNS-SD | Service `_arcforges._tcp.local`, instance `<node name>`. TXT records: `id` (node ID, base32), `v` (protocol range, for example `1-1`), `fp` (first 16 hex digits of the certificate SHA-256), `acct` (first 8 hex digits of the account-ID hash, or `-`), `tls=1`. Windows registers and browses with `DnsServiceRegister`/`DnsServiceBrowse` (V-T04). Linux uses the in-process responder and browser (RFC 6762/6763 subset: PTR, SRV, TXT, A, AAAA; probing; announcements; TTL 120 s). |
| Manual | `PeerService.AddPeerAddress(host, port)` |
| Account hints (Pro) | `NodeEnrollmentService.GetLanHints` returns same-account nodes' last LAN endpoints and fingerprints |
| Advertisement control | Policy `lan.advertise` (default true while LAN features are on) |

Discovered peers appear as `DISCOVERED` (untrusted) and are never used until paired (R-LAN-001).

## 3. Pairing

### 3.1 Same account (Pro)

Both nodes hold account certificates for the same `account_id`. After the mTLS handshake validates the chain, the account SAN and the revocation list, the peer is `PAIRED (ACCOUNT)`. No confirmation is needed, because both nodes are already enrolled by the same signed-in user. The default policy is status-only until the user widens it.

### 3.2 Local confirmation (Free and Pro; any two nodes)

1. A user starts pairing on node A for discovered peer B (`PeerService.BeginPairing`). B shows an incoming request to its user, which can be accepted or rejected.
2. A opens a TLS connection to B using self-signed certificates, unverified for now.
3. The commitment exchange (`peer.v1.PairingService`, all over that TLS session):
   1. A sends `commit = SHA-256(nonce_A ‖ fp_A ‖ exporter)`, where `exporter` = TLS exported keying material (label `"EXPORTER-arcforges-pairing"`, 32 bytes).
   2. B sends `nonce_B` and `fp_B`.
   3. A reveals `nonce_A` and `fp_A`, and B verifies the commitment.
4. Both compute `SAS = uint32(HMAC-SHA-256(nonce_A ‖ nonce_B, fp_A ‖ fp_B ‖ exporter ‖ "arcforges-pairing-v1")[0..4]) mod 1,000,000`, shown as six digits.
5. Both users confirm the digits match (`ConfirmPairing`). Each node pins the other's certificate fingerprint, and the peer becomes `PAIRED (PINNED)`.
6. Mismatch, rejection or a 120 s timeout aborts the pairing. Five failed attempts per peer per hour block it (R-LAN-002).

### 3.3 Revocation

`PeerService.RemovePeer` unpins locally and notifies the peer when it is reachable. Account revocation propagates through the CA revocation list.

## 4. Peer policy and status

`PeerPolicy`:
- `allow_place_to`, `accept_from`;
- `cache_read`, `cache_write`;
- `max_cpu_share` and `max_mem_share` (fractions of the peer's managed budget offered to us, set by that peer);
- `allowed_toolchains[]`, `allowed_command_patterns[]`;
- `require_approval`;
- `data_out` = `{source, outputs, logs}`.

The default for a new pairing is status only. `PeerStatusService.WatchStatus` streams the peer's capabilities, toolchains, enforcement state, budget summary and queue length (D0/D1 data) (R-LAN-004).

## 5. Placement

### 5.1 Scoring

For each task with `placement=ANY` (or naming a node), the origin computes for each candidate `c` (local, and peers whose policy allows):

```
eligible(c) = constraints met (os, arch, toolchains, labels) ∧ policy allows ∧ peer reachable ∧ compatible protocol
score(c) = w_t · est_start_delay(c) + w_d · est_duration(c) + w_x · transfer_seconds(c) − w_c · cache_warmth(c)
  est_start_delay: from the candidate's offer (queue ETA)
  est_duration: operational memory DURATION p50 scaled by the candidate's CPU class (relative benchmark score exchanged at pairing)
  transfer_seconds: (input bytes the candidate lacks) / measured LAN throughput (EWMA of past transfers, default 50 MB/s)
  cache_warmth: share of the task's cache bindings for which the candidate holds a matching compat_key cache with hits in the last 7 days
defaults: w_t = w_d = w_x = 1 (seconds), w_c = 60 s × cache_warmth
choose argmin(score); local wins ties.
```

Placement is re-evaluated only before start. Running attempts never migrate (R-LAN-005).

### 5.2 Protocol (`peer.v1.PlacementService`)

1. `RequestOffer` takes a task summary (sanitized per `data_out`), demand, requirements, input byte estimate and priority. It returns an `Offer` (`offer_id`, `accept_by` 30 s, queue ETA, reservation, `missing_toolchains[]`, `cache_warmth`). The executor reserves budget for the offer's lifetime.
2. `AcceptOffer(offer_id, attempt_ref, task_spec, input_manifest_digest)` creates a **remote attempt** with a lease (5 min).
3. Input transfer (§6). The executor starts the attempt automatically when inputs are complete and its admission grants the reservation.
4. `WatchRemoteAttempt(remote_attempt_id, cursor)` streams states, output chunks, segments, sample summaries and the final result. The origin mirrors them into its task record.
5. `RenewAttemptLease` every 60 s. `CancelRemoteAttempt` cancels. `ReleaseRemoteAttempt` frees the remote workspace when retention ends.
6. Output return (§6). The origin materializes declared outputs per `output_conflict` (`OVERWRITE`, `SKIP_EXISTING` or `FAIL`), default `OVERWRITE` inside declared output paths only.

**Environment on the executor.** `inherit=CALLER` becomes `inherit=NODE` on the executor, because origin paths are not portable. Explicit `set` entries are transferred. Path-like values that point inside the origin workspace are rewritten to the remote workspace root, and the record shows each rewrite.

## 6. Transfer (`peer.v1.TransferService`)

- **Input manifest:**
  - git workspaces: `git ls-files -s` (tracked) plus `git ls-files --others --exclude-standard` (untracked, not ignored), restricted to declared `inputs.include` and `inputs.exclude` globs;
  - other workspaces: a walk with globs.

  Each entry is `{path, mode, size, sha256}`. Digests come from the `file_digest_cache` (path, size, mtime, file ID → digest). The manifest itself is content-addressed.
- **Executor pull:**
  1. The executor calls `PutManifest` on itself.
  2. It computes what is missing against its CAS and the remote workspace's current manifest.
  3. It pulls blobs from the origin with `DownloadBlob` (server stream, 4 MiB chunks, SHA-256 verified per blob, resumable by offset).
  4. It materializes the remote workspace `work/remote/<origin_node>/<origin_workspace>/` by hardlinking from the CAS on the same volume (copying otherwise), and deletes files absent from the manifest inside that directory only.
- **Outputs** use the same mechanism in reverse, origin pulling.
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

## 8. Gating

- Placement needs the origin account's entitlement `lan.placement`.
- Accepting placements needs the executor account's entitlement `lan.accept`.
- Cache serving and consuming need `lan.cache`.

Each is verified offline from the signed entitlement token ([AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §5). Pairing and status viewing are free.

## 9. WSL guests are not LAN peers

The host–guest link uses the `wsl.exe` bridge and `peer.v1.GuestLinkService` over a byte stream ([03](03-resource-control.md) §6). Trust is established by the host launching the bridge as the same user plus a link token, not by pairing. A guest appears in the UI as part of its host machine.
