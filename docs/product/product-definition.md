# ArcForges product definition

Status: authoritative for active development from 2026-10-12 ([AD-0001](../decisions/AD-0001-flagship-pivot.md)).

## 1. Problem

AI agents and automation can request operations, but nothing coordinates the operating-system resources those operations consume. Several agents, subagents and scripts independently start builds, tests, package restores, scans and other processes. The result:

- no shared allocation of CPU and memory, and no protection for the person using the machine;
- inconsistent working directories, temporary files and per-task copies of caches, so the same packages are downloaded and stored repeatedly;
- no reliable execution state: a process that "exists" is assumed to be progressing, and work is lost or repeated when an agent turn ends;
- no evidence of where time goes. Waiting, contention, retries, repeated verification and stalled commands look identical to useful work.

The 2026-10-11 waiting audit of the previous ArcForges delivery run measured this directly. 56% of agent time was queueing for a single workstation lock, and a third of locked time was duplicated verification. Some checks waited eight minutes of queue for each minute of work, and dead locks held the machine idle for hours in earlier sessions. Details are in ArcForges-Design-Parallel and `C:\MyFile\Projects\ArcForges\.claude\coordinator\waiting-audit-2026-10-11.md`.

## 2. Product

**ArcForges is a cross-platform resource-control and execution platform for AI and automation, local and across a LAN.** A background service on each machine (an **ArcForges node**) owns the authoritative execution and resource state of that machine. It:

1. accepts work once, keeps it, and starts it when capacity, policy and dependencies allow, so no caller has to poll or compete for a lock;
2. computes CPU and memory budgets from real host capacity, current load, user-reserved headroom and policy, so callers never need to guess allowances;
3. enforces those budgets with operating-system mechanisms (Windows job objects; Linux cgroup v2), and states honestly where enforcement is unavailable;
4. runs **many useful tasks concurrently** under that control. Parallelism is the default and a selling point. Users can restrict or disable it through policy;
5. directs managed work into consistent directories and shared, compatible caches, and makes disk usage and waste visible and safely reclaimable;
6. records what actually happened (admission wait, restore, build, test, network or disk wait, retries, stalls and repeated work) and diagnoses waste from evidence;
7. integrates with existing AI clients (Claude Code and Codex first) through MCP, hooks and configuration, and reports honestly what it can and cannot see;
8. extends the same model across trusted machines on a LAN: task placement, workspace transfer and cache sharing, with LAN traffic kept local;
9. offers subscribers remote status, control and notifications through arcforges.com and an Android app.

ArcForges is not a command queue, an MCP server, a coding-agent wrapper, a cache dashboard or another AI agent. Those are interfaces or capabilities of the platform. Its value is the coherent system underneath: one authority per machine, real enforcement, durable execution state and evidence.

The platform is general-purpose. Programming workloads are first, but nothing in the node is specific to source code, and future products (ArcSlate, ArcScope) can use its execution, resource and fleet capabilities through the same contracts ([AD-0013](../decisions/AD-0013-reuse-and-supersession.md)).

## 3. Users and primary journeys

| User | Needs | Primary journeys |
|---|---|---|
| Developer using AI coding agents | Many agents building and testing in parallel without freezing the machine; no repeated restores; knowing why work is slow | J-01 install and connect an AI client; J-02 agent runs builds through ArcForges; J-04 diagnose slow or stuck work; J-05 reclaim disk |
| Developer or automation author without AI | A reliable queue for long commands, resource limits, logs and history | J-03 run, queue and limit commands from the CLI or GUI |
| Owner of several machines (desktop, laptop, build box, WSL) | Use idle machines and shared caches on the LAN | J-06 pair a machine; J-07 place work on another node |
| Subscriber away from the desk | See status, get notified, take a confirmed action | J-08 subscribe; J-09 remote status and actions from web or Android |
| ArcForges operator (the vendor) | Keep the service affordable, safe, supportable and lawful | J-10 operate, support and enforce limits |

Journeys are specified in [experience/journeys.md](../experience/journeys.md).

## 4. Surfaces

