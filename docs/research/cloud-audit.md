# Cloud, Web and Contracts audit for ArcForges V2

Audit date: 2026-11-14. Status: source audit and V2 disposition, not product implementation or deployment acceptance. This report supports [Go Center](../architecture/09-go-center.md), [Blazor Dashboard](../architecture/10-blazor-dashboard.md), [identity and commerce](../architecture/11-identity-commerce.md) and [PostgreSQL transition](../data/cloud-store.md).

## 1. Conclusion and evidence boundary

The Go Center contains reusable identity, sessions, Node enrollment, PostgreSQL persistence, account/operator authorization, entitlement resolution and a bounded authenticated outbound Node channel. These are implemented packages with meaningful integration tests, not empty architectural boxes. The old routed business operations are Task/Fleet/file/workspace operations; none is a delivered V2 Sandbox/Run management API. Keep the underlying guarantees, replace the active business route catalogue and remove cancelled product composition after a finite migration. [C-server] [C-routes] [C-access] [C-hub] [C-fleet]

The Web repository contains a working Blazor WebAssembly/build/transport foundation, a session-probe Account page, a Hello-probe Chat page and an Operations skeleton. It does not contain the requested device, Sandbox, resource, Run, security or subscription Dashboard. Keep the framework, strict browser session client and delivery tooling; implement the product pages. The C# Commerce module is only a boundary declaration, and the current Go Center has no commerce package. The entitlement resolver is real; subscription checkout/webhooks/provider reconciliation remain new work. [W-app] [W-account] [W-chat] [W-operations] [W-session] [C-commerce] [C-entitlement]

Two constraints determine the transition. First, an existing schema-10 database cannot simply run the present migration 0011: its current security bridge is deliberately unbound. Second, many independent repositories still consume published Contracts cohorts, including retired output families. Removing old APIs from the ArcForges V2 composition does not authorize editing, deleting, unpublishing or registry-deprecating those artifacts. [C-bridge] [C-migrate] [K-policy] [K-packages]

### Audited immutable revisions

The parent audit verified these repository `main` revisions against GitHub before analysis. Source links in this report use immutable commits. No product repository was changed by this audit.

| Repository | Commit | Role in this audit |
|---|---|---|
| Cloud | `6df33c525fcbc20495e46c9c4c011086146da796` | Go Center, legacy C# modules, database/migration/deployment composition |
| Web | `56bb40fe7d1693013b4b1e2a82f1b796a65629c5` | Blazor/static shells, browser transport and build infrastructure |
| Contracts | `de3dba76266e89654be9b4d29d097d525a281c6a` | Public/internal schemas, package ownership, immutable output policy |
| ArcForges | `10f692224f94916cfc93fbad971f80ec340c5edf` | Current Node/CLI consumer and old remote business API boundary |
| DesktopPlatform | `e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6` | Shared package consumer; independent ContentSandbox distinction |
| Mobile | `072ee675e8ea67e779922082dbf65dbc02ed6916` | Cancelled ArcForges V2 client; published API consumer |
| AI | `70f8b22d56d67abd2a983f8b448846731ee22902` | Independent old npm contract consumer |
| ArcScope | `485c8d6d9a84825eb5bc737c9808b8bc4b616643` | Independent application/API consumer |
| ArcSlate | `569785a050c97a8022fe264f6af986285766bf87` | Independent application/API consumer |
| ArcNotes | `2839da696cf3d6cc8ab3c241212eea8403c5a0a1` | Independent application/API consumer |
| ArcForges-Design | `62172622550fff73a553135ca178f9b7117c9cbd` | Prior target design, frozen as history in this V2 transition |
| Plan | `742ed2660c5e934e1df86f90e54198b3a199e2b1` | Historical delivery/evidence ledger, not proof of new V2 work |

### What evidence labels mean

| Label | Meaning |
|---|---|
| Implemented; source inspected | Concrete code paths and state/transaction/authorization behavior were read. This report does not claim that they were run in this audit. |
| Tests present | Relevant tests exist in the pinned source. Historical ledger acceptance is identified separately. No new test pass is inferred from a filename or a green historical task. |
| Contract/interface only | A generated API, module boundary or target design exists without the corresponding admitted runtime behavior. |
| Missing V2 | The proposed V2 operation/page/state machine is not implemented at the audited baseline. |
| Historical delivery | The frozen Plan records the stated delivery, with its original limitations. It does not establish current hosted activation or an unperformed external proof. |

This audit performed repository reads, package/consumer inspection and cross-document design checks. It did not execute native Windows/Linux host acceptance, a PostgreSQL migration, a browser E2E journey, a provider transaction, or a production deployment. Those gates remain named implementation/hosting tasks. No secret values were needed.

## 2. Disposition vocabulary

`KEEP` retains an asset's useful responsibility and guarantees; it does not assert every line can remain unchanged. `REWORK` retains a foundation but changes its domain, interface, composition or incomplete behavior. `REPLACE_WITH_MXC` applies to isolation/runtime responsibilities moved to the pinned upstream backend; Cloud/Web must consume its truthful capabilities rather than implement a replacement sandbox. `REMOVE` removes an obsolete ArcForges V2 runtime dependency or delivery item after consumer/migration checks. `FUTURE` identifies a possible extension with no prerequisite, implementation task or promise in this V2 plan.

In every `REMOVE` row, immutable package versions, committed migration checksums and historical delivery receipts stay preserved. Removing an ArcForges product dependency does not delete an independent product repository.

## 3. Go Center asset disposition

