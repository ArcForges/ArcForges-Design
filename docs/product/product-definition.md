# Product definition — ArcForges V2

## 1. Purpose and user

ArcForges runs general command-line programs and their managed descendants inside an OS-backed sandbox, retains each sandbox's private data, and coordinates CPU and memory so the owner can continue using the computer. It supports shells, scripts, compilers, tests, interactive terminal tools, AI CLIs and long-running command-line services without understanding their internal business logic. A program's internal commands are not separately scheduled tasks.

The product has one execution core. The local CLI is a first-class client. The optional Go Center connects enrolled devices and routes explicitly authorized management requests to that same core. A responsive Blazor Web dashboard provides overview, devices, sandboxes, runs, resources, security and account/subscription pages. No separate desktop or mobile client is required.

## 2. Commercial boundary

The open-source distribution includes local execution, resource control, data management, the Go Center, and the corresponding Web dashboard. Local operation requires neither account nor subscription nor network connectivity. Self-hosted Center users get remote management without contacting official entitlement infrastructure. Official hosted node connections and remote management require the official subscription service; the hosted dashboard belongs to that service. Subscription expiry affects new hosted access and remote command admission, never already running local workloads or access to local data.

Prices, paid quotas, trial terms, payment activation and provider configuration are undecided business settings. Do not embed guessed prices or create local paid-feature switches. Operator-configured limits on a self-host are local administration, not a dependency on an official entitlement.

## 3. Supported product surface

| Object/surface | User outcome |
|---|---|
| Sandbox | Persistent named environment with private data root, explicit host access, network policy and resource policy |
| Run | One execution in a sandbox, with its whole descendant process group, immutable launch snapshot, output, exit and resource records |
| Local CLI | Create/configure/list/inspect/delete, start/attach/detach/stop, import/export/usage and resources, with normal terminal interaction |
| Resource manager | Observe host and managed usage, reserve host headroom, allocate bounded budgets, verify OS-applied limits and explain pressure actions |
| Go Center | Accounts, devices, enrollment, authenticated outbound node channel, grants, typed management routes, audit and hosting entitlements |
| Blazor Web | Modern responsive remote management, useful loading/offline/error states, explicit destructive-action previews and exact operation status |

Initial native platform profiles are Windows ProcessContainer and native Linux Bubblewrap, using official stable MXC distribution contracts. No WSL, macOS or GUI-app profile is part of this delivery. OS/build and privilege eligibility are checked using actual backend capability probes; a version string alone never establishes isolation. Detailed prerequisites and known stable SDK limitations are in [02](../architecture/02-mxc-integration.md).

## 4. Product truth and completion

Sandbox persistence is filesystem and metadata persistence, not a promise of a persistent MXC container or a memory snapshot. Detach changes a terminal attachment, not Run lifetime. A Node restart is distinct from RunSupervisor failure or machine reboot. A Run continues after a Node reconnect only when the supervisor and its verified confinement remain alive. A host reboot ends all runs; V2 does not silently restart programs.

A private data root and environment variables improve data locality. They do not transparently redirect arbitrary absolute writes. Undeclared host writes must be rejected by confinement; an explicitly writable host grant is an intentional exception visible in inspect and delete preview. Direct filesystem observations and native tests, not path naming, establish containment.

A full V2 release requires both native platform profiles to pass the mandatory engine, terminal, resource, filesystem, network, lifecycle and recovery experiments. Development work can be merged in a disabled capability profile; such a profile is not presented as complete support. An unresolved engine combination is a real delivery gate with a named owner and next action, never a reason to substitute pipes for a terminal or an uncontained process for a sandbox.
