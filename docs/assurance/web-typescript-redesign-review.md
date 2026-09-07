# React/TypeScript Web Redesign — Stage 2 Review

> Status: **Design amendment reviewed**; implementation evidence remains open
> Reviewed on: 2026-09-07
> Layer: Assurance
> Authority: [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008), including the adopted [P2-003](../decisions/phase-2-specification-decisions.md#rule-p2-003)
> Baseline: design branch `design/phase-2-specifications`, parent `9833e84ddf9e81314efe04daaa8d4925d591729d`

## 1. Scope and result

This amendment replaces the Web technology throughout the current requirements, architecture, operation/schema design, monorepo/build plan and assurance obligations. The selected stack is React/TypeScript on Node.js/npm, with public contracts authored in C# and exported to OpenAPI/JSON Schema before generating the TS SDK. Windows uses one Web esproj inside win.slnx; other platforms use the same npm workspace independently of dotnet and CMake.

The work was planned, edited and reviewed in the existing design worktree. It does not implement React components, an esproj, authentication middleware or a running deployment in the product repository. Desktop Avalonia, MAUI mobile, the C# Cloud host and the subscription/single-Harness product scope retain their existing boundaries. The preserved input corpus is unchanged; old quoted decisions and inspected C# code observations remain history with explicit supersession.

The design amendment is complete at the review scope below. [PG-23](open-gates-register.md#rule-pg-23) remains an implementation gate. Its open state is not an undecided technology choice.

## 2. Evidence and review method

The local `C:\Users\J7Rdm\source\repos\ReactApp2` demo was inspected for its slnx, esproj, package manifest/lock, Vite configuration, ASP.NET project and launch profiles. It establishes a concrete Visual Studio integration pattern; it does not prove ArcForges behavior.

| Reference file | SHA-256 of inspected bytes |
|---|---|
| `ReactApp2.slnx` | `56FC97350CD7C563D883723C9A64B4700CFE3A0CD54BCEF32B47B86EDAE859FF` |
| `reactapp2.client/reactapp2.client.esproj` | `85046F943FE2F3B4F80A7F061F2CB666106E02AB795F075394A4F2664649B843` |
| `reactapp2.client/package.json` | `E18DDA1C19B6176A8D9B6FD323633F3A50465C31B1635DA004E8E1C51D9F1C0D` |

Current official documentation was checked for JavaScript SDK command properties, npm workspaces, Node support lifecycle, React Router static/client rendering, ASP.NET OpenAPI, TS generation and SignalR transport behavior. Links and their design implications are retained in [the toolchain specification](../architecture/25-web-toolchain-and-sdk.md#6-primary-references-checked-for-this-decision). Exact package versions still require the declared implementation manifest and compatibility proof; the demo's floating versions are not adopted.

Review followed each producer into its consumers: authority → requirement → architecture/operation/storage contract → work package/dependency → real test/release obligation. The scenarios below were checked against those layers, followed by full-corpus link/citation, package-graph and invariant-accounting checks.

## 3. Counterexamples checked and corrections made

| Case | Failure that had to be prevented | Final design and verification owner |
|---|---|---|
| 1. Two incompatible Web authorities | A future executor obeys the old Blazor/Node prohibition while implementing React | Dated decision amendment, effective scope/runtime tables and updated Web requirements; historical inputs/quotes preserved. [Web requirements](../requirements/products/arcforges-web.md), [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008). |
| 2. VS succeeds while portable builds break | Cloud.csproj imports esproj; generic Directory.Build properties impose .NET/AOT settings on JS; install races rewrite a lock | One workspace esproj, explicit root npm ci, no implicit install, managed-only portable solution and scoped properties. [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02). |
| 3. Frontend development secretly needs a running backend | SDK generation requires Cloud secrets/services or a globally installed generator | Committed generated schema baselines support Node-only work; full CI re-exports actual C# first and fails drift. [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03). |
| 4. JSON quietly loses billing/revision precision | A C# int64/decimal becomes a JS Number, or schema says string while runtime still emits number | Canonical integer/decimal string wire encoding with matching C# converters and generated validators; bidirectional boundary vectors and versioned migration if already deployed. [Exact-value rules](../architecture/25-web-toolchain-and-sdk.md#31-exact-wire-values). |
| 5. Browser auth accidentally exposes native credentials | React calls native token issuance, a sibling origin shares cookies, or JSON writes rely only on SameSite | Same-origin C# cookie adapter; browser edge excludes native bearer issuance/refresh; host-only cookies, explicit antiforgery and exact Origin; safe login/recovery projection. [Browser session architecture](../architecture/10-web-architecture.md#5-browser-session-architecture--p2-003-resolved). |
| 6. Concurrent authentication or revocation creates inconsistent state | A reused challenge creates another trusted session; a late idle update revives revoked state; a replica loses login authority | Bounded bound challenge rows, single transaction for flow/device/session, lowest browser trust, conditional activity updates, shared PostgreSQL and protected antiforgery keys. [Session model](../architecture/data-model/01-cloud-data-model.md#browser-session-storage), [WP-22.08](../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22.08). |
| 7. Shared session storage is mistaken for SignalR scale-out | Negotiate/long-poll requests switch replicas even though authentication is shared | Browser WebSockets-only with skipNegotiation; ordinary HTTP recovery on failure and periodic authoritative catch-up for lost cross-replica hints. No browser correctness dependency on affinity/backplane. [Realtime contract](../architecture/contracts/03-realtime-and-bridge.md), [WP-24.06](../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.06). |
| 8. C# streaming assumptions leak into TS | JS UTF-16 length is used as a UTF-8 byte cursor; reconnect repeats a paid turn; an old session's response repopulates a new account | Generated event contracts, bounded decoding/backfill, stable command identity, independent language adapters, scope cancellation and cache clearing. [Web toolchain](../architecture/25-web-toolchain-and-sdk.md#32-realtime-and-streaming), [WP-49](../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49). |
| 9. A framework change is mistaken for visual acceptance | Starter components ship with incomplete pricing/chat states, weak accessibility or heavy initial load | Owned tokens/components, approved representative layouts, all asynchronous states, locale/theme/narrow-screen checks and production budgets. [WP-47.07](../planning/work-packages/47-static-public-site.md#rule-wp-47.07), [Web visual requirements](../requirements/products/arcforges-web.md#62-consumer-visual-and-interaction-quality). |
| 10. Build/deploy changes invalidate the proof | Web is built before contract export, production uses Vite, stale HTML loses chunks, or rollback combines incompatible config/assets | Producer-first CI, no-script static output, versioned approved pricing input, profile artifacts built once, retained chunks, schema-bound public config and coherent edge/header rollback. [Build contract](../architecture/25-web-toolchain-and-sdk.md#4-build-test-and-release-closure), [WP-50.06](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.06). |
| 11. Architecture has no scheduled producer | Static Site starts before npm governance; browser account begins before its session adapter; runtime choices remain deferred | Dependency edge 02 → 47, browser producer in 22.08, shared design system in 47.07, generated SDK/event work in 03/23/24 and release proof in 50.06. [Sequence](../planning/implementation-sequence.md), [work-package index](../planning/work-packages/README.md). |
| 12. A green .NET build is called Web proof | Fixture screens, scaffolded projects or the old WASM gate substitute for production browser behavior | Separate TS unit/component/contract/browser suites; real C# + PostgreSQL flows, approved payment test environment, visual/accessibility/runtime evidence and both IDE/CLI paths. [PG-23](open-gates-register.md#rule-pg-23) cannot close on this document. |

The old C# Web project inventory now carries explicit replacement/retention actions. It was not relabelled as an implemented React application. Unrelated anchor additions were removed; applicable architecture rules and stable existing citations remain intact.

## 4. Coverage and verification

| Layer | Amended coverage |
|---|---|
| Authority and requirements | Effective Web/runtime/client scope, generated SDK, origin/session requirements and commercial visual acceptance |
| Architecture | Web application/static output; toolchain; solution/licence graph; public and realtime contracts; browser session/pre-auth storage and transaction family; security; deployment |
| Implementation | Foundation 01–06; Identity/API/realtime 22–24; Site/Account/Chat 47–49; release 50. Existing package identities retained. |
| Assurance | Test-family mapping, release obligations, code-inventory disposition, traceability and the Web implementation gate |

The existing [design repair verification](design-repair-verification.md) supplies the executable corpus checker and the baseline design counterexamples. Their source was extracted to a temporary directory; execution produced no product source changes.

```text
python check_design.py "<design-worktree>"
python design_counterexamples.py
git -C "<design-worktree>" diff --check
git -C "<design-worktree>" diff main -- docs/inputs
```

**Recorded result:** all checks passed.

| Check | Observed result |
|---|---|
| Complete corpus | 147 Markdown files; 9,928 local links, including 8,802 qualified rule links; zero missing files/fragments, duplicate stable anchors or checker-reported raw citations |
| Implementation sequence | 51 active work packages, each retaining its nine mandatory sections; 135 directed dependencies, symmetric index/header/dependency declarations and no forward dependency |
| Invariant accounting | 429 catalogue entries and the same 429 item-level coverage entries |
| Gate recount | 39 actual register rows, including the suffixed simulator gate: 5 design-closed, 33 implementation-open, 1 merged |
| Existing executable design counterexamples | 20 tests passed; these exercise the baseline design models, not a React/Cloud runtime |
| Scoped diff and preserved input check | git diff --check clean; git diff main -- docs/inputs empty; 52 edited plus 2 new Markdown documents, UTF-8/LF/final newline and no trailing whitespace |
| Read-only references | ArcForges implementation HEAD `ede43db5b2237104dd0008b99398090c54a2cf94` remains clean; the three template hashes above match the final reread |

No npm install/build, Visual Studio load/build, real C# browser authentication test, provider payment flow or Web deployment was run in this documentation task. Those are explicitly scheduled implementation evidence, not results of the structural checker.

## 5. Remaining implementation evidence

The register contains **39 entries: five closed on design evidence, 33 implementation-open including two dormant entries, and one merged entry**. There is no unresolved Web technology/deployment decision after this amendment. The future implementation must still establish exact tool versions, generate/build real outputs, exercise live API/session/commerce behavior, approve visual quality and prove release/rollback under [PG-23](open-gates-register.md#rule-pg-23). A later measured implementation defect is corrected through the existing evidence-driven revision process.
