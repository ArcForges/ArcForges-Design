# Explicit non-goals and retirement boundary

The following are retired from current product delivery: product MCP servers/adapters; Claude/Codex hooks; AI Harness, session interpretation, agent/subagent scheduling; Task/Attempt queues, DAG dependencies, automatic retries, result caches; toolchain registries and compiler adapters; sccache/ccache integration; cache-hit analytics, CAS/dedup/shared cache; managed Git worktrees and automatic archives; general disk cleanup; obsolete Center workspace/search/edit services; LAN placement, distributed compilation and cache sharing; Android/iOS and standalone desktop clients; GUI application sandboxing; the old C# Center runtime; bespoke isolation that duplicates MXC.

No placeholder contracts, tables, projects or abstraction layers are introduced for plugins, a marketplace, network-management extensions, GPU scheduling or advanced future features. Ordinary programs may use their own caches inside their sandbox; ArcForges neither classifies nor tunes those caches.

The repository audit differentiates real old implementations from aspirational projects. Remove actual modules and their package/build/schema/route consumers after replacement gates. Do not invent a deletion for a module that never existed. Preserve required historical migrations and already published packages as immutable evidence. A historical file is not an active compatibility runtime.

Shared DesktopPlatform and Contracts components used by ArcScope, ArcSlate, ArcNotes, AI or Mobile are not deleted because ArcForges changed direction. Those products are not V2 prerequisites. Their continued existence does not bring their features into V2.

Development MCP access to the Windows and Linux verification hosts is retained. Retiring product MCP does not authorize disabling those hosts, repository checks, review gates or protections.
