# AD-0008 — LAN: discovery, trust, placement, transfer and caches

- Status: Accepted (2026-10-12; revised after the independent review the same day: SAS bound to certificate fingerprints, listener access rule, copy or reflink for remote workspaces; revised 2026-10-13 after the findings review: per-attempt workspace slots, output conflict detection, TLS 1.3 platform floor; revised 2026-10-13 by the product owner's decisions (AD-0015): LAN free; account-based trust and hints deferred (RM-01))

## Decision

1. **Discovery is not trust.** Nodes advertise `_arcforges._tcp.local` through DNS-SD:
   - Windows uses `DnsServiceRegister` and `DnsServiceBrowse` (V-T04).
   - Linux uses an in-process C# mDNS responder and browser on UDP 5353, which works without Avahi (L-11).

   Users may also add peers by `host:port`. Account-assisted hints through the cloud are accepted future work (roadmap RM-01). Removal events are unreliable on Windows, so entries expire by TTL (120 s) unless refreshed.
2. **Node identity.** Each node generates an ECDSA P-256 key at first start (non-exportable where the OS allows). Its self-signed certificate carries `node_id` in the subject alternative name.
3. **Trust comes from local pairing.**
   - **Local pairing:** two nodes run a commitment-based exchange over a TLS session. Each side checks that the certificate fingerprints claimed in the exchange equal the certificates presented in that TLS session. Both displays show a 6-digit short authentication string derived from the nonces and both fingerprints; the user confirms on both, and each pins the other's certificate fingerprint. A man in the middle presents its own certificates, so the two sides compute different strings. .NET 10 offers no TLS exporter (V-N05), so none is used.
   - **Account trust is deferred** (roadmap RM-01): node certificates issued by an account CA in ArcForges Cloud, so that nodes of one account trust each other without pairing. The contracts keep the reserved RPCs (`NodeEnrollmentService.IssueNodeCertificate`, `GetLanHints`, `ReportLanEndpoints`), which release 1 does not serve.

   LAN **pairing, placement and cache sharing are free** and need no account, entitlement or cloud connection ([AD-0015](AD-0015-direction-editions-roadmap.md) §2). A newly paired peer gets the status-only policy until the user widens it (item 5). WSL guests are not LAN peers and need no pairing: they link to their host through the bridge (03 §6).
4. **Transport.** gRPC over HTTP/2 with mutual TLS 1.3 on a configurable TCP port (default 47820). TLS 1.3 needs Windows 11 on Windows (Schannel; V-N06), which is the platform floor ([AD-0002](AD-0002-platform-scope.md)).
   - **At the TLS handshake:** the listener accepts any well-formed client certificate, so that unpaired nodes can pair.
   - **After the handshake:** a gRPC interceptor admits unpaired identities only to `PeerHandshakeService.Hello` and `PairingService`. Every other service requires a pinned (paired) identity, and a blocked identity gets nothing.
5. **Per-peer policy.** Each peer has these settings:
   - allow placement to it, and accept placement from it;
   - accept cache read and accept cache write;
   - maximum CPU and memory share offered;
   - allowed toolchains and command patterns;
   - approval required, and data classes allowed to leave (source, outputs, logs).

   The default for a newly paired peer is status-only.
6. **Placement.** The origin node scores candidates: local, and peers whose policy allows placement and whose offer meets the constraints. The score combines constraint fit, offered free resources, estimated duration from operational memory, transfer cost (input bytes not already on the peer), cache warmth (matching compatibility keys on the peer) and the current queue.
   - The origin requests **offers** (`PlacementService.RequestOffer`, valid 30 s with a reservation token), accepts the best, and falls back to the local queue if none qualify.
   - Only **separate tasks** are placed. A single process never spans machines (R-LAN-010).
7. **Transfer.**
   - Inputs travel as a content-addressed manifest (path, mode, size, SHA-256) of the workspace view the task needs. It is computed from the git index and working tree with declared includes and excludes, or from an explicit path set.
   - The executor requests missing blobs (`TransferService`, 4 MiB chunks, verified digests) and materializes them into a **workspace slot** leased by that one remote attempt. Slots are kept per origin workspace for incremental reuse (at most `lan.max_workspace_slots`, default 2), so concurrent attempts never share a writable directory. Files are copied, or block-cloned where the file system supports it (ReFS/Dev Drive duplicate extents, Linux `FICLONE`). They are never hardlinked to the content store, because a build that writes in place would corrupt the stored blob.
   - Declared outputs return the same way and are applied with conflict detection against the digests recorded at submission. Files changed locally in the meantime are staged and reported by default, never silently overwritten ([09](../architecture/09-lan.md) §6). Logs stream live through the attempt stream.
   - LAN data never routes through the cloud (R-LAN-006).
8. **Failure and ownership.**
   - A remote attempt keeps running when the origin disconnects. The origin resumes the attempt stream by cursor.
   - The executor holds a lease renewed by the origin (default 5 min). If the origin disappears beyond the lease, the executor applies its policy: finish and retain results (default), or cancel.
   - If the executor disappears beyond the lease, the origin marks the attempt `LOST`, and retries elsewhere only if the task is retryable.
   - The executor's local policy may refuse or preempt remote work at any time. Preemption is reported as `PREEMPTED`.
9. **Shared caches.**
   - A node may serve its sccache and ccache stores to peers through an authenticated **WebDAV-compatible endpoint** over the same mTLS listener (`/cache/<cache_id>/`). This uses standard client configuration: `SCCACHE_WEBDAV_ENDPOINT` (V-T02), and ccache HTTP remote storage or a helper (V-T03).
   - The serving node enforces quotas and read/write policy.
   - NuGet and Cargo package caches are not shared over the LAN in this scope. Each node keeps its own shared local cache, and duplicate downloads across nodes are reported.
10. **Versioning.** The peer handshake exchanges protocol version ranges and feature flags. Incompatible peers are shown as `INCOMPATIBLE` with the required versions.
