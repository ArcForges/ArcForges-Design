# AD-0016 — Local-first verification, owner-only lightweight CI and testing techniques

- Status: Accepted (2026-10-16; the user's instruction of that day, with the coordinator's implementation decisions made under the user's grant to "make implementation decisions independently")
- Amends: [AD-0014](AD-0014-delivery-method.md) §4 (the "Hosted CI" row) and §5 ("hosted CI is the merge gate"), which now apply to external PRs only
- Related: [16 testing strategy](../architecture/16-testing-strategy.md), [15 performance targets](../architecture/15-performance-targets.md), [13 distribution](../architecture/13-distribution-updates.md) §2 (release builds stay hosted), [conflicts](../reuse/conflicts.md) C-07

## Context

Under [AD-0014](AD-0014-delivery-method.md) hosted CI was the merge gate for every PR, so each of the owner's PRs ran its full build and test matrix on GitHub runners after the author had already run the affected suites on the workstation, and main pushes ran it again. On 2026-10-16 the user asked for a coordinated change of the development workflow. The central principle and the intended behaviour, quoted from the user (2026-10-16):

> **The central principle is simple: anything that can be reliably built, tested, or validated on my local Windows/WSL environment should run locally, not on GitHub Actions for my own PRs.**

> | PR author | Local verification | GitHub Actions |
> |---|---|---|
> | deku2026 | Mandatory comprehensive validation through Git hooks | Only genuinely necessary GitHub-specific operations |
> | Everyone else | No mandatory local hook requirement | Existing comprehensive CI |

The user also asked for a more effective local testing strategy ("reliable, meaningful defect detection", not maximum test counts or coverage), evaluated property-based, fault-injection, fuzz, mutation, stress and model-based testing, and asked that flaky tests be fixed at their cause. The decisions below are the coordinator's; the user's statements are attributed where quoted.

## Decision

1. **Merge gate.**
   - **Owner PRs** (author `deku2026`): the repository-managed pre-push verification at the pushed head, recorded in the PR by the hook's PASS line, plus the independent review at the same head ([AD-0014](AD-0014-delivery-method.md) §4). GitHub shows the validation jobs as skipped.
   - **External PRs** (anyone else, Dependabot included): full hosted CI as before, plus review. External contributors need no local hook.
2. **CI job classes.** The PR author is read only from the event, `github.event.pull_request.user.login == 'deku2026'`; there are no repository variables, secrets or API lookups.

   | Class | Owner PR | External PR | Push to main | Schedule | `workflow_dispatch`, `merge_group` |
   |---|---|---|---|---|---|
   | Validation: build, test, AOT, packaging checks, format, analyzers, policy and tool tests, workflow lint, cross-platform and ARM64 matrices | skipped | runs, unchanged coverage | skipped | skipped | runs |
   | Security analysis: CodeQL, secret scan, dependency review, dependency audit | skipped | runs | skipped | runs where a schedule exists | runs |
   | Delivery: jobs that build the published or deployed bytes, and the publish and deploy jobs | — | — | runs | — | unchanged |

   - Validation and security jobs carry one job-level condition, identical across repositories apart from the events a workflow has: `github.event_name != 'push' && github.event_name != 'schedule' && !(github.event_name == 'pull_request' && github.event.pull_request.user.login == 'deku2026')` (security jobs with a schedule drop the `schedule` term).
   - **Push to main runs no validation.** Every main commit arrives through a PR verified either by the owner's hook or by full PR CI. Main-push runs keep only delivery work; a workflow without delivery work has no push trigger.
   - **Delivery pipelines are unchanged.** Where publication embeds its gates in the evidence of the published bytes, the main-push pipeline stays as it is; only jobs that do not feed delivery are skipped on push. Release builds stay hosted ([13](../architecture/13-distribution-updates.md) §2).
   - **Required checks** are reduced to `Verify` where a repository required more. A skipped job reports success to a required check, but a skipped matrix job does not report its expanded name and the code-scanning `CodeQL` check never appears without an analysis, so `Verify` requires every validation and security job for external PRs. Check names that stay required keep their names.
   - `workflow_dispatch` keeps a manual full run wherever it exists.
3. **Pre-push verification** (decision level; the core is one script, `eng/verify.py`, identical in every active repository, with the repository's steps in `eng/verify_steps.py`).
   - **Installation:** `python eng/verify.py install` sets `core.hooksPath` to the tracked `.githooks`, once per clone, shared by all its worktrees.
   - **Source state:** every pushed commit is verified, never the working tree: in a dedicated detached worktree on Windows and a Linux-native clone in WSL Debian, both checked out at the pushed commit and cleaned of untracked files (ignored build output stays, so builds are incremental). The step table and the core are read from the pushed commit.
   - **Lanes:** steps are grouped into lanes (Windows, WSL and small independent lanes) that run concurrently, each lane in order. Timing- or resource-sensitive steps are `exclusive` and run alone after all lanes.
   - **Fail closed:** a step that fails, times out (its process tree is killed) or cannot run (a missing tool, WSL Debian unavailable) rejects the push, naming the step, the last lines of its log and the log path.
   - **Reuse:** a pass is recorded under the Git common directory, keyed by the commit's tree, the hashes of both scripts and the tool versions on each host. An identical key is not verified again.
   - **Profiles:** each repository selects steps from the paths changed since the merge base with `main`. A change that touches only Markdown documentation outside code, tests, scripts and workflows runs a light profile (whitespace, secret scan); anything else runs the full profile. In this repository Markdown is the source, so every change runs the full profile.
   - **Coverage:** the CI-equivalent profile of each repository (build, analyzers, format, tests, closed loop on Native AOT, AOT publish x64, size and startup gates, packaging, contract checks, `actionlint` when workflows change, secret scan of the pushed range with the CI's pinned gitleaks image, NuGet audit through the locked restore and `npm audit --audit-level=high` where a repository has npm).
   - **Not reproduced locally:** CodeQL and GitHub dependency review are GitHub services; they keep running for external PRs and on the existing schedules. ARM64 legs are removed from the owner path by the user's instruction ("ARM64 CI coverage is explicitly removed from my lightweight PR path"). macOS is out of scope ([AD-0002](AD-0002-platform-scope.md)).
   - **Rules for agents.** The user's rule: "AI agents must never use `git push --no-verify` to bypass required validation." Hooks are never disabled, removed, modified or circumvented merely to allow a push; a failure is investigated and fixed at its cause; a required test that cannot run is never silently skipped or reported as passed. Each repository's `AGENTS.md` states these rules verbatim. Changing the verification scripts as reviewed engineering work is allowed; changing them to get a push through is not.
4. **Startup regression gate.** It compares against the PR's base commit built on the same machine: the merge base in the hook, the base commit on the same runner in external-PR CI. The previous main run's uploaded binaries are no longer used ([15](../architecture/15-performance-targets.md)).
5. **Testing techniques** (evaluated, not installed wholesale):

   | Technique | Decision | Evidence or reason |
   |---|---|---|
   | Property-based | **Adopt CsCheck** (one test-only package, no dependencies, Apache-2.0) for invariants, boundary conditions, resource constraints and parsers | Works from plain xunit facts, shrinks failures, and includes model-based and linearizability testing. FsCheck's xunit integration would couple to the repositories' `xunit.v3.mtp-v2` runner for no extra capability. |
   | Model-based and concurrency | **Adopt through CsCheck** for state machines and concurrent components | Same package. |
   | Fault injection | **Strengthen with real processes**, no new framework | Kill, crash, memory-limit, disconnect, permission and timeout faults are injected with the existing harness: `TestLoad` scenarios, real node and supervisor processes, real pipes and Unix sockets, real ACLs. Fakes stay limited to [AD-0014](AD-0014-delivery-method.md) §6. |
   | Stress and stability | **Add a repeat mode** to the test scripts (selected suites N times, stop at the first failure, per-iteration timing) for the deep tier | The flakes found so far (a settle window, PID reuse, the commit limit) needed repetition to surface. |
   | Coverage-guided fuzzing | **Not adopted now** | SharpFuzz needs AFL++ (Linux) or libFuzzer (Windows); neither is installed, and installations are the user's. Protobuf parsing is generated upstream code. Generated-input properties cover the parsers ArcForges owns (frames, configuration, CLI arguments, redaction). Revisit when a parser of untrusted input is added. |
   | Mutation testing | **Not adopted now** | Measured 2026-10-16: Stryker.NET 5.0.0 refuses Microsoft.Testing.Platform projects as not yet supported (stryker-net issue 3094), and every ArcForges test project is xunit v3 on that platform. Switching runners to VSTest only for mutation runs is not justified. Revisit when Stryker supports it. |
   | Deterministic testing | **Fix flakes at the cause** | The Windows commit-limit test failed intermittently because the .NET GC's default hard limit (75 % of the job's commit limit) throws `OutOfMemoryException` before the job limit is reached, so the job's memory event never occurs; job notifications are not guaranteed either (V-W03). The test exercises the job limit itself and asserts the guaranteed contract (commit never above the limit, violation classified from a guaranteed source), not an optional notification. Fixed sleeps become condition waits; generous timeouts stay only on the failure path; no retries or weakened assertions hide a defect. |

   **Tiers.**
   - *Routine (inner loop):* the affected suites, built once, then reruns without rebuilding.
   - *Pre-push (the hook):* the full CI-equivalent profile on Windows and WSL Debian.
   - *Deep (manual, release preparation, after a flaky failure):* stress repeats, performance and WSL-bridge suites, long property runs, and ARM64 through a manual `workflow_dispatch` when wanted.

   **Parallelism.** Test projects run concurrently with a bounded default chosen from recorded measurements (wall time, CPU, failures over repeated runs). Serial collections remain only where tests share machine-wide state. Timing-, CPU-share- and memory-sensitive tests carry the trait `isolation=exclusive` and run in a separate exclusive phase.

## Consequences

- The owner's PRs use no runner time for build, test or analysis; external PRs keep their full coverage, and merge commits trigger only delivery.
- PR evidence for owner PRs is the hook's PASS line (`arcforges-verify: PASS <sha> tree <tree> profile <name> …`), quoted by the coordinator, plus the review record.
- The Plan's execution policy, delivery procedure and prompts follow this decision; each active repository's `AGENTS.md` states the local-verification rules.
- **Known limitations:**
  - DesktopPlatform publication re-runs its gates on main, because its evidence chain binds them to the published bytes; changing that chain is out of scope.
  - ARM64 regressions in owner PRs surface only through an external PR or a manual dispatch.
  - CodeQL and GitHub dependency review run only for external PRs and on schedules; owner PRs rely on the local analyzers, NuGet and npm audits and secret scan.
  - Hooks are bypassable by design. The user accepted this for a trusted workflow ("I do not want a complicated enforcement infrastructure"); the rules above and the PASS line in each PR are the controls.
