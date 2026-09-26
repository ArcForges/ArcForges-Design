# Application composition — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Independent application composition, typed host ports and the minimal ArcNotes services that prove them.

Tasks: 8 · Owning repositories: ArcNotes, DesktopPlatform · Integration owner(s): ArcNotes integration owner, DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [APP.01](#task-app-01) | Assistant.Abstractions host ports and application identity | producer | M | [CON.02](contracts.md#task-con-02) (contract), [PLT.17](platform.md#task-plt-17) (artifact), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [APP.02](#task-app-02) | Minimal ArcNotes application services (read/create/append) | producer | M | [APP.01](#task-app-01) (artifact), [PLT.24](platform.md#task-plt-24) (artifact), [PLT.38](platform.md#task-plt-38) (artifact) | not-started |
| [APP.03](#task-app-03) | Clean Native AOT package-consumer composition for ArcNotes | producer | S | [APP.01](#task-app-01) (artifact), [APP.02](#task-app-02) (artifact), [PRF.04](runtime-proofs.md#task-prf-04) (artifact), [NAT.01](native.md#task-nat-01) (artifact) | not-started |
| [APP.04](#task-app-04) | Idempotency and revision against the real store | producer | S | [APP.02](#task-app-02) (artifact), [FND.02](foundation.md#task-fnd-02) (artifact), [FND.03](foundation.md#task-fnd-03) (artifact) | not-started |
| [APP.05](#task-app-05) | Approval at the owner | producer | M | [APP.01](#task-app-01) (artifact), [PLT.39](platform.md#task-plt-39) (artifact) | not-started |
| [APP.06](#task-app-06) | Context and artifact integration | producer | M | [APP.01](#task-app-01) (artifact), [PLT.21](platform.md#task-plt-21) (artifact), [PLT.22](platform.md#task-plt-22) (artifact), [PLT.41](platform.md#task-plt-41) (artifact) | not-started |
| [APP.07](#task-app-07) | Independent lifecycle | producer | S | [APP.01](#task-app-01) (artifact), [PLT.32](platform.md#task-plt-32) (artifact) | not-started |
| [APP.08](#task-app-08) | Owned-artifact receipt and UX acceptance | acceptance | M | [APP.01](#task-app-01) (artifact), [APP.02](#task-app-02) (artifact), [APP.03](#task-app-03) (artifact), [APP.04](#task-app-04) (artifact), [APP.05](#task-app-05) (artifact), [APP.06](#task-app-06) (artifact), [APP.07](#task-app-07) (artifact) | not-started |

## Tasks

<a id="task-app-01"></a>

### APP.01 — Assistant.Abstractions host ports and application identity

**Outcome.** Assistant.Abstractions published with IHostContext/IHostActions/IHostResources/IHostNavigation/IHostLifecycle/IHostPlatformServices, product/profile identity and lifetime; two independent application identities cannot share stores/registration.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-01` and ledger record `ledger/tasks/app-01.md` in the Plan repository; task branch `task/app-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) — full |
| Provides | assistant-abstractions-pkg; host-ports-v1; application-scope-identity |
| Start prerequisites | **contract** [CON.02](contracts.md#task-con-02) — published capability/resource contract records (descriptor/risk/context shapes). *Why:* host port signatures (IHostResources/IHostActions) are typed against these Contracts records<br>**artifact** [PLT.17](platform.md#task-plt-17) — real ArcForges.Application.Abstractions (application identity and in-process composition), not the current placeholder assembly. *Why:* Assistant.Abstractions composes on top of Application.Abstractions per architecture 27; DesktopPlatform repo currently has only AssemblyPlaceholder.cs for that project<br>**artifact** [FND.01](foundation.md#task-fnd-01) — real ArcForges.Foundation identity/error/version primitives, not the current placeholder assembly. *Why:* host port identity/lifetime types build on Foundation primitives; currently only a placeholder assembly exists |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.02](#task-app-02), [APP.03](#task-app-03), [APP.05](#task-app-05), [APP.06](#task-app-06), [APP.07](#task-app-07), [APP.08](#task-app-08), [AST.01](assistant.md#task-ast-01), [EXE.01](execution.md#task-exe-01), [NOTES.03](arcnotes.md#task-notes-03), [PLT.57](platform.md#task-plt-57) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Abstractions/**`<br>`DesktopPlatform:tests/AssistantAbstractionsTests/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit tests only (two identities/no shared store); Native AOT compile check; no live Cloud/device in CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Source commit, Assistant.Abstractions package version/hash, two-identity isolation test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: git ls-files DesktopPlatform src/ has no Assistant/ or Communication/ tree at all (HEAD fe8476d); only generic BuildingBlocks placeholders (AssemblyPlaceholder.cs) and Native/DesktopHelpers trees exist. |
| Notes | Root of the whole area's dependency graph; every other WP14 to WP17/26 desktop task starts from this package. |

<a id="task-app-02"></a>

### APP.02 — Minimal ArcNotes application services (read/create/append)

**Outcome.** Real read/create/append document commands through typed application handlers and local persistence, with descriptor/risk/context validation and one write path shared by UI and own-app capability invocation. Professional document completion remains WP18.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/app-02` and ledger record `ledger/tasks/app-02.md` in the Plan repository; task branch `task/app-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-14.01](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.01) — full |
| Provides | arcnotes-minimal-services; arcnotes-write-path |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published Assistant.Abstractions host ports and product identity. *Why:* ArcNotes application handlers register through the real host ports, not a private stand-in<br>**artifact** [PLT.24](platform.md#task-plt-24) — real ICapabilityProvider.InvokeAsync invocation pipeline (owner-side decode/validate). *Why:* the one write path for UI and own-app capability must go through the real pipeline; WP14.01 testing explicitly requires descriptor/risk/context validation on a real path<br>**artifact** [PLT.38](platform.md#task-plt-38) — published security decision pipeline enforcement point. *Why:* the write path must enforce real risk/permission decisions, not a bypass |
| Entry condition | [ADOPT.04.app-composition](adoption.md#task-adopt-04-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.03](#task-app-03), [APP.04](#task-app-04), [APP.08](#task-app-08) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Application/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Infrastructure/**`<br>`ArcNotes:tests/**` |
| Validation | Offline unit tests (descriptor/risk/context validation, one write path); no live Cloud in CI. |
| Completion evidence | Source commit, command receipt samples, validation-failure cases. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcNotes HEAD 268c3290 has only src/ArcForges.ArcNotes(.Core) hello-world bootstrap (BuildIdentity, CloudHelloClient, HelloViewModel, MainWindow, Program); no Domain/Application/Infrastructure/AssistantIntegration trees exist. |
| Notes | This is the ONLY product-repo work in WP14 to WP17/26; full ArcNotes document model is WP18, not here. |

<a id="task-app-03"></a>

### APP.03 — Clean Native AOT package-consumer composition for ArcNotes

**Outcome.** A clean Native AOT ArcNotes consumer built purely from published Platform/Contracts packages and in-process typed host ports; no source reference or local-RPC product loop. Package-only restore, publish/run, command/cancel/result and owner refusal proven.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/app-03` and ledger record `ledger/tasks/app-03.md` in the Plan repository; task branch `task/app-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S · early risk proof |
| Obligations | [WP-14.02](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.02) — full |
| Provides | arcnotes-aot-consumer-proof |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published Assistant.Abstractions package (not project reference). *Why:* the consumer must restore this as a package, not a source/project reference, per the substep's own rule<br>**artifact** [APP.02](#task-app-02) — published ArcNotes application-services package surface. *Why:* same package-only consumption rule applies to the product's own services<br>**artifact** [PRF.04](runtime-proofs.md#task-prf-04) — proven Local RPC under Native AOT pattern. *Why:* reuse the already-proven AOT-safe local RPC approach rather than re-deriving one<br>**artifact** [NAT.01](native.md#task-nat-01) — confirmed Native AOT device-tool/capability-invocation feasibility from the high-risk probe. *Why:* this task is the first real product proof built on that probe; it should not re-litigate AOT feasibility |
| Entry condition | [ADOPT.04.app-composition](adoption.md#task-adopt-04-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.08](#task-app-08), [HAR.05](harness.md#task-har-05) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes/**`<br>`ArcNotes:packaging/**` |
| Validation | Native AOT publish/run in CI (package-only restore), offline command/cancel/result tests; no installed-package or public-release install/upgrade CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | AOT publish log, package hash manifest, command/cancel/result and owner-refusal test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcNotes host project (ArcForges.ArcNotes) exists only as a hello-world Avalonia-style bootstrap; no host-port composition yet. |
| Notes | Narrow early-risk proof: first real evidence that the whole Assistant.Abstractions/host-port composition model survives Native AOT package-only consumption for an actual product. Failure here invalidates the composition model assumed by WP15 to WP17. |

<a id="task-app-04"></a>

### APP.04 — Idempotency and revision against the real store

**Outcome.** Command receipt and expected local revision exercised against the real store; draft/conflict behavior and unknown-outcome classification preserved under duplicate command, stale revision and process-kill-around-commit.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-04` and ledger record `ledger/tasks/app-04.md` in the Plan repository; task branch `task/app-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-14.03](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03) — full |
| Provides | host-idempotency-proof |
| Start prerequisites | **artifact** [APP.02](#task-app-02) — real local persistence write path to kill/duplicate against. *Why:* a fixture store would hide the recovery defects this substep tests<br>**artifact** [FND.02](foundation.md#task-fnd-02) — published execution identity and idempotency records (command identity). *Why:* duplicate-command detection needs the real command-identity shape<br>**artifact** [FND.03](foundation.md#task-fnd-03) — published revision and sequence records. *Why:* stale-revision detection needs the real revision/sequence contract |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.08](#task-app-08) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Abstractions/**`<br>`DesktopPlatform:tests/AssistantAbstractionsTests/**` |
| Validation | Offline unit/process-kill tests (duplicate command, stale revision, kill-around-commit); no live environment. |
| Completion evidence | Kill-around-commit recovery log, duplicate/stale-revision test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No idempotency/revision handling exists yet; depends on APP.01/APP.02 projects which do not exist. |
| Notes | Shares vocabulary (command identity, revision) with WP16 execution engine (EXE.01) but is the host-port-level idempotency check, not the ProductJob engine itself. |

<a id="task-app-05"></a>

### APP.05 — Approval at the owner

**Outcome.** Expiry/modified-input/revocation cannot bypass owner checks.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-05` and ledger record `ledger/tasks/app-05.md` in the Plan repository; task branch `task/app-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) — full |
| Provides | owner-approval-enforcement |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published host ports to render the approval surface through. *Why:* approval UI composes into the same host-port model as the rest of the app<br>**artifact** [PLT.39](platform.md#task-plt-39) — published approval/steering/step-up mechanism. *Why:* owner enforcement re-checks using the real security pipeline's approval primitive, not a private one |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.08](#task-app-08), [AST.12](assistant.md#task-ast-12), [DEV.03](device-bridge.md#task-dev-03) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Abstractions/**`<br>`DesktopPlatform:tests/AssistantAbstractionsTests/**` |
| Validation | Offline unit tests: expiry, modified-input, revocation cannot bypass owner checks. |
| Completion evidence | Expiry/modified-input/revocation test results tied to a real approval record. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No approval surface exists yet. |
| Notes | contracts/02-local-rpc-operations.md confirms InvokeAsync performs owner-side final validation under [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) AND [WP-26.02](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02) -- this is the SAME enforcement mechanism DEV.03 (26.02) re-invokes at the device-bridge call site, not a duplicate. |

<a id="task-app-06"></a>

### APP.06 — Context and artifact integration

**Outcome.** Own-app resource references frozen at selection time, preview opened through the product port, egress enforced separately, provenance preserved. Selection changes after freeze, missing resource, denied export and bounded artifact all handled.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-06` and ledger record `ledger/tasks/app-06.md` in the Plan repository; task branch `task/app-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-14.05](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05) — full |
| Provides | host-context-freeze; host-artifact-preview-port |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published IContextProvider/IArtifactHandler/IResourceAccess host port shapes. *Why:* context/artifact integration implements these exact [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) port interfaces<br>**artifact** [PLT.21](platform.md#task-plt-21) — real context providers and freezing implementation. *Why:* own-app resource freezing must use the real context-provider freeze mechanism<br>**artifact** [PLT.22](platform.md#task-plt-22) — real resources-and-artifacts implementation. *Why:* artifact preview/bounding builds on the real resource/artifact primitives<br>**artifact** [PLT.41](platform.md#task-plt-41) — published egress control mechanism. *Why:* denied export must be enforced by the real egress control, separate from context freezing itself |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.08](#task-app-08), [AST.03](assistant.md#task-ast-03), [AST.16](assistant.md#task-ast-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Abstractions/**`<br>`DesktopPlatform:tests/AssistantAbstractionsTests/**` |
| Validation | Offline unit tests: selection-after-freeze, missing resource, denied export, bounded artifact size. |
| Completion evidence | Freeze/preview/egress test results with provenance trace samples. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No context/artifact integration exists yet. |
| Notes | AST.03 (15.02 attachments) and AST.16 (17.06 preview/host context) both reuse this exact freeze+preview port rather than duplicating it. |

<a id="task-app-07"></a>

### APP.07 — Independent lifecycle

**Outcome.** Launch/save works with Cloud unavailable and the assistant view closed; views dispose independently from services; two windows with different drafts and independent app crash lose no canonical data.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-07` and ledger record `ledger/tasks/app-07.md` in the Plan repository; task branch `task/app-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-14.06](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.06) — full |
| Provides | host-independent-lifecycle |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published IHostLifecycle port. *Why:* independent lifecycle implements this exact [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) port<br>**artifact** [PLT.32](platform.md#task-plt-32) — published lifecycle/menus/shutdown shell pattern. *Why:* professional app shutdown handling reuses the platform shell's lifecycle pattern rather than inventing a second one |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.08](#task-app-08) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Abstractions/**`<br>`DesktopPlatform:tests/AssistantAbstractionsTests/**` |
| Validation | Offline unit/process tests: two windows/different drafts, independent crash, no data loss; no live-environment CI. |
| Completion evidence | Two-window and crash-recovery test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No lifecycle handling exists yet. |

<a id="task-app-08"></a>

### APP.08 — Owned-artifact receipt and UX acceptance

**Outcome.** WP14 built/packed once from a clean environment; all applicable UX acceptance groups recorded; package/contract/owner/version compatibility and failure/recovery evidence attached; no later-provider fixture used to close a real WP14 gate.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-08` and ledger record `ledger/tasks/app-08.md` in the Plan repository; task branch `task/app-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-14.90](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.90) — full |
| Provides | wp14-accepted-artifact |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — completed [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00). *Why:* aggregation requires every WP14 substep complete<br>**artifact** [APP.02](#task-app-02) — completed [WP-14.01](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.01). *Why:* aggregation<br>**artifact** [APP.03](#task-app-03) — completed [WP-14.02](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.02). *Why:* aggregation<br>**artifact** [APP.04](#task-app-04) — completed [WP-14.03](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03). *Why:* aggregation<br>**artifact** [APP.05](#task-app-05) — completed [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04). *Why:* aggregation<br>**artifact** [APP.06](#task-app-06) — completed [WP-14.05](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05). *Why:* aggregation<br>**artifact** [APP.07](#task-app-07) — completed [WP-14.06](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.06). *Why:* aggregation |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](assistant.md#task-ast-17) |
| Write scope | `DesktopPlatform:artifacts/evidence/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Build/pack once in CI producing the immutable candidate; UX-A/B ledger rows recorded per experience/03; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope only (no macOS/E2E/live-service CI). |
| Completion evidence | Source commit, package/artifact versions and hashes, environment, UX-A/B acceptance rows, named later-fixture list (none expected for WP14 itself). |
| Baseline (unreviewed unless accepted) | not-started |
