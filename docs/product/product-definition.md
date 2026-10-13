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
8. extends the same model across trusted machines on a LAN, free and without an account: task placement, workspace transfer and compiler-cache sharing, with LAN traffic kept local;
9. offers subscribers remote status, control and notifications through arcforges.com and an Android app.

**Direction** ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md)). AI clients such as Claude Code and Codex provide reasoning; ArcForges provides the execution side of AI-driven work: unified execution, resource control and operational management. The long-term target is every non-reasoning operation: commands and their subprocesses, worktrees, temporary directories, disk space, caches, scheduling and task lifecycle, including work that subagents start. Success means useful completion time and reliability on the machine and the LAN, not concurrency counts or CPU utilization. Each release states exactly which operations it manages (§9), and the [roadmap](https://github.com/ArcForges/Plan/blob/main/roadmap.md) holds the rest (§10).

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
| MCP adapter | `arcforges mcp serve` (stdio; a local HTTP transport is roadmap RM-05) | AI-client interface translating MCP tool calls to node gRPC |
| arcforges.com | C# static site plus Blazor WebAssembly account and fleet profiles behind Cloudflare | Product presentation, downloads, account, devices, subscription, remote status |
| ArcForges for Android | .NET MAUI, Android only | Fleet view, notifications, confirmed actions, pairing, Google Play subscription |
| ArcForges Cloud | C# Native AOT host in Cloudflare Containers; thin TypeScript Worker and Durable Object adapters | Accounts, devices, entitlements, commerce, relay, push, support |

## 5. Editions and gating

**Principle** ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md)): local and LAN functionality is free, including future local and LAN capabilities. Only cloud-backed services need a subscription, and no local capability is restricted to create subscription value.

| Capability | Free (no account needed) | Pro (subscription) |
|---|---|---|
| Local node, CLI, Desktop, MCP and AI-client integration | Yes | Yes |
| Resource control, queueing, records, diagnosis, operational memory | Yes | Yes |
| WSL guest node on the same machine | Yes | Yes |
| Managed storage, caches, disk analysis and cleanup | Yes | Yes |
| LAN pairing, peer status, placement with file transfer, and compiler-cache sharing | Yes | Yes |
| Remote access outside the LAN: live status and confirmed actions from arcforges.com and Android, through the cloud relay | No | Yes |
| Mobile monitoring and control (Android app) | No | Yes |
| Push notifications | No | Yes |
| Support response targets | Community | Standard |

- **No cloud dependency for local or LAN work.** Local and LAN execution never require a cloud connection or an account.
- **Entitlements cover cloud features only.** The signed entitlement token describes cloud features (`remote.*`, `push`); no local or LAN feature checks it ([AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §5).
- **Plan definitions are data.** Plans are defined in the existing Entitlement module and can change without code changes. The table above is the launch configuration.
- **Later cloud services.** Hosted history and team administration are accepted future work (roadmap RM-06, RM-07).

## 6. Platform scope

The active scope is **Windows 11 (x64, arm64)** (the minimum Windows version, confirmed by the product owner on 2026-10-13; no effort goes into Windows 10) and **Linux, including WSL2 on Windows (x64, arm64)** for the node, CLI, MCP adapter and Desktop. It also covers **Android 8.0+** for the mobile app and **current evergreen browsers** for the web. macOS is outside the current implementation and acceptance scope ([AD-0002](../decisions/AD-0002-platform-scope.md)). Platform boundaries are kept clean so a macOS backend can be added later without redesign. Nothing for macOS is built or claimed now.

## 7. Non-goals

- Transparently running one arbitrary process across several computers. Only separate tasks are placed on different nodes, and distributed compilation is used only where a toolchain supports it (sccache-dist, FASTBuild, distcc-class tools).
- In release 1, sharing **dependency caches** (NuGet, npm, Cargo, pip) over the LAN, and **managing FASTBuild remote workers**: accepted future work (roadmap RM-02, RM-03). Each node keeps its own managed dependency caches; FASTBuild `-dist` is observed and labelled. LAN sharing covers compiler caches and placement transfers ([05](../architecture/05-toolchains-caches.md) §6).
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
| Explained delay and waste | Queueing, repeated and stale work, retries, downloads and cache misses are visible per task, session and workspace | Correlated records ([07](../architecture/07-records-diagnosis-memory.md) §1.5) and the waste report |

## 9. Release 1: supported operations and coverage

Release 1 manages the operations below end to end on Windows 11 and Linux, including WSL2 (R-AI-011). Everything else is observed where possible and reported as a coverage gap. A prompt that asks an AI client to use ArcForges is never counted as interception.

| Operation | Managed in release 1 (route) | Reported as a gap |
|---|---|---|
| Commands and their subprocesses | The CLI, Desktop and the MCP `run` tool; Claude Code and Codex shell commands rewritten by hooks (`rewrite` for heavy commands, `rewrite-all` for every command except passthrough patterns). Each runs in a job object or transient unit under budgets, keys and records. | Commands while hooks are disabled, untrusted or failed; background launches; processes the client starts itself (MCP servers, language servers, IDE tasks): observed as bypassed or unmanaged ([08](../architecture/08-ai-integration.md) §4.4; roadmap RM-12) |
| Work started by subagents | The same routes; Claude Code subagent commands carry the agent ID | Subagent attribution for Codex and for MCP calls: labelled unknown |
| Worktrees | Managed creation, locks, verified archive and restore (MCP, CLI, Desktop) | Worktrees a client creates itself: observed and registered as workspaces |
| Temporary directories | Per-attempt `tmp/<attempt>` with limits and cleanup | Tools that ignore `TMP`/`TEMP`/`TMPDIR`: reported by disk analysis |
| Disk space | Managed roots, limits by kind, runtime limits, the low-space guard, analysis and two-phase cleanup with quarantine | Writes by unmanaged processes |
| Caches | Managed NuGet, npm, Cargo, pip, sccache, ccache and FASTBuild caches, redirected where the tool honours it; compiler-cache sharing on the LAN | Dependency-cache sharing on the LAN (RM-02); redirection the tool may ignore is labelled `BEST_EFFORT` |
| Scheduling and task lifecycle | Queue, pools, priorities, dependencies, services, retries by assertion, cancellation, hand-off before client timeouts, joins | — |
| Machines | The WSL guest node with coordinated admission; LAN placement with content-addressed transfer between paired nodes | Managed FASTBuild workers (RM-03) |
| Evidence | Correlated records per attempt ([07](../architecture/07-records-diagnosis-memory.md) §1.5) | Network use per process (inferred only) |

**Pro in release 1** is the cloud offering of §5: remote access outside the LAN, mobile monitoring and control, and push notifications.

## 10. Roadmap

The canonical [roadmap](https://github.com/ArcForges/Plan/blob/main/roadmap.md) lives in ArcForges/Plan ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §9). It separates committed delivery (the tasks of the delivery graph), accepted future work (RM-*) and exploratory ideas (EX-*), and records for each deferred item its purpose, the reason for deferral, prerequisites and the conditions for revisiting it.

