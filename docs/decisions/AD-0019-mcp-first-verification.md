# AD-0019 — MCP-first development and verification

- Status: Accepted (2026-10-21; the product owner's architecture decision of that day; amended 2026-10-22 after DesktopPlatform PR #195: no build output travels between the two hosts, so the Linux host no longer receives DesktopPlatform's native hand-off archive, §3, §8 and the known limitations)
- Decider: the product owner
- Amends: [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §5 (where each leg runs) and its known limitation on a WSL2 Linux host, [AD-0016](AD-0016-local-first-verification.md) §3 and its §5 amendment of 2026-10-17 (the Linux venue of the OS secret-store tier)
- Unchanged: [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §§1–4 (native Windows and native Linux product support; a user may still run the general Linux node in a WSL2 distribution as an ordinary Linux node) and the rest of §5 (legs, exact commit, pass records, real-OS checks, PR evidence)
- Related: [16 testing strategy](../architecture/16-testing-strategy.md) §3, Plan acceptance register H-22 and H-23

## Context

AD-0018 §5 moved pre-push verification onto two native legs. The Windows leg already ran on the owner's workstation through a Windows MCP server. The Linux leg ran where a session happened to have Linux: the Claude Code Cloud container for the checks it could run, and, as an interim real Linux host, the owner's local WSL Debian used as a plain Linux machine (Plan H-22). AD-0018 also still allowed a WSL2 distribution as that real host, and the OS secret-store tier kept its Linux tests in the `ArcForgesTest` WSL distribution.

On 2026-10-21 the product owner moved development and verification to an MCP-first workflow:
- Windows verification runs through the existing Windows MCP server.
- Linux verification runs through an independent Linux MCP server, hosted on a VPS or another suitable Linux environment.
- No development or verification workflow depends on local WSL2 or Debian, uses it as a fallback, or requires it to be installed.
- Claude Code and Codex use the same standard MCP servers.
- If the Linux MCP server is unavailable, verification fails clearly and stops; tests are never skipped silently and hooks are never bypassed.

## Decision

1. **Two standard MCP servers.** Agents reach the verification hosts only through two MCP servers that implement the standard Model Context Protocol, so any conforming client can use them. Claude Code and Codex register the same two servers, each in its own client configuration:
   - the **Windows MCP server** on the owner's Windows 11 workstation (the existing server);
   - the **Linux MCP server** on an independent native Linux host: a VPS, or another suitable Linux environment that the owner provisions. It is never local WSL.

   Repositories hold no client configuration, server address or credential for them. Each client's configuration and the servers' credentials stay with the owner, outside every repository.
2. **Where each leg runs** (replaces the "Where" item of AD-0018 §5).
   - **Windows leg:** on the workstation, through the Windows MCP server, in an isolated worktree at the exact commit, as before.
   - **Linux leg:** on the Linux MCP server's host, through that server, in a Linux-native clone at the exact commit. An agent's own sandbox, such as a cloud container, is not a Linux verification host. A leg runs only on the operating system it names, and `eng/verify.py` stays unaware of MCP: it runs on the host and writes the pass record there. The agent brings the record to the pushing clone, where `python eng/verify.py import` checks it (AD-0018 §5, unchanged).
3. **What the Linux host provides.** Owner-provisioned, and outside every repository:
   - native Linux (glibc), a systemd user manager with `cpu`, `memory` and `pids` delegated on cgroups v2;
   - the repositories' pinned toolchains (the .NET SDK of `global.json`, Node and npm as pinned, Python 3.14, clang and lld for Native AOT), Docker Engine with the pinned images, and network access to the NuGet and npm registries and `mcr.microsoft.com`;
   - a Linux-native working area for the verification clones;
   - a way to receive a commit as a Git bundle from the workstation without passing it through an agent's context, checked by digest as today. Nothing else travels between the hosts: each leg builds what it verifies from the commit alone. *Amended 2026-10-22:* this item also named DesktopPlatform's native hand-off archive (several MB), which carried the Windows leg's native stage to the Linux leg; since DesktopPlatform PR #195, its Windows leg produces the native stage and everything that needs it (the architecture gate, the NuGet candidate and its packaging tests), and its Linux leg needs no Windows output;
   - separately, and only for the opt-in OS secret-store tier: an isolated test account or machine, separate from the verification account (item 6). The legs do not need it.
4. **No WSL.** Local WSL2 or Debian is not used for development or verification, not even as a fallback, and does not need to be installed. No step, script or document names a WSL distribution as a venue. This replaces AD-0018's interim WSL Debian host (H-22) and its known limitation that allowed a WSL2 distribution as the real Linux host. A product user may still run the Linux node inside WSL2 (AD-0018 §1, unchanged); that is a product scenario, not a verification venue.
5. **Fail clearly, never degrade.** If the Linux MCP server is not configured, cannot be reached, refuses, or its host lacks a prerequisite of item 3, the agent stops verification and reports the exact failure. The Linux leg then has no pass record, and the pre-push hook rejects the push, naming the missing leg and this decision. The agent never:
   - skips, mocks or weakens a step;
   - runs the leg on another host: local WSL, its own sandbox (such as a cloud container) or any other machine;
   - writes or edits a pass record by hand;
   - uses `git push --no-verify` or disables a hook.

   The same holds for the Windows MCP server and the Windows leg.
6. **OS secret-store tier, Linux.** The Linux Secret Service tests of the tier ([16](../architecture/16-testing-strategy.md) §1) run only on an isolated Linux secret-store test host reached through the Linux MCP server, never in the verification account or a user's session keyring. The host marks itself as isolated with a root-owned marker file, `/etc/arcforges/isolated-secret-store-test-host`, which its provisioning creates. The tier runner refuses Linux unless the marker is a regular file owned by root and writable by no one else, in a directory owned by root, and the runner is not root (the provisioning, not the test account, creates the marker). This replaces the `ArcForgesTest` WSL distribution. The tier stays opt-in and outside routine verification, and its Windows tests are unchanged.
7. **Kept unchanged:**
   - native Windows (job objects) and native Linux (systemd, cgroups v2) support;
   - Git worktrees;
   - the mandatory pre-push hook;
   - verification of the exact commit, pass records keyed by tree, base, profile, steps, scripts and context, and `import`;
   - every step and test of every repository;
   - fail-closed behaviour, logs and process-tree cleanup;
   - Native AOT builds.
8. **Effective date, no transition venue.** This decision takes effect in each repository when its PR of this decision merges. There is no transition venue. The Linux MCP server is provisioned separately (H-22), and until it is in place, no Linux leg can be recorded, so every push is rejected (item 5). The commits that introduce this decision are verified under the rule of their base (AD-0018 §5), before it takes effect, and never on local WSL. For ArcForges-Design, Plan, Contracts, Mobile and Web, the Linux leg ran in the Claude Code Cloud Linux environment. ArcForges, Cloud and DesktopPlatform need a real Linux host for their whole Linux leg (systemd and cgroups v2, a NuGet-reaching Docker build, and, until DesktopPlatform PR #195 withdrew it on 2026-10-22, the native hand-off, §3). That environment cannot provide one, and local WSL is no longer allowed, so their commits of this decision wait for H-22 like any other push.

## Consequences

| Changed | Effective |
|---|---|
| AD-0018 §5 "Where": the Windows leg through the Windows MCP server, the Linux leg through the Linux MCP server (§2); the interim WSL Debian host is withdrawn | now |
| AD-0016 §3 (where the legs run) and its 2026-10-17 amendment: the Linux Secret Service tier moves from `ArcForgesTest` to the isolated test host (§6) | now |
| [16](../architecture/16-testing-strategy.md) §1 and §3: the Linux rows name the Linux MCP host | now |
| Plan: H-22 becomes the Linux MCP server and its host, and H-23 the isolated secret-store test host; AGENTS.md, the execution policy, the execution prompt and the baseline name the two MCP servers | the Plan PR of this decision |
| Each repository: `AGENTS.md` and the shared `eng/verify.py` name the MCP servers and the stop rule; DesktopPlatform's and ArcForges's OS secret-store tier runners use the marker of §6 | each repository's PR of this decision |
| §3 (amended 2026-10-22): the Linux host receives Git bundles only; DesktopPlatform's native hand-off archive is withdrawn, and each leg builds what it verifies (DesktopPlatform PR #195) | now; Plan H-22 in the Plan PR of this amendment |

- **Known limitations.**
  - Until H-22 is met, no repository can push once this decision has merged there (§8). This is intended: a missing leg is not a pass. Claude Code and Codex then use the same two servers (§1).
  - Git bundles must not travel through an agent's context, so the Linux host needs a file channel from the workstation (§3). How it is provided is part of provisioning the server. *Amended 2026-10-22:* the native hand-off archive this item also named is withdrawn (§3).
  - Historical evidence (proof records and PR evidence run on WSL Debian) stays as history and is not rewritten (AD-0018 §6).
