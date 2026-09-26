# Platform Projects and Application Assistants

Authority: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012). This is the concrete project, package, composition and lifetime contract. Native function/layout authority remains [annex 06](contracts/06-native-functional-abi.md); product semantics remain [profiles 26](26-product-behavior-profiles.md). [Assistant UX](../experience/01-embedded-assistant.md) defines presentation and [history storage](data-model/05-application-history.md) defines persistence.

## 1. Repository and runtime ownership

Nine independently built repositories are current: DesktopPlatform, Contracts, ArcNotes, ArcScope, ArcSlate, Cloud, AI, Web and Mobile. ArcChat is the historical name for the assistant feature family; it is no longer a required repository, executable, application runtime or dependency. Its accepted chat/task/project/skill/automation features are implemented by the Platform assistant packages and the Web/Android companions. Existing `CH-*`, `CO-*`, [`WP-15`](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15) and [`WP-17`](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17) identifiers retain their feature meaning.

Each professional desktop is independently installable. Its UI composes its own domain/application/infrastructure libraries and the packages below. Platform supplies complete reusable assistant functionality, storage and communication, but does not own Notes block rules, Scope acquisition/measurement or Slate timeline/render rules. No product references another product repository. Cloud consumes Contracts, not DesktopPlatform UI/native assemblies. Android implements its own Kotlin presentation/storage over published Contracts. Web consumes npm artifacts. No source-sharing folder, submodule, adjacent project reference or all-capabilities metapackage is allowed.

## 2. DesktopPlatform tree and actual projects

```text
DesktopPlatform/
  DesktopPlatform.slnx                 # managed library + verification projects
  native-ide/win.slnx                  # generated local native IDE view, not authority
  global.json  Directory.Build.props  Directory.Packages.props
  NuGet.config  .editorconfig  .gitattributes  .gitignore
  .github/workflows/                   # verify -> build -> pack -> publish
  .github/dependabot.yml  .githooks/    # shared policy, no secret-dependent hook
  SECURITY.md  LICENSE  NOTICE  README.md
  native/                             # CMake, headers, implementation, vcpkg pins/overlays
  src/BuildingBlocks/                 # projects in the mechanism table below
  src/Communication/                  # Cloud.Client and Device.Runtime
  src/Assistant/                      # Abstractions, Core, Persistence.Sqlite, Cloud, Avalonia
  src/Native/                         # managed ABI wrappers only
  src/DesktopHelpers/                 # ContentSandbox executable and broker facades
  eng/                                # reproducible build/pack/ABI/license/consumer scripts
  tests/{Unit,Contracts,Integration,Native,Consumers}/
  samples/AssistantHost/               # first-party minimal test consumer, never a product
  artifacts/                          # ignored candidates/evidence; no checked-in binaries
```

Every row is a project named exactly as its package unless noted. `src/<group>/<project>/<project>.csproj`; no project is created solely to hold an empty placeholder. Keep the existing SQLite project identity; do not publish a second synonym `ArcForges.Persistence`.

