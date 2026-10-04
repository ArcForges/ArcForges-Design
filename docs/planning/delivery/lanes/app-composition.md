# Application composition — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Independent application composition, typed host ports and the minimal ArcScope services that prove them.

Tasks: 8 · Owning repositories: ArcScope, DesktopPlatform · Integration owner(s): ArcScope integration owner, DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [APP.01](#task-app-01) | Assistant.Abstractions host ports and application identity | producer | M | [CON.02](contracts.md#task-con-02) (contract), [PLT.17](platform.md#task-plt-17) (artifact), [FND.02](foundation.md#task-fnd-02) (artifact), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [APP.02](#task-app-02) | Minimal ArcScope application services (read/create/append annotations) | producer | M | [APP.01](#task-app-01) (artifact), [PLT.24](platform.md#task-plt-24) (artifact), [PLT.38](platform.md#task-plt-38) (artifact) | not-started |
| [APP.03](#task-app-03) | Clean Native AOT package-consumer composition for ArcScope | producer | S | [APP.01](#task-app-01) (artifact), [APP.02](#task-app-02) (artifact), [PRF.04](runtime-proofs.md#task-prf-04) (artifact), [NAT.01](native.md#task-nat-01) (artifact) | not-started |
| [APP.04](#task-app-04) | Idempotency and revision against the real store | producer | S | [APP.02](#task-app-02) (artifact), [FND.02](foundation.md#task-fnd-02) (artifact), [FND.03](foundation.md#task-fnd-03) (artifact) | not-started |
| [APP.05](#task-app-05) | Approval at the owner | producer | M | [APP.01](#task-app-01) (artifact), [PLT.39](platform.md#task-plt-39) (artifact) | not-started |
| [APP.06](#task-app-06) | Context and artifact integration | producer | M | [APP.01](#task-app-01) (artifact), [PLT.21](platform.md#task-plt-21) (artifact), [PLT.22](platform.md#task-plt-22) (artifact), [PLT.41](platform.md#task-plt-41) (artifact) | not-started |
| [APP.07](#task-app-07) | Independent lifecycle | producer | S | [APP.01](#task-app-01) (artifact), [PLT.32](platform.md#task-plt-32) (artifact) | not-started |
| [APP.08](#task-app-08) | Owned-artifact receipt and UX acceptance | acceptance | M | [APP.01](#task-app-01) (artifact), [APP.02](#task-app-02) (artifact), [APP.03](#task-app-03) (artifact), [APP.04](#task-app-04) (artifact), [APP.05](#task-app-05) (artifact), [APP.06](#task-app-06) (artifact), [APP.07](#task-app-07) (artifact), [PLT.17](platform.md#task-plt-17) (artifact), [PLT.27](platform.md#task-plt-27) (artifact), [PLT.01](platform.md#task-plt-01) (artifact) | not-started |

## Tasks

<a id="task-app-01"></a>

### APP.01 — Assistant.Abstractions host ports and application identity

**Outcome.** Assistant.Abstractions published with IHostContext/IHostActions/IHostResources/IHostNavigation/IHostLifecycle/IHostPlatformServices, product/profile identity and lifetime; two independent application identities cannot share stores/registration.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-01` and ledger record `ledger/tasks/app-01.md` in the Plan repository; task branch `task/app-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) — Host-port signatures, product/profile identity and lifetime, and two-identity unit isolation only; APP.08 owns the [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) minimal real-integration sample. |
| Provides | assistant-abstractions-pkg; host-ports-v1; application-scope-identity |
| Start prerequisites | **contract** [CON.02](contracts.md#task-con-02) — published capability/resource contract records (descriptor/risk/context shapes). *Why:* host port signatures (IHostResources/IHostActions) are typed against these Contracts records<br>**artifact** [PLT.17](platform.md#task-plt-17) — delivered ArcForges.Capabilities application identity and explicit in-process composition pattern. *Why:* PLT.17 publishes ArcForges.Capabilities, not Application.Abstractions; use it as identity/composition precedent only. Architecture 27 permits Assistant.Abstractions direct dependencies only on Foundation and Application.Abstractions, so do not add a direct Capabilities dependency<br>**artifact** [FND.02](foundation.md#task-fnd-02) — published ArcForges.Application.Abstractions cancellation and lifecycle ports. *Why:* FND.02 is the producer of the real ArcForges.Application.Abstractions package consumed by Assistant.Abstractions<br>**artifact** [FND.01](foundation.md#task-fnd-01) — published ArcForges.Foundation identity/error/version primitives. *Why:* host port identity/lifetime types build on the real Foundation primitives delivered by FND.01 |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.02](#task-app-02), [APP.03](#task-app-03), [APP.05](#task-app-05), [APP.06](#task-app-06), [APP.07](#task-app-07), [APP.08](#task-app-08), [AST.01](assistant.md#task-ast-01), [EXE.01](execution.md#task-exe-01), [PLT.57](platform.md#task-plt-57), [PRF.02](runtime-proofs.md#task-prf-02) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Abstractions/**`<br>`DesktopPlatform:tests/AssistantAbstractionsTests/**`<br>`DesktopPlatform:DesktopPlatform.slnx (register APP.01 producer and its test project only)`<br>`DesktopPlatform:.github/workflows/package-validation.yml (run the APP.01 test project only)`<br>`DesktopPlatform:eng/packaging/packages.json (APP.01 package entry and Architecture 27 owned-package edges only)`<br>`DesktopPlatform:eng/version-sources.json (APP.01 package source declaration only)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (APP.01 production/test project registrations for the exact Architecture 27 dependency edges only)`<br>`DesktopPlatform:eng/policy/dependency-reviews/app-01-*.json (new immutable APP.01 successor only for already-admitted dependency identities, if required; no new dependency or version)`<br>`DesktopPlatform:eng/policy/licence-boundary.json (APP.01 production/test project registrations only)`<br>`DesktopPlatform:eng/policy/reconciliation/project-updates.json (APP.01 project registrations only)`<br>`DesktopPlatform:eng/policy/reconciliation/source.json (APP.01 source inventory only)`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json (APP.01 active project registrations only; preserve frozen inventories)`<br>`DesktopPlatform:eng/policy/runtime-ownership.json (APP.01 project classifications only)`<br>`DesktopPlatform:eng/policy/architecture-projects.json (append exactly the APP.01 producer as role=Abstractions with production=true and aot=true, and its test project as role=Test with production=false and aot=false; preserve every other row and field)`<br>`DesktopPlatform:eng/provenance/files.json (APP.01 owned-source inventory rows only)`<br>`DesktopPlatform:eng/provenance/records/assistant-abstractions-*.json (new immutable APP.01 source/package receipts only; preserve all prior records)`<br>`DesktopPlatform:eng/packaging/packages.py (exact existing external dependency pins in the APP.01 package closure only; add no package ID or version)`<br>`DesktopPlatform:eng/packaging/test_packages.py (APP.01-owned positive/negative checks for those exact existing pins only)`<br>`DesktopPlatform:README.md (current APP.01 package production claim only)`<br>`DesktopPlatform:docs/compliance/third-party-license-register.md (APP.01 package binding to already-admitted external dependencies only)`<br>`DesktopPlatform:Directory.Packages.props (append only ArcForges.Assistant.Abstractions and AssistantAbstractionsTests to the existing ArcForges.Contracts.Foundation 1.0.0-ci.216.1 MSBuildProjectName selector; preserve the 1.0.0-ci.113.1 default)`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only exact APP.01 public API-to-focused-test bindings in the AssistantAbstractionsTests project)` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline unit tests only (two identities/no shared store); Native AOT compile check; no live Cloud/device in CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Source commit, Assistant.Abstractions package version/hash, two-identity isolation test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: git ls-files DesktopPlatform src/ has no Assistant/ or Communication/ tree at all (HEAD fe8476d); only generic BuildingBlocks placeholders (AssemblyPlaceholder.cs) and Native/DesktopHelpers trees exist. |
| Notes | Root of the whole area's dependency graph; every other WP14 to WP17/26 desktop task starts from this package. FND.02 is the real ArcForges.Application.Abstractions producer; PLT.17 provides only the ArcForges.Capabilities application-identity/composition pattern. Keep Architecture 27's Assistant.Abstractions direct dependency table exactly Foundation plus Application.Abstractions; do not add a direct ArcForges.Capabilities dependency. CON.02 remains a host-port shape prerequisite and does not authorize another dependency edge. Register only APP.01's package, producer/test projects, and provenance/reconciliation rows, using already-admitted dependency identities and exact existing version pins; do not add package IDs, pins, versions, dependency owners, or expand the package closure. Append this producer's package entry and build-config project/CI rows; after rebase regenerate lock files and never hand-merge them. Write-scope repair 2026-10-04 (w-c20261004-app01): Directory.Packages.props and eng/policy/architecture-contract-tests.json are append-only supporting bindings for the APP.01 producer and test projects (central transitive pinning rejects restore of a project that reaches ArcForges.Foundation under the 1.0.0-ci.113.1 default; [RP-10](../../../architecture/01-solution-and-project-layout.md#rule-rp-10) requires a [Fact] binding for every public API method of the Abstractions project). They add no dependency, package ID, version or pin. |

<a id="task-app-02"></a>

### APP.02 — Minimal ArcScope application services (read/create/append annotations)

**Outcome.** Real read/create/append annotation commands through typed application handlers and local persistence, with descriptor/risk/context validation and one write path shared by UI and own-app capability invocation. Professional ArcScope completion remains WP33-WP35.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/app-02` and ledger record `ledger/tasks/app-02.md` in the Plan repository; task branch `task/app-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-14.01](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.01) — full |
| Provides | arcscope-minimal-services; arcscope-write-path |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published Assistant.Abstractions host ports and product identity. *Why:* ArcScope application handlers register through the real host ports, not a private stand-in<br>**artifact** [PLT.24](platform.md#task-plt-24) — real ICapabilityProvider.InvokeAsync invocation pipeline (owner-side decode/validate). *Why:* the one write path for UI and own-app capability must go through the real pipeline; WP14.01 testing explicitly requires descriptor/risk/context validation on a real path<br>**artifact** [PLT.38](platform.md#task-plt-38) — published security decision pipeline enforcement point. *Why:* the write path must enforce real risk/permission decisions, not a bypass |
| Entry condition | [ADOPT.05.app-composition](adoption.md#task-adopt-05-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.03](#task-app-03), [APP.04](#task-app-04), [APP.08](#task-app-08) |
| Write scope | `ArcScope:src/ArcForges.ArcScope.Application/**`<br>`ArcScope:src/ArcForges.ArcScope.Infrastructure/**`<br>`ArcScope:tests/**` |
| Validation | Offline unit tests (descriptor/risk/context validation, one write path); no live Cloud in CI. |
| Completion evidence | Source commit, command receipt samples, validation-failure cases. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcScope HEAD 31551f8 has only the src/ArcForges.ArcScope(.Core) bootstrap (ArcScopeApp, BuildIdentity, CloudHelloClient, HelloViewModel, LiveSmoke, MainWindow, Program); no Domain/Application/Infrastructure/AssistantIntegration trees exist. |
| Notes | This is the ONLY product-repo work in WP14 to WP17/26; professional ArcScope completion is WP33-WP35, not here. |

<a id="task-app-03"></a>

### APP.03 — Clean Native AOT package-consumer composition for ArcScope

**Outcome.** A clean Native AOT ArcScope consumer built purely from published Platform/Contracts packages and in-process typed host ports; no source reference or local-RPC product loop. Package-only restore, publish/run, command/cancel/result and owner refusal proven.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/app-03` and ledger record `ledger/tasks/app-03.md` in the Plan repository; task branch `task/app-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S · early risk proof |
| Obligations | [WP-14.02](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.02) — full |
| Provides | arcscope-aot-consumer-proof |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published Assistant.Abstractions package (not project reference). *Why:* the consumer must restore this as a package, not a source/project reference, per the substep's own rule<br>**artifact** [APP.02](#task-app-02) — published ArcScope application-services surface. *Why:* same package-only consumption rule applies to the product's own services<br>**artifact** [PRF.04](runtime-proofs.md#task-prf-04) — proven Local RPC under Native AOT pattern. *Why:* reuse the already-proven AOT-safe local RPC approach rather than re-deriving one<br>**artifact** [NAT.01](native.md#task-nat-01) — confirmed Native AOT device-tool/capability-invocation feasibility from the high-risk probe. *Why:* this task is the first real product proof built on that probe; it should not re-litigate AOT feasibility |
| Entry condition | [ADOPT.05.app-composition](adoption.md#task-adopt-05-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.08](#task-app-08), [HAR.05](harness.md#task-har-05) |
| Write scope | `ArcScope:src/ArcForges.ArcScope/**`<br>`ArcScope:packaging/**` |
| Validation | Native AOT publish/run in CI (package-only restore), offline command/cancel/result tests; no installed-package or public-release install/upgrade CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | AOT publish log, package hash manifest, command/cancel/result and owner-refusal test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: the ArcScope host project (ArcForges.ArcScope) exists only as a hello-world Avalonia bootstrap; no host-port composition yet. |
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

**Outcome.** A minimal, runnable WP14 integration sample composes the host ports with real ArcForges.Capabilities, ArcForges.Desktop.Shell and ArcForges.Persistence.Sqlite, and demonstrates product/profile identity, lifecycle and isolated local-store use; WP14 is built/packed once from a clean environment with all applicable UX acceptance groups and package/contract/owner/version compatibility and failure/recovery evidence recorded. No later-provider fixture closes a real WP14 gate.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/app-08` and ledger record `ledger/tasks/app-08.md` in the Plan repository; task branch `task/app-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) — Minimal real-integration sample only: compose the [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) host ports with real ArcForges.Capabilities, ArcForges.Desktop.Shell and ArcForges.Persistence.Sqlite; no fakes or stand-ins.<br>[WP-14.90](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.90) — full |
| Provides | wp14-accepted-artifact |
| Start prerequisites | **artifact** [APP.01](#task-app-01) — published [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) host-port signatures and product/profile identity/lifetime. *Why:* the APP.08 real-integration sample composes through APP.01's delivered host ports and identity; APP.08 owns the separate sample portion of [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00)<br>**artifact** [APP.02](#task-app-02) — completed [WP-14.01](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.01). *Why:* aggregation<br>**artifact** [APP.03](#task-app-03) — completed [WP-14.02](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.02). *Why:* aggregation<br>**artifact** [APP.04](#task-app-04) — completed [WP-14.03](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03). *Why:* aggregation<br>**artifact** [APP.05](#task-app-05) — completed [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04). *Why:* aggregation<br>**artifact** [APP.06](#task-app-06) — completed [WP-14.05](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05). *Why:* aggregation<br>**artifact** [APP.07](#task-app-07) — completed [WP-14.06](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.06). *Why:* aggregation<br>**artifact** [PLT.17](platform.md#task-plt-17) — real ArcForges.Capabilities application identity and composition root. *Why:* the sample must compose with the delivered capability/application-identity implementation, not a fake or stand-in<br>**artifact** [PLT.27](platform.md#task-plt-27) — real ArcForges.Desktop.Shell project and window/panel host. *Why:* the sample directly consumes the delivered same-repository Shell project; PLT.27 is named directly rather than inferred through another APP task, and no PLT.35 package is required<br>**artifact** [PLT.01](platform.md#task-plt-01) — real single-write-path Persistence.Sqlite store. *Why:* the sample must exercise the existing real local transactional store rather than an in-memory fake or a second persistence mechanism |
| Entry condition | [ADOPT.02.app-composition](adoption.md#task-adopt-02-app-composition) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](assistant.md#task-ast-17) |
| Write scope | `DesktopPlatform:samples/AssistantHost/** (minimal runnable sample only; its packages.lock.json is generated from existing approved dependency identities)`<br>`DesktopPlatform:DesktopPlatform.slnx (register only the APP.08 sample)`<br>`DesktopPlatform:.github/workflows/package-validation.yml (build/run only the sample in the existing validation flow; no new job, matrix or deployment)`<br>`DesktopPlatform:eng/policy/architecture-projects.json (append only the sample project classification)`<br>`DesktopPlatform:eng/policy/runtime-ownership.json (append only the sample's non-production ownership classification)`<br>`DesktopPlatform:eng/policy/licence-boundary.json (append only the sample project classification)`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json (append only the sample project)`<br>`DesktopPlatform:eng/policy/reconciliation/project-updates.json (append only the sample project registration)`<br>`DesktopPlatform:eng/policy/reconciliation/source.json (append only the sample source inventory)`<br>`DesktopPlatform:eng/provenance/files.json (classify only the task-owned sample source and project/lock inputs)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (only exact sample project/lock input bindings for already-admitted dependency identities)`<br>`DesktopPlatform:eng/policy/dependency-reviews/app-08-r1.json (immutable sample admission receipt only if required by the existing dependency gate; no dependency identity, version or closure changes)`<br>`DesktopPlatform:artifacts/evidence/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Build and run the real minimal sample in the existing package-validation flow under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), alongside the single WP14 CI build/pack producing the immutable candidate; record UX-A/B ledger rows per experience/03. No macOS, E2E or live-service CI. |
| Completion evidence | Source commit, package/artifact versions and hashes, environment, UX-A/B acceptance rows, named later-fixture list (none expected for WP14 itself). |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | APP.01 owns only [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00) host-port signatures, product/profile identity and lifetime, and two-identity unit isolation; APP.08 owns [WP-14.00](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00)'s minimal real-integration sample plus [WP-14.90](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.90) acceptance. The sample composes existing host ports with real ArcForges.Capabilities, ArcForges.Desktop.Shell and ArcForges.Persistence.Sqlite; it must not use fakes or fixture stand-ins, implement full AssistantHost UI ([WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17)), add a package identity, or require PLT.35. Register only the sample project/build/run path and its exact existing-policy, reconciliation, provenance and lock bindings; preserve all package identities and dependency versions/closure. Shared build-config and policy-data updates are append-only. |
