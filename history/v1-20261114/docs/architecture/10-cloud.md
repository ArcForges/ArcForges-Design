# 10 — Cloud

Decisions: [AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md), [AD-0010](../decisions/AD-0010-commerce-and-entitlements.md), [AD-0011](../decisions/AD-0011-identity-and-login.md). Contracts: `arcforges.fleet.v1`, `arcforges.relay.v1`, and the reused `arcforges.publicapi.v1`. Persistence: [data/cloud-store.md](../data/cloud-store.md).

**Current delivery (2026-11-09; [AD-0021](../decisions/AD-0021-central-access-go-center.md)).** The Go center on PostgreSQL serves its own account and node-enrollment surfaces. AF-CTR-04 is complete, including mobile native authorization (Cloud #141/#142 and ArcForges #70/#71); production stays dark. AF-CTR-05's merged Cloud parts E0–E3 and node parts N1–N3 implement the node channel, Fleet registry, routed task methods and local CLI proxy. The checked-in E3 proof target prepares `relay,nodes` while retaining `identity,pages,operations,fleet,mobile`; this is not evidence of an E3 hosted deployment. Signed hosted and Windows-to-Linux device acceptance remains NOT PROVEN under the owner/mock exception. Viewer streams, routed files/workspaces, MCP and push are later work.

The Worker remains a thin edge adapter, and node connections terminate in the Go center rather than a per-account `FleetHub` Durable Object. A call for an offline target is refused; the center holds no envelope queue. The center derives its pages and URLs from its configured public base URL. The configured limits in §5 are operating bounds and illustrative owner placeholders, not approved plan prices or allowances.

## 1. Components

**Current implementation.** The Worker routes the binary gRPC-Web methods and passes the node WebSocket upgrade through the Container Durable Object; the center authenticates its credential. The Go center runs the `hub` and Fleet routing over PostgreSQL; the Durable Object provides Container lifecycle and socket proxying, not a per-account Fleet hub. The production Worker keeps the flagship surface list empty. The following original C#/D1 and FleetHub component table is historical design, not the currently deployed center:

| Component | Implementation | Responsibility |
|---|---|---|
| Worker ingress (existing) | Cloud `worker/ingress/*` (TypeScript, thin) | Routes binary gRPC-Web business calls to the C# host. Applies edge limits. Serves provider webhook routes. |
| Relay routes (new) | Cloud `worker/relay/*` (TypeScript, thin) | `GET /v1/node` and `GET /v1/view` WebSocket upgrades. Token verification (HMAC-SHA256, audience, expiry, scope). Forwards to the account's `FleetHub` DO. |
| `FleetHub` Durable Object (new) | Cloud `worker/relay/fleet-hub.ts` (thin) | One per account. Hibernating WebSockets for nodes and viewers. Routes frames, keeps bounded latest-state caches, enforces token-carried limits, forwards envelopes to and from the C# host, guards its own alarm loop (AD-0009 §7). |
| C# host (existing) | Cloud `ArcForges.Cloud` (Containers, Native AOT) | All business logic |
| D1 (storage layer existing; production database to be provisioned) | Cloud `ArcForges.Cloud.Storage.D1` | Account, registry, entitlement, commerce, commands, audit |
| R2 (bucket to be provisioned) | Release artifacts, support uploads | Static release manifests (`releases.arcforges.com`), support bundles (consented) |
| Queue (to be provisioned) | The wake-queue pattern of Cloud's `proof` environment (`WAKE_QUEUE`, with a dead-letter queue) | Wakes the C# host for queued background work (outbox dispatch, jobs) |

**Historical production bindings proposal.** At Cloud main `92ba1dc9`, only the `proof` environment of `wrangler.json` declares D1, R2 and Queue bindings, and `crons` is empty. AF-CLD-01 adds a repository provisioning script that creates the D1 database, the R2 bucket (with the lifecycle rules of §3.11) and the Queue, and the binding definitions it writes. The production `wrangler.json` receives those bindings only during production activation (§8), with the user's approval (H-20). AF-CLD-04 adds the `FleetHub` Durable Object class and its migration (no external resource), and AF-PLAT-01 the cron trigger.

**Historical viewer transport proposal (not built; AF-CLD-04).** Viewers (web, Android) receive live fleet state over a **WebSocket to `FleetHub` carrying `arcforges.relay.v1.ViewerFrame` protobuf messages**, not over a gRPC-Web stream. A streaming HTTP response would keep the Durable Object awake and billed for the stream's lifetime, while hibernating WebSockets do not (V-C01). The frames and the snapshot/delta/cursor semantics are the same contract the gRPC-Web method `FleetService.WatchFleet` defines. `WatchFleet` stays available as a gRPC-Web server stream for clients that cannot use WebSockets, and is served by the C# host with a 10-minute lifetime cap (R-API-004).

## 2. C# modules

*Historical baseline and planned reuse.* The Go center now owns delivered identity, device, entitlement and fleet operations. The C# and D1 table below describes the earlier baseline and later target modules, not the implementation of the node channel or routed task calls.

**Baseline reality** (Cloud main `92ba1dc9`, checked 2026-10-12):
- The host serves only `HelloService` over gRPC.
- **Identity** holds user and credential domain rules and its D1 store (enrollment), but no authentication ceremonies, sessions, step-up, recovery or deletion endpoints.
- **Entitlement** holds the resolver, snapshots and grants, but no service endpoints.
- **Audit, Commerce, Configuration, Devices, Notification, Support and TrustSafety** are empty placeholders.
- The D1 schema for all of them exists.

"Reuse" below therefore means the **contracts, D1 schema and domain code that exist**. Every endpoint and flow marked *new work* is built by the named task.

| Module | What is reused | New work (task) |
|---|---|---|
| Identity | Contracts (`publicapi.v1.IdentityService`), D1 tables, user and credential domain rules and store | WebAuthn ceremonies, e-mail codes, cookie and native-bearer sessions with refresh rotation, step-up (AF-CTR-03). E-mail goes through a provider adapter: Postmark, with Amazon SES as fallback, the historical Cloud design's choice. Delivered by AF-CTR-03 (Cloud #127): both adapters (Postmark over HTTPS, Amazon SES over SMTP with TLS) behind one sender, tested against local doubles (MOCKED) and by two REAL probes that deliver nothing (Postmark's API accepted a request with its public test token; an SES endpoint's TLS handshake up to AUTH); e-mail is disabled in every deployed environment, and no account can hold an e-mail identity yet (the center enrolls passkeys only, and the browser channel offers passkeys only), so no real account can be mailed until e-mail enrollment is delivered (AF-ID-02). The provider account and sending domain are prerequisite H-19; tests use `FakeMailSender` (Cloud's `mail.Fake`, and the local Postmark and SMTP servers of `center/internal/mail/mailtest`), and live delivery is AR-14. Recovery, account deletion with grace, data export (`DataService`), security activity (AF-ID-02). New: an `account` session approves node sign-ins and device codes; phone sessions are scoped (§3.3). |
| Devices | Contracts (`DeviceService`, product and platform are strings), D1 tables | Register (AF-ID-02); list (AF-CTR-03, Cloud #118); rename, revoke and the revocation cascade (AF-CTR-03, Cloud #120); the remaining cascade participants register in their own tasks (agent grants, AF-CTR-07; push registrations, AF-CLD-06; [cloud-store](../data/cloud-store.md) §6). Product values `arcforges-node`, `arcforges-mobile` and `arcforges-web` (one device record per browser installation that signs in to the center's pages or the Web profiles; [AD-0021](../decisions/AD-0021-central-access-go-center.md) §7). Each node is its own device record (cloud-store §3); a Linux node a user runs in WSL2 is an ordinary node ([AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md)). |
| Fleet | **New** (`ArcForges.Cloud.Modules.Fleet`) | `NodeEnrollmentService`: native sign-in (PKCE loopback), device authorization, phone pairing, relay tokens, entitlement tokens (node certificates and LAN hints are reserved for roadmap RM-01 and not served in release 1). `FleetService`: node list, rename, revoke, snapshots, viewer grants, remote commands. Relay envelope processing. |
| Entitlement | Resolver, snapshots, grants (implemented), D1 tables | `EntitlementService` endpoints, plan catalogue for the flagship, entitlement-token claim projection (AF-CLD-03) |
| Commerce | Contracts (`CommerceService`), D1 tables, the historical Paddle design (BC-01) | Paddle provider: catalogue, checkout attempts, verified webhooks, subscription lifecycle, customer portal, refunds, billing history (AF-COM-01). Google Play provider: `StoreBillingService`, RTDN, acknowledgement job (AF-CLD-07). |
| Notification | Contracts (`NotificationService`), D1 tables, the historical FCM HTTP v1 design | Implemented by AF-CLD-06: `List`, `Acknowledge`, `RegisterPush`, `UnregisterPush`, the FCM HTTP v1 sender with short-lived service-account tokens. Push kinds `node.task_failed`, `node.task_finished`, `node.approval_needed`, `node.offline`, `node.finding`; batching from relay envelopes; preferences per kind and node (`FleetService.GetPushPreferences` and `UpdatePushPreferences`, table `fleet_push_preference`) |
| Support | Contracts (`SupportService`), D1 tables | Cases, messages and access grants, plus consented support-bundle attachments (R2 object keys) (AF-SUP-01) |
| Audit | D1 tables | Audit event writer and reader for enrollment, revocation, remote commands, commerce and operator actions (AF-PLAT-01) |
| Platform | Implemented in the D1 storage layer: command receipts and the command guard, the commit tail (outbox publisher, inbox, outbox and archive purge plans), and the shared-families `lease` guard (holder and fence). Schema only: `platform_job_lease`, operating budgets and reservations. | AF-PLAT-01: job lease and fence plans (reusing the shared `lease` guard), a job runner started by a Worker cron trigger, scheduled retention sweeps (expired receipts, inbox rows, flows and the cloud-store retention schedule) and the compact command fence; the operating-budget service and budget checks on metered paths. |
| Configuration | D1 `config_revision` | Configuration revisions, kill switches (`relay.live_streaming`, `relay.new_connections`, `push.enabled`, `fleet.commands`) and limits (AF-PLAT-01). The operator console comes in AF-OPS-01. |
| Chat, Task, Agent, Sync, Resource, Search, Scope, PackageCatalog, TrustSafety, Policy | Retain (unused) | Not composed into the flagship host profile. Their tables stay untouched. |

## 3. Flows

### 3.1 Native node sign-in (browser, PKCE loopback; R-AUTH-001)

*Restated 2026-11-05 as built by AF-CTR-04: the center by Cloud #130, #132 and #135, the node by ArcForges #63 and #69. The center's full rules are Cloud `docs/center-fleet.md`, "Browser sign-in"; `<center>` below is the center's public base URL, for example `https://arcforges.com/api`.*

1. The node binds its loopback receiver, then calls `NodeEnrollmentService.BeginNodeSignIn{code_challenge (S256), redirect_uri=http://127.0.0.1:<port>/callback (or http://[::1]:<port>/callback), state, node, node_public_key}` without a credential. It receives `{flow_id, authorize_url, expires_at (10 min)}`. A key that an installation holds or held is refused before approval (`CONFLICT/already_exists`, `state.state` `node_key`); the node replaces its key once and begins again, so a sign-in after a sign-out brings a new key. A newer Begin of the same node ID and key expires that node's PENDING flows.
2. `authorize_url` is `<center>/connect#flow=<flow_id>` (the flow ID in the fragment, in its lower-case 8-4-4-4-12 form). The node derives it from the center it captured at the flow's start and requires an exact match: otherwise the flow fails (`VALIDATION/invalid_argument`, `center_url_mismatch`) and nothing is opened or printed. It opens only the derived URL in the system browser. The center serves `/connect` itself (surface `fleet`; [web](../experience/web.md), "Center pages"): the account signs in, reviews the node as the node describes itself (`GetNodeSignInFlow`) and decides within 10 minutes of its review. An approval needs a step-up of class `fleet.approveNodeSignIn` bound to the flow ID; a denial needs none. An approval issues a one-use code (2 minutes by default, never past the flow), and the result page carries the link back to the node's receiver, `<redirect_uri>?code=<code>&state=<state>` (after a denial `?error=access_denied&state=<state>`), which the page's script follows after checking its exact shape. The browser must run on the computer that runs the node.
3. The node calls `CompleteNodeSignIn{flow_id, code, code_verifier, node_key_proof}` without a credential. The node key proof is ES256 (low-S) over a fixed prefix, the purpose `0x01`, the SHA-256 of the center's public base URL, the node ID, the flow ID and the code. The node receives the node credential (`NodeCredentials`: tokens of scope `node`, the access lifetime, the family's absolute end, the installation, the account's ID, display name and masked e-mail address, and the center's published keys; no entitlement token), and an `arcforges-node` installation is registered. The optional `csr` field and the certificate chain are reserved for account-based LAN trust (roadmap RM-01).