| ID | Existing asset and actual state | Disposition | V2 action and boundary | Evidence |
|---|---|---|---|---|
| C01 | Go `Center` composition, public/admin listeners, explicit surface admission; implemented | KEEP | One Go business server for official/self-hosted deployment; Sandbox Core stays on Node | [C-server] |
| C02 | Worker/Container ingress and generated Go route/budget table; implemented infrastructure | REWORK | Publish V2 fixed typed routes/budgets; keep transport/provenance controls; no Worker business retries or entitlement decisions | [C-routes] [C-server] |
| C03 | Required `official-hosted` or `self-hosted` mode; configured public base URL; implemented | KEEP | Self-host has no official URL, account or subscription dependency; reject missing/invalid mode | [C-config] |
| C04 | Passkey/email-code sign-in, bootstrap, enrollment, profile, step-up and credential management; implemented | KEEP | Preserve one-use proofs, account/device boundaries, transaction limits and rate controls | [C-identity] [C-identity-routes] |
| C05 | Recovery, account deletion/export and email-change public declarations; explicitly unregistered | REWORK | Complete minimal recovery/deletion/export lifecycle in `AFV2-ID-01` (`R-CTR-004`); expose only supported actions; do not call the entire public IdentityService implemented | [C-identity-routes] |
| C06 | Browser cookie and native token sessions, refresh reuse detection, device/install joins and revocation; implemented | KEEP | Reuse strict exact-origin/CSRF browser handling and separate Node credentials; all remote readers respond to revocation | [C-session] [C-pages] |
| C07 | Center-owned account/passkey/session/device/sign-in pages; implemented | KEEP | Preserve headless/self-host enrollment and security remediation while Blazor consumes the same identity core | [C-pages] [C-pages-routes] |
| C08 | Node loopback/PKCE and device-code enrollment, installation key proof, registry/names; implemented | REWORK | Keep identity and proof semantics; add V2 protocol epoch/capabilities and replace Fleet business vocabulary | [C-fleet] [C-fleet-api] |
| C09 | Account ownership and operator-role checks; typed operation table with scope/step-up/resource/audit/gate order; implemented | REWORK | Initial V2 is account ownership plus local grants; fixed per-method authorization; no implicit operator access to user execution/output | [C-access] |
| C10 | Local Sandbox/provision remote grants | REWORK | Missing V2 behavior: local default-off grants, exact Center/enrollment binding, bounded provisioning template, immediate revoke; Center cannot mint or widen them | [C-access] [C-fleet-api] |
| C11 | One outbound authenticated Node WebSocket, challenge/signature proof, heartbeat/session recheck, connection replacement; implemented | REWORK | Reuse transport guarantees with a separate V2 protocol/signature domain and truthful capabilities; no old Task enums reinterpreted | [C-hub] [C-hub-upgrade] |
| C12 | Singleton PostgreSQL hub lease with fencing, renew/expiry and channel closure; implemented | KEEP | One active channel owner per database initially; qualify capacity and failover; no unplanned distributed hub redesign | [C-hub-lease] |
| C13 | Bounded queue/frame/rate/in-flight handling and signing-key freshness; implemented | KEEP | Preserve bounds, cancellation and fail-closed stale-key behavior; negotiate release limits as operational caps | [C-hub-calls] [C-hub-keyring] |
| C14 | Signed typed relay request/result digest binding and exact result-byte forwarding; implemented | REWORK | Reuse integrity and payload-minimization rules for explicit `sandbox.v2` methods; exclude remote terminal input/attach | [C-hub-sign] [C-hub-calls] |
| C15 | Durable content-free routed receipts, delivered/abandoned race handling and conservative unknown settlement; implemented | REWORK | Stable command ID/intent hash, Node outcome query and tombstones; no automatic new-command retry | [C-fleet-routed] [C-hub-calls] |
| C16 | Submit/Get/List/Wait/Cancel/ReadOutput NodeTask remote routes; implemented old domain | REMOVE | Remove from final V2 composition after receipt/identity migration; use Sandbox/Run services without Task/Attempt/DAG adapter | [C-fleet-routed] [C-fleet-api-routed] |
| C17 | Routed file edit/search/cleanup/workspace operations and CTR06 target receipts; implemented old domain | REMOVE | Replace active surface with bounded Sandbox-relative regular-file manifests/chunks; preserve old receipts/tombstones, not the old editor/cleanup runtime | [C-fleet-files] [C-fleet-api-files] |
| C18 | Legacy relay caller/Agent/Human product seams | REMOVE | Keep necessary cryptographic origin/credential distinction; remove AI-agent orchestration and plugin-facing product semantics | [C-hub-sign] [C-access] |
| C19 | Native mobile authorization and mobile approval pages; implemented | REMOVE | Cancel ArcForges mobile product routes and new delivery; keep generic CLI device-code enrollment and old public artifact availability | [C-mobile] [C-mobile-routes] |
| C20 | Deterministic Go entitlement resolver, snapshots, revisions, grants/revocations/terms and C# parity fixtures; implemented | KEEP | Retain historical facts and needed hosted-service resolution; no entitlement in local execution path | [C-entitlement] [C-entitlement-parity] |
| C21 | Six old feature keys and task/MCP/push operation groups; implemented | REWORK | Active V2 keys `center.nodes`, `remote.view`, `remote.control`; preserve old historical meanings; self-host ignores official paid entitlements | [C-feature] [C-feature-gate] |
| C22 | Operator grants/configuration/release definitions and essential ungated security routes; implemented | REWORK | Keep small hosted operating controls and audit; no full enterprise RBAC/policy product | [C-entitlement-operator] [C-access] |
| C23 | C# `CommerceModule` boundary; no Go commerce adapter | REWORK | Implement minimal web provider checkout/events/subscriptions/reconciliation and billing UI; do not infer provider behavior from the module name | [C-commerce] [C-internal] |
| C24 | C# Center host/D1 and broad old module composition | REMOVE | Retain useful algorithms/fixtures/schema evidence as needed; remove executable alternative host after qualified data/consumer cutover | [C-src] [C-entitlement-parity] |
| C25 | PostgreSQL store, audit/outbox/command primitives, least-privilege table catalogue | KEEP | PostgreSQL remains Center system of record; no SQLite substitution for acceptance | [C-schema] [C-migrate] [C-store] |
| C26 | Immutable 0001–0011 migrations and CTR06 runtime/restore admission guards | REWORK | Preserve history/checksums and security proof; qualify fresh/schema10/schema11 V2 transition; remove finite transition runtime after cutover | [C-migrations] [C-bridge] [C-restore] |
| C27 | Restore/backup/legacy-writer isolation code; implemented with specialized proof requirements | REWORK | Retain proof obligations and compatible tooling; replace obsolete artifact binding through a reviewed V2 successor, never a force flag | [C-bridge] [C-restore] [C-prepare] |
| C28 | V2 Sandbox/Run/resource/log live telemetry | REWORK | Missing product behavior: bounded on-demand reads, epochs/cursors/staleness/gaps, grant recheck, no authoritative Center Run machine | [C-routes] [C-fleet-api-routed] |
| C29 | Isolation responsibility behind the existing Node/Fleet API; Node-owned rather than Go execution | REPLACE_WITH_MXC | Node profiles use pinned MXC plus necessary local OS supervision; Center consumes truthful capability status and does not grow an isolation engine | [MXC integration](../architecture/02-mxc-integration.md) [C-fleet-api-routed] |
| C30 | Old MCP/stdio/AI execution delivery items | REMOVE | Cancel their active Plan continuation; no MCP facade or AI configuration enters V2 | [P-graph] |
| C31 | Organization sharing/custom roles, distributed hub, plugin marketplace | FUTURE | No implementation or dependency in the current V2 plan; later proposals must preserve local authority | [../architecture/09-go-center.md](../architecture/09-go-center.md) |

