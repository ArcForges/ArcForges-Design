# AD-0018 — Native Windows and native Linux, without dedicated WSL integration

- Status: Accepted (2026-10-21; the product owner's scope correction of that day)
- Decider: the product owner
- Supersedes for the active product: [AD-0005](AD-0005-resource-enforcement.md) "WSL2 model" items 1–3 (the guest link, guest capacity and accounting, coordinated admission), [03 resource control](../architecture/03-resource-control.md) §6 (WSL host–guest coordination), [09 LAN](../architecture/09-lan.md) §9 (WSL guests), the state machine SM-GUEST-LINK, requirements R-RES-010 and R-RES-011, and Plan task AF-WSL-01
- Amends: [AD-0002](AD-0002-platform-scope.md) (scope wording and the Linux validation venue), [AD-0003](AD-0003-architecture-and-runtimes.md) (the `bridge wsl` role), [AD-0004](AD-0004-contracts-and-state.md) (the host–guest transport), [AD-0005](AD-0005-resource-enforcement.md) item 4 (restated in §2 below), [AD-0008](AD-0008-lan-trust-and-placement.md), [AD-0011](AD-0011-identity-and-login.md), [AD-0013](AD-0013-reuse-and-supersession.md), [AD-0016](AD-0016-local-first-verification.md) §3 (the verification topology, §5 below)
- Related: [01 system overview](../architecture/01-system-overview.md), [16 testing strategy](../architecture/16-testing-strategy.md), [contracts](../contracts/README.md) §7, [node store](../data/node-store.md)

## Context

The design had a dedicated Windows–WSL integration: a guest node in each managed WSL2 distribution, linked to the Windows host node through `arcforges bridge wsl`, with one fair queue spanning host and guests, a CPU and memory split that summed to the host's budget, leases, reservations during link loss and a boot marker for restarted distributions (AD-0005 "WSL2 model", 03 §6, AF-WSL-01). None of it was implemented; the contracts of AF-CON-01 already declare its wire surface.

On 2026-10-21 the product owner dropped that integration. The reasons recorded with the decision:
- WSL2 is a Linux virtual machine, not a normal Windows process environment. Windows job objects cannot control the Linux processes inside it as Windows processes.
- Each operating system already has its own native mechanisms: job objects on Windows, systemd and cgroups v2 on Linux. A Windows node controls Windows workloads; a Linux node controls Linux workloads.
- No Windows–WSL bridge, guest coordination, shared resource scheduling or special WSL management is required.

The same day the owner removed local WSL Debian as a dependency of the development workflow: Linux development and validation run in an independent Linux environment, and Windows validation runs on the native Windows workstation (§5).

## Decision

1. **Platform scope.** ArcForges supports native Windows 11 and native Linux (glibc, a systemd user manager, cgroups v2) independently. macOS stays a future target ([AD-0002](AD-0002-platform-scope.md) Direction). WSL is not a separately supported product target.
   - A user may run the general Linux node inside a compatible WSL2 distribution (systemd enabled, user delegation of cpu, memory and pids). It is then an ordinary Linux node: the same code, the same mechanisms, no detection of or special behaviour for WSL, and no WSL-specific acceptance guarantee.
   - No Windows–WSL bridge, guest node, host–guest link, guest budget, shared queue, coordinated admission or WSL-specific management is designed, implemented or claimed.
   - General cross-platform abstractions (the execution-platform seam of AD-0002), LAN peers ([09](../architecture/09-lan.md)), remote nodes and the cloud fleet are unchanged. A Linux node inside WSL2 is a separate machine-level node like any other; it can pair over the LAN like any other Linux node, with no host relationship to the Windows node.
2. **What the Windows node still states about WSL** (the surviving half of AD-0005 item 4 and R-RES-011, now part of R-RES-002). The WSL VM is observed like any other virtual machine: one consumer labelled `GUEST_VM`, part of unmanaged load in the budgets, never summed from guest-internal processes. A Windows task that runs `wsl.exe` (or any launcher into a VM) is flagged `crosses_vm_boundary`; the Linux processes it starts are outside the Windows job and are never presented as controlled.
3. **Retired v1 wire surfaces.** The contracts of AF-CON-01 are published and their v1 rules are additive only ([contracts](../contracts/README.md) §7), so the guest-link declarations stay declared for wire compatibility. They are **retired**: no node serves, calls, sets or relies on them, no client shows them, and no later change extends them. A future major version may drop them.
   - `arcforges.peer.v1.GuestLinkService` and its messages (`GuestHello`, `GrantRequest`, `GrantRelease`, `GuestUsageReport`, `GrantDecision`).
   - `ResourceService.ListGuestLinks`, `SetGuestLink`, `GetHostLink` and `TrustHost`, with `GuestLinkView` and `GuestLinkState`.
   - `NODE_ROLE_GUEST` (every node is `NODE_ROLE_HOST`), `NodeRef.host_node_id`, `ORIGIN_GUEST` and `ORIGIN_HOST`, `ResourceSnapshot.guests` and `GuestConsumer`, `NodeInfo.guest_links`, `EVENT_TOPIC_GUESTS` and `NodeEvent.guest_link`, `FINDING_KIND_GUEST_LINK_LOST`, `ResourcePolicy.guest_standalone_fraction`, `ProbeObservation.wsl_distro`, the fleet's `role` and `host_node_id` for guests, and the error `STATE/link_down`.
   - **Still in use:** `PROCESS_LABEL_GUEST_VM` and `ProcessView.crosses_vm_boundary` (§2).
4. **Retired node-store tables.** The node store schema is expand-only ([13](../architecture/13-distribution-updates.md) §9), so `guest_link`, `host_link` and `guest_grant` stay in schema v1, are never written, and are dropped only by a future major schema. `store_meta.node_role` is always HOST.
5. **Verification topology** (amends [AD-0016](AD-0016-local-first-verification.md) §3; the merge gate of §1 and the job classes of §2 are unchanged).
   - **Legs.** Each step of `eng/verify_steps.py` runs on one host, `win` (native Windows) or `linux` (native Linux); a host's steps are the commit's leg for it. `eng/verify.py` runs only the leg of the machine's own operating system, never through WSL, a VM bridge or a remote shell.
   - **Where.** The Windows leg runs on the owner's Windows 11 workstation, in an isolated worktree at the exact commit; a cloud session reaches it through the owner's Windows-MCP connection. The Linux leg runs on a native Linux machine: the Claude Code Cloud Linux environment for steps it can run, and a real Linux host with a systemd user manager and cgroups v2 delegation for steps that need them. Local WSL Debian is not a dependency.
   - **Exact commit.** Each leg checks out the commit itself (a detached worktree on Windows, a Linux-native clone on Linux). A commit that is not yet on GitHub reaches the other machine as a Git bundle, which Git verifies object by object.
   - **Pass records.** A passed leg writes a record keyed by the commit's tree (its exact commits when a step reads history), the merge base, the profile, the leg's host and step set, the scripts and the step table's context (such as the Plan's Design main commit). The record of a leg that passed on another machine is accepted with `python eng/verify.py import`, which recomputes the key and refuses any mismatch or any step that did not pass. A push needs a passed or imported record for every leg of every pushed commit; one missing leg rejects the push, as one failed step does.
   - **Real-OS checks never degrade silently.** A Linux leg whose steps need a systemd user manager or cgroups v2 delegation checks for them first and fails when they are missing, so tests that would skip with a reason elsewhere cannot pass a leg on a machine without them.
   - **PR evidence.** The PR quotes each leg's `LEG PASS` line (machine, tree, profile) and the combined `arcforges-verify: PASS` line at the pushed head. The rules for agents of AD-0016 §3 apply unchanged.
