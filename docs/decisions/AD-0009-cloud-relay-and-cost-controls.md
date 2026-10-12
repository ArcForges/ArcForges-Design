# AD-0009 — Cloud relay, remote control, push and cost controls

- Status: Accepted (2026-10-12)
- Evidence: V-C01–V-C04

## Decision

1. **Live connections terminate in hibernating Durable Objects, not in the C# container.**
   - One `FleetHub` Durable Object per account holds node uplinks and viewer streams, using the WebSocket Hibernation API (V-C01).
   - The C# host (Containers, V-C02) runs only for business operations: authorization, entitlement, commands, audit, commerce, push. It sleeps when idle.
2. **Thin TypeScript adapter boundary.** The relay Durable Object and Worker may only:
   - verify signed tokens (HMAC-SHA256 with a key shared with the C# host through secret bindings) for expiry, audience and scope;
   - route frames between sockets of the same account;
   - keep a bounded per-node latest-snapshot cache (opaque protobuf bytes) and a bounded per-viewer queue;
   - enforce rate and size limits taken from the signed token;
   - forward envelopes to and from the C# host over the existing internal container route.

   They make no authorization decision beyond token validation, and never inspect business payloads beyond frame headers.
3. **Tokens.**
   - **Node token** (`relay.node`, 15 min): issued by C# `FleetService.IssueRelayToken` to an enrolled node with a valid device credential. It carries account, node, rate limits and allowed frame kinds.
   - **Viewer grant** (`relay.view`, 10 min): issued by C# `FleetService.OpenFleetWatch` after authorization and entitlement checks. It carries account, permitted node IDs, detail level and rate limits.
   - Both are refreshed before expiry. A revoked device or an entitlement loss stops refresh, and the DO closes the sockets at expiry.
4. **Demand-driven telemetry (R-CLOUD-003).**
   - Without viewers, a node sends presence (WebSocket ping, which does not wake the DO) and summary changes, at most one summary per 60 s.
   - When a viewer subscribes, the DO sends the node a `DemandSignal` with interval (≥2 s) and duration (≤10 min, renewed while watched), and the node streams snapshot deltas at that rate.
   - Command lines, environment and output are never sent unless a viewer explicitly requests the output tail of a task and the node's privacy policy allows it (R-OPS-003).
5. **Remote commands (R-CLOUD-004).**
   - The client calls `FleetService.SendNodeCommand`.
   - C# then: authenticates; checks entitlement; applies the command risk class (low: refresh, pause/resume queue; medium: cancel task, change priority; high: run new command, cleanup, change policy); requires step-up or confirmation for medium and high; writes `fleet_remote_command`; and audits.
   - C# signs the command envelope with the account relay key and sends it through the DO.
   - The node verifies the signature, the expiry (≤5 min) and its **local remote-control policy** (default: low allowed; medium needs the local policy flag; high disabled), executes, and returns a signed result. C# records the outcome.
   - A command not delivered within its expiry becomes `EXPIRED` and is never executed late.
6. **Push.** Node events that matter (approval needed, task failed or finished, node offline, finding raised) reach C# as batched envelopes. The existing Notification module applies user preferences, deduplication and rate limits, and sends FCM HTTP v1 data messages (R-CLOUD-005).
7. **Cost controls are application-enforced (V-C04).**
   - **Per account:** maximum nodes, viewers, frames per minute, bytes per day, commands per hour, push per day and support uploads per day. These are taken from the plan catalogue and enforced in C# (token claims) and in the DO (token-carried limits).
   - **Global:** operating budgets per resource class, using the reused `platform_operating_budget` and `platform_operating_reservation`. **Kill switches** in the configuration module can disable live streaming (degrading to on-demand snapshots), push, or new relay connections within one token lifetime.
   - **DO alarm-loop guard:** alarms are scheduled only with bounded backoff, and the DO counts its own wake-ups per hour against a ceiling. When the ceiling is exceeded it closes non-essential sockets and stops scheduling alarms until the next hour.
   - Cloudflare budget alerts are configured as notification only and are never counted as enforcement.
8. **Storage choices.**
   - D1 holds the account, device and node registry, entitlement, commerce, remote commands and audit (V-C03).
   - Live status lives only in DO memory and storage (bounded: latest snapshot per node, last 100 summary changes).
   - Execution history stays on nodes. No telemetry time series is stored in D1.
