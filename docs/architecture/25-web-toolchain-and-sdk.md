# Web Toolchain, Generated SDK and Developer Workflow

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008), [D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009), [D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)
> Companions: [Web architecture](10-web-architecture.md), [solution layout](01-solution-and-project-layout.md), [build architecture](14-build-packaging-and-release.md)

This is the implementation contract for the React/TypeScript boundary. Handwritten proto in Contracts is authored business wire authority; C# owns business behavior. Node.js runs development, generation, tests and static production builds; production browser assets are served by the edge and all dynamic business requests execute in the existing ASP.NET Core Cloud host.

## 1. Selected stack and ownership

| Area | Baseline | Owner and constraint |
|---|---|---|
| UI | React + React DOM; strict TypeScript | One account/chat application, with separately built profile route graphs |
| Routing and public generation | React Router framework mode on Vite; runtime SSR disabled | Application profiles use client loaders; Site pre-renders the complete public locale/URL inventory at build time |
| Design system | Tailwind CSS, owned shadcn/ui-derived components, Motion where interaction requires it | Shared tokens, accessible behavior and reviewed upstream updates; ordinary CSS transitions for simple effects |
| Data access | Generated gRPC-Web SDK; TanStack Query | SDK from released Contracts proto; query cache is a projection, never authority |
| Runtime validation | Generated Zod schemas | Wire shape only; server remains responsible for authorization and business validation |
| Realtime | Generated unary EventService.Poll; separate CF WS/HTTP presentation | Same version/recovery rules as C# clients, with independent language adapters |
| Toolchain | Node.js 24 LTS + npm workspaces | Exact supported Node patch and bundled npm version pinned when [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) creates the implementation manifest; no Bun, Deno, yarn or pnpm baseline |
| Tests | Vitest, React Testing Library, Playwright, accessibility checks | TypeScript tests run under Node/browser, C# server tests retain Microsoft.Testing.Platform |
| VS integration | One JavaScript SDK `.esproj` in `win.slnx` | Windows IDE entry only; no JavaScript SDK dependency in the portable managed graph |

| # | Rule |
|---|---|
| <a id="rule-wts-01"></a>WTS-01 | **All first-party Web UI and Web build/test automation are TypeScript.** Configuration may use JSON, XML, CSS and declarative formats. Browser production output is JavaScript; this does not authorize JavaScript/DOM UI inside Avalonia desktops. |
| <a id="rule-wts-02"></a>WTS-02 | **One npm workspace root at ArcForges-Web and one committed `package-lock.json` there.** It owns both deliverables and internal packages; no nested lockfiles or second package manager. |
| <a id="rule-wts-03"></a>WTS-03 | **Pin direct dependencies exactly, including code generators, and commit the resolved closure.** Node/npm, React, Router, Vite, TypeScript, the JS SDK, and all CI actions/images carry reviewed versions. No `latest` or prerelease baseline; an upgrade regenerates and verifies the contracts and production artifacts. |
| <a id="rule-wts-04"></a>WTS-04 | **NuGet central management governs .NET, npm manifests govern Web.** An npm dependency is not a `Directory.Packages.props` entry. Both graphs join the repository licence, secret, provenance and vulnerability policy. |
| <a id="rule-wts-05"></a>WTS-05 | **Node is not a second business backend.** No Express/Nest API, Node agent loop, provider credentials or billing implementation is introduced. Static rendering during a build is permitted; request-time Node SSR and React Server Components are outside this baseline. |

**Source/configuration policy.** New TS/TSX/tooling source carries the applicable SPDX header. npm JSON manifests use their licence metadata; JSON cannot acquire invalid comment headers. Repository policy recognizes these formats explicitly. Shared .NET Directory.Build imports are conditioned on managed project type so esproj never inherits language/AOT/NuGet settings intended for csproj.

## 2. Independent Web repository

ArcForges-Web owns apps/site (static public generation), apps/app (explicit Account/Chat/operator/status route profiles), packages/ui (AGPL), tooling/, tests/, package.json/package-lock.json, .node-version, ArcForges.Web.esproj and win.slnx. Consume @arcforges/proto/api-client from Contracts; there is no local SDK source tree, Cloud ProjectReference or native build dependency. Portable npm commands work without Visual Studio; esproj delegates to those same commands and explicit npm ci, with no implicit install/build race.

Development may start an exact released Cloud container or explicit built candidate from an independently checked-out Cloud repository. F5 identifies its image/endpoint and waits for health; no automatic second business host is launched. Account and Chat development origins are distinct hostnames, not only different ports. Only a reviewed dev profile permits dev certificates/HMR; no dev proxy/CSP relaxation enters release.


