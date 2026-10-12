# AD-0013 — Reuse, adaptation, retention and supersession

- Status: Accepted (2026-10-12)

## Decision

1. **Four classes.** Every existing artifact relevant to the new product is classified in [reuse/inventory-and-classification.md](../reuse/inventory-and-classification.md):

| Class | Meaning | Obligation |
|---|---|---|
| **Reuse unchanged** | Used as is (pinned version) | Consumer pins an existing published version; no source change |
| **Adapt** | Used after a bounded change | The change is a named delivery task with its write scope; behaviour not needed by ArcForges stays untouched |
| **Retain (future)** | Kept for future products (ArcScope, ArcSlate, ArcNotes, ArcChat-family services) | Not scheduled, not deleted, not a prerequisite. Repositories and published versions stay as they are. |
| **Superseded** | Replaced for active development by a decision named in the inventory | Historical record kept; active documents no longer cite it as authority |

2. **Conflicts resolve in favour of the new direction** for active development. Each conflict, its resolution and its decision are listed in [reuse/conflicts.md](../reuse/conflicts.md), with historical traceability (repository, commit, path).
3. **Ownership of OS resource control.** Process launching, job objects, cgroups, WSL linking and resource sampling live in the **ArcForges repository**, in projects `ArcForges.Node.Platform.Windows` and `ArcForges.Node.Platform.Linux`. They are the product's core and evolve with it. Future products use these capabilities through the node API, not by linking the controller. This keeps DesktopPlatform's change minimal.
4. **Smallest coherent DesktopPlatform refactor** ([reuse/desktopplatform-refactor.md](../reuse/desktopplatform-refactor.md)):
   - `ArcForges.LocalRpc`: a **service endpoint mode** for a long-lived per-user service with several client kinds. It needs a **stream lane** for long-lived server streams with heartbeats, which the current 10–30 s deadline caps prevent. It also needs **per-method limit profiles** and a **peer identity provider** returning client process id, user and start time.
   - `ArcForges.Security.Secrets`: Linux backends (Secret Service through D-Bus, and the documented 0600-file fallback), behind the existing abstraction.

   No other DesktopPlatform package changes for this product. Unfinished DesktopPlatform features (ContentSandbox Linux TSYNC, Desktop.Shell Avalonia adapter, PLT.66 Contracts move, wrong-user procedures) are **not** prerequisites.
5. **Unfinished historical work** (local branches of NAT.01, POL.01, CLOUD.05, CLOUD.13; CON.43 merged but unrecorded; the other open historical tasks) is preserved and classified, and never resumed implicitly. Where the new plan needs similar capability, it schedules a new task with its own scope. That task may cherry-pick a classified branch only after reviewing it ([Plan legacy disposition](https://github.com/ArcForges/Plan/blob/main/history/legacy-disposition.md)).
