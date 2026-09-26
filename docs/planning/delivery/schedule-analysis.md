# Schedule Analysis

> Generated from [the delivery graph](delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](README.md).

All values below are computed by Plan tools/delivery.py from the current graph. Structural facts (task counts, edge types, chain length, level widths, critical path) are properties of the documented dependencies. Makespans are unmeasured estimates that depend on the stated assumptions. The retired model advanced the same obligations one numbered substep at a time from a single Current task, so its schedule equals the one-worker row; its package-level graph also made each package wait for every upstream package and each substep wait for the previous one.

## Structural facts (computed from the graph)

| Measure | Value |
|---|---|
| Delivery tasks | 529 (6 carried as accepted baseline), plus 58 adoption slices |
| Dependency edges by type | artifact 1269, contract 98, design 1, integration(completion) 201, release 42 |
| Remaining work (size units: S=1, M=2, L=4, XL=8) | 1374 |
| Longest dependency chain (levels) | 19 |
| Widest level (tasks whose longest prerequisite chain has equal length) | 68 |
| Critical path length (size units) | 62 |
| Retired model | 447 numbered substeps advanced one at a time from a single Current task |

## Work by lane

| Lane | Tasks | Size units | Owning repositories |
|---|---|---|---|
| [Adoption stage](lanes/adoption.md) | 11 | 11 | AI, ArcNotes, ArcScope, ArcSlate, Cloud, Contracts, Design, DesktopPlatform, Mobile, Plan, Web |
| [Family governance and policy tests](lanes/governance.md) | 16 | 50 | AI, ArcNotes, ArcScope, ArcSlate, Cloud, Contracts, DesktopPlatform, Mobile, Web |
| [Contracts schema closures](lanes/contracts.md) | 25 | 61 | Contracts |
| [Foundation values](lanes/foundation.md) | 7 | 8 | DesktopPlatform |
| [Runtime proofs](lanes/runtime-proofs.md) | 10 | 31 | ArcNotes, ArcScope, ArcSlate, Cloud, DesktopPlatform, Mobile, Web |
| [Desktop platform mechanisms](lanes/platform.md) | 56 | 134 | DesktopPlatform |
| [Native producers and probes](lanes/native.md) | 25 | 54 | DesktopPlatform |
| [Application composition](lanes/app-composition.md) | 8 | 13 | ArcNotes, DesktopPlatform |
| [Embedded assistant](lanes/assistant.md) | 22 | 49 | DesktopPlatform |
| [Execution engine](lanes/execution.md) | 9 | 19 | DesktopPlatform |
| [Application presence and tool bridge](lanes/device-bridge.md) | 12 | 22 | Cloud, DesktopPlatform |
| [ArcNotes](lanes/arcnotes.md) | 35 | 92 | ArcNotes |
| [ArcScope](lanes/arcscope.md) | 27 | 67 | ArcScope |
| [ArcScope Cloud simulator](lanes/simulator.md) | 10 | 36 | ArcScope, Cloud |
| [ArcSlate](lanes/arcslate.md) | 41 | 125 | ArcSlate |
| [Cloud core](lanes/cloud.md) | 60 | 142 | Cloud, DesktopPlatform |
| [Commerce, entitlement and credits](lanes/commerce.md) | 15 | 52 | Cloud |
| [Dynamic policy and configuration](lanes/policy.md) | 11 | 26 | Cloud, DesktopPlatform |
| [Operations, support and trust and safety](lanes/operations.md) | 13 | 35 | Cloud, Web |
| [Knowledge search and retrieval](lanes/search.md) | 8 | 19 | Cloud |
| [Extension platform and integrations](lanes/extensions.md) | 12 | 32 | AI, Cloud, Contracts, DesktopPlatform |
| [Workers AI routing and metering](lanes/ai-routing.md) | 11 | 28 | AI, Cloud |
| [Cloud Harness](lanes/harness.md) | 9 | 38 | AI, Cloud |
| [Android companion](lanes/android.md) | 26 | 63 | Mobile |
| [Web](lanes/web.md) | 31 | 78 | Web |
| [Desktop distribution and update](lanes/updater.md) | 8 | 21 | DesktopPlatform |
| [Release readiness and family release](lanes/release.md) | 11 | 42 | ArcNotes, ArcScope, ArcSlate, Cloud, Contracts, DesktopPlatform, Mobile, Web |

