# Schedule Analysis

> Generated from [the delivery graph](delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](README.md).

All values below are computed by Plan tools/delivery.py from the current graph. Structural facts (task counts, edge types, chain length, level widths, critical path) are properties of the documented dependencies. Makespans are unmeasured estimates that depend on the stated assumptions. The retired model advanced the same obligations one numbered substep at a time from a single Current task, so its schedule equals the one-worker row; its package-level graph also made each package wait for every upstream package and each substep wait for the previous one.

## Structural facts (computed from the graph)

| Measure | Value |
|---|---|
| Delivery tasks | 433 (6 carried as accepted baseline), plus 50 adoption slices |
| Out of scope (excluded from every measure here; not completed) | 35 tasks under P2-026 |
| Dependency edges by type | artifact 1081, contract 127, integration(completion) 265, release 35 |
| Remaining work (size units: S=1, M=2, L=4, XL=8) | 1125 |
| Longest dependency chain (levels) | 31 |
| Widest level (tasks whose longest prerequisite chain has equal length) | 58 |
| Critical path length (size units) | 98 |
| Retired model | 384 numbered substeps advanced one at a time from a single Current task |

## Work by lane

| Lane | Tasks | Size units | Owning repositories |
|---|---|---|---|
| [Adoption stage](lanes/adoption.md) | 9 | 10 | AI, ArcScope, Cloud, Contracts, Design, DesktopPlatform, Mobile, Plan, Web |
| [Family governance and policy tests](lanes/governance.md) | 16 | 52 | ArcScope, Cloud, Contracts, DesktopPlatform |
| [Contracts schema closures](lanes/contracts.md) | 30 | 72 | Contracts |
| [Foundation values](lanes/foundation.md) | 7 | 8 | DesktopPlatform |
| [Runtime proofs](lanes/runtime-proofs.md) | 7 | 26 | ArcScope, Cloud, DesktopPlatform, Mobile, Web |
| [Desktop platform mechanisms](lanes/platform.md) | 54 | 130 | DesktopPlatform |
| [Native producers and probes](lanes/native.md) | 9 | 18 | DesktopPlatform |
| [Application composition](lanes/app-composition.md) | 8 | 16 | ArcScope, DesktopPlatform |
| [Embedded assistant](lanes/assistant.md) | 21 | 48 | DesktopPlatform |
| [Execution engine](lanes/execution.md) | 9 | 19 | DesktopPlatform |
| [Application presence and tool bridge](lanes/device-bridge.md) | 12 | 22 | Cloud, DesktopPlatform |
| [ArcScope](lanes/arcscope.md) | 26 | 66 | ArcScope |
| [ArcScope Cloud simulator](lanes/simulator.md) | 10 | 36 | ArcScope, Cloud |
| [Cloud core](lanes/cloud.md) | 69 | 158 | Cloud, DesktopPlatform |
| [Commerce, entitlement and credits](lanes/commerce.md) | 16 | 56 | Cloud |
| [Dynamic policy and configuration](lanes/policy.md) | 11 | 26 | Cloud, DesktopPlatform |
| [Operations, support and trust and safety](lanes/operations.md) | 12 | 33 | Cloud, Web |
| [Knowledge search and retrieval](lanes/search.md) | 8 | 19 | Cloud |
| [Extension platform and integrations](lanes/extensions.md) | 1 | 4 | Contracts |
| [Workers AI routing and metering](lanes/ai-routing.md) | 10 | 26 | Cloud |
| [Cloud Harness](lanes/harness.md) | 9 | 44 | Cloud |
| [Android companion](lanes/android.md) | 28 | 71 | Mobile |
| [Web](lanes/web.md) | 34 | 92 | Web |
| [Desktop distribution and update](lanes/updater.md) | 8 | 21 | DesktopPlatform |
| [Release readiness and family release](lanes/release.md) | 9 | 34 | ArcScope, Cloud, Contracts, DesktopPlatform, Mobile, Web |

## Concurrency inside each repository

Tasks on the same delivery level have no prerequisite path between them, so they can be in progress at the same time in one repository, each in its own worktree and write scope, subject only to their declared shared resources. The counts are structural properties of the graph, not measured throughput.

