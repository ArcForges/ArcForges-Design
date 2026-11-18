# AD-0022 — ArcForges CLI Sandbox Platform Pivot

- Status: Accepted product and architecture direction; runtime combinations remain subject to named verification gates.
- Date: 2026-11-14
- Amendment: 2026-11-17; owner-approved local process visibility boundary below supersedes the Linux request-environment argv-only admission blocker.
- Amendment: 2026-11-18. The official MXC wrapper boundary below scopes Windows MVP acceptance to local native behavior.
- Decision owner: product owner, through the supplied ArcForges V2 migration instruction.
- Scope: current Design and Plan; this decision does not claim product code delivery.

## Decision

ArcForges becomes the open-source general CLI sandbox and intelligent resource-management platform specified in [product definition](../product/product-definition.md). Microsoft MXC official stable SDK/API and shipped official executable contracts provide isolation and payload creation. The platform preserves proven resource-observation and budgeting algorithms, reworks their coupling to the old scheduler, and deletes redundant/retired product implementations after their replacements are verified.

The primary model is persistent Sandbox plus one-execution Run. Local CLI is a full offline-capable path. The optional Go Center and Blazor Web management product use the same constrained Sandbox Core. Local and self-hosted use is free; only official-hosted service access is subscription-gated. The official service can manage devices owned by the user; it is not a cloud compute service and cannot bypass local host grants.

Official .NET SDK APIs are preferred. Where stable .NET APIs lack a required facility, a narrowly scoped terminal/control adapter may invoke an unchanged, officially shipped MXC executor through its documented stable contract. The adapter uses documented official policy and reports MXC's real result. The required native composition is defined by the [experiment protocol](../verification/mxc-experiments.md). Unsupported combinations fail with a concrete capability error.

### Official MXC wrapper boundary — 2026-11-18 amendment

Official stable MXC owns the isolation engine and native policy enforcement. ArcForges translates the requested policy into the documented official contract, invokes the intended official backend, and reports support, refusal and errors at the boundary it can observe. ArcForges owns its local filesystem/control boundaries, terminal, outer resource scope, process lifetime and recovery. Those integrations retain real native acceptance, including their safety checks together in the same Run.

Record official source support, local native observations and unverified behavior separately. Windows external selected TCP/UDP egress, and the composition cases that need a reachable external peer, remain unverified on the designated host. Preserve the original attempted and unrun cases with their outcomes. Those cases are outside the required Windows MVP matrix and do not gate Core, other work or acceptance within the declared release matrix. Windows validation still covers the local cases in the [revised experiment protocol](../verification/mxc-experiments.md#3-windows-experiments). Linux retains its scoped native evidence and requirements.

The Windows MVP uses local fixtures and existing host settings. An explicitly requested policy that the official contract supports and ArcForges can safely translate is submitted without semantic changes. An unverified mode cannot satisfy a requirement for locally demonstrated behavior. Actual unsupported policies and requests whose required safety constraints cannot be applied return their existing typed errors. A native refusal or uncertain outcome is reported for that request. ArcForges leaves underlying enforcement to MXC and preserves the requested policy across any failure.

### Local process visibility — 2026-11-17 amendment

The owner permits user-requested environment values to be visible in official MXC/helper process arguments to the owning host user, local administrators and their trusted host inspection tools. This visibility alone is not a sandbox boundary violation and must not block MXC admission or dependent delivery. The product does not promise to hide a Run's intentionally supplied inputs from these trusted host principals. An untrusted Sandbox payload remains outside that trust boundary, including when its OS UID is shared with the owner.

Continue to reject implicit inheritance of host credentials, SSH agents, credential sockets and Node signing material, and unauthorized access by a payload or another principal across Sandbox/control boundaries. Raw secrets, request environments and secret-bearing argv must not enter public Plan/GitHub records, exported evidence or ordinary logs. Native inspection uses synthetic fixtures and records only redacted observations and observer authority; it must not suppress an observed value or relabel a protected host observation as an unauthorized payload read.

The 2026-11-16 Linux observation `argv_sentinel_observed=true` and its original FAILED report remain historical facts under the criterion then applied. This amendment supersedes that argv-only rejection criterion, not the evidence. F-AOT-01 becomes pending revalidation; no old run is rewritten as a pass or a complete profile admission. Resume the authorized MXC work with the existing official pin and remaining native/artifact requirements. See [trust boundaries](../architecture/08-security-trust.md), [current experiment interpretation](../verification/mxc-experiments.md#owner-decision-and-resumption--2026-11-17-utc) and [acceptance](../verification/acceptance.md#local-process-visibility).

## Supersession

All earlier product/architecture/contract/state/experience requirements conflicting with this decision are superseded. AD-0001–AD-0013, AD-0015, AD-0017 and AD-0021 are historical product decisions. In particular, AD-0021's requirement that all user execution go through Center no longer applies. Its Go Center investment, identity and outbound node channel are reused under the V2 trust model.

AD-0014, AD-0016, AD-0018, AD-0019 and AD-0020 retain serial implementation, native-only platforms, independent review, and exact pushed-head verification requirements. Their old product-task references are historical; current procedures and explicit task ranges live in Plan V2. No rule, status, host, hook or branch protection is relaxed by the pivot.

The previous Design snapshot is [frozen](../../history/v1-20261114-notice.md). The previous Plan's 63 tasks are frozen separately at its exact main SHA. All leave the current execution graph, including historical completed tasks. New tasks all begin planned and use AFV2 identifiers. No task after the old completed Center file work resumes automatically.

## Alternatives and consequences

Keeping the old Task runtime as the permanent implementation would preserve unnecessary queues, sessions, contracts and data structures, so it is rejected. Replacing all code with a new resource manager would discard validated budgeting/pressure work, so algorithms are extracted and re-tested instead. Treating MXC as a universal transparent filesystem redirector or resource governor is unsupported; access rules and resource ownership are explicit.

Two independent repositories require one comprehensive PR each, with Design merged before final Plan validation against Design main. Verification on unavailable native hosts is reported missing; author diagnostics cannot be relabelled as host statuses. This document authorizes planning and research only. Future product implementation starts under a separate user-authorized V2 range.

## Acceptance of the design migration

One active authority; complete requirements→Design→tasks mapping; source-pinned asset and MXC matrices; explicit experiment owners; executable APIs/state/storage contracts; frozen historical evidence; detailed removal/compatibility/DB migration tasks; complete Plan validator/tests; independent review and unresolved-gate disclosure. See [acceptance](../verification/acceptance.md).
