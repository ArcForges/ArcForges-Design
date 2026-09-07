# Web Toolchain, Generated SDK and Developer Workflow

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008), [D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009), [D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)
> Companions: [Web architecture](10-web-architecture.md), [solution layout](01-solution-and-project-layout.md), [build architecture](14-build-packaging-and-release.md)

This is the implementation contract for the React/TypeScript boundary. C# remains the authored source of public wire contracts and business behavior. Node.js runs development, generation, tests and static production builds; production browser assets are served by the edge and all dynamic business requests execute in the existing ASP.NET Core Cloud host.

## 1. Selected stack and ownership

| Area | Baseline | Owner and constraint |
|---|---|---|
| UI | React + React DOM; strict TypeScript | One account/chat application, with separately built profile route graphs |
| Routing and public generation | React Router framework mode on Vite; runtime SSR disabled | Application profiles use client loaders; Site pre-renders the complete public locale/URL inventory at build time |
| Design system | Tailwind CSS, owned shadcn/ui-derived components, Motion where interaction requires it | Shared tokens, accessible behavior and reviewed upstream updates; ordinary CSS transitions for simple effects |
| Data access | Generated Fetch SDK; TanStack Query | SDK from local generated OpenAPI; query cache is a projection, never authority |
| Runtime validation | Generated Zod schemas | Wire shape only; server remains responsible for authorization and business validation |
| Realtime | Official SignalR JavaScript client, JSON; generated event DTOs/validators | Same version/recovery rules as C# clients, with independent language adapters |
| Toolchain | Node.js 24 LTS + npm workspaces | Exact supported Node patch and bundled npm version pinned when [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) creates the implementation manifest; no Bun, Deno, yarn or pnpm baseline |
| Tests | Vitest, React Testing Library, Playwright, accessibility checks | TypeScript tests run under Node/browser, C# server tests retain Microsoft.Testing.Platform |
| VS integration | One JavaScript SDK `.esproj` in `win.slnx` | Windows IDE entry only; no JavaScript SDK dependency in the portable managed graph |

| # | Rule |
|---|---|
| <a id="rule-wts-01"></a>WTS-01 | **All first-party Web UI and Web build/test automation are TypeScript.** Configuration may use JSON, XML, CSS and declarative formats. Browser production output is JavaScript; this does not authorize JavaScript/DOM UI inside Avalonia desktops. |
| <a id="rule-wts-02"></a>WTS-02 | **One npm workspace root at `src/Web` and one committed `package-lock.json` there.** It owns both deliverables and internal packages; no nested lockfiles or second package manager. |
| <a id="rule-wts-03"></a>WTS-03 | **Pin direct dependencies exactly, including code generators, and commit the resolved closure.** Node/npm, React, Router, Vite, TypeScript, the JS SDK, and all CI actions/images carry reviewed versions. No `latest` or prerelease baseline; an upgrade regenerates and verifies the contracts and production artifacts. |
| <a id="rule-wts-04"></a>WTS-04 | **NuGet central management governs .NET, npm manifests govern Web.** An npm dependency is not a `Directory.Packages.props` entry. Both graphs join the repository licence, secret, provenance and vulnerability policy. |
| <a id="rule-wts-05"></a>WTS-05 | **Node is not a second business backend.** No Express/Nest API, Node agent loop, provider credentials or billing implementation is introduced. Static rendering during a build is permitted; request-time Node SSR and React Server Components are outside this baseline. |

**Source/configuration policy.** New TS/TSX/tooling source carries the applicable SPDX header. npm JSON manifests use their licence metadata; JSON cannot acquire invalid comment headers. Repository policy recognizes these formats explicitly. Shared .NET Directory.Build imports are conditioned on managed project type so esproj never inherits language/AOT/NuGet settings intended for csproj.

## 2. Monorepo paths

