# Delivery Planning

This directory contains the implementation dependency model and the numbered work-package sequence derived from the accepted requirements and architecture.

The [deprecated inputs](../deprecated-inputs/README.md) are excluded from ongoing planning and design-completeness audits. Historical input citations do not require implementers or reviewers to reconstruct design from that archive. A missing definition must be resolved in the current formal design before implementation depends on it.

All content here is **authoritative**, and is governed by **[D-017](../decisions/phase-1-foundation-decisions.md#rule-d-017)** (this is where numbered implementation work packages belong) and **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** (one serial numbered sequence, `00 → 01 → 02 → … → NN`, with no predetermined maximum).

## Documents

| Document | Covers |
|---|---|
| [`implementation-sequence.md`](implementation-sequence.md) | The ordering principles that produce the sequence, the completed **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** ordering and its prerequisite evidence, the phase structure, the binding mock policy, parallelisation rules, roles, the required per-package format, and what the sequence deliberately does not do |
| [`work-packages/README.md`](work-packages/README.md) | The sequence itself: 51 active packages in `00`–`52` (`27`/`29` retired), in their actual dependency order, each with its upstream dependencies, plus the downstream dependency index and the scheduling of every open gate |
| [`evidence-driven-revisions.md`](evidence-driven-revisions.md) | Every change the completed prerequisite evidence caused, with the evidence, the affected statement, the correction, the downstream consumers and the verification |

## How to read this layer

1. Read [`implementation-sequence.md`](implementation-sequence.md) first. It explains why the order is what it is, and states the rules every package obeys.
2. Read [`work-packages/README.md`](work-packages/README.md) for the sequence and the dependency graph.
3. Read an individual package only when its upstream dependencies are complete. A package read out of order will reference gates that do not yet exist.

## Rules that govern this layer

- **The sequence is a dependency order, not a schedule.** There are no dates, durations or resourcing assumptions anywhere in it.
- **A package is complete only when its gate is satisfied with recorded evidence** ([`../assurance/release-gates.md`](../assurance/release-gates.md)).
- **A package that discovers a genuine architecture conflict stops and raises it** (**[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001)**), rather than resolving it locally.
- **Phase 1 decisions are not reopened here.** Where a package touches a decided area, it implements the decision.
- **One main context advances the sequence serially** (**[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)**).
- **The plan was derived after its prerequisite evidence**, as **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** requires — the five Reference Coverage Matrices and the item-level code inventory existed first. An earlier decision that substituted a different ordering is withdrawn and recorded in [`../decisions/phase-2-specification-decisions.md`](../decisions/phase-2-specification-decisions.md) ([P2-002](../decisions/phase-2-specification-decisions.md#rule-p2-002), superseded by [P2-004](../decisions/phase-2-specification-decisions.md#rule-p2-004)).

The [frozen-semantic consumer order](implementation-sequence.md#frozen-semantics-before-the-first-consumer) is binding: content origin, Notes scalar queries and Scope measurement profiles are fully defined before their first schema/contract consumer. Implementers consume those definitions and the per-package vectors; they do not reopen these design decisions.

## P2-009 implementation entry

Implement the adopted [architecture amendment](../decisions/phase-2-specification-decisions.md#rule-p2-009) through the [complete sequence/graph](implementation-sequence.md#9-p2-009-complete-artifact-dependency-graph). Contracts/Platform publish pinned inputs before consumers; C# Cloud is Native AOT, Mobile RN/Hermes, and WP52 owns the sole CF loop. Every active package has an explicit repository/artifact/provider binding and WPxx.90 acceptance. Formal schema/state choices are already fixed; early proof validates the selected choices rather than authorizing ad-hoc redesign.

## Staged artifact integration

Producer existence is a prerequisite, not something every package may assume. A candidate is published to a private immutable feed/channel with its final package version, hash, source and evidence. Promotion changes channel access, never embedded version/bytes. The following stages govern every execution binding and WPxx.90 gate.

| Stage / first producer | Required input | Output and actual proof |
|---|---|---|
| WP00 authority freeze | Accepted Design and permitted inventory evidence | Rules/owner/rights inventory; no generated package or Cloud manifest dependency. |
| WP01 independent roots | WP00 and read-only source disposition inventory | Each root builds its retained source closure using existing locked dependencies; no invented future consumer package. Fenced old code is unreachable. |
| WP02 build/publication governance | WP01 roots and selected build policy | BuildPolicy candidate plus usable isolated restore/pack/feed/signing metadata pipelines. Packaging mechanisms belong here; product signatures/store/public promotion remain WP50. Schema generation and real native capability package proofs have later producers. |
| WP03 Contracts; WP04 foundation values | WP02 policy/pipeline | Handwritten proto/HTTP schemas, descriptors, generated C#/TS public/internal packages and independent fixtures; then Foundation value packages. Each publishes a real candidate; no circular self-restore. |
| WP05/06 policy and actual runtime foundation | Published WP02–04 candidates | Real AOT/native capability packages and minimal host, RN/Hermes/browser/CF/R2 proof. Missing future business handlers are explicitly labelled foundation fixtures. |
| WP07 onward capability/product owners | Only applicable already-produced Contracts/Platform/provider candidates | Publish changed capability packages before the consuming product build, even within one WP. Product clean checkout consumes the feed, never Platform source; record separate producer/consumer commits and hashes. |
| WP21 Cloud consolidation | Prior producer manifests | Cloud assembles the progressively complete integration manifest; future owners are pending. WP23 proves transport/Identity handlers; every later business owner supplies its actual handler/contract proof. |
| WP47 early static slice | WP00/02 content/toolchain and private fixture metadata | Static and design-system proof may use visibly test-only approved-shape offer/download fixtures; no public release/download/price claim. Actual public projection from WP42/44 and released artifacts join at WP50. |
| WP50 family release | Every scheduled real owner and joined manifest | Complete product/RID/Web/Cloud/AI/Contracts closure, real integration/recovery and applicable commercial/store evidence; promote tested immutable artifacts. Partial manifests and mocks cannot close this gate. |

Each package records operation/capability → provider package/version/hash → test scenario → real or fixture → closing WP. At WP23 the real endpoint set is Identity/Workspace/Device plus transport foundation; future Sync/commerce/search/task/simulator handlers remain marked pending for WP25/42/40/52/51. Real object lifecycle closes at WP25. A registered descriptor and a mock HTTP response alone are never that owner's completion evidence. Generated SDK compatibility covers the whole schema from WP03, while real behavioral coverage grows with actual owners. WP50 rejects a missing or fixture-backed release operation.

WP15/19 export-client fixture acceptance closes locally; WP25.08 runs real Cloud Notes/Chat exports. WP17 automation UI closes locally; WP52.06 runs real occurrences/cascade protection and replaces all AI turn fixtures. WP45 rehearses operations already implemented and records remaining recovery/CF cases as pending; WP46 runs actual backup/data restoration, WP52 actual Harness failures and WP50 the combined active/waiting/unknown-effect disaster drill. PG04/L13/paid go-live close only when those combined required records exist.
