# WP02.03 runtime and directory boundaries

Scope: [WP02.03](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.03), the [ordered execution plan](wp02-03-runtime-boundary-profile.md), and the owner-local build/runtime contracts. This closes the foundation runtime/entry-point boundary step only. Functional WP03/06 proof and complete commercial application acceptance remain separate obligations.

## Reviewed change and identities

[Design PR 50](https://github.com/ArcForges/ArcForges-Design/pull/50) established the complete plan before source edits, merged as `04d3e4e692aaa272064dd8e1765ddeae29ef5457`. [Web PR 8](https://github.com/ArcForges/Web/pull/8) was fully reviewed at `8aae6b48d6ecb4c1768505d8fcdae5676ff1814c` and merged as `6678e12cf3c71f5c8be04b4b3b5f4cc3aefacf81` after every applicable check passed, including the separate CodeQL scanning result. The reviewed and merged Git trees are identical. Primary Web was pulled with fast-forward only.

The Web solution now explicitly selects its esproj for Build and local IDE Deploy. Explicit solution Restore runs root `npm ci --ignore-scripts`; Build and design-time evaluation do not install. A Windows CI verifier requires actual npm dispatch and a verified candidate, checks lock stability and effective build/start properties, and retains logs. The local IDE profile launches installed Chrome against the same portable development command at strict loopback port 5173. The development guide documents the browser prerequisite and the difference between local IDE Deploy and Cloudflare promotion. No dependency version, package identity or browser provenance oracle was changed.

The eight-file change is confined to Web: `win.slnx`, `ArcForges.Web.esproj`, `.vscode/launch.json`, `apps/site/package.json`, `tooling/ide.ts`, `.github/workflows/ci.yml`, `eng/provenance/files.json` and `docs/development.md`. Source worktree/branch `Web/.worktree/wp02-03-runtime-boundaries` / `codex/wp02-03-runtime-boundaries` is retained. Design retains its plan worktree and `.worktree/wp02-03-runtime-acceptance` / `codex/wp02-03-runtime-acceptance` receipt worktree.

## Actual entry-point verification

Local verification used Visual Studio `18.10.1`, JavaScript SDK `1.0.6578810`, .NET SDK `10.0.401`, Node `24.21.0` and npm `11.19.0`.

- The full source check passed: policy, provenance, formatting, lint, strict typing, 22 unit tests and 53 provenance tests. The local production candidate passed 18 Chromium/Firefox/WebKit tests; the wire-fixture case remains labelled as a fixture.
- Actual solution Restore/Build succeeded. Lock hashes remained stable, installed dependency metadata was unchanged during Build, and design-time Restore did not invoke npm install. Effective Web AOT properties are empty and ProjectReference is empty. The SDK's internal target-framework plumbing does not produce a .NET application.
- Disabling the solution's Build selection caused the verifier to reject skipped restore dispatch. An occupied port 5173 caused the development server to fail instead of selecting another port. The negative probe restored the exact original solution bytes; the final positive verifier passed again.
- Actual `devenv /Run` loaded this solution, built it and started JavaScript debugging. DTE reported the expected solution/startup project and `DebugMode=3`; the IDE output recorded the Vite connection. An independent Chromium interaction against that IDE-started server entered a name and received `Hello, IDE verification!`. This is actual IDE startup evidence, distinct from direct MSBuild dispatch. Debugging was stopped and the owned server was no longer listening after cleanup.
- The initial Edge profile failed because Edge was absent. The existing Chrome installation resolved that concrete failure without installing software. The successful rerun, not the initial error, is the acceptance evidence. The plan's execution note records this browser selection correction.

## Unchanged owner boundaries

The [machine-readable receipt](wp02-03-runtime-boundary-evidence.json) records fresh remote/main identity checks and owner-local solution/ProjectReference inventories. DesktopPlatform, Contracts, ArcNotes, ArcScope, ArcSlate, Cloud, AI and Mobile remain clean at the exact previously accepted commits. All managed solution entries and project references stay within their owning repository. Cloud's three managed projects contain no Web, Mobile or native solution target. Products consume pinned packages without sibling product source.

The unchanged [WP02.02 sweep](wp02-02-aot-sweep-evidence.md) supplies effective properties for all 43 managed projects and the 31 AOT analysis postures, six complete builds, Windows desktop/helper Native AOT execution, isolated public Contracts consumption and Linux Cloud Native AOT execution. Its JSON hash is bound here. The [WP02.01 receipt](wp02-01-implementation-evidence.md) supplies the same-commit non-Windows CI/runtime evidence, five desktop RIDs, Kotlin/Gradle Android devices and real TypeScript AI/Cloud deployment. These unchanged owner runs were not relabelled as fresh rebuilds. Fresh Web Linux CI independently exercises portable npm without Visual Studio. No CMake/vcpkg reinstall or replacement Maven publication occurred.

The first consolidated foundation integration manifest remains WP06-owned under the staged producer contract. Existing exact producer versions and candidate identities remain intact. This step creates no new business API, session, billing flow, native capability or shared application host.

## Merged candidate and public delivery

[PR CI 35584520972](https://github.com/ArcForges/Web/actions/runs/35584520972) and [main CI 35585002760](https://github.com/ArcForges/Web/actions/runs/35585002760) passed all applicable jobs. Main repeated the actual Windows solution verifier and portable Linux checks, passed 18 candidate browser tests, deployed the original tested artifact without rebuilding, and passed 15 live domain tests. The separate main CodeQL result also passed.

The [public prerelease `web-0.1.0-ci.24.1`](https://github.com/ArcForges/Web/releases/tag/web-0.1.0-ci.24.1) identifies the exact merge source. Its archive SHA256 is `dce9847910106b07efdaaaf869fed25f28a8431855218649e32fc1a955de2322`. All 50 archive members, including the manifest and its 49 sealed files, match the downloaded original CI candidate byte-for-byte. The owner verifier accepted that downloaded candidate with the expected merge SHA. Independent public delivery reads matched all 21 directly served asset hashes. The release deployment receipt reports the same version/source and successful real-domain verification.

Independent Chromium, Firefox and WebKit sessions then opened the deployed connection page and clicked its button. Each made a real same-origin binary gRPC-Web request, received HTTP 200 and a 45-byte protobuf/trailer response, and displayed `Hello, ArcForges!` without page errors or route interception. This verifies the existing deployed Cloud Hello boundary, not future authenticated business behavior. Cloud remains at its unchanged accepted source identity.

The first independent probe incorrectly demanded a response `+proto` suffix. The actual response is `application/grpc-web`, which [the gRPC-Web protocol](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md) defines as default protobuf. The corrected probe accepts only the binary media type with an optional explicit protobuf suffix; all three real calls passed. Python urllib asset requests returned 403 on the recorded attempts; the browser-context request client successfully verified those same public bytes. Neither unsuccessful probe is reported as a pass or used to weaken a product requirement.

**Result: WP02.03 passed. No external prerequisite is unavailable.** This receipt closes the runtime/entry-point boundary step. Version-axis plumbing remains WP02.04; no later substep is implemented by this change.