```text
ArcForges/
├─ ArcForges.slnx                       managed projects only
├─ win.slnx                             managed + Windows native + Web esproj
├─ native/                              existing CMake path on each platform
├─ contracts/
│  ├─ public-api/v1/openapi.json         committed generated compatibility baseline
│  ├─ browser-session/v1/openapi.json    C# browser-session adapter contract baseline
│  └─ realtime/v1/events.schema.json    C# event envelope/payload baseline
└─ src/Web/
   ├─ package.json                      private npm workspace; canonical commands
   ├─ package-lock.json                  only Web dependency lockfile
   ├─ .node-version                     exact Node patch
   ├─ .npmrc                            engine-strict and reproducible install policy
   ├─ ArcForges.Web.esproj               entire Web workspace in Visual Studio
   ├─ tsconfig.base.json                strict shared compiler settings
   ├─ ArcForges.Web.App/                 @arcforges/web-app
   │  ├─ package.json
   │  └─ app/                           shell + account/chat feature route modules
   ├─ ArcForges.Web.Site/                @arcforges/web-site; static deliverable
   │  ├─ package.json
   │  └─ app/                           public pages + versioned documentation
   ├─ packages/
   │  ├─ sdk/                           @arcforges/api-client; Apache-2.0
   │  │  └─ src/generated/              generated, ignored; never edited manually
   │  ├─ ui/                            @arcforges/web-ui; AGPL product UI
   │  └─ testing/                       fixtures, render helpers and test adapters
   ├─ tooling/                          typed Node orchestration and verification
   ├─ tests/                            TS contract/browser/visual suites
   └─ artifacts/                        ignored site/account/chat outputs and reports
```

The Site is a build-time static producer, not a second interactive account/chat application. The SDK has no import from product UI, private Cloud policy, persistence or local IPC; only public wire semantics and transport adapters enter its Apache boundary. C# browser-session implementation stays in `ArcForges.Cloud.PublicApi` and Identity, inside the single Cloud deployment.

### 2.1 Windows

| # | Rule |
|---|---|
| <a id="rule-wvs-01"></a>WVS-01 | **`win.slnx` includes `src/Web/ArcForges.Web.esproj` alongside its managed and native projects.** A focused Web solution filter may select the same esproj and Cloud dependencies. There is no duplicate source tree or duplicate browser application. |
| <a id="rule-wvs-02"></a>WVS-02 | **The esproj is a thin adapter over the workspace's npm commands.** `StartupCommand` is `npm run dev:account` by default; named account/chat/site startup profiles select the corresponding command. `BuildCommand` is `npm run build`, `BuildOutputFolder` is the workspace artifacts directory, `ShouldRunBuildScript=true` and `ShouldRunNpmInstall=false`. Set the Vitest test framework and `TestCommand=npm run test`; the test root is the Web workspace. |
| <a id="rule-wvs-03"></a>WVS-03 | **A single explicit restore runs `npm ci` at the workspace root.** The esproj restore target calls that command once; Build checks that the lockfile/toolchain install stamp is current and never silently runs `npm install`. All Web packages share this root, so parallel project builds cannot race on node_modules. |
| <a id="rule-wvs-04"></a>WVS-04 | **Cloud.csproj and portable .NET projects have no esproj ProjectReference.** The solution/startup profile supplies IDE composition. Publishing Cloud never builds or copies Web assets, and building an esproj never publishes Cloud. |
| <a id="rule-wvs-05"></a>WVS-05 | **F5 profiles launch Cloud plus the selected Web dev server exactly once.** Do not combine multi-project startup with SpaProxy's auto-launch. API forwarding targets a declared local endpoint, waits for health, and reports startup failure. Use separate HTTPS development hostnames for account and chat because cookies are not isolated by port. |
| <a id="rule-wvs-06"></a>WVS-06 | **Only approved local development profiles may relax certificate validation.** Release config contains neither a dev certificate, Vite dev/HMR server, localhost fallback nor `secure:false` proxy. Source diagnostics and test reports must be reachable from VS; esproj load/build success alone does not prove the product. |