### Concrete reuse decisions

The current mode gate already supports the required business separation. Self-hosted availability is calculated from configured feature keys and explicit operator disables, without consulting official account entitlements. Official mode requires a valid catalog and an account snapshot. An entitlement-store read error is different from an expired subscription. Reworking the active key set is safer and smaller than creating a second self-host binary or adding a Node license check. Current settings bound connections, frames, calls and database pools; those technical bounds must not be advertised as commercial quotas. [C-feature] [C-feature-gate] [C-config]

The channel is also more than a WebSocket placeholder. It proves a Node installation key, replaces old connections, rechecks session validity, closes on lapse/revoke, signs routed traffic and retains a fenced singleton lease. The current route is `/fleet/v1/node` and the protocol is `arcforges.relay.v1`; V2 needs a separately versioned handshake and domains. Preserving a byte-compatible channel name while changing the meaning of its routed enums would erase the boundary the existing code enforces. [C-hub] [C-hub-upgrade] [C-hub-sign] [C-hub-lease]

The existing receipt code already treats uncertain delivery conservatively. The reusable part is admission-before-send, immutable command intent, monotonic evidence of delivery, verified final response and explicit unknown outcome. The obsolete part is the Task/file result vocabulary and method catalogue. A lost reply after Run start must query the original Node command receipt; it must never become automatic task resubmission. [C-fleet-routed] [C-fleet-files] [C-hub-calls]

The current authorization table is account/operator ownership plus specific operation controls, not a fully delivered organizational RBAC service. It checks target ownership before exposing details and provides essential registry/security actions independently of paid remote operation availability. V2 should extend that explicit model with local grants, preserving non-enumerating foreign/revoked/unknown target responses. [C-access]

## 4. Web disposition and missing UI

| ID | Asset and actual state | Disposition | V2 action | Evidence |
|---|---|---|---|---|
| W01 | Blazor WebAssembly App and shared Razor UI library; implemented scaffold | KEEP | Static browser client with Go API; no ASP.NET business server, Blazor Server circuit or BFF duplication | [W-app] [W-ui] |
| W02 | Session bootstrap/logout client: generated strict schema, exact origin, no-store, CSRF, bounds and no automatic redirect following | KEEP | Build all account-aware view state on these guarantees; keep bearer/private credentials out of browser storage and bundles | [W-session] |
| W03 | Account session probe and stable focus/retry/sign-out behavior | REWORK | Real account/security/session views backed only by implemented methods | [W-account] |
| W04 | Chat Hello probe | REMOVE | Remove from V2 navigation/bundle; it is neither delivered chat nor a reason to retain AI product scope | [W-chat] |
| W05 | Operations skeleton | REWORK | Minimal separately authorized service/billing controls as needed; no automatic operator control of user Nodes | [W-operations] |
| W06 | Static Site, build profiles, candidate sealing/budgets/provenance and locked dependency checks | KEEP | Reuse delivery infrastructure and self-host assets; update content/navigation for CLI/Sandbox product | [W-tools] [W-policy] |
| W07 | Overview/devices/Sandbox/Run/resources/data views | REWORK | Missing product screens. Implement typed operations, truthful capability status, conflict/unknown/empty/loading/offline/stale states | [W-pages] [P-graph] |
| W08 | Subscription catalog/checkout/history/provider portal UI | REWORK | Missing behavior; hosted-only paid service, essential security/billing after lapse; self-host no official upsell | [W-pages] [C-commerce] |
| W09 | Responsive visual system/accessibility of new Dashboard | REWORK | Implement light/dark tokens, keyboard/focus/reflow and numerical chart alternatives; verify finished screens before claiming conformance | [../architecture/10-blazor-dashboard.md](../architecture/10-blazor-dashboard.md) |
| W10 | Browser terminal/remote PTY | REMOVE | Outside V2 delivery. Local CLI owns terminal attach/input; Dashboard can start/stop and read bounded logs | [../architecture/10-blazor-dashboard.md](../architecture/10-blazor-dashboard.md) |
| W11 | Plugin/mobile/AI/cache/DAG/toolchain/LAN management screens | REMOVE | Remove cancelled product scope rather than leave inactive navigation promises | [P-graph] |

The complete page-to-API map is in [the Dashboard design](../architecture/10-blazor-dashboard.md). Creation is deliberately bounded: the browser selects a locally issued provisioning grant and immutable template revision, then may only preserve or narrow its configuration. A normal Sandbox grant requires an existing Sandbox ID. Neither paid subscription nor account enrollment grants arbitrary host paths or node-wide execution. Missing provisioning authority is a normal visible state, not a reason to hide an unsafe free-form API.

Resource views distinguish requested limits, OS-effective limits and verified enforcement. Unknown measurements render unavailable; an offline last-running observation renders stale. Run views include `DRAINING` while managed descendants remain after root/executor exit and `RECOVERY_REQUIRED` when Core cannot establish containment/lifetime. A process/executor exit code alone is not proof that the managed group is empty or that the application exit status is known. Terminal attach stays local; ordinary log rendering treats all bytes as untrusted text.

## 5. Contracts and consumer protection

### Contract disposition

| Asset | Actual state | Disposition | Required action |
|---|---|---|---|
| Foundation request/response metadata, errors, command/revision/effect vocabulary | Published and widely consumed | KEEP | Preserve v1 field/enum meanings; `RequestMeta.command_id` and `expected_rev` remain canonical; cross-language digest vectors for V2 |
| Existing Node/Fleet/Relay v1 Task/file schemas | Published; current Node/Center consumes 450.1 cohort | REMOVE from V2 consumption | New `arcforges.sandbox.v2` and `arcforges.management.v2`; no in-place reinterpretation or Task-to-Run compatibility facade |
| Existing PublicApi Identity/Device and strict browser session schema | Published and current Go/Web consumers | REWORK selectively | Reuse registered implemented operations; fill explicit product gaps separately; keep independent consumers' old packages resolvable |
| New Sandbox/Run/Resource/Data/Node services | Missing at baseline; design specification now supplied | REWORK/new implementation | Closed generated typed methods and clients; explicit remote allowlist; local terminal excluded from Center |
| `arcforges.local.sandbox.v1` / `ArcForges.Contracts.LocalRpc.Sandbox` | Independent DesktopPlatform ContentSandbox contract | KEEP | Do not rename/reuse/delete because the new product also uses the word Sandbox |
| Package/access/foundation inventories | Policy-controlled append-only ownership/retirement history | KEEP | Add V2 entries through normal policy; preserve retired rows and retirement receipts |
| Already retired TypeScript/Kotlin/etc. output families | Generated delivery retired; published packages still consumed | KEEP historical artifacts | No resurrection, republish, unpublish, delete or registry deprecation to make V2 clean |
| Plugin abstraction / AI-specific service envelope | Outside new V2 scope | FUTURE / REMOVE dependency | No package dependency or delivery gate in V2; independent products retain current contracts |

