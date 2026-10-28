# 10 — Cloud

Decisions: [AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md), [AD-0010](../decisions/AD-0010-commerce-and-entitlements.md), [AD-0011](../decisions/AD-0011-identity-and-login.md). Contracts: `arcforges.fleet.v1`, `arcforges.relay.v1`, and the reused `arcforges.publicapi.v1`. Persistence: [data/cloud-store.md](../data/cloud-store.md).

**Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) (target until each AF-CTR task is delivered).** The C# host of §1–§2 becomes the Go center (`center/` in the Cloud repository) on Neon/PostgreSQL; D1 is no longer the center's store; the Worker stays a thin adapter and passes node WebSocket upgrades and MCP requests to the Container. Node connections terminate in the Go center (§3.4 and §4 describe the earlier `FleetHub` design, kept as history; a per-account Durable Object hub is exploratory roadmap EX-28). Remote commands (§3.6) become center-routed calls under the node's local policy; each routed call is signed by the center with the ES256 command-signing key and verified by the node, as AD-0021 §10 states (AF-CTR-05). The per-node envelope buffer of §3.6 is not built: a call for an offline node is refused. The center serves its own sign-in, `/connect` and `/activate` pages so that self-hosted centers need no Web deployment, and derives every URL from its configured public base URL. The limits of §5 are current settings to assess, not decided prices or allowances. Surfaces deploy dark (§8) under the same activation rule, with the center's surfaces (`identity`, `fleet_api`, the node channel, `mcp`).

## 1. Components

| Component | Implementation | Responsibility |
|---|---|---|
| Worker ingress (existing) | Cloud `worker/ingress/*` (TypeScript, thin) | Routes binary gRPC-Web business calls to the C# host. Applies edge limits. Serves provider webhook routes. |
| Relay routes (new) | Cloud `worker/relay/*` (TypeScript, thin) | `GET /v1/node` and `GET /v1/view` WebSocket upgrades. Token verification (HMAC-SHA256, audience, expiry, scope). Forwards to the account's `FleetHub` DO. |
| `FleetHub` Durable Object (new) | Cloud `worker/relay/fleet-hub.ts` (thin) | One per account. Hibernating WebSockets for nodes and viewers. Routes frames, keeps bounded latest-state caches, enforces token-carried limits, forwards envelopes to and from the C# host, guards its own alarm loop (AD-0009 §7). |
| C# host (existing) | Cloud `ArcForges.Cloud` (Containers, Native AOT) | All business logic |
| D1 (storage layer existing; production database to be provisioned) | Cloud `ArcForges.Cloud.Storage.D1` | Account, registry, entitlement, commerce, commands, audit |
| R2 (bucket to be provisioned) | Release artifacts, support uploads | Static release manifests (`releases.arcforges.com`), support bundles (consented) |
| Queue (to be provisioned) | The wake-queue pattern of Cloud's `proof` environment (`WAKE_QUEUE`, with a dead-letter queue) | Wakes the C# host for queued background work (outbox dispatch, jobs) |

**Production bindings.** At Cloud main `92ba1dc9`, only the `proof` environment of `wrangler.json` declares D1, R2 and Queue bindings, and `crons` is empty. AF-CLD-01 adds a repository provisioning script that creates the D1 database, the R2 bucket (with the lifecycle rules of §3.11) and the Queue, and the binding definitions it writes. The production `wrangler.json` receives those bindings only during production activation (§8), with the user's approval (H-20). AF-CLD-04 adds the `FleetHub` Durable Object class and its migration (no external resource), and AF-PLAT-01 the cron trigger.

**Viewer transport.** Viewers (web, Android) receive live fleet state over a **WebSocket to `FleetHub` carrying `arcforges.relay.v1.ViewerFrame` protobuf messages**, not over a gRPC-Web stream. A streaming HTTP response would keep the Durable Object awake and billed for the stream's lifetime, while hibernating WebSockets do not (V-C01). The frames and the snapshot/delta/cursor semantics are the same contract the gRPC-Web method `FleetService.WatchFleet` defines. `WatchFleet` stays available as a gRPC-Web server stream for clients that cannot use WebSockets, and is served by the C# host with a 10-minute lifetime cap (R-API-004).

## 2. C# modules

**Baseline reality** (Cloud main `92ba1dc9`, checked 2026-10-12):
- The host serves only `HelloService` over gRPC.
- **Identity** holds user and credential domain rules and its D1 store (enrollment), but no authentication ceremonies, sessions, step-up, recovery or deletion endpoints.
- **Entitlement** holds the resolver, snapshots and grants, but no service endpoints.
- **Audit, Commerce, Configuration, Devices, Notification, Support and TrustSafety** are empty placeholders.
- The D1 schema for all of them exists.

