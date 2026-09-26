# Delivery Planning

Execution follows [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018) and [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) with the [CI/local policy](../assurance/ci-and-local-validation-policy.md). Work is scheduled as delivery tasks with typed prerequisites; any number of ready tasks may run concurrently while CPU-heavy local work stays serialized per workstation. Runtime scenarios are scoped local opt-in, not hosted CI or repeated post-merge gates; macOS CI is prohibited. Historical completion evidence is not a rerun requirement.

This directory contains the obligation catalogue (numbered work packages), the delivery model that schedules it, and the producer and integration rules both depend on.

The [deprecated inputs](../deprecated-inputs/README.md) are excluded from ongoing planning and design-completeness audits. Historical input citations do not require implementers or reviewers to reconstruct design from that archive. A missing definition must be resolved in the current formal design before implementation depends on it.

All content here is **authoritative** and is governed by **[D-017](../decisions/phase-1-foundation-decisions.md#rule-d-017)** (planning location and format), **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** (the plan is derived after requirements, architecture, licence matrices and code reconciliation) and [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018) (task-level parallel scheduling, which replaced the serial single-context execution rule of [D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)).

## Documents

| Document | Covers |
|---|---|
| [`delivery/README.md`](delivery/README.md) | **The delivery model**: obligations versus tasks, the typed dependency classes, contract closure readiness, substitutes and progressive integration, task lifecycle, atomic claims, integration ownership and plan changes |
| [`delivery/delivery-graph.json`](delivery/delivery-graph.json) | The single scheduling source: every task, typed edge, substitute, shared resource, package obligation and gate mapping |
| [`delivery/lanes/`](delivery/lanes/) · [`traceability.md`](delivery/traceability.md) · [`substitutes.md`](delivery/substitutes.md) · [`shared-resources.md`](delivery/shared-resources.md) · [`schedule-analysis.md`](delivery/schedule-analysis.md) | Generated views of the graph: task records per lane, obligation and gate coverage, substitute replacement, resource protocols, critical path and throughput analysis |
| [`delivery/adoption.md`](delivery/adoption.md) | The one-time adoption stage that reconciles existing implementation with the graph, in independently claimable slices per repository and lane |
| [`implementation-sequence.md`](implementation-sequence.md) | The dependency model's principles: ordering principles, the binding mock and substitute policy, frozen semantics, roles and the work-package format |
| [`work-packages/README.md`](work-packages/README.md) | The obligation catalogue: 51 active packages in `00`–`53` (`20` future-only; `27`/`29` retired) and the scheduling of every open gate |
| [`producer-artifacts-and-integration.md`](producer-artifacts-and-integration.md) | What each producer must deliver, evidence classes and the candidate lifecycle |
| [`evidence-driven-revisions.md`](evidence-driven-revisions.md) | Every change the completed prerequisite evidence caused, with the evidence, the affected statement, the correction, the downstream consumers and the verification |

## How to read this layer

1. Read the [delivery model](delivery/README.md). It defines how work is selected, claimed, executed and completed.
2. Open the task you are working on in its [lane catalogue](delivery/lanes/); follow its obligation links into the work packages for the authoritative definition of what must be done, tested and accepted.
3. Read an obligation package in full when you work on any of its tasks; its section 9 lists the package's tasks and their prerequisites.

## Rules that govern this layer

- **The delivery graph is a dependency structure, not a calendar.** There are no dates, durations or resourcing assumptions; relative sizes serve only the schedule analysis.
- **A task starts when its own prerequisites are satisfied**, never because a numbered step, a package or a wave has finished ([DLV-24](delivery/README.md#rule-dlv-24), [DLV-25](delivery/README.md#rule-dlv-25)).
- **An obligation is complete only when every task mapped to it is complete with recorded evidence**; a work package is complete only when its gate is satisfied ([`../assurance/release-gates.md`](../assurance/release-gates.md)).
- **A task that discovers a genuine architecture conflict stops and raises it** (**[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001)**), rather than resolving it locally.
- **Phase 1 decisions are not reopened here.** Where a task touches a decided area, it implements the decision.
- **Coordination happens at the narrowest boundary**: repository integration owners for merges and shared files, the Architecture Owner for contract and design changes, the Release Engineering Owner for release tasks ([DLV-29](delivery/README.md#rule-dlv-29), [DLV-30](delivery/README.md#rule-dlv-30)).
- **The plan was derived after its prerequisite evidence**, as **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** requires — the five Reference Coverage Matrices and the item-level code inventory existed first. An earlier decision that substituted a different ordering is withdrawn and recorded in [`../decisions/phase-2-specification-decisions.md`](../decisions/phase-2-specification-decisions.md) ([P2-002](../decisions/phase-2-specification-decisions.md#rule-p2-002), superseded by [P2-004](../decisions/phase-2-specification-decisions.md#rule-p2-004)).

The [frozen-semantic consumer order](implementation-sequence.md#frozen-semantics-before-the-first-consumer) is binding: content origin, Notes scalar queries and Scope measurement profiles are fully defined before their first schema/contract consumer. Implementers consume those definitions and the per-task vectors; they do not reopen these design decisions.

## [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) implementation entry

Implement the adopted [architecture amendment](../decisions/phase-2-specification-decisions.md#rule-p2-009) through the [delivery graph](delivery/README.md). Contracts and DesktopPlatform publish pinned inputs before the tasks that consume them; C# Cloud is Native AOT, Mobile Kotlin/Jetpack Compose, and the Harness tasks own the sole Cloudflare loop. Every task has an explicit owning repository, obligations and evidence, and every active package keeps its `.90` owned-artifact and real-integration acceptance. Formal schema/state choices are already fixed; early proof validates the selected choices rather than authorizing ad-hoc redesign.

## Staged artifact integration

Producer existence is a prerequisite only where a task actually consumes the producer's artifact, and then only for that task. A candidate uses its approved owner feed/channel with exact version, hash, source and evidence; access may be public while publisher credentials remain restricted. Public candidate access and mutable channel pointers do not declare production stability. Promotion never rewrites embedded version/bytes. Contracts development Maven uses the separately defined SNAPSHOT identity/retention protocol; formal releases remain immutable. The following stages describe which kinds of producer each group of tasks consumes; the task edges in the [delivery graph](delivery/delivery-graph.json) state the exact producing task.

| Stage / first producer | Required input | Output and actual proof |
|---|---|---|
| Authority freeze (accepted) | Accepted Design and permitted inventory evidence | Rules/owner/rights inventory; no generated package or Cloud manifest dependency. |
| Independent roots (accepted) | Freeze and read-only source disposition inventory | Each root builds its retained source closure using existing locked dependencies; fenced old code is unreachable. |
| Build/publication governance (accepted) | Independent roots and selected build policy | BuildPolicy candidate plus usable isolated restore/pack/feed/signing metadata pipelines. Product signatures, store and public promotion remain release tasks. |
| Contracts closures; Foundation values | Accepted governance pipeline | Handwritten proto/HTTP schemas, descriptors, generated C#/TS/Kotlin packages and independent fixtures, published closure by closure; Foundation value packages. Each merge publishes a real candidate; no circular self-restore. |
| Policy tests and runtime proofs | The accepted governance outputs and the closures they exercise | Per-repository policy suites and real minimal AOT host, native-header/package, Kotlin Android, browser and Cloudflare/R2 transport proofs, each gating only its own runtime's consumers. Missing future business handlers are explicitly labelled foundation fixtures. |
| Capability and product producers | Only the closures, packages and proofs named by each task's edges | Publish changed capability packages before the consuming product build. A product clean checkout consumes the feed, never Platform source; producer and consumer commits and hashes are recorded separately. |
| Cloud foundation and modules | The Cloud foundation tasks and the module's own closures | Cloud assembles the progressively complete integration manifest; each business owner supplies its actual handler and contract proof; unfinished owners are pending, never fixtures in a release build. |
| Early static site | Accepted content/toolchain and private fixture metadata | Static and design-system work may use visibly test-only approved-shape offer/download fixtures; no public release/download/price claim. Actual public projection from commerce and policy owners and released artifacts join at release. |
| Family release | Every release-readiness task and the joined manifest | Complete product/RID/Web/Cloud/AI/Contracts closure, real integration/recovery and applicable commercial/store evidence; promote tested immutable artifacts. Partial manifests and substitutes cannot close this gate. |

Each task records operation/capability → provider package/version/hash → test scenario → real or substitute → removing task. Generated SDK compatibility covers the whole schema published so far, while real behavioral coverage grows with actual owners. A registered descriptor and a mock HTTP response alone are never an owner's completion evidence, and the family release rejects a missing or substitute-backed release operation.

Export-client and automation-client substitute acceptance closes locally in the assistant and ArcNotes tasks; the real Cloud export producer, the Harness automation scheduler and the fixture-removal tasks named in the [substitute registry](delivery/substitutes.md) replace them. Operations tasks rehearse what is already implemented and record remaining recovery and Cloudflare cases as pending; backup and data restoration, Harness failures and the combined active/waiting/unknown-effect disaster drill are separate tasks whose evidence the release tasks join.

Start with [producer artifacts and real integration](producer-artifacts-and-integration.md). [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010) fixes complete initial C#/TS/Kotlin contracts, complete functional native package delivery, Android-only implementation and explicit mock replacement. All 51 active packages remain required under their accepted scope. The [family completion review](../assurance/family-design-completion-review.md) records the earlier document review and the remaining implementation gates.

The earlier [producer and local gRPC review](../assurance/producer-and-local-grpc-closure-review.md) remains historical evidence. The [Cloudflare and application assistant review](../assurance/cloudflare-app-assistants-review.md) records the graph, contracts, package producers and evidence limits at its date.

## Current implementation profiles

[P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) uses [concrete project/package producers](../architecture/27-platform-projects-and-application-assistants.md), [D1](../architecture/data-model/04-d1-execution-profile.md), [history](../architecture/data-model/05-application-history.md), [scope/streams](../architecture/contracts/10-application-scope-and-streams.md) and [complete client UX](../experience/README.md). All 51 active packages include these where applicable. WP20 is [future only](../future/cross-product-collaboration/README.md), with no current dependency or gate.

Current coordinated repair: [P2-014](../decisions/phase-2-specification-decisions.md#rule-p2-014); see [final findings verification](../assurance/final-findings-remediation-verification.md). Earlier dated reviews retain their evidence baselines; real runtime and commercial gates remain separate and open.

## Accepted implementation baseline

[WP02 stage acceptance](../assurance/wp02-stage-acceptance.md) closes build/publication governance under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). [WP03.00](../assurance/wp03-00-implementation-evidence.md), [WP03.01](../assurance/wp03-01-implementation-evidence.md) and [WP03.02](../assurance/wp03-02-implementation-evidence.md) completion receipts accept the contract project structure, the foundation schema and the serialization posture under their approved profiles; [F-026](../assurance/open-gates-register.md#rule-f-026) remains open for the generated-client AOT proof. Implementation is complete through Substep 03.02; Substep 03.03 has not started, and its closures are open delivery tasks. The ordered execution steps inside those dated profiles and receipts, including advancing a Plan Current task, are historical records superseded by [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018); they are not execution instructions. None of these receipts closes WP03 or a later runtime or commercial gate.