**The node's receiver and flow** (ArcForges #69). The receiver binds `127.0.0.1` (`[::1]` only when IPv4 cannot bind) on a port the center admits (1024..65535). It accepts exactly the center's two redirects: `GET /callback` with the code and state or with `error=access_denied` and state, exactly one `Host` equal to its own authority, no other or repeated key, no `%`, no body, the state compared in constant time. Any other request is answered 400 and does not end the flow. Each connection has one 5 s deadline for its request; once 8 connections are idle (no complete request line, nothing to read, older than one second), a new connection closes the oldest idle one, and at a hard cap of 256 open connections a new one closes the oldest that has not completed its request. The answer is a static page without script, and the receiver then stops. The verifier is 48 random bytes and the state 32, both fresh for every Begin. One flow runs at a time; it lives in memory, so a node restart cancels it.

**Failure states:** the user denies (the flow ends `DENIED`); the flow expires, or the approval lapsed because the approving session was revoked, an epoch of it moved or the account is no longer Active (`STATE/expired`); the loopback port cannot be bound (the node falls back to device authorization, `fell_back_to_device_code`), while a browser that does not open is only a warning (`browser_not_opened`); a correct code with a wrong verifier or key proof revokes the flow; the code presented again is refused (`CONFLICT/code_reused`) and revokes the credentials the flow delivered, so the node never sends a Complete again once its body may have reached the center (`complete_reply_lost`: it signs in again).