The authoritative policy is explicit: already published versions remain immutable and resolvable, including retired families. A source-level/API deprecation notice, removing a consumer reference, retiring a future generator output and deleting a method in a new major namespace are different actions. None licenses modifying or registry-deprecating the published old package. Within a v1 protocol, existing field numbers and enum meanings are never reassigned. [K-policy] [K-packages] [K-access] [K-foundation]

### Observed package consumers

These are exact central version pins at the source revision, not a claim that every file in the package is used. Consumer ownership must be checked before any shared schema/output deletion.

| Repository | Observed package cohort(s) | Impact of V2 | Pinned evidence |
|---|---|---|---|
| ArcForges | Fleet/Foundation/Node/Relay `1.0.0-ci.450.1`; LocalRpc `138.1`; Observability and Security.Secrets `141.1`; Build.Policy `138.1` (same CI version prefix) | Replace CLI/Node old domain references with new cohort; retain required foundation/build/security pieces; no old executable Task service retained indefinitely | [D-node] |
| Cloud Go Center | `github.com/ArcForges/Contracts/go v1.0.0-ci.450.1` | Publish compatible new Go module cohort alongside C# generated contracts; update after contracts accepted | [C-gomod] |
| Cloud legacy C# | PublicApi/CloudInternal `1.0.0-ci.287.1`; Validation `205.1`; Build `94.1` | Remove obsolete host/module consumption after cutover; do not delete corresponding published cohorts | [D-cloud] |
| Web | PublicApi `1.0.0-ci.287.1`; Build `94.1` | Add V2 typed clients and retain required browser/identity schemas; replace probes | [D-web] |
| DesktopPlatform | Foundation `113.1`; LocalRpc.Platform/Sandbox and Sdk.Contracts `216.1`; Events/PublicApi `270.1` in current centralized pins (same CI prefix) | ContentSandbox/platform SDK and realtime consumers remain independent; no blanket shared-contract deletion | [D-desktop] |
| Mobile | PublicApi/Events `1.0.0-ci.324.1`; Validation `205.1` | Cancel ArcForges V2 mobile client work; preserve existing consumer history/packages and generic identity semantics | [D-mobile] |
| AI | `@arcforges/proto 1.0.0-ci.287.1` | Existing consumer of an already retired output family; stop V2 dependency, do not destroy its pin or resurrect generator | [D-ai] |
| ArcScope | PublicApi `36.1`; Foundation and shared abstractions `29.1`; LocalRpc.Scope/Foundation `113.1`; selected assistant/capabilities/persistence `130.1`; Sdk.Contracts `216.1` (same CI prefix) | Separate product remains buildable; scope/source ownership must be checked before shared API changes | [D-scope] |
| ArcSlate | PublicApi `1.0.0-ci.36.1`; Build `20.1` | Independent product; no new V2 implementation task and no deletion of old package availability | [D-slate] |
| ArcNotes | PublicApi `1.0.0-ci.36.1`; Build `20.1` | Independent product; no new V2 implementation task and no deletion of old package availability | [D-notes] |

For the mixed version rows, a suffix such as `216.1` denotes the repository's exact `1.0.0-ci.216.1` pin. No package upgrade was performed in this audit. Package names and concrete project references remain the authority when a future implementation removes a dependency.

Direct source use is narrower than the large public package names imply. ArcScope, ArcSlate and ArcNotes instantiate the generated `HelloServiceClient` in their `CloudHelloClient`; the mobile network client also calls Hello, and AI's `src/hello.ts` imports the generated Hello request/response schemas. These are real dependency edges, not proof that those repositories implemented the old broad Cloud service catalogue. ArcScope additionally uses foundation value/protobuf types in its annotation persistence path. DesktopPlatform's `ContentSandboxContract` explicitly wraps the generated `ContentSandboxService` descriptor and LocalRpc.Sandbox package, making the independent sandbox-name collision concrete. [D-scope-hello] [D-slate-hello] [D-notes-hello] [D-mobile-hello] [D-ai-hello] [D-scope-data] [D-content-sandbox]

### Safe removal sequence

1. Publish a new versioned contract cohort with fixed method ownership and compatibility vectors. Do not modify an existing published package/version or change old v1 semantics.
2. Move ArcForges Node/CLI, Go Center and Web to the V2 methods. Record every current consumer of the old schema/output in the migration task.
3. Stop consuming obsolete old Task/Fleet/MCP/AI/cache/toolchain/worktree APIs in the V2 product. Remove their registrations, runtime dependencies, configuration and executable implementation once the qualified cutover is complete.
4. Preserve old package resolvability and append-only retirement/inventory receipts. Source API removal follows a new major namespace/output decision and must not remove independent product APIs by name association.
5. Keep historical migrations/data identities and non-executable command tombstones needed to reject replay. Do not ship permanent legacy services merely to preserve source history.

## 6. PostgreSQL migration: concrete hard stop and transition

The migration runner embeds the contiguous SQL chain, hashes applied migrations, uses a dedicated locked migration connection and rejects changed/deleted history. The runtime schema catalogue enumerates tables and permissions; the migration role and serving role differ. The new cloud schema must be PostgreSQL and must use the real chain for execution tests. The former Design checker running cloud SQL as SQLite does not prove PostgreSQL compatibility. [C-migrate] [C-schema] [C-grants]

### Current schema facts

