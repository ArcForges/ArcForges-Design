# Extension platform and integrations — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Extension host, protocol, capability boundary, package runtime, catalog, SDK and CLI, MCP connectors.

Tasks: 1 · Owning repositories: Contracts · Integration owner(s): Contracts integration owner · Out of scope: 11 (final section)

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [EXT.02](#task-ext-02) | Dual capability boundary (typed layer + closed dynamic value model) | producer | L | [CON.05](contracts.md#task-con-05) (contract) | not-started |

## Tasks

<a id="task-ext-02"></a>

### EXT.02 — Dual capability boundary (typed layer + closed dynamic value model)

**Outcome.** The typed extension-point layer exists as ordinary versioned contracts and the dynamic layer as the closed, AOT-safe StructuredValue/ValueSchema model with bidirectional validation; a repository policy test proves StructuredValue never appears in a first-party domain or product contract, and the host still publishes AOT cleanly.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/ext-02` and ledger record `ledger/tasks/ext-02.md` in the Plan repository; task branch `task/ext-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-41.02](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.02) — full |
| Provides | dual-capability-boundary |
| Start prerequisites | **contract** [CON.05](contracts.md#task-con-05) — the published foundation/value-model proto types this layer extends. *Why:* StructuredValue must build on the already-published foundation types (e.g. arcforges.foundation.v1), not a parallel definition |
| Entry condition | [ADOPT.03.extensions](adoption.md#task-adopt-03-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.03](#task-ext-03) — out of scope, [EXT.04](#task-ext-04) — out of scope, [EXT.08](#task-ext-08) — out of scope, [EXT.90](#task-ext-90) — out of scope, [SCOPE.25](arcscope.md#task-scope-25) |
| Write scope | `Contracts:public/proto/arcforges/extensions/v1/**`<br>`Contracts:public/proto/constraints/ext-02-dual-capability.json (only EXT.02-authored new messages)`<br>`Contracts:public/proto/constraints.json (regenerated from the EXT.02-owned shard; preserve all other shards)`<br>`Contracts:.gitleaks.toml (only exact-path-and-digest generic-api-key exceptions for the six observed input-hash lines described below)`<br>`Contracts:tests/StructureTests/ExtensionBoundaryCases.cs (negative containment test for StructuredValue in first-party domain/product contracts)`<br>`Contracts:tests/StructureTests/Fixtures/structured-value-first-party-domain.proto (task-owned negative test fixture only)`<br>`Contracts:tests/StructureTests/Program.cs (register exactly ExtensionBoundaryCases.Run(root) in the existing console runner only)`<br>`Contracts:tests/tooling/test_dependency_admission.py (only positive and negative tests for the task's exact path-plus-digest Gitleaks exception boundary)`<br>`DesktopPlatform:Directory.Packages.props (only pin the existing ArcForges.Contracts.PublicApi and ArcForges.Sdk.Contracts packages to the exact candidates published by this task's Contracts stage)`<br>`DesktopPlatform:DesktopPlatform.slnx (only register the task-owned product, Tests and AotProbe projects)`<br>`DesktopPlatform:.github/workflows/package-validation.yml (only build, test and AOT-compile steps for this task's projects)`<br>`DesktopPlatform:src/Extensions/ArcForges.Extensions.Contracts/** (product plus nested Tests/AotProbe only)`<br>`DesktopPlatform:eng/policy/architecture-projects.json (task-owned project rows only)`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (task-owned public-API-to-actual-test rows only)`<br>`DesktopPlatform:eng/policy/dependency-policy.json and eng/policy/dependency-reviews/ext-02-r1.json (task-owned inputs and immutable admission receipt only; record the exact PublicApi and Sdk.Contracts candidates from the same Contracts merge, preserve all other coordinates/versions and the existing transitive, xunit and TestSdk closure)`<br>`DesktopPlatform:eng/policy/licence-boundary.json (task-owned project/test classifications only)`<br>`DesktopPlatform:eng/policy/runtime-ownership.json (task-owned extension project row only)`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json, eng/policy/reconciliation/project-updates.json and eng/policy/reconciliation/source.json (task-owned active project/update/source rows only; preserve history)`<br>`DesktopPlatform:eng/provenance/files.json (task-owned source, test, AotProbe and generated project-input classifications only)`<br>`DesktopPlatform:artifacts/evidence/** (task-owned evidence of the extension-host substep only)` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Contracts stage: authored constraint-shard and aggregate checks, generated-shape and fixture checks, and applicable schema/structure tests. Only after that Contracts merge publishes both task candidates, Desktop stage pins the exact ArcForges.Contracts.PublicApi and ArcForges.Sdk.Contracts packages from the same merge and builds/tests the product and nested tests against those packages (never Contracts source); verify value-model coverage per type, bidirectional validation and executable first-party containment rejection. The nested AotProbe must AOT-compile with the platform present under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); compilation only, with no hosted/runtime execution. Keep the pinned Gitleaks scan enabled. Its generic-api-key exception may match only the six observed lines/four unique verified public input SHA256 values in eng/policy/dependency-policy.json and eng/policy/dependency-reviews/ext-02-r1.json, requiring the exact path and digest on the same line (AND); tests must cover exact positives and reject a changed digest, another path, and any unrelated 64-hex value. Do not allow generic 64-hex patterns, whole-file or commit suppressions, scanner/workflow/rule-algorithm changes, or new dependencies. |
| Completion evidence | Contracts source/generation/test results and both exact published package identities, versions and content hashes; Desktop exact two-package pins, locked restore/build/test results, executable containment negative, and native AOT compile result; pinned Gitleaks results and positive/negative exact exception-boundary tests. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Contracts already has public/proto/arcforges/extensions/v1/extensions.proto with ExtensionLease/ExtensionHostService.RenewLease and a generated ArcForges.Sdk.Client (ExtensionLeaseClient.cs) -- WP-03-level groundwork this task extends, not yet the StructuredValue/ValueSchema model itself. |
| Notes | [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) Sec.1 names the AOT-vs-dynamic-value tension as 'the platform's hardest design problem' -- narrow early risk proof. The first-party containment test must execute and reject StructuredValue in first-party domain/product contract source, not merely retain a textual fixture; Program.cs may only register ExtensionBoundaryCases.Run(root), without runner refactoring, other registrations, or execution-order/exit-semantics changes. The fixture and test are task-owned evidence. This is a staged cross-repository task: finish and merge the Contracts proto/owned constraint shard/tests first, then consume only the exact ArcForges.Contracts.PublicApi and ArcForges.Sdk.Contracts candidates published by that same Contracts merge before starting the Desktop consumer stage; never reference unpublished Contracts source. Contracts package ownership is fixed: PublicApi supplies the existing StructuredValue/CapabilityArguments/CapabilityResult types, while Sdk.Contracts owns the generated ValueSchema types from extensions.proto; do not duplicate ValueSchema locally or move extensions.proto into PublicApi. No new package ID or package ecosystem is introduced: the only added dependency identities are these two already-existing NuGet package IDs at their exact task-produced candidate versions; preserve every other coordinate/version and the existing transitive, xunit and TestSdk closure unchanged. Desktop changes are confined to the exact project/configuration/policy/evidence paths listed above, with task-owned additive rows and immutable receipt; no runtime, security, schema, generator, package-identity or unrelated algorithm changes are authorized. The root constraints aggregate is regenerated through the existing generator from only the new EXT.02 shard; do not alter extensions.json, the generator, its manifest or other shards/messages. |

## Out of scope

Excluded from the active plan by the decision named under each heading. These tasks are not completed, are never claimable and are not remaining work; their records and ledger history are kept here.

### P2-026

| Task | Title | Note | Mode | Ledger status |
|---|---|---|---|---|
| [EXT.00](#task-ext-00) | Extension host process and supervision | No necessary ArcScope consumer: the out-of-process extension host is post-V1 because V1 extensions are first-party and in-process ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.01](#task-ext-01) | Handshake and protocol versioning | No necessary ArcScope consumer: the out-of-process extension handshake is post-V1 with the extension host ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.03](#task-ext-03) | Declarative UI and settings contribution | No necessary ArcScope consumer: declarative extension UI panels are post-V1, since no first-party V1 surface uses them ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.04](#task-ext-04) | Package manifest/workflow/panel validators and lifecycle state machine | No necessary ArcScope consumer: manifest validation and the staged install lifecycle are post-V1 because package installation is excluded from V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.05](#task-ext-05) | Six contribution-kind runtime wiring | No necessary ArcScope consumer: runtime wiring of the six package contribution kinds (MCP, connectors, catalog) is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.06](#task-ext-06) | Cloud PackageCatalog producer | No necessary ArcScope consumer: the Cloud PackageCatalog producer serves the community catalog, which is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.07](#task-ext-07) | Desktop and CLI catalog consumers | No necessary ArcScope consumer: the desktop and CLI catalog consumers serve the community catalog, which is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.08](#task-ext-08) | Public SDK and CLI | No necessary ArcScope consumer: the public extension SDK and CLI are post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5); the accepted WP03 groundwork stays as history. | excluded | no record |
| [EXT.09](#task-ext-09) | Local MCP stdio behind the owned connector child | No necessary ArcScope consumer: local MCP stdio connectors are post-V1, and MCP is not in the ArcChat V1 table ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.10](#task-ext-10) | Cloud MCP HTTP placement in the C# Agent module (thin Worker egress route) | No necessary ArcScope consumer: Cloud-placed MCP HTTP connections are post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |
| [EXT.90](#task-ext-90) | Verify owned artifact and real integration (extension platform) | No necessary ArcScope consumer: verification of the out-of-process extension platform and MCP transports is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). | excluded | no record |

<a id="task-ext-00"></a>

#### EXT.00 — Extension host process and supervision

**Outcome.** Per-installation extension processes start on demand and stop when idle inside the package-specific OS isolation profile; resource limits are enforced by termination, crashes trigger backoff restart then quarantine, in-flight invocations fail typed, and no ambient credential is inherited.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: the out-of-process extension host is post-V1 because V1 extensions are first-party and in-process ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-00` and ledger record `ledger/tasks/ext-00.md` in the Plan repository; task branch `task/ext-00` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-41.00](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.00) — full |
| Provides | extension-host |
| Start prerequisites | **artifact** [PLT.45](platform.md#task-plt-45) — the OS-level process isolation / ContentSandbox primitives (broker grants, syscall restriction). *Why:* [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22) require actual packaged-RID isolation; the extension host reuses [WP-11](../../work-packages/11-security-foundation.md#rule-wp-11)'s isolation infrastructure rather than building a new sandbox -- a substitute would fail [PG-22](../../../assurance/open-gates-register.md#rule-pg-22)'s 'no same-user full-trust fallback' bar<br>**contract** [PLT.19](platform.md#task-plt-19) — the typed capability/resource contribution model. *Why:* the host must enforce the same capability model first-party code uses, per [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41)'s own input table |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.01](#task-ext-01) — out of scope, [EXT.09](#task-ext-09) — out of scope, [EXT.90](#task-ext-90) — out of scope |
| Write scope | `DesktopPlatform:src/Extensions/ArcForges.Extensions.Runtime/Host/**` |
| Validation | Hostile-package tests against product DB/token paths, network, sibling-package and process APIs on the real target OS per platform (Windows primary; macOS is outside the delivery scope per [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)); crash/hang/memory-exhaustion/unbounded-output tests; quarantine behaviour; credential-absence assertion. No device/emulator CI -- these run as local/affected-scope checks per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Hostile-process behaviour and credential-absence results ([PG-22](../../../assurance/open-gates-register.md#rule-pg-22)). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |
| Notes | Narrow early risk proof: if real OS-level sandboxing cannot reach [PG-22](../../../assurance/open-gates-register.md#rule-pg-22)'s bar on the target platforms, the whole out-of-process extension model needs redesign. |

<a id="task-ext-01"></a>

#### EXT.01 — Handshake and protocol versioning

**Outcome.** Identity is verified against the installed manifest before any contribution is invoked; more than one protocol version is negotiated during a migration window; impersonation and reserved-namespace claims are refused with a clean explanation.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: the out-of-process extension handshake is post-V1 with the extension host ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-01` and ledger record `ledger/tasks/ext-01.md` in the Plan repository; task branch `task/ext-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.01](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.01) — full |
| Provides | extension-handshake |
| Start prerequisites | **artifact** [EXT.00](#task-ext-00) — a running extension process to handshake with. *Why:* handshake happens over the process EXT.00 supervises |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `DesktopPlatform:src/Extensions/ArcForges.Extensions.Runtime/Handshake/**` |
| Validation | Impersonation and reserved-namespace negative tests; version-negotiation matrix including refusal -- offline/local, no live device needed. |
| Completion evidence | Impersonation, namespace and negotiation results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |

<a id="task-ext-03"></a>

#### EXT.03 — Declarative UI and settings contribution

**Outcome.** Panel declarations from a closed, versioned element vocabulary render with first-party controls; settings schemas are declarative; secret fields yield references only; extension-contributed surfaces are visibly attributed.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: declarative extension UI panels are post-V1, since no first-party V1 surface uses them ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-03` and ledger record `ledger/tasks/ext-03.md` in the Plan repository; task branch `task/ext-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.03](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.03) — full |
| Provides | extension-declarative-ui |
| Start prerequisites | **artifact** [EXT.02](#task-ext-02) — the closed StructuredValue/panel.v1 schema. *Why:* panel declarations are validated against the same closed value model EXT.02 defines |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `DesktopPlatform:src/Extensions/ArcForges.Extensions.Runtime/DeclarativeUi/**` |
| Validation | Vocabulary coverage tests; negative test for raw markup/script rejection; secret-field test; attribution test -- all offline UI-layer tests. |
| Completion evidence | Vocabulary, markup-rejection, secret and attribution results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |

<a id="task-ext-04"></a>

#### EXT.04 — Package manifest/workflow/panel validators and lifecycle state machine

**Outcome.** manifest.v1/workflow.v1/panel.v1 validators exist from published Contracts, and package installation moves only through the immutable staged states (acquired/verified/staged/awaitingConsent/active/disabled/quarantined/removed) with no state that resets an effect fence.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: manifest validation and the staged install lifecycle are post-V1 because package installation is excluded from V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/ext-04` and ledger record `ledger/tasks/ext-04.md` in the Plan repository; task branch `task/ext-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.04](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.04) — manifest.v1/workflow.v1/panel.v1 validators and the immutable staged install/update/drain/migration/revocation/rollback state machine |
| Provides | package-lifecycle-engine |
| Start prerequisites | **artifact** [EXT.02](#task-ext-02) — the closed value model workflow.v1 nodes are typed against. *Why:* workflow.v1 DAG nodes are StructuredValue-typed and must validate against EXT.02's schema validator<br>**artifact** [CON.16](contracts.md#task-con-16) — android-update.v1 format and [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) fixture signing keys (catalog and realm schemas are out, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). *Why:* archive signature verification in the lifecycle state machine needs a signed vector to check against; production keys are not required this early (see SUB-catalog-fixture-signing) |
| Entry condition | [ADOPT.03.extensions](adoption.md#task-adopt-03-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.05](#task-ext-05) — out of scope, [EXT.90](#task-ext-90) — out of scope |
| Permitted substitutes | [SUB-signed-format-fixture-keys](../substitutes.md#sub-signed-format-fixture-keys) |
| Write scope | `Contracts:public/proto/arcforges/extensions/v1/**`<br>`DesktopPlatform:src/Extensions/ArcForges.Extensions.Packaging/Lifecycle/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Archive traversal/size/signature tests, DAG bounds (maxItems<=100, nesting<=2, 256 expanded steps), increased-permission re-consent, active-old-job, private-state rollback incompatibility, unknown-effect tests -- all offline against fixture-signed archives. |
| Completion evidence | Lifecycle matrix, re-consent, uninstall and revoke results (part). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |

<a id="task-ext-05"></a>

#### EXT.05 — Six contribution-kind runtime wiring

**Outcome.** Each of the six contribution kinds registers and executes through the lifecycle engine and the dual capability boundary; a running task freezes the package version it started with ([BR-10](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-10)); uninstall never cascade-deletes professional resources the extension created ([BR-11](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-11)).

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: runtime wiring of the six package contribution kinds (MCP, connectors, catalog) is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-05` and ledger record `ledger/tasks/ext-05.md` in the Plan repository; task branch `task/ext-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-41.04](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.04) — the six package contribution kinds (skill/template/workflow/mcp/connector/extension) runtime registration and execution wiring |
| Provides | extension-contribution-kinds |
| Start prerequisites | **artifact** [EXT.04](#task-ext-04) — the lifecycle state machine to register kinds into. *Why:* a contribution kind has nothing to attach to before install states exist |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `DesktopPlatform:src/Extensions/ArcForges.Extensions.Registry/Contributions/**` |
| Validation | Per-kind lifecycle tests; version-freeze-during-running-task test; uninstall-preserves-resources test -- offline. |
| Completion evidence | Lifecycle matrix, re-consent, uninstall and revoke results (remainder). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |

<a id="task-ext-06"></a>

#### EXT.06 — Cloud PackageCatalog producer

**Outcome.** Cloud PackageCatalog accepts immutable submissions with DNS publisher verification, holds review-state/revocation authority and produces a signed static index; only OperatorService (not the console or the Extensions implementation) writes PackageCatalog tables.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: the Cloud PackageCatalog producer serves the community catalog, which is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ext-06` and ledger record `ledger/tasks/ext-06.md` in the Plan repository; task branch `task/ext-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-41.05](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.05) — Cloud PackageCatalog producer: DNS publisher verification, immutable submissions, review-state/revocation authority, signed static index<br>[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) PackageCatalog ownership paragraph (Sec.5-6 boundary): OperatorService is sole authenticator/caller; neither Extensions Runtime nor console writes PackageCatalog tables — package-level obligation contribution |
| Provides | package-catalog-producer |
| Start prerequisites | **artifact** [CLOUD.16](cloud.md#task-cloud-16) — publisher identity/PAT and operator authentication. *Why:* owner/PAT/operator separation is a completion requirement; catalog submission must authenticate against the real identity surface<br>**artifact** [CLOUD.42](cloud.md#task-cloud-42) — durable blob storage for submitted package archives. *Why:* immutable submissions need durable, content-addressed storage<br>**artifact** [CON.16](contracts.md#task-con-16) — [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) fixture catalog/index/revocation/update/realm schemas and signed vectors. *Why:* the index producer can be built and tested against fixture signing keys before [WP-53](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) production keys exist (see SUB-catalog-fixture-signing) |
| Entry condition | [ADOPT.07.extensions](adoption.md#task-adopt-07-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.07](#task-ext-07) — out of scope, [EXT.08](#task-ext-08) — out of scope, [EXT.90](#task-ext-90) — out of scope, [OPS.11](operations.md#task-ops-11) — out of scope |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.PackageCatalog/** (the one project of the module, CLOUD.02 layout; its Domain, Application and Infrastructure layers are folders and namespaces)` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Owner/PAT/operator separation, duplicate-version conflict, invalid archive, review/revoke replay, signed-index rollback/expiry, offline installed-package behavior -- Cloud integration tests against ephemeral D1, no live DNS/public network in CI. |
| Completion evidence | Hostile catalog and unreachable-catalog results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-ext-07"></a>

#### EXT.07 — Desktop and CLI catalog consumers

**Outcome.** Desktop and CLI consume the signed static index and PackageCatalog methods to install/update packages, with correct offline behavior when the catalog is unreachable.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: the desktop and CLI catalog consumers serve the community catalog, which is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-07` and ledger record `ledger/tasks/ext-07.md` in the Plan repository; task branch `task/ext-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.05](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.05) — desktop/CLI catalog consumers |
| Provides | package-catalog-consumers |
| Start prerequisites | **artifact** [EXT.06](#task-ext-06) — the real signed static index format and PackageCatalog API. *Why:* a consumer cannot be finished against an unpublished producer shape, though it may develop against EXT.06's fixture-signed index first |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `DesktopPlatform:src/Extensions/ArcForges.Extensions.Registry/CatalogClient/**` |
| Validation | Catalog-unavailable-never-disables-installed-packages test; signed-index rollback/expiry consumption test -- offline. |
| Completion evidence | Hostile catalog and unreachable-catalog results (consumer half). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |
| Notes | [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) (the commerce, policy and operations lanes OPS review console) is a downstream consumer of these same EXT.06/07 methods -- noted for integration owner cross-check, not a completion blocker here. |

<a id="task-ext-08"></a>

#### EXT.08 — Public SDK and CLI

**Outcome.** The SDK, validators and tool-payload projections generate from authored public proto; the CLI uses eligible publisher PAT and catalog/resource methods; validate matches host install checks; no generated schema is inferred from C# reflection.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: the public extension SDK and CLI are post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5); the accepted WP03 groundwork stays as history. |
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/ext-08` and ledger record `ledger/tasks/ext-08.md` in the Plan repository; task branch `task/ext-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.06](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.06) — full<br>[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 8: MCP vocabulary mapping + SDK version pin -- [VG-02](../../../assurance/open-gates-register.md#rule-vg-02) — package-level obligation contribution |
| Provides | extension-public-sdk |
| Start prerequisites | **artifact** [EXT.02](#task-ext-02) — the published extension protocol/value-model proto to generate from. *Why:* the SDK generator's input is EXT.02's authored proto<br>**artifact** [CLOUD.16](cloud.md#task-cloud-16) — publisher PAT issuance. *Why:* the CLI publish flow requires a real PAT-scoped identity |
| Entry condition | [ADOPT.03.extensions](adoption.md#task-adopt-03-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [EXT.06](#task-ext-06) — the real Cloud PackageCatalog submit endpoint. *Why:* CLI publish must submit for review against the real endpoint, not a fixture, to close this substep's own gate ('CLI publish submits for review and never uploads directly into public catalog visibility') |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `Contracts:src/SDK/ArcForges.SDK.*/**`<br>`Contracts:src/SDK/ArcForges.Cli/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Independent SDK consumer test, manifest/tag compatibility, PAT scope tests, generated-vs-reflection negative test -- offline codegen tests. |
| Completion evidence | Generator, validate-parity and first-party build results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Contracts already has src/public/dotnet/ArcForges.Sdk.Client and ArcForges.Sdk.Contracts with generated ExtensionLeaseClient.cs and proto-generated types -- early groundwork, not the full SDK/CLI generator this task builds. |

<a id="task-ext-09"></a>

#### EXT.09 — Local MCP stdio behind the owned connector child

**Outcome.** Local MCP servers run stdio behind an owned connector child process; only that child speaks ArcForges gRPC; origin/scope changes invalidate consent; no browser/Android local subprocess exists; child crash/lease recovery works.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: local MCP stdio connectors are post-V1, and MCP is not in the ArcChat V1 table ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-09` and ledger record `ledger/tasks/ext-09.md` in the Plan repository; task branch `task/ext-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.07](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) — local MCP stdio placement behind the owned connector child process<br>[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 8: MCP vocabulary mapping + SDK version pin -- [VG-02](../../../assurance/open-gates-register.md#rule-vg-02) — package-level obligation contribution |
| Provides | mcp-local-placement |
| Start prerequisites | **artifact** [EXT.00](#task-ext-00) — the extension host's process supervision primitives. *Why:* the connector child reuses the same supervised-process model EXT.00 builds, per [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)'s out-of-process default |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `DesktopPlatform:src/Communication/Mcp/**` |
| Validation | Origin/scope-change consent invalidation test; no-unrestricted-AI-fetch test; child crash/lease recovery test -- offline/local process tests. |
| Completion evidence | MCP mapping record, connector secret and no-delegation structural results (local half). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |

<a id="task-ext-10"></a>

#### EXT.10 — Cloud MCP HTTP placement in the C# Agent module (thin Worker egress route)

**Outcome.** Cloud-placed MCP connections are owned in C#: the MCP client, connection registry, placement and secret-reference owner live in the Cloud Agent module; standard MCP protocol is preserved; each connection has one placement and one secret owner with exact failure and egress behavior; MCP content is treated as untrusted data ([HV-19](../../../architecture/17-agent-harness.md#rule-hv-19)). Cloud-placed MCP HTTP placement ([WP-41.07](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07)) is delivered through a separate MCP egress route: C# decides each connection, destination, secret reference and failure mapping, and the Cloud Worker outbound handler is thin transport that enforces only the C#-supplied host allowlist and the transport guards (443 only, no private addresses, no redirects). The route is not the ai.internal adapter, which [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 5 limits to Workers AI on the env.AI binding.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: Cloud-placed MCP HTTP connections are post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ext-10` and ledger record `ledger/tasks/ext-10.md` in the Plan repository; task branch `task/ext-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-41.07](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) — Cloud MCP HTTP placement (functional acceptance kept as written; satisfied by a working placement through the C#-decided MCP egress route, never by a refusal)<br>[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 8: MCP vocabulary mapping + SDK version pin -- [VG-02](../../../assurance/open-gates-register.md#rule-vg-02) — package-level obligation contribution |
| Provides | mcp-cloud-placement |
| Start prerequisites | **contract** [CON.15](contracts.md#task-con-15) — the generated internal HTTP registry, to attach the MCP egress route (C#-supplied allowlist) to. *Why:* the MCP egress route is declared in the fixed generated registry, not registered ad hoc |
| Entry condition | [ADOPT.07.extensions](adoption.md#task-adopt-07-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.90](#task-ext-90) — out of scope |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/Mcp/**`<br>`Cloud:tests/ArcForges.Cloud.Tests/Mcp/**`<br>`Cloud:worker/mcp/** (thin outbound transport adapter for the MCP egress route; enforces only the C#-supplied allowlist and transport guards)` |
| Validation | Standard-MCP-transport preservation test over a loopback MCP fixture server reached from the test process only (a test transport, not the production egress path); secret-as-reference test; HTTP placement test that runs a Cloud-placed MCP HTTP connection through the MCP egress route to the same loopback fixture; egress-control tests: a destination outside the C#-supplied allowlist, a non-443 port, a private address and a redirect are each refused fail-closed with the egress-denied failure, and an architecture test shows that the ai.internal adapter carries no MCP traffic; MCP content untrusted-data test. In ArcForges.Cloud.Tests, offline; no live external MCP endpoint and no hosted CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | MCP mapping record, connector secret and no-delegation structural results (Cloud half); HTTP placement result through the MCP egress route against the loopback fixture (test transport); egress-control and no-ai.internal-MCP architecture results; coordinator adjudication 6 (2026-10-08, brief section 6, MCP and connector egress) as the decision reference. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08. No MCP code in either repository. AI main b2b3aa2 has no src/mcp tree (runtime is src/index.ts, hello.ts, model.ts, deployment.ts, model-diagnostics.ts). Cloud b05361e has the module shell src/ArcForges.Cloud.Modules.Agent (AgentModule.cs and project only), no extension module, and no MCP or AI route in worker/. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021); coordinator adjudication 6): the MCP client moves from the AI repository (src/mcp, not on main) to the C# Cloud Agent module. MCP HTTP egress is decided: C# decides, and the Worker outbound handler is thin transport enforcing only the C#-supplied host allowlist and the transport guards (443 only, no private addresses, no redirects). The route cannot reuse the ai.internal adapter ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 5). The connection-registry, secret-reference and untrusted-data rules stay C#-owned. [WP-41.07](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) functional acceptance is kept as written, and no obligation is removed. |

<a id="task-ext-90"></a>

#### EXT.90 — Verify owned artifact and real integration (extension platform)

**Outcome.** SDK/protocol, desktop host/runtime and Cloud registry ownership are verified split correctly; standard MCP transports and out-of-process extensions are preserved; no external-agent delegation or in-process third-party plugin exists anywhere; [VG-02](../../../assurance/open-gates-register.md#rule-vg-02) and [PG-09](../../../assurance/open-gates-register.md#rule-pg-09) close.

| Field | Value |
|---|---|
| Scope | Out of scope (P2-026): No necessary ArcScope consumer: verification of the out-of-process extension platform and MCP transports is post-V1 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S5). |
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ext-90` and ledger record `ledger/tasks/ext-90.md` in the Plan repository; task branch `task/ext-90` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Package acceptance | Records the [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-41.90](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.90) — full<br>[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 9: extension protocol conformance suite -- [PG-09](../../../assurance/open-gates-register.md#rule-pg-09) — package-level obligation contribution |
| Provides | extension-platform-acceptance |
| Start prerequisites | **artifact** [EXT.00](#task-ext-00) — all prior EXT tasks complete (EXT.00-EXT.10). *Why:* acceptance aggregates every EXT task's evidence<br>**artifact** [EXT.01](#task-ext-01) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.02](#task-ext-02) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.03](#task-ext-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.04](#task-ext-04) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.05](#task-ext-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.06](#task-ext-06) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.07](#task-ext-07) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.08](#task-ext-08) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.09](#task-ext-09) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [EXT.10](#task-ext-10) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.02.extensions](adoption.md#task-adopt-02-extensions) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:tests/McpAotTests/**`<br>`DesktopPlatform:tests/ExtensionPlatformTests/**` |
| Validation | SDK licence/protocol compatibility, capability checks, hostile-extension/process isolation and owner execution tests; local gRPC closure suite (extension host<->child real generated gRPC roles, ConnectorBroker consent/secret rotation/revocation, forged-identity/direct-SSO-access denial). |
| Completion evidence | Owned artifact and real-integration receipt; [PG-09](../../../assurance/open-gates-register.md#rule-pg-09) protocol conformance suite pass; [VG-02](../../../assurance/open-gates-register.md#rule-vg-02) MCP vocabulary mapping + SDK version pin record. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform repo has no src/Extensions or src/Communication tree; only src/Build, src/BuildingBlocks, src/DesktopHelpers, src/Native exist. |