### 3.2 Device authorization (headless; R-AUTH-001)

*Restated 2026-11-05 as built by AF-CTR-04: the center by Cloud #130, #134 and #135, the node by ArcForges #69. The center's full rules are Cloud `docs/center-fleet.md`, "Device-code sign-in".*

1. `StartDeviceAuthorization{node, node_public_key}`, without a credential, returns `{device_code, user_code (8 letters of BCDFGHJKLMNPQRSTVWXZ, shown XXXX-XXXX), verification_uri <center>/activate, verification_uri_complete <center>/activate#code=XXXX-XXXX, interval 5 s, expires_in 600}`. The node derives both URIs and requires an exact match, as in 3.1; the held-key refusal and the expiry of PENDING authorizations by a newer Start of the same node ID and key are as for Begin.
2. The user opens the URI on any device (the CLI prints the URI, the code, the center's host and the node key's fingerprint with its last group named; there is no terminal QR, decision Q19 of AF-CTR-04), signs in, enters the code (case and separators ignored) or follows the complete URI, and reviews the node (`LookupDeviceCode`). On `/activate` the page withholds the fingerprint's last group, which the person types from the node's own output. Within 10 minutes of the lookup the account approves, with a step-up of class `fleet.approveDeviceCode` bound to the code, or denies, without one.
3. The node calls `PollDeviceAuthorization{device_code, node_key_proof}` (the proof as in 3.1 with the purpose `0x02` over the device code) and gets `PENDING`, `SLOW_DOWN`, `APPROVED` (with credentials as in 3.1, delivered once), `DENIED` or `EXPIRED`. A poll after the delivery is a reuse: it is answered `COMPLETED` without credentials and revokes the delivered family. A poll earlier than its interval less 500 ms is `SLOW_DOWN`, and the interval grows by 5 s up to 60 s. The node polls one at a time, the first poll one interval after Start and each next one an interval after the previous reply, never more often than every 5 s nor less often than every 60 s; it takes the interval of a `SLOW_DOWN` reply and stops after 630 s.