"Reuse" below therefore means the **contracts, D1 schema and domain code that exist**. Every endpoint and flow marked *new work* is built by the named task.

| Module | What is reused | New work (task) |
|---|---|---|
| Identity | Contracts (`publicapi.v1.IdentityService`), D1 tables, user and credential domain rules and store | WebAuthn ceremonies, e-mail codes, cookie and native-bearer sessions with refresh rotation, step-up (AF-ID-01). E-mail goes through a provider adapter: Postmark, with Amazon SES as fallback, the historical Cloud design's choice. The provider account and sending domain are prerequisite H-19; development uses `FakeMailSender`, and live delivery is AR-14. Recovery, account deletion with grace, data export (`DataService`), security activity (AF-ID-02). New: an `account` session approves node sign-ins and device codes; phone sessions are scoped (§3.3). |
| Devices | Contracts (`DeviceService`, product and platform are strings), D1 tables | Register, list, rename, revoke and cascade (AF-ID-02). Product values `arcforges-node` and `arcforges-mobile`. Each node is its own device record (cloud-store §3); a Linux node a user runs in WSL2 is an ordinary node ([AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md)). |
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

1. The node calls `NodeEnrollmentService.BeginNodeSignIn{code_challenge (S256), redirect_uri=http://127.0.0.1:<port>/callback, node_info}`. It receives `{flow_id, authorize_url, expires_at (10 min)}`.
2. The node opens `authorize_url` (`https://arcforges.com/connect?flow=<id>`) in the system browser. The web profile authenticates the user (existing flows) and shows "Connect ArcForges node <name> (<os>) to <account>?". On approval, the C# host issues a one-use code bound to the flow and redirects to the loopback URI.
3. The node calls `CompleteNodeSignIn{flow_id, code, code_verifier}` and receives `{node credential (refresh token, scope node), account summary, entitlement token}`. The installation is registered (`NODE`). The optional `csr` field and the certificate chain are reserved for account-based LAN trust (roadmap RM-01).

**Failure states:** the user denies (`ACCESS_DENIED`); the flow expires; the loopback port is unavailable (the node falls back to device authorization); the code is reused (refused, and the flow is revoked).

### 3.2 Device authorization (headless; R-AUTH-001)

1. `StartDeviceAuthorization{node_info}` returns `{device_code, user_code (8 characters, alphabet BCDFGHJKLMNPQRSTVWXZ), verification_uri https://arcforges.com/activate, verification_uri_complete, interval 5 s, expires_in 600}`.
2. The user opens the URI (or scans the QR), signs in, enters or confirms the code and approves.
3. The node calls `PollDeviceAuthorization{device_code}` and gets `PENDING`, `SLOW_DOWN` (the interval grows by 5 s), `APPROVED` (with credentials as in 3.1), `DENIED` or `EXPIRED`. There are 5 code-entry attempts per user code (AD-0011 §7).

### 3.3 Phone sign-in by QR from a signed-in node (R-AUTH-002)

1. The Desktop asks the node to call `CreatePhonePairing{}` and gets `{pairing_id, qr = "arcforges://pair?i=<pairing_id>&s=<secret>", expires_at (120 s)}`.
2. The phone scans and calls `ClaimPhonePairing{pairing_id, secret, phone_installation_info}`, and the state becomes `AWAITING_CONFIRMATION`.
3. The Desktop (polling `GetPhonePairing`, or through a node event) shows "Allow <phone model> to sign in as <account>?". The user calls `ConfirmPhonePairing{pairing_id, approve}`.
4. The phone polls `PollPhonePairing{pairing_id, claim_token}` and receives a session with scope `mobile.limited` for its own installation (product `arcforges-mobile`).
5. Medium- and high-risk actions, billing and account settings require a step-up on the phone (reused `IdentityService.BeginStepUp`/`CompleteStepUp`), which upgrades the session to `account`. A stolen node credential can therefore never yield account control (AD-0011 §3, T-19).

Each secret is single-use. A wrong secret consumes the pairing.

### 3.4 Relay connection (node)

1. The node calls `IssueRelayToken{}` with its node credential and gets `{token, expires_at (15 min), relay_url}`. The token claims: `aud=relay.node`, `acct`, `node`, `kinds_allowed`, `limits {frames_per_min, bytes_per_day, snapshot_max_bytes}` and `kid`.
2. The node opens `wss://relay.arcforges.com/v1/node` with header `Authorization: Bearer <token>`. The Worker verifies the token and routes to `FleetHub(acct)`, which calls `acceptWebSocket` with attachment `{kind: node, node, limits, exp}`.
3. The node sends `NodeHello`, `StatusSummary` (≤4 KiB) and then summary changes (≤1 per 60 s), with WebSocket pings every 30 s; pings do not wake the DO.
4. The node refreshes the token at 2/3 of its lifetime with a `TokenRefresh` frame. At expiry without refresh, the DO closes the socket with code 4401.

