# Agent instructions: ArcForges-Design

This repository is the **design authority** for ArcForges. The delivery plan, ledger and procedures live in `ArcForges/Plan`; read its `AGENTS.md` before any delivery work.

## Rules

1. **Scope.** Design only: product, decisions, architecture, contracts (protos as specifications), data models, state machines, experience, reuse, verification and traceability. No implementation code; tools are the exception.
2. **Branches and worktrees.** Work in a git worktree under `.worktree/` (ignored), never in the main checkout. Branch names: `design/<topic>`. One PR per coherent change.
3. **Serial delivery** ([AD-0014](docs/decisions/AD-0014-delivery-method.md), [AD-0016](docs/decisions/AD-0016-local-first-verification.md)). One active task at a time. Delegation is allowed to one worker or reviewer at a time, on Opus 5.5 only (never Haiku). There is no build slot. The owner's (`deku2026`) PRs are gated by the local verification below plus the independent review; external PRs by the hosted `Design checks` workflow plus review.
4. **Generated files.**
   - `docs/contracts/api-catalogue.md` and `docs/state-machines/README.md` are generated. Edit the protos or `machines.json` instead, then run `python tools/check_design.py --write`.
   - The protos under `docs/contracts/proto/` are hand-maintained specifications that follow [docs/contracts/README.md](docs/contracts/README.md).
5. **Contract changes.** Additive only within `v1`. Every RPC carries the annotations `auth`, `idempotency`, `deadline`, `stream`, `errors` and `locality`; every request field carries a `validate:` rule; every error code is catalogued in `errors.md`. The checks enforce this.
6. **Decisions.** A change to an accepted decision is a new or amended ADR with status and date. Superseded material stays as history and names its successor.
7. **Honesty.**
   - Facts are cited by verification ID (V/L/A/F) in [docs/verification/platform-capabilities.md](docs/verification/platform-capabilities.md).
   - Assumptions name their future-validation owner task.
   - Real-world validation that cannot run now goes to the Plan acceptance register, never reported as proven.
8. **Local verification** ([AD-0016](docs/decisions/AD-0016-local-first-verification.md)).
   - Install once per clone: `python eng/verify.py install` copies `.githooks/*` into the clone's common hooks directory, so every worktree runs them. It uses no `core.hooksPath` and removes one if set. Re-run it when `.githooks/` changes. A push from a worktree whose commit has no `eng/verify.py` is rejected; rebase it onto `main`.
   - The pre-push hook verifies each pushed commit, not the working tree, in `.worktree/_verify` (Windows) and a WSL Debian clone, concurrently. It runs what `design.yml` runs: the locked restore of `tools/proto-toolchain/ProtoToolchain.csproj`, `python tools/check_design.py --require-protoc --compile` and `python -m unittest discover -s tests -v`, plus `actionlint` when `.github/workflows/**` changed. Every change runs this full profile.
   - `python eng/verify.py list` shows the steps; `python eng/verify.py run` verifies `HEAD` before pushing, and the push reuses that pass for the identical tree, step set, scripts and tools.
   - A failure, timeout or missing tool (including WSL Debian) rejects the push and prints the step, the last log lines and the log path. Read the log, fix the cause, push again.
   - Record the hook's `arcforges-verify: PASS` line in the PR. The reviewer re-runs only checks whose inputs they doubt, or whose tooling the PR changed (AD-0014 §4).
   - AI agents must never use `git push --no-verify` to bypass required validation. They must also never disable, remove, modify, or otherwise circumvent the hooks merely to allow a push.
   - If validation fails, investigate and fix the underlying issue.
   - If a required local test cannot run, do not silently skip it or claim successful verification.
   - Changing `eng/verify*.py` or `.githooks/` as reviewed engineering work is allowed; changing them to get a push through is not.
9. **Efficient execution.** The cross-repository rules are in the Plan's [`AGENTS.md`](https://github.com/ArcForges/Plan/blob/main/AGENTS.md); here:
   - Run long commands in the background and wait for their completion notification; no sleep loops or fixed delays.
   - Restore once; builds stay incremental (never clean without cause).
   - While iterating, run `python tools/check_design.py --require-protoc` (add `--compile` when protos changed) and the tool tests; the full profile runs once, in the hook.
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