**Code entries** (decision Q8 as built). A live code admits 5 lookups; the sixth and later are `VALIDATION/code_invalid` (`device_code_lookups`), and the authorization stays `PENDING`. Malformed input costs nothing. Every other entry reserves one unit of the account's budget (`device_entry_account`, 5 per 15 minutes) and one of the network's (`device_entry_prefix`, 20 per 15 minutes). Only a lookup that shows the node (a `PENDING`, unexpired code with fewer than 5 lookups) and a decision made (or a decision of a reviewed code refused for its step-up or the node cap) give both back; every other entry keeps them, a spent code's sixth lookup among them. Once either budget is spent, every entry, a right one too, is `RESOURCE/rate_limited` until its window ends. There is no per-code attempt counter. Steps 2 and 3 and these rules supersede AD-0011 §2 ("a QR") and §7 ("5 attempts per code") by the AF-CTR-04 Plan decisions Q19 and Q8, as the amended [AD-0011](../decisions/AD-0011-identity-and-login.md) records.

### 3.3 Phone sign-in by QR from a signed-in node (R-AUTH-002)

*Future design, not served by AF-CTR-04 or AF-CTR-05.*

1. The Desktop asks the node to call `CreatePhonePairing{}` and gets `{pairing_id, qr = "arcforges://pair?i=<pairing_id>&s=<secret>", expires_at (120 s)}`.
2. The phone scans and calls `ClaimPhonePairing{pairing_id, secret, phone_installation_info}`, and the state becomes `AWAITING_CONFIRMATION`.
3. The Desktop (polling `GetPhonePairing`, or through a node event) shows "Allow <phone model> to sign in as <account>?". The user calls `ConfirmPhonePairing{pairing_id, approve}`.
4. The phone polls `PollPhonePairing{pairing_id, claim_token}` and receives a session with scope `mobile.limited` for its own installation (product `arcforges-mobile`).
5. Medium- and high-risk actions, billing and account settings require a step-up on the phone (reused `IdentityService.BeginStepUp`/`CompleteStepUp`), which upgrades the session to `account`. A stolen node credential can therefore never yield account control (AD-0011 §3, T-19).

