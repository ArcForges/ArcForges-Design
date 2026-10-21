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
8. **Local verification** ([AD-0016](docs/decisions/AD-0016-local-first-verification.md); topology [AD-0018](docs/decisions/AD-0018-native-platforms-without-wsl-integration.md) §5, as amended by [AD-0019](docs/decisions/AD-0019-mcp-first-verification.md)).
   - Install once per clone, from the main checkout on `main`: `python eng/verify.py install` copies `.githooks/*` into the clone's common hooks directory, so every worktree runs them. It uses no `core.hooksPath`: it removes any, including per-worktree values left by older scripts, and refuses while one remains elsewhere. Re-run it when `.githooks/` changes. A push from a worktree whose commit has no `eng/verify.py` is rejected; rebase it onto `main`.
   - The pre-push hook verifies each pushed commit, not the working tree, in two legs on two machines: the Windows leg on native Windows in `.worktree/_verify`, reached through the Windows MCP server, and the Linux leg on the Linux MCP host in a Linux-native clone, reached through the Linux MCP server (both standard MCP servers, the same for Claude Code and Codex; AD-0019). `eng/verify.py` runs only the leg of the machine's own operating system, never through WSL or a remote shell. Local WSL is never used, not even as a fallback. If the Linux MCP server is unavailable, stop and report it: the Linux leg has no record, so the push stays rejected; never skip a step, use another host (an agent's own sandbox included) or bypass the hook (AD-0019 §5, §8). Each leg runs what `design.yml` runs: the locked restore of `tools/proto-toolchain/ProtoToolchain.csproj`, `python tools/check_design.py --require-protoc --compile` and `python -m unittest discover -s tests -v`, plus `actionlint` when `.github/workflows/**` changed. Every change runs this full profile.
   - `python eng/verify.py list` shows the steps and each leg's state; `python eng/verify.py run` verifies this machine's leg of `HEAD` and records it (keyed by the tree, the merge base, the step set and the scripts). On the other machine, check out the exact commit in a worktree (a commit not yet on GitHub travels as a bundle: `git bundle create <file> HEAD --not origin/main`, then `git fetch <file> HEAD` there), run `python eng/verify.py run` there, and accept its record here with `python eng/verify.py import <record>`, which refuses any mismatch. A push needs a passed or imported record of both legs.
   - A failure, timeout, missing tool or missing leg record rejects the push and prints the step, the last log lines and the log path. Read the log, fix the cause, push again.
   - Record each leg's `arcforges-verify: LEG PASS` line and the hook's `arcforges-verify: PASS` line in the PR. The reviewer re-runs only checks whose inputs they doubt, or whose tooling the PR changed (AD-0014 §4).
   - AI agents must never use `git push --no-verify` to bypass required validation. They must also never disable, remove, modify, or otherwise circumvent the hooks merely to allow a push.
   - Only `python eng/verify.py import` brings in another machine's leg, and only the record that `python eng/verify.py run` wrote on that machine at the exact commit: writing, editing or reusing a pass record by hand is circumventing the hooks.
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
12. **Priority Research Prompts** ([docs/research-prompts/](docs/research-prompts/README.md)).
    - A PRP (`PRP-0001`, …) holds a complete prompt for research that will be performed later.
    - PRP research has higher consideration priority than ordinary `RM-*` and `EX-*` roadmap research: when the owner requests a future research topic, check the PRPs before beginning ordinary roadmap exploration.
    - Saving a PRP does not authorize executing it. A PRP is researched only when the owner explicitly requests it.
    - A PRP does not supersede delivery authorization (serial delivery, the Plan's delivery graph), accepted decisions, or the canonical roadmap in `ArcForges/Plan` and its governance (AD-0015 §9).