| Group / project | Owns and exposes | Allowed direct dependencies | Producer |
|---|---|---|---|
| BuildingBlocks/ArcForges.Foundation | IDs, exact-value adapters, clock/errors/version primitives | Contracts.Foundation | WP04 |
| BuildingBlocks/ArcForges.Application.Abstractions | cancellation, typed operation results, lifecycle ports | Foundation | WP04 |
| BuildingBlocks/ArcForges.Persistence.Sqlite | connection factory, serialized writes, migration/journal/resource-store mechanics; parameterized SQL only | Foundation, Microsoft.Data.Sqlite | WP07 |
| BuildingBlocks/ArcForges.LocalRpc | parent/helper authenticated Named Pipe/UDS transport and bounded protobuf calls | Foundation, Contracts.LocalRpc.Platform/Sandbox | WP08 |
| BuildingBlocks/ArcForges.Capabilities | own-application descriptors, typed registration, frozen context and availability | Foundation, Contracts public/product descriptors | WP09 |
| BuildingBlocks/ArcForges.Security | actor chain, approvals, OS secret access and egress evaluation | Foundation, Application.Abstractions | WP11 |
| BuildingBlocks/ArcForges.Observability | consent-aware/redacted logs, Activity/Meter and support bundles | Foundation | WP12 |
| BuildingBlocks/ArcForges.Execution | local ProductJob journal, cancellation/checkpoint/effect certainty | Foundation, Persistence.Sqlite, Security | WP16 |
| BuildingBlocks/ArcForges.DesignSystem | semantic tokens, shared controls, accessibility/localization | Foundation, Avalonia | WP10 |
| BuildingBlocks/ArcForges.Desktop.Shell | windows/docks, commands, settings, attention and navigation | DesignSystem, Application.Abstractions, Capabilities | WP10 |
| BuildingBlocks/ArcForges.Update | signed feed/download/stage/apply/rollback lifecycle | Foundation, Security, Persistence.Sqlite, Observability | WP53 |
| Communication/ArcForges.Cloud.Client | authenticated gRPC-Web channel/session lifecycle, typed SDK facade, events, upload/download resume, per-scope cache/cursor invalidation | Foundation, Security, Contracts.PublicApi/Events, generated HTTP exceptions | WP06 minimal, WP23/24 complete; WP25 transfer |
| Communication/ArcForges.Device.Runtime | own-app registration/presence, pull/claim/result, local reauthorization and typed device tool dispatch | Cloud.Client, Capabilities, Security, Execution | WP17 fixture boundary; WP26 real |
| Assistant/ArcForges.Assistant.Abstractions | public typed host/store/cloud ports and composition identities; no UI/store implementation | Foundation, Application.Abstractions | WP14 |
| Assistant/ArcForges.Assistant.Core | conversation/branch/project/profile/skill services, immutable turns, drafts, search/export orchestration, typed host/store/cloud ports | Assistant.Abstractions, Foundation, Capabilities | WP15 |
| Assistant/ArcForges.Assistant.Persistence.Sqlite | full app-assistant schema, repositories, local search, migration, pending commits and history promotion journal | Assistant.Core, Persistence.Sqlite | WP15 |
| Assistant/ArcForges.Assistant.Cloud | run/turn/task/approval/automation orchestration; history sync, transient output recovery, budget/admission UI state | Assistant.Core, Cloud.Client, Device.Runtime | WP17; real WP26/52 acceptance |
| Assistant/ArcForges.Assistant.Avalonia | complete docked/floating/expanded view, presentation models, host composition entry point | Assistant.Core, Assistant.Cloud, Assistant.Persistence.Sqlite, Desktop.Shell | WP17 |
| Native/ArcForges.Native.Abstractions | ABI/status/lifetime and SafeHandle primitives | Foundation | WP13 |
| Native/ArcForges.Native.{Media,Colour,Image,Otio,Instruments,Pdf,Graphics} | typed wrappers over the complete functional annex 06 exports | Native.Abstractions; Media also Foundation | WP13 |
| DesktopHelpers/ArcForges.ContentSandbox.Contracts | facade over generated sandbox wire types, no duplicate proto | Contracts.LocalRpc.Sandbox, Foundation | WP11 |
| DesktopHelpers/ArcForges.ContentSandbox.Broker | restricted launch and brokered resources/buffers | ContentSandbox.Contracts, LocalRpc, Security | WP11 |
| DesktopHelpers/ArcForges.ContentSandbox | signed Native AOT executable, packaged as Runtime.<rid> | broker protocol and only admitted parser wrappers | WP11 hostile fixture; WP13 production composition |
| eng/ArcForges.Build.Policy | build-only NuGet rules | no runtime dependencies | WP02 |

The seven native families publish `Runtime.<rid>` packages only for RIDs actually produced under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017), with exact compatible managed/runtime versions and the complete native dependency/NOTICE closure for each produced RID. macOS source support does not imply an automated macOS package or tested release. NuGet consumers select the needed family and RID explicitly; they never build CMake. The helper has its own signed runtime family. Assistant consumers do not transitively download FFmpeg, Instruments or OTIO: attachment parsing requests the host's admitted sandbox capability and unsupported previews have a visible fallback. Existing first-party licensing boundaries apply: public Contracts/Foundation/SDK Apache, desktop implementation and assistant UI in the existing DesktopPlatform implementation boundary; no Android import of those implementations.

## 3. Host integration contract

