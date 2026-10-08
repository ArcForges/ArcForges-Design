# Schedule Analysis

> Generated from [the delivery graph](delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](README.md).

All values below are computed by Plan tools/delivery.py from the current graph. Structural facts (task counts, edge types, chain length, level widths, critical path) are properties of the documented dependencies. Makespans are unmeasured estimates that depend on the stated assumptions. The retired model advanced the same obligations one numbered substep at a time from a single Current task, so its schedule equals the one-worker row; its package-level graph also made each package wait for every upstream package and each substep wait for the previous one.

## Structural facts (computed from the graph)

| Measure | Value |
|---|---|
| Delivery tasks | 460 (6 carried as accepted baseline), plus 50 adoption slices |
| Dependency edges by type | artifact 1118, contract 116, design 1, integration(completion) 250, release 33 |
| Remaining work (size units: S=1, M=2, L=4, XL=8) | 1183 |
| Longest dependency chain (levels) | 28 |
| Widest level (tasks whose longest prerequisite chain has equal length) | 58 |
| Critical path length (size units) | 81 |
| Retired model | 384 numbered substeps advanced one at a time from a single Current task |

## Work by lane

| Lane | Tasks | Size units | Owning repositories |
|---|---|---|---|
| [Adoption stage](lanes/adoption.md) | 9 | 10 | AI, ArcScope, Cloud, Contracts, Design, DesktopPlatform, Mobile, Plan, Web |
| [Family governance and policy tests](lanes/governance.md) | 23 | 62 | AI, ArcScope, Cloud, Contracts, DesktopPlatform, Mobile, Web |
| [Contracts schema closures](lanes/contracts.md) | 28 | 69 | Contracts |
| [Foundation values](lanes/foundation.md) | 7 | 8 | DesktopPlatform |
| [Runtime proofs](lanes/runtime-proofs.md) | 10 | 35 | ArcScope, Cloud, DesktopPlatform, Mobile, Web |
| [Desktop platform mechanisms](lanes/platform.md) | 55 | 132 | DesktopPlatform |
| [Native producers and probes](lanes/native.md) | 16 | 35 | DesktopPlatform |
| [Application composition](lanes/app-composition.md) | 8 | 14 | ArcScope, DesktopPlatform |
| [Embedded assistant](lanes/assistant.md) | 22 | 49 | DesktopPlatform |
| [Execution engine](lanes/execution.md) | 9 | 19 | DesktopPlatform |
| [Application presence and tool bridge](lanes/device-bridge.md) | 12 | 22 | Cloud, DesktopPlatform |
| [ArcScope](lanes/arcscope.md) | 27 | 67 | ArcScope |
| [ArcScope Cloud simulator](lanes/simulator.md) | 10 | 36 | ArcScope, Cloud |
| [Cloud core](lanes/cloud.md) | 66 | 151 | Cloud, DesktopPlatform |
| [Commerce, entitlement and credits](lanes/commerce.md) | 16 | 56 | Cloud |
| [Dynamic policy and configuration](lanes/policy.md) | 11 | 26 | Cloud, DesktopPlatform |
| [Operations, support and trust and safety](lanes/operations.md) | 13 | 35 | Cloud, Web |
| [Knowledge search and retrieval](lanes/search.md) | 8 | 19 | Cloud |
| [Extension platform and integrations](lanes/extensions.md) | 12 | 32 | Cloud, Contracts, DesktopPlatform |
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
| AI | 2 | 1 | level 3: 1 | 1 | [GOV.19](lanes/governance.md#task-gov-19) AI Wrangler and undici dependency admission (clear the repository security gate) |
| ArcScope | 33 | 6 | level 9: 9 | 2 | [APP.03](lanes/app-composition.md#task-app-03) Clean Native AOT package-consumer composition for ArcScope, [SCOPE.07](lanes/arcscope.md#task-scope-07) Durable capture writer, chunked verifiable store and crash recovery, [SCOPE.09](lanes/arcscope.md#task-scope-09) Long-running capture in the shell, [SCOPE.12](lanes/arcscope.md#task-scope-12) Visualisation: virtualised rendering, downsampling, cursors and markers |
| Cloud | 151 | 13 | level 15: 15 | 8 | [CLOUD.32](lanes/cloud.md#task-cloud-32) Durable unary fallback (Poll/readOutput), [COM.09](lanes/commerce.md#task-com-09) Ledgers and reconciliation, [DEV.04](lanes/device-bridge.md#task-dev-04) Execution and result deduplication -- Cloud D1 attempt/result store, [HAR.06](lanes/harness.md#task-har-06) Durable Cloud automation, scheduling and automation-fixture removal |
| Contracts | 31 | 4 | level 3: 7 | 7 | [CON.04](lanes/contracts.md#task-con-04) ContentSandbox service schema (15 methods: session/slot/image/PDF), [CON.05](lanes/contracts.md#task-con-05) Extension/Connector/LocalBootstrap service schema (annex09 helper closure minus ContentSandbox), [CON.12](lanes/contracts.md#task-con-12) Extension and policy schemas: manifest.v1/workflow.v1/panel.v1/policy body.v1/configuration.v1, [CON.16](lanes/contracts.md#task-con-16) Signed catalog/update/realm formats (catalog-index.v1, catalog-revocations.v1, android-update.v1, realm.v1) |
| DesktopPlatform | 154 | 14 | level 7: 23 | 8 | [EXE.02](lanes/execution.md#task-exe-02) Lifecycle states and reason facets, [GOV.20](lanes/governance.md#task-gov-20) Build.Policy banned-symbol scanner: audit unmanaged function-pointer invocations instead of throwing, [NAT.05](lanes/native.md#task-nat-05) Probe evidence, licence positions, conclusions and hardware-lab inventory seed, [PLT.11](lanes/platform.md#task-plt-11) Child registration lifecycle |
| Mobile | 32 | 4 | level 18: 5 | 2 | [AND.07](lanes/android.md#task-and-07) Foundation integration evidence: real candidate against deployed 22/23/24/25, [AND.08](lanes/android.md#task-and-08) Authentication, Home and workspace (AN01-AN06), [AND.12](lanes/android.md#task-and-12) Presence, push, links and settings (AN20-AN24), [AND.24](lanes/android.md#task-and-24) Real CF Harness generation/tool loop observed end to end on Android |
| Web | 42 | 5 | level 11: 8 | 0 | [OPS.04](lanes/operations.md#task-ops-04) Status page, [WEB.02](lanes/web.md#task-web-02) Versioned public content and pricing inputs (catalogue.json), [WEB.03](lanes/web.md#task-web-03) Rendering and performance, [WEB.04](lanes/web.md#task-web-04) Internationalisation |

## Critical path

| # | Task | Size | Title |
|---|---|---|---|
| 1 | [ADOPT.01](lanes/adoption.md#task-adopt-01) | M | Retarget repository instructions and freeze the adoption baseline |
| 2 | [ADOPT.07.cloud](lanes/adoption.md#task-adopt-07-cloud) | S | Adopt Cloud: Cloud core |
| 3 | [CLOUD.01](lanes/cloud.md#task-cloud-01) | M | Ingress and host pipeline |
| 4 | [CLOUD.02](lanes/cloud.md#task-cloud-02) | M | Nineteen module boundaries and D1 named-plan bridge |
| 5 | [CLOUD.03](lanes/cloud.md#task-cloud-03) | L | D1 migration runner and exact physical mapping |
| 6 | [CLOUD.06](lanes/cloud.md#task-cloud-06) | M | Shared atomic family guarded-batch engine |
| 7 | [CLOUD.04](lanes/cloud.md#task-cloud-04) | M | Receipts, outbox, inbox dedup and change archive |
| 8 | [COM.16](lanes/commerce.md#task-com-16) | L | Entitlement grant port and durable Entitlement store |
| 9 | [CLOUD.72](lanes/cloud.md#task-cloud-72) | M | Identity production store, identifier source and enrollment family call over the plan-execution port |
| 10 | [CLOUD.13](lanes/cloud.md#task-cloud-13) | M | Device, installation, instance and session (four distinct concepts) |
| 11 | [CLOUD.19](lanes/cloud.md#task-cloud-19) | L | Browser cookie-session adapter and full account-surface closure |
| 12 | [CLOUD.26](lanes/cloud.md#task-cloud-26) | L | Generated C# clients (native and Grpc.Net.Client.Web browser) against Identity/Workspace/Device |
| 13 | [PRF.12](lanes/runtime-proofs.md#task-prf-12) | L | MAUI Android release proof: Mono AOT release, trimming and R8, 16 KB alignment, signing, unary, server stream, trailers, cancel and Keystore against the proof ingress |
| 14 | [AND.02](lanes/android.md#task-and-02) | L | Real MAUI module graph and AN01-AN28 route/state contracts |
| 15 | [AND.03](lanes/android.md#task-and-03) | L | Android runtime and OS adapters (MAUI, Credential Manager, Keystore wrapper, WorkManager, FCM registration, SAF/MediaStore) |
| 16 | [AND.06](lanes/android.md#task-and-06) | M | Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation |
| 17 | [AND.08](lanes/android.md#task-and-08) | L | Authentication, Home and workspace (AN01-AN06) |
| 18 | [AND.13](lanes/android.md#task-and-13) | L | Native interaction and recovery: full experience-02 device matrix |
| 19 | [AND.15](lanes/android.md#task-and-15) | M | Complete companion acceptance |
| 20 | [AND.16](lanes/android.md#task-and-16) | S | Signed Android release artifacts (AAB + direct APK) |
| 21 | [AND.21](lanes/android.md#task-and-21) | L | Physical device and recovery gates |
| 22 | [AND.23](lanes/android.md#task-and-23) | M | Distribution acceptance |
| 23 | [AND.26](lanes/android.md#task-and-26) | M | Real FCM sending and physical Android receipt |
| 24 | [OPS.12](lanes/operations.md#task-ops-12) | S | Owned-artifact receipt |
| 25 | [REL.06](lanes/release.md#task-rel-06) | XL | Cloud/AI production readiness (deployment, migration, backup, self-host) |
| 26 | [REL.09](lanes/release.md#task-rel-09) | L | Combined disaster drill and operational readiness confirmation |
| 27 | [REL.11](lanes/release.md#task-rel-11) | L | Family release readiness audit and honest statement |

## Level widths

| Level | Tasks |
|---|---|
| 1 | 1 |
| 2 | 58 |
| 3 | 28 |
| 4 | 24 |
| 5 | 34 |
| 6 | 30 |
| 7 | 31 |
| 8 | 24 |
| 9 | 38 |
| 10 | 27 |
| 11 | 32 |
| 12 | 27 |
| 13 | 24 |
| 14 | 20 |
| 15 | 25 |
| 16 | 22 |
| 17 | 17 |
| 18 | 15 |
| 19 | 9 |
| 20 | 5 |
| 21 | 2 |
| 22 | 3 |
| 23 | 1 |
| 24 | 1 |
| 25 | 2 |
| 26 | 1 |
| 27 | 2 |
| 28 | 1 |

## Simulated makespan (unmeasured estimate)

Assumptions: task effort is its relative size (S=1, M=2, L=4, XL=8 units, never measured); every worker can execute any task; review, CI, merge-queue and publication latency are not modelled; tasks accepted before this plan count as complete; the baseline freeze runs first and every adoption slice is one unit; a task starts when its start prerequisites and the adoption slice of its repository and lane are complete, and finishes no earlier than its completion prerequisites; ready tasks are scheduled longest-remaining-path first. The retired model executed the same work one substep at a time, so its makespan equals the one-worker row. Real throughput will be lower where review capacity, merge queues, shared environments, hardware and provider access, or the single heavy local build slot per workstation become the constraint.

| Workers | Makespan (size units) | Estimated speed-up over one worker |
|---|---|---|
| 1 | 1183 | 1.0× |
| 2 | 593 | 2.0× |
| 4 | 298 | 4.0× |
| 8 | 150 | 7.9× |
| 16 | 81 | 14.6× |
| 32 | 81 | 14.6× |
| 64 | 81 | 14.6× |
| unbounded | 81 | 14.6× |

## Provisional initial ready set

Tasks whose start prerequisites are satisfied once their adoption slices have confirmed the accepted baseline, assuming no other existing work is inherited. The actual first ready set is established slice by slice during adoption and grows as reviewed existing work is recorded as inherited.

[AND.01](lanes/android.md#task-and-01), [AND.22](lanes/android.md#task-and-22), [CLOUD.01](lanes/cloud.md#task-cloud-01), [CLOUD.44](lanes/cloud.md#task-cloud-44), [CLOUD.55](lanes/cloud.md#task-cloud-55), [COM.01](lanes/commerce.md#task-com-01), [COM.02](lanes/commerce.md#task-com-02), [COM.05](lanes/commerce.md#task-com-05), [CON.04](lanes/contracts.md#task-con-04), [CON.05](lanes/contracts.md#task-con-05), [CON.12](lanes/contracts.md#task-con-12), [CON.16](lanes/contracts.md#task-con-16), [CON.17](lanes/contracts.md#task-con-17), [CON.18](lanes/contracts.md#task-con-18), [CON.23](lanes/contracts.md#task-con-23), [FND.01](lanes/foundation.md#task-fnd-01), [FND.02](lanes/foundation.md#task-fnd-02), [FND.03](lanes/foundation.md#task-fnd-03), [FND.04](lanes/foundation.md#task-fnd-04), [FND.05](lanes/foundation.md#task-fnd-05), [FND.06](lanes/foundation.md#task-fnd-06), [GOV.17](lanes/governance.md#task-gov-17), [GOV.19](lanes/governance.md#task-gov-19), [NAT.03](lanes/native.md#task-nat-03), [OPS.01](lanes/operations.md#task-ops-01), [POL.01](lanes/policy.md#task-pol-01), [SCOPE.02](lanes/arcscope.md#task-scope-02), [SCOPE.10](lanes/arcscope.md#task-scope-10)

## Remaining serial dependencies and bottlenecks

- **Adoption stage.** A one-time entry condition per repository and lane: each adoption slice opens its own tasks as soon as it is recorded, independently of other slices and repositories. It adds one short review step in front of each lane, and slices run in parallel.
- **Contracts merge queue.** Closures are authored concurrently, but every merge to Contracts main publishes all packages at one version, so merges are ordered through one integration owner. Consumers wait only for the closure they use; the descriptor closure and the operation closures their lanes need are the most shared.
- **Cloud foundation chain.** Host pipeline, module boundary and plan bridge, migration runner and physical mapping, identity core, sessions and endpoint mapping precede most Cloud modules and the Harness. It is the densest Cloud prefix and carries must-be-real-early proofs (real email, guarded D1 batches).
- **Assistant and device-bridge chain.** Local helper gRPC and the security decision pipeline precede the assistant Cloud client, the device bridge and the Harness execution proof. Each assistant surface starts from the specific history, context and bridge components it uses, not from package acceptance.
- **Harness fixture removal.** The fixture turn endpoint is deleted only after the desktop assistant, Android and Web consumers each switch to the real Harness, so the Harness proof waits for the slowest consumer switch-over.
- **Android distribution and real push.** The Android companion release chain (foundation, companion acceptance, signed artifacts, physical-device gates and distribution) ends in the real push proof on the distributed artifact ([PG-24](../../assurance/open-gates-register.md#rule-pg-24)). The Operations package acceptance includes that proof and Cloud and AI production readiness include the Operations acceptance, so this chain joins Android distribution to the Cloud release tail. Android features themselves start from the foundation modules and need the deployed-service evidence only to complete.
- **Release tail.** Cloud and AI production readiness, the combined disaster drill and the family release are necessarily sequential and require every obligation package accepted.
- **External prerequisites.** Hardware-lab devices, provider accounts (mail, payment, payout, push, independent backup storage), store listings and signing custody can block acceptance regardless of worker count. They are recorded on tasks and never passed without evidence.
- **Exclusive resources and review capacity.** The deployed Cloud test environment during live runs, the lockstep publication queues of Contracts and DesktopPlatform, the heavy local build slot per workstation and reviewer availability are not modelled in the makespans and will lower real throughput.
