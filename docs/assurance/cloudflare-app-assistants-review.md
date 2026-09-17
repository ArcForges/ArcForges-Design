# Cloudflare and Application Assistants — Final Design Review

Date: 2026-09-16. Baseline: `e974df5d0724247f4556d038b1e80c4603edd033`, after PR9. Decision: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012). This review covers the current documentation change, not implementation readiness.

## 1. Method and scope

The work followed collection, consolidation, reviewed edit plan, concentrated edits and a complete resulting-design review. Collection and its review were committed in the local Plan repository before formal edits. The second pass followed the implementer's sequence, checked each changed producer/consumer boundary, reconciled the current main bodies and applied only corrections to the agreed scope. No subagents, implementation changes, reference execution, package publication or deployment were used.

The reviewed scope includes all three professional desktops, reusable assistant features, Kotlin Android, Web, Cloud/AI, generated Contracts, native package producers, identity/permissions, data ownership, commerce, release, upgrade and recovery. Current requirements and retained product profiles remain binding. Reference sources supplied targeted behavior evidence; their unrelated functionality did not become requirements. Archived input bodies were excluded. Eleven dated assurance reports remain unchanged.

## 2. Resulting design and closure

| Closure | Decision and authoritative definition | Implementation and independent evidence owner |
|---|---|---|
| K01 portfolio | Nine active repositories; three standalone professional desktops; independent per-application assistant/store/channel in [architecture27](../architecture/27-platform-projects-and-application-assistants.md) | WP01/14/17; isolated package consumers |
| K02 package ownership | Concrete Platform projects, dependencies and public host ports; five Assistant packages plus Cloud.Client/Device.Runtime in architecture27 and [registry01](../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry) | WP14 abstractions, WP15 core/store, WP17 UI/cloud fixture, WP23–26/52 real adapters; native WP13 unchanged |
| K03 history | [Model05](../architecture/data-model/05-application-history.md): local/Cloud/temporary bodies, exact SQLite tables/operations, per-window drafts, explicit restartable promotion and deletion | WP15/25.09/31/49/52; lost acknowledgement and interrupted output cases |
| K04 transport | [Annex10](../architecture/contracts/10-application-scope-and-streams.md): binary gRPC-Web, unary commands and finite server streams in C#/TS/Kotlin; explicit standard/private exceptions | WP03/06/23/24/31/49/52; actual protocol/RID/device receipts |
| K05 local processes | [IPC03](../architecture/03-local-ipc-and-process-model.md) and [helper09](../architecture/contracts/09-local-grpc-and-sandbox.md): product ports in process, private generated gRPC only for admitted parent/child boundaries | WP06/08/11/13/14; OS isolation and no product listener |
| K06 D1 execution | [D1 profile](../architecture/data-model/04-d1-execution-profile.md): named prepared plans through a private Worker bridge, guarded atomic batches, exact values and idempotent receipts | WP21/24; real D1 rollback/concurrency/publication tests |
| K07 data and transactions | Existing logical aggregates/atomic families preserved; one database per realm, explicit capacity/admission/migration rules | WP21/25/42/44/46; measured workload and commercial race cases |
| K08 search | Own-application retrieval, D1 FTS5/Vectorize derived indexes and current owner authorization; exact Notes scalar semantics preserved | WP19/28/40; stale index, missing index, permission and numeric fixtures |
| K09 operations | Sleeping Containers with checkpointed work; D1 export/change archives, Time Travel and independent restrictive restore journal; existing RPO/RTO preserved | WP21/45/46/50; actual independent restore, capacity and generation drills |
| K10 Android | [25-route native UI](../experience/02-android-companion.md): five-tab navigation, selected application, permissions, push, offline work and process death | WP30/31/32; emulator plus physical Android evidence |
| K11 assistant UX | [13 surfaces](../experience/01-embedded-assistant.md): docked/floating/expanded windows, complete feature navigation, composer/context/approval/results and host ports | WP10/14/15/17; native input/accessibility and clean package-only hosts |
| K12 device control | Frozen product/device/installation target and epoch; current local reauthorization; no retargeting of pending commands or approvals | WP22/26/31/52; stale/forged target, restart, timeout and unknown-effect cases |
| K13 contracts | [335 existing operation scope assignments](../architecture/contracts/11-operation-scope-manifest.md), 13 new operations, appended fields, archive records and effective authorization/retry profiles | WP03 complete immutable NuGet/npm/Maven artifacts; downstream real consumers |
| K14 future boundary | [Separate future examples](../future/cross-product-collaboration/README.md); WP20 reserved, no active dependency or release requirement | Active registration/tool/UI exclusions; future work requires a separate accepted plan |
| K15 executable plan | [Sequence](../planning/implementation-sequence.md), phase groups, both dependency indexes, package headers and producer stages agree | 51 active WPs, 157 edges; .90 receipts supplement concrete production substeps |
| K16 evidence | Link/anchor, graph, scope, UI/package inventory and SQL-shape checks; final correction ledger below | Documentation E0–E2 only; runtime/provider/financial gates remain open |

