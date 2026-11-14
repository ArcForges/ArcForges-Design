# AD-0016 — Local-first verification, owner-only lightweight CI and testing techniques

- Status: Accepted; current V2 scope clarified by AD-0022.
- Date: 2026-11-14

Author checks are targeted and distinct. All repository-required native Windows/Linux verification runs after pushing the exact head. External hosted CI remains required where configured. No device, GUI, browser, live-service or inference CI is added.

The [original decision](../../history/v1-20261114/docs/decisions/AD-0016-local-first-verification.md) is frozen evidence. Its old product task IDs and activation exceptions do not start new work. The current [pivot](AD-0022-cli-sandbox-platform-pivot.md), Plan execution policy and repository AGENTS define V2 scope; verification and review gates remain unchanged.
