# Inventory and classification

Decision: [AD-0013](../decisions/AD-0013-reuse-and-supersession.md). Classes: **Reuse** (unchanged, pinned), **Adapt** (bounded change by a named task), **Retain** (kept for future products; not scheduled, not deleted), **Superseded** (history only for active development).

**Baseline** (the main heads inspected on 2026-10-12):

| Repository | Head | Licence |
|---|---|---|
| ArcForges (implementation) | `966f062` (initial commit, licence only) | AGPL-3.0 |
| Contracts | `b774c322` | Apache-2.0 |
| DesktopPlatform | `60309ec9` | AGPL-3.0 |
| Cloud | `92ba1dc9` | AGPL-3.0 |
| Web | `dd0a5de3` | AGPL-3.0 |
| Mobile | `6702e281` | Apache-2.0 |
| ArcScope | `485c8d6d` | — |
| ArcSlate | `569785a` | — |
| ArcNotes | `2839da6` | — |
| AI | `70f8b22` | — |
| ArcForges-Design-Parallel | `64173614` | — |
| Plan-Parallel | `5ccbb392` | — |

## 1. Contracts

| Item | Class | Use / reason | Task |
|---|---|---|---|
| `arcforges.foundation.v1` | Reuse | Envelope, error, ID and paging types for every new package | AF-CON-01 (pins) |
| `publicapi.v1` Identity, Entitlement, Commerce, Support, Notification, Data | Reuse (contracts unchanged; endpoints are new work, §3) | Account, plan, checkout, support, push and export ([contracts/reuse-map.md](../contracts/reuse-map.md)) | AF-ID-01, AF-ID-02, AF-CLD-03, AF-COM-01, AF-SUP-01, AF-CLD-06 |
| `publicapi.v1` Device | Reuse (no schema change) | Product values `arcforges-node` and `arcforges-mobile` are data; one device per node and per phone | AF-ID-02 |
| `publicapi.v1` `SupportAccessService` (new file `support_access.proto`) | New, additive | The owner reads an operator's access request before deciding it | AF-CON-01, AF-SUP-01 |
| `operator.v1.OperatorService` | Reuse (contract unchanged; implementation new) | Operations profile | AF-OPS-01 |
| `operator.v1` `OperatorReadService` (new file `operator_read.proto`) | New, additive | Audit events, operating budgets and the monthly report for W-66 and W-67 | AF-CON-01, AF-OPS-01 |
| `events.v1` | Retain | Stream position shape mirrored, not imported | — |
| `publicapi.v1` chat, content, connector, scope, sync, transfer, application, descriptors; `catalog`, `extensions`, `simulation`, `hello`; internal `cf.*`, `local.*` | Retain | Earlier product family | — |
| `ArcForges.Cli` tool package (command `arcforges`) | Adapt | Rename the command in its next version (conflict C-03) | AF-CON-02 |
| Published versions (including rolled-back `1.0.0-ci.350.1`) | Reuse as history | Never unpublished, deprecated or deleted. Rolled-back versions are never pinned. | — |

## 2. DesktopPlatform