| Migration group | Retained facts | V2 treatment |
|---|---|---|
| 0001 platform/audit/signing keys | Command receipts, inbox/outbox, leases, runtime credential, audit events/chain and signing key history | Keep necessary guarantees and least privilege |
| 0002 identity/device/session | Accounts, identities, sessions/spent refresh, flows, device/install, step-up/bootstrap/rate limit | Keep identity; rotate/fence incompatible credentials at protocol cutover |
| 0003 + 0007 entitlement | Revisions, snapshots, grants/revocations/terms/status/definitions/operator facts | Preserve immutable history; append explicit V2 translation facts where required |
| 0004–0006 enrollment/mobile | Node registry/sign-in/device authorization plus separate mobile authorization | Keep generic Node enrollment; retire mobile route/data writes with retention rules |
| 0008–0009 channel/names | Singleton hub lease, presence and names | Keep fenced hub ownership; add V2 protocol epoch |
| 0010 routed calls | Old Task command identity/digest/delivery/outcome receipts | Preserve/tombstone identities; stop Task dispatch |
| 0011 routed files + floor/admission | File command/target receipts and runtime-floor/restore/legacy credential evidence | Preserve checksums/security proof; qualify exact transition; stop old file dispatch |

The specific problem is `RequireCTR06SecurityBridge()`: the present implementation intentionally returns `ErrCTR06SecurityBridgeUnbound`. The phase-one release does not bind an admitted successor security artifact. For existing schema-10 data, 0011 checks retired writer/runtime identity and restore admission; arbitrary public `BridgeProof` input is rejected. Fresh bootstrap is a different, tightly checked path: it requires absence of legacy receipts/lease/runtime history and unsafe other connections/roles, and reserves non-login role identities in the migration transaction. `ctr06_prepare` metadata alone is not a promoted bridge proof. [C-bridge] [C-migrate] [C-prepare]

Consequently, “append 0012 and deploy,” “delete the obsolete 0011,” “rotate one password,” or “pass force/assume-fenced” are not valid V2 strategies. A reviewed V2 transition artifact must replace the obsolete artifact binding while preserving proof that all old writers, sessions and privilege paths are unable to mutate the serving database. It must qualify separate fresh, existing-schema10 and existing-schema11 fixtures and fail closed for unknown/ahead/incomplete state. Backup restore is target-specific; a copied source readiness marker cannot authorize a restored database. [C-bridge] [C-restore]

The concrete sequence and rollback boundaries are normative in [Cloud store](../data/cloud-store.md): inventory exact DB/artifact/credential identities; make and restore-test a qualified backup; fence old writers and sessions; run the reviewed transition and immutable SQL chain; add V2 tables/epochs/identity tombstones; verify least privilege and recovery; activate only the V2 surface; contract obsolete writers/runtime after all readers have moved. Before a V2 effect, rollback uses the qualified isolated backup and compatible artifact. After a V2 effect or payment fact, only a compatible forward/rollback build may serve the expanded schema; otherwise repair forward or reconcile all post-backup outcomes before restore. Never lose a receipt and then replay a Run or charge.

The V2 PostgreSQL design deliberately stores Center-owned identities, remote operation receipts, catalog/provider associations and audit facts. It does not introduce an authoritative Center Run state table or store process output/file payloads. Node Core owns Sandbox/Run/resource/data lifecycle. Channel telemetry is bounded, on-demand and explicitly stale after loss. Cloud receipt states and process states are distinct: the routing integer map is `1 ACCEPTED`, `2 reserved`, `3 SUCCEEDED`, `4 FAILED`, `5 REJECTED`, `6 EXPIRED`, `7 UNKNOWN`, `8 NOT_DELIVERED`; foundation effect values remain `1 DID_NOT_HAPPEN`, `2 HAPPENED`, `3 UNKNOWN`.

## 7. Historical delivery versus current product readiness

The frozen Plan records these distinctions. They are retained as history rather than reused as completed V2 task status. [P-graph] [P-ledger] [P-acceptance]

| Historical item | Recorded delivery/evidence | V2 consequence |
|---|---|---|
| AF-CTR-01 | Contracts baseline delivered through prior cohort | Reuse foundation discipline; publish new namespace rather than mutate old cohort |
| AF-CTR-02 | `delivered`, with H24 Neon history-retention evidence still pending | Infrastructure is real; do not relabel full external acceptance complete |
| AF-CTR-03 | Go identity/session/device and pages accepted within stated native scope | Retain implementation; recovery/deletion gaps remain explicit route exclusions |
| AF-CTR-04 | Enrollment/device auth accepted with listed browser/passkey/mobile evidence limits | Keep generic Node enrollment; remove cancelled mobile product |
| AF-CTR-05 | Node channel/routed-call delivery accepted; historical official dark deployment remained Hello-only | Existing source does not establish a live paid remote-management product |
| AF-CTR-06 | Current normal native scope accepted; immutable Contracts 450.1 and current ArcForges/Cloud sources delivered | External qualification/bootstrap/successor/dark deploy AR26 remained deferred/not proven; schema transition guard cannot be assumed satisfied |
| AF-CTR-07/08 | MCP/stdio planned | Cancel active continuation |
| AF-CTR-09 and later retained-domain tasks | Planned broader Go port and C# retirement | Replace with selective V2 migration/composition tasks, not blanket porting |
| AF-WEB-01/02/03 | Planned product pages | No product Dashboard completion inherited from scaffold/build success |
| AF-CLD-03 | Broader entitlement endpoints/tokens planned | Resolver implementation is reusable; not all advertised endpoint surface exists |
| AF-CLD-07 | Google Play/subscription work planned | Remove mobile purchase scope; minimal web subscription adapter remains new work |

One concrete historical hosted receipt identifies a PostgreSQL-18 schema-10 dark deployment with `surfaces=none` and Hello-only ordinary health on 2026-11-09. That is useful deployment lineage, not evidence that current schema11 or V2 management is publicly activated. Exact source/package/deploy IDs remain in the frozen ledger; the new Plan must retain their limitations rather than compress them into “Cloud done.” [P-graph] [P-ledger]

## 8. Implementation allocation and acceptance