| Surface | Technology | Role |
|---|---|---|
| ArcForges node (service) | C# .NET 10 Native AOT, one per user per machine; a guest node inside each managed WSL distribution | Authority for execution and resource state; local gRPC API; LAN peer; cloud uplink |
| `arcforges` CLI | Same Native AOT executable as the node (multi-role binary) | Direct use and automation; MCP adapter role; hook handler role; WSL bridge role |
| ArcForges Desktop | Avalonia, Native AOT, optional | Visual control centre; tray presence on Windows |
| MCP adapter | `arcforges mcp serve` (stdio); local Streamable HTTP optional | AI-client interface translating MCP tool calls to node gRPC |
| arcforges.com | C# static site plus Blazor WebAssembly account and fleet profiles behind Cloudflare | Product presentation, downloads, account, devices, subscription, remote status |
| ArcForges for Android | .NET MAUI, Android only | Fleet view, notifications, confirmed actions, pairing, Google Play subscription |
| ArcForges Cloud | C# Native AOT host in Cloudflare Containers; thin TypeScript Worker and Durable Object adapters | Accounts, devices, entitlements, commerce, relay, push, support |

## 5. Editions and gating

| Capability | Free | Pro (subscription) |
|---|---|---|
| Local node, CLI, Desktop, MCP and AI-client integration | Yes | Yes |
| Resource control, queueing, records, diagnosis, operational memory | Yes | Yes |
| WSL guest node on the same machine | Yes | Yes |
| Managed storage, caches, disk analysis and cleanup | Yes | Yes |
| LAN pairing and peer status | Yes | Yes |
| LAN multi-node placement and LAN cache sharing | No | Yes (launch decision; see below) |
| Remote status and control (web, Android) through the cloud relay | No | Yes |
| Push notifications | No | Yes |
| Support response targets | Community | Standard |

- **No cloud dependency for local work.** Local execution never requires a cloud connection.
- **Offline grace for LAN features.** LAN features verify a signed entitlement token offline, with a grace period ([AD-0010](../decisions/AD-0010-commerce-and-entitlements.md)), so a LAN keeps working through cloud outages.
- **Plan definitions are data.** Plans are defined in the existing Entitlement module and can change without code changes. The table above is the launch configuration.
- **Why LAN placement and cache sharing are Pro.** They consume no cloud resources, and the product brief makes only **cloud-backed** resources subscriber-only. Putting multi-machine work in Pro is a commercial launch decision: it is the main value for teams and multi-machine users, and the offline-verified entitlement token keeps it working through cloud outages. Pairing and peer status stay free. Because plans are data, making LAN features free later needs no code change ([AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §1).

## 6. Platform scope

The active scope is **Windows 11 (x64, arm64)** and **Linux, including WSL2 on Windows (x64, arm64)** for the node, CLI, MCP adapter and Desktop. It also covers **Android 8.0+** for the mobile app and **current evergreen browsers** for the web. macOS is outside the current implementation and acceptance scope ([AD-0002](../decisions/AD-0002-platform-scope.md)). Platform boundaries are kept clean so a macOS backend can be added later without redesign. Nothing for macOS is built or claimed now.

## 7. Non-goals

- Transparently running one arbitrary process across several computers. Only separate tasks are placed on different nodes, and distributed compilation is used only where a toolchain supports it (sccache-dist, FASTBuild, distcc-class tools).
- At launch, sharing **dependency caches** (NuGet, npm, Cargo, pip) over the LAN, and **managing FASTBuild remote workers**. Each node keeps its own managed dependency caches; FASTBuild `-dist` is observed and labelled. LAN sharing covers compiler caches and placement transfers ([05](../architecture/05-toolchains-caches.md) §6).
- Taking control of unrelated applications. The node observes the whole machine but controls only processes it launched, or processes the user explicitly adopts.
- Exact P-core/E-core placement or other low-level scheduler knobs.
- Replacing the AI client, the build system or the operating system's resource-control machinery.
- Modifying the ArcForges program itself during an ordinary managed task. Extensions arrive through normal development, review and release.

## 8. Success measures (product level)

| Measure | Target | Evidence |
|---|---|---|
| Agent time spent waiting in client-side retry loops for capacity | 0 (submissions queue in the node) | Execution records |
| Machine responsiveness under heavy managed load | User-reserved headroom held (see [performance targets](../architecture/15-performance-targets.md)) | Automated load tests on Windows and WSL2 |
| Duplicate dependency downloads across managed tasks on one node | Visible per toolchain, and avoided where caches are shared | Cache statistics |
| Idle node footprint | Within [performance targets](../architecture/15-performance-targets.md) | Benchmarks |
| Integration honesty | Every managed or bypassed operation an integration can observe is attributed; unobservable state is labelled unknown | Coverage reports |
