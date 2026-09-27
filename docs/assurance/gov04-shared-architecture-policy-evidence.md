# GOV.04 shared architecture policy evidence

Status: source merged after all retained CI passed; normal main publication and final assurance/ledger acceptance remain pending. This draft does not record completion.

Claim: GOV.04 epoch 1 (w-20260927-dgov). Source: [DesktopPlatform PR67](https://github.com/ArcForges/DesktopPlatform/pull/67), reviewed head `2e180f7826ef9cae0b679db7d10459e51027d4b2`; independent full/delta review [5860461159](https://github.com/ArcForges/DesktopPlatform/pull/67#issuecomment-5860461159). Final whitespace-only delta approved [5860492140](https://github.com/ArcForges/DesktopPlatform/pull/67#issuecomment-5860492140). Packaging-delta approval [5860560182](https://github.com/ArcForges/DesktopPlatform/pull/67#issuecomment-5860560182) binds the final source. Producer scope was accepted by Design PR85 and Plan PR48.

## Producer and owning graph

The existing `ArcForges.Build.Policy` package contains a single shared C# engine under `tools/architecture`. Consumers explicitly source-link `ArchitecturePolicy.props` in an offline test/build host with PrivateAssets; normal package imports add no architecture hook, package identity or runtime dependency. DesktopPlatform tests compile that same source. Fixture compilation uses its selected SDK Roslyn binaries, with no new Roslyn NuGet dependency.

The owning gate evaluates all 19 actual MSBuild projects, actual Compile/ReferencePath/project edges and restored package closure, including generated compiler sources and BeforeCompile inputs. Every solution/runtime-owned project is classified explicitly. 117 method-to-contract-test mappings bind real public methods to actual Xunit Fact/Theory methods in an owned test project. Cross-project same-name types cannot mask a production API. Native input reuses the existing same-source CMake configure receipt and its target types/dependencies; only the explicitly marked existing test executable is nonproduction. Production dependencies on test-only targets fail.

Canonical naming uses the existing admitted `ArcForges.Contracts.Validation/1.0.0-ci.129.1` package once, including six negative forbidden-alias fixtures. Secret evidence reuses the existing Gitleaks job. Joined evidence requires the exact source commit, workflow run and attempt; stale/missing/failing results fail closed. No duplicate secret scan or fabricated local successful receipt is used.

## Positive/negative fixture coverage

Every row below is exercised by the same-engine `EveryRuleAcceptsItsValidFixtureAndRejectsItsViolation` test; the positive fixture must pass and the changed negative fixture must fail its specific rule.

| Rule | Positive fixture | Rejected negative |
|---|---|---|
| AT-01 | Domain depends on abstractions | Infrastructure project edge; additional Domain/Application package-layer negatives |
| AT-02 | Local adapter depends on abstractions | UI project dependency |
| AT-03 | Public adapter depends on abstractions | UI project dependency |
| AT-04 | Contracts depend on Foundation | Native adapter dependency |
| AT-05 | Other-owner abstraction | Other-owner domain dependency |
| AT-06 | Managed integer boundary | Raw pointer return; delegate pointer/SafeHandle signatures |
| AT-07 | Same-module persistence | Other-module persistence |
| AT-08 | Typed local RPC argument | Untyped object argument |
| AT-09 | Nonproduction native test target | Production native executable; production-to-test dependency |
| AT-10 | Reviewed safe HTTP fixture | Refit runtime dependency |
| AT-11 | Generated canonical RPC base and application port | Missing port mapping |
| AT-12 | Generated wire type bound to owned schema hash | Authored ungenerated wire type |
| AT-13 | Cross-module abstraction | Cross-module infrastructure |
| AT-14 | Shared Shell depends on Foundation | Product domain dependency |
| RP-01 | Passing exact naming evidence | Failing naming evidence |
| RP-02 | Correct SPDX boundary declaration | Empty licence |
| RP-03 | Apache-to-Apache edge | Apache-to-AGPL edge |
| RP-04 | Permitted MIT mobile package | GPL-only mobile package |
| RP-05 | Central package management and locks | Central management disabled |
| RP-06 | Exact admitted toolchain hash | Changed global.json |
| RP-07 | Preserved diagnostics | Trim diagnostics suppressed |
| RP-08 | Passing exact alias evidence | Failing alias evidence |
| RP-09 | Passing exact secret evidence | Failing secret evidence |
| RP-10 | Public API mapped to actual contract test | Missing mapping; Trait-only/non-test owner rejected |

Seven semantic banned-symbol categories have compiled positive/negative examples: reflection on AOT paths, dynamic code generation, blocking waits on async paths (including nested lambdas/local functions and configured awaiters), direct provider SDK calls outside adapters, content/secret logging, floating-point money arithmetic and raw pointer fields. Additional tests cover semantic aliases/static imports, native stale/unclassified receipts, unresolved compilation rejection, and managed/recursive delegates without false pointer classification. Exact owned expiring exceptions are supported; current production exception list is empty.

## Observed validation

- Local SDK 10.0.401 was invoked directly using ignored invocation-only compatibility targets fixed to ILLink/ILCompiler 10.0.11; `global.json` remains 10.0.400 and exact .400 CI is authoritative. Full Release solution build passed with zero warnings/errors.
- Final shared semantic suite: 58/58 passed. Two compiled public-boundary contracts and 65 Foundation tests passed during the source work. Evidence adapter tests: 11; runtime ownership: 23; licence: 12, including canonical positive/six negative naming checks.
- Actual local evaluation reconstructed all 19 compilations without source errors. The complete graph deliberately failed only absent hosted naming/secret and native receipts. This is not a claim that the full local graph passed.
- Dependency admission: 33 NuGet and 10 Python packages, 201 inputs; source provenance: 412 files/139 records. Seven-owner reconciliation passed after refreshing the actual native CMake project blob. Historical admission/provenance records are unchanged.
- [All 12 retained exact-head CI checks in run36356489836](https://github.com/ArcForges/DesktopPlatform/actions/runs/36356489836) passed, including 67 architecture tests, 65 Foundation tests, native compilation and exact package-content verification.

No toolchain provisioning, macOS CI, hosted GUI/device/browser/live-service/inference, native execution or installed-consumer test was introduced. This producer acceptance does not close policy adoption in the other six repositories, GOV.13 accounting, GOV.14 specification integrity or GOV.15 stage acceptance.

The prior exact-.400 CI at source `4187ed3` passed all 67 architecture tests (including the real complete owning graph) and 65 Foundation tests. The package verifier then rejected an incorrectly nested architecture import. The explicit None item fix was locally packed and all seven architecture asset paths were confirmed; `gov04-r2` records this binding correction without changing any dependency closure or required-content allowlist. The later exact-head source CI passed as recorded above.

## Final delivery receipt

Source merged at `8cb04f44116b5e77f7c3c54d58d89ac5b4ab78bc` after rechecking GOV.04 epoch 1, DesktopPlatform integration epoch 2 and exact reviewed head `2e180f7826ef9cae0b679db7d10459e51027d4b2`, using --match-head-commit. The clean primary checkout was fast-forwarded. [Normal main publication run36356901718](https://github.com/ArcForges/DesktopPlatform/actions/runs/36356901718) completed successfully with all 14 jobs, including [publish job108727298811](https://github.com/ArcForges/DesktopPlatform/actions/runs/36356901718/job/108727298811). The provider log records successful pushes of the original candidate at `1.0.0-ci.30.1`, including `ArcForges.Build.Policy`.

Original uploaded candidate metadata: `nuget-candidate-36356901718-1`, artifact ID `10943693370`, provider digest `sha256:0f14cbc65befe6692c6c0640d873ddd7ab3b547a8eb3b554056c8c1cea172ec0`. Joined owning-gate evidence: `architecture-gates-36356901718-1`, artifact ID `10944760069`, provider digest `sha256:6ae372559a221d386960057933fca6beac5a6904b1fcc193c1f3ced35d417a40`. These are provider artifact identities, not individual NuGet package hashes.

Post-merge verification used merge/job/publication status and provider metadata only. No public archive was downloaded and no runtime/consumer cycle was repeated. Final assurance and ledger receive independent exact-head review before task completion.
