# WP01.01 implementation evidence

Scope: [current contract split assignment](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.01), under the [contract access profile](wp01-01-contract-access-policy.md). This receipt closes current type assignment and dependency consistency. It does not assert completed production schemas or product behavior.

## Authority and implementation

[Design PR34](https://github.com/ArcForges/ArcForges-Design/pull/34), merge `94b3ec43389d8ec6f8cd3ad277daf0eac5e9259e`, defined the current-source assignment, closed inventory and compiled dependency requirements before implementation. Both public and internal sets use Apache-2.0; access restrictions remain distinct from licence identity.

[Contracts PR25](https://github.com/ArcForges/Contracts/pull/25), reviewed head `6ee078e6551818f966e9570ef26eb182edd3c83c`, merged as `ef9e0aa9d90d47ff8355dc38b037fd5860b4476c`. The complete reviewed diff SHA256 is `d318d9b13d830deab4029a39a1aac30293696d9d02518d2996fc246990b3b6cb`. All 11 applicable PR checks passed in [CI](https://github.com/ArcForges/Contracts/actions/runs/35542065514) and [Security](https://github.com/ArcForges/Contracts/actions/runs/35542065498); the three publication jobs correctly apply only to main pushes. Full local and remote diff review left no outstanding findings.

The eight-file change adds `eng/policy/contract-access.json`, `eng/check_contract_access.mjs`, ten test groups and implementation documentation; it connects the gate to build/pack and CI and registers the new files in provenance. Authored schemas, generated distribution bytes, package identities, dependency locks and consumer pins are unchanged.

## Assignment and enforcement

| Boundary | Verified result |
|---|---|
| Authored protocol | `SayHelloRequest`, `SayHelloResponse` and `HelloService`: all three definitions assigned public Apache-2.0 |
| Distributed source | All 18 files, including 15 generated and three authored files; all 34 declared source types assigned to seven public packages |
| Package graph | All 24 current package graph input files closed and hash-bound |
| Reclassification | No current public type requires internal reassignment; no current internal type requires public reassignment |
| Dependency direction | Compiled descriptor file imports, nested definitions, message/enum references and RPC input/output closures reject public-to-internal dependencies; internal-to-public reuse is allowed |

The policy SHA256 is `82d1ff075cb907cc87a4c4ef44fbfc4f36efefc3a30a446a3cb4c0e18a3407cc`. Unknown or missing schema/source/package assignments, hash drift, unsafe paths and linked source fail closed. Real protoc fixtures cover direct, transitive and unused private imports, nested assignment omissions, invalid references and both dependency directions. Source-language declarations use a bounded lexical inventory backed by exact source hashes and mandatory regeneration; it is not a general whole-program analyzer. Generated private helper visibility does not reclassify the wire contract. Extension declarations require a reviewed future profile.

## Verification and published candidate

Local validation passed: ten access test groups, 85 existing tooling tests, locked restore, unchanged regeneration, Release build with zero warnings/errors, three npm wire tests, Gradle assemble/check, full candidate packing, naming, provenance and formatting. An initial premature tooling run lacked its package/JDK prerequisites; after the package completed and the pinned JDK was configured, the complete 85-test run passed. No test was removed or weakened.

Local Windows and PR/main Linux and Windows isolated consumers passed C# gRPC, TypeScript gRPC-Web, Kotlin gRPC, Kotlin Connect gRPC-Web/gRPC and Native AOT success/error calls using empty caches and candidate archives outside the repository. PR tests used `1.0.0-ci.59.1` at synthetic merge `4372e1f639d60b864bae61e71ea6d369acf6d304`; local precommit tests used `1.0.0-ci.0.0`. Neither is substituted for the final main candidate.

[Main CI](https://github.com/ArcForges/Contracts/actions/runs/35542448605) and [main Security](https://github.com/ArcForges/Contracts/actions/runs/35542448598) succeeded on the merge. Candidate **`1.0.0-ci.60.1`**, manifest SHA256 `b79fc213994cdd4ef261d08d41407c32027252d0df334804f488d703a0bbb6dc`, passed both main consumers before publication. Downloaded access reports matched the policy hash and clean merged commit.

Public registry verification passed: all **13 original NuGet ZIP members** match (only registry-added `.signature.p7s` excluded), both **npm tarballs** are byte-identical, and all **20 Maven candidate files** are byte-identical. Exact candidate and public hashes, consumer identities and reports are in the [machine-readable receipt](wp01-01-implementation-evidence.json). Initial 404s were retried without overwriting versions.

Maven attempt 1 remained `PUBLISHING` for over 20 minutes. At the user's request it was cancelled, its deployment receipt retained, and only the failed Maven job retried. Attempt 2 resumed deployment `69143abb-d8f5-40d3-b9fe-bc030561be28` and reached `public-bytes-verified`. No candidate rebuild or duplicate upload occurred. Future Maven runs in this execution use the requested ten-minute cancellation/retry threshold, preserving deployment identity. The [official status page](https://status.maven.org/) reported no incident when checked on 2026-09-20; actual deployment/public-byte evidence governs acceptance.

A fresh read-only nine-owner reconciliation after the merge passed: 75 current projects, 166 historical entries, 359 directory dispositions and seven historical native entries. Other owner project graphs and published consumer pins remain unchanged.

## Retention and remaining scope

Retained worktrees under each repository's `.worktree/`: Design `wp01-01-contract-access-policy` and `wp01-01-completion-evidence`, Contracts `wp01-01-contract-access`; branches use the corresponding `codex/` names. Contracts primary and implementation worktree were fast-forwarded after merging. Design primary is synchronized after each documentation merge.

No unavailable external prerequisite remains for WP01.01. No new browser or Android device run was needed for this policy-only change; the consumer reports explicitly mark those scenarios as not run. Full public/internal/operator/local/AI production schemas and generated packages remain WP03. Shared-foundation review and later reconciliation steps remain separate obligations, and Hello compatibility probes do not establish commercial readiness.
