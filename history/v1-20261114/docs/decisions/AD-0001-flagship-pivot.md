# AD-0001 — ArcForges becomes the flagship product; new authoritative repositories

- Status: Accepted (2026-10-12)
- Decider: product owner instruction of 2026-10-12 ("ArcForges Product Pivot — Complete Design and Planning Before Implementation"), recorded by the coordinator
- Supersedes: the ArcScope-centred product-family scope and the parallel delivery model of ArcForges-Design-Parallel and Plan-Parallel for **active** development

## Context

Until 2026-10-11, development followed an ArcScope-centred product-family design (ArcChat, ArcNotes, ArcScope, ArcSlate) and a parallel delivery model. That model ran up to ten concurrent agents competing for one workstation build slot. The delivery run exposed the underlying problem the new product addresses: agents request operations but nothing coordinates the operating-system resources they consume. The 2026-10-11 waiting audit quantified it. Agents spent 56% of their time queueing, a third of locked time was duplicated verification, and earlier sessions held dead locks for hours.

On 2026-10-12 the GitHub repositories were rearranged:

| Repository | Created | Role from 2026-10-12 |
|---|---|---|
| `ArcForges/ArcForges-Design-Parallel` (formerly `ArcForges-Design`) | 2026-09-04 | Frozen history at main `64173614`. Read-only reference. |
| `ArcForges/Plan-Parallel` (formerly `Plan`) | 2026-09-20 | Frozen history at main `5ccbb392`. Read-only reference. |
| `ArcForges/ArcForges-Design` (new) | 2026-10-12 | **Authoritative design** for active development (this repository). |
| `ArcForges/Plan` (new) | 2026-10-12 | **Authoritative plan, delivery graph, ledger and tooling.** |
| `ArcForges/ArcForges` (new) | 2026-10-12 | Implementation repository of the flagship product (node, CLI, MCP adapter, Desktop, installers). |

Working clones: `C:\MyFile\Projects\ArcForges\ArcForges-Design` and `C:\MyFile\Projects\ArcForges\Plan`. Each has a read-only `upstream` remote that points at the corresponding `*-Parallel` repository, with its push URL disabled, so historical records can be cited by commit. The historical local clones `C:\MyFile\Projects\ArcForges-Design` and `C:\MyFile\Projects\Plan` track the `*-Parallel` repositories and are history only.

## Decision

1. **Product.** ArcForges, a cross-platform resource-control and execution platform for AI and automation ([product definition](../product/product-definition.md)), is the first flagship product presented on arcforges.com.
2. **Design authority.** This repository is the design authority for active development. The new design does not inherit the historical corpus by copying it. It cites historical decisions by repository, commit and path where it reuses them, and classifies every reused or retained item in [reuse/inventory-and-classification.md](../reuse/inventory-and-classification.md).
3. **Plan authority.** `ArcForges/Plan` holds the only active delivery graph, execution policy, procedure, entry prompts, ledger and planning tool. Historical claims, leases, roles, ledger records and branches in Plan-Parallel are preserved as history and are never resumed by the new plan ([Plan history/legacy-disposition.md](https://github.com/ArcForges/Plan/blob/main/history/legacy-disposition.md)).
4. **Implementation repositories.**
   - **Active:** `ArcForges` (new product), Contracts, DesktopPlatform, Cloud, Web and Mobile.
   - **Retained for future products, outside the active scope:** ArcScope, ArcSlate and ArcNotes.
   - **Read-only history:** AI (its harness role ended with HAR.40).
5. **Launcher.** The launcher `C:\MyFile\Projects\ArcForges - Final.md` is rewritten to the new single objective. The previous text is archived in Plan `history/`.

## Consequences

- No task, claim or branch of the previous graph is resumed because it still exists. Delivered work is reused through the [classification](../reuse/inventory-and-classification.md), and the new plan schedules only what the new product needs.
- Implementation repositories link to `github.com/ArcForges/ArcForges-Design`, which now resolves to this repository. Their `AGENTS.md` and README references to the old corpus are retargeted by an early delivery task ([Plan](https://github.com/ArcForges/Plan)), so no agent follows a dead historical link.
- Historical links that pointed into `ArcForges/ArcForges-Design/blob/main/...` now break. Citations in this repository therefore always use `ArcForges-Design-Parallel` with an explicit commit.
- Unfinished historical branches and uncommitted files (NAT.01, POL.01, CLOUD.05 and CLOUD.13 worktrees; recorded in the Plan legacy disposition) are preserved untouched and evaluated only through the classification.

## Alternatives considered

- **Continue in the renamed repositories.** Rejected. Their active instructions encode the obsolete scope and the parallel, build-slot delivery model, and a future session could resume them by accident.
- **Import the full history into the new repositories.** Rejected. It would carry 255 design files and a 2.4 MB graph whose active meaning is superseded, defeating the clean authority boundary. Pinned citations give the same traceability.
