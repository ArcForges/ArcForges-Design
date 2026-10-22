# Agent instructions: ArcForges-Design

This repository is the **design authority** for ArcForges. The delivery plan, ledger and procedures live in `ArcForges/Plan`; read its `AGENTS.md` before any delivery work.

## Rules

1. **Scope.** Design only: product, decisions, architecture, contracts (protos as specifications), data models, state machines, experience, reuse, verification and traceability. No implementation code; tools are the exception.
2. **Branches and worktrees.** Work in a git worktree under `.worktree/` (ignored), never in the main checkout. Branch names: `design/<topic>`. One PR per coherent change.
3. **Serial delivery** ([AD-0014](docs/decisions/AD-0014-delivery-method.md), [AD-0016](docs/decisions/AD-0016-local-first-verification.md)). One active task at a time. Delegation is allowed to one worker or reviewer at a time, on Opus 5.5 only (never Haiku). There is no build slot. The owner's (`deku2026`) PRs are gated by the required host statuses of rule 8 plus the independent review; external PRs by the hosted `Design checks` workflow plus review.
4. **Generated files.**
   - `docs/contracts/api-catalogue.md` and `docs/state-machines/README.md` are generated. Edit the protos or `machines.json` instead, then run `python tools/check_design.py --write`.
   - The protos under `docs/contracts/proto/` are hand-maintained specifications that follow [docs/contracts/README.md](docs/contracts/README.md).
5. **Contract changes.** Additive only within `v1`. Every RPC carries the annotations `auth`, `idempotency`, `deadline`, `stream`, `errors` and `locality`; every request field carries a `validate:` rule; every error code is catalogued in `errors.md`. The checks enforce this.
6. **Decisions.** A change to an accepted decision is a new or amended ADR with status and date. Superseded material stays as history and names its successor.
7. **Honesty.**
   - Facts are cited by verification ID (V/L/A/F) in [docs/verification/platform-capabilities.md](docs/verification/platform-capabilities.md).
   - Assumptions name their future-validation owner task.
   - Real-world validation that cannot run now goes to the Plan acceptance register, never reported as proven.
8. **Verification** ([AD-0016](docs/decisions/AD-0016-local-first-verification.md) as amended by [AD-0020](docs/decisions/AD-0020-post-push-verification-and-required-checks.md); hosts [AD-0019](docs/decisions/AD-0019-mcp-first-verification.md)). Push → Fetch → Local verification → Report status → Required checks → Review → Merge.
   - **Push** the branch to GitHub; nothing is verified before a push. There is no pre-push hook: `python eng/verify.py install`, run once per clone from the main checkout on `main`, removes the retired one that an earlier `eng/verify.py` installed (and any `core.hooksPath`).
   - **Fetch and verify on each host.** Reach the Windows host through the Windows MCP server and the Linux host through the Linux MCP server (both standard MCP servers, the same for Claude Code and Codex). In that host's clone of this repository, fetch the pushed commit from GitHub and run the command in a worktree at it:

     ```
     git fetch origin <branch>
     git worktree add --detach .worktree/verify-<sha> <sha>
     cd .worktree/verify-<sha>
     python eng/verify.py run-and-report
     ```

     Fetch `refs/pull/<n>/head` for a pull request from a fork, and only after reading its diff (the host runs its code).
   - **What runs.** The command runs this host's leg of the commit, exactly what `design.yml` runs:
     - the locked restore of `tools/proto-toolchain/ProtoToolchain.csproj`;
     - `python tools/check_design.py --require-protoc --compile`;
     - `python -m unittest discover -s tests -v`;
     - `actionlint` on Linux when `.github/workflows/**` changed.

     Every change runs this full profile. The Windows leg runs on native Windows in `.worktree/_verify`, the Linux leg in a Linux-native clone; `eng/verify.py` runs only the leg of the host's own operating system, never through WSL or a remote shell, and local WSL is never used. `python eng/verify.py list` shows each host's steps; `python eng/verify.py run` runs the leg without reporting.
   - **Report status.** The command reports the commit status `arcforges/windows` or `arcforges/linux` on that exact commit:
     - `pending` when it starts;
     - `success` only when every step of the leg ran and passed;
     - `failure` when a step failed, `error` when the leg could not complete.

     It exits non-zero unless it reported success. A failure prints the step, the last log lines and the log path, and the logs and a `summary.json` stay on the host. Read the log, fix the cause, push, verify again.
   - **Credentials.** The host reports with `ARCFORGES_STATUS_TOKEN` when set (a token limited to commit statuses), otherwise with its own `gh` login. Never print or copy either.
   - **Required checks.** The `main` ruleset requires both statuses for every PR, with no bypass actors, and the branch must be up to date with `main`. A missing, pending or failed status blocks the merge, and every new push needs verifying again on both hosts.
   - **Review.** The independent review looks at the head that carries both successful statuses, and the PR names them. The reviewer re-runs only checks whose inputs they doubt, or whose tooling the PR changed (AD-0014 §4).
   - **If a host's MCP server is unavailable,** stop and report it: its status stays missing and the PR cannot merge. Never skip a step, run the leg on another host (an agent's own sandbox included) or weaken it (AD-0019 §5).
   - **Statuses and rulesets.** A status is reported only by `python eng/verify.py run-and-report` on the host it names, at the commit it verified. Never post, edit or copy an `arcforges/*` status by hand (for example with `gh api …/statuses`). Never change a ruleset, branch protection or required check to get a PR merged.
   - AI agents must never use `git push --no-verify` to bypass required validation. They must also never disable, remove, modify, or otherwise circumvent the hooks or required checks merely to get a change through.
   - If validation fails, investigate and fix the underlying issue.
   - If a required local test cannot run, do not silently skip it or claim successful verification.
   - Changing `eng/verify*.py`, `.githooks/` or the rulesets as reviewed engineering work is allowed; changing them to get a change through is not.
9. **Efficient execution.** The cross-repository rules are in the Plan's [`AGENTS.md`](https://github.com/ArcForges/Plan/blob/main/AGENTS.md); here:
   - Run long commands in the background and wait for their completion notification; no sleep loops or fixed delays.
   - Restore once; builds stay incremental (never clean without cause).
   - While iterating, run `python tools/check_design.py --require-protoc` (add `--compile` when protos changed) and the tool tests; the full profile runs once per pushed head, on each host (rule 8).
   - Reviewers add a worktree to the existing clone (`git worktree add`) instead of cloning, and re-run only distinct evidence.
   - Measure before restricting parallelism or resources.
10. **Standing constraints.**
    - Never read or print secrets.
    - Cloudflare only through repository scripts.
    - No proxy or network changes.
    - Never unpublish, deprecate or delete a published version.
    - Leave Dependabot PRs untouched.
    - Never change repository security settings.
11. **Commits and PRs.** Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. PR bodies end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
12. **Priority Research Prompts** ([docs/research-prompts/](docs/research-prompts/README.md)).
    - A PRP (`PRP-0001`, …) holds a complete prompt for research that will be performed later.
    - PRP research has higher consideration priority than ordinary `RM-*` and `EX-*` roadmap research: when the owner requests a future research topic, check the PRPs before beginning ordinary roadmap exploration.
    - Saving a PRP does not authorize executing it. A PRP is researched only when the owner explicitly requests it.
    - A PRP does not supersede delivery authorization (serial delivery, [AD-0014](docs/decisions/AD-0014-delivery-method.md); the Plan's delivery graph), accepted decisions, or the canonical roadmap in `ArcForges/Plan` and its governance ([AD-0015](docs/decisions/AD-0015-direction-editions-roadmap.md) §9).