| Package | Class | Use / reason | Task |
|---|---|---|---|
| `ArcForges.LocalRpc` | Adapt | Service-endpoint mode, stream lane, per-method limit profiles, peer identity provider ([desktopplatform-refactor.md](desktopplatform-refactor.md)) | AF-DP-01 |
| `ArcForges.Security.Secrets` | Adapt | Linux backends: Secret Service over D-Bus, and a 0600-file fallback reported as weaker | AF-DP-02 |
| `ArcForges.Observability` | Reuse | Structured logging with the redaction processor (node, CLI, Desktop) | AF-NODE-01 |
| `ArcForges.DesignSystem`, `ArcForges.Desktop.Shell` | Reuse | Tokens, surface catalogue, command palette, layout persistence, lifecycle, accessibility tree, pseudo-localizer (models). The Avalonia view adapter is written in the ArcForges repository. | AF-DESK-01 |
| `ArcForges.Build.Policy` | Reuse | Repository build policy (analyzers, AOT settings, lock files) for the new ArcForges repository. Never the rolled-back `1.0.0-ci.124.1`. | AF-REPO-01 |
| `ArcForges.Persistence.Sqlite` | Reuse if it fits | SQLite AOT setup and migration helpers. AF-NODE-02 checks its fit against [node-store.md](../data/node-store.md); if it does not fit, the node uses `Microsoft.Data.Sqlite` directly and the package stays Retain. | AF-NODE-02 |
| `ArcForges.NativeInterop` | Reuse if it fits | Source-generated P/Invoke helpers. The node's platform layer may use it; otherwise its own `LibraryImport` declarations. | AF-EXEC-01 |
| `ArcForges.Foundation`, `ArcForges.Security`, `ArcForges.Security.Audit` | Reuse if it fits | Base helpers and local audit primitives, evaluated by the first task that needs them | AF-NODE-01 |
| `ArcForges.Application.Abstractions`, `Assistant.Abstractions`, `Capabilities`, `Contributions`, `Desktop.Experience`, `Desktop.Graphics`, `Desktop.Preview`, `Desktop.RichContent`, `Desktop.Text`, `Persistence.Derived`, `Persistence.Resources`, `Observability.Desktop` | Retain | Application-family building blocks for ArcScope, ArcSlate and ArcNotes | — |
| `ArcForges.ContentSandbox*`, `ArcForges.Native.Image*` | Retain | Document and image sandboxing for future products | — |
| Unfinished: ContentSandbox Linux TSYNC, the Desktop.Shell Avalonia adapter inside DesktopPlatform, the PLT.66 Contracts move, wrong-user procedures | Retain | Not prerequisites (AD-0013 §4) | — |

## 3. Cloud

| Item | Class | Use / reason | Task |
|---|---|---|---|
| C# host `ArcForges.Cloud` (Containers, AOT; serves only `HelloService` at `92ba1dc9`), Worker ingress, guarded deploy scripts, local workerd verification scripts | Reuse | The flagship host profile composes only the modules it needs | AF-CLD-01 |
| D1 storage layer: command receipts and guard, commit tail (outbox publisher, inbox, purge plans) | Reuse | Implemented and tested | AF-CLD-01 |
| Job leases, job runner and scheduled sweeps (`platform_job_lease` table only; `wrangler.json` has no cron triggers) | Schema reused; implementation **new** | Lease and fence plans, a Worker cron trigger calling the host, retention sweeps | AF-PLAT-01 |
| Identity: user and credential domain rules and the D1 store (enrollment) | Reuse (domain and schema); endpoints **new** | No authentication ceremonies, sessions, step-up, recovery or deletion endpoints exist. They are built from the reused contracts: passkeys, e-mail codes, sessions with native bearer and step-up (AF-ID-01); recovery, deletion with grace, export, devices and security activity (AF-ID-02). | AF-ID-01, AF-ID-02 |
| Entitlement: resolver, snapshots, grants | Reuse (domain and schema); endpoints **new** | `EntitlementService` endpoints, flagship plan catalogue, token claim projection | AF-CLD-03 |
| Devices, Commerce, Notification, Support, Audit, Configuration (15-line placeholders at `92ba1dc9`) | Contract and schema reused; implementation **new** | [10](../architecture/10-cloud.md) §2: device endpoints; Paddle provider; FCM sender; support cases and access grants; audit writer and reader; configuration revisions and kill switches | AF-ID-02, AF-COM-01, AF-CLD-06, AF-SUP-01, AF-PLAT-01 |
| Operating budgets and reservations (tables only) | Schema reused; service **new** | Budget checks on metered paths | AF-PLAT-01 |
| Google Play provider | New | `StoreBillingService`, RTDN, acknowledgement job | AF-CLD-07 |
| Operator endpoints (`operator.v1.OperatorService`), including the TrustSafety enforcement and appeal methods (TrustSafety is a placeholder at `92ba1dc9`) | Contract and schema reused; implementation **new** | The operator console reads and acts through it; new `OperatorReadService` for audit and budgets | AF-OPS-01 |
| New module Fleet; Worker relay routes and `FleetHub` Durable Object | New | [10](../architecture/10-cloud.md) | AF-CLD-02, AF-CLD-04 |
| Modules Chat, Task, Agent, Sync, Resource, Search, Scope, PackageCatalog, Policy, Workspace | Retain | Not composed into the flagship host profile; tables untouched | — |
| D1 schema and migrations | Reuse + Adapt | [cloud-store.md](../data/cloud-store.md) | AF-CLD-01 |

## 4. Web