The supplied `C:\Users\J7Rdm\source\repos\ReactApp2` template is evidence for the solution/esproj/Vite integration shape. Its floating packages, default install behavior, development proxy and server-to-esproj publish reference are not adopted as production policy. The JS SDK itself is pinned to the version verified in [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02); the inspected template uses `Microsoft.VisualStudio.JavaScript.Sdk/1.0.5984942`.

### 2.2 macOS, Linux and independent development

| # | Rule |
|---|---|
| <a id="rule-wcli-01"></a>WCLI-01 | **Open `src/Web` directly and use Node/npm.** No Visual Studio, esproj evaluation, .NET workload or CMake invocation is required to edit, typecheck, test or build Web from the committed contract baselines. |
| <a id="rule-wcli-02"></a>WCLI-02 | **Run each toolchain in its own directory.** Managed builds use the managed solution/project, native builds use CMake presets, and Web uses npm. CI composes their declared artifacts; Windows solution conveniences never become cross-platform prerequisites. |
| <a id="rule-wcli-03"></a>WCLI-03 | **Backend-free UI development uses generated-contract fixtures through MSW**, explicitly labelled test fixtures. The same screens switch to the real C# API via configuration. A fixture run cannot satisfy an API, payment, persistence or release gate. |
| <a id="rule-wcli-04"></a>WCLI-04 | **Portable npm commands have the same meaning from VS, shells and CI.** Implement orchestration in TypeScript with explicit child-process arguments and exit-code forwarding, not shell-specific commands, tracked ps1/sh wrappers, or an undocumented global CLI. Run typed tool scripts using the pinned TS runner; Node's built-in TS stripping is not assumed to handle every build script. |

| Workspace command | Contract |
|---|---|
| `npm ci` | Locked root install; no lock rewrite; record Node/npm and lock hash |
| `npm run contracts:generate` | Generate SDK and event validators from checked-in generated baselines; no running Cloud or registry access |
| `npm run contracts:verify` | Check deterministic regeneration and the input/output fingerprints; full CI additionally compares fresh C# export to the baselines |
| `npm run dev:site` / `dev:account` / `dev:chat` | Generate missing SDK output, select one route profile and start Vite; explicit fixture/real mode |
| `npm run typecheck` / `lint` | Generate required contracts, then check all workspace packages and import boundaries |
| `npm run test` / `test:unit` / `test:component` | Aggregate or select deterministic Vitest/RTL suites, isolated fixtures |
| `npm run test:contract` | Generated TS SDK against the declared real C# test host; no MSW interception |
| `npm run build` | Generate SDK, typecheck, lint and produce site/account/chat production artifacts in declared order |
| `npm run test:browser` | Playwright against production assets, edge headers/routing and real Cloud test deployment |
| `npm run verify` | Aggregate the applicable checks with retained reports; skipped external prerequisites fail a required gate |

These scripts are implementation deliverables, not claims that commands already exist. Only the C# contract-export job needs .NET; a Web developer uses the committed generated baseline until an API change requires a reviewed regeneration.

## 3. C# → OpenAPI → TypeScript

```text
Authored C# public DTOs + endpoint metadata + STJ converter policy
       ↓ build-time export in a network-free design-time host
OpenAPI 3.1 + JSON Schema 2020-12 + operation/security metadata
       ↓ compatibility diff against committed generated baselines
Pinned @hey-api/openapi-ts
       ↓
TS DTOs + Fetch SDK + Zod validators + TanStack Query options
       ↓
React account/chat application
```

