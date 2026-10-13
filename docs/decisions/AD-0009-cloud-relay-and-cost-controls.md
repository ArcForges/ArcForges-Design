# AD-0009 — Cloud relay, remote control, push and cost controls

- Status: Accepted (2026-10-12; revised 2026-10-13 after the findings review: complete billing dimensions, structural bounds, degradation ladder, residual exposure)
- Evidence: V-C01–V-C04, V-C08

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
   - C# then: authenticates; checks entitlement; applies the command risk class of `fleet.v1.NodeCommandBody`:
     - low: refresh, pause or resume a queue, read an output tail;
     - medium: cancel a task, change a priority;
     - high: run a task, decide an approval, set parallelism (a policy change), apply an update, stop the node.

     There is no remote cleanup or general policy editing.
   - The C# host requires a step-up or confirmation for medium and high commands, writes `fleet_remote_command`, and audits.
   - C# signs the command payload with the ES256 command key (V-N05) and sends it through the DO.
   - The node verifies the signature, the expiry (≤5 min) and its **local remote-control policy** (default: low allowed; medium needs the local policy flag; high disabled), executes, and returns a signed result. C# records the outcome. Output tails travel only as relay frames to the requesting viewer and are never stored (R-OPS-003).
   - A command not delivered within its expiry becomes `EXPIRED` and is never executed late.
6. **Push.** Node events that matter (approval needed, task failed or finished, node offline, finding raised) reach C# as batched envelopes. The Notification module applies user preferences, deduplication and rate limits, and sends FCM HTTP v1 data messages (R-CLOUD-005).
7. **Cost controls are application-enforced (V-C04).**
   - **Per account:** maximum nodes, viewers, frames per minute, bytes per day, commands per hour, push per day and support uploads per day. These are taken from the plan catalogue and enforced in C# (token claims) and in the DO (token-carried limits).
   - **Global:** operating budgets for **every billable dimension** of the products in use, including duration-based charges: container instance time (provisioned memory and disk accrue while an instance runs) and Durable Object active duration. They use the existing `platform_operating_budget` and `platform_operating_reservation` tables, with the budget service built by AF-PLAT-01 ([14](../architecture/14-commercial-operations.md) §7.1).
   - **Structural bounds** in the deployment: `max_instances`, the instance type and the idle `sleepAfter` for containers, `limits.cpu_ms` for Workers, and hibernation for every WebSocket.
   - **Degradation ladder:** live streaming off; existing relay sockets closed and new ones refused; push batched, then stopped; uploads refused; essential-only mode, in which the Worker answers non-essential routes without waking the container. It stops ongoing billable activity, not only new connections ([14](../architecture/14-commercial-operations.md) §7.3).
   - **Residual exposure** that no switch can stop (essential requests, storage at rest, logs, edge traffic) is computed as a daily worst case and shown to operators ([14](../architecture/14-commercial-operations.md) §7.4).
   - **DO alarm-loop guard:** alarms are scheduled only with bounded backoff, and the DO counts its own wake-ups per hour against a ceiling. When the ceiling is exceeded it closes non-essential sockets and stops scheduling alarms until the next hour.
   - Cloudflare budget alerts are configured as notification only and are never counted as enforcement. Subscription gating limits who may use the service, not what it costs.
8. **Storage choices.**
   - D1 holds the account, device and node registry, entitlement, commerce, remote commands and audit (V-C03).
   - Live status lives only in DO memory and storage (bounded: latest snapshot per node, last 100 summary changes).
   - Execution history stays on nodes. No telemetry time series is stored in D1.