| Repository | Open tasks | Lanes | Widest level (tasks at once) | Ready after its adoption slices | Examples that can run at the same time |
|---|---|---|---|---|---|
| ArcScope | 32 | 6 | level 9: 7 | 1 | [SCOPE.07](lanes/arcscope.md#task-scope-07) Durable capture writer, chunked verifiable store and crash recovery, [SCOPE.12](lanes/arcscope.md#task-scope-12) Visualisation: virtualised rendering, downsampling, cursors and markers, [SCOPE.13](lanes/arcscope.md#task-scope-13) Triggers with pre/post windows, [SCOPE.14](lanes/arcscope.md#task-scope-14) Measurements: scope.measurement.v1 |
| Cloud | 152 | 12 | level 15: 11 | 8 | [CLOUD.14](lanes/cloud.md#task-cloud-14) Device trust and remote gating, [COM.04](lanes/commerce.md#task-com-04) Provider event inbox, [HAR.06](lanes/harness.md#task-har-06) Durable Cloud automation, scheduling and automation-fixture removal, [OPS.10](lanes/operations.md#task-ops-10) Customer push delivery and registration lifecycle |
| Contracts | 31 | 4 | level 3: 7 | 7 | [CON.04](lanes/contracts.md#task-con-04) ContentSandbox service schema (15 methods: session/slot/image/PDF), [CON.05](lanes/contracts.md#task-con-05) Extension/Connector/LocalBootstrap service schema (annex09 helper closure minus ContentSandbox), [CON.12](lanes/contracts.md#task-con-12) Extension and policy schemas: manifest.v1/workflow.v1/panel.v1/policy body.v1/configuration.v1, [CON.16](lanes/contracts.md#task-con-16) Signed catalog/update/realm formats (catalog-index.v1, catalog-revocations.v1, android-update.v1, realm.v1) |
| DesktopPlatform | 134 | 13 | level 7: 20 | 8 | [EXE.02](lanes/execution.md#task-exe-02) Lifecycle states and reason facets, [GOV.20](lanes/governance.md#task-gov-20) Build.Policy banned-symbol scanner: audit unmanaged function-pointer invocations instead of throwing, [NAT.01](lanes/native.md#task-nat-01) Probe A: device tool execution under Native AOT, [PLT.11](lanes/platform.md#task-plt-11) Child registration lifecycle |
| Mobile | 30 | 3 | level 22: 5 | 1 | [AND.07](lanes/android.md#task-and-07) Foundation integration evidence: real candidate against deployed 22/23/24/25, [AND.08](lanes/android.md#task-and-08) Authentication, Home and workspace (AN01-AN06), [AND.12](lanes/android.md#task-and-12) Presence, push, links and settings (AN20-AN24), [AND.24](lanes/android.md#task-and-24) Real CF Harness generation/tool loop observed end to end on Android |
| Web | 39 | 4 | level 11: 8 | 0 | [OPS.04](lanes/operations.md#task-ops-04) Status page, [WEB.02](lanes/web.md#task-web-02) Versioned public content and pricing inputs (catalogue.json), [WEB.03](lanes/web.md#task-web-03) Rendering and performance, [WEB.04](lanes/web.md#task-web-04) Internationalisation |

## Critical path

| # | Task | Size | Title |
|---|---|---|---|
| 1 | [ADOPT.01](lanes/adoption.md#task-adopt-01) | M | Retarget repository instructions and freeze the adoption baseline |
| 2 | [ADOPT.03.contracts](lanes/adoption.md#task-adopt-03-contracts) | S | Adopt Contracts: Contracts schema closures |
| 3 | [CON.23](lanes/contracts.md#task-con-23) | M | Retire the contract and naming elements outside the product family |
| 4 | [CON.02](lanes/contracts.md#task-con-02) | M | Capability/action/context/version/health descriptor records + immutable oversized-body reference (EncodedBodyRef) |
| 5 | [CON.06](lanes/contracts.md#task-con-06) | L | Product in-process port completion: IScopeOperations/IChatOperations + infra ports |
| 6 | [CON.10](lanes/contracts.md#task-con-10) | L | Task/approval/bridge/chat/agent/automation/search operation registry + ai-internal package |
| 7 | [CON.11](lanes/contracts.md#task-con-11) | M | Application/history/execution/events operations (annex10's 13 additions) + EventService.Poll |
| 8 | [CON.07](lanes/contracts.md#task-con-07) | L | Identity/session/device operation registry + native-auth and browser HTTP exceptions |
| 9 | [WEB.40](lanes/web.md#task-web-40) | XL | Blazor migration of the existing Web (C# static Site, Blazor WebAssembly profiles, C# policy) |
| 10 | [CON.40](lanes/contracts.md#task-con-40) | L | C#-only SDK standardization: stop TypeScript and Kotlin/Maven publication after consumer migration; keep @arcforges/ai-internal |
| 11 | [CON.41](lanes/contracts.md#task-con-41) | S | Publish the public operation metadata in the PublicApi package |
| 12 | [CLOUD.21](lanes/cloud.md#task-cloud-21) | L | Public endpoint mapping and validation |
| 13 | [CLOUD.12](lanes/cloud.md#task-cloud-12) | L | Native and browser authentication with Postmark/SES mail adapters (live delivery evidence blocked-external) |
| 14 | [CLOUD.15](lanes/cloud.md#task-cloud-15) | M | Step-up challenges for sensitive operations |
| 15 | [CLOUD.16](lanes/cloud.md#task-cloud-16) | M | PAT and actor authorization |
| 16 | [CLOUD.19](lanes/cloud.md#task-cloud-19) | L | Browser cookie-session adapter and full account-surface closure |
| 17 | [CLOUD.26](lanes/cloud.md#task-cloud-26) | L | Generated C# clients (native and Grpc.Net.Client.Web browser) against Identity/Workspace/Device |
| 18 | [PRF.12](lanes/runtime-proofs.md#task-prf-12) | L | MAUI Android release proof: Mono AOT release, trimming and R8, 16 KB alignment, signing, unary, server stream, trailers, cancel and Keystore against the proof ingress |
| 19 | [AND.02](lanes/android.md#task-and-02) | L | Real MAUI module graph and AN01-AN28 route/state contracts |
| 20 | [AND.05](lanes/android.md#task-and-05) | L | SQLite history, drafts, outbox and receipts (versioned migrations through an admitted Apache-2.0 SQLite binding) |
| 21 | [AND.09](lanes/android.md#task-and-09) | L | Conversations and context (AN07-AN10/15/16) |
| 22 | [AND.24](lanes/android.md#task-and-24) | M | Real CF Harness generation/tool loop observed end to end on Android |
| 23 | [HAR.05](lanes/harness.md#task-har-05) | XL | Own-application execution proof and fixture turn-endpoint removal |
| 24 | [HAR.90](lanes/harness.md#task-har-90) | M | Verify owned artifact and real integration (Harness) |
| 25 | [REL.06](lanes/release.md#task-rel-06) | XL | Cloud/AI production readiness (deployment, migration, backup, self-host) |
| 26 | [REL.09](lanes/release.md#task-rel-09) | L | Combined disaster drill and operational readiness confirmation |
| 27 | [REL.11](lanes/release.md#task-rel-11) | L | Family release readiness audit and honest statement |

## Level widths

| Level | Tasks |
|---|---|
| 1 | 1 |
| 2 | 58 |
| 3 | 25 |
| 4 | 22 |
| 5 | 29 |
| 6 | 22 |
| 7 | 28 |
| 8 | 24 |
| 9 | 30 |
| 10 | 21 |
| 11 | 28 |
| 12 | 23 |
| 13 | 23 |
| 14 | 15 |
| 15 | 14 |
| 16 | 12 |
| 17 | 9 |
| 18 | 12 |
| 19 | 13 |
| 20 | 12 |
| 21 | 14 |
| 22 | 12 |
| 23 | 9 |
| 24 | 6 |
| 25 | 4 |
| 26 | 4 |
| 27 | 2 |
| 28 | 2 |
| 29 | 1 |
| 30 | 1 |
| 31 | 1 |

## Simulated makespan (unmeasured estimate)

Assumptions: task effort is its relative size (S=1, M=2, L=4, XL=8 units, never measured); every worker can execute any task; review, CI, merge-queue and publication latency are not modelled; tasks accepted before this plan count as complete; the baseline freeze runs first and every adoption slice is one unit; a task starts when its start prerequisites and the adoption slice of its repository and lane are complete, and finishes no earlier than its completion prerequisites; ready tasks are scheduled longest-remaining-path first. The retired model executed the same work one substep at a time, so its makespan equals the one-worker row. Real throughput will be lower where review capacity, merge queues, shared environments, hardware and provider access, or the single heavy local build slot per workstation become the constraint.

| Workers | Makespan (size units) | Estimated speed-up over one worker |
|---|---|---|
| 1 | 1125 | 1.0× |
| 2 | 564 | 2.0× |
| 4 | 283 | 4.0× |
| 8 | 143 | 7.9× |
| 16 | 98 | 11.5× |
| 32 | 98 | 11.5× |
| 64 | 98 | 11.5× |
| unbounded | 98 | 11.5× |

## Provisional initial ready set

Tasks whose start prerequisites are satisfied once their adoption slices have confirmed the accepted baseline, assuming no other existing work is inherited. The actual first ready set is established slice by slice during adoption and grows as reviewed existing work is recorded as inherited.

[AND.01](lanes/android.md#task-and-01), [CLOUD.01](lanes/cloud.md#task-cloud-01), [CLOUD.44](lanes/cloud.md#task-cloud-44), [CLOUD.55](lanes/cloud.md#task-cloud-55), [COM.01](lanes/commerce.md#task-com-01), [COM.02](lanes/commerce.md#task-com-02), [COM.05](lanes/commerce.md#task-com-05), [CON.04](lanes/contracts.md#task-con-04), [CON.05](lanes/contracts.md#task-con-05), [CON.12](lanes/contracts.md#task-con-12), [CON.16](lanes/contracts.md#task-con-16), [CON.17](lanes/contracts.md#task-con-17), [CON.18](lanes/contracts.md#task-con-18), [CON.23](lanes/contracts.md#task-con-23), [FND.01](lanes/foundation.md#task-fnd-01), [FND.02](lanes/foundation.md#task-fnd-02), [FND.03](lanes/foundation.md#task-fnd-03), [FND.04](lanes/foundation.md#task-fnd-04), [FND.05](lanes/foundation.md#task-fnd-05), [FND.06](lanes/foundation.md#task-fnd-06), [GOV.17](lanes/governance.md#task-gov-17), [NAT.03](lanes/native.md#task-nat-03), [OPS.01](lanes/operations.md#task-ops-01), [POL.01](lanes/policy.md#task-pol-01), [SCOPE.02](lanes/arcscope.md#task-scope-02)

## Remaining serial dependencies and bottlenecks

- **Adoption stage.** A one-time entry condition per repository and lane: each adoption slice opens its own tasks as soon as it is recorded, independently of other slices and repositories. It adds one short review step in front of each lane, and slices run in parallel.
- **Contracts merge queue.** Closures are authored concurrently, but every merge to Contracts main publishes all packages at one version, so merges are ordered through one integration owner. Consumers wait only for the closure they use; the descriptor closure and the operation closures their lanes need are the most shared.
- **Cloud foundation chain.** Host pipeline, module boundary and plan bridge, migration runner and physical mapping, identity core, sessions and endpoint mapping precede most Cloud modules and the Harness. It is the densest Cloud prefix and carries must-be-real-early proofs (real email, guarded D1 batches).
- **Assistant and device-bridge chain.** Local helper gRPC and the security decision pipeline precede the assistant Cloud client, the device bridge and the Harness execution proof. Each assistant surface starts from the specific history, context and bridge components it uses, not from package acceptance.
- **Harness fixture removal.** The fixture turn endpoint is deleted only after the desktop assistant, Android and Web consumers each switch to the real Harness, so the Harness proof waits for the slowest consumer switch-over.
- **Android distribution and real push.** The Android companion release chain (foundation, companion acceptance, signed artifacts, physical-device gates and distribution) ends in the real push proof on the distributed artifact ([PG-24](../../assurance/open-gates-register.md#rule-pg-24)). The Operations package acceptance includes that proof and Cloud and AI production readiness include the Operations acceptance, so this chain joins Android distribution to the Cloud release tail. Android features themselves start from the foundation modules and need the deployed-service evidence only to complete.
- **Release tail.** Cloud and AI production readiness, the combined disaster drill and the family release are necessarily sequential and require every obligation package accepted.
- **External prerequisites.** Hardware-lab devices, provider accounts (mail, payment, payout, push, independent backup storage) and signing custody can block acceptance regardless of worker count. They are recorded on tasks and never passed without evidence.
- **Exclusive resources and review capacity.** The deployed Cloud test environment during live runs, the lockstep publication queues of Contracts and DesktopPlatform, the heavy local build slot per workstation and reviewer availability are not modelled in the makespans and will lower real throughput.
