# Applied Plan source-scope audit

All 39 delivery tasks were checked against the pinned source layout. Exact applied path arrays and future-path notes live in the current [Plan graph](https://github.com/ArcForges/Plan/blob/plan/v2-cli-sandbox-20261114/delivery-graph.json). This is a dated source/layout audit supporting review finding R1, not a second task authority. The read-only scope auditor proposed paths; the coordinator applied and validated the repaired graph. No product source was changed.

## Source identity

| Repository | Pinned source commit |
|---|---|
| ArcForges | `10f692224f94916cfc93fbad971f80ec340c5edf` |
| Cloud | `6df33c525fcbc20495e46c9c4c011086146da796` |
| Contracts | `de3dba76266e89654be9b4d29d097d525a281c6a` |
| Web | `56bb40fe7d1693013b4b1e2a82f1b796a65629c5` |
| DesktopPlatform | `e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6` |

Reviewed task-path baseline: Plan commit `4e22eb17c79266e3e9cd003f3b4af9e27e0070e2`. The parent is separately repairing its current task acceptance/dependencies; replacement arrays do not overwrite those fields.

## Incorrect existing-path references

| Original reference | Actual pinned location / correction |
|---|---|
| Contracts `proto/**` | `public/proto/**` and `internal/proto/**` |
| Contracts `packages/**` | Generated language packages are under `src/**` and `go/**`; fixtures and checks are `fixtures/**` and `tests/**` |
| Contracts `buf.yaml`, `buf.gen.yaml` | Neither exists; actual code generation lives in `eng/**` |
| Cloud `center/internal/node/**` | Existing registry/enrollment adapter is `fleetapi/**`, domain is `fleet/**`; new V2 management adapter is explicitly planned `management/**` |
| Cloud `center/internal/identitytests/**` | Identity API implementation and co-located tests live in `identityapi/**` |
| Cloud `center/internal/httpapi/**` | Browser account/enrollment pages live in `pages/**`; composition is `server/**` |
| Cloud `src/ArcForges.Cloud.Runtime*`, `src/ArcForges.Cloud.Host*` | Neither exists; actual host is `src/ArcForges.Cloud/**`, backed by the listed `Modules.*` and `Storage.D1` projects |
| Cloud/Web `eng/deploy/**` | Actual deploy/candidate implementation is `tooling/**`, Worker/root configuration and Cloud Dockerfile; Cloud `deploy/**` currently contains monitoring |
| ArcForges `eng/packaging/**` | Actual `eng/package.ps1`, `eng/publish.ps1`, `eng/verify_linux.py`, `packaging/**` |
| ArcForges `eng/admission/**` | Actual `eng/policy/dependency-admissions.json` |
| ArcForges `tests/ArcForges.CommandLine.Tests/**` | There is no such project; CLI tests are in `tests/ArcForges.Client.Tests/**` |
| ArcForges `Node.Core/CenterRouting.cs` | Actual `src/ArcForges.Node.Core/Security/CenterRouting.cs` |
| ArcForges `Node.Platform/WorkspacePath*` | Actual partial class and supporting safety primitives are in `src/ArcForges.Node.Core/Platform/**` |
| Assumed Web solution name | Actual solution is `win.slnx` |

## Wiring and generated-output scope

ArcForges `Node.Api/NodeApiServer.cs` registers the concrete handlers, and `Node.Api/NodeHost.cs` composes the runtime, dispatcher and `CloudLinkService`. `Node.Core/NodeRuntime.cs` is the Core composition point. New source-only handler directories cannot complete the advertised observable path without these existing adapters. New Sandbox/Run/Data/resource and CenterControl tasks therefore include their composition points and actual existing test projects.

`CommandLine/CliApplication.cs` directly registers the command groups. CLI01 owns the complete offline core/admin CLI. FILE01/02 own their data/delete command and Client integration. CENTER02 owns Center connect/flow/disconnect/status/cancel/signout, the local typed `CenterControlServiceHandler.cs`, Client integration, and the existing `CenterCommands.cs`/`LoginCommands.cs`. `Node.CloudLink/**` is the existing bounded project containing CloudLinkService, SignInOrchestrator and protected credentials/control-file handling. The V2 adapter must not depend on the obsolete Node.v1 dispatcher merely to obtain those services.

In Cloud, `center/internal/server/server.go` constructs `identityapi`, `fleetapi` and `mobileauth`; `server/routed.go` bridges `fleetapi` to the hub. Routes also have a generated Worker table: `center/internal/workertables/**`, `center/cmd/center-gen/**`, and `worker/tables/center-tables.generated.ts`. Every task changing the route catalogue or identity/enrollment/control adapters includes those points. CENTER02/03/04 also include `center/internal/schema/**`, `store/**`, `pgtest/**` and Node.Store/tests so `node_owner_epoch` remains bound to enrollment/routed command identity across channel replacement, re-handshake and reconciliation.

WEB02/03 now include the existing `ArcForges.Web.App` project, not just `App/Pages`: typed clients, session state, view models and `Program.cs` wiring belong to the same bounded module. Existing `Web.Ui` and real browser/component test scopes remain present. HOST03 prepares actual infrastructure and deployment composition; the complete new Go/PostgreSQL/Blazor assembly belongs to DIST01 after WEB04 and consumer cutover.

## Concrete C# Cloud retirement coverage

`Cloud.slnx` names these 22 real projects:

- `src/ArcForges.Cloud/**`
- `src/ArcForges.Cloud.Storage.D1/**`
- `src/ArcForges.Cloud.Modules.Abstractions/**`
- `src/ArcForges.Cloud.Modules.Agent/**`
- `src/ArcForges.Cloud.Modules.Audit/**`
- `src/ArcForges.Cloud.Modules.Chat/**`
- `src/ArcForges.Cloud.Modules.Commerce/**`
- `src/ArcForges.Cloud.Modules.Configuration/**`
- `src/ArcForges.Cloud.Modules.Devices/**`
- `src/ArcForges.Cloud.Modules.Entitlement/**`
- `src/ArcForges.Cloud.Modules.Identity/**`
- `src/ArcForges.Cloud.Modules.Notification/**`
- `src/ArcForges.Cloud.Modules.PackageCatalog/**`
- `src/ArcForges.Cloud.Modules.Policy/**`
- `src/ArcForges.Cloud.Modules.Resource/**`
- `src/ArcForges.Cloud.Modules.Scope/**`
- `src/ArcForges.Cloud.Modules.Search/**`
- `src/ArcForges.Cloud.Modules.Support/**`
- `src/ArcForges.Cloud.Modules.Sync/**`
- `src/ArcForges.Cloud.Modules.Task/**`
- `src/ArcForges.Cloud.Modules.TrustSafety/**`
- `src/ArcForges.Cloud.Modules.Workspace/**`

The pinned `Dockerfile` compiles and copies both C# and Go binaries but its final entrypoint is `/app/ArcForges.Cloud`. `worker/foundation/cloud-container.ts` selects Go through `ARCFORGES_HELLO_RUNTIME`; otherwise the old runtime path remains reachable. MIG01 therefore includes Dockerfile, Worker, actual tooling/build provenance, solution/package entries, generator `tools/ArcForges.Cloud.Generation/**`, and actual C#/Worker tests. Source removal alone would leave the old release path incompletely retired.

The Worker foundation also contains the necessary Go Container transport/lifecycle. Its whole directory is not disposable. Rework the remaining transport and remove its old runtime switch/old AI-mobile settings after their consumers are retired. Similarly, enrollment/session/keys/authentication in Go fleet/fleetapi/server remain required; only the obsolete Task/Fleet/file/mobile behaviors are retired after V2 replacements are accepted. Applied migration/D1 history remains immutable evidence.

MIG01's ArcForges source wildcard is narrowed to named current Node/Core/Store/CloudLink/platform/CLI/Client/Host/Supervisor projects plus the planned RunSupervisor project. `ArcForges.Supervisor` is the existing Node startup supervisor, distinct from the new RunSupervisor process; a similarly named project is not automatically obsolete.

The recommendation removes DesktopPlatform write scope from MIG01 because no concrete source adaptation was identified. Cross-repository consumer inspection/build verification does not require write permission. A later demonstrated necessary change must declare its actual module, rather than treating independent products as collateral cleanup. MIG02 Contracts is correspondingly restricted to `eng/v2-consumers/**`: its live SQLite/PostgreSQL contraction work does not require proto source edits. Published package versions remain immutable; any approved current-source API retirement is the finite consumer-gated MIG01 work.

## Legitimate planned paths

Absence from current main is expected for V2 implementation modules. The recommendation explicitly classifies every unmatched pattern instead of treating future files as broken references:

| Repository | Planned examples |
|---|---|
| ArcForges | `tools/ArcForges.MxcProbe/**`, `eng/mxc/**`, `Node.Platform/Capabilities/**`, `Node.Core/Sandboxes/**`, `Runs/**`, `SandboxData/**`, `Updates/**`, `src/ArcForges.RunSupervisor/**`, native `Mxc/**`/`Terminal/**` folders, new Sandbox/Run/Data/CenterControl handlers, new Data/Sandbox/Update CLI files, new focused tests and V2 docs |
| Cloud | `center/internal/management/**`, `center/internal/commerce/**`, V2 migration assets, operation/self-host/acceptance docs, new self-host content beneath existing deploy root |
| Contracts | `eng/v2-consumers/**`; new public Sandbox/management protos and internal channel versions live beneath the real roots |
| Web | New self-host and UX acceptance docs beneath their declared paths |
| ArcForges-Design | V2 research/reuse/data/architecture artifacts exist in the candidate worktree rather than pinned historical main |

A broad existing test project path allows new focused tests within the real project. A `tests/**/Terminal*`-style supplementary pattern is not evidence that a dedicated test project already exists.

## Task coverage

The count of future/new patterns below includes new documentation and test names as well as code. The current graph contains the exact applied arrays and explicit future-path notes.

| Task | Recommended repositories | Planned/new unmatched patterns |
|---|---|---:|
| `AFV2-BASE-01` | ArcForges (2 paths), Cloud (2 paths), Contracts (1 paths), ArcForges-Design (3 paths) | 7 |
| `AFV2-BASE-02` | ArcForges (15 paths) | 0 |
| `AFV2-MXC-01` | ArcForges (6 paths), ArcForges-Design (2 paths) | 4 |
| `AFV2-MXC-02` | ArcForges (3 paths), ArcForges-Design (2 paths) | 4 |
| `AFV2-MXC-03` | ArcForges (3 paths), ArcForges-Design (2 paths) | 4 |
| `AFV2-MXC-04` | ArcForges (2 paths), ArcForges-Design (3 paths) | 4 |
| `AFV2-API-01` | Contracts (10 paths) | 0 |
| `AFV2-DATA-01` | ArcForges (3 paths) | 1 |
| `AFV2-CORE-01` | ArcForges (10 paths) | 4 |
| `AFV2-CORE-02` | ArcForges (20 paths) | 6 |
| `AFV2-CORE-03` | ArcForges (14 paths) | 6 |
| `AFV2-SEC-01` | ArcForges (13 paths) | 1 |
| `AFV2-RES-01` | ArcForges (11 paths) | 0 |
| `AFV2-RES-02` | ArcForges (16 paths) | 1 |
| `AFV2-RES-03` | ArcForges (8 paths) | 2 |
| `AFV2-REC-01` | ArcForges (16 paths) | 5 |
| `AFV2-CLI-01` | ArcForges (6 paths) | 1 |
| `AFV2-CLI-02` | ArcForges (8 paths) | 3 |
| `AFV2-FILE-01` | ArcForges (16 paths) | 5 |
| `AFV2-FILE-02` | ArcForges (17 paths) | 6 |
| `AFV2-CENTER-01` | Cloud (15 paths) | 2 |
| `AFV2-ID-01` | Cloud (17 paths) | 0 |
| `AFV2-CENTER-02` | Cloud (22 paths), ArcForges (15 paths) | 3 |
| `AFV2-CENTER-03` | Cloud (16 paths), ArcForges (10 paths) | 2 |
| `AFV2-CENTER-04` | Cloud (15 paths), ArcForges (11 paths) | 4 |
| `AFV2-HOST-01` | Cloud (12 paths) | 1 |
| `AFV2-HOST-02` | Cloud (17 paths) | 1 |
| `AFV2-HOST-03` | Cloud (18 paths), Web (8 paths) | 2 |
| `AFV2-WEB-01` | Web (13 paths) | 0 |
| `AFV2-WEB-02` | Web (3 paths) | 0 |
| `AFV2-WEB-03` | Web (3 paths) | 0 |
| `AFV2-WEB-04` | Web (4 paths) | 1 |
| `AFV2-MIG-01` | ArcForges (16 paths), Cloud (56 paths), Contracts (8 paths) | 1 |
| `AFV2-MIG-02` | ArcForges (3 paths), Cloud (7 paths), Contracts (1 paths), ArcForges-Design (2 paths) | 5 |
| `AFV2-DIST-01` | ArcForges (10 paths), Cloud (8 paths), Web (7 paths) | 3 |
| `AFV2-DIST-02` | ArcForges (16 paths), Cloud (8 paths) | 4 |
| `AFV2-ACC-01` | ArcForges (4 paths), ArcForges-Design (1 paths) | 1 |
| `AFV2-ACC-02` | Cloud (4 paths), Web (3 paths), ArcForges (4 paths), ArcForges-Design (1 paths) | 3 |
| `AFV2-PROD-01` | Cloud (4 paths), Web (6 paths), ArcForges (5 paths) | 2 |

## Validation boundary

This is a pinned source/layout and composition review. Every proposed source pattern was checked for an existing match; unmatched patterns were classified explicitly. No source or database migration was executed, no product tests/native host profiles were claimed, and no shared graph/document/product file was changed by this subagent.

## Final applied-scope delta check

After the parent applied the recommendations, all 39 current task/repository arrays exactly matched the audited map. No unmatched path was left without a planned/candidate classification, and all five checked local main refs still matched the pinned commits above. The normalized task/repository scope map SHA-256 was `6b9a3bf0860f0fa14cb95251a9a99264be303131c8506145757e6e92d2562bcc`. DataService.InspectTransfer fits the declared FILE01 DataServiceHandler/SandboxData/Client integration scope. This follow-up remained read-only for all shared repositories.
