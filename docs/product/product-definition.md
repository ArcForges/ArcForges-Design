# ArcForges product definition

**Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) (target until each AF-CTR task is delivered).** Ordinary use goes through a configured center, official or self-hosted: clients use its business API, cloud AI its MCP endpoint, local AI the stdio adapter to the same center, each naming an explicitly selected node; the node keeps execution authority. The center is a Go service on Neon/PostgreSQL, not the C# Native AOT host and Durable Object adapters described below. LAN ("local and across a LAN", the LAN persona, the node as a LAN peer, LAN rows and parts of §5 and §9) is out of current delivery (roadmap RM-19). "Pro … through ArcForges Cloud" and the editions of §5 are the earlier launch configuration; plan contents under center access are an open owner question (AD-0021).

Status: authoritative for active development from 2026-10-12 ([AD-0001](../decisions/AD-0001-flagship-pivot.md)).

## 1. Problem

AI agents and automation can request operations, but nothing coordinates the operating-system resources those operations consume. Several agents, subagents and scripts independently start builds, tests, package restores, scans and other processes. The result:

- no shared allocation of CPU and memory, and no protection for the person using the machine;
- inconsistent working directories, temporary files and per-task copies of caches, so the same packages are downloaded and stored repeatedly;
- no reliable execution state: a process that "exists" is assumed to be progressing, and work is lost or repeated when an agent turn ends;
- no evidence of where time goes. Waiting, contention, retries, repeated verification and stalled commands look identical to useful work.

The 2026-10-11 waiting audit of the previous ArcForges delivery run measured this directly. 56% of agent time was queueing for a single workstation lock, and a third of locked time was duplicated verification. Some checks waited eight minutes of queue for each minute of work, and dead locks held the machine idle for hours in earlier sessions. Details are in ArcForges-Design-Parallel; the audit's working notes are not published.

**Direction (roadmap; not release 1).** Added 2026-10-19. The same gap exists beyond AI-driven work, for every native application the owner runs: a messenger, an IDE, a media tool, the background work beside a game, a local service. Nothing lets the owner write one policy per application, have the operating system enforce what it genuinely can, see per limit what was actually enforced and against whom, and learn whether a limit the owner set caused a failure. Priority tools offer hints that look like limits; per-application quota tools rarely state what they enforced; sandboxes mostly arrive only with a vendor's packaging ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md); [18](../architecture/18-application-workload-control.md)).

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

*(Direction note, 2026-10-19: under [AD-0017](../decisions/AD-0017-delegated-execution-direction.md) as amended, this paragraph describes the first workload family, the one release 1 is built for, of the application and workload control direction below; it no longer defines the product.)*

ArcForges is not a command queue, an MCP server, a coding-agent wrapper, a cache dashboard or another AI agent. Those are interfaces or capabilities of the platform. Its value is the coherent system underneath: one authority per machine, real enforcement, durable execution state and evidence.

The platform is general-purpose. Programming workloads are first, but nothing in the node is specific to source code, and future products (ArcSlate, ArcScope) can use its execution, resource and fleet capabilities through the same contracts ([AD-0013](../decisions/AD-0013-reuse-and-supersession.md)).

### Direction (roadmap; not release 1): application and workload control, with verified contracts

Added 2026-10-19 and restated 2026-10-19 ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), amended; proposed model in [18](../architecture/18-application-workload-control.md) and [17](../architecture/17-delegated-execution.md)). As a Design description, not a product name, ArcForges' long-term direction is, in the product owner's words, *"a cross-platform, local-first application and workload control infrastructure that unifies resource coordination, process lifecycle management, policy enforcement, verifiable access restrictions, and operational diagnostics."* The operating system enforces; ArcForges coordinates, sets the owner's policy and reports.

