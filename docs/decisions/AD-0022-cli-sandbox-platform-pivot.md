# AD-0022 — ArcForges CLI Sandbox Platform Pivot

- Status: Accepted product and architecture direction; runtime combinations remain subject to named verification gates.
- Date: 2026-11-14
- Decision owner: product owner, through the supplied ArcForges V2 migration instruction.
- Scope: current Design and Plan; this decision does not claim product code delivery.

## Decision

ArcForges becomes the open-source general CLI sandbox and intelligent resource-management platform specified in [product definition](../product/product-definition.md). Microsoft MXC official stable SDK/API and shipped official executable contracts provide isolation and payload creation. The platform preserves proven resource-observation and budgeting algorithms, reworks their coupling to the old scheduler, and deletes redundant/retired product implementations after their replacements are verified.

The primary model is persistent Sandbox plus one-execution Run. Local CLI is a full offline-capable path. The optional Go Center and Blazor Web management product use the same constrained Sandbox Core. Local and self-hosted use is free; only official-hosted service access is subscription-gated. The official service can manage devices owned by the user; it is not a cloud compute service and cannot bypass local host grants.

Official .NET SDK APIs are preferred. Where stable .NET APIs lack a required facility, a narrowly scoped terminal/control adapter may invoke an unchanged, officially shipped MXC executor through its documented stable contract. This is not a private MXC fork, copied engine code, a Node.js product runtime, or an alternate isolation engine. Its terminal/resource/network composition must pass the experiments before admission. Unsupported combinations fail with a concrete capability error.

## Supersession

All earlier product/architecture/contract/state/experience requirements conflicting with this decision are superseded. AD-0001–AD-0013, AD-0015, AD-0017 and AD-0021 are historical product decisions. In particular, AD-0021's requirement that all user execution go through Center no longer applies. Its Go Center investment, identity and outbound node channel are reused under the V2 trust model.

AD-0014, AD-0016, AD-0018, AD-0019 and AD-0020 retain serial implementation, native-only platforms, independent review, and exact pushed-head verification requirements. Their old product-task references are historical; current procedures and explicit task ranges live in Plan V2. No rule, status, host, hook or branch protection is relaxed by the pivot.

The previous Design snapshot is [frozen](../../history/v1-20261114-notice.md). The previous Plan's 63 tasks are frozen separately at its exact main SHA. All leave the current execution graph, including historical completed tasks. New tasks all begin planned and use AFV2 identifiers. No task after the old completed Center file work resumes automatically.

## Alternatives and consequences

Keeping the old Task runtime as the permanent implementation would preserve unnecessary queues, sessions, contracts and data structures, so it is rejected. Replacing all code with a new resource manager would discard validated budgeting/pressure work, so algorithms are extracted and re-tested instead. Treating MXC as a universal transparent filesystem redirector or resource governor is unsupported; access rules and resource ownership are explicit.

Two independent repositories require one comprehensive PR each, with Design merged before final Plan validation against Design main. Verification on unavailable native hosts is reported missing; author diagnostics cannot be relabelled as host statuses. This document authorizes planning and research only. Future product implementation starts under a separate user-authorized V2 range.

## Acceptance of the design migration

One active authority; complete requirements→Design→tasks mapping; source-pinned asset and MXC matrices; explicit experiment owners; executable APIs/state/storage contracts; frozen historical evidence; detailed removal/compatibility/DB migration tasks; complete Plan validator/tests; independent review and unresolved-gate disclosure. See [acceptance](../verification/acceptance.md).