### 3.5 Viewer watch (web, Android)

1. The client calls `FleetService.OpenFleetWatch{node_ids (empty = all), detail: SUMMARY | FULL}`. C# authorizes the account session, checks entitlement `remote.view` and limits, and returns `{grant (aud=relay.view, 10 min), ws_url}`.
2. The client connects to `wss://relay.arcforges.com/v1/view`. Browsers cannot set headers on WebSockets, so every viewer sends the grant as a subprotocol: `Sec-WebSocket-Protocol: arcforges.v1, grant.<base64url grant>`. The Worker validates the grant **before** routing to the Durable Object, so unauthenticated sockets never wake it, and answers with the subprotocol `arcforges.v1`. Grants never appear in URLs. `FleetHub` sends `ViewerFrame.snapshot` for the permitted nodes from its cache. If `detail=FULL` and a cached snapshot is older than 10 s, it sends `DemandSignal{interval 2 s, duration 10 min}` to each node, and the nodes then stream `StatusDelta` frames, which the DO fans out.
3. Each frame carries `{node_id, node_seq, generation}`. The client resumes after reconnect by sending `ViewerResume{cursors}`. A gap beyond the cache yields `reset` plus a snapshot.
4. The grant is refreshed through `OpenFleetWatch` before expiry, sent as a `GrantRefresh` frame.

### 3.6 Remote command (R-CLOUD-004)

1. The client calls `FleetService.SendNodeCommand{node_id, command (oneof), meta.command_id}`.
2. C# then:
   - authenticates the session;
   - checks entitlement `remote.control`;
   - classifies risk (AD-0009 §5);
   - requires a step-up (passkey or recent authentication) for `MEDIUM` and `HIGH`;
   - writes `fleet_remote_command` (`ACCEPTED`, `expires_at` = now + 5 min);
   - audits;
   - signs the `NodeCommand` payload (`fleet.v1`) with the ES256 **command signing key** (ECDSA P-256; `kid`; V-N05).
3. C# posts the envelope to the internal relay route (HMAC-authenticated container-to-Worker route, existing coordination pattern). `FleetHub` delivers it if the node is connected. Otherwise it stores the envelope (≤20 per node) and delivers it on reconnect if it has not expired.
4. The node verifies the signature (public keys from enrollment and updates), the expiry, the target, and its local remote-control policy. It executes through its own API with origin `REMOTE`, and replies with a `NodeCommandResult` (receipt or error), signed ES256 with its node key. For `ReadOutputTail` the result carries only the tail's SHA-256 and size. The tail itself goes to the requesting viewer as a relay `OutputTail` frame (node → DO → viewer) and is never stored in D1 or Durable Object storage (R-OPS-003).
5. `FleetHub` forwards the result envelope to C#, which updates the command (`SUCCEEDED`, `FAILED`, `REJECTED_BY_NODE`) and audits. Viewers see the update. Undelivered commands become `EXPIRED`.

### 3.7 Push (R-CLOUD-005)

1. Nodes send `EventBatch` frames for push-worthy events when the user enabled them on that node.
2. `FleetHub` batches them and forwards to C# immediately for `approval_needed`, and every 30 s otherwise.
3. C# Notification applies preferences, deduplication (`notification_suppression`) and limits (≤50 per day per account by default), then sends FCM HTTP v1 data messages to the account's registered `arcforges-mobile` installations (the historical push design, V-C07; the sender is new work in AF-CLD-06).

### 3.8 Entitlement token (R-COM-004)

`RefreshEntitlementToken{}` (node credential) returns a compact ES256-signed token (`SignedBlob` with `EntitlementClaims`): `{acct, node, plan, features[], issued_at, not_after (14 days), revoked_nodes[] (reserved for RM-01, empty in release 1), kid}`. It describes cloud features only; local and LAN features never check it ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2). Nodes refresh it every 24 h while online. Public keys ship in releases, and `GetEntitlementKeys` serves rotations.

### 3.9 Google Play (R-COM-002)