Its workloads are every compatible native workload: AI agents and their commands, MCP servers and tools, builds, native desktop applications (closed-source and first-party, ArcSlate included), media production and rendering, IDEs and their indexers, compatible games and launchers, and long-running local services. For each, the owner writes one policy; ArcForges will state what it may use, realize it with operating-system mechanisms, read the realization back, refuse when a requirement cannot be met, supervise what it launched or the owner adopted, record what happened, diagnose whether a limit the owner set caused a failure, and let the owner revoke it from any surface. Applications will take part through independent facets (seen, held, limited, confined, cooperating; [18](../architecture/18-application-workload-control.md) §4); confinement needs a launch, and neither confinement nor cooperation is a precondition of the other. An application will need no SDK to be observed, supervised or resource-controlled, and will be confinable at launch where the operating system and the application are compatible; an application that integrates will also be able to request resources, never beyond the owner's maximums (accepted goals, not working capabilities: [18](../architecture/18-application-workload-control.md) §2.4). Work the owner delegates to AI agents and tools ("delegated execution, with verified contracts") is one family of these workloads. It is the umbrella of the direction above: the execution side of AI-driven work ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md)) is its first workload family, the one release 1 is built for, and keeps its force for that family; it no longer defines the product.

"Your machine. Your rules." is read in a bounded way, after the owner's own words: "the machine owner determines what applications may access, how much resource capacity managed workloads may consume, when work should be admitted or deferred, and which policies are actually enforced."
- **"Your rules":** the owner writes one policy per application or workload, and every launch or adoption ArcForges performs either realizes it or is refused with a reason. "Actually enforced" is the value read back from the operating system, never the number typed. This holds today for resource requirements; for per-application limits, access, lifecycle and diagnosis it is direction, taking effect row by row as the roadmap rows are promoted.
- **"Your machine":** ArcForges runs as the user and never elevates at run time, so it cannot control everything on the machine. It controls what it launched or what the owner explicitly adopted (and, from EX-15's holds stage and only by the owner's decision, what the owner held); it observes what a standard user can see and labels it; it never claims more than the operating system enforces. ArcForges is not a graphical display isolation system or a secure desktop.

**The end-state sentence:** *For everything it runs or the owner adopted, ArcForges will state who asked, what was granted, what the operating system actually enforces and against whom, and what happened, including whether a limit the owner set caused a failure; for everything else, it observes and says so.*

**What release 1 says:** release 1 reports access as NONE (same-user) where it reports it at all. It confines no workload, and its stated limits are in §9.

*Superseded 2026-10-19, kept as history:* the subsection "Direction (roadmap; not release 1): "Your machine. Your rules."" of 2026-10-19 read: "As a Design description, not a product name, ArcForges' long-term direction is *the local authority for delegated execution, with verified contracts*. When the owner hands work to a delegate (an AI agent, an MCP server, a tool, a script, a portable application, a LAN peer), ArcForges will state what that work may use, realize it with operating-system mechanisms, read the realization back, refuse when a requirement cannot be met, own or honestly label the lifecycle of what the delegate brought onto the machine, record what happened, and let the owner revoke it from any surface." Its "Your rules" bullet read "the owner writes policy once, and every launch ArcForges performs either obeys it or is refused with a reason", and its end-state sentence read "*For everything it runs, ArcForges will state who asked, what was granted, what the operating system actually enforces, and what happened; for everything else, it observes and says so.*" Its successor is the subsection above, after the product owner's correction of 2026-10-19 ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md)).

## 3. Users and primary journeys

| User | Needs | Primary journeys |
|---|---|---|
| Developer using AI coding agents | Many agents building and testing in parallel without freezing the machine; no repeated restores; knowing why work is slow | J-01 install and connect an AI client; J-02 agent runs builds through ArcForges; J-04 diagnose slow or stuck work; J-05 reclaim disk |
| Developer or automation author without AI | A reliable queue for long commands, resource limits, logs and history | J-03 run, queue and limit commands from the CLI or GUI |
| Owner of several machines (desktop, laptop, build box) | Use idle machines and shared caches on the LAN | J-06 pair a machine; J-07 place work on another node |
| Subscriber away from the desk | See status, get notified, take a confirmed action | J-08 subscribe; J-09 remote status and actions from web or Android |
| ArcForges operator (the vendor) | Keep the service affordable, safe, supportable and lawful | J-10 operate, support and enforce limits |

Journeys are specified in [experience/journeys.md](../experience/journeys.md).

## 4. Surfaces

