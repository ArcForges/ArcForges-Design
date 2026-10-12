# Agent instructions: ArcForges-Design

This repository is the **design authority** for ArcForges. The delivery plan, ledger and procedures live in `ArcForges/Plan`; read its `AGENTS.md` before any delivery work.

## Rules

1. **Scope.** Design only: product, decisions, architecture, contracts (protos as specifications), data models, state machines, experience, reuse, verification and traceability. No implementation code; tools are the exception.
2. **Branches and worktrees.** Work in a git worktree under `.worktree/` (ignored), never in the main checkout. Branch names: `design/<topic>`. One PR per coherent change.
3. **Serial delivery** ([AD-0014](docs/decisions/AD-0014-delivery-method.md)). One active task at a time. Delegation is allowed to one worker or reviewer at a time, on Opus 5.5 only (never Haiku). There is no build slot.
4. **Generated files.**
   - `docs/contracts/api-catalogue.md` and `docs/state-machines/README.md` are generated. Edit the protos or `machines.json` instead, then run `python tools/check_design.py --write`.
   - The protos under `docs/contracts/proto/` are hand-maintained specifications that follow [docs/contracts/README.md](docs/contracts/README.md).
5. **Contract changes.** Additive only within `v1`. Every RPC carries the annotations `auth`, `idempotency`, `deadline`, `stream`, `errors` and `locality`; every request field carries a `validate:` rule; every error code is catalogued in `errors.md`. The checks enforce this.
6. **Decisions.** A change to an accepted decision is a new or amended ADR with status and date. Superseded material stays as history and names its successor.
7. **Honesty.**
   - Facts are cited by verification ID (V/L/A/F) in [docs/verification/platform-capabilities.md](docs/verification/platform-capabilities.md).
   - Assumptions name their future-validation owner task.
   - Real-world validation that cannot run now goes to the Plan acceptance register, never reported as proven.
8. **Checks before review.** Run `python tools/check_design.py --require-protoc` and `python -m unittest discover -s tests` and record the results in the PR. The reviewer re-runs only checks whose inputs they doubt, or whose tooling the PR changed (AD-0014 §4).
9. **Standing constraints.**
   - Never read or print secrets.
   - Cloudflare only through repository scripts.
   - No proxy or network changes.
   - Never unpublish, deprecate or delete a published version.
   - Leave Dependabot PRs untouched.
   - Never change repository security settings.
10. **Commits and PRs.** Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. PR bodies end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
