<a id="rule-wp-31"></a>
# WP-31 — Complete ArcChat Android Companion

> Status: Authoritative implementation plan under P2-010
> Phase: J — Platform and client integration
> Upstream: `26` · `30` · `45` · `52` · Downstream: `32`

## 1. Scope and purpose

Implement this stage of the complete Android ArcChat companion. [Mobile architecture](../../architecture/11-mobile-architecture.md), [client journeys](../../architecture/contracts/07-client-journeys-and-ports.md), [companion requirements](../../requirements/products/arcchat-mobile-and-web.md) and [producer stages](../producer-artifacts-and-integration.md) fix scope, behavior and evidence. Source repositories are implementation/reference evidence only; their hello scaffolds do not define completion.

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


Use the exact released Contracts Maven package/descriptor/fixture set, compatible Cloud/AI manifest and completed upstream owner outputs. Android toolchain and OS decisions come from Mobile architecture and WP06 proof; a blocking local toolchain/Android environment problem is reported before dependent execution. No producer source checkout or browser TS runtime is an input.

## 3. Binding rules and decisions

Android only, Kotlin/JVM/Jetpack Compose, Apache-2.0; no GPL-family implementation in the app. Command/owner/recovery identity, explicit permissions/consent, exact values, immutable producer artifacts, full accepted companion scope and consumption-only commercial restrictions are mandatory. [Wire registry](../../architecture/contracts/04-protobuf-wire-registry.md) owns the complete field and operation inventory. Equivalent internal classes/layout choices may vary only when observable behavior and acceptance remain identical.

## 4. Projects, directories, files and major types affected

Mobile owns app/, core/domain, core/data, core/network, core/security, core/designsystem, feature/home, feature/chat, feature/tasks, feature/library and feature/settings, tests and Android build/release governance. An equivalent module partition may preserve the same boundaries. No edits in other implementation repositories are required to bypass their published artifact boundary.

## 5. Required implementation work

<a id="rule-wp-31.00"></a>
### WP-31.00 — Identity, Home and workspace

**What must be fully done.** Implement full identity/enrollment/recovery/profile/sign-out and workspace/device binding plus Home attention/inbox from Mobile architecture. Navigation Home/Conversations/Tasks/Library/Settings preserves unread/approval/blocked/error states and access explanations.

**Testing requirements.** Actual official and supported self-host flows; no-workspace first run, restricted account, expired/revoked sessions, duplicate attention hints.

**Completion gate.** All accepted account/attention paths complete and accessible; no hello-world scope substitution.

<a id="rule-wp-31.01"></a>
### WP-31.01 — Conversations, projects and retrieval

**What must be fully done.** Implement ordinary/agent/temporary turns, history/branch/search/filter/pin/archive, drafts/attachments, projects/memory controls, selected-source consent, citations and explicit Web search. Fetch real Contracts/CF owner states and preserve modes/temporary expiry.

**Testing requirements.** Actual selected Workers AI, paid admission and protected-context overflow; save/close temporary, offline drafts, no accidental Task, query egress rejection.

**Completion gate.** Every conversation/project/retrieval row in Mobile architecture works with actual52 owner outputs.

<a id="rule-wp-31.02"></a>
### WP-31.02 — Tasks, tools, approvals and automation

**What must be fully done.** Implement task list/details/paged steps/logs/artifacts, steering/cancel/pause/resume, explicit promotion from ordinary turn, approvals with proposal revision/expiry/target, eligible-device/capability choices and narrow remote grants. Implement simple automation list/create/edit/enable/run/history within accepted companion scope.

**Testing requirements.** Real desktop bridge and owner tools; offline/stale device, refused permission, expiry, timeout after external effect, duplicate delivery and ambiguous status.

**Completion gate.** One actual owner outcome/settlement per command, no broad implicit grant or hidden background write.

<a id="rule-wp-31.03"></a>
### WP-31.03 — Library, resources and portability