| Task family | Required concrete outcome from this audit |
|---|---|
| `AFV2-API-01` | New versioned generated core/management contract cohort; exact fixed remote allowlist, digest/enum vectors, provisioning grants, operation reconciliation, epochs/cursors, ownership/retirement inventory |
| `AFV2-BASE-01` | Initial actual source/schema/artifact/consumer inventory and read-only preflight; no production migration or runtime deletion |
| `AFV2-CENTER-01` | Guarded PostgreSQL transition, fresh/schema10/schema11/restore fixtures, credential floors, V2 store/receipt grants and preserved migration bytes |
| `AFV2-ID-01` | After CENTER-01, bounded account recovery/deletion/export, proof and revocation races, account-bound temporary export, no local data/process action; owns `R-CTR-004` |
| `AFV2-CENTER-02` | V2 enrollment/Device List/Inspect/Revoke/outbound channel and local-only CenterControl adapter/working CLI after CLI-01; preserve secure credential internals without old Node.v1 dispatch |
| `AFV2-CENTER-03` | Typed Sandbox/Run/Resource control through the same Core; local grants/provision bounds; original Node owner-epoch/idempotency/uncertainty; no generic dispatch |
| `AFV2-CENTER-04` | Bounded status/resource/log/data reads and transfers; epochs/cursors/gaps/backpressure/revoke, no remote terminal |
| `AFV2-WEB-01` | Responsive Blazor shell, account/session and overview/devices using existing strict transport/build assets |
| `AFV2-WEB-02` | Sandbox/Run/resource/data pages, safe creation/deletion/conflict/unknown flow against real Core |
| `AFV2-WEB-03` | Security/account/subscription views against real supported identity/commerce APIs; no Device rename or obsolete probe/account product composition |
| `AFV2-WEB-04` | Complete responsive/accessibility/keyboard/offline/reconnect and uncertain-operation qualification across all finished pages |
| `AFV2-HOST-01` | Official entitlement/mode correctness and real free self-host independence; preserve local execution after lapse |
| `AFV2-HOST-02` | Minimal provider checkout/events/subscription/catalog/reconciliation; real crypto/business/PostgreSQL with explicitly bounded external payment fixtures |
| `AFV2-HOST-03` | Deployment/operations infrastructure, static-origin contract, TLS/bootstrap/backup/restore, guarded tooling, capacity/cost/alerts; no claim that the future Dashboard bundle is complete |
| `AFV2-MIG-01` | Final consumer cutover and actual retired runtime/route/C# host deletion after CLI/file/Center/Web/hosting acceptance; no early Center dependency on this late task |
| `AFV2-MIG-02` | Forward live-schema contraction after consumer cutover, preserved unresolved effects and immutable history |
| `AFV2-DIST-01` | Final coherent native and actual Go/PostgreSQL/Blazor self-host product after WEB-04 transitively through MIG-01; reject probe/placeholder bundles |

Required native acceptance uses actual Go Center + PostgreSQL + real Windows/Linux Nodes. Exercise wrong account/revoked grant, bounded remote provision, unsupported backend combinations, duplicate/different-intent command IDs, crash before/after send, uncertain Run start, query-only reconciliation, lease takeover, session/entitlement expiry, cursor eviction, slow viewer, root exit with descendants, interrupted transfer/deletion and local continuation after network/official service loss. Schema acceptance includes existing schema10/11 and interrupted/restored fixtures, not just a fresh empty database.

Browser acceptance must show successful user journeys plus loading/empty/offline/stale/forbidden/incompatible/conflict/unknown states and keyboard/responsive behavior. Local process isolation/resource containment is not proven by a mocked Web view. Subscription acceptance uses verified provider sandbox behavior where available, duplicate/out-of-order event recovery and stable purchase identities; browser checkout return is never proof of payment. Missing designated-host or production/provider evidence remains `NOT PROVEN` with its task owner. This source audit creates no completed implementation or deployment status.

The repaired Plan explicitly permits only bounded external mail/authenticator-input, payment/deployment transport and component-rendering fixtures in their named tasks. Real proof/signature verification, authorization, account/entitlement state, PostgreSQL transactions and native Node effects are never replaced. Provider sandbox/live merchant/mail/domain qualification stays separate from development evidence. CLI-01 owns complete offline core/admin commands; FILE-01/02 own working data/delete CLI integration, while CENTER-02 owns actual center-control commands and their local adapter. This avoids both fixture-policy deadlocks and prematurely registered command shells.

## 9. Source-scoped implementation and retirement map

The repaired Plan checked all 39 task path allowlists against the immutable source revisions above. Thirty-two needed corrections or missing integration paths. A new V2 target is identified as planned in the task's notes; an existing module is named by its real path. This is a source-scope audit, not an assertion that any V2 implementation exists. Ancillary solution/package/lock changes remain limited to the declared modules.

