# WP02.00 toolchain pins and locked restore evidence

Scope: [WP02.00](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.00), under the reviewed [toolchain profile and ordered plan](wp02-00-toolchain-profile.md). The plan was merged in [Design PR45](https://github.com/ArcForges/ArcForges-Design/pull/45) before implementation. This receipt closes toolchain pin/restore work only; the remaining WP02 substeps and commercial product acceptance remain separate.

## Changes and review

All eight implementation PRs were reviewed in full and merged after every applicable PR check passed. Their main publication and runtime checks also passed. Primary checkouts match remote main; implementation branches and worktrees remain available. Exact commits, check URLs, lock hashes, local log hashes and public/runtime receipts are retained in the [machine-readable evidence](wp02-00-implementation-evidence.json).

| Owner | Reviewed PR | Main commit | Main verification |
|---|---|---|---|
| DesktopPlatform | [55](https://github.com/ArcForges/DesktopPlatform/pull/55) | `14f4c5c2b9243dfafa54dee0fc65f6d9ce22d3cb` | [35560603400](https://github.com/ArcForges/DesktopPlatform/actions/runs/35560603400) |
| Contracts | [28](https://github.com/ArcForges/Contracts/pull/28) | `e8353720af5d61c462c3b550e46620dddb445ae9` | [35560943991](https://github.com/ArcForges/Contracts/actions/runs/35560943991) |
| ArcNotes | [5](https://github.com/ArcForges/ArcNotes/pull/5) | `c40116ac8ae0c76e539b3c19552a65ec08c8d94b` | [35560953892](https://github.com/ArcForges/ArcNotes/actions/runs/35560953892) |
| ArcScope | [5](https://github.com/ArcForges/ArcScope/pull/5) | `1b13c9827f98578c8ba2f7db0c046db114aa7cb8` | [35560962880](https://github.com/ArcForges/ArcScope/actions/runs/35560962880) |
| ArcSlate | [5](https://github.com/ArcForges/ArcSlate/pull/5) | `0cc8093d51cdef20bae8057e77c4bcd80d32b39e` | [35560972674](https://github.com/ArcForges/ArcSlate/actions/runs/35560972674) |
| Cloud | [6](https://github.com/ArcForges/Cloud/pull/6) | `4f53ed6a072cc9680101633e8c7e01efd450b84e` | [35560981353](https://github.com/ArcForges/Cloud/actions/runs/35560981353) |
| AI | [11](https://github.com/ArcForges/AI/pull/11) | `b50098108cdabdd3d0bdefc44e724c71aba2b0a6` | [35560988965](https://github.com/ArcForges/AI/actions/runs/35560988965) |
| Mobile | [6](https://github.com/ArcForges/Mobile/pull/6) | `f067f3447708ae2e62c334653a8dd4d544980032` | [35561935091](https://github.com/ArcForges/Mobile/actions/runs/35561935091) |
| Web | Validation only; no source change | `84939ca1fde0f0653d2cb4d8b8f9e5dd1057abb5` | Existing [35437014881](https://github.com/ArcForges/Web/actions/runs/35437014881), supplemented by the local checks below |

The inventory contains **43 managed projects and 43 NuGet locks**, plus **four root npm locks** owned by Contracts, Cloud, AI and Web. DesktopPlatform/Contracts retain .NET SDK `10.0.400`; other managed owners retain `10.0.401`. Node/npm remain `24.21.0`/`11.19.0`. ArcNotes, ArcScope, ArcSlate and Cloud now enable central transitive pinning; their resolved dependency graphs did not change. AI and Cloud check the executing Node/npm patches. Contracts and Mobile CI repeat Gradle resolution offline; Contracts also repeats npm restore offline.

DesktopPlatform now pins Python `3.14.7`, pre-commit `4.6.0` and its complete ten-package dependency closure with archive hashes. Contracts/Cloud CI select Temurin `17.0.20`; Mobile selects `21.0.12`. Hosted setup/build logs establish availability: Contracts ran `17.0.20+1` on Linux and `17.0.20+101` on Windows; Mobile ran `21.0.12+1` and `21.0.12+101.0`, respectively. Compatible existing local JDKs were reused and are identified separately in the JSON receipt. Bytecode targets, generated bindings, native baseline and publication channels remain unchanged.

The Cloud central-property change required a new immutable release profile and superseding provenance records. Mobile's required release lint identified the published Contracts `1.0.0-ci.60.1` update. The six Maven JAR/POM/module inputs were independently checked against their public bytes. Compared with the previous `ci.54.1` package, class/schema bytes are unchanged; NOTICE version strings, source identity and SBOM change. The catalog, generated locks/checksums and superseding legal/resource records were updated together. Archive expectations came from reviewed inputs and the verified previous public AAB before replacement construction. Historical profiles remain intact and release lint remains enabled.

## Local and negative verification

Clean source worktrees performed locked online restores; NuGet/npm used isolated caches. Offline repeats used actual package-manager offline or source-isolation modes. The empty-source NuGet proof alone disabled vulnerability auditing; ordinary online/CI auditing remained enabled. Python passed a fresh hash-checked environment install and an offline install from downloaded wheels.

| Owner | Executed local verification |
|---|---|
| DesktopPlatform | Managed build; 5 architecture, 63 engineering and 41 tooling tests; formatting/provenance/pre-commit; native Windows build with zero warnings/errors and one ABI test |
| Contracts | Locked regeneration without drift; 92 tooling tests; independent C#, TypeScript, Kotlin and Native AOT consumers of the main candidate; live Maven Snapshot restore |
| Each desktop application | Locked/offline restore, Release build, formatting/provenance and 89 tests |
| Cloud | 67 tooling and 5 managed tests; actual Linux AOT container through existing WSL Docker; .NET/TypeScript/Kotlin protocols and restart checks |
| AI | Complete npm check, including 82 tooling tests and Worker/Workflow bundle checks; separate real inference evidence below |
| Web | Complete npm check including 53 provenance tests; verified build candidate; 18 Chromium/Firefox/WebKit E2E tests; direct esproj dispatch with zero warnings/errors |
| Mobile | 49 tooling tests; shared/app tests; release lint; actual APK/AAB construction and source/resource/legal/bytecode verification |

**Local native dependencies were reused.** The existing vcpkg installation and already installed dependency tree compiled successfully with `VcpkgManifestInstall=false`. No vcpkg reinstall or native dependency rebuild was performed. Local compatible binaries are not represented as the reviewed CI producer closure; ordinary application consumers still restore packaged native artifacts.

Negative checks rejected a stale NuGet central selection (`NU1004`), missing npm lock membership (`EUSAGE`), incorrect executing Node/npm patches, an altered Python wheel hash and an altered published Maven JAR checksum. Existing engineering/tooling guards also rejected native baseline/closure drift. Temporary negative mutations were restored; all retained source worktrees are clean.

Web's direct `ArcForges.Web.esproj` build executed npm and produced its verified candidate without implicit npm installation. CLI MSBuild of `win.slnx` skipped the esproj; that invocation is **not** accepted as solution/IDE execution evidence. Full solution/IDE entry-point verification belongs to WP02.03. No empty Web PR was created.

## Published artifacts and actual runtime checks

- **DesktopPlatform `1.0.0-ci.18.1`:** ten public NuGet packages were independently downloaded. Every original archive member matches the tested candidate; only the registry-added signature is excluded. The exact main candidate passed five isolated JIT/AOT cases, C17 calls and four negative loader cases.
- **Contracts `1.0.0-ci.67.1`:** all original public NuGet members match, both npm tarballs are byte-identical, and all twenty Maven files at snapshot timestamp `20260921.043550-2` match the candidate. Maven remains `1.0.0-SNAPSHOT`; formal Central publication still requires an explicit release tag. The local independent consumer uses empty package caches, a local feed for verified NuGet/npm candidate archives, and the live Sonatype Snapshot repository for Kotlin. C# gRPC, TypeScript binary gRPC-Web, Kotlin gRPC/Connect and Native AOT calls passed. This is not a claim that NuGet/npm consumer restore used their remote registries.
- **ArcNotes/ArcScope/ArcSlate `0.1.0-ci.10.1`:** all fifteen public archives across five RIDs match their candidate receipts. Hosted native UI/live Cloud/error-path checks passed for each RID. Those receipts retain the older Cloud revision actually observed (`4571ec8â€¦`); they are not relabelled as calls against the later deployment.
- **Cloud `0.1.0-ci.20.1`:** the actual deployed Native AOT image at revision `4f53ed6â€¦` passed public Worker-boundary TypeScript/Kotlin binary gRPC-Web, Unicode, invalid-argument, resource-exhaustion and wrong-prefix checks. The receipt retains image and registry digest identities.
- **AI `0.1.0-ci.28.1`:** the deployed Workflow made two actual Workers AI calls to `@cf/openai/gpt-oss-20b` and executed the `say_hello` tool. This provider evidence is separate from mocked local tests.
- **Mobile `0.1.0-ci.16.1` / code `1601`:** both API 26 and 36 independently downloaded and verified the public signed package, upgraded from code `901` with the same certificate, UID and first-install identity, and invoked real Cloud from the minified APK. APK/AAB hashes, certificate fingerprint and upgrade receipts are retained.

Transient TLS failures interrupted local verification. One retry also failed during loopback HTTP/2 verification; the attempt was superseded by a successful run with no source change. The failed attempts remain identified separately in the log inventory. Retries reused the same published candidates; no replacement release or manual publication was used to recover. No unavailable external prerequisite remains for WP02.00. These foundation probes do not establish later business workflows, production/store promotion or complete commercial readiness.
