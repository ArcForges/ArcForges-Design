# Asset disposition and retirement gates

This index is normative for migration. Exact class/file/table/consumer findings are in the [local audit §6–8](../research/runtime-audit.md) and [cloud/shared audit](../research/cloud-audit.md), both pinned to the [baseline](../research/baseline.md). Those audit tables are the detailed per-asset inventory; their historical implementation labels are evidence, not delivery status. When an asset needs extraction and later removal, the target below names the surviving responsibility and the final deletion explicitly.

| Asset and owner | Decision | Retained/new responsibility | Removal or migration boundary | V2 owner |
|---|---|---|---|---|
| ArcForges resource samplers, pure pressure/budget math | KEEP | Host observation, headroom, conservative memory and bounded pressure | Re-test with new Run/native scope inputs | AFV2-RES-01 |
| ResourceMonitor, CriticalShedding, running-attempt accounting and fairness | REWORK | Run/Sandbox grants and pressure response | Delete Task/pool/queue/AI coupling | AFV2-RES-01, AFV2-RES-03 |
| Windows ProcessLauncher/AttemptRunner and Linux execution/guard launchers | REPLACE_WITH_MXC | Official admitted backend creates payload | Keep essential executor until complete profile/core/local acceptance; then delete old launch runtime | AFV2-MXC-04, AFV2-CORE-02, AFV2-MIG-01 |
| Windows Job and Linux systemd/cgroup control primitives | REWORK | Resource-before-exec ownership, limits and independent readback/cleanup | Old nesting topology is not transplanted; no use of private MXC Job handle | AFV2-RES-02 |
| DirectAttemptHandle, host-process adoption and escaped-process inference | REMOVE | No uncontained or foreign-process fallback | Delete at new runtime cutover | AFV2-MIG-01 |
| Task/Attempt/DAG/retry/queue/pool/ToolConcurrency implementation | REMOVE | Immediate bounded Run admission only | Drain old work; export historic records without relabeling | AFV2-RES-03, AFV2-MIG-01, AFV2-MIG-02 |
| Node/Client/LocalRpc/store/supervisor infrastructure | REWORK | One core, protected endpoint, durable receipts and per-Run owner | Preserve useful transaction/recovery identity; eliminate old business composition | AFV2-DATA-01, AFV2-CORE-01, AFV2-REC-01 |
| CLI parsing/output/config helpers | REWORK | First-class offline Sandbox/Run/resources/data commands | Remove old diagnostic-only local gate, Task/queue/job/AI flags | AFV2-CLI-01, AFV2-CLI-02 |
| Native file identity/staging/quarantine/recovery primitives | REWORK | Owned Sandbox import/export/delete | Preserve unknown-effect safety, remove broad host editor/search/workspace platform | AFV2-FILE-01, AFV2-FILE-02 |
| Desktop scaffold/Avalonia closure in ArcForges | REMOVE | No standalone desktop product | Remove early after consumer inventory; keep Node supervisor | AFV2-BASE-02 |
| Cache/CAS/toolchain/AI/LAN/mobile dormant tables and planned contracts | REMOVE | No replacement abstractions | Some never shipped; delete actual schemas/configs, not invented implementations | AFV2-MIG-02 |
| Go Center identity/enrollment/channel/PostgreSQL | REWORK | Secure optional remote management with local grants | Retain actual source assets; qualify schema10/11 guards and migrate typed methods | AFV2-CENTER-01, AFV2-CENTER-02, AFV2-CENTER-03 |
| Go self-host mode and entitlement resolver | KEEP | Explicit official/self-host service mode | Replace obsolete entitlement keys; never add local paid gate | AFV2-HOST-01 |
| Commerce/provider/account lifecycle interfaces | REWORK | Implement actual Go web commerce and missing lifecycle flows | Generated interfaces/scaffold are not implementation; no mobile purchases | AFV2-ID-01, AFV2-HOST-02 |
| Old C# Center, TaskService/Fleet/Relay host-file business routes | REMOVE | Typed V2 routes in Go and same Node Core | Finite bridge/cutover preserves security floors and uncertain receipts; no permanent double runtime | AFV2-MIG-01 |
| Cloud guarded deployment and operations | REWORK | Self-host instructions, hosted service controls, recovery and cost bounds | Retire cancelled AI/mobile dashboards; preserve main-push/security admission | AFV2-HOST-03 |
| Web Blazor/static/CSP/build infrastructure | KEEP | Browser delivery and origin/identity foundation | Reuse proven build assets; no claim existing Dashboard is complete | AFV2-WEB-01 |
| Web probe/Hello/chat/operations pages | REWORK | Seven modern responsive management areas with real APIs | Replace navigation/page models; remove unused probe production routes | AFV2-WEB-01, AFV2-WEB-02, AFV2-WEB-03, AFV2-WEB-04 |
| Contracts foundation and published v1 cohorts | KEEP | Immutable public history and shared consumers | Stop ArcForges consumption where obsolete; source retirement is separate from registry artifact deletion | AFV2-API-01, AFV2-MIG-01 |
| New Sandbox/management APIs | REWORK | Explicit V2 namespaces/C#/Go/browser bindings | Never reuse shared ContentSandbox local v1 | AFV2-API-01 |
| DesktopPlatform LocalRpc, Security.Secrets, Observability, Build.Policy | KEEP | Reuse only actual Node/CLI dependencies | Shared identity/integrity/secret-store boundaries stay; no blanket cleanup | AFV2-BASE-01, AFV2-SEC-01 |
| DesktopPlatform desktop/image/content libraries and Mobile/AI/ArcScope/ArcSlate/ArcNotes | FUTURE | Independent products retain their own code and consumed contracts | Not V2 prerequisites; protect their real call sites and do not force migration | AFV2-BASE-01, AFV2-MIG-01 |
| Plugins/marketplace/network management/GPU/advanced extensions | FUTURE | Research only if separately authorized | No tables/interfaces/projects now | No current delivery task |

The final removal sweep covers source, tests that assert cancelled behavior, registrations, dependency locks, solution entries, build/package inventories, routes, active schema, CLI help/completions, UI navigation and current docs. It must not delete immutable applied migrations, accepted historical evidence, published package versions, shared consumer assets, or development MCP access.

An asset absent from current source is marked absent in the audit and has no fabricated migration cost. Relevant conceptual designs and empty tables still leave current authority. Any new main-branch drift must be audited by the baseline/preflight task before it widens deletion scope.

The [applied Plan source-scope audit](plan-scope-audit.md) checks all 39 task allowlists against these real source locations, including concrete C# Center retirement and shared-consumer preservation. It is dated review evidence; the Plan graph remains the task authority.
