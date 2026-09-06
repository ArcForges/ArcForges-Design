# Delivery Planning

This directory contains the implementation dependency model and the numbered work-package sequence derived from the accepted requirements and architecture.

All content here is **authoritative**, and is governed by **D-017** (this is where numbered implementation work packages belong) and **D-019** (one serial numbered sequence, `00 → 01 → 02 → … → NN`, with no predetermined maximum).

## Documents

| Document | Covers |
|---|---|
| [`implementation-sequence.md`](implementation-sequence.md) | The ordering principles that produce the sequence, the completed **D-019** ordering and its prerequisite evidence, the phase structure, the binding mock policy, parallelisation rules, roles, the required per-package format, and what the sequence deliberately does not do |
| [`work-packages/README.md`](work-packages/README.md) | The sequence itself: 51 packages from `00` to `50`, each with its upstream dependencies, plus the downstream dependency index and the scheduling of every open gate |
| [`evidence-driven-revisions.md`](evidence-driven-revisions.md) | Every change the completed prerequisite evidence caused, with the evidence, the affected statement, the correction, the downstream consumers and the verification |

## How to read this layer

1. Read [`implementation-sequence.md`](implementation-sequence.md) first. It explains why the order is what it is, and states the rules every package obeys.
2. Read [`work-packages/README.md`](work-packages/README.md) for the sequence and the dependency graph.
3. Read an individual package only when its upstream dependencies are complete. A package read out of order will reference gates that do not yet exist.

## Rules that govern this layer

- **The sequence is a dependency order, not a schedule.** There are no dates, durations or resourcing assumptions anywhere in it.
- **A package is complete only when its gate is satisfied with recorded evidence** ([`../assurance/release-gates.md`](../assurance/release-gates.md)).
- **A package that discovers a genuine architecture conflict stops and raises it** (**D-001**), rather than resolving it locally.
- **Phase 1 decisions are not reopened here.** Where a package touches a decided area, it implements the decision.
- **One main context advances the sequence serially** (**D-019**).
- **The plan was derived after its prerequisite evidence**, as **D-019** requires — the five Reference Coverage Matrices and the item-level code inventory existed first. An earlier decision that substituted a different ordering is withdrawn and recorded in [`../decisions/phase-2-specification-decisions.md`](../decisions/phase-2-specification-decisions.md) (`P2-002`, superseded by `P2-004`).