The public entry point is `AssistantHost.Create(AssistantHostOptions, AssistantHostServices) -> IAssistantSession`. `AssistantHostOptions` fixes `ProductId`, immutable `InstallationId`, display name/icon, platform data root, initial profile partition, and available presentation modes. Product IDs are `arcnotes`, `arcscope`, `arcslate`; companion origin is `companion`. User-visible names may be localized; IDs never are. Options cannot select another product's directory. Composition is explicit/AOT-safe, without scanning assemblies.

| Host port | Required calls / values | Ownership and refusal |
|---|---|---|
| `IHostContext` | `DescribeSelection()` returns typed resources/revisions/counts and labels; `Freeze(selectionIds, budget)` returns immutable authorized context or typed partial/refusal | Product selection changes never change a submitted turn. No automatic entire document/media/capture upload. |
| `IHostActions` | registers each generated operation descriptor with its specific typed request/result delegate; `GetAvailability(operationId, context)` | Only this product's allowlist. No arbitrary reflection, universal domain Invoke or another app's descriptor. |
| `IHostResources` | `Resolve(ResourceVersionRef)`, `OpenRead(grant, range)`, `Present(ref, previewMode)`, `SaveAs(ref, destination)` | Product/Cloud owner rechecks authority; paths remain private; read permission does not imply export. |
| `IHostNavigation` | `OpenOwnedResource(ref, anchor)`, `RequestPanel(presentation)`, `ShowAttention(attentionId)` | Only own-app routes; missing resources yield unavailable reasons. Cross-product handoff is future. |
| `IHostLifecycle` | `GetBusyState()`, `PrepareShutdown()`, `OnProfileChanging()`, `OnResumed()` | Shutdown summarizes running local jobs/remote tools; local work is checkpointed or explicitly refused. |
| `IHostPlatformServices` | clock, dispatcher, OS secure storage, file-picker grants, clipboard, locale/theme/accessibility, diagnostics consent | Testable bounded abstractions; no global service locator. |

`IAssistantSession` exposes `OpenSurface(mode, windowId, conversationId?)`, `CreateConversation(historyMode)`, `OpenConversation(id)`, `AttachContext(refs)`, `ObserveAttention()`, `SwitchProfile(profile)`, `PrepareShutdown()` and async disposal. All mutations use Core services and typed results; UI receives no SQL connection, raw auth token or unmanaged pointer. `AssistantHost.Create` rejects an already-open foreign partition; two windows of the same application reuse one session/store writer, with separate draft IDs. A product can customize title/icon/theme and context/action contribution, not fork storage/protocol logic or silently suppress mandatory consent/error UI.

Scope disposal cancels view subscriptions and current network calls, flushes acknowledged local commits, locks credentials, and releases native/broker resources. Closing one window does not terminate a Cloud task. Quitting the application makes its device tools unavailable; Cloud-only work can continue. User stop is an explicit command with idempotency/effect semantics, not a side effect of window disposal.

## 4. Product repository trees

Each product has `<Product>.slnx`, the common root policy/build files, `src/<Product>.Domain`, `.Application`, `.Infrastructure`, `.Desktop`, `.AssistantIntegration`, and `tests/{Domain,Application,Integration,Acceptance}`. Domain owns canonical rules; Application owns use cases/ports; Infrastructure owns product SQLite/resource/native adapters; AssistantIntegration registers typed host actions/context; Desktop is UI/composition. References: Desktop → Application/Infrastructure/AssistantIntegration/packages; AssistantIntegration → Application + platform assistant ports; Infrastructure → Application/Domain + selected platform packages; Domain → admitted Foundation only. Infrastructure migration schemas never move into UI code.

| Product | Required owned services in Application/Infrastructure | Platform native selection |
|---|---|---|
| ArcNotes | block/document command handlers, scalar evaluator, notebook sync/pending-edit lineage, search, import/export, PDF attachment adapter | Pdf; Image only for admitted image preview; sandbox required |
| ArcScope | serial/USB/TCP/UDP input, decoder/acquisition pipeline, capture store, exact measurement/report and simulator ingestion | Instruments, Graphics as required by selected renderer; no Media merely for assistant |
| ArcSlate | asset/relink, timeline/edit/undo, playback clock/processing, render snapshot/export and OTIO adapters | Media, Colour, Image, Graphics, Otio; sandbox for untrusted parsing |