| Task group | Existing retained/reworked paths and explicit new targets | Required boundary |
|---|---|---|
| `AFV2-BASE-01/02`, `AFV2-MXC-01..04` | Existing `ArcForges/src/ArcForges.Desktop`, `eng/package.ps1`, `eng/publish.ps1`, `eng/verify_linux.py`, `packaging/` and `eng/policy/dependency-admissions.json`; planned `tools/ArcForges.MxcProbe`, `eng/mxc`, `eng/v2-migration` and profile capability modules | No fictional `eng/packaging` or `eng/admission` directory; preserve native verification gates while changing the declared composition. [A-src] [A-eng] [A-packaging] |
| `AFV2-API-01` | Contracts `public/proto`, `internal/proto`, `src`, `go`, `tests`, `fixtures`, `eng` and relevant docs/solution | Add the explicit V2 surfaces and generated cohort through the actual producer. There is no root `proto`/`packages`/buf-config layout to authorize. Existing published schemas and independent API meanings remain immutable. [K-public-proto] [K-internal-proto] [K-generated] [K-tests] [K-fixtures] [K-packages] |
| `AFV2-DATA-01`, `AFV2-CORE-01..03`, `AFV2-SEC-01`, `AFV2-RES-01..03`, `AFV2-REC-01` | Existing `ArcForges.Node.Core`, `Node.Store`, platform OS projects and real Core/store/platform tests; `Node.Api/NodeApiServer.cs`, `NodeHost.cs` and concrete service handlers where required; planned `Sandboxes`, `Runs`, `SandboxData`, `RunSupervisor`, MXC/terminal/capability submodules | Reuse proved resource/IPC/path primitives, register real handlers and composition, and delete the replaced execution domain only at its qualified cutover. `CenterRouting.cs` is in `Node.Core/Security`; existing path guards are in `Node.Core/Platform`. [A-src] [A-tests] |
| `AFV2-CLI-01/02`, `AFV2-FILE-01/02` | Existing `ArcForges.CommandLine`, `ArcForges.Client`, `CliApplication.cs`, `ArcForges.Host/Program.cs` and `tests/ArcForges.Client.Tests`; planned data/delete command files and local terminal module | CLI-01 delivers working offline core/admin commands. FILE-01/02 own their real data/delete command, client and test integration; no nonexistent CommandLine test project or placeholder commands. [A-src] [A-tests] |
| `AFV2-CENTER-01`, `AFV2-ID-01` | Cloud `center/internal/schema`, `store`, `bridgeproof`, `dbtest`, `pgtest`, `identity`, `identityapi`, `pages`, `session`, `device`, `oneuse`, `mail`, `ratelimit`, `access`, `server`, actual route files and generated-table producer | Guarded migration and real lifecycle adapters must change with their SQL/authorization/route integration. No duplicate invented `httpapi` or `identitytests` tree. [C-internal] [C-server] [C-routes] |
| `AFV2-CENTER-02..04` | Cloud `fleet`, `fleetapi`, `hub`, `server`, `routes`, `access`, `ingress`, schema/store/PG fixtures, `workertables`, `center/cmd/center-gen` and `worker/tables/center-tables.generated.ts`; planned `center/internal/management`; Node `CloudLink`, API composition/dispatch, store and real CloudLink/Core/client tests | CENTER-02 owns working local `CenterControlService` plus center CLI commands and protected credential reuse; CENTER-03 owns typed control; CENTER-04 owns bounded observation including `InspectTransfer`. Route adapters, generated transport tables and actual Node wiring are part of each slice. [C-internal] [C-fleet-api] [C-server] [C-worker] [A-src] [A-tests] |
| `AFV2-HOST-01..03` | Cloud feature/entitlement/config/server/access/store modules; planned `center/internal/commerce`; actual `tooling`, `worker`, `Dockerfile`, `wrangler.json` and deployment tests; Web actual `tooling/cloudflare.ts`, `project.ts`, `candidate.ts`, Worker and provenance tests | Keep real authorization/crypto/business/PG behavior. `deploy` currently includes monitoring; the guarded deployment implementation is in tooling and Worker, not `eng/deploy`. HOST-03 delivers infrastructure, with finished Dashboard assembly deferred to DIST-01. [C-internal] [C-tooling] [C-worker] [C-docker] [W-tools] |
| `AFV2-WEB-01..04` | Web `src/ArcForges.Web.App`, `ArcForges.Web.Ui`, relevant Site/profile composition, actual tests, build/tooling/Worker integration; planned UX acceptance records | Page-only scope would omit typed clients, view models, session state and Program wiring. Rendering fixtures cannot establish final business/control effects. [W-app] [W-ui] [W-pages] [W-tools] |
| `AFV2-MIG-01/02` | The named Node/CLI/client/platform projects; the exact Cloud C# paths listed below; Go fleet/mobile adapters and registrations; actual Contracts producer roots for approved current-source retirement, followed by inventory-only `eng/v2-consumers` during database contraction | Remove the old execution/serving path after real replacement acceptance. DesktopPlatform and other independent apps are read-only consumer checks; a proven required change needs its own concrete reviewed scope. Applied migration bytes, immutable published artifacts and independent APIs stay preserved. [A-src] [C-src] [C-mobile] [K-policy] |
| `AFV2-DIST-01/02`, `AFV2-ACC-01/02`, `AFV2-PROD-01` | Actual ArcForges packaging/publish/update composition and tests; actual Cloud/Web guarded tooling, Worker/deployment/operations records; declared acceptance tests and planned install/release records | DIST-01 assembles the real completed Go/PostgreSQL/Blazor product after WEB-04 through MIG-01. Runtime/native evidence and provider activation remain separate; source paths do not grant authority to alter verification or deployment guards. [A-eng] [A-packaging] [C-tooling] [W-tools] |

The retired Cloud C# host is `src/ArcForges.Cloud/`, with storage in `src/ArcForges.Cloud.Storage.D1/`. The current module directories are `src/ArcForges.Cloud.Modules.Abstractions/`, `Agent/`, `Audit/`, `Chat/`, `Commerce/`, `Configuration/`, `Devices/`, `Entitlement/`, `Identity/`, `Notification/`, `PackageCatalog/`, `Policy/`, `Resource/`, `Scope/`, `Search/`, `Support/`, `Sync/`, `Task/`, `TrustSafety/` and `Workspace/`, where each shortened name has the same `src/ArcForges.Cloud.Modules.` prefix. MIG-01's machine-readable paths enumerate every full project name. They are REMOVE from the serving/build/deploy composition after qualified Go replacement, not permanently disabled alternative hosts. Needed entitlement algorithms/vectors and immutable D1/applied migration bytes are preserved or extracted as evidence first. No independent application API is deleted by this host retirement. [C-src] [C-entitlement-parity]

Go `fleet`/`fleetapi` are mixed assets: retain or move enrollment/proof/registry behavior, then delete old Task/file/workspace business handlers. Remove ArcForges `mobileauth`, `mobiletest`, `center/cmd/mobile-probe` and their routes/pages/server registrations after the cancelled product inventory closes. Rework Worker foundation transport and the Docker entrypoint to the sole Go server; do not delete useful Go Container ingress merely because it shares old composition files. [C-fleet] [C-fleet-api] [C-mobile] [C-internal] [C-docker] [C-worker]

## Source index

Every source citation above resolves to the audited immutable commit. Referenced file/directory paths were checked against the corresponding local source revision; no moving `main` link is used as evidence.