**Preserved rule anchors.** These identifiers now resolve to the selected rules in this section: <a id="rule-wvs-01"></a>WVS-01 <a id="rule-wvs-02"></a>WVS-02 <a id="rule-wvs-03"></a>WVS-03 <a id="rule-wvs-04"></a>WVS-04 <a id="rule-wvs-05"></a>WVS-05 <a id="rule-wvs-06"></a>WVS-06 <a id="rule-wcli-01"></a>WCLI-01 <a id="rule-wcli-02"></a>WCLI-02 <a id="rule-wcli-03"></a>WCLI-03 <a id="rule-wcli-04"></a>WCLI-04.

---

<a id="3-c--openapi--typescript"></a>
## 3. Proto to C# and TypeScript

Contracts handwritten public proto → pinned protoc/C#/protobuf-es generation → released descriptors and compatibility fixtures → Apache generated API client → Web/RN consumers. [Wire registry](contracts/04-protobuf-wire-registry.md) fixes every numbered field, method, exact value, error and previous/current case. Business proto is not generated from C# handlers/OpenAPI.

<a id="31-exact-wire-values"></a>
### 3.1 Exact wire values

Use protobuf bigint for all 64-bit counters and integer microcredits; JSON exceptions use canonical decimal strings. Money uses exact Decimal string, media uses signed ticks/reduced rational, GUID uses canonical16 bytes, scalar null/absent is explicit. These preserve the complete content-origin/Notes/Scope profile oracles. No number coercion or metadata-only OpenAPI transformer may change actual bytes. [Independent vectors](contracts/04-protobuf-wire-registry.md#2-exact-values-canonical-identity-and-evolution) are required in both directions.

<a id="32-realtime-and-streaming"></a>
### 3.2 Realtime and streaming

React uses createGrpcWebTransport with generated unary EventService.Poll plus authoritative reads. All 17 hints are optional and never commit state. CF AI uses same-origin WebSocket presentation and bounded HTTP range recovery; Unicode offsets, supersession, truncation and final-message reference follow the shared CF contract. No SignalR package or mandatory fetch-streaming path remains.


**Preserved rule anchors.** These identifiers now resolve to the selected rules in this section: <a id="rule-wsdk-01"></a>WSDK-01 <a id="rule-wsdk-02"></a>WSDK-02 <a id="rule-wsdk-03"></a>WSDK-03 <a id="rule-wsdk-04"></a>WSDK-04 <a id="rule-wsdk-05"></a>WSDK-05 <a id="rule-wsdk-06"></a>WSDK-06 <a id="rule-wsdk-07"></a>WSDK-07 <a id="rule-wsdk-08"></a>WSDK-08 <a id="rule-wnum-01"></a>WNUM-01 <a id="rule-wnum-02"></a>WNUM-02 <a id="rule-wnum-03"></a>WNUM-03 <a id="rule-wev-01"></a>WEV-01 <a id="rule-wev-02"></a>WEV-02 <a id="rule-wev-03"></a>WEV-03 <a id="rule-wev-04"></a>WEV-04.

---

## 4. Build, test and release closure

| # | Rule |
|---|---|
| <a id="rule-wci-01"></a>WCI-01 | **Full validation orders producers before consumers:** locked restores → proto generation → compatibility diff → TS SDK generation → TS check/lint/test → production builds → real API/browser tests → SBOM/attestation. A later export cannot validate an earlier build made from stale contracts. |
| <a id="rule-wci-02"></a>WCI-02 | **CI has separate managed, native and Web jobs.** Web changes run Node checks; authored public proto changes also trigger export and TS/browser contract jobs. Shared tokens, dependency locks, edge auth and deployment changes trigger the affected Web artifacts and browser tests. |
| <a id="rule-wci-03"></a>WCI-03 | **Build one release set containing site/account/chat and their manifest**, then promote those same bytes. Runtime public config is fetched from a same-origin, schema-validated, non-cacheable config document before API access; it contains no secret and cannot redirect authenticated requests to an arbitrary host. Profile selection and route inclusion are build inputs, environment endpoints are deployment configuration. |
| <a id="rule-wci-04"></a>WCI-04 | **Cache hashed assets immutably, HTML briefly, and authenticated API/session/config data with no-store.** Retain old assets through the client compatibility window. CSP and security headers are served by the edge; rollback restores the matching assets, manifest and compatible headers/config. |
| <a id="rule-wci-05"></a>WCI-05 | **No default service worker or persistent account/chat query cache.** Keep unsent text through a transient connection loss in memory; logout, workspace/user change and revocation clear UI caches and abort requests. A late response from a prior session cannot repopulate the next user's state. |
| <a id="rule-wci-06"></a>WCI-06 | **Tests prove both independence and real integration.** Fixture UI checks are fast; release checks use production assets, a real C# host and PostgreSQL plus approved payment test environments. Playwright covers Chromium/Firefox/WebKit with real Safari/assistive checks for the supported browser matrix. |
| <a id="rule-wci-07"></a>WCI-07 | **Supply-chain evidence covers shipped browser code and build tooling.** Package locks, generator versions, source maps, npm licence/NOTICE output and SBOM are retained; public source maps are disabled unless explicitly reviewed. Configure trusted lifecycle scripts during restore; builds do not fetch dependencies, fonts, content or live pricing. |
| <a id="rule-wci-08"></a>WCI-08 | **Windows and non-Windows entry points are verified independently.** VS solution load/build/F5 is a Windows verification obligation; npm commands are exercised on Windows/Linux/macOS as appropriate. Existing CMake and .NET gates retain their own evidence and never substitute for Web checks. |

## 5. Implementation ownership

| Producer | Required output | Consumers |
|---|---|---|
| [WP-01](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01) / [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) | Web workspace, esproj/solution boundary, Node/npm pins, lock, commands and scoped policy | [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-47](../planning/work-packages/47-static-public-site.md#rule-wp-47) |
| [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) / [WP-04](../planning/work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) | authored proto/descriptor baseline, exact primitive wire values, generated SDK foundation | [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-23](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23) |
| [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) / [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) | Architecture constraints and first production React/SDK/real C# round trip | All later Web integration |
| [WP-22](../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22) / [WP-23](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23) / [WP-24](../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24) | Browser session adapter, production public APIs, SDK and event conformance | [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48), [WP-49](../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49) |
| [WP-47](../planning/work-packages/47-static-public-site.md#rule-wp-47) | Static site plus owned visual component/token baseline | [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48) |
| [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48) / [WP-49](../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49) | Account and Chat experiences using the real Cloud | [WP-50](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50) |
| [WP-50](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50) | Complete artifact, browser, origin, rollback and release evidence | Commercial release |

## 6. Primary references checked for this decision

- [Visual Studio JavaScript MSBuild properties](https://learn.microsoft.com/en-us/visualstudio/javascript/javascript-project-system-msbuild-reference?view=visualstudio): explicit install/build/start commands and esproj behavior.
- [Visual Studio React/ASP.NET template](https://learn.microsoft.com/en-us/visualstudio/javascript/tutorial-asp-net-core-with-react?view=visualstudio): Vite client and solution integration.
- [npm workspaces](https://docs.npmjs.com/cli/v11/using-npm/workspaces/), [Node release lifecycle](https://nodejs.org/en/about/previous-releases): one dependency workspace and supported Node LTS.
- [React Router rendering](https://reactrouter.com/start/framework/rendering): client rendering and build-time pre-rendering with runtime SSR disabled.
- [ASP.NET Core OpenAPI](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-10.0?view=aspnetcore-10.0#openapi): historical C# OpenAPI approach, superseded by P2-009.
- [gRPC-Web protocol](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md) and [Connect Web transport](https://connectrpc.com/docs/web/choosing-a-protocol/): selected binary unary request/status/trailer framing and generated TS transport.
- [shadcn/ui](https://ui.shadcn.com/docs), [Motion](https://motion.dev/docs/react): owned composable components and optional richer interaction.

These establish the selected mechanisms, not a completed production build. Exact package compatibility and security behavior remain implementation checks with the owners above.

## 7. Selected Web baseline

Web retains React/Vite/React Router static profiles, selects React 19.3.0/Router 8.3.1/Vite 8.3.0/TS7.0.2 with existing UI/query/accessibility choices. Root paths apps/site, apps/app, packages/ui, tooling, tests, win.slnx + ArcForges.Web.esproj; no SDK source in Web (consume Apache Contracts package). Account/Chat/operator/status are explicit separately built route graphs; no runtime SSR. Pin other existing direct UI/test deps from their own approved manifest during initial build, without changing architecture; equivalent patch lock resolution is an implementation detail. Origins/runtime config/CSP/CSRF/cookie segregation and asset rollback rules remain.

[Mobile](11-mobile-architecture.md#3-runtime-libraries-and-lifecycle-baseline) owns the RN stack; Web consumes only its declared package/route profile. [Wire registry](contracts/04-protobuf-wire-registry.md) owns public schemas and adapters.
