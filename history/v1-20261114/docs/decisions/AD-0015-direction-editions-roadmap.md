# AD-0015 — Product direction, editions and roadmap governance

- Status: Accepted (2026-10-13; the product owner's decisions of that day; amended 2026-10-19 by AD-0017: §1, §2 and §7 gain future-tense direction for delegated execution with verified contracts; amended 2026-10-19 by AD-0017 as amended: §1, §2 and §7 gain direction for application and workload control; §8 and every release-1 statement unchanged; amended 2026-10-28 by [AD-0021](AD-0021-central-access-go-center.md): §2, the promise of account-free, center-free normal operation is withdrawn; §4, LAN leaves current delivery (AD-0021 §12, §13))
- Amends: [AD-0010](AD-0010-commerce-and-entitlements.md) (feature gating), [AD-0008](AD-0008-lan-trust-and-placement.md) (account trust deferred), [AD-0002](AD-0002-platform-scope.md) (Windows 11 floor confirmed)
- Related: [product definition](../product/product-definition.md) §5 and §9; the canonical roadmap is [`roadmap.md` in ArcForges/Plan](https://github.com/ArcForges/Plan/blob/main/roadmap.md)

## Context

ArcForges is the flagship product ([AD-0001](AD-0001-flagship-pivot.md)). ArcScope and ArcSlate are potential future consumers of its contracts, not current implementation targets. On 2026-10-13 the product owner confirmed the editions principle, the platform floor and the initial LAN scope, set the long-term direction, and asked for one governed roadmap that separates committed delivery from future work.

## Decision

1. **Direction.** AI clients (Claude Code, Codex and similar) provide reasoning; ArcForges provides the execution side of AI-driven work: unified execution, resource control and operational management.
   - The long-term target is every non-reasoning operation: commands and their subprocesses, worktrees, temporary directories, disk space, caches, scheduling and task lifecycle. Work that subagents start takes part in the same system.
   - The objective is useful completion time and reliability on the machine and the LAN, not concurrency counts or CPU utilization.
2. **Editions.** Local and LAN functionality is free, including future local and LAN capabilities. Only cloud-backed services need a subscription. Local and LAN execution never depend on cloud availability, and no local capability is restricted to create subscription value.
   - **Pro at launch** is the cloud offering: remote access through ArcForges Cloud from anywhere (live status and confirmed actions through the relay, from the web and Android), mobile monitoring and control, and push notifications.
   - Hosted history and team administration are accepted future work (roadmap RM-06, RM-07). Account-based LAN trust and cloud discovery hints are deferred (RM-01); pairing provides LAN trust without an account.
3. **Platform.** Windows 11 is the minimum Windows version. No effort goes into Windows 10 ([AD-0002](AD-0002-platform-scope.md)).
4. **Initial LAN scope.** Placement with content-addressed file transfer, and compiler-cache sharing (sccache, ccache). Dependency-cache sharing (RM-02) and managed FASTBuild remote workers (RM-03) are accepted future work.
5. **Each release states its supported operations.** The release defines exactly which operations it manages, makes them work end to end, and documents the gaps ([product definition](../product/product-definition.md) §9, [08](../architecture/08-ai-integration.md) §4.4). A prompt that asks an AI client to use ArcForges is never evidence that an operation is intercepted.
6. **Evidence.** Records correlate enough operational evidence to explain delay and waste: task and attempt, originating session or agent where known, workspace, processes, queueing reasons, execution phases, downloads and cache usage, resource consumption, retries and outcomes. Collection overhead, retention, disk use and sensitive data are bounded ([07](../architecture/07-records-diagnosis-memory.md) §1.5).
7. **Foundations, not premature features.** Where a future capability needs interfaces or data now, the current delivery includes them without implementing the capability:
   - operational-memory facts and correlated evidence feed later prediction (RM-08);
   - resource hints, queue explanations and capacity reads feed later real-time resource requests from AI clients (RM-09);
   - the result cache's observe mode feeds later restore (RM-04);
   - published adapter manifests and the compiled-in adapter contract feed later adapters and plugins (RM-11, EX-01).
8. **Extensions.** Any future plugin (integration, cache backend, diagnostic, adapter) runs through the core permission, execution, resource and recording mechanisms; none bypasses them. A plugin marketplace does not imply charging for local functionality. Release 1 has no runtime plugins.
9. **Roadmap governance.** One canonical roadmap, `roadmap.md` in ArcForges/Plan, has three tiers:
   - committed delivery: exactly the tasks of the delivery graph;
   - accepted future work (RM-*);
   - exploratory ideas (EX-*).

   Each deferred item states its purpose, the reason for deferral, prerequisites and the conditions for revisiting it. An item becomes committed work only through a reviewed Design change (requirements, decisions, architecture) followed by a reviewed Plan change that adds tasks with acceptance criteria. Nothing on the roadmap is implemented without that promotion.

## Direction (roadmap; not release 1)

Amended 2026-10-19 by [AD-0017](AD-0017-delegated-execution-direction.md). Each item extends the section it names; none replaces it, and none changes release 1. **Effective:** now, as future-tense direction; each capability takes effect only when its roadmap row is promoted.
- **§1 gains:** work that ArcForges launches will carry a verified contract for resources, access and lifecycle; work it does not launch will be observed and labelled ([AD-0017](AD-0017-delegated-execution-direction.md), principle 1; [17](../architecture/17-delegated-execution.md)). The objective of §1, useful completion time and reliability, keeps its force through AD-0017's mission-level rule (principle 9).
- **§2 gains:** the local and LAN capabilities of this direction will be free, confinement included, and no local default may depend in practice on a Pro remote decision; their remote views and actions stay the cloud offering of §2 ([17](../architecture/17-delegated-execution.md) §5.4, §7.6).
- **§7 gains:** for this direction, the only release-1 foundations are the release coverage statement's stated limits of 2026-10-19 (the per-client routing statements, the credential sentence, the same-user qualifier and the generic UAC sentence served by `GetReleaseScope`, AF-AI-01; [product definition](../product/product-definition.md) §9). No other interface or data is added to release 1 for it.
- **§8 is unchanged.**

Amended 2026-10-19 by [AD-0017](AD-0017-delegated-execution-direction.md) as amended. Each item extends the section it names; none replaces it, and none changes release 1. **Effective:** now, as future-tense direction; each capability only when its roadmap row is promoted.
- **§1 gains:** the long-term direction widens to application and workload control ([AD-0017](AD-0017-delegated-execution-direction.md) principle 1 as amended); the execution side of AI-driven work stated in §1 stays its first workload family, the one release 1 is built for, and no longer defines the product; it covers compatible native application workloads of every kind, owner-directed and cooperative, with per-limit enforcement statements and failure diagnosis ([AD-0017](AD-0017-delegated-execution-direction.md) principle 1; the goals in the owner's words in [18](../architecture/18-application-workload-control.md) §2.4). The objective of §1, useful completion time and reliability, keeps its force for batch work; for interactive work the measure is the interactive cost measure of AD-0017 principle 9 as amended.
- **§2 gains:** owner-directed application control, the cooperative resource API and its SDK, failure diagnosis and the interactive guard will be local capabilities when their rows are promoted, and therefore free; their remote views and leased remote commands are the cloud offering.
- **§7 gains** (the product owner's decision of 2026-10-19, [18](../architecture/18-application-workload-control.md) §19, decision 26: "None now (Recommended)". The option text read: "Release 1 stays exactly as committed. The fields are considered when application control (EX-25) is promoted."): for this direction no release-1 foundation is added. Optional fields stay additive after an RPC is served, so "cheaper while unserved" does not justify adding adoption resource fields or a per-task CPU cap field to release 1. RM-09's recorded foundations stay as they are; its widening is the owner's decision on an accepted row.
- **§8 and §9 are unchanged.** An application that uses the cooperative API is not a plugin; nothing of this direction bypasses the core mechanisms.

## Consequences

- LAN placement, LAN cache sharing and pairing need no account, entitlement or cloud connection. LAN delivery no longer depends on cloud tasks.
- The entitlement token describes cloud features only ([AD-0010](AD-0010-commerce-and-entitlements.md) §5).
- Deferred items keep their reserved contract elements (for example `NodeEnrollmentService.IssueNodeCertificate`, `RESULT_CACHE_MODE_RESTORE`), marked as roadmap and refused or not served in release 1. The contracts stay additive within `v1`.