Same-product device requests invoke these Application handlers in process, using the same validation, permission, revision and write path as direct UI actions. A target session never opens a product-to-product local socket.

## 5. Other repository directory plan

| Repository | Concrete layout and responsibilities |
|---|---|
| Contracts | `public/proto/arcforges/<domain>/v1`; `internal/proto` for helpers/product ports/operator; `internal/ai-http/v1`; `public/http/v1`; existing `src/public/dotnet` and `src/internal/dotnet` C# owners, `src/public/ts/{proto,api-client,contract-fixtures}`, `src/internal/ts/{ai-internal,operator-client}`, `src/public/kotlin/{contracts-proto,contracts-connect-client,contract-fixtures}`; generation/compatibility scripts and explicitly local consumer diagnostics. Generated source stays in its owning package, committed, reproducibly regenerated and diff-checked; schemas are handwritten only here. Native-grpc-only contracts-client is retired at the first business release. Preserve the existing `ArcForges.Contracts.slnx` identity for C# producers/tests. |
| Cloud | `Cloud.slnx`; `src/Cloud.Host`, `src/Modules/<Name>/<Name>.{Domain,Application,Infrastructure} (all 21 owners, including PackageCatalog)`, `src/Cloud.Storage.D1`, `src/Cloud.Integrations`; `worker/src/{routing,container,bindings,events,jobs}`; `storage/{migrations,plans}`; `deploy` manifests; `tests/{Module,Sql,Bindings,Integration,Recovery}`. Worker executes fixed storage plans; C# owns decisions. |
| AI | `src/{workflows,models,context,streams,objects,ports}`, generated internal contract dependency, Wrangler bindings and exact Workflow/model versions; one Harness only. |
| Web | existing independent `site`, `account`, `chat`, `operations` build profiles over shared TS UI/auth/client libraries; no .NET desktop assembly import or server-side production Node requirement. |
| Mobile | Gradle root/versions/locks plus `app`, `core/{model,contracts,network,database,security,designsystem,testing}`, `feature/{auth,home,chat,tasks,library,devices,settings}`. Features depend core interfaces; app composes them. Room data stays private per profile; generated Maven client is a pinned dependency. No iOS tree/build deliverable. |

## 6. Producer and consumer completion

Each package publishes an immutable candidate only after its applicable owned checks. A clean package-only consumer diagnostic uses exact versions, compiles AOT where relevant and invokes the affected public surface locally only when the existing environment supports it and the change requires it, under P2-017 below. AssistantHost sample demonstrates two separate product identities with separate roots/connections and multiple windows within one application. It is a test executable, not ArcChat reborn. At WP17, Cloud AI/remote behavior is a named fixture; WP26/52 replace it with actual Cloud/CF and WP31/49 verify Android/Web. UI acceptance remains open until real services replace those fixtures.

Under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017), producer CI is necessary static/targeted offline checks → Windows/Linux compilation and applicable AOT compilation → pack once → required licence/provenance/signing and candidate identity checks → publish those bytes after main integration. No macOS, installed-package consumer execution, GUI/browser/device, live-service or real-inference CI is retained. Relevant runtime and consumer diagnostics are local only when supported by the existing environment and required by the change; their evidence and untested coverage remain distinct from compilation. Existing package versions are never overwritten; adding behavior requires a new version and proportionate compatibility evidence. CodeQL scope follows selected supported languages without duplicating security scans; local native diagnostics follow the same policy.

## 7. Observed bootstrap versions and transition

Read-only repository baselines dated 2026-09-16 are Contracts d77aefa, Cloud 6554400 and Mobile 15145a4. Their exact observed Hello World pins remain source evidence; Design does not maintain a competing patch-version list. WP01 reconciles actual roots and WP02/03 record coherent committed toolchain/generator manifests and locks; WP30 F-1 replaces any preview Android stack with a compatible stable stack before production. No family-wide SDK or product version lockstep is implied.

Exact toolchain patch pins are owned by each producer repository's committed manifests/locks and immutable build provenance. Design selects tool families and required compatibility, not duplicate patch-version inventories. Android source/application identity is com.arcforges.mobile; four Web outputs are site/account/chat/operations. PackageCatalog is a Cloud module with WP41 producer and WP45 review console.
