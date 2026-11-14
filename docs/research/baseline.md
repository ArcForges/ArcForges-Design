# Source and delivery baseline — 2026-11-14

The GitHub main branch API was read for every repository below; its SHA matched a clean existing local checkout. No uncommitted product changes were found in these audited checkouts. This work uses separate Design/Plan worktrees. Product repositories are read-only for this migration.

| Repository | Main commit | Last commit UTC |
|---|---|---|
| [ArcForges/ArcForges-Design](https://github.com/ArcForges/ArcForges-Design) | [`62172622550fff73a553135ca178f9b7117c9cbd`](https://github.com/ArcForges/ArcForges-Design/commit/62172622550fff73a553135ca178f9b7117c9cbd) | 2026-11-13T11:56:04Z |
| [ArcForges/Plan](https://github.com/ArcForges/Plan) | [`742ed2660c5e934e1df86f90e54198b3a199e2b1`](https://github.com/ArcForges/Plan/commit/742ed2660c5e934e1df86f90e54198b3a199e2b1) | 2026-11-13T15:08:56Z |
| [ArcForges/ArcForges](https://github.com/ArcForges/ArcForges) | [`10f692224f94916cfc93fbad971f80ec340c5edf`](https://github.com/ArcForges/ArcForges/commit/10f692224f94916cfc93fbad971f80ec340c5edf) | 2026-11-13T15:05:22Z |
| [ArcForges/DesktopPlatform](https://github.com/ArcForges/DesktopPlatform) | [`e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6`](https://github.com/ArcForges/DesktopPlatform/commit/e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6) | 2026-10-25T16:49:51Z |
| [ArcForges/Contracts](https://github.com/ArcForges/Contracts) | [`de3dba76266e89654be9b4d29d097d525a281c6a`](https://github.com/ArcForges/Contracts/commit/de3dba76266e89654be9b4d29d097d525a281c6a) | 2026-11-09T12:48:01Z |
| [ArcForges/Cloud](https://github.com/ArcForges/Cloud) | [`6df33c525fcbc20495e46c9c4c011086146da796`](https://github.com/ArcForges/Cloud/commit/6df33c525fcbc20495e46c9c4c011086146da796) | 2026-11-13T12:50:31Z |
| [ArcForges/Web](https://github.com/ArcForges/Web) | [`56bb40fe7d1693013b4b1e2a82f1b796a65629c5`](https://github.com/ArcForges/Web/commit/56bb40fe7d1693013b4b1e2a82f1b796a65629c5) | 2026-10-22T09:51:12Z |
| [ArcForges/Mobile](https://github.com/ArcForges/Mobile) | [`072ee675e8ea67e779922082dbf65dbc02ed6916`](https://github.com/ArcForges/Mobile/commit/072ee675e8ea67e779922082dbf65dbc02ed6916) | 2026-10-22T09:54:42Z |
| [ArcForges/AI](https://github.com/ArcForges/AI) | [`70f8b22d56d67abd2a983f8b448846731ee22902`](https://github.com/ArcForges/AI/commit/70f8b22d56d67abd2a983f8b448846731ee22902) | 2026-10-11T04:25:21Z |
| [ArcForges/ArcScope](https://github.com/ArcForges/ArcScope) | [`485c8d6d9a84825eb5bc737c9808b8bc4b616643`](https://github.com/ArcForges/ArcScope/commit/485c8d6d9a84825eb5bc737c9808b8bc4b616643) | 2026-10-11T15:39:14Z |
| [ArcForges/ArcSlate](https://github.com/ArcForges/ArcSlate) | [`569785a050c97a8022fe264f6af986285766bf87`](https://github.com/ArcForges/ArcSlate/commit/569785a050c97a8022fe264f6af986285766bf87) | 2026-09-26T04:57:15Z |
| [ArcForges/ArcNotes](https://github.com/ArcForges/ArcNotes) | [`2839da696cf3d6cc8ab3c241212eea8403c5a0a1`](https://github.com/ArcForges/ArcNotes/commit/2839da696cf3d6cc8ab3c241212eea8403c5a0a1) | 2026-09-26T04:57:05Z |

## Current delivery facts

The old graph has 63 tasks: 11 delivered, 8 complete, 36 planned, 8 superseded; none active. Its frozen SHA is `742ed2660c5e934e1df86f90e54198b3a199e2b1`. Completed facts remain historical and none becomes a completed V2 task. Design baseline is `62172622550fff73a553135ca178f9b7117c9cbd`. Both authoritative repositories had no open PR at baseline. The [machine-readable baseline](baseline.json) includes all observed open PR URLs across the audited repositories; those dependency-update PRs were left unchanged.

The [runtime audit](runtime-audit.md) and [cloud audit](cloud-audit.md) distinguish source implementation, historical native acceptance, design-only interfaces, scaffolds and cancelled behavior. A historical pass is not a V2 engine/terminal/composition pass. Windows Job/Linux cgroup execution and resource algorithms are real; current CLI pipes do not establish PTY; Blazor pages are scaffolding; Go commerce provider and some account lifecycle endpoints remain new implementation.

## Verification and access in this design session

GitHub rulesets were read: Design rule `25623782` and Plan rule `24914426` are active, require strict up-to-date `arcforges/windows` and `arcforges/linux`, have no bypass actors, and require resolved review threads. No protection or verification script is changed in this work. The ruleset PR approval count is zero, but the repositories separately require independent review.

No designated Windows or Linux MCP tool is exposed in this session. Discovery for ArcForges plugins returned no connector. This is a current-session capability limitation, not evidence that the owner's hosts are broken. Author static diagnostics may run here; required host statuses and MXC native experiments remain NOT_RUN unless actual host evidence is later obtained. No source-code audit or agent sandbox result is promoted to a native pass.

The repository archive notice and snapshot hashes preserve all previous Design content and Plan graph/ledger. No formal product code, deployment, package publication or data migration is performed by this design task.