**What must be fully done.** Implement approved Notes/cloud resource preview/search/citation/deep-link/handoff, upload/download/sharing, export/import status and fidelity, data health and irrecoverable guidance. No full Notes/Scope/Slate editor is introduced on Mobile.

**Testing requirements.** Real R2 range/part/hash/expiry, absent owning desktop, denied preview, missing blob, cancellation and resumable transfer.

**Completion gate.** All resource/Library journeys complete; no unavailable bytes represented as empty success.

<a id="rule-wp-31.04"></a>
### WP-31.04 — Presence, push, deep links and settings

**What must be fully done.** Implement visible device readiness, installation and capability availability, push token registration/rotation/revocation, notification channel controls, settings/accessibility/localization/account-data actions and consumption-only capacity/credit consent. Push contains identifiers only and always re-fetches authorized state.

**Testing requirements.** Physical foreground/background/non-GMS tests, doze/process kill, stale push, account change, screen reader/font scaling and expired approval link.

**Completion gate.** Companion stays usable through declared polling/notification fallback; purchase/store billing remains absent.

<a id="rule-wp-31.05"></a>
### WP-31.05 — Offline and recovery integration

**What must be fully done.** Exercise the complete Mobile storage/outbox/network rules against real Cloud/CF and desktop, including restore generation, unknown external result, transient input TTL, partially completed export and client update.

**Testing requirements.** Independent journey matrix at least login→ordinary→Task promotion→approval→artifact; search→citation; automation→attention; logout/revoke→quarantine recovery.

**Completion gate.** Real52/26/25 evidence passes on release APK; mocks do not close any required journey.

<a id="rule-wp-31.06"></a>
### WP-31.06 — Scope and licence enforcement

**What must be fully done.** Check all companion requirements, consumption-only restrictions, public Maven-only imports and absence of desktop secrets, device-local paths or excluded professional editing surfaces. Validate all third-party code provenance.

**Testing requirements.** Package content/dependency/privacy checks and complete surface action inventory cross-check.

**Completion gate.** Required scope is complete; Android licence and commerce boundary hold without removing accepted behavior.

<a id="rule-wp-31.90"></a>
### WP-31.90 — Complete companion acceptance

**What must be fully done.** Join actual31 evidence with producer manifests, signed candidate and full52/26/25/42/45 compatible integration manifest.

**Testing requirements.** Run full physical-device release scenarios and injected failure matrix; record exact device/OS/server/worker/package identities.

**Completion gate.** Companion behavior passes; distribution/store activation remains32.

## 6. Impacts

Contracts delivers the complete public Kotlin package; Cloud/AI deliver the same owner behavior as desktop/Web. Mobile maintains its own lifecycle/storage/UI. Changes in package/signing/schema versions require an explicit compatible manifest and tested migration.

## 7. Tests and verification evidence

Separate unit/schema/fixture tests, clean packaged consumers, actual Cloud/CF/desktop interactions, physical-device release evidence and distribution/store evidence. Record exact hashes/versions/device identity and limitations. A green build cannot substitute for a missing stage.


| Evidence | Produced by |
|---|---|
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-31.90](#rule-wp-31.90) |

## 8. Completion gate

[PG-24](../../assurance/open-gates-register.md#rule-pg-24): exercise the actual WP45.09 sender and push.v1 on a physical arm64 Android device, including Doze/background generic attention, authoritative detail/approval, duplicate suppression, rotation/revocation, no-GMS and denied-permission foreground recovery. Provider acceptance alone is insufficient.

Every numbered substep and applicable inherited requirement passes; the complete surface/action/state matrix is exercised. Unfinished required behavior blocks completion. Candidate and producer identities are immutable and all temporary fixtures have the named replacement stage. No scope reduction or design decision is deferred to consumer coding.

## 9. Dependencies

**Upstream:** `26` · `30` · `45` · `52`. Consume completed stage outputs.

**Downstream:** `32`. Consumers use exact released artifacts.