| Item | Class | Use / reason | Task |
|---|---|---|---|
| `ArcForges.Web.Site` (static C# generator), `ArcForges.Web.Ui`, profile bundle and budget tooling, Worker static-asset adapter, guarded deploy | Reuse | Public site pages are rewritten for ArcForges | AF-WEB-01 |
| `ArcForges.Web.App` Account profile | Adapt | Pages W-20…W-29 | AF-WEB-02 (W-24 with AF-CLD-07, W-25 with AF-SUP-01, W-29 with AF-CLD-06) |
| `ArcForges.Web.App` Chat profile | Retain | Not routed for the flagship | — |
| Fleet profile | New | W-40, W-41 | AF-WEB-03 |
| `ArcForges.Web.Operations` | Adapt | Skeleton becomes the operator console (W-60…W-67) | AF-OPS-01 |

## 5. Mobile

| Item | Class | Use / reason | Task |
|---|---|---|---|
| MAUI app shell, AOT/R8 release configuration, gRPC-Web network layer (`ArcForges.Mobile.Network`), Keystore wrapper (`ArcForges.Mobile.Security`) | Reuse | [12](../architecture/12-client-applications.md) §6 | AF-AND-01 |
| Screens, view models, Play Billing, FCM, QR | New | [experience/android.md](../experience/android.md) | AF-AND-* |
| "Play channel out of scope" position (README) | Superseded | AD-0010; conflict C-05 | AF-AND-03 |

## 6. ArcScope, ArcSlate, ArcNotes, AI

| Repository | Class | Notes |
|---|---|---|
| ArcScope | Retain | Future product. It will consume the node API for execution and resources ([AD-0013](../decisions/AD-0013-reuse-and-supersession.md)). No changes now. |
| ArcSlate, ArcNotes | Retain | Future products |
| AI (TypeScript harness) | Superseded (read-only history) | Its harness role ended with HAR.40. AI-client integration is now in the C# node. |

## 7. Historical design and plan

| Item (ArcForges-Design-Parallel `64173614` unless noted) | Class | Notes |
|---|---|---|
| P2-021 C#-first stack decision | Reuse (cited) | AD-0003 |
| BC-01 Paddle as sole web Merchant of Record; FCM HTTP v1 push design; system-browser PKCE for native sign-in | Reuse (cited) | V-C07, AD-0010, AD-0011 |
| Registry04 contract records and conventions | Reuse (via Contracts) | Foundation conventions |
| Security and observability architecture chapters (`08-security-architecture.md`, `13-observability-and-operations.md`) | Reuse (cited where applicable) | [11](../architecture/11-security-privacy.md), [14](../architecture/14-commercial-operations.md) |
| ArcScope-centred family scope and journeys | Superseded | AD-0001 |
| Parallel delivery model: P2-018 graph, DLV-25, DLV-31 build slot, DLV-42 coordinator capacity, `delivery.py` claims, leases and roles | Superseded | AD-0014 |
| "Reviewer coverage" (2026-10-08) and "Pre-push coverage" (2026-10-09) practices | Superseded | AD-0014 §4 |
| Dependency-admission practice (receipts, provenance, review reseal, locked restores) | Reuse | Applies unchanged to the repositories that already use it, and to the ArcForges repository |
| Plan-Parallel graph, ledger, claims, entry prompts and launcher | Superseded (history) | Plan `history/` and `history/legacy-disposition.md` |
| Unfinished branches (NAT.01, POL.01, CLOUD.05, CLOUD.13) and CON.43 (merged, unrecorded) | Retain (history) | Classified in the Plan legacy disposition; never resumed implicitly |

## 8. Local working environment

| Item | Class | Notes |
|---|---|---|
| `C:\MyFile\Projects\ArcForges - Final.md` launcher | Superseded and rewritten | The new single objective; the old text is archived in Plan `history/` |
| `haiku-worker` agent definitions (project-level and user-level) | Superseded | The legacy build-slot workflow is retired; current delegation follows AD-0014 without a required provider or model. On 2026-10-12 both definitions, and the user-level backup, were moved to `ArcForges/.claude/coordinator/retired-agents/` and archived in Plan `history/legacy-agents/` (conflict C-14). |
| Coordinator notes (`.claude/coordinator/`) | Retain (history) | Waiting audit and scope status kept as evidence |