[C-server]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/server/server.go
[C-config]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/config/config.go
[C-routes]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/routes/routes.go
[C-identity]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/identity
[C-identity-routes]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/routes/identity.go
[C-session]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/session/verify.go
[C-pages]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/pages
[C-pages-routes]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/routes/pages.go
[C-fleet]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/fleet
[C-fleet-api]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/fleetapi
[C-access]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/access/access.go
[C-hub]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/hub/hub.go
[C-hub-upgrade]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/hub/upgrade.go
[C-hub-lease]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/hub/lease.go
[C-hub-calls]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/hub/calls.go
[C-hub-keyring]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/hub/keyring.go
[C-hub-sign]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/hub/sign.go
[C-fleet-routed]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/fleet/routed.go
[C-fleet-api-routed]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/fleetapi/routed.go
[C-fleet-files]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/fleet/routed_files.go
[C-fleet-api-files]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/fleetapi/routed_files.go
[C-mobile]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/mobileauth
[C-mobile-routes]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/routes/mobile.go
[C-entitlement]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/entitlement
[C-entitlement-parity]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/entitlement/parity_test.go
[C-entitlement-operator]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/entitlement/operator.go
[C-feature]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/feature/feature.go
[C-feature-gate]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/feature/gate.go
[C-commerce]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/src/ArcForges.Cloud.Modules.Commerce/CommerceModule.cs
[C-internal]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal
[C-src]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/src
[C-store]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/store
[C-schema]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/schema/schema.go
[C-migrations]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/schema/migrations
[C-migrate]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/store/migrate/migrate.go
[C-grants]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/store/migrate/grants.go
[C-bridge]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/store/migrate/ctr06_bridge_gate.go
[C-prepare]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/store/migrate/ctr06_prepare.go
[C-restore]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/internal/store/migrate/ctr06_restore_admission.go
[C-gomod]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/center/go.mod
[W-app]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.App/ArcForges.Web.App.csproj
[W-ui]: https://github.com/ArcForges/Web/tree/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.Ui
[W-account]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.App/Pages/Account.razor
[W-chat]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.App/Pages/Chat.razor
[W-operations]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.Operations/Pages/Shell.razor
[W-session]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.App/Probe/SessionProbe.cs
[W-tools]: https://github.com/ArcForges/Web/tree/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/tooling
[W-policy]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/AGENTS.md
[W-pages]: https://github.com/ArcForges/Web/tree/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/src/ArcForges.Web.App/Pages
[K-policy]: https://github.com/ArcForges/Contracts/blob/de3dba76266e89654be9b4d29d097d525a281c6a/AGENTS.md
[K-packages]: https://github.com/ArcForges/Contracts/blob/de3dba76266e89654be9b4d29d097d525a281c6a/eng/contract-packages.json
[K-access]: https://github.com/ArcForges/Contracts/blob/de3dba76266e89654be9b4d29d097d525a281c6a/eng/policy/contract-access.json
[K-foundation]: https://github.com/ArcForges/Contracts/blob/de3dba76266e89654be9b4d29d097d525a281c6a/eng/foundation-inventory.json
[K-public-proto]: https://github.com/ArcForges/Contracts/tree/de3dba76266e89654be9b4d29d097d525a281c6a/public/proto
[K-internal-proto]: https://github.com/ArcForges/Contracts/tree/de3dba76266e89654be9b4d29d097d525a281c6a/internal/proto
[K-generated]: https://github.com/ArcForges/Contracts/tree/de3dba76266e89654be9b4d29d097d525a281c6a/go
[K-tests]: https://github.com/ArcForges/Contracts/tree/de3dba76266e89654be9b4d29d097d525a281c6a/tests
[K-fixtures]: https://github.com/ArcForges/Contracts/tree/de3dba76266e89654be9b4d29d097d525a281c6a/fixtures
[A-src]: https://github.com/ArcForges/ArcForges/tree/10f692224f94916cfc93fbad971f80ec340c5edf/src
[A-tests]: https://github.com/ArcForges/ArcForges/tree/10f692224f94916cfc93fbad971f80ec340c5edf/tests
[A-eng]: https://github.com/ArcForges/ArcForges/tree/10f692224f94916cfc93fbad971f80ec340c5edf/eng
[A-packaging]: https://github.com/ArcForges/ArcForges/tree/10f692224f94916cfc93fbad971f80ec340c5edf/packaging
[C-tooling]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/tooling
[C-worker]: https://github.com/ArcForges/Cloud/tree/6df33c525fcbc20495e46c9c4c011086146da796/worker
[C-docker]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/Dockerfile
[D-node]: https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/Directory.Packages.props
[D-cloud]: https://github.com/ArcForges/Cloud/blob/6df33c525fcbc20495e46c9c4c011086146da796/Directory.Packages.props
[D-web]: https://github.com/ArcForges/Web/blob/56bb40fe7d1693013b4b1e2a82f1b796a65629c5/Directory.Packages.props
[D-desktop]: https://github.com/ArcForges/DesktopPlatform/blob/e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6/Directory.Packages.props
[D-mobile]: https://github.com/ArcForges/Mobile/blob/072ee675e8ea67e779922082dbf65dbc02ed6916/Directory.Packages.props
[D-ai]: https://github.com/ArcForges/AI/blob/70f8b22d56d67abd2a983f8b448846731ee22902/package.json
[D-scope]: https://github.com/ArcForges/ArcScope/blob/485c8d6d9a84825eb5bc737c9808b8bc4b616643/Directory.Packages.props
[D-slate]: https://github.com/ArcForges/ArcSlate/blob/569785a050c97a8022fe264f6af986285766bf87/Directory.Packages.props
[D-notes]: https://github.com/ArcForges/ArcNotes/blob/2839da696cf3d6cc8ab3c241212eea8403c5a0a1/Directory.Packages.props
[D-scope-hello]: https://github.com/ArcForges/ArcScope/blob/485c8d6d9a84825eb5bc737c9808b8bc4b616643/src/ArcForges.ArcScope.Core/CloudHelloClient.cs
[D-slate-hello]: https://github.com/ArcForges/ArcSlate/blob/569785a050c97a8022fe264f6af986285766bf87/src/ArcForges.ArcSlate.Core/CloudHelloClient.cs
[D-notes-hello]: https://github.com/ArcForges/ArcNotes/blob/2839da696cf3d6cc8ab3c241212eea8403c5a0a1/src/ArcForges.ArcNotes.Core/CloudHelloClient.cs
[D-mobile-hello]: https://github.com/ArcForges/Mobile/blob/072ee675e8ea67e779922082dbf65dbc02ed6916/src/core/ArcForges.Mobile.Network/CloudHelloClient.cs
[D-ai-hello]: https://github.com/ArcForges/AI/blob/70f8b22d56d67abd2a983f8b448846731ee22902/src/hello.ts
[D-scope-data]: https://github.com/ArcForges/ArcScope/blob/485c8d6d9a84825eb5bc737c9808b8bc4b616643/src/ArcForges.ArcScope.Infrastructure/Annotations/SqliteAnnotationStore.cs
[D-content-sandbox]: https://github.com/ArcForges/DesktopPlatform/blob/e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6/src/DesktopHelpers/ArcForges.ContentSandbox.Contracts/ContentSandboxContract.cs
[P-graph]: https://github.com/ArcForges/Plan/blob/742ed2660c5e934e1df86f90e54198b3a199e2b1/delivery-graph.json
[P-ledger]: https://github.com/ArcForges/Plan/blob/742ed2660c5e934e1df86f90e54198b3a199e2b1/ledger/ledger.jsonl
[P-acceptance]: https://github.com/ArcForges/Plan/blob/742ed2660c5e934e1df86f90e54198b3a199e2b1/acceptance-register.md