As in [AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §3:
- RTDN arrives at `POST /hooks/play-rtdn` as a Pub/Sub push with an authenticated OIDC token, verified in C# (`aud`, `email` of the Pub/Sub service account).
- It is stored in `fleet_play_notification` (deduplicated by message ID) and processed by a job that re-reads `subscriptionsv2`.
- The acknowledgement job runs with a platform job lease and retries until success or an operator alert at 24 h.

### 3.10 Paddle (AF-COM-01)

`POST /hooks/paddle`: verify the raw body HMAC, dedup through the platform inbox, then apply the subscription state to the reused commerce tables. The Paddle provider follows the historical adapter design (BC-01); its implementation is new.

### 3.11 Support bundle upload (R-OPS-005)

1. After the user reviews the file list and consents, the node calls `NodeEnrollmentService.BeginSupportUpload` (node credential) with the case reference (or a new case subject), file name, size and SHA-256.
2. C# checks the plan's daily upload limit and the `support uploads` kill switch, creates the case if needed, and returns an R2 presigned PUT URL for the key `support-pending/<upload_id>`, valid for 15 minutes. C# signs it with SigV4 using a bucket-scoped R2 S3 API credential (prerequisite H-16), for the declared length and SHA-256 checksum where R2 enforces them (A-C03). Step 4 verifies both in any case.
3. The node uploads the bundle directly to R2 over HTTPS; the bytes never pass through the Container.
4. The node calls `CompleteSupportUpload`. C# verifies the pending object's size and checksum, copies it server-side to `support-bundles/<case_id>/<upload_id>`, deletes the pending object, then appends a case message whose `diagnostic` reference names the final object.
5. R2 lifecycle rules work by prefix: objects under `support-pending/` are deleted after 1 day (uploads never completed), and objects under `support-bundles/` after 30 days.

## 4. Durable Object layout (`FleetHub`)

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

| Limit | Free | Pro | Enforced at |
|---|---|---|---|
| Nodes per account (relay) | 0 | 10 | `IssueRelayToken` |
| Concurrent viewers | 0 | 5 | `OpenFleetWatch` + DO |
| Node frames per minute | — | 30 (summary), 60 (delta while demanded) | DO (token claim) |
| Relay bytes per account per day | — | 500 MiB | DO counter, C# budget |
| Remote commands per hour | — | 120 | C# |
| Push per account per day | — | 50 | C# Notification |
| Support bundle uploads per day | 1 | 5 | C# Support |
| DO wakes per hour per account | — | 3,600 | DO guard |

**Global operating budgets** (`platform_operating_budget`) cover every billable dimension of the products in use, per UTC day ([14](14-commercial-operations.md) §7.1). Exceeding 80% raises operator alerts. At 100% the degradation ladder of [14](14-commercial-operations.md) §7.3 applies: live streaming off, then existing relay sockets closed and new ones refused, push batched then stopped, uploads refused, and finally essential-only mode, in which the Worker answers non-essential routes without waking the container. The residual exposure is computed and shown (§7.4 there). Budget alerts from Cloudflare are informational (V-C04).

## 6. Failure handling

| Failure | Behaviour |
|---|---|
| Container cold or unavailable | The Worker returns `UNAVAILABLE` with retry advice. Relay sockets keep working with cached data. Commands queue in the C# outbox when the container returns. |
| D1 overloaded (V-C03) | C# returns `RESOURCE` + `retry after`. Command submission is idempotent by `command_id`. |
| DO restart or eviction | Sockets survive hibernation. On a real restart, nodes reconnect with jittered backoff (1 s → 60 s) and re-send their summaries. |
| Clock skew | Tokens allow ±60 s. Commands carry a server-issued expiry checked against node time ±120 s, and the record notes the skew when detected. |

## 7. Observability

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
  - **Cloud:** the Worker variable `FLAGSHIP_SURFACES` in `wrangler.json` lists the enabled surfaces (`identity`, `fleet_api`, `relay`, `push`, `support`, `commerce`); it is empty by default. It is a deployment setting, not a D1 configuration revision, because the production D1 binding does not exist until activation, and it changes only through a reviewed main-push deploy. A disabled surface is answered by the Worker with `STATE/not_activated`, without waking the container. While no surface is enabled, the scheduled (cron) handler returns at once, so nothing wakes the container.
  - **Web:** the repository's deploy configuration holds the switches `public_site`, `web_account` and `web_fleet`, all off. While a switch is off, the guarded deploy keeps publishing the current pages and leaves that part out, so nothing new becomes visible.
- **No production prerequisites at merge.** Implementation tasks are verified on the local cloud stack ([16](16-testing-strategy.md) §3.1). They never need production key material, domains or provisioned resources. Until activation, the production migration step reports "not applicable" (no D1 binding), and readiness lists the flagship modules as "not provisioned".
- **Activation** (Plan task AF-PROD-01, after the release candidate) needs the user's approval and these prerequisites:

  | Surface | Prerequisites |
  |---|---|
  | Core: provisioning, `identity`, `fleet_api`, `relay` | H-05 (domains), H-06 (account settings), H-09 (the cost ceiling the production budgets derive from), H-16 (key material), H-19 (transactional e-mail for sign-in codes and security notices), H-20 (provisioning) |
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