6. **Documents.** Superseded text stays as history and names this decision ([AD-0013](AD-0013-reuse-and-supersession.md)); research records are not rewritten.

## Consequences

| Changed | Effective |
|---|---|
| [AD-0002](AD-0002-platform-scope.md): scope "Linux, including a Linux node a user runs in WSL2, without integration"; the Linux validation venue is a native Linux machine | now |
| [AD-0005](AD-0005-resource-enforcement.md): "WSL2 model" items 1–3 superseded; item 4 restated as §2 | now |
| [03](../architecture/03-resource-control.md): guest terms leave the budgets (the WSL VM is unmanaged load); §6 superseded | now |
| [09](../architecture/09-lan.md) §9, [01](../architecture/01-system-overview.md) topology T2, the bridge role, guest origins and trust boundary B2: superseded | now |
| SM-GUEST-LINK retired: never entered, kept as history because the retired `GuestLinkService.OpenLink` annotation of the v1 protos names it; `guest_link`, `host_link`, `guest_grant` retired (§4) | now |
| R-RES-010 and R-RES-011 retired; R-RES-002 carries §2; R-TOOL-001, R-DIAG-004, R-API-002, R-RES-008 lose their guest wording; real-test venues read "native Linux" | now |
| Plan: AF-WSL-01 superseded; AF-SCHED-01 and AF-ACC-01 lose their WSL terms; M2 and M3 outcomes restated | the Plan PR of this decision |
| Contracts: the surfaces of §3 documented as retired (a machine-readable `retiredOperations` marking of the guest-link RPCs needs the Contracts dependency-input review and is left to it) | the Contracts PR of this decision |
| [AD-0016](AD-0016-local-first-verification.md) §3: the verification topology of §5 | each repository's verification PR |

- **Known limitations.**
  - Users who relied on the documented Windows-plus-WSL coordination lose it: a Linux node in WSL2 and the Windows node budget independently, and the Windows node sees the WSL VM only as unmanaged load.
  - Retired wire declarations remain in the v1 packages until a major version.
  - The Linux real-OS steps (systemd units, cgroups) need a real Linux host; until one is available to a repository, its Linux leg cannot pass there and pushes are rejected. Using a WSL2 distribution as that Linux host is allowed (§1) but is not a development dependency.
  - The OS secret-store tier's Linux leg is opt-in and outside routine verification; its isolated venue ([AD-0016](AD-0016-local-first-verification.md) §5 amendment) is unchanged by this decision.
