# PRP-0001 — Network management, plugins and product positioning

- **ID:** PRP-0001
- **Status:** Saved, not researched
- **Saved:** 2026-10-21, at the product owner's request
- **Kind:** architectural research and feasibility study; no implementation and no roadmap promotion
- **Related:** [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) (§7 adapter and plugin foundations (RM-11, EX-01), §8 extensions, §9 roadmap governance), [AD-0017](../decisions/AD-0017-delegated-execution-direction.md), [AD-0012](../decisions/AD-0012-distribution-and-updates.md), [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md), chapters [17](../architecture/17-delegated-execution.md) and [18](../architecture/18-application-workload-control.md), the canonical [roadmap](https://github.com/ArcForges/Plan/blob/main/roadmap.md)
- **Use:** only when the owner explicitly requests PRP-0001; see [README](README.md). Saving it authorizes neither the research nor any implementation.

## Prompt

The text between the quotation marks is the prompt, verbatim as saved.

```text
"
Conduct a comprehensive architectural research and feasibility study on extending ArcForges with network management, a general-purpose plugin ecosystem, and any necessary refinement of its product positioning.
ArcForges is a cross-platform, local-first application and workload control infrastructure. Its purpose is to provide a coherent management, coordination, policy, and reporting layer over the mechanisms each operating system genuinely supports.
The research must build upon the existing ArcForges architecture, particularly AD-0015, AD-0017, the application/workload control model, existing resource and disk management, the capability-reporting framework, and the current Roadmap.
Do not assume that the product positioning must change. Determine whether these extensions are already covered by its established purpose or whether a carefully justified refinement is necessary.
Network management
Investigate network capabilities as another major resource and policy dimension alongside CPU, memory, disk, and process lifecycle management.
Cover application-level traffic monitoring, upload and download bandwidth control, traffic accounting, network permissions, connection restrictions, DNS policies, routing, proxy integration, and application-specific network rules.
Examine supported native Windows, Linux, and future macOS mechanisms, their limitations, privileges, and actual enforcement guarantees.
On Windows, investigate Job Object network rate control, Windows Firewall, and WFP, without assuming that a custom kernel driver is required or desirable.
Use sing-box as a technical reference for network management concepts, including rule matching, application identification, DNS, routing, and supported non-VLESS proxy transport integration.
The goal is not to recreate sing-box or build an unrestricted proxy-protocol ecosystem. Determine what belongs in ArcForges Core, what should be an optional network backend, and what should be provided by plugins or external integrations.
Distinguish network observation, bandwidth shaping, access enforcement, and traffic routing. Never treat proxy configuration as equivalent to OS-enforced network confinement.
General-purpose plugin ecosystem
Research a flexible plugin architecture that extends ArcForges beyond its built-in capabilities without compromising the trusted core.
Plugins must not be limited to network functions.
Potential plugin categories include networking, storage and disk management, application identification, policy templates, permission management, diagnostics, automation, developer tools, cache backends, and external integrations.
Study the appropriate Core APIs and capability boundaries so plugins can request operations through controlled interfaces rather than bypassing the core's resource, execution, permission, lifecycle, and audit mechanisms.
Investigate Native AOT compatibility, out-of-process plugin execution, versioned contracts, plugin isolation, permission declarations, user authorization, capability negotiation, compatibility, error handling, and recovery.
Consider how ArcForges can recognize installed applications, associate reliable identities with running processes, select applicable policies or scripts, obtain authorization where necessary, apply OS-specific controls, verify their effects, and safely restore the previous state.
Avoid building a generic privileged script executor disguised as a plugin system.
Plugin distribution and trust
Research an end-to-end distribution model using Cloudflare R2 where appropriate.
Cover plugin package formats, manifests, version compatibility, source repositories, reproducible or attestable builds, cryptographic signatures, integrity checks, open-source review, security auditing, permission review, installation, updates, revocation, rollback, and removal.
Investigate how persistent operating-system changes made through plugin capabilities are recorded and reversed safely.
The lifecycle must form a complete, reviewable loop from publication to verification, installation, operation, update, revocation, and uninstall.
Prefer existing ArcForges distribution, signing, auditing, and lifecycle infrastructure instead of inventing independent systems.
A marketplace must not require charging for local functionality.
Architectural integration
Reassess the relationship between application identity, policy enforcement, resources, permissions, plugins, native platform backends, and user-controlled automation.
Identify functionality already designed, functionality already implemented, missing capabilities, duplication risks, and unsupported assumptions.
Determine which components must remain trusted Core functionality and which can safely become extensible.
Maintain the established Windows/Linux native platform direction, with macOS remaining a future target. Do not revive dedicated WSL integration.
Respect ArcForges' existing security principles, Native AOT direction, local-first operation, honest capability reporting, and explicit user control.
Expected research outcome
Produce evidence-backed architecture options, technical feasibility comparisons, a coherent recommended direction, clearly identified gaps, security and compatibility risks, and proposed Roadmap adjustments.
Include independent critical review and unresolved product-owner decisions.
Keep observed facts, supported mechanisms, proposals, and unverified assumptions clearly separated.
Do not implement functionality or promote Roadmap items into delivery tasks without explicit authorization.
The final recommendation must explain whether this direction meaningfully strengthens ArcForges as a general-purpose application and workload control platform, and what should be prioritized when implementation is eventually authorized.
"
```