Each secret is single-use. A wrong secret consumes the pairing.

### 3.4 Relay connection (node)

A signed-in node opens `GET <center>/fleet/v1/node` with its node credential and subprotocol `arcforges.relay.v1`. The Worker checks the upgrade route and forwards it unchanged; the Go center authenticates, applies the `center.nodes` entitlement after authorization and audit, and upgrades. Its 32-byte connection-specific challenge must be signed by the key of that credential's installation, with matching node and installation IDs, within 10 seconds. Only a proved replacement may close the old connection (4409). `ChannelAccepted` carries its connection ID, current signing key IDs and limits; frames carry a per-connection sequence.

The hub sends a heartbeat every 25 seconds, closes on 60 seconds of silence and fences presence writes with the singleton PostgreSQL hub lease (renewed every 10 seconds, 30-second TTL). The node sends `TokenRefresh` after a credential rotation on the same connection; the center rechecks session, installation and node, and closes on revocation or entitlement lapse. Close codes and the node's 1–60 second jittered backoff, refresh-first 4401 handling and REFUSED retry after one hour or a subsequent credential rotation are in [SM-RELAY](../state-machines/README.md#sm-relay). The proxy's open socket keeps a Container instance and Durable Object active; actual cost remains an owner decision (H-09/H-06).

### 3.5 Viewer watch (web, Android)

*Historical proposal, not built.* Viewer streams and telemetry are AF-CLD-04; the node channel above does not implement this FleetHub viewer design.

1. The client calls `FleetService.OpenFleetWatch{node_ids (empty = all), detail: SUMMARY | FULL}`. C# authorizes the account session, checks entitlement `remote.view` and limits, and returns `{grant (aud=relay.view, 10 min), ws_url}`.
2. The client connects to `wss://relay.arcforges.com/v1/view`. Browsers cannot set headers on WebSockets, so every viewer sends the grant as a subprotocol: `Sec-WebSocket-Protocol: arcforges.v1, grant.<base64url grant>`. The Worker validates the grant **before** routing to the Durable Object, so unauthenticated sockets never wake it, and answers with the subprotocol `arcforges.v1`. Grants never appear in URLs. `FleetHub` sends `ViewerFrame.snapshot` for the permitted nodes from its cache. If `detail=FULL` and a cached snapshot is older than 10 s, it sends `DemandSignal{interval 2 s, duration 10 min}` to each node, and the nodes then stream `StatusDelta` frames, which the DO fans out.
3. Each frame carries `{node_id, node_seq, generation}`. The client resumes after reconnect by sending `ViewerResume{cursors}`. A gap beyond the cache yields `reset` plus a snapshot.
4. The grant is refreshed through `OpenFleetWatch` before expiry, sent as a `GrantRefresh` frame.