## 3. Corrections from the final pass

The final pass removed remaining active WP20 references from the serial/phase/traceability lists, replaced residual Android native-gRPC and AI custom-stream text, and corrected package names and producer registrations. Assistant.Abstractions is produced before its Core/UI consumers. The package registry now includes all five assistant packages and the communication packages. The sandbox table separates WP11 launch/protocol production from WP13 production-parser composition.

The pass also closed the local-history Cloud metadata path: local agent Tasks and ordinary turns retain typed execution/usage receipts without dummy Cloud Chat messages; transient body loss is distinct from a failed execution. The archive records now carry explicit per-branch ordinals/timestamps, and all 13 added operations have concrete authorization, retry and compatibility profiles. The new history-import producer is in WP25's main work and evidence table. These are corrections to the planned history/contract boundary, not additional product features.

## 4. Validation receipts and limits

| Check | Result |
|---|---|
| Markdown diff whitespace | `git diff --check` passes |
| File/anchor scan outside excluded archive | No broken current-design links introduced. Two pre-existing broken links remain only in the unchanged dated `design-repair-verification.md` at lines312/319; baseline bytes match exactly |
| Active dependency graph | 51 nodes, 157 edges, acyclic; reciprocal downstream lists agree; serial order is topological and every active WP occurs in exactly one phase; WP20/27/29 absent |
| Operation scope inventory | All 335 registry bindings match the unique scope manifest; eight closed classes; 13 distinct added operations with no duplicate existing operation ID |
| UI/package inventories | 13 assistant surfaces, 25 Android routes, eight UX acceptance groups; five Assistant package identities in both project plan and registry |
| D1 SQL shape on Python SQLite | Invalid revision guard rolls back owner/receipt/outbox changes; successful batch commits them; duplicate receipt failure rolls back; command guard is cleaned up |
| Local history SQL shape | Documented DDL creates successfully with foreign keys enabled; this is not a complete storage implementation test |
| Source/workspace isolation | Main Design checkout stays at the baseline; ten implementation repositories retain their recorded clean heads; all formal changes are Markdown in the independent worktree; native ABI registry and dated assurance reports unchanged |

The local SQLite checks do **not** validate D1 bindings, D1 batch limits, production concurrency, AOT, OS containment, CF streaming, Android lifecycle, signing, push, model behavior or commerce. Their named implementation gates remain open. Hello World artifacts and successful package publication are not accepted substitutes.

Two material provider constraints are explicit design limits: D1 has a [hard database size bound](https://developers.cloudflare.com/d1/platform/limits/), and Container/DO HTTP streams must be budgeted as active connections rather than assumed to use [WebSocket hibernation](https://developers.cloudflare.com/durable-objects/reference/faq/). Independent S3 COMPLIANCE backup remains a deliberate recovery exception; a [removable R2 bucket lock](https://developers.cloudflare.com/r2/buckets/bucket-locks/) is not substituted for it. Actual production capacity and recovery must be demonstrated before paid launch.

## 5. Disposition

The agreed documentation changes and K01–K16 closure conditions are satisfied at design level. No product-scope decision is awaiting user input. Current implementation work starts from the updated producer sequence and must satisfy its actual artifact/runtime gates. Cross-product collaboration and cross-realm automatic repartitioning have no current implementation commitment; they cannot be quietly enabled by reusing reserved descriptors or database utilities.
