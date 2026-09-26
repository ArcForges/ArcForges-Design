# Adoption Stage

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018) (decision 6), [DLV-22](README.md#rule-dlv-22)
> Tasks and slices: the [adoption lane](lanes/adoption.md) of the [delivery graph](delivery-graph.json)

The adoption stage is the one-time reconciliation between the implementation that already exists and the task structure of the [delivery model](README.md). It is **defined here and not executed by the planning change that introduced it**. Nothing in this document certifies existing implementation as conforming: it defines who reviews what, against which evidence standard, and what each review must record before normal parallel execution begins in a repository lane. Section 4 lists observations made while the plan was researched; they are inputs to the reviewers, not review results.

**Historical baseline.** At introduction, implementation was complete through [WP-03.02](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02): the accepted receipts of WP00, WP01, WP02 and [WP-03.00](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.00)–[WP-03.02](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02) are carried by the accepted-baseline tasks `GOV.01`–`GOV.03` and `CON.90`–`CON.92`. [WP-03.03](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) had not started; its closures are the tasks `CON.02` and `CON.03`. No other existing work was accepted by that baseline; current progress is recorded in the merged ledger.

## 1. Responsibilities

| # | Rule |
|---|---|
| <a id="rule-adp-01"></a>ADP-01 | **Review against the new definitions.** For every delivery task in its scope, the adoption reviewer compares the repository's main branch, open pull requests and accepted receipts with the task's outcome, obligations or named parts, write scope, validation and evidence fields. |
| <a id="rule-adp-02"></a>ADP-02 | **Classify each task exactly once:** *inherited* — accepted or newly reviewed evidence satisfies every mapped obligation part; *inherited with adjustment* — the existing work stands but concrete named changes remain, recorded as the task's remaining scope; *gap* — the outcome does not exist, although scaffolding may; *conflicting* — existing work contradicts current design and is raised under [D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001) before dependent work proceeds. |
| <a id="rule-adp-03"></a>ADP-03 | **Evidence standard for inheritance.** Only reviewed evidence counts: an accepted receipt, or merged source with its retained applicable CI results and publication receipts that the reviewer checks against the task's evidence field. Hello World bootstraps, probes, generated contracts without their vectors, historical dated reviews, plans and unmerged branches are never inherited as completed product behavior; work without merged source and recorded evidence stays open. |
| <a id="rule-adp-04"></a>ADP-04 | **Map results to the new structure.** Each inherited result names the task and part it satisfies. Existing work that serves an obligation mapped to another repository's task is recorded for that repository's reviewer, not silently claimed. Required adjustments that do not fit an existing task's scope become a planning change that adds a task; obligations never move out of scope. |
| <a id="rule-adp-05"></a>ADP-05 | **Record a slice, then open its lane.** Adoption is performed in independently claimable slices, one per repository and lane ([DLV-22](README.md#rule-dlv-22)). When a slice record is merged in the Plan ledger, the tasks of that lane in that repository become eligible under the normal dependency-readiness rule, subject to their recorded classification and unresolved findings, while other slices of the same repository and every other repository remain under review. Several slices may be reviewed in one pull request, each with its own record. |
| <a id="rule-adp-06"></a>ADP-06 | **No verification cycle.** Adoption reuses existing receipts and CI results. It performs no public downloads, repeated publication checks, installed-consumer runs, device or hosted runtime tests, and it does not rebuild products except where a task's own evidence field requires a local check that has never been run, under [P2-017](../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| <a id="rule-adp-07"></a>ADP-07 | **Bind planned scopes to the actual layout.** A task's write scope names planned additions, not existing code. Before a task's first edit, its slice (or the task itself) binds the scope to the repository's actual project, namespace and source-inventory layout and records any required project, lock or inventory addition as an explicit adjustment. Existing package identities, installation identities and accepted source are never renamed or rewritten to match a planned path. |
| <a id="rule-adp-08"></a>ADP-08 | **Blocked slices stay local.** A slice whose source, tool, environment or contract cannot be reconciled records the concrete blocker and the tasks it affects; other slices and repositories continue. A missing optional environment is recorded as untested scope, not as a new provisioning task. |

## 2. Stage structure

The baseline freeze runs once; every slice, repository record and the documentation reconciliation can then run in parallel.

| Unit | Owner | Scope |
|---|---|---|
| Baseline freeze (`ADOPT.01`) | Plan | Record each repository's main head, open pull requests and branches, the latest published candidate per registry and the ledger skeleton. |
| Adoption slice (`ADOPT.NN.<lane>`, one per repository and lane) | That repository's integration owner or a reviewer they assign | Apply [ADP-01](#rule-adp-01)–[ADP-05](#rule-adp-05) and [ADP-07](#rule-adp-07) to the tasks of that lane in that repository, including recording accepted-baseline tasks in scope as inherited. The [slice table](lanes/adoption.md#adoption-slices) lists every slice and the tasks it opens. |
| Repository record (`ADOPT.02`–`ADOPT.10`) | That repository's integration owner | Record the repository-wide facts once — main head, retained CI workflow inventory under [P2-017](../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory — for the slices to cite; the record closes when every slice of the repository is complete. |
| Documentation reconciliation (`ADOPT.11`) | Design and Plan | Resolve documentation findings that affect adoption decisions, confirm the generated views match the graph, and keep the ledger's slice status current. |

Exit: a slice is complete when its record is merged in the Plan ledger with a classification for every task in its scope. Before implementation, each worker reads its merged slice classification and later adoption adjustments, reuses inherited evidence and implements only the recorded remaining scope for inherited-with-adjustment work. An unresolved conflict or blocker stops only the affected task and is recorded in its claim; [D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001) governs conflict resolution, and dependency readiness never overrides that restriction. Otherwise normal execution starts immediately under [DLV-22](README.md#rule-dlv-22); a task whose prerequisites belong to another lane or repository stays blocked only on those prerequisites. A slice may cite repository-wide facts before the repository record closes; a later finding in the repository record that changes a slice's classification is recorded as an adjustment to the affected tasks.

## 3. Ledger records produced by adoption

| Record | Location in Plan | Content |
|---|---|---|
| Baseline | `ledger/adoption/baseline.md` | Repository heads, open pull requests and branches, latest candidates |
| Slice | `ledger/tasks/adopt-nn-<lane>.md` with `status: complete` (for example `ledger/tasks/adopt-03-contracts.md`) | One row per task in the slice: classification, evidence references, bound write scope, remaining scope, conflicts raised, blockers |
| Repository record | `ledger/adoption/<repository>.md` and `ledger/tasks/adopt-nn.md` | Repository-wide facts, links to every slice record and the combined classification table |
| Inherited task | `ledger/tasks/<key>.md` with `status: inherited`, where the key is the task identifier in lower case with dots replaced by hyphens | Obligation parts satisfied, receipts and source commits relied on, untested coverage carried forward |
| Planning change | Design and Plan pull requests | New or adjusted tasks for adjustments that do not fit existing scope |

## 4. Observations recorded while planning (unreviewed inputs)

Recorded 2026-09-23 from the repositories' main branches and rechecked on 2026-09-24, when every head was unchanged. These are facts for the reviewers to confirm, not classifications.

| Repository (main head) | Observed state | Known adjustment candidates |
|---|---|---|
| Contracts (`e6c4a77`) | Accepted foundation and serialization posture ([WP-03.00](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.00)–[WP-03.02](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02)) and the 22 published package identities; foundation records include ResourceRef, ResourceVersionRef, BlobRef and ArtifactRef. [WP-03.03](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) has not started: there are no capability, action, context, version or health descriptor records, no oversized-body reference record and no business service definitions beyond the bootstrap examples. | Shard the shared constraint files before concurrent closures (`CON.01`); consumer repositories still pin pre-foundation candidates. |
| DesktopPlatform (`fe8476d`) | Accepted build governance, dependency admission and lockstep NuGet publication; building-block projects are placeholders; native families are probe-level (version, build and error exports) with no instruments library; no downstream consumer of its packages. | Its design-policy check validates the retired work-package graph and serial order; it must be replaced by delivery-graph validation before the Design pin moves (see section 5). |
| ArcNotes (`268c329`), ArcScope (`5e68634`), ArcSlate (`1214224`) | Native AOT bootstraps with accepted build identity and dependency policy; no product domain code. | None beyond adopting the accepted build baseline. |
| Cloud (`ce0a32a`) | Bootstrap Native AOT host and deployment pipeline with build-once, serialized deployment; no product modules, D1 plans, R2 lifecycle or backup code. | Pin the current Contracts candidates when module work starts. |
| AI (`233d1e3`) | Bootstrap Worker and Workflow scaffolding with dependency admission; no Harness behavior. | None beyond the accepted baseline. |
| Web (`120f209`) | Working static-site generator and canonical-host Worker; the Account and Chat application is a placeholder. | Update the stale Contracts SDK pin when the first consumer task starts. |
| Mobile (`d32df20`) | Android bootstrap with the development package identity and a preview-only shared module; transport probe client. | Package identity migration to the permanent Android identity is an existing obligation of the Android foundation task. |
| Design (this repository) | DesktopPlatform's existing corpus checker reports 26 link errors and 35 unclassified identifier occurrences that predate the delivery model (mostly links labelled with the validation-policy decision that point to the policy document); the delivery model resolved 4 and added none. | Restore citation integrity before the DesktopPlatform pin moves. |

## 5. Required documentation-tool adjustment

DesktopPlatform's `eng/design_graph.py` and `eng/design_policy.py` validate the work-package header and section 9 tables, the retired package-level forward and reverse tables, the serial execution line and edge counts, and derive the set of active invariant owners from that serial order. Under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018) the corresponding specification in [design policy export](../../architecture/29-design-policy-export.md) now requires validation of the delivery graph instead. The DesktopPlatform governance slice (`ADOPT.02.governance`) records this as an adjustment, and the replacement is implemented through its specification-integrity policy task (`GOV.14`) before DesktopPlatform moves its pinned Design commit. Until then the existing pin remains valid for its glossary and invariant exports. This planning change does not modify DesktopPlatform.