## Concurrency inside each repository

Tasks on the same delivery level have no prerequisite path between them, so they can be in progress at the same time in one repository, each in its own worktree and write scope, subject only to their declared shared resources. The counts are structural properties of the graph, not measured throughput.

| Repository | Open tasks | Lanes | Widest level (tasks at once) | Ready after its adoption slices | Examples that can run at the same time |
|---|---|---|---|---|---|
| AI | 14 | 4 | level 7: 4 | 0 | [AIR.05](lanes/ai-routing.md#task-air-05) Content-origin marking at the provider generation boundary, [EXT.10](lanes/extensions.md#task-ext-10) Cloud MCP HTTP through the AI Worker adapter, [AIR.07](lanes/ai-routing.md#task-air-07) Provider test-environment coverage, [AIR.09](lanes/ai-routing.md#task-air-09) ASR/Whisper capability closure and inference-late-outcome reconciliation |
| ArcNotes | 40 | 5 | level 6: 8 | 2 | [NOTES.06](lanes/arcnotes.md#task-notes-06) Links, backlinks and outline over the canonical block store, [NOTES.07](lanes/arcnotes.md#task-notes-07) Document-level typed properties and tags (basic), [NOTES.08](lanes/arcnotes.md#task-notes-08) Managed and external attachments (non-PDF): storage, availability, preview levels 1-2, [NOTES.10](lanes/arcnotes.md#task-notes-10) Undo, history, checkpoint and trash as four distinct mechanisms |
| ArcScope | 31 | 5 | level 9: 8 | 2 | [SCOPE.07](lanes/arcscope.md#task-scope-07) Durable capture writer, chunked verifiable store and crash recovery, [SCOPE.09](lanes/arcscope.md#task-scope-09) Long-running capture in the shell, [SCOPE.12](lanes/arcscope.md#task-scope-12) Visualisation: virtualised rendering, downsampling, cursors and markers, [SCOPE.13](lanes/arcscope.md#task-scope-13) Triggers with pre/post windows |
| ArcSlate | 44 | 4 | level 6: 9 | 2 | [SLATE.07](lanes/arcslate.md#task-slate-07) Edit command pipeline and placement operations, [SLATE.10](lanes/arcslate.md#task-slate-10) Project persistence and store infrastructure (V1 migration baseline), [SLATE.15](lanes/arcslate.md#task-slate-15) Native media boundary consumption (ArcSlate.Media wrapper and safety suite), [SLATE.18](lanes/arcslate.md#task-slate-18) Processing graph and keyframe engine (pure evaluation) |
| Cloud | 132 | 13 | level 12: 15 | 9 | [CLOUD.32](lanes/cloud.md#task-cloud-32) Durable unary fallback (Poll/readOutput), [COM.09](lanes/commerce.md#task-com-09) Ledgers and reconciliation, [DEV.04](lanes/device-bridge.md#task-dev-04) Execution and result deduplication -- Cloud D1 attempt/result store, [SIM.05](lanes/simulator.md#task-sim-05) Cloud-side simulation.* operations, manifest listing and segment fetch |
| Contracts | 28 | 4 | level 3: 11 | 11 | [CON.01](lanes/contracts.md#task-con-01) Shard contended eng inventory/constraint files by domain; fix one-owner merge protocol, [CON.02](lanes/contracts.md#task-con-02) Capability/action/context/version/health descriptor records + immutable oversized-body reference (EncodedBodyRef), [CON.04](lanes/contracts.md#task-con-04) ContentSandbox service schema (24 methods: session/slot/media/image/PDF/OTIO), [CON.05](lanes/contracts.md#task-con-05) Extension/Connector/LocalBootstrap service schema (annex09 helper closure minus ContentSandbox) |
| DesktopPlatform | 156 | 14 | level 7: 29 | 10 | [AST.02](lanes/assistant.md#task-ast-02) Branches and window drafts, [EXE.02](lanes/execution.md#task-exe-02) Lifecycle states and reason facets, [NAT.05](lanes/native.md#task-nat-05) Probe evidence, licence positions, conclusions and hardware-lab inventory seed, [PLT.11](lanes/platform.md#task-plt-11) Child registration lifecycle |
| Mobile | 29 | 4 | level 8: 4 | 1 | [AND.06](lanes/android.md#task-and-06) Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation, [AND.09](lanes/android.md#task-and-09) Conversations and context (AN07-AN10/15/16), [AND.10](lanes/android.md#task-and-10) Tasks, approvals and automation (AN11-AN13/19/25), [AND.11](lanes/android.md#task-and-11) Library and resources (AN14-AN18/22) |
| Web | 38 | 5 | level 4: 9 | 3 | [OPS.04](lanes/operations.md#task-ops-04) Status page, [PRF.08](lanes/runtime-proofs.md#task-prf-08) React production build and generated TS SDK proof, [WEB.02](lanes/web.md#task-web-02) Versioned public content and pricing inputs (catalogue.json), [WEB.03](lanes/web.md#task-web-03) Rendering and performance |

## Critical path

| # | Task | Size | Title |
|---|---|---|---|
| 1 | [ADOPT.01](lanes/adoption.md#task-adopt-01) | S | Freeze the adoption baseline |
| 2 | [ADOPT.07.runtime-proofs](lanes/adoption.md#task-adopt-07-runtime-proofs) | S | Adopt Cloud: Runtime proofs |
| 3 | [PRF.07](lanes/runtime-proofs.md#task-prf-07) | XL | Cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof |
| 4 | [PRF.10](lanes/runtime-proofs.md#task-prf-10) | L | Android Kotlin/Jetpack Compose gRPC-Web and CF proof |
| 5 | [AND.01](lanes/android.md#task-and-01) | M | Android production identity and stable toolchain reconciliation |
| 6 | [AND.02](lanes/android.md#task-and-02) | L | Real Android module graph and AN01-AN25 route/state contracts |
| 7 | [AND.03](lanes/android.md#task-and-03) | L | Android runtime and OS adapters (Compose, Credential Manager, Keystore wrapper, WorkManager, FCM registration, SAF/MediaStore) |
| 8 | [AND.06](lanes/android.md#task-and-06) | M | Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation |
| 9 | [AND.08](lanes/android.md#task-and-08) | L | Authentication, Home and workspace (AN01-AN06) |
| 10 | [AND.13](lanes/android.md#task-and-13) | L | Native interaction and recovery: full experience-02 device matrix |
| 11 | [AND.15](lanes/android.md#task-and-15) | M | Complete companion acceptance |
| 12 | [AND.16](lanes/android.md#task-and-16) | S | Signed Android release artifacts (AAB + direct APK) |
| 13 | [AND.21](lanes/android.md#task-and-21) | L | Physical device and recovery gates |
| 14 | [AND.23](lanes/android.md#task-and-23) | M | Distribution acceptance |
| 15 | [AND.26](lanes/android.md#task-and-26) | M | Real FCM sending and physical Android receipt |
| 16 | [OPS.12](lanes/operations.md#task-ops-12) | S | Owned-artifact receipt |
| 17 | [REL.06](lanes/release.md#task-rel-06) | XL | Cloud/AI production readiness (deployment, migration, backup, self-host) |
| 18 | [REL.09](lanes/release.md#task-rel-09) | L | Combined disaster drill and operational readiness confirmation |
| 19 | [REL.11](lanes/release.md#task-rel-11) | L | Family release readiness audit and honest statement |

## Level widths

| Level | Tasks |
|---|---|
| 1 | 1 |
| 2 | 68 |
| 3 | 40 |
| 4 | 50 |
| 5 | 56 |
| 6 | 55 |
| 7 | 65 |
| 8 | 46 |
| 9 | 52 |
| 10 | 38 |
| 11 | 26 |
| 12 | 26 |
| 13 | 20 |
| 14 | 16 |
| 15 | 12 |
| 16 | 5 |
| 17 | 2 |
| 18 | 2 |
| 19 | 1 |

## Simulated makespan (unmeasured estimate)

Assumptions: task effort is its relative size (S=1, M=2, L=4, XL=8 units, never measured); every worker can execute any task; review, CI, merge-queue and publication latency are not modelled; tasks accepted before this plan count as complete; the baseline freeze runs first and every adoption slice is one unit; a task starts when its start prerequisites and the adoption slice of its repository and lane are complete, and finishes no earlier than its completion prerequisites; ready tasks are scheduled longest-remaining-path first. The retired model executed the same work one substep at a time, so its makespan equals the one-worker row. Real throughput will be lower where review capacity, merge queues, shared environments, hardware and provider access, or the single heavy local build slot per workstation become the constraint.

| Workers | Makespan (size units) | Estimated speed-up over one worker |
|---|---|---|
| 1 | 1374 | 1.0× |
| 2 | 688 | 2.0× |
| 4 | 345 | 4.0× |
| 8 | 173 | 7.9× |
| 16 | 87 | 15.8× |
| 32 | 62 | 22.2× |
| 64 | 62 | 22.2× |
| unbounded | 62 | 22.2× |

## Provisional initial ready set

Tasks whose start prerequisites are satisfied once their adoption slices have confirmed the accepted baseline, assuming no other existing work is inherited. The actual first ready set is established slice by slice during adoption and grows as reviewed existing work is recorded as inherited.

[AND.22](lanes/android.md#task-and-22), [CLOUD.01](lanes/cloud.md#task-cloud-01), [CLOUD.44](lanes/cloud.md#task-cloud-44), [CLOUD.55](lanes/cloud.md#task-cloud-55), [COM.01](lanes/commerce.md#task-com-01), [COM.02](lanes/commerce.md#task-com-02), [COM.05](lanes/commerce.md#task-com-05), [CON.01](lanes/contracts.md#task-con-01), [CON.02](lanes/contracts.md#task-con-02), [CON.04](lanes/contracts.md#task-con-04), [CON.05](lanes/contracts.md#task-con-05), [CON.07](lanes/contracts.md#task-con-07), [CON.08](lanes/contracts.md#task-con-08), [CON.12](lanes/contracts.md#task-con-12), [CON.13](lanes/contracts.md#task-con-13), [CON.16](lanes/contracts.md#task-con-16), [CON.17](lanes/contracts.md#task-con-17), [CON.18](lanes/contracts.md#task-con-18), [FND.01](lanes/foundation.md#task-fnd-01), [FND.02](lanes/foundation.md#task-fnd-02), [FND.03](lanes/foundation.md#task-fnd-03), [FND.04](lanes/foundation.md#task-fnd-04), [FND.05](lanes/foundation.md#task-fnd-05), [FND.06](lanes/foundation.md#task-fnd-06), [GOV.04](lanes/governance.md#task-gov-04), [GOV.11](lanes/governance.md#task-gov-11), [GOV.14](lanes/governance.md#task-gov-14), [NAT.03](lanes/native.md#task-nat-03), [NAT.06](lanes/native.md#task-nat-06), [NOTES.13](lanes/arcnotes.md#task-notes-13), [NOTES.21](lanes/arcnotes.md#task-notes-21), [OPS.01](lanes/operations.md#task-ops-01), [POL.01](lanes/policy.md#task-pol-01), [PRF.07](lanes/runtime-proofs.md#task-prf-07), [SCOPE.02](lanes/arcscope.md#task-scope-02), [SCOPE.10](lanes/arcscope.md#task-scope-10), [SLATE.01](lanes/arcslate.md#task-slate-01), [SLATE.13](lanes/arcslate.md#task-slate-13), [WEB.01](lanes/web.md#task-web-01), [WEB.08](lanes/web.md#task-web-08)

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
