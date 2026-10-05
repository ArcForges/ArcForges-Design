# [WP-03.90](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) owned artifact and real-integration receipt

Status: **[WP-03.90](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) verified for the Contracts-owned artifact** (delivery task [CON.19](../planning/delivery/lanes/contracts.md#task-con-19), claim epoch 2). This receipt records the exact source, producer release, candidate identity, provider reality and real-versus-fixture status required by [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) [§7](../planning/work-packages/03-contract-foundation-and-licence-split.md#7-tests-and-verification-evidence) and answers the [§8 completion gate](../planning/work-packages/03-contract-foundation-and-licence-split.md#8-completion-gate) items 1 to 6 under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). The [machine-readable receipt](wp03-90-implementation-evidence.json) mirrors it. The Contracts-side detail, including every stopped attempt, is [docs/wp03-90-verification.md](https://github.com/ArcForges/Contracts/blob/main/docs/wp03-90-verification.md) (Contracts PR [86](https://github.com/ArcForges/Contracts/pull/86)).

## Authority and verified source

| Item | Value |
|---|---|
| Source commit | Contracts `a6c5c02f349479ee2fc50a512285744753b5e61c` on `main` ([PR 85](https://github.com/ArcForges/Contracts/pull/85), merged at its approved head `69edd280918dd0c812717c8d15b7bca269b7f86c`), after CON.25 `1eb74c2` ([PR 83](https://github.com/ArcForges/Contracts/pull/83)) and PR 84 `cc5bc99` |
| Producer release | NuGet and npm `1.0.0-ci.320.1` (run number 320, attempt 1; log-derived from `Verified candidate contents: 1.0.0-ci.320.1`); Maven channel `1.0.0-SNAPSHOT`, snapshot `20261004.234018`, build 52 |
| Hosted run | [CI 37243548599](https://github.com/ArcForges/Contracts/actions/runs/37243548599): Build candidate, Verify, Publish NuGet, Publish Maven channel, Publish npm all `success`; [Security 37243548623](https://github.com/ArcForges/Contracts/actions/runs/37243548623): Secret scan and four CodeQL jobs `success`, Dependency review `skipped` on a push |
| Candidate archive | GitHub artifact 11318451913 `contracts-candidate-37243548599-1`, 159,794,187 bytes, `sha256:ed82448c4746263e70d662b953822dc09054a3d9499e534f985632e545667f82` as reported by the artifact API; the manifest inside it is the authority for per-package hashes and was not downloaded |
| Evidence and Maven receipt artifacts | `naming-evidence-37243548599-1` 11318935958 (`sha256:1642dec5…c36cc3d`); `maven-deployment-37243548599-1` 11318148847 (`sha256:b73d4dfe…b88f06`) |
| Planning inputs | Design [211](https://github.com/ArcForges/ArcForges-Design/pull/211) / Plan 263 (consumer-restore evidence form), Design 215 / Plan 270 and CON.25 (ConnectorService, LocalCallContext, af-segment records), Design [217](https://github.com/ArcForges/ArcForges-Design/pull/217) / Plan 279 and Design [219](https://github.com/ArcForges/ArcForges-Design/pull/219) / Plan 282 (consume-diagnostic repair paths) |

The first verification attempt (epoch 1, 2026-10-02, candidate `1.0.0-ci.287.1`, Contracts PR 75) concluded not accepted on four findings; each is resolved below.

## What was verified

| Condition | Result |
|---|---|
| §8 items 1 to 6 and independent vectors | Observed in the hosted Build candidate job at the candidate: 31 Apache project declarations; contract access (26 schema files, 1,320 contract types, 20 packages, no reclassification); foundation inventory (109 messages, 47 ID domains, 11 negative cases) and 362 independent C# and TypeScript cases; serialization policy (406 lock entries, 27 proto files, 69 catalogue services) and the Linux Native AOT probe (31 binary and 51 JSON vectors, 1,174 messages, 244 bound methods, no dynamic code); generation `--check` clean; 304 Node tests and 420 tooling tests passing; StructureTests lines for CON.02 and CON.05 to CON.25 |
| Operation scope | 335 registered, 0 pending, 7 reserved against the 342-row oracle (the six `connector.*` rows are registered) |
| Registry04 coverage | 297 operation rows = 252 authored + 38 in-process ports + 7 reserved Hub entries; 300 record names, 0 absent (`LocalCallContext` and the four Simulation records are authored; six reserved Hub records and four HTTP-schema records are not proto messages by design) |
| Compatibility matrix | Foundation and PublicApi against `1.0.0-ci.113.1`, plus the later-services window: ten pinned published descriptors, 20 previous-client/current-server and current-client/minimum-server legs, 13 closed JSON schemas, 0 errors |
| Provider receipts and registry metadata | 12 NuGet pushes (all 12 flat-container indexes list the version), 5 npm packages with signed provenance (registry `dist.integrity` prefix equals the publish log; `latest` points to the candidate), 3 Maven coordinates on the Sonatype snapshot channel; no payload download, hash audit or tag |
| Local opt-in consumer run | One `python eng/contracts.py consume` run recorded for the verified commit, from a fresh pack in a clean dedicated worktree at `a6c5c02`: C# (`HelloHost`, `HelloClient`) and TypeScript consumers restored, compiled and passed real gRPC and gRPC-Web success and error checks; the Kotlin consumer passed its identity checks, the CON.11, CON.22, CON.21, CON.24, CON.25 and CON.07 cases and the real Hello checks over gRPC-Web and gRPC; the command ended `Independent package consumers passed` |

## Real versus fixture status

| Obligation element | Status |
|---|---|
| Handwritten proto from the frozen first-version registry | Complete against Registry04; real authored schema |
| Public/internal split, Apache closure | Real build and static policy output |
| Generated C#, TypeScript and Kotlin artifacts | Real generation, compilation, packaging and publication with provider receipts |
| Profiles, independent fixtures, version metadata | Fixture. Vectors are declarative or shape-level; no owner handler, transaction, identity, service or runtime behavior runs |
| Remove C# to OpenAPI as business wire authority | Static policy evidence |
| Deterministic generation, compatibility, reserved-field checks | Offline static and codec checks |
| Three ecosystems restore actual candidate artifacts | Provider receipts and registry metadata for the original candidate, plus the local consume run from the locally packed candidate `1.0.0-ci.0.0`. The local run proves the clients restore, compile and pass their offline and loopback checks; it does not prove the bytes of the published packages |
| Private CF binding/event definitions | Mapped to CON.15; included in the candidate, not re-verified here |

Provider reality: nuget.org, npmjs.org (with provenance) and the Sonatype snapshot repository for the receipts and metadata; GitHub-hosted Linux for the build and security checks (ubuntu-latest, .NET SDK 10.0.400, Node 24.21.0, Python 3.14.7, Temurin 17.0.20). The local run used one Windows 11 workstation (.NET SDK 10.0.400, Node 24.20.0, npm 12.0.2, JDK 17.0.20.1, Gradle 9.7.1) with these recorded adaptations: relaxed Node and npm pin checks and `engine-strict` off, the Visual Studio Installer directory on PATH, the test-only `ArchitectureTests` assembly omitted from one build-identity inspection (it carries a build id twice on this workstation; hosted CI passes), and npm 12's `pack --json` output reshaped. The local run also exercised a Windows Native AOT publish and probe of the same source.

## Attempts and repairs

The consume diagnostic stopped four times before the recorded run completed, each on a defect of the Contracts consumer code rather than of a published candidate, and each is recorded with its path in the verification record: NU1506 from a duplicate `PublicApi` central version (`eng/consumer_tools.py`, PR 84); two server-streaming calls written as unary (`Con11ApplicationStreamsCases.kt`, PR 84); the Kotlin entry point requiring `ContractSet.values` of a module that has none (`Main.kt`), the repository-root lookup, camelCase name mapping and the encoded-body pair (PR 85). Each repair kept every vector and assertion, was validated only by an offline test and a local Kotlin leg, and was reviewed at its exact head. None of those validations is evidence for this receipt.

## Gate contributions and remaining owners

- [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009): the [WP-03.90](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) gate conditions (deterministic generation, compatibility and reserved-field checks, Apache closure, independent precise-value, error and profile vectors, three ecosystems restoring the candidate under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017)) pass on this one candidate closure, with the CON.15 parts as stated above.
- [VG-04](open-gates-register.md#rule-vg-04): the [WP-03.04](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.04) producer contribution (every local RPC interface carries generated identity, guarded by a policy test) is observed again; the gate stays open until the published-host RPC proof of package 06.
- [F-026](open-gates-register.md#rule-f-026): the [WP-03.02](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02) contribution is observed again, including a Windows Native AOT probe; the gate stays open until WP06.02 proves a real generated-client call in the published host and client AOT artifacts.
- Remaining owners: real runtime behavior of every operation (packages 04, 05, 06, 09, 21, 23, 30 and their owners), a Cloud runtime owner and the provider callback schema for `ConnectorService` (deferred by CON.25, not invented), and the later IM.* integration proposals.

## Untested coverage

Published package bytes and the candidate manifest hashes (not downloaded or compared); installed-package consumers in CI (prohibited by [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017)); the Native AOT C# client call and live snapshot consumer of `consume` (`--aot` and `--snapshot-registry` not requested); Kotlin vector behavior in hosted CI; the tooling suite on the local workstation; macOS; any live service, device, browser, GUI or real inference; operation runtime behavior. The candidate's `1.0.0-SNAPSHOT` Maven label is mutable and is bound to the candidate only through the receipt and timestamp.

## Review boundary

This Design contribution follows complete review with JSON, link and consistency checks; the repository has no configured CI. Post-merge verification is limited to the expected merge commit and a clean primary fast-forward.