| Surface | Technology | Role |
|---|---|---|
| ArcForges node (service) | C# .NET 10 Native AOT, one per user per machine (a Linux node a user runs in a WSL2 distribution is an ordinary Linux node, without integration; [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md)) | Authority for execution and resource state; local gRPC API; LAN peer; cloud uplink |
| `arcforges` CLI | Same Native AOT executable as the node (multi-role binary) | Direct use and automation; MCP adapter role; hook handler role |
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
| Managed storage, caches, disk analysis and cleanup | Yes | Yes |
| LAN pairing, peer status, placement with file transfer, and compiler-cache sharing | Yes | Yes |
| Remote access through ArcForges Cloud, from anywhere: live status and confirmed actions from arcforges.com and Android | No | Yes |
| Mobile monitoring and control (Android app) | No | Yes |
| Push notifications | No | Yes |
| Support response targets | Community | Standard |

- **No cloud dependency for local or LAN work.** Local and LAN execution never require a cloud connection or an account.
- **Entitlements cover cloud features only.** The signed entitlement token describes cloud features (`remote.*`, `push`); no local or LAN feature checks it ([AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §5).
- **Plan definitions are data.** Plans are defined in the existing Entitlement module and can change without code changes. The table above is the launch configuration.
- **Later cloud services.** Hosted history and team administration are accepted future work (roadmap RM-06, RM-07).

*Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §2, §13.* The promise of account-free, center-free normal operation above is withdrawn: ordinary use goes through a configured center, official or self-hosted, while node-accepted work never depends on the center's availability. User-owned compute and the open-source software are distinct from the official hosted center, which is a service; a self-hosted center needs no official service. The LAN row and the "no cloud dependency for local or LAN work" bullet are out of current delivery (LAN is roadmap RM-19). No price, free allowance, device limit or package is decided by this amendment; the table is the earlier launch configuration, to be re-decided by the owner (H-07).

## 6. Platform scope

The active scope is **Windows 11 (x64, arm64)** (the minimum Windows version, confirmed by the product owner on 2026-10-13; no effort goes into Windows 10) and **Linux (x64, arm64)** for the node, CLI, MCP adapter and Desktop. It also covers **Android 8.0+** for the mobile app and **current evergreen browsers** for the web. macOS is outside the current implementation and acceptance scope ([AD-0002](../decisions/AD-0002-platform-scope.md)). Platform boundaries are kept clean so a macOS backend can be added later without redesign. Nothing for macOS is built or claimed now. A user may run the Linux node in a compatible WSL2 distribution, without integration: it is an ordinary Linux node with no WSL-specific behaviour or acceptance guarantee ([AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md)).

## 7. Non-goals

- Transparently running one arbitrary process across several computers. Only separate tasks are placed on different nodes, and distributed compilation is used only where a toolchain supports it (sccache-dist, FASTBuild, distcc-class tools).
- In release 1, sharing **dependency caches** (NuGet, npm, Cargo, pip) over the LAN, and **managing FASTBuild remote workers**: accepted future work (roadmap RM-02, RM-03). Each node keeps its own managed dependency caches; FASTBuild `-dist` is observed and labelled. LAN sharing covers compiler caches and placement transfers ([05](../architecture/05-toolchains-caches.md) §6).
- Taking control of unrelated applications. The node observes the whole machine but controls only processes it launched, or processes the user explicitly adopts.
- Exact P-core/E-core placement or other low-level scheduler knobs.
- Replacing the AI client, the build system or the operating system's resource-control machinery.
- Modifying the ArcForges program itself during an ordinary managed task. Extensions arrive through normal development, review and release.

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md) boundaries 3.4, 3.11 … 3.13, added 2026-10-19):* the long-term direction adds three non-goals: a graphical display isolation system or a secure desktop environment; an application store, a replacement for the desktop's launcher, menu or store, a VM manager, or a replacement for the operating system; a system optimizer or a "game booster". "Taking control of unrelated applications" stays: it is the positioning's own qualifier ("what it launched or what the owner explicitly adopted").

## 8. Success measures (product level)

