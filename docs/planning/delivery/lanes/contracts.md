# Contracts schema closures — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Handwritten proto and HTTP-exception closures, generated C#, TypeScript and Kotlin packages, vectors and compatibility gates.

Tasks: 25 · Owning repositories: Contracts · Integration owner(s): Contracts integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [CON.01](#task-con-01) | Shard contended eng inventory/constraint files by domain; fix one-owner merge protocol | governance | S | none | not-started |
| [CON.02](#task-con-02) | Capability/action/context/version/health descriptor records + immutable oversized-body reference (EncodedBodyRef) | contract | M | [CON.91](#task-con-91) (contract) | not-started |
| [CON.03](#task-con-03) | Resource/Sync owner-body admission: closed Sync mutation allowlist + cross-owner/wrong-revision/opaque-object/forbidden-path negatives | contract | M | [CON.02](#task-con-02) (contract) | not-started |
| [CON.04](#task-con-04) | ContentSandbox service schema (24 methods: session/slot/media/image/PDF/OTIO) | contract | L | none | not-started |
| [CON.05](#task-con-05) | Extension/Connector/LocalBootstrap service schema (annex09 helper closure minus ContentSandbox) | contract | M | none | not-started |
| [CON.06](#task-con-06) | Product in-process port completion: INotesOperations/IScopeOperations/ISlateOperations/IChatOperations + infra ports | contract | L | [CON.02](#task-con-02) (contract) | not-started |
| [CON.07](#task-con-07) | Identity/session/device operation registry + native-auth and browser HTTP exceptions | contract | L | none | not-started |
| [CON.08](#task-con-08) | Entitlement/commerce operation registry | contract | M | none | not-started |
| [CON.09](#task-con-09) | Sync/resource-transfer/objects operation registry + realm-transfer.v1 | contract | L | [CON.03](#task-con-03) (contract) | not-started |
| [CON.10](#task-con-10) | Task/approval/bridge/chat/agent/automation/search operation registry + ai-internal package | contract | L | [CON.02](#task-con-02) (contract) | not-started |
| [CON.11](#task-con-11) | Application/history/execution/events operations (annex10's 13 additions) + EventService | contract | M | [CON.10](#task-con-10) (contract) | not-started |
| [CON.12](#task-con-12) | Extension and policy schemas: manifest.v1/workflow.v1/panel.v1/policy body.v1/configuration.v1 | contract | M | none | not-started |
| [CON.13](#task-con-13) | Package catalog operation registry (CatalogService) | contract | S | none | not-started |
| [CON.14](#task-con-14) | Operator control service (OperatorService, full §9/9.1/9.2 protocol) | contract | L | [CON.13](#task-con-13) (contract) | not-started |
| [CON.15](#task-con-15) | Cloudflare-internal HTTP bindings (AI Worker <-> C# ports beyond ai-internal's chat/task family) | contract | M | [CON.11](#task-con-11) (contract) | not-started |
| [CON.16](#task-con-16) | Signed catalog/update/realm formats (catalog-index.v1, catalog-revocations.v1, android-update.v1, realm.v1) | contract | M | none | not-started |
| [CON.17](#task-con-17) | Cross-language compatibility window + canonical semantic hash | contract | M | [CON.92](#task-con-92) (contract) | not-started |
| [CON.18](#task-con-18) | Operation-scope manifest + authorization-reachability matrix generator | contract | S | none | not-started |
| [CON.19](#task-con-19) | WP03.90 — verify the owned Contracts artifact and its real (non-consumer) integration | contract | M | [CON.02](#task-con-02) (contract), [CON.18](#task-con-18) (contract), [CON.03](#task-con-03) (artifact), [CON.04](#task-con-04) (artifact), [CON.05](#task-con-05) (artifact), [CON.06](#task-con-06) (artifact), [CON.07](#task-con-07) (artifact), [CON.08](#task-con-08) (artifact), [CON.09](#task-con-09) (artifact), [CON.10](#task-con-10) (artifact), [CON.11](#task-con-11) (artifact), [CON.12](#task-con-12) (artifact), [CON.13](#task-con-13) (artifact), [CON.14](#task-con-14) (artifact), [CON.15](#task-con-15) (artifact), [CON.16](#task-con-16) (artifact), [CON.17](#task-con-17) (artifact), [CON.20](#task-con-20) (artifact), [CON.21](#task-con-21) (artifact), [CON.22](#task-con-22) (artifact), [CON.01](#task-con-01) (artifact) | not-started |
| [CON.20](#task-con-20) | Notes public operation registry | contract | M | [CON.02](#task-con-02) (contract) | not-started |
| [CON.21](#task-con-21) | Simulation operation registry | contract | M | [CON.02](#task-con-02) (contract) | not-started |
| [CON.22](#task-con-22) | Account support, notification, data, preference, policy-bundle and export-job operations | contract | M | [CON.02](#task-con-02) (contract) | not-started |
| [CON.90](#task-con-90) | WP03.00 — split project structure (accepted, historical) | contract | M | none | accepted |
| [CON.91](#task-con-91) | WP03.01 — foundation contract types (accepted, historical) | contract | L | none | accepted |
| [CON.92](#task-con-92) | WP03.02 — serialization posture (accepted, historical) | contract | M | none | accepted |

## Tasks

<a id="task-con-01"></a>

### CON.01 — Shard contended eng inventory/constraint files by domain; fix one-owner merge protocol

**Outcome.** public/proto/constraints.json and internal/proto/constraints.json are split into small per-domain shard files (mirroring the already-proven fixtures/public/wp03-NN.json pattern) merged by eng/contracts.py; eng/contract-packages.json and eng/foundation-inventory.json gain a documented append protocol; a short CONTRIBUTING note fixes the single Contracts integration owner who serially merges CON.* branches.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-01` and ledger record `ledger/tasks/con-01.md` in the Plan repository; task branch `task/con-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — contention reduction that lets Contracts closures be authored concurrently |
| Provides | sharded-constraint-files; contracts-merge-protocol |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19) |
| Write scope | `Contracts:eng/contracts.py`<br>`Contracts:public/proto/constraints/**`<br>`Contracts:internal/proto/constraints/**`<br>`Contracts:CONTRIBUTING.md` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: eng/contracts.py generate --check round-trips the sharded constraints back to the same effective merged content; existing eng/check_foundation.py and check_serialization.py pass unchanged. |
| Completion evidence | eng/contracts.py generate --check clean; diff shows only file-layout change, zero constraint-content change. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: public/proto/constraints.json is a single 3070-line file today (confirmed by direct read), alphabetically ordered by fully-qualified message name; internal/proto/constraints.json is a single 107-line file. No sharding exists yet. |
| Notes | Optional enabler: without it, closure pull requests edit the same constraint files and are merged one at a time with rebase-and-regenerate by the Contracts integration owner, which remains the fallback protocol. |

<a id="task-con-02"></a>

### CON.02 — Capability/action/context/version/health descriptor records + immutable oversized-body reference (EncodedBodyRef)

**Outcome.** CapabilityDescriptor, ActionDescriptor, ContextProvider/ContextDescriptor, CompatibilityDescriptor/ContractVersion/FeatureSet and HealthSnapshot/InstancePresence/InstanceHealth/InstanceReadiness records (architecture 02-contracts-and-protocols.md §4/5/6/11/12 domain model) are generated in Foundation or PublicApi as appropriate, plus EncodedBodyRef (registry04 §4) wired into every ResponseMeta.value oneof tag-4 read projection; independent positive/negative fixtures cover descriptor shape and the >4MiB large-read-projection envelope (messageType/descriptorHash/byteLength/snapshotToken/ResourceVersionRef SHA256 check before decode).

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-02` and ledger record `ledger/tasks/con-02.md` in the Plan repository; task branch `task/con-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) — capability/action/context/version/health descriptor records only, plus EncodedBodyRef (the immutable oversized-body reference form); excludes the Sync mutation allowlist and cross-owner/wrong-revision/opaque-object/forbidden-path negative vectors, which are CON.03 |
| Provides | capability-action-context-descriptors; encoded-body-ref |
| Start prerequisites | **contract** [CON.91](#task-con-91) — published Foundation ResourceRef/ResourceVersionRef/ArtifactRef (already generated) as the base EncodedBodyRef.resource field type. *Why:* EncodedBodyRef's resource field is a ResourceVersionRef; without the already-published Foundation closure this can't compile. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.01](app-composition.md#task-app-01), [CON.03](#task-con-03), [CON.06](#task-con-06), [CON.10](#task-con-10), [CON.19](#task-con-19), [CON.20](#task-con-20), [CON.21](#task-con-21), [CON.22](#task-con-22), [SCOPE.20](arcscope.md#task-scope-20) |
| Write scope | `Contracts:public/proto/arcforges/foundation/v1/foundation.proto`<br>`Contracts:public/proto/constraints/foundation-descriptors.json`<br>`Contracts:fixtures/public/con-02-descriptors.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline unit tests for descriptor round-trip (C#/TS), decode-limit fixtures (exact 64MiB boundary and 64MiB+1 refusal) reusing WP03.02's WireLimits constants, deterministic regeneration, generated-header/import checks; no macOS/device/live-service CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Independent fixture file con-02-descriptors.json; C#/TS conformance report; descriptor baseline diff. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Grepped the whole repo for CapabilityDescriptor/ActionDescriptor/ContextDescriptor/HealthSnapshot/InstancePresence/InstanceHealth/InstanceReadiness/CompatibilityDescriptor/EncodedBodyRef/ApplicationPresence: zero matches anywhere. None of these types exist in any form. |
| Notes | This is the 'descriptor' half of [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03). Small and foundational: many later domain tasks (CON.06 in-process ports, CON.10 task/chat tool binding) reference CapabilityDescriptor for tool metadata, so this should land early even though nothing strictly blocks it from running in parallel with CON.03-CON.05. |

<a id="task-con-03"></a>

### CON.03 — Resource/Sync owner-body admission: closed Sync mutation allowlist + cross-owner/wrong-revision/opaque-object/forbidden-path negatives

**Outcome.** A generated/schema-derived validator enforces that Sync (registry04 §10) accepts client-origin writes only for NotebookBody/NotesDocument/PropertyDefinition/SavedViewRecord/TagRecord and authorized ScopeMetadata/SlateMetadata (AggregateBody's Cloud-writable subset), refusing TaskSnapshot/AutomationView/ConversationBody/AgentProfile/SkillRecord/ChatProjectRecord/MemoryRecord/PreferenceRecord as client writes (Cloud-authored-only); externalBody indirection resolves to the same allowlist before validation. Independent negative vectors cover cross-owner reference, wrong-revision precondition, opaque/unknown AggregateBody variant, and forbidden-path (non-allowlisted body kind) attempts, plus compatible unknown-response preservation.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-03` and ledger record `ledger/tasks/con-03.md` in the Plan repository; task branch `task/con-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) — the Sync mutation allowlist and oversized-body admission negative-vector half; ResourceRef/ResourceVersionRef/BlobRef schema itself is already done (CON.91/[WP-03.01](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.01)) |
| Provides | sync-mutation-allowlist; owner-body-admission-negatives |
| Start prerequisites | **contract** [CON.02](#task-con-02) — EncodedBodyRef record. *Why:* the 'immutable oversized-body reference form' [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) asks for is EncodedBodyRef; the admission validator must recognize it as the alternative to an inline AggregateBody. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.37](cloud.md#task-cloud-37), [CON.09](#task-con-09), [CON.19](#task-con-19), [NOTES.02](arcnotes.md#task-notes-02) |
| Write scope | `Contracts:public/proto/arcforges/publicapi/v1/content.proto`<br>`Contracts:fixtures/public/con-03-sync-allowlist.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline positive/negative fixture suite (C#/TS); schema-level validator only (no owner authorization, persistence or transaction — those stay with [WP-07](../../work-packages/07-local-persistence-foundation.md#rule-wp-07)/[WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) per CA rules). |
| Completion evidence | fixtures/public/con-03-sync-allowlist.json with named negative cases; validator unit test report. |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: The underlying AggregateBody oneof (all 16 branches) and every named record it references already exist and are published (WP03.01). Only the ADMISSION RULE (which branches Sync may accept as a client write) and its negative vectors are missing — confirmed by grepping content.proto for SyncScope/SyncChange/ChangeProposal/ChangeReceipt/AggregateView/ConflictView/BootstrapManifest: none exist yet either (those are CON.09's job, registry04 §5 Sync service operations, not this validator). |
| Notes | Deliberately scoped narrower than 'author SyncService.* RPC methods' (that's CON.09, part of the huge [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) business-operation registry). CON.03 is only the shared-record ADMISSION RULE that CON.09's SyncService.pushChange/pushBatch and [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21)'s real D1 sync both must obey — keeping it separate lets [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) pin an early closure (CON.03) without waiting for the full SyncService RPC surface (CON.09). |

<a id="task-con-04"></a>

### CON.04 — ContentSandbox service schema (24 methods: session/slot/media/image/PDF/OTIO)

**Outcome.** internal/proto/arcforges/local/sandbox/v1/sandbox.proto has the complete ContentSandboxService with all 24 methods, generated into ArcForges.Contracts.LocalRpc.Sandbox; wrong-child-direction/removed-method/cross-product-registration negative fixtures pass; policy test asserts every method carries the generated service/descriptor identity (CA rule).

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-04` and ledger record `ledger/tasks/con-04.md` in the Plan repository; task branch `task/con-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.04](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.04) — ContentSandboxService only, from annex 09 §§2-6 (OpenSession/RenewSession/GrantSlot/AckBuffer/ProbeMedia/OpenMediaReader/ReadMediaFrame/SeekMedia/CopyVideoFrame/CopyAudioFrame/CloseFrame/CloseReader/OpenImage/GetImageInfo/ReadImageTile/CloseImage/OpenPdf/GetPdfPage/ExtractPdfText/RenderPdfTile/ClosePdf/ReadOtio/WriteOtio/OtioReadChunk/CancelSession/CloseSession = 24 methods)<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) §7 evidence: Local gRPC closure — complete.LocalRpc.Platform/.Sandbox typed parser/connector/hint/bootstrap methods before consumers — package-level obligation contribution |
| Provides | content-sandbox-schema |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [PLT.09](platform.md#task-plt-09), [PLT.15](platform.md#task-plt-15), [PLT.45](platform.md#task-plt-45) |
| Write scope | `Contracts:internal/proto/arcforges/local/sandbox/v1/sandbox.proto`<br>`Contracts:src/internal/dotnet/ArcForges.Contracts.LocalRpc.Sandbox/**`<br>`Contracts:fixtures/internal/con-04-content-sandbox.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: wrong-direction/removed-method/parent-death/cross-product-registration negative fixtures (per annex09 §6 required test list); policy test for generated service/descriptor identity; no real helper process, no live parser (that is [WP-11](../../work-packages/11-security-foundation.md#rule-wp-11)/[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13)). |
| Completion evidence | fixtures/internal/con-04-content-sandbox.json; RPC policy test report. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: SandboxLimits (7-field record) already exists as a WP03.00 seed slice. No ContentSandboxService and none of its 24 methods exist (confirmed: grep '^service ' finds only HelloService and ExtensionHostService anywhere in the repo). |
| Notes | The single biggest service in the whole registry (24 methods). Independently implementable in parallel with CON.05/CON.06 — different proto file (sandbox/v1 vs platform/v1), different owning package (.LocalRpc.Sandbox vs.LocalRpc.Platform/.Chat/.Notes/.Scope/.Slate). |

<a id="task-con-05"></a>

### CON.05 — Extension/Connector/LocalBootstrap service schema (annex09 helper closure minus ContentSandbox)

**Outcome.** Public ExtensionHostService gains Handshake/Invoke/Stop (Handshake already partially scoped by extensions.proto's ExtensionLease); internal LocalBootstrapService (platform/v1) and ConnectorBroker are generated with the exact bootstrap transcript (HMAC-SHA256 challenge/confirm, one-use 32-byte secret) and connector state machine from annex09 §§2,6; IHubRegistry/IHubRouting/DeviceSsoBrokerService names are reserved in a retirement manifest and asserted absent from active service registration by a structural test.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-05` and ledger record `ledger/tasks/con-05.md` in the Plan repository; task branch `task/con-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.04](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.04) — ExtensionHostService (remaining Handshake/Invoke/Stop; RenewLease already done), ILocalBootstrap (Challenge/Confirm/Renew), IConnectorBroker (ListDefinitions/ListConnections/BeginConnection/CompleteConnection/GetConnection/RevokeConnection); reserve removed Hub/SSO/transfer names (IHubRegistry/IHubRouting/DeviceSsoBrokerService) without registering them<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) §7 evidence: Local gRPC closure — complete.LocalRpc.Platform/.Sandbox typed parser/connector/hint/bootstrap methods before consumers — package-level obligation contribution |
| Provides | extension-connector-bootstrap-schema |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [EXT.02](extensions.md#task-ext-02), [PRF.04](runtime-proofs.md#task-prf-04) |
| Write scope | `Contracts:public/proto/arcforges/extensions/v1/extensions.proto`<br>`Contracts:internal/proto/arcforges/local/platform/v1/platform.proto`<br>`Contracts:fixtures/internal/con-05-extension-connector-bootstrap.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: replayed/cross-connection confirm, expired nonce, wrong child direction/role negative fixtures (annex09 §2/§6); structural test asserting Hub/SSO registration absence; no live OS pipe/socket (that is [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)/[WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08)/[WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09)/[WP-11](../../work-packages/11-security-foundation.md#rule-wp-11)). |
| Completion evidence | fixtures/internal/con-05-extension-connector-bootstrap.json; retirement-manifest structural test report. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ExtensionLease + ExtensionHostService.RenewLease exist (WP03.00 seed). Handshake/Invoke/Stop, LocalBootstrapService and ConnectorBroker do not exist at all. |
| Notes | Independent of CON.04 (different proto files/packages). |

<a id="task-con-06"></a>

### CON.06 — Product in-process port completion: INotesOperations/IScopeOperations/ISlateOperations/IChatOperations + infra ports

**Outcome.** Every method in manifest11's 'in-process' scope class (ICapabilityProvider, IContextProvider, IArtifactHandler, IResourceAccess, IProductLifecycle, IDeepLinkTarget, INotesOperations [26 methods], IScopeOperations [13], ISlateOperations [19], IChatOperations [8]) is generated as a typed request/result pair per registry04 §6, with product-port packages containing only in-process records (no listener/gRPC registration) and a policy test proving that.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-06` and ledger record `ledger/tasks/con-06.md` in the Plan repository; task branch `task/con-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.04](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.04) — the 'Product interfaces use generated records and static in-process adapters' half — full method surface for the four product-port packages plus ICapabilityProvider/IContextProvider/IArtifactHandler/IResourceAccess/IProductLifecycle/IDeepLinkTarget<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (source KnowledgePolicy/Patch/View, typed one-use overrides, Notes run/atom/table-cell positions, complete initial owner/profile records) — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior: source KnowledgePolicy/Patch/View and typed one-use overrides (source.getPolicy/setPolicy/clearPolicy, source.createConsent/revokeConsent) fall inside IChatOperations/context-provider scope; stable Notes run/atom/table-cell positions (NotesTextPosition already exists in content.proto from WP03.01 — this task only needs to verify no gap remains for table-cell addressing); package-level obligation contribution |
| Provides | product-in-process-ports |
| Start prerequisites | **contract** [CON.02](#task-con-02) — CapabilityDescriptor/ContextDescriptor shapes. *Why:* ICapabilityProvider.Describe returns CapabilityDescriptor[] and IContextProvider.ProvideContext returns a ContextContribution keyed on those descriptor shapes; without CON.02 this can't be typed. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [SLATE.12](arcslate.md#task-slate-12) |
| Write scope | `Contracts:internal/proto/arcforges/local/chat/v1/chat.proto`<br>`Contracts:internal/proto/arcforges/local/notes/v1/notes.proto`<br>`Contracts:internal/proto/arcforges/local/scope/v1/scope.proto`<br>`Contracts:internal/proto/arcforges/local/slate/v1/slate.proto`<br>`Contracts:fixtures/internal/con-06-product-ports.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: policy test asserting no product gRPC listener/registration exists; positive/negative fixtures for representative methods per product (full behavioral testing stays with each product's own WP1x/3x). |
| Completion evidence | fixtures/internal/con-06-product-ports.json; in-process-only policy test report. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Each of the four LocalRpc product packages has exactly one seed result record from WP03.00 (e.g. NotesOperationsServiceTrashDocumentValue). The other ~25/12/18/7 methods per product do not exist. |
| Notes | Four independent product sub-surfaces (Notes/Scope/Slate/Chat) that could in principle be four separate tasks; kept as one task because they share the same infra-port dependency (ICapabilityProvider etc.) and are individually S-to-M sized — splitting further would violate the 'do not create one task per trivial item' guidance. A future re-split by product is reasonable if a product-area team wants to own its own port slice. |

<a id="task-con-07"></a>

### CON.07 — Identity/session/device operation registry + native-auth and browser HTTP exceptions

**Outcome.** IdentityService/WorkspaceService/DeviceService are generated with all listed operations, exact request/response field tags, and the eight authorization fields exported per operation; GET /session/v1/native/authorize, POST /session/v1/native/token and the four /session/v1 browser routes have generated strict-JSON exception schemas (reusing WP03.02's JsonSerializerContext posture); independent fixtures cover the identity journeys table in contracts07 §1 (account creation, email/passkey/OIDC login, recovery, step-up, refresh, logout, PAT).

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-07` and ledger record `ledger/tasks/con-07.md` in the Plan repository; task branch `task/con-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — IdentityService (29 ops)/WorkspaceService (4)/DeviceService (6) from registry04 §5, plus contracts07 §1 native PKCE token endpoint and the four /session/v1 browser routes as declared JSON exceptions |
| Provides | identity-session-device-ops; native-browser-auth-exceptions |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.04](android.md#task-and-04), [CLOUD.20](cloud.md#task-cloud-20), [CON.19](#task-con-19), [WEB.10](web.md#task-web-10) |
| Write scope | `Contracts:public/proto/arcforges/publicapi/v1/identity.proto`<br>`Contracts:public/http/v1/schema.json`<br>`Contracts:fixtures/public/con-07-identity.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline positive/negative vectors per contracts07 §1 table (used/expired proof never replays, bad proof same bounded denial shape, wrong PKCE verifier never consumes valid code, etc.); no live provider, no real email/passkey ceremony ([WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) owns that). |
| Completion evidence | fixtures/public/con-07-identity.json; C#/TS/Kotlin conformance report. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No IdentityService/WorkspaceService/DeviceService and none of their ~39 operations exist (confirmed via service grep). |
| Notes | Largest single domain in the public registry by operation count. [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) (Identity/Workspace/Device, owned by the Cloud lane) is the direct downstream consumer and is the one WP explicitly still gated behind the OLD 'whole WP03' edge in implementation-sequence.md §9 (22 depends on 11,21; 21 depends on 03,05,12) — this task is what actually unblocks [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22)'s real work, not [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) as a monolith. |

<a id="task-con-08"></a>

### CON.08 — Entitlement/commerce operation registry

**Outcome.** EntitlementService/CommerceService generated with all listed operations and exact fields; every operation is tagged compatibility-class=frozen per [CC-04](../../../architecture/04-desktop-application-architecture.md#rule-cc-04); independent fixtures cover the closed condition set's entitlement.*/commerce.* error rows.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-08` and ledger record `ledger/tasks/con-08.md` in the Plan repository; task branch `task/con-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — EntitlementService (6 ops) + CommerceService (~14 ops) from registry04 §5, all declared 'frozen' compatibility class per catalogue00 [CC-04](../../../architecture/04-desktop-application-architecture.md#rule-cc-04) |
| Provides | entitlement-commerce-ops |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [WEB.14](web.md#task-web-14) |
| Write scope | `Contracts:public/proto/arcforges/publicapi/v1/commerce.proto`<br>`Contracts:fixtures/public/con-08-entitlement-commerce.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline positive/negative vectors; frozen-class compatibility baseline entries so any future field addition here fails the diff gate without an explicit new version (this is deliberate — financial operations must never silently gain an additive field). |
| Completion evidence | fixtures/public/con-08-entitlement-commerce.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No EntitlementService/CommerceService exist. |
| Notes | Independent of every other CON.0x domain task. Needed to start by [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) (commerce/entitlement/credits, the commerce, policy and operations lanes). |

<a id="task-con-09"></a>

### CON.09 — Sync/resource-transfer/objects operation registry + realm-transfer.v1

**Outcome.** SyncService/ResourceService/TransferService generated with all listed operations; SyncService.pushChange/pushBatch enforce CON.03's mutation allowlist at the schema-validator boundary; realm-transfer.v1's included/excluded-roots manifest and chunked-batch (<=100 roots) semantics are schema-encoded per contracts07 §5.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-09` and ledger record `ledger/tasks/con-09.md` in the Plan repository; task branch `task/con-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — SyncService (~10 ops incl. listScopes/pullChanges/pushChange/pushBatch/getAggregate/listConflicts/resolveConflict/requestFullResync/getBootstrapPage), ResourceService transfer ops (beginUpload/completeUpload/getDownloadTicket/getMetadata/release/getUploadStatus/renewUploadTicket), TransferService (realm-transfer.v1: requestExport/previewImport/commitImport/get/list/cancel) from registry04 §5 and contracts07 §5 |
| Provides | sync-resource-transfer-ops; realm-transfer-v1 |
| Start prerequisites | **contract** [CON.03](#task-con-03) — the closed Sync mutation allowlist validator. *Why:* SyncService.pushChange/pushBatch cannot be schema-complete without the admission rule that rejects non-allowlisted AggregateBody variants — generating the RPC methods without it would let a consumer invent Sync semantics, which [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03)'s own completion gate explicitly forbids. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.37](cloud.md#task-cloud-37), [CON.19](#task-con-19), [SLATE.37](arcslate.md#task-slate-37) |
| Write scope | `Contracts:public/proto/arcforges/publicapi/v1/sync.proto`<br>`Contracts:public/proto/arcforges/publicapi/v1/transfer.proto`<br>`Contracts:fixtures/public/con-09-sync-transfer.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline positive/negative vectors incl. stale revision -> preserved conflict proposal, absent-hash-never-promotes, expired-pin-blocks-adoption; no real D1/R2 ([WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21)/[WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) own that). |
| Completion evidence | fixtures/public/con-09-sync-transfer.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No SyncService/ResourceService/TransferService exist; SyncScope/SyncChange/ChangeProposal/ChangeReceipt/AggregateView/ConflictView/ConflictResolution/BootstrapManifest records (registry04 §4) are also absent. |
| Notes | [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) (Cloud D1/sync engine, the Cloud lane) is the direct consumer that most needs this + CON.03 to start; it does NOT need CON.07/08/10-16. |

<a id="task-con-10"></a>

### CON.10 — Task/approval/bridge/chat/agent/automation/search operation registry + ai-internal package

**Outcome.** All listed public services generated with exact fields and eight authorization fields; @arcforges/ai-internal and CloudInternal gain the ~15 internal/ai/v1 HTTP port schemas (authorize/claim/renew/reconcile/context/model-intent/model-outcome/settle/prepare-tools/cloud-tool/wait/finalize/stream-state/late-outcome + the inference-job family) from contracts05 §3/§8 as closed JSON records with CommitReceipt-style semantics.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-10` and ledger record `ledger/tasks/con-10.md` in the Plan repository; task branch `task/con-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — TaskService(~9)/ApprovalService(2)/BridgeService(3)/public ChatOperationsService(~25)/AgentService(3)/AutomationService(9)/search.query from registry04 §5, plus internal/ai-http/v1 schema.json (ai-internal npm/CloudInternal package) for the C#<->AI-Worker internal HTTP ports in contracts05 §3<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (source KnowledgePolicy/Patch/View, typed one-use overrides, Notes run/atom/table-cell positions, complete initial owner/profile records) — package-level obligation contribution |
| Provides | task-chat-agent-automation-ops; ai-internal-package |
| Start prerequisites | **contract** [CON.02](#task-con-02) — CapabilityDescriptor. *Why:* registry04 tail section 'Initial capability binding' requires one CapabilityDescriptor per tool-eligible method on I*Operations plus each declared Cloud tool — this task's ToolRequest/ToolProposal wiring needs that shape to exist. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.00](ai-routing.md#task-air-00), [AST.11](assistant.md#task-ast-11), [AST.14](assistant.md#task-ast-14), [CON.11](#task-con-11), [CON.19](#task-con-19), [DEV.02](device-bridge.md#task-dev-02), [DEV.04](device-bridge.md#task-dev-04), [HAR.00](harness.md#task-har-00), [HAR.02](harness.md#task-har-02), [SRCH.00](search.md#task-srch-00), [SRCH.01](search.md#task-srch-01) |
| Write scope | `Contracts:public/proto/arcforges/publicapi/v1/chat.proto`<br>`Contracts:internal/ai-http/v1/schema.json`<br>`Contracts:fixtures/public/con-10-chat-task-agent.json`<br>`Contracts:fixtures/internal/con-10-ai-internal.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline positive/negative vectors for ChatTurn/AgentTask journeys per contracts07 §2 table; ai-internal codecs reuse WP03.02's strict-JSON posture; no live CF Worker ([WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) owns that). |
| Completion evidence | fixtures/public/con-10-chat-task-agent.json + fixtures/internal/con-10-ai-internal.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No TaskService/ApprovalService/BridgeService/ChatOperationsService(public)/AgentService/AutomationService exist. internal/ai-http/v1/schema.json currently contains only CommitReceipt. |
| Notes | Second-largest domain task. [WP-15](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15)/16/17 (ArcChat core/execution/independent-core, the assistant lanes) are the direct consumers; [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) (Cloud Harness, the AI lanes) needs both this and CON.11. |

<a id="task-con-11"></a>

### CON.11 — Application/history/execution/events operations (annex10's 13 additions) + EventService

**Outcome.** ApplicationService/HistoryService/ExecutionService/EventService generated with all 13+1 operations, RequestMeta.applicationScope(8)/historyMode(11) and ToolRequest.targetApplication(16) appended without renumbering existing fields; the 17 EventService.Poll hint payloads (sync.changed through config.revisionActivated) generated from one event registry; binary server-streaming frames validated at 32KiB/frame; reserved future Hub/DeviceSso methods verified absent from active registration.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-11` and ledger record `ledger/tasks/con-11.md` in the Plan repository; task branch `task/con-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — the annex10 13 new operations (ApplicationService.List/Heartbeat/Disconnect, HistoryService.BeginImport/FinalizeImport/GetImport/CancelImport, ExecutionService.StartTransientTurn/ReadOutput/WatchOutput/AcknowledgeOutput/PurgeTransient, EventService.Watch) plus EventService.Poll's 17 hint payloads ([CA-12](../../../architecture/02-contracts-and-protocols.md#rule-ca-12)) and StreamFrame/OutputChunk/StreamPosition/StreamReset server-streaming framing<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) Current application and stream contract completeness (annex10+manifest11, explicitly required before 03 completion) — 'Current application and stream contract completeness' package-level obligation — explicitly required before 03 completion, not a.90-deferred item |
| Provides | application-history-execution-events-ops |
| Start prerequisites | **contract** [CON.10](#task-con-10) — TaskSnapshot/ChatTurnProgress shapes for ExecutionProgress's oneof. *Why:* ExecutionProgress.task/turn oneof needs the real TaskSnapshot (already published, WP03.01) and ChatTurnProgress (new in CON.10); ExecutionOwner conceptually unifies Task and ChatTurn ownership so this task is easiest to review once CON.10's ChatTurn shapes exist. Not a hard compiler block since TaskSnapshot alone already exists — treat as a strong sequencing preference, not an absolute gate. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.04](android.md#task-and-04), [AND.05](android.md#task-and-05), [AST.01](assistant.md#task-ast-01), [AST.07](assistant.md#task-ast-07), [CLOUD.29](cloud.md#task-cloud-29), [CON.15](#task-con-15), [CON.19](#task-con-19), [DEV.01](device-bridge.md#task-dev-01), [HAR.01](harness.md#task-har-01) |
| Write scope | `Contracts:public/proto/arcforges/publicapi/v1/application.proto`<br>`Contracts:public/proto/arcforges/events/v1/events.proto`<br>`Contracts:fixtures/public/con-11-application-streams.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: binary unary/stream frame fixtures, scope/presence/unknown-field vectors, contract fixtures with mismatched resource owner/forged target/stale epoch per annex10 §6; no live gRPC-Web transport ([WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)/23/24/30 own that). |
| Completion evidence | fixtures/public/con-11-application-streams.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: ApplicationScope(record)/HistoryMode(enum) already exist as Foundation types (WP03.01 seed, since annex10 defines ApplicationScope and it was pulled into Foundation early). ApplicationTarget/ApplicationPresence/TransientTurnRequest/StreamPosition/StreamFrame/OutputChunk/StreamReset/ExecutionOutput/ExecutionProgress/ChatTurnProgress and all 4 new services are absent. events.proto has only EntitlementChanged. |
| Notes | Directly required by [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) (realtime/reliable events) and [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) (device bridge), both the Cloud lane; also the substep the WP03 text is most emphatic about ('required before 03 completion, not a.90 design task'). |

<a id="task-con-12"></a>

### CON.12 — Extension and policy schemas: manifest.v1/workflow.v1/panel.v1/policy body.v1/configuration.v1

**Outcome.** The five contracts08 schema families are authored as closed JSON schemas (manifest.v1/workflow.v1/panel.v1 under public/http or a dedicated extensions schema path; policy body.v1 and configuration.v1 under public/http and internal/ai-http respectively) with generated C#/TS validators; independent vectors cover malformed archive, permission expansion, revoke-during-work, private-schema-rollback-refusal and the deterministic bucket-assignment hash vectors from contracts08 §5.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-12` and ledger record `ledger/tasks/con-12.md` in the Plan repository; task branch `task/con-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — extension/policy schemas named in [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) §4's projects table ('Selected CF/auth/provider HTTP exceptions') and contracts08 in full:.arcpkg manifest.v1, workflow.v1 DAG, panel.v1 declarative UI, PolicyBundle body.v1, internal ConfigurationDocument (20 sections) |
| Provides | extension-policy-schemas |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [POL.02](policy.md#task-pol-02), [POL.09](policy.md#task-pol-09) |
| Write scope | `Contracts:public/http/v1/schema.json`<br>`Contracts:internal/ai-http/v1/schema.json`<br>`Contracts:fixtures/public/con-12-extension-policy.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline vectors per contracts08 (allocation-0/10000 boundary bucket tests, lower-value-dominates capacity limit test, invalid commercial credential blocks activation); no live broker/OS profile ([WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09)/[WP-11](../../work-packages/11-security-foundation.md#rule-wp-11)/[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41)/[WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) own that). |
| Completion evidence | fixtures/public/con-12-extension-policy.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: None of manifest.v1/workflow.v1/panel.v1/policy-body.v1/configuration.v1 exist in the repo in any form. |
| Notes | Needed to start by [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) (extensions) and [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) (policy/configuration), both currently blocked on the whole-WP03 edge in the old serial graph. |

<a id="task-con-13"></a>

### CON.13 — Package catalog operation registry (CatalogService)

**Outcome.** arcforges.catalog.v1 generated with the 7 public CatalogService operations and their records; DNS TXT publisher-verification challenge format and the PAT-eligible subset (catalog.search/getPackage/listVersions/submitVersion/getSubmission per catalogue00's PAT allowlist) are schema-encoded.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-13` and ledger record `ledger/tasks/con-13.md` in the Plan repository; task branch `task/con-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / S |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — the public CatalogService (search/getPackage/listVersions/registerPublisher/verifyPublisher/submitVersion/getSubmission, 7 ops) and PublisherView/CatalogPackageView/CatalogVersionView/CatalogSubmissionView/CatalogReviewDecision records from registry04 §4/§5 |
| Provides | package-catalog-ops |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.14](#task-con-14), [CON.19](#task-con-19) |
| Write scope | `Contracts:public/proto/arcforges/catalog/v1/catalog.proto`<br>`Contracts:fixtures/public/con-13-package-catalog.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline vectors for the catalogue00 PAT-allowlist assertion and submission-integrity checks (matching ID/version/digest/license). |
| Completion evidence | fixtures/public/con-13-package-catalog.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No CatalogService or catalog records exist. |
| Notes | Small and self-contained. |

<a id="task-con-14"></a>

### CON.14 — Operator control service (OperatorService, full §9/9.1/9.2 protocol)

**Outcome.** internal/proto/arcforges/operator/v1/operator.proto generated with all 29 OperatorService methods (ListCases through catalog.review/catalog.revoke), OperatorCallContext(tag100)/OperatorProposalRef(tag101) appended per method, and the typed propose/approve/execute protocol (§9.2) with its 9 mutation-variant table rows (grant/revokeGrant/issueCredit/adjustCredit/refund/catalogReview/catalogRevoke/appeal/kill); independent negative vectors cover distinct-approver violation, stale hash/revision/configuration, role revocation, expiry, concurrent consumption and lost receipt; no direct SQL or public-SDK import of operator schema.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-14` and ledger record `ledger/tasks/con-14.md` in the Plan repository; task branch `task/con-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — OperatorService's ~29 methods with all eight authorization fields and the [OC-03](../../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role matrix<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) 'Operator contract closure' package-level obligation — schema and negative vectors only; [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) owns real identity/dispatch, [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) financial owners, [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) config/policy owners, [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) the console join — 'Operator contract closure' package-level obligation — schema and negative vectors only; [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) owns real identity/dispatch, [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) financial owners, [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) config/policy owners, [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) the console join; package-level obligation contribution |
| Provides | operator-service-ops |
| Start prerequisites | **contract** [CON.13](#task-con-13) — CatalogSubmissionView/CatalogVersionView. *Why:* operator.catalog.review and catalog.revoke request/result fields reference these exact record types; they must exist first. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.13](commerce.md#task-com-13), [CON.19](#task-con-19), [OPS.05](operations.md#task-ops-05), [OPS.11](operations.md#task-ops-11), [OPS.13](operations.md#task-ops-13), [POL.05](policy.md#task-pol-05) |
| Write scope | `Contracts:internal/proto/arcforges/operator/v1/operator.proto`<br>`Contracts:src/internal/dotnet/ArcForges.Contracts.CloudInternal/**`<br>`Contracts:src/internal/ts/operator-client/src/**`<br>`Contracts:fixtures/internal/con-14-operator.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline negative vectors per registry04 §9.1/§9.2 (public customer/PAT/agent access refuses; distinct approver enforced; stale hash/revision fails); no live Entra OIDC session ([WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)/[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) own that). |
| Completion evidence | fixtures/internal/con-14-operator.json. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Only OperatorCallContext (the 3-field context record) exists from the WP03.00 seed. None of the 29 OperatorService methods, roles or the propose/approve/execute protocol exist. |
| Notes | @arcforges/operator-client package already exists as an empty-ish scaffold (WP03.00); this task is what actually fills it. [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) (operations console, the commerce, policy and operations lanes) is the direct consumer. |

<a id="task-con-15"></a>

### CON.15 — Cloudflare-internal HTTP bindings (AI Worker <-> C# ports beyond ai-internal's chat/task family)

**Outcome.** The remaining ~15 contracts05 internal HTTP ports and their records are generated as closed JSON schemas in internal/ai-http/v1/schema.json (or a dedicated internal/cf-http/v1 if the CON.10 file is already large), reusing WP03.02's strict-JSON posture; independent vectors cover duplicate dispatch, lease takeover, R2 part mismatch and stale-epoch rejection per contracts05 §7's injection list (schema-level only — no live Worker).

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-15` and ledger record `ledger/tasks/con-15.md` in the Plan repository; task branch `task/con-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.90](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) — 'Private CF binding/event definitions' input — the remaining contracts05 ports not already covered by CON.10 (ai-internal): /internal/objects/v1/* (authorize/part-receipt/verification/job-grant/job-authorize), /internal/ai/v1/dispatch/control/delete (Worker-side), inference-job family (embedding/rerank), and CfDeletionTarget/CfDeletionReceipt/SessionBinding/BackupManifest records |
| Provides | cf-internal-bindings |
| Start prerequisites | **contract** [CON.11](#task-con-11) — ExecutionOwner/StreamPosition shapes. *Why:* several CF internal ports (claim/reconcile/finalize/stream-state) carry run identity and stream state that mirror annex10's ExecutionOwner/StreamPosition; authoring them before CON.11 exists would risk a duplicate, incompatible shape. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [EXT.10](extensions.md#task-ext-10), [HAR.00](harness.md#task-har-00) |
| Write scope | `Contracts:internal/ai-http/v1/schema.json`<br>`Contracts:fixtures/internal/con-15-cf-internal.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline vectors only; explicitly NOT a live-Worker/D1/R2 test (that is [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) minimal probe and [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) real Harness per the producer matrix's WP03 row: 'Owner handlers are deliberately absent; codec/validator fixtures prove schema only'). |
| Completion evidence | fixtures/internal/con-15-cf-internal.json. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: None of contracts05's ~25 internal HTTP ports exist beyond CommitReceipt (WP03.00 seed, shared with CON.10). |
| Notes | Consumed by [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) (D1 execution lease), [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) (R2/object lifecycle), [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) (Harness) — all the Cloud lane/the AI lanes. This is schema-only; the actual Worker deployment is explicitly out of WP03 scope (WP03 §1 'Out of scope:... The cloud endpoint implementations (23)'). |

<a id="task-con-16"></a>

### CON.16 — Signed catalog/update/realm formats (catalog-index.v1, catalog-revocations.v1, android-update.v1, realm.v1)

**Outcome.** The four signed-format schemas are authored under public/http (or a dedicated signed-formats path) with canonical signing-vector fixtures and a deterministic fixture-only trust root (Ed25519, distinct from any production key); malformed/expired/rollback/mixed-shard negative vectors exist per [WP-03.07](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.07)'s gate; android-update.v1 matches registry04's tail-section field list exactly (packageId/channel/versionName/versionCode-as-string/minSdk/minSupportedVersionCode/apkUrl/sha256/size/signingCertificateSha256/releaseNotesUrl/publishedAt, expiry<=7 days).

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-16` and ledger record `ledger/tasks/con-16.md` in the Plan repository; task branch `task/con-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.07](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.07) — full — publish catalog-index.v1, catalog-revocations.v1, android-update.v1 and realm.v1 schemas, canonical signing vectors and separate fixture trust roots; production keys are explicitly [WP-53](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) output, not a [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) input |
| Provides | signed-catalog-update-realm-formats |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.20](android.md#task-and-20), [CON.19](#task-con-19), [EXT.04](extensions.md#task-ext-04), [EXT.06](extensions.md#task-ext-06), [UPD.07](updater.md#task-upd-07) |
| Permitted substitutes | [SUB-signed-format-fixture-keys](../substitutes.md#sub-signed-format-fixture-keys) |
| Write scope | `Contracts:public/http/v1/signed-formats.schema.json`<br>`Contracts:fixtures/public/con-16-signed-formats.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline signature/hash verification vectors; no real key custody, no live distribution ([WP-32](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32)/[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41)/[WP-53](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) own those). |
| Completion evidence | fixtures/public/con-16-signed-formats.json with named trust-root fixture and its provenance note ('fixture only, never production'). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: None of the four schemas exist yet. |
| Notes | Fully independent of every other CON.0x task (self-contained format definitions). Gate explicitly states 'WP32/WP41 can implement complete consumers with deterministic fixture keys and named later production replacement' — this is the textbook named-scaffolding pattern from implementation-sequence.md §3.1. |

<a id="task-con-17"></a>

### CON.17 — Cross-language compatibility window + canonical semantic hash

**Outcome.** A canonical-semantic-hash implementation (per registry04 §2's exact algorithm: sorted ASCII property names, canonical integer/decimal strings, NFC where required) exists in C#/TS with shared golden vectors; a compatibility-matrix test harness runs previous-published-client-assembly against current server and current client against a pinned minimum-server descriptor set, both directions; deliberate deletion/tag-reuse/type-change mutations are injected and must fail the baseline-diff gate before publication.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-17` and ledger record `ledger/tasks/con-17.md` in the Plan repository; task branch `task/con-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M · early risk proof |
| Obligations | [WP-03.06](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.06) — full — wire bigint/decimal-coefficient-scale/oneof-presence/unknown-field/additive-response-evolution profile; canonical semantic hash distinct from wire byte hash; independent versioning of descriptors from applications; supported-window enforcement (previous-client/current-server and current-client/minimum-server matrices); deletion/tag-reuse/type-change failure tests |
| Provides | compat-window-semantic-hash |
| Start prerequisites | **contract** [CON.92](#task-con-92) — already-published Foundation/PublicApi as the 'previous stable' fixture. *Why:* the compatibility matrix needs an actual previously-published package version to compare against; the WP03.01/03.02 published releases (1.0.0-ci.89.1 / 1.0.0-ci.92.1) already serve as that baseline, so this can start immediately. |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CON.18](#task-con-18) — full coverage of the compatibility matrix against every later-added service (CON.07-CON.16). *Why:* the harness and hash algorithm can be built and unit-tested now, but [WP-03.06](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.06)'s own completion gate ('all selected values retain meaning across clients') is only fully evidenced once the domain tasks it must protect actually exist — this is an integration-style completion dependency, not a start blocker. |
| Unblocks | [CON.19](#task-con-19) |
| Write scope | `Contracts:eng/check_compatibility.py`<br>`Contracts:tests/tooling/test_compatibility_matrix.py`<br>`Contracts:fixtures/public/con-17-compat-hash.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: golden semantic-hash vectors (order-independent, explicit-null-sensitive per registry04 §2's exact examples); deliberate-break injection tests; no live multi-version deployment (that is [WP-23.06](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.06)'s real bidirectional test). |
| Completion evidence | fixtures/public/con-17-compat-hash.json; compatibility-matrix CI job report. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No semantic-hash implementation or compatibility-matrix harness exists yet; only the basic descriptor-diff regeneration check from WP03.00/01/02 exists (a much narrower 'did anything change' check, not the full previous/current-client x current/minimum-server matrix). |
| Notes | Marked early_risk_proof=true: getting the canonical semantic hash algorithm right (vs. wire byte hash) early is exactly the kind of narrow risk proof that should stay early, because every later domain task's fixtures implicitly depend on hash determinism, and a late discovery of a hash-algorithm bug would invalidate many already-published fixture files. |

<a id="task-con-18"></a>

### CON.18 — Operation-scope manifest + authorization-reachability matrix generator

**Outcome.** A generator/policy-test tool reads manifest11's ~380-row scope-class table as its oracle, cross-references every currently-registered service method's exported eight authorization fields (capability/risk/approval/stepUp/localPresence/egress/patEligible/actorKinds), and fails the build on any unclassified, ambiguous, or nonexistent-idempotency-example method, or any tool reachability of a human-only approval/credential/commerce/policy method.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-18` and ledger record `ledger/tasks/con-18.md` in the Plan repository; task branch `task/con-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / S |
| Obligations | [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) §7 evidence: operation-by-actor reachability matrix ([AZ-04](../../../architecture/08-security-architecture.md#rule-az-04)) for public/local/operator/CF/exception bindings — §7 evidence requirement: 'Generate an operation-by-actor reachability matrix for every public/local/operator/CF/exception binding under catalogue 00 [AZ-04](../../../architecture/08-security-architecture.md#rule-az-04), with all seven effective authorization fields and source profile. Fail unclassified/ambiguous fields...'; package-level obligation contribution |
| Provides | operation-scope-manifest-tooling |
| Start prerequisites | none |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.17](#task-con-17), [CON.19](#task-con-19), [GOV.16](governance.md#task-gov-16) |
| Write scope | `Contracts:eng/check_operation_scope.py`<br>`Contracts:eng/operation-scope-manifest.json` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline: the tool itself is tested against the current (mostly 'pending') state and against synthetic unclassified/ambiguous fixtures that must fail. |
| Completion evidence | eng/operation-scope-manifest.json plus its policy-test pass/fail report. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No such generator or manifest file exists; manifest11 is a Design document only, not yet mirrored into Contracts tooling. |
| Notes | Small and foundational — should land early so every CON.07-CON.16 domain task can self-check against it as it lands, rather than everything being checked only at the very end (CON.19). |

<a id="task-con-19"></a>

### CON.19 — WP03.90 — verify the owned Contracts artifact and its real (non-consumer) integration

**Outcome.** Deterministic generation, compatibility/reserved-field checks (CON.17's harness), Apache closure, and independent precise-value/error/profile vectors all pass across the complete CON.02-CON.18 closure; all three generated client ecosystems (NuGet, npm, Maven/Kotlin) restore the actual published candidate artifacts in isolated consumer tests; the [WP-03.90](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) completion receipt records exact artifact identities and real-vs-fixture status per obligation.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-19` and ledger record `ledger/tasks/con-19.md` in the Plan repository; task branch `task/con-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Package acceptance | Records the [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-03.90](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) — all work except the parts mapped to CON.15<br>[WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) §8 completion gate (6 items) + [P2-009](../../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[VG-04](../../../assurance/open-gates-register.md#rule-vg-04)/[F-026](../../../assurance/open-gates-register.md#rule-f-026) scoped gate contributions — §8 completion gate items 1-6 and the [P2-009](../../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[VG-04](../../../assurance/open-gates-register.md#rule-vg-04)/[F-026](../../../assurance/open-gates-register.md#rule-f-026) gate contributions; package-level obligation contribution |
| Provides | wp03-complete-closure |
| Start prerequisites | **contract** [CON.02](#task-con-02) — all CON.02-CON.18 tasks complete and published. *Why:* this is the aggregate closure gate; it cannot assert 'deterministic generation across the complete closure' until the closure is complete. (Listing CON.02 as representative; the real dependency is the full set CON.02-CON.18.)<br>**contract** [CON.18](#task-con-18) — full operation-scope manifest with zero pending rows. *Why:* §7's [OV-01](../../../architecture/23-simulator-and-interchange.md#rule-ov-01) requires every operation classified; this can't pass until every domain task has flipped its rows.<br>**artifact** [CON.03](#task-con-03) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.04](#task-con-04) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.05](#task-con-05) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.06](#task-con-06) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.07](#task-con-07) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.08](#task-con-08) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.09](#task-con-09) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.10](#task-con-10) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.11](#task-con-11) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.12](#task-con-12) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.13](#task-con-13) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.14](#task-con-14) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.15](#task-con-15) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.16](#task-con-16) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.17](#task-con-17) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.20](#task-con-20) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.21](#task-con-21) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.22](#task-con-22) — closure published. *Why:* the owned-artifact receipt verifies the complete generated package set; it never gates consumers of an individual closure<br>**artifact** [CON.01](#task-con-01) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `Contracts:docs/wp03-90-verification.md`<br>`Contracts:artifacts/contracts/**` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | the full P2-017-scoped suite: deterministic regen, all isolated NuGet/npm/Maven consumer restore-and-compile tests, descriptor baseline diff clean, Apache boundary clean; explicitly NOT live-service/device/macOS per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) — 'no missing owner decision deferred to consumer coding' per the producer matrix's WP03 acceptance row. |
| Completion evidence | [WP-03.90](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.90) completion receipt: source commit, producer release, candidate hashes, actual runtime/OS/provider identity tested, scenario, result, limitations, real-versus-fixture status per obligation (matching the format of the WP03.00/01/02 receipts already on file). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cannot start meaningfully until the domain tasks exist; this entry exists now so the integration owner can see the terminal aggregation point and its exact evidence shape (modeled on the three existing wp03-0X-implementation-evidence.md receipts, which are unusually precise: exact PR numbers, merge SHAs, CI run URLs, publication versions). |
| Notes | This is WP03's own closure, NOT waiting for [WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04)/05/06/09/21/23/30 to build real consumers — per producer-artifacts-and-integration.md's WP03 row, WP03's own acceptance is schema/fixture/candidate-restore evidence only ('Owner handlers are deliberately absent'). Real cross-repo integration is separate IM.* proposals below. |

<a id="task-con-20"></a>

### CON.20 — Notes public operation registry

**Outcome.** NotesService is generated with all notes.* operations (notebooks, folders, documents, revisions, checkpoints, restore and requestExport), exact fields, authorization profiles and independent vectors in C#, TypeScript and Kotlin.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-20` and ledger record `ledger/tasks/con-20.md` in the Plan repository; task branch `task/con-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — notes.* operations (17), their records, eight authorization fields and vectors |
| Provides | Notes public operation registry |
| Start prerequisites | **contract** [CON.02](#task-con-02) — capability/action/context/resource descriptor and oversized-body reference records. *Why:* these operations carry resource references, descriptors and immutable body references defined by the shared descriptor closure |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.37](cloud.md#task-cloud-37), [CLOUD.45](cloud.md#task-cloud-45), [CON.19](#task-con-19), [NOTES.20](arcnotes.md#task-notes-20) |
| Write scope | `Contracts:public/proto/arcforges/*/v1/**`<br>`Contracts:fixtures/public/con-{i}-*.json`<br>`Contracts:src/public/**/Generated/**` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Deterministic regeneration, descriptor/tag/compatibility checks, closed-schema validators, independent positive and negative vectors in C#, TypeScript and Kotlin; Windows/Linux compilation and packaging only ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Merged pull request, published Contracts candidate identity containing the closure, vector and compatibility results, and the operation-scope manifest rows flipped to verified for these operations. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Added so that every operation family in the operation-scope manifest has a closure task. |

<a id="task-con-21"></a>

### CON.21 — Simulation operation registry

**Outcome.** SimulationService is generated with all simulation.* operations (definitions, scenario versions, run control, segments, segment tickets and state polling), exact fields and vectors in C#, TypeScript and Kotlin.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-21` and ledger record `ledger/tasks/con-21.md` in the Plan repository; task branch `task/con-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — simulation.* operations (12), their records, authorization fields and vectors |
| Provides | Simulation operation registry |
| Start prerequisites | **contract** [CON.02](#task-con-02) — capability/action/context/resource descriptor and oversized-body reference records. *Why:* these operations carry resource references, descriptors and immutable body references defined by the shared descriptor closure |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.19](#task-con-19), [SIM.01](simulator.md#task-sim-01), [SIM.05](simulator.md#task-sim-05), [SIM.06](simulator.md#task-sim-06) |
| Write scope | `Contracts:public/proto/arcforges/*/v1/**`<br>`Contracts:fixtures/public/con-{i}-*.json`<br>`Contracts:src/public/**/Generated/**` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Deterministic regeneration, descriptor/tag/compatibility checks, closed-schema validators, independent positive and negative vectors in C#, TypeScript and Kotlin; Windows/Linux compilation and packaging only ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Merged pull request, published Contracts candidate identity containing the closure, vector and compatibility results, and the operation-scope manifest rows flipped to verified for these operations. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Added so that every operation family in the operation-scope manifest has a closure task. |

<a id="task-con-22"></a>

### CON.22 — Account support, notification, data, preference, policy-bundle and export-job operations

**Outcome.** Support case, notification and push registration, data export request/state, preference, policy bundle and export-job status/cancel/download operations are generated with exact fields, authorization profiles and vectors in C#, TypeScript and Kotlin.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-22` and ledger record `ledger/tasks/con-22.md` in the Plan repository; task branch `task/con-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.05](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05) — support.*, notification.*, data.*, preference.*, policy.getBundle and export.* operations (15), records and vectors |
| Provides | Account support, notification, data, preference, policy-bundle and export-job operations |
| Start prerequisites | **contract** [CON.02](#task-con-02) — capability/action/context/resource descriptor and oversized-body reference records. *Why:* these operations carry resource references, descriptors and immutable body references defined by the shared descriptor closure |
| Entry condition | [ADOPT.03.contracts](adoption.md#task-adopt-03-contracts) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.12](android.md#task-and-12), [CLOUD.45](cloud.md#task-cloud-45), [CON.19](#task-con-19), [OPS.07](operations.md#task-ops-07), [OPS.10](operations.md#task-ops-10), [POL.09](policy.md#task-pol-09), [WEB.15](web.md#task-web-15) |
| Write scope | `Contracts:public/proto/arcforges/*/v1/**`<br>`Contracts:fixtures/public/con-{i}-*.json`<br>`Contracts:src/public/**/Generated/**` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Deterministic regeneration, descriptor/tag/compatibility checks, closed-schema validators, independent positive and negative vectors in C#, TypeScript and Kotlin; Windows/Linux compilation and packaging only ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Merged pull request, published Contracts candidate identity containing the closure, vector and compatibility results, and the operation-scope manifest rows flipped to verified for these operations. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Added so that every operation family in the operation-scope manifest has a closure task. |

<a id="task-con-90"></a>

### CON.90 — WP03.00 — split project structure (accepted, historical)

**Outcome.** 22 package identities (14 NuGet/5 npm/3 Maven) exist as real source-bearing projects with generators wired; native-grpc-only contracts-client retired from new publication.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-90` and ledger record `ledger/tasks/con-90.md` in the Plan repository; task branch `task/con-90` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M |
| Obligations | [WP-03.00](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.00) — full |
| Provides | contracts-project-split |
| Start prerequisites | none |
| Completion prerequisites | none |
| Unblocks | [GOV.05](governance.md#task-gov-05), [PRF.10](runtime-proofs.md#task-prf-10) |
| Write scope | `Contracts:eng/contract-packages.json`<br>`Contracts:src/**`<br>`Contracts:public/**`<br>`Contracts:internal/**` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | accepted; see docs/assurance/wp03-00-implementation-evidence.md |
| Completion evidence | Contracts PR33/34/35 merged; accepted source 30ddcad2bcb3634e089abb5e29d6c9ce05d38386; published 1.0.0-ci.86.1 |
| Baseline (unreviewed unless accepted) | accepted — Design receipts wp03-00-implementation-evidence.md/.json; the Contracts pull requests recorded there are merged. |
| Notes | Historical record only, not new work. |

<a id="task-con-91"></a>

### CON.91 — WP03.01 — foundation contract types (accepted, historical)

**Outcome.** 148 records (32 Foundation incl. ResourceRef/ResourceVersionRef/BlobRef/ArtifactRef/ContentOrigin, 116 PublicApi incl. all 16 AggregateBody branches) generated with safe value wrappers; 476 C#/TS conformance cases pass.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-91` and ledger record `ledger/tasks/con-91.md` in the Plan repository; task branch `task/con-91` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / L |
| Obligations | [WP-03.01](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.01) — full |
| Provides | foundation-types; resource-ref-types; aggregate-body-closure |
| Start prerequisites | none |
| Completion prerequisites | none |
| Unblocks | [AST.01](assistant.md#task-ast-01), [CLOUD.01](cloud.md#task-cloud-01), [CLOUD.21](cloud.md#task-cloud-21), [CLOUD.23](cloud.md#task-cloud-23), [CLOUD.37](cloud.md#task-cloud-37), [CON.02](#task-con-02), [FND.01](foundation.md#task-fnd-01), [FND.02](foundation.md#task-fnd-02), [FND.03](foundation.md#task-fnd-03), [FND.05](foundation.md#task-fnd-05), [FND.07](foundation.md#task-fnd-07), [NOTES.01](arcnotes.md#task-notes-01), [NOTES.02](arcnotes.md#task-notes-02), [NOTES.07](arcnotes.md#task-notes-07), [NOTES.12](arcnotes.md#task-notes-12), [NOTES.18](arcnotes.md#task-notes-18), [NOTES.20](arcnotes.md#task-notes-20), [NOTES.23](arcnotes.md#task-notes-23), [NOTES.24](arcnotes.md#task-notes-24), [PLT.17](platform.md#task-plt-17), [PLT.19](platform.md#task-plt-19), [PRF.01](runtime-proofs.md#task-prf-01), [PRF.02](runtime-proofs.md#task-prf-02), [PRF.03](runtime-proofs.md#task-prf-03), [SCOPE.01](arcscope.md#task-scope-01), [SCOPE.02](arcscope.md#task-scope-02), [SCOPE.14](arcscope.md#task-scope-14) |
| Write scope | `Contracts:public/proto/arcforges/foundation/v1/**`<br>`Contracts:public/proto/arcforges/publicapi/v1/content.proto` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | accepted; see docs/assurance/wp03-01-implementation-evidence.md |
| Completion evidence | Contracts PR36 merged as 4b8134eaf8a4174922d6378da003ed390b85a94a; published 1.0.0-ci.89.1 |
| Baseline (unreviewed unless accepted) | accepted — Design receipts wp03-01-implementation-evidence.md/.json; the recorded foundation and content records are generated and published. |
| Notes | Historical record. IMPORTANT: this substep's dependency-closure side effect already generated ResourceRef/ResourceVersionRef/BlobRef/ArtifactRef — WP03.03 does not need to invent these, only add capability/action/context/health descriptors, the Sync mutation allowlist validator, and EncodedBodyRef (still absent). |

<a id="task-con-92"></a>

### CON.92 — WP03.02 — serialization posture (accepted, historical)

**Outcome.** Google.Protobuf/protobuf-es are the only business serializers; decode limits (4MiB/256KiB/32KiB/64MiB), strict HTTP-exception JSON codecs, explicit service catalogues, forbidden-serializer policy gate and a test-only Native AOT probe (13 libraries, Linux CI + Windows local) all pass.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/con-92` and ledger record `ledger/tasks/con-92.md` in the Plan repository; task branch `task/con-92` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | contract / M · early risk proof |
| Obligations | [WP-03.02](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02) — full |
| Provides | serialization-posture; decode-limit-constants; aot-probe-harness |
| Start prerequisites | none |
| Completion prerequisites | none |
| Unblocks | [CON.17](#task-con-17), [PRF.05](runtime-proofs.md#task-prf-05), [PRF.07](runtime-proofs.md#task-prf-07), [PRF.08](runtime-proofs.md#task-prf-08) |
| Write scope | `Contracts:eng/check_serialization.py`<br>`Contracts:tests/public/SerializationProbe/**` |
| Shared resources | [RES-contracts-generated-baseline](../shared-resources.md#res-contracts-generated-baseline) (regenerate), [RES-contracts-publication](../shared-resources.md#res-contracts-publication) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | accepted; see docs/assurance/wp03-02-implementation-evidence.md |
| Completion evidence | Contracts PR37 merged as e6c4a77f3ba48d70de4bf524623985b29278c784 (= current HEAD); published 1.0.0-ci.92.1 |
| Baseline (unreviewed unless accepted) | accepted — Design receipts wp03-02-implementation-evidence.md/.json; Contracts main e6c4a77 (pull request 37) is the last merge. [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) has not started. |
| Notes | This is Contracts' current HEAD. Every task below starts from this baseline. Both the Contracts repo's own docs/wp03-02-serialization.md and Design's evidence doc independently state '03.03 is next and has not started' — and no artifact anywhere (git log --all, all.worktree dirs, gh pr list --state all, fixtures/ directory contents, proto message/service inventory) contradicts that.. |
