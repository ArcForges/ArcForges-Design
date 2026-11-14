# AD-0019 — MCP-first development and verification

- Status: Accepted; current V2 scope clarified by AD-0022.
- Date: 2026-11-14

The Windows workstation and H-22 native Linux host are reached through their designated MCP servers. Agent scratch, local WSL, SSH and another machine never substitute for required host verification. If a host is unavailable, the required status stays missing and merge is blocked. Do not provision tools or alter the hosts to bypass a prerequisite.

The [original decision](../../history/v1-20261114/docs/decisions/AD-0019-mcp-first-verification.md) is frozen evidence. Its old product task IDs and activation exceptions do not start new work. The current [pivot](AD-0022-cli-sandbox-platform-pivot.md), Plan execution policy and repository AGENTS define V2 scope; verification and review gates remain unchanged.
