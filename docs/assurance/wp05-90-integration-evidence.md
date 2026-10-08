# WP-05.90 cross-repository integration evidence

> **SUPERSEDED IN PART (2026-10-08)** by [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021): the React/TypeScript, Node/npm, Kotlin/Maven/Gradle and Blazor/MAUI toolchain statements. The recorded result is retained as dated history and is not rewritten.

Authority: [WP-05.90](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.90), [staged producer integration](../planning/README.md#staged-artifact-integration) and [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). Task: [GOV.15](../planning/delivery/lanes/governance.md#task-gov-15). The [stage acceptance](wp05-stage-acceptance.md) joins this record with the ten preceding GOV.04-GOV.14 results.

Labels: **observed** means read by the claimant from a provider response or file at the recorded identity during this task; **claimant-reported** means produced by the claimant's own local run and not yet independently reproduced; **ledger** means taken from a Plan ledger record without re-observation.

## What was built

DesktopPlatform `eng/stage_integration/` (pull request [DesktopPlatform#142](https://github.com/ArcForges/DesktopPlatform/pull/142)) adds a cross-repository integration graph. For one pinned commit per repository it reads only published package and dependency metadata: NuGet `packages.lock.json`, npm manifests and locks, Gradle lock files and settings, the producer registries `eng/packaging/packages.json` (DesktopPlatform) and `eng/contract-packages.json` (Contracts), wrangler configuration, workflow declarations, and each repository's own `eng/policy/exceptions.json` and `licence-boundary.json`. It lists one tree and fetches only those files over HTTPS; no repository is cloned and no source is read. Eleven rules, SI-01..SI-11, are evaluated over the direct and transitive closure of each repository:

| Rule | Assertion |
|---|---|
| SI-01 | every ArcForges-owned coordinate consumed has exactly one registered producer |
| SI-02 | no cross-repository project, source, submodule, link or include-build dependency |
| SI-03, SI-04 | direct and transitive consumption follows the producer access matrix (internal Contracts packages, Build.Policy, DesktopPlatform packages); every owned package a lock lists is checked, including one reached only through a third-party package; a transitive edge through producer-declared or lock-declared dependencies is reported with its path; a registry package that is not public with no audience in the policy fails closed |
| SI-05 | no AGPL-produced package in an Apache closure unless the consumer's own unexpired RP-03 row covers that project |
| SI-06 | no desktop native or UI asset reachable from Cloud ([NS-02](../architecture/21-platform-and-dependency-matrix.md#rule-ns-02)) |
| SI-07 | the Mobile closure contains no AGPL implementation and no unregistered ArcForges coordinate |
| SI-08 | exactly one Harness owner (AI) |
| SI-09 | each repository's own policy host runs as a command (not print-only text) in a workflow a pull request reaches (directly or by reusable call) without a `paths`, `branches` or `types` filter, unconditionally, without continue-on-error or `; true`/`|| echo`/`set +e` suppression, and its host markers exist |
| SI-10 | the snapshot covers exactly the seven repositories, pins full commits with source digests, is bound to the policy hash and is not older than 45 days |
| SI-11 | exception data is owned and unexpired |

The pull-request job `stage-integration` in `pr-gate.yml` runs the 47 offline tests and `verify` over the committed snapshot; a finding exits non-zero, fails the job and, because the job is listed in the aggregate `ci` job's `needs`, fails `ci`. Its write scope was added by the planning repair [Design#226](https://github.com/ArcForges/ArcForges-Design/pull/226) with [Plan#292](https://github.com/ArcForges/Plan/pull/292).

## Pinned metadata and result

The snapshot was read live (claimant-run, **observed** from the provider) at these `main` heads on 2026-10-05 and evaluated with zero findings across all eleven rules:

| Repository | Pinned commit | Boundary | Metadata files read | Own policy host in a pull-request-reachable workflow |
|---|---|---|---:|---|
| DesktopPlatform | `5405d80a7e49d7d5b385db6859ab9ab3c5d6dd18` | AGPL | 68 | architecture suite and invariant accounting (package-validation, called from pr-gate), specification integrity (design-policy) |
| Contracts | `db9df61430cd8a6c3765a7986bcc4b4165307abc` | Apache | 40 | hosted architecture suite in the Security workflow secrets job |
| ArcScope | `80dd7f24009a5259cf432551b26d70b634b7b746` | AGPL | 10 | hosted architecture suite in the CI quality job |
| Cloud | `ea08736d571cf0f4b44e022117cb44652a392e66` | AGPL | 13 | hosted architecture gate and forbidden-term scan in the CI quality job |
| AI | `5421c3789240093b2fce36322c2eb7773325ec7b` | AGPL | 7 | `npm run check`, which runs the owned policy |
| Web | `794ef933d3dba836c60b29a481091d40ab4a2b1a` | AGPL | 9 | `npm run check` (Linux), which runs the owned policy |
| Mobile | `377fa5d6e00b7a50d37d2f8434f915850c6d5b9f` | Apache | 9 | `spotlessCheck`, which depends on the Gradle policy verification |

Facts found in the real metadata: the only Apache-to-AGPL edge is the Contracts `tests/ArchitectureTests` host consuming `ArcForges.Build.Policy`, covered by the single Contracts RP-03 row (owner Contracts, expiry 2027-04-04); Cloud consumes no DesktopPlatform package except the build-only Build.Policy and reaches no native or UI package; the Mobile closure holds only `io.github.arcforges` Contracts Maven artifacts; no repository carries a submodule, `includeBuild`, outside-root link or foreign project reference; only AI declares Harness workflow classes; the 17 DesktopPlatform and 20 Contracts producer registry rows have no duplicate identity.

## Negative fixtures

`test_stage_integration.py` builds synthetic seven-repository worlds (**fixtures, not observations of the real repositories**) and proves each rule fails when violated: an unregistered and a duplicate producer; a project reference to another repository; a submodule, include-build, outside-root file link and a GitHub source dependency; an internal package outside its audience; a forbidden transitive edge recorded only in producer metadata and one recorded only in a lock; an AGPL package in an Apache closure and a non-covering or expired exception; Cloud reaching a native runtime package and a foreign UI package; Mobile importing an AGPL-produced and an unregistered coordinate; a second and a missing Harness owner; a gate that is missing, not pull-request reachable, continue-on-error, suppressed, conditional or lacking its host marker; a tampered snapshot policy hash, commit, coverage, digests and boundary; incomplete, foreign-owned and expired exception rows. The committed real snapshot with one injected Cloud-to-native edge is also rejected. Local run (claimant-reported): 47 tests OK. After the independent review, tests were added for each of its reported gaps and surviving mutants: a forbidden owned package behind a third-party package (NuGet and npm), unregistered and duplicate producers as separate findings, npm lock edges, a non-public registry package without an audience, a workspace name equal to a foreign producer id, every-lock and rule-name matching of exceptions, foreign UI packages by substring and when transitive, Harness package names and every wrangler file (json, jsonc, toml, several files), echo or printf-only gates, `; true`, `|| echo`, `|| :`, `set +e` and silent-continue suppression, a masking duplicate step, pull-request path/branch/type filters, job-level conditions and continue-on-error, mismatched gate facts, snapshot coverage, boundary, schema version, collection date, staleness and digest shape, and a real-date expiry in `verify`.

## Hosted CI observed

At the pinned heads the hosted main-push runs (**observed** through the provider API, job conclusions only) were: Contracts CI `37251542304` and Security `37251542319` success; ArcScope CI `37227084942` success; Cloud CI `37255090427` success; AI CI `37207551785` success; Web CI `37111148859` success; Mobile CI `37072330027` success; DesktopPlatform Publish NuGet `37208797893` success (it calls the pull-request gate). On pull request [DesktopPlatform#142](https://github.com/ArcForges/DesktopPlatform/pull/142) the job `stage-integration` passed in hosted run `37262285837` (**observed**). No artifact was downloaded.

## Limits and deferred checks

- The snapshot is a pin with an owner and a bound: the DesktopPlatform integration owner (holder of `roles/integration-desktopplatform`) runs `snapshot` and reviews the diff after any merge that changes a repository's published metadata and at least every 45 days; `verify` fails SI-10 once the pin is older, so the gate itself forces the refresh. Between refreshes the offline gate cannot see metadata merged in another repository; that repository's own host still gates its change. No scheduled job performs the refresh; that remains manual and is an open item.
- Offline `verify` checks the snapshot's internal consistency; it does not re-read the providers, so edited facts pass offline. `drift` (local opt-in) re-reads the pins and finds that. The foreign-UI denylist is name-pattern based and SI-02 reads locks, manifests and settings only, not project files, `build.gradle.kts` or `NuGet.config`.
- The DesktopPlatform pin predates the pull request that adds the `stage-integration` job, so that job is evidenced by its own hosted run, not by a pinned gate fact.
- Metadata cannot prove runtime behaviour: no native isolation, AOT, device, Cloudflare or commercial gate is closed by this record, and fixtures are not real-integration proof for those gates.
- [GOV.07](../planning/delivery/lanes/governance.md#task-gov-07) was delivered when this record was written, with the ArcScope executable classified non-production. It is now complete (ArcScope #24 after GOV.20): the executable is production-classified, with one carve-out: its own generated System.Text.Json files are filtered from `BAN-REFLECTION` at an anchored path and are not reflection-enforced. See the [stage acceptance](wp05-stage-acceptance.md) completion follow-up; the pins in this record are the first snapshot (2026-10-05), refreshed there.
- [GOV.13](../planning/delivery/lanes/governance.md#task-gov-13) classifies all 406 invariants as not-yet-implemented (none enforced); [PG-11](open-gates-register.md#rule-pg-11) therefore stays open.