| # | Rule |
|---|---|
| <a id="rule-wsdk-01"></a>WSDK-01 | **There is one authored wire definition.** Never hand-author matching TS DTOs, independent OpenAPI/TypeSpec/Fory schemas, or a React-only business API. Browser-session transport endpoints have their own C# metadata and share the existing Identity application services. |
| <a id="rule-wsdk-02"></a>WSDK-02 | **Export public APIs at build time without starting hosted workers, contacting providers, or reading production configuration.** The exporter registers the real endpoint/serializer metadata in design-time mode; its output contains no secret, internal operator endpoint or environment-specific hostname. |
| <a id="rule-wsdk-03"></a>WSDK-03 | **Committed schemas are generated compatibility fixtures, not a competing source of truth.** CI exports from the current C# tree and fails on unexplained drift; updating a baseline requires the compatibility declaration. TS generated source is regenerated, not checked in or edited. |
| <a id="rule-wsdk-04"></a>WSDK-04 | **Stable operationId, verb/path, success and error bodies/statuses, headers, auth alternatives, limits and nullability are exported.** Metadata from typed C# results and explicit endpoint declarations must include failures as well as the happy path. The TS SDK consumes the same contract semantics as generated C# clients. |
| <a id="rule-wsdk-05"></a>WSDK-05 | **Use the pinned Hey API Fetch, TS, Zod and TanStack Query generators against local files.** No hosted generation service or production API introspection. Unsupported schema constructs fail generation; never silently degrade a business payload to `any`. |
| <a id="rule-wsdk-06"></a>WSDK-06 | **Keep handwritten transport policy outside generated files.** Base paths, same-origin cookie credentials, CSRF header attachment, AbortSignal, timeout, bounded Retry-After and typed errors are in a small reviewed wrapper. Never retry an uncertain mutation with a new CommandId or change expectedRev automatically. |
| <a id="rule-wsdk-07"></a>WSDK-07 | **Validate incoming data at the boundary.** Generated validators preserve allowed additive response fields; unknown optional event/enum values degrade safely and trigger authoritative reread where required. Unknown required shapes fail as protocol errors rather than appearing as valid empty data. Server authorization/business validation is mandatory regardless of TS compilation or Zod success. |
| <a id="rule-wsdk-08"></a>WSDK-08 | **Public/browser APIs use HTTP/JSON.** Fory, MessagePack, protobuf/gRPC and tRPC are not introduced by this Web decision. Uploads/media remain separate binary/object transports with scoped resource authorization. |

### 3.1 Exact wire values

| Value | JSON and TS representation | C# implementation and required check |
|---|---|---|
| UUID/stable ID/cursor | String, opaque; validated format where applicable | Existing identity types; never infer ordering or parse a cursor |
| 64-bit revision, offset, sequence, token count, byte count, microcredits | Canonical decimal integer string; no exponent, plus sign or leading zeros; signedness/range follows the field | Explicit source-generation-compatible converter; schema string pattern plus documented range; TS uses BigInt only internally and converts back to canonical string |
| Money/rate decimal | Canonical base-10 string with the field's declared scale/range | Decimal converter and schema agree; exact decimal formatting/arithmetic where necessary, never Number coercion for accounting |
| Bounded int32 counter/enum-independent count | JSON number, finite integer in declared range | int32 constraints; no 64-bit value masquerades as this type |
| Time | Canonical RFC 3339 UTC string; duration uses an explicitly named unit | Date/time conversion only for display; no locale text in API requests |
| Optional vs nullable | Missing and explicit null are distinct where the C# contract distinguishes them | Patch presence is explicit; generation cannot turn both into an unconditional nullable property |
| Result/error/event union | Stable discriminator + typed payload | Match the C# envelope and compatibility policy; unknown response reason codes have a generic safe display |