### 3.6 Center-routed tasks (R-CLOUD-004)

The Go center serves `SubmitNodeTask`, `GetNodeTask`, `ListNodeTasks`, `WaitNodeTask`, `ReadNodeTaskOutput` and `CancelNodeTask` on `nodes`. A caller uses an account session or a node credential only as a verified node relay. For a relayed call the local node signs an assertion over the exact inner request digest, identity, target, method, command ID and a one-use center nonce. The center authenticates and authorizes, applies resource controls, appends `access.authorized`, then asks the appropriate feature gate (`center.execute`, `remote.view`, or `remote.control`). An account-session Submit or Cancel requires fresh, target-bound step-up on each actual delivery; the relay is confined by target policy instead. A lapsed account can still list and revoke its nodes.

The hub signs each call with its loaded ES256 command key. The target checks the signature, target, expiry and local center-routed policy before dispatching to its existing TaskService; it signs the result with its node key. The center verifies the result against the exact transmitted bytes. A disconnected target with no possible prior delivery is `STATE/node_offline`, with no store-and-forward buffer; if an earlier mutation may have reached it, the refusal preserves `UNKNOWN` instead. A read has no routing record. Submit and Cancel use `fleet.routed_call` keyed by account and command ID; it stores IDs, metadata, state, lengths and digests, never argv, environment, output or request/response bytes ([cloud store](../data/cloud-store.md#6-postgresql-model-ad-0021)).

A mutation that may have reached the target and lacks a verified outcome is `UNKNOWN`, never silently treated as not executed. Same-command retry preserves the original inner bytes and ID; the node's deduplication converges on the original outcome. A possible-delivery replay outside the configured window is `STATE/invalid_state` `replay_window_passed`, and a mismatching replayed result is `STATE/node_unreachable` `replay_digest_differs`; neither authorizes a fresh command ID. See [SM-ROUTED-CALL](../state-machines/README.md#sm-routed-call) and [CLI](../experience/cli.md#c-01-run-and-tasks). The historical `SendNodeCommand`/FleetHub envelope and its legacy wire-state machine are unbuilt and retained only for compatibility.

### 3.7 Push (R-CLOUD-005)

*Historical proposal, not built; AF-CLD-06 owns the push sender.*

1. Nodes send `EventBatch` frames for push-worthy events when the user enabled them on that node.
2. `FleetHub` batches them and forwards to C# immediately for `approval_needed`, and every 30 s otherwise.
3. C# Notification applies preferences, deduplication (`notification_suppression`) and limits (≤50 per day per account by default), then sends FCM HTTP v1 data messages to the account's registered `arcforges-mobile` installations (the historical push design, V-C07; the sender is new work in AF-CLD-06).

### 3.8 Entitlement token (R-COM-004)

*Historical future design, not served:* current node credentials carry no entitlement token; the Go center gates each channel and routed call.

`RefreshEntitlementToken{}` (node credential) returns a compact ES256-signed token (`SignedBlob` with `EntitlementClaims`): `{acct, node, plan, features[], issued_at, not_after (14 days), revoked_nodes[] (reserved for RM-01, empty in release 1), kid}`. It describes cloud features only; local and LAN features never check it ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2). Nodes refresh it every 24 h while online. Public keys ship in releases, and `GetEntitlementKeys` serves rotations.

### 3.9 Google Play (R-COM-002)

*Future design, not served by AF-CTR-05.*

As in [AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §3:
- RTDN arrives at `POST /hooks/play-rtdn` as a Pub/Sub push with an authenticated OIDC token, verified in C# (`aud`, `email` of the Pub/Sub service account).
- It is stored in `fleet_play_notification` (deduplicated by message ID) and processed by a job that re-reads `subscriptionsv2`.
- The acknowledgement job runs with a platform job lease and retries until success or an operator alert at 24 h.

### 3.10 Paddle (AF-COM-01)

`POST /hooks/paddle`: verify the raw body HMAC, dedup through the platform inbox, then apply the subscription state to the reused commerce tables. The Paddle provider follows the historical adapter design (BC-01); its implementation is new.

### 3.11 Support bundle upload (R-OPS-005)

*Future design, not served by AF-CTR-05.*

1. After the user reviews the file list and consents, the node calls `NodeEnrollmentService.BeginSupportUpload` (node credential) with the case reference (or a new case subject), file name, size and SHA-256.
2. C# checks the plan's daily upload limit and the `support uploads` kill switch, creates the case if needed, and returns an R2 presigned PUT URL for the key `support-pending/<upload_id>`, valid for 15 minutes. C# signs it with SigV4 using a bucket-scoped R2 S3 API credential (prerequisite H-16), for the declared length and SHA-256 checksum where R2 enforces them (A-C03). Step 4 verifies both in any case.
3. The node uploads the bundle directly to R2 over HTTPS; the bytes never pass through the Container.
4. The node calls `CompleteSupportUpload`. C# verifies the pending object's size and checksum, copies it server-side to `support-bundles/<case_id>/<upload_id>`, deletes the pending object, then appends a case message whose `diagnostic` reference names the final object.
5. R2 lifecycle rules work by prefix: objects under `support-pending/` are deleted after 1 day (uploads never completed), and objects under `support-bundles/` after 30 days.

## 4. Durable Object layout (`FleetHub`)

*Historical proposal, not built:* the current per-center Go hub and PostgreSQL lease replace this per-account Durable Object design.

| Key | Content | Bound |
|---|---|---|
| `n/<node>/sum` | Latest `StatusSummary` bytes | 4 KiB per node |
| `n/<node>/snap` | Latest full snapshot bytes (when demanded) | 256 KiB per node |
| `n/<node>/chg` | Ring of the last 100 summary changes | 100 × 4 KiB |
| `n/<node>/cmd/<id>` | Pending command envelopes | 20 per node, ≤8 KiB each |
| `up/batch` | Outbound envelope batch to C# | 256 KiB |
| `wake/<hour>` | Wake counter for the alarm-loop guard | — |

All values are opaque bytes plus small headers. Socket attachments hold `{kind, id, exp, limits}` (≤1 KiB).

## 5. Limits and cost controls (R-CLOUD-006)

The delivered bounds are configuration and safety limits, not subscription prices or approved plan allowances. H-07 remains open. Cloud `docs/center.md`, `docs/center-identity.md` and `docs/center-fleet.md` are the implementation-level sources.

| Bound | Current default and scope |
|---|---|
| Node connections | 256 per center process, configurable 1–4096; separate from the per-account enrollment cap (default 100, configurable 1–1000). There is no additional per-account connected-node cap. |
| Channel | 1 MiB/frame; 8 in-flight calls per node; 25 s heartbeats and 60 s deadline. |
| Routed controls | 3,600 calls/account/hour and 16 in-flight/account; 600 upgrades/account/hour and 60/node/hour. These are illustrative policy defaults, not plan limits. |
| Routing | Submit inner request at most 253,952 bytes; other routed requests 3,072 bytes; node reply at most 1,040,384 bytes. Wait is at most 50 seconds and output long-poll at most 20 seconds. |
| Replay | 23-hour default, configurable from 1 hour to 23 hours 52 minutes; node command deduplication is 24 hours. |
| Signing keys | At most eight private bindings loaded by a relay process; published public sets have no eight-key cap. Supported registration checks the entire sign-in, poll and refresh reply against the fleet's 65,536-byte transport bound, including framing and trailer allowance. Validity is at most 400 days; a successor overlaps currently valid keys by at least seven days. |

The node channel keeps the hosted Container and proxy Durable Object active while connected. A cost ceiling and commercial limits are owner decisions, not implemented plan tiers; the older per-account FleetHub viewer, push and operating-budget ladder remain future design.

## 6. Failure handling

| Failure | Current routed behavior |
|---|---|
| Target is offline before any possible delivery | `STATE/node_offline`, `DID_NOT_HAPPEN`; the center does not queue a request. |
| Connection or center lost after a mutation may have reached the node | `STATE/node_unreachable`, `UNKNOWN` with same-command retry; never claim no effect and never create a new command ID solely because the reply is missing. Reads and mutations never delivered are `DID_NOT_HAPPEN`. |
| Replay window passed | `STATE/invalid_state` `replay_window_passed`, `DID_NOT_HAPPEN` for this delivery but the original command may have run; inspect the named task where known. |
| Credential revoked | The affected node channel closes 4401 after committed revocation; accepted tasks already running remain on the node. |
| Clock skew or expiry | The node checks the signed expiry with the configured 120-second skew; an expired call is not executed late. |

The former FleetHub cache, D1 outbox and offline-envelope retry behavior in earlier revisions is not implemented.

## 7. Observability

*The following original dashboard and cost dimensions are target work; current hub and routing audit events are documented in Cloud `docs/center-fleet.md`.*

- Structured logs (C# and Worker) with correlation IDs.
- Metrics:
  - relay sockets, frames, bytes, wakes;
  - command latency and outcomes;
  - sign-in funnel;
  - Play and Paddle webhook latency and errors;
  - push sends and failures;
  - operating-budget consumption.
- Health endpoints per component.

Runbooks are in [14-commercial-operations.md](14-commercial-operations.md) (R-OPS-006).

## 8. Production activation

Implementation delivery and production activation are separate steps ([AD-0014](../decisions/AD-0014-delivery-method.md) §9):
- **Dark deploys.** The Cloud and Web repositories keep deploying on every main push through their guarded scripts, and flagship features ship **disabled**:
  - **Cloud:** `FLAGSHIP_SURFACES` is empty in production. Actual supported names are `identity`, `pages`, `operations`, `fleet`, `mobile`, `relay` and `nodes`. `fleet` needs `identity,pages`; `mobile` needs them and a valid issuer; `relay` needs `identity,fleet` and a valid loaded command key; `nodes` needs `identity,fleet,relay`. The protected E3 proof target is `identity,pages,operations,fleet,mobile,relay,nodes`, but its checked-in configuration is not evidence of a hosted E3 run. The last AF-CTR-04 proof deployment included the first five. The Worker forwards the enabled set to the Go center and refuses disabled routes before waking the Container. Self-hosted defaults admit the available surfaces and omit `mobile` for an invalid issuer, or `relay,nodes` when no command key is configured. `operations` is official-hosted only.
  - **Web:** the repository's deploy configuration holds the switches `public_site`, `web_account` and `web_fleet`, all off. While a switch is off, the guarded deploy keeps publishing the current pages and leaves that part out, so nothing new becomes visible.
- **No production prerequisites at merge.** Implementation tasks are verified on the local cloud stack ([16](16-testing-strategy.md) §3.1). They never need production key material, domains or provisioned resources. The guarded Cloud main-push path may apply PostgreSQL migrations while the production surfaces remain disabled; activation and owner-only integrations remain separate.
- **Activation** (Plan task AF-PROD-01, after the release candidate) needs the user's approval and these prerequisites:

  | Surface | Prerequisites |
  |---|---|
  | Core: provisioning, `identity`, `pages` (the center's account pages; needs `identity`), `fleet`, `mobile`, `relay`, `nodes` | H-05 (domains), H-06 (account settings), H-09 (the cost ceiling the production budgets derive from), H-16 (key material), H-19 (transactional e-mail for sign-in codes and security notices), H-20 (provisioning) |
  | `support` | The core, and the R2 credential of H-16 |
  | `push` | The core, and H-03 (Firebase) |
  | `commerce` | The core, H-01 (Paddle) and, for Play, H-02, with H-07 (prices) and the published legal pages (H-10) |
  | `public_site`, `web_account`, `web_fleet` | H-05 and, for the public site, H-10 |

  A surface whose prerequisites are missing stays off and is recorded; it does not hold back the others. The steps:
  1. provision the resources with the repository script;
  2. the user stores the key material;
  3. add the production bindings;
  4. run the migrations;
  5. set the production operating budgets from the cost ceiling ([14](14-commercial-operations.md) §7.2 and §7.4);
  6. enable the surfaces one at a time, each with a production smoke check;
  7. publish the public site and the web profiles after the user approves their content.

  Provisioning runs the repository script with the user's approval, and the user stores the key material; every other step is a reviewed main-push deploy or a configuration activation. Removing a surface from the switch list withdraws it.
- **Real-world acceptance** stays in the acceptance register (AR-05 to AR-09, AR-14).
