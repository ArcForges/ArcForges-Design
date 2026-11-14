# AD-0020 — Post-push host verification and required status checks

- Status: Accepted; current V2 scope clarified by AD-0022.
- Date: 2026-11-14

Push the branch; fetch its exact SHA on each designated host; use a worktree at that SHA; run python eng/verify.py run-and-report; require all configured arcforges/windows and arcforges/linux statuses and independent review at that head. Never forge/copy statuses, weaken checks, disable hooks or change security rules. Design merges first. Plan host verification then checks the actual new Design main; reverify if Design main changes.

The [original decision](../../history/v1-20261114/docs/decisions/AD-0020-post-push-verification-and-required-checks.md) is frozen evidence. Its old product task IDs and activation exceptions do not start new work. The current [pivot](AD-0022-cli-sandbox-platform-pivot.md), Plan execution policy and repository AGENTS define V2 scope; verification and review gates remain unchanged.