| # | Rule |
|---|---|
| <a id="rule-wnum-01"></a>WNUM-01 | **Serializer output, OpenAPI and TS validators must agree on exact wire values.** Applying an OpenAPI transformer without changing the running serializer is a defect. Do not globally stringify int32 values by accident. |
| <a id="rule-wnum-02"></a>WNUM-02 | **Cross-language vectors include values above 2^53−1, the signed/unsigned 64-bit boundaries actually supported, nine-place pricing, null/omitted fields, unknown additive values and malformed payloads.** Test C#→TS and TS→C#, current/previous compatible clients, and real HTTP status/header behavior. |
| <a id="rule-wnum-03"></a>WNUM-03 | **A legacy numeric 64-bit wire field requires an explicit compatibility migration.** At the initial implementation freeze establish string encoding before production clients ship; if a deployed client already exists, add a versioned endpoint/contract and support its window instead of silently changing its field type. |

### 3.2 Realtime and streaming

| # | Rule |
|---|---|
| <a id="rule-wev-01"></a>WEV-01 | **Generate event DTOs and Zod validators from the C# realtime schema export.** Use the same pinned generator on an exporter-created schema wrapper if needed; the wrapper is generated and is not a runtime HTTP endpoint. Refit and STJ remain C# implementation details; TypeScript does not run a C# realtime client. |
| <a id="rule-wev-02"></a>WEV-02 | **SignalR uses its official JS client and JSON on the browser boundary.** Generated method/event names and payload checks prevent handwritten parallel event contracts. Connection hints do not authorize a tool, debit credits or commit a task. |
| <a id="rule-wev-03"></a>WEV-03 | **Reconnect, duplicate delivery, sequence gaps, authorization loss and polling fallback obey the existing realtime catalogue.** Browser SignalR is WebSockets-only with `skipNegotiation=true`; a blocked/failed upgrade falls back to bounded generated HTTP polling and range reads, not SignalR long polling. Periodic bounded authoritative catch-up also covers missed wakeups across Cloud replicas. Neither reconnect nor reload resubmits an AI command. |
| <a id="rule-wev-04"></a>WEV-04 | **Task output keeps its existing UTF-8 byte-offset contract.** JavaScript string length is not a byte offset; decoding must respect frame boundaries and bounded buffers. Completion/truncation/eviction/supersession and Task terminal state remain separate. |

## 4. Build, test and release closure

| # | Rule |
|---|---|
| <a id="rule-wci-01"></a>WCI-01 | **Full validation orders producers before consumers:** locked restores → C# metadata export → compatibility diff → TS SDK generation → TS check/lint/test → production builds → real API/browser tests → SBOM/attestation. A later export cannot validate an earlier build made from stale contracts. |
| <a id="rule-wci-02"></a>WCI-02 | **CI has separate managed, native and Web jobs.** Web changes run Node checks; C# public DTO/endpoint/serializer changes also trigger export and TS/browser contract jobs. Shared tokens, dependency locks, edge auth and deployment changes trigger the affected Web artifacts and browser tests. |
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
| [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) / [WP-04](../planning/work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) | C# schema/export baseline, exact primitive wire values, generated SDK foundation | [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-23](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23) |
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
- [ASP.NET Core OpenAPI](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-10.0?view=aspnetcore-10.0#openapi): C# generation of OpenAPI 3.1 and JSON Schema 2020-12.
- [Hey API generation](https://heyapi.dev/docs/openapi/typescript/get-started): local spec inputs, generated SDK/validation integrations, and the explicit need to pin its version during initial development.
- [SignalR JavaScript client](https://learn.microsoft.com/en-us/aspnet/core/signalr/javascript-client?view=aspnetcore-10.0) and [production scaling](https://learn.microsoft.com/en-us/aspnet/core/signalr/scale?view=aspnetcore-10.0): browser adapter and the WebSockets-only/skip-negotiation condition that avoids transport affinity; HTTP recovery remains authoritative.
- [shadcn/ui](https://ui.shadcn.com/docs), [Motion](https://motion.dev/docs/react): owned composable components and optional richer interaction.

These establish the selected mechanisms, not a completed production build. Exact package compatibility and security behavior remain implementation checks with the owners above.