| Measure | Target | Evidence |
|---|---|---|
| Agent time spent waiting in client-side retry loops for capacity | 0 (submissions queue in the node) | Execution records |
| Machine responsiveness under heavy managed load | User-reserved headroom held (see [performance targets](../architecture/15-performance-targets.md)) | Automated load tests on Windows and native Linux |
| Duplicate dependency downloads across managed tasks on one node | Visible per toolchain, and avoided where caches are shared | Cache statistics |
| Idle node footprint | Within [performance targets](../architecture/15-performance-targets.md) | Benchmarks |
| Integration honesty | Every managed or bypassed operation an integration can observe is attributed; unobservable state is labelled unknown | Coverage reports |
| Explained delay and waste | Queueing, repeated and stale work, retries, downloads and cache misses are visible per task, session and workspace | Correlated records ([07](../architecture/07-records-diagnosis-memory.md) §1.5) and the waste report |

## 9. Release 1: supported operations and coverage

Release 1 manages the operations below end to end on Windows 11 and Linux (R-AI-011). Everything else is observed where possible and reported as a coverage gap. A prompt that asks an AI client to use ArcForges is never counted as interception.

| Operation | Managed in release 1 (route) | Reported as a gap | Verified by |
|---|---|---|---|
| Commands and their subprocesses | The CLI, Desktop and the MCP `run` tool; Claude Code shell commands rewritten by hooks (`rewrite` for heavy commands, `rewrite-all` for every command except passthrough patterns); Codex shell commands rewritten when the user pre-approves rewritten commands (`routing.rewrite_permission=ALLOW`). Each runs in a job object or transient unit under budgets, keys and records. | Commands while hooks are disabled, untrusted or failed; Codex shell commands without the pre-approval (heavy ones are denied with guidance to the `run` tool, the rest run unmanaged); background launches; processes the client starts itself (MCP servers, language servers, IDE tasks): observed as bypassed or unmanaged ([08](../architecture/08-ai-integration.md) §4.4; roadmap RM-12) | J-02, J-03 |
| Work started by subagents | The same routes; Claude Code subagent commands carry the agent ID | Subagent attribution for Codex and for MCP calls: labelled unknown | J-11 |
| Worktrees | Managed creation, locks, verified archive and restore (MCP, CLI, Desktop) | Worktrees a client creates itself: observed and registered as workspaces | J-11 |
| Temporary directories | Per-attempt `tmp/<attempt>` with limits and cleanup | Tools that ignore `TMP`/`TEMP`/`TMPDIR`: reported by disk analysis | J-11 |
| Disk space | Managed roots, limits by kind, runtime limits, the low-space guard, analysis and two-phase cleanup with quarantine | Writes by unmanaged processes | J-05 |
| Caches | Managed NuGet, npm, Cargo, pip, sccache, ccache and FASTBuild caches, redirected where the tool honours it; compiler work behind a cache runs inside the requesting attempt (one sccache server per attempt); compiler-cache sharing on the LAN | Dependency-cache sharing on the LAN (RM-02); redirection the tool may ignore is labelled `BEST_EFFORT`; downloads outside managed caches (for example a script's own download) are not counted | J-02, J-07 |
| Scheduling and task lifecycle | Queue, pools, priorities, dependencies, services, retries by assertion, cancellation, hand-off before client timeouts, joins | — | J-02, J-03, J-04 |
| Machines | LAN placement with content-addressed transfer between paired nodes | Managed FASTBuild workers (RM-03) | J-01, J-06, J-07 |
| Evidence | Correlated records per attempt ([07](../architecture/07-records-diagnosis-memory.md) §1.5) | Network use per process (inferred only) | J-04 |

**Stated limits** (added 2026-10-19). Release 1 confines no workload: every managed process runs as the signed-in user, with that user's access. The rows below state what follows, in the same columns; they are part of the release coverage statement. Their Verified by column names the journey that shows them, and `GetReleaseScope` is checked against this text (R-AI-011).

| Subject | What release 1 does | Stated limit | Verified by |
|---|---|---|---|
| `routing:claude-code` | The MCP run tool and hook rewrites give routed commands resource control, keys and records | Commands routed through ArcForges (MCP run, hook rewrites) gain resource control and records, but run outside Claude Code's own sandbox. Claude Code's own process, with its file tools, hooks and MCP servers, keeps the user's full access. | J-01, J-02 |
| `routing:codex` | The MCP run tool and, with the pre-approval, hook rewrites give routed commands resource control, keys and records | Commands routed through ArcForges (MCP run, and hook rewrites where pre-approved) gain resource control and records, but run outside Codex's own sandbox. Codex's own process, with its hooks and MCP servers, keeps the user's full access. | J-01, J-02 |
| Credentials | The node's own credentials and data key are kept in the OS secret store; task secrets are sealed at rest and appear in records as presence only | Unsandboxed managed processes can read every credential the signed-in user can read. ArcForges does not read or record them. The node data key, sealed task secrets and running environments are protected from other users, not from the signed-in user's own processes. | J-01 |
| Administrator rights | ArcForges never elevates, and its core features need no administrator rights | On an administrator account without Administrator protection, UAC is not a security boundary; unconfined workloads may obtain administrator rights silently. Never elevating does not prevent privileged changes that a workload obtains through the OS, such as system-bus requests that polkit authorizes on Linux. | J-01 |
| ArcForges' own containers | Limits, kill and records hold against accidental and over-privileged workloads | A guardrail only against workloads that target ArcForges' objects: same-user code can change or end ArcForges' containers, and work launched outside the recorded ancestry (through WMI, a broker, a service, a scheduled task or a spoofed parent) never joins them and is not detected. | J-01 |
| Paired LAN peers | Placement from a peer only where its per-peer policy allows it; placement is opt-in per peer | A peer with placement rights executes code as the local user; per-peer command patterns are argument filters, which are guardrails. | J-01 |

- **Selecting a client's row.** The Subject column is the entry's `operation`. The two routing rows use the fixed strings `routing:claude-code` and `routing:codex`, so a surface selects the row for a session's client without a contract change and labels it "Commands routed from Claude Code" or "Commands routed from Codex". The Stated limit text of a client's routing row is the per-client routing statement: the integration consent copy uses it verbatim, and D-14's integration consent panel, `arcforges coverage` and the MCP `session_coverage` tool show it from this row; D-07 and `arcforges session coverage` link to the release coverage statement ([AD-0007](../decisions/AD-0007-ai-integration.md) §4; [08](../architecture/08-ai-integration.md) §5).
- **Design references.** The Stated limit cells are served as written, so their references are kept here: the routing rows [11](../architecture/11-security-privacy.md) §1, T-24 (V-A03, V-A06; A-A03); Credentials [04](../architecture/04-execution.md) §2 and [11](../architecture/11-security-privacy.md) §3, T-25; Administrator rights T-26 (V-W07, V-W08, V-L08); ArcForges' own containers T-22, T-23 ([03](../architecture/03-resource-control.md) §5, §9); Paired LAN peers T-27 ([09](../architecture/09-lan.md) §4).

The release coverage statement is the same on every node of a release. It carries no host-posture fact and no user path, because AGENT callers and the MCP `session_coverage` tool read it: the host's account type and Administrator protection state are reported only by the doctor's HUMAN-only host-posture check ([07](../architecture/07-records-diagnosis-memory.md) §2.4).

**Where gaps are reported.** Gaps that belong to a session (bypassed commands, route failures, unknown attribution) appear in its coverage report ([08](../architecture/08-ai-integration.md) §5). The node serves both tables above, in order, as the product's **release coverage statement** (`SessionService.GetReleaseScope`). D-14, `arcforges coverage` and the MCP `session_coverage` tool show it next to the session's facts, and D-07 and `arcforges session coverage` link to it, so no surface implies broader coverage.

*Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §12.* The LAN parts of the tables above (compiler-cache sharing on the LAN in Caches, LAN placement in Machines, and the Paired LAN peers row) are out of current delivery. When AF-AI-01 builds `GetReleaseScope`, it serves this statement without them.

**Pro in release 1** is the cloud offering of §5: remote access through ArcForges Cloud, mobile monitoring and control, and push notifications.

## 10. Roadmap

The canonical [roadmap](https://github.com/ArcForges/Plan/blob/main/roadmap.md) lives in ArcForges/Plan ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §9). It separates committed delivery (the tasks of the delivery graph), accepted future work (RM-*) and exploratory ideas (EX-*), and records for each deferred item its purpose, the reason for deferral, prerequisites and the conditions for revisiting it.

