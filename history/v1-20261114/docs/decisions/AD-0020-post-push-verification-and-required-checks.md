# AD-0020 — Post-push host verification and required status checks

- Status: Accepted (2026-10-22; the product owner's instruction of that day, with the coordinator's implementation decisions made under the owner's grant to "make routine technical and architectural implementation decisions")
- Decider: the product owner
- Amends: [AD-0016](AD-0016-local-first-verification.md) §1 (the owner's merge gate), §2 (required checks), §3 (the pre-push verification becomes the post-push verification of each host), the "Pre-push" tier of §5 and the consequences; [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §5 ("Exact commit", "Pass records", "PR evidence"); [AD-0019](AD-0019-mcp-first-verification.md) §2 (the record import), §3 (the Git-bundle channel), §5 (what a missing leg blocks), §7 (the mandatory pre-push hook, pass records and `import`) and its known limitations; [AD-0014](AD-0014-delivery-method.md)'s 2026-10-16 amendment (the owner's gate)
- Unchanged: every repository's verification steps, profiles and lanes; which operating system runs which step; the two MCP servers and their hosts ([AD-0019](AD-0019-mcp-first-verification.md) §1, §3, §4, §6); fail-closed behaviour, logs and process-tree cleanup; the CI job classes and the hosted CI of external PRs ([AD-0016](AD-0016-local-first-verification.md) §2); the independent review; release, deployment, signing and publication pipelines
- Related: [16 testing strategy](../architecture/16-testing-strategy.md) §3, Plan execution policy, every repository's `AGENTS.md` and `eng/verify.py`

## Context

Under [AD-0016](AD-0016-local-first-verification.md) §3, as amended by [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §5 and [AD-0019](AD-0019-mcp-first-verification.md), a push of the owner's branch was rejected by a pre-push hook until both native legs had passed: the Windows leg on the workstation and the Linux leg on the Linux MCP host. A commit that was not yet on GitHub had to reach the other host as a Git bundle, and that host's pass record had to come back to the pushing clone and be imported. In practice the bundles and records travelled through the agent's context, which AD-0019 §3 had ruled out, and every push waited for the slower leg.

On 2026-10-22 the product owner replaced that gate. The intended workflow, quoted from the owner:

> 1. Develop and commit normally.
> 2. Push the feature branch directly to GitHub. Dual-platform verification is no longer required before pushing.
> 3. Windows-MCP and Linux-MCP fetch the exact pushed commit directly from GitHub.
> 4. Each host independently runs its existing platform-specific verification steps.
> 5. Each host reports its verification result to GitHub using the Commit Status API or an appropriate equivalent.
> 6. GitHub Required Status Checks enforce that every applicable platform verification succeeds before the PR can merge into `main`.
> 7. Preserve the existing independent review requirements.

> GitHub handles source-code distribution. MCP handles execution. GitHub handles the merge gate.

The owner also asked that the existing verification requirements stay intact ("Only the timing, coordination, and enforcement mechanism should change"), that success never be reported when tests were skipped unexpectedly or verification was incomplete, and that agents cannot bypass the required checks.

## Decision

1. **The flow.** Push → Fetch → Local verification → Report status → Required checks → Review → Merge.
2. **Push.** A branch is pushed to GitHub without verifying it first. The pre-push verification hook is retired:
   - `.githooks/pre-push` is removed from every repository.
   - `python eng/verify.py install` removes a pre-push hook that an earlier `eng/verify.py` installed, and keeps any other.
   - A retired hook that is still installed calls `eng/verify.py pre-push`, which now lets the push through and says how to remove the hook.
   - A worktree still at a commit from before this decision has the old `eng/verify.py`, whose gate the retired hook would still run. Running `install` once per clone removes the hook, and with it that case.
   - Lightweight hooks stay where a repository has them (the `pre-commit` whitespace check).
3. **Fetch.** Each verification host fetches the exact pushed commit from GitHub into its own clone of the repository:
   - `git fetch origin <branch>`, or `refs/pull/<n>/head` for a pull request from a fork;
   - then a detached worktree at that commit.

   No Git bundle, cross-machine file transfer, pass record or other binary data travels between the hosts or through an agent's context.
4. **Local verification.** In that worktree, `python eng/verify.py run-and-report` runs this host's leg of the commit. The leg is exactly what the pre-push hook ran:
   - the steps of `eng/verify_steps.py` for the host's operating system, selected by the profile of the paths changed since the merge base with `main`;
   - the same isolated checkouts, lanes, timeouts, real-OS prerequisites and fail-closed rules;
   - the same logs, plus a `summary.json` per leg under the clone's `arcforges-verify/logs`.

   The step table and the script are read from the commit itself, so a commit is verified by its own definition. `python eng/verify.py run` runs the same leg without reporting, as a local check.
5. **Report status.** The host reports a GitHub commit status on the exact commit verified, through the Commit Status API (`gh api repos/<owner>/<repo>/statuses/<sha>`). The contexts are `arcforges/windows` and `arcforges/linux`.

   | State | When |
   |---|---|
   | `pending` | The leg starts. It is reported before any step runs, so a commit that is not on GitHub, or credentials that cannot write statuses, stop the leg at once. |
   | `success` | Every step of the leg ran and passed. A host whose leg has no steps for the commit reports success with a description saying so, for example "no Windows steps apply (profile 'docs')"; the step table decides that, not the agent. |
   | `failure` | A step failed, timed out or could not run. The description names the step. |
   | `error` | The leg could not complete, for example a broken step table, a shallow clone, or an interruption (Ctrl+C, SIGTERM, SIGHUP). |

   The command exits 0 after reporting success, 1 when a step failed, and 2 when the leg could not complete or its status could not be reported. A `pending` left by a host that stopped answering keeps the merge blocked.

   **Credentials.** The status is posted with the GitHub CLI:
   - It uses `ARCFORGES_STATUS_TOKEN` when that is set: a fine-grained token limited to *Commit statuses: write* on the ArcForges repositories, which the owner provisions on each host outside every repository.
   - Otherwise it uses the host's own `gh` login.
   - The script removes that token and the other GitHub tokens of the environment (`GH_TOKEN`, `GITHUB_TOKEN` and their enterprise forms) from the environment of every step. It unsets them again inside each Linux step, after the login profile has run, passes them only to `gh`, and never prints them.
   - The remote must be a github.com URL; statuses are posted to github.com only.
6. **Required checks.** Each repository's `main` ruleset requires the status of every host whose steps the repository's step table defines:
   - it applies to all pull requests targeting `main`, whatever their author;
   - it has no bypass actors, administrators included;
   - it uses the strict policy (the branch must be up to date with `main`), so a moved `main` means updating the branch and verifying again.

   A status belongs to one commit, so a new push has none and blocks the merge until both hosts have verified it. A missing, `pending`, `failure` or `error` status blocks the merge.

   | Repository | Required statuses | Note |
   |---|---|---|
   | ArcForges-Design | `arcforges/windows`, `arcforges/linux` | |
   | Plan | `arcforges/windows`, `arcforges/linux` | |
   | Contracts | `arcforges/linux` | Its step table has no Windows steps |
   | ArcForges | `arcforges/windows`, `arcforges/linux` | A documentation-only change has no Windows steps, so Windows reports success saying so |
   | DesktopPlatform | `arcforges/windows`, `arcforges/linux` | |
   | Cloud | `arcforges/windows`, `arcforges/linux` | |
   | Web | `arcforges/windows`, `arcforges/linux` | |
   | Mobile | `arcforges/windows`, `arcforges/linux` | |

   The hosted `Verify` check stays required where it already was. It is the external-PR gate of [AD-0016](AD-0016-local-first-verification.md) §2 and reports a skipped job for the owner's PRs. No other hosted job is added for the owner's PRs: the host statuses are the evidence, and the native builds and tests are not repeated on GitHub's runners.
7. **Review and merge.** The independent review is unchanged: it reviews the head commit that carries both successful statuses, and the PR is merged only once the review is done and the required checks pass. The statuses are the PR's verification evidence, and the host log directory named in the command's output is the diagnostic record. The PR no longer quotes `LEG PASS` lines.
8. **External PRs.** Hosted CI runs for them as before ([AD-0016](AD-0016-local-first-verification.md) §2). The required statuses apply to them too. Because a host executes the contributor's code as the host's user, who holds the reporting credential, a maintainer reads the diff before any host verifies `refs/pull/<n>/head`.
9. **Rules for agents.**
   - A status is reported only by `python eng/verify.py run-and-report` on the host whose operating system it names, at the commit it verified. Agents never post, edit or copy a status by hand.
   - Agents never change a ruleset, branch protection or required check to get a PR merged. They never add bypass actors.
   - The rules of [AD-0019](AD-0019-mcp-first-verification.md) §5 still hold, now with this consequence: if a host's MCP server is unavailable or its leg fails, the agent stops and reports it, and the status stays missing or failed. The agent never skips, mocks or weakens a step, and never runs the leg on another host.
   - "If validation fails, investigate and fix the underlying issue." "If a required local test cannot run, do not silently skip it or claim successful verification." ([AD-0016](AD-0016-local-first-verification.md) §3, unchanged.)
10. **Effective date and migration.** This decision takes effect in each repository when that repository's PR of it merges and its ruleset requires the statuses.
    - ArcForges-Design goes first. Its PR proves the mechanism: a success on each host, a failure that blocks, a missing status that blocks, a new push that clears the statuses, and a merge once both succeed and the review is done.
    - The other repositories follow one at a time.
    - Each migration PR is verified by `run-and-report` from its own commit before its ruleset starts requiring the statuses, so the change never blocks itself.

## Consequences

| Changed | Effective |
|---|---|
| [AD-0016](AD-0016-local-first-verification.md) §1: the owner's merge gate is the required host statuses at the PR head plus the review (no longer the hook's PASS line) | each repository's PR of this decision |
| [AD-0016](AD-0016-local-first-verification.md) §2 "Required checks": `arcforges/windows` and `arcforges/linux` are required alongside `Verify` | each repository's ruleset |
| [AD-0016](AD-0016-local-first-verification.md) §3 and §5 "Pre-push" tier: the same profile runs after the push, on each host, and is reported to GitHub (§2–§5) | each repository's PR |
| [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §5: the exact commit comes from GitHub, not a bundle; no pass records or `import`; the PR evidence is the statuses | each repository's PR |
| [AD-0019](AD-0019-mcp-first-verification.md) §2, §3, §5, §7 and the known limitations: no record import and no bundle channel; a missing leg blocks the merge, not the push | each repository's PR |
| [16](../architecture/16-testing-strategy.md) §1–§3: the "Pre-push verification" row becomes the post-push host verification | now |
| Plan: the execution policy, delivery procedure, prompts and H-22 (no file channel for Git bundles) | the Plan PR of this decision |
| Each repository: the shared `eng/verify.py` (`run-and-report`), `.githooks/pre-push` removed, `AGENTS.md` and the contributor documents | each repository's PR of this decision |

- **Known limitations.**
  - **Statuses are not tied to a source.** A required check on a commit status can be pinned to a source only when a GitHub App posts it. Anyone holding a token with status-write access to a repository could post `arcforges/*` by hand. The controls are:
    - the rules of §9;
    - the review, which looks at the statuses' descriptions (host, machine, step count);
    - and keeping that access to the owner's hosts.

    A GitHub App posting the statuses would close this; it is not set up.
  - **Fallback credential.** Until the owner provisions `ARCFORGES_STATUS_TOKEN` on a host, that host reports with its `gh` login, which carries the owner's broader `repo` scope. Steps never receive it through the environment. It stays on the host, but the code under verification runs as the same user and could read it from the host's `gh` configuration. This is why §8 applies to external PRs, and why a token limited to commit statuses is the intended setup.
  - **Unverified branches.** Pushing no longer waits for verification, so a branch on GitHub can hold unverified commits. Only `main` is protected, and only by the required statuses.
  - **Strict policy.** Merging one PR makes the others out of date, so they need updating and verifying again before they can merge. Delivery is serial ([AD-0014](AD-0014-delivery-method.md)), so this costs little.
  - **History.** Earlier PRs' `LEG PASS` lines and imported records stay as history and are not rewritten ([AD-0013](AD-0013-reuse-and-supersession.md)).
