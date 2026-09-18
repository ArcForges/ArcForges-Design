# In-Process Product Ports and Private Helper Operations

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Contracts
> Governing authority: [`00-operation-catalogue.md`](00-operation-catalogue.md), [`../03-local-ipc-and-process-model.md`](../03-local-ipc-and-process-model.md), **[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)**
> Companions: [`../02-contracts-and-protocols.md`](../02-contracts-and-protocols.md), [`../data-model/02-desktop-data-model.md`](../data-model/02-desktop-data-model.md)

Product ports use generated records and statically registered in-process handlers. Only the closed parent/child services in contracts 09 use native gRPC over Named Pipe/UDS. No product advertises a peer endpoint. All asynchronous operations remain cancellation-aware; cancellation after a dispatched effect reconciles its receipt.

---

## 1. Interface map

| Interface | Hosted by | Consumed by |
|---|---|---|
| `ILocalBootstrap`, `ILocalEvents` | Owned helper/extension channel | Verified launch pair; lease and bounded hints |
| `IConnectorBroker` | Owned connector child | Exact parent on behalf of foreground human; no Device SSO |
| `IContentSandbox` | Restricted helper | Exact launch-bound parent only |
| `ICapabilityProvider` | Every product | owning application composition, for its authorized callers |
| `IContextProvider` | Owning product in process | Its embedded assistant |
| `IArtifactHandler` | Owning product in process | Its embedded assistant |
| `IResourceAccess` | Owning product or admitted helper boundary | Own handler or exact child grant |
| `IProductLifecycle` | Every product | owning application composition |
| `IDeepLinkTarget` | Every product | owning application composition |
| `INotesOperations`, `IScopeOperations`, `ISlateOperations`, `IChatOperations` | The owning product | owning application composition, for its authorized callers |
| `IExtensionHost` | Product process | Extension process *(the protocol of [`../15-extension-platform-architecture.md`](../15-extension-platform-architecture.md), listed here for completeness)* |

---

<a id="rule-rt-02"></a>
## 2. Registration and routing

`IHubRegistry` and `IHubRouting` are reserved historical names, excluded from current generated server registration and runtime. There is no application-to-application discovery or routing. Their future use requires activation of the [cross-product plan](../../future/cross-product-collaboration/README.md).

Current product services below are typed in-process Application ports. The Platform assistant registers only its own application's operations; Cloud's tool bridge dispatches to one authenticated application installation and the owner calls the same handlers. Private parent/helper discovery and bootstrap are separately specified in annex 09.

## 3. Capability invocation

### `ICapabilityProvider`

```
DescribeAsync()                              → ArcResult<CapabilityDescriptor[]>
EvaluateAvailabilityAsync(ActionKey, FrozenContext)
                                             → ArcResult<AvailabilityResult>
InvokeAsync(InvocationRequest)               → ArcResult<InvocationOutcome>
```

`InvocationRequest` is the generated registry 04 `Invocation`: invocationId, commandId, capability, FrozenContext (including ActorChain), typed CapabilityArguments, optional approvalId/leaseId and exactly one declared expected-version field. [LocalCallContext](09-local-grpc-and-sandbox.md#2-discovery-peer-verification-and-bootstrap) carries the same validated actor/evidence references through transport and typed forwarding. It is not a second hand-authored DTO or an unspecified ApprovalToken/LeaseToken wire format.

| # | Rule |
|---|---|
| <a id="rule-ci-01"></a>CI-01 | **`EvaluateAvailabilityAsync` is side-effect free** and cheap enough to run on UI enumeration ([WP-09.03](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03)). |
| <a id="rule-ci-02"></a>CI-02 | InvokeAsync always performs owner-side final validation under WP14.04/WP26.02. An approval reference is resolved by the owner, never authority by possession. |
| <a id="rule-ci-07"></a>CI-07 | **`InvokeAsync` is the boundary, not a product contract.** It decodes into a generated typed request and calls the product's typed operation (`§3.1`). The structured value never travels past the decode step, so [AC-02](../00-architecture-overview.md#rule-ac-02)'s prohibition on a catch-all first-party call holds where it matters — in the product's own contracts. |
| <a id="rule-ci-03"></a>CI-03 | **Context is frozen by the caller and immutable in transit** ([WP-09.04](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.04)). The provider never re-reads live context mid-invocation. |
| <a id="rule-ci-04"></a>CI-04 | **The outcome carries the resulting authority-specific version**, so the caller can chain without re-reading. |
| <a id="rule-ci-05"></a>CI-05 | **Large arguments and results cross by `ResourceRef`**, never inline ([BR-10](../../planning/work-packages/08-local-ipc-and-registration.md#rule-br-10) of [WP-08](../../planning/work-packages/08-local-ipc-and-registration.md#rule-wp-08)). |
| <a id="rule-ci-06"></a>CI-06 | **An invocation is idempotent on `CommandId`** — a retry after a lost response returns the original outcome ([WP-14.03](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03)). |

---

## 3.1 From an untyped request to a typed product operation

[AC-02](../00-architecture-overview.md#rule-ac-02) prohibits a catch-all `Invoke(string, object)`, and [L2-06](../15-extension-platform-architecture.md#rule-l2-06)/[XT-05](../15-extension-platform-architecture.md#rule-xt-05) require that the structured value type never appear in a first-party product contract. `ICapabilityProvider.InvokeAsync` nevertheless takes a `CapabilityKey` and structured `Arguments` — because that is exactly what arrives from a model or an extension, which cannot be compiled against ArcForges' types.

Both are correct. What was missing is the **decode step between them**, and the precise scope of the containment rule.

```
model tool call  /  extension invocation
        |  CapabilityKey + structured Arguments
        v
  +----------------------------------------------------+
  |  BOUNDARY  -- ICapabilityProvider.InvokeAsync       |   structured value permitted HERE
  |    1. resolve CapabilityKey in the allowlist        |   and only here
  |    2. validate Arguments against the descriptor's   |
  |       schema, rejecting unknown fields (L2-08)      |
  |    3. DECODE into the generated typed request       |
  +----------------------------------------------------+
        |  ApplyBlockEditsRequest  (a generated record)
        v
  INotesOperations.ApplyBlockEditsAsync(...)              typed, compile-time checked
        |
        v
  application service -> domain                            no structured value anywhere
```

| # | Rule |
|---|---|
| <a id="rule-dp-01"></a>DP-01 | **The structured value model is permitted at exactly one place: the boundary dispatch contract** (`ICapabilityProvider`). It appears in no domain type, no application service signature, no product operation interface and no persisted schema. |
| <a id="rule-dp-02"></a>DP-02 | **[XT-05](../15-extension-platform-architecture.md#rule-xt-05) is scoped accordingly**: the containment test asserts the structured value type is absent from every **domain, application and product-operation** assembly, and permitted **only** in the boundary dispatch assembly. A test that simply forbade it everywhere would fail against the boundary the design requires, which is why the previous unscoped wording was a defect rather than a stricter rule. |
| <a id="rule-dp-03"></a>DP-03 | **The decoder is generated, never hand-written and never reflective.** The pinned contract generator reads each authored proto request/service descriptor and its declared operation profile and emits: the descriptor's schema, the allowlist entry, and the decode function. Adding an operation therefore cannot forget to update any of the three ([CF-01](../15-extension-platform-architecture.md#rule-cf-01) of the extension architecture). |
| <a id="rule-dp-04"></a>DP-04 | **`CapabilityKey` resolves through a closed generated allowlist**, not a dictionary lookup at runtime and not a name-to-type map. An unknown key is a typed protocol error before any validation ([RC-02](../17-agent-harness.md#rule-rc-02) of the harness). |
| <a id="rule-dp-05"></a>DP-05 | **Decode failure is a typed protocol error attributed to the caller** ([L2-05](../15-extension-platform-architecture.md#rule-l2-05)), never a host exception and never a partially applied operation. Validation completes before the typed request is constructed. |
| <a id="rule-dp-06"></a>DP-06 | **AOT holds because nothing is discovered at runtime**: the allowlist, the schemas and the decoders are all generated at compile time, so there is no reflection, no `MakeGenericType` and no assembly scanning on the invocation path ([AC-04](../00-architecture-overview.md#rule-ac-04)). |
| <a id="rule-dp-07"></a>DP-07 | **Versioning lives on the authored proto contract.** Typed records and tool schemas are generated from it, so a field added to the record is a schema change by construction, and the compatibility class of the operation governs whether that addition is permitted (`§6` of the operation catalogue). The schema is never edited independently of the record. |
| <a id="rule-dp-08"></a>DP-08 | **The same decode step serves a model tool call and an extension invocation.** There is one boundary, not two, which is what keeps the security pipeline, the validation rules and the audit trail identical for both. |

| # | Rule |
|---|---|
| <a id="rule-dp-09"></a>DP-09 | **A product operation is never reachable except through its typed interface.** The boundary calls `INotesOperations`, `IScopeOperations`, `ISlateOperations` or `IChatOperations`; it never touches an application service or a repository directly, and an architecture test asserts it ([WP-05](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05)). |
| <a id="rule-dp-10"></a>DP-10 | **`ResourceRef` and `ArtifactRef` cross the boundary by identity**; large payloads never travel inside the structured value ([CI-05](#rule-ci-05)). |

---

## 4. Context and artifacts

### `IContextProvider`

```
DescribeContextKindsAsync()                     → ArcResult<ContextKindDescriptor[]>
ProvideContextAsync(ContextRequest)             → ArcResult<ContextContribution>
```

`ContextRequest` names the kind, an optional selector, and a **budget** in items and bytes.

| # | Rule |
|---|---|
| <a id="rule-cx-01"></a>CX-01 | **Oversized context is refused explicitly**, never silently truncated ([WP-17](../../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17)). The refusal names what was requested and what the budget allows. |
| <a id="rule-cx-02"></a>CX-02 | **A contribution states its size before it is used**, so the user can see what is being shared ([WP-17](../../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17)). |
| <a id="rule-cx-03"></a>CX-03 | **Raw evidence never enters a contribution** where the product's rules forbid it — ArcScope raw capture and ArcSlate media are structurally excluded ([WP-35.01](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01), [WP-39.01](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.01)). |

### `IArtifactHandler`

```
DescribeArtifactKindsAsync()          → ArcResult<ArtifactKindDescriptor[]>
ResolveAsync(ArtifactRef)             → ArcResult<ArtifactResolution>
RenderPreviewAsync(ArtifactRef, PreviewRequest)
                                      → ArcResult<PreviewResult>
OpenAsync(ArtifactRef, OpenIntent)    → ArcResult<Unit>
```

| # | Rule |
|---|---|
| <a id="rule-ar-01"></a>AR-01 | **`ResolveAsync` re-checks permission at access** ([WP-14.05](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05)), never trusting that the reference was obtained legitimately. |
| <a id="rule-ar-02"></a>AR-02 | **A stale or deleted target is reported honestly** — `state.gone` rather than a plausible-looking empty result ([WP-17](../../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17)). |
| <a id="rule-ar-03"></a>AR-03 | **`RenderPreviewAsync` returns a bounded presentable form**, never the underlying body (`§4` of the rich-content architecture). |
| <a id="rule-ar-04"></a>AR-04 | An assistant-generated artifact belongs to its frozen application/Cloud execution scope and existing resource owner. Shared UI does not create a separate ArcChat owner or another product's write permission. |

---

## 5. Resource access and lifecycle

### `IResourceAccess`

```
GetMetadataAsync(ResourceId)                    → ArcResult<ResourceRef>
OpenReadAsync(ResourceId, RangeRequest?)        → ArcResult<TransferChannel>
ReleaseAsync(ResourceId, ReferrerRef)           → ArcResult<Unit>
```

| # | Rule |
|---|---|
| <a id="rule-ra-01"></a>RA-01 | **A path is never returned.** `TransferChannel` carries controlled access; `LocalResourceLocator` is resolved by the owner and is not a user-visible path ([XS-01](../data-model/00-data-model-overview.md#rule-xs-01), [I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)). |
| <a id="rule-ra-02"></a>RA-02 | **Range, checksum, cancellation and rate limiting are all supported**. |
| <a id="rule-ra-03"></a>RA-03 | **Resource bodies stay with the owning product adapter.** The assistant consumes a bounded authorized preview or opaque handle; no shared process, path-based relay or cross-product body route exists. |

### `IProductLifecycle` and `IDeepLinkTarget`

```
GetStateAsync()                          → ArcResult<ProductState>
PrepareForShutdownAsync(ShutdownReason)  → ArcResult<ShutdownDecision>
HandleDeepLinkAsync(DeepLink)            → ArcResult<DeepLinkOutcome>
```

| # | Rule |
|---|---|
| <a id="rule-lc-01"></a>LC-01 | **`PrepareForShutdownAsync` may refuse with a reason** — running capture, unsaved work, active render — and the shell surfaces the consequence rather than proceeding ([LF-04](../../requirements/09-shared-desktop-experience.md#rule-lf-04)). |
| <a id="rule-lc-02"></a>LC-02 | **A deep link is untrusted input carrying no secret** ([DL-02](../../requirements/09-shared-desktop-experience.md#rule-dl-02), [DL-03](../../requirements/09-shared-desktop-experience.md#rule-dl-03)), and `HandleDeepLinkAsync` validates before acting. |

---

## 6. Product operation interfaces

These are the domain operations each product exposes as capabilities. They are the concrete answer to *what can an authorized assistant or companion do within this application*.

### `INotesOperations` — ArcNotes

The methods below use the version preconditions in [NO-02](#rule-no-02). Notebook/folder create, rename, move, reorder, trash and restore mirror the typed Cloud structural requests with local composite preconditions; their pending events and frozen sync batches retain the same command identity. Local Scope/Slate operations instead return NativeContentRevision and ProductJobRef. `ExpectedRev`/`Revision` in the abbreviated signatures is not a shared untyped integer across these authorities.

| Operation | Risk / approval | Class |
|---|---|---|
| `SearchAsync(NotesQuery)` → `Page<DocumentSummary>` | `R1`, none | `Q` |
| `GetDocumentAsync(DocumentId, DocumentProjection)` → `DocumentView` | `R1`, none | `Q` |
| `CreateDocumentAsync(CreateDocument)` → `DocumentRef` | `R2`, `perOperation` | `CC` |
| `AppendBlocksAsync(DocumentId, Block[], ExpectedRev)` → `Revision` | `R2`, `perOperation` | `AP` |
| `ApplyBlockEditsAsync(DocumentId, BlockEdit[], ExpectedRev)` → `Revision` | `R2`, `perOperation` | `IW` |
| `SetPropertiesAsync(DocumentId, PropertyValue[], ExpectedRev)` → `Revision` | `R2`, `perOperation` | `IW` |
| `AddTagsAsync` / `RemoveTagsAsync` | `R1`, none | `IW` |
| `CreateLinkAsync(DocumentId, LinkSpec, ExpectedRev)` → `Revision` | `R2`, `perOperation` | `IW` |
| `TrashDocumentAsync(DocumentId, ExpectedRev)` → `Revision` | `R3`, `perOperation` | `DE` |
| `ExportAsync(ExportRequest)` → `ArtifactRef` | `R2`, `perOperation`; **`egress = declared`** when the target is outside the workspace | `NI` |

| # | Rule |
|---|---|
| <a id="rule-no-01"></a>NO-01 | ApplyBlockEdits takes the typed notes.commands.v1 edit list and validates the whole document at expected LocalNotesVersion before one owner commit/undo/outbox publication. Local block commands do not imply per-block Cloud sync. Whole-document conflict preservation and admitted Cloud owner writes follow Notes authority; no blind document replacement bypasses the revision guard. |
| <a id="rule-no-02"></a>NO-02 | **Local Notes edits use LocalNotesVersion(acked_rev, head_local_seq).** A Cloud tool with only an acknowledged revision requires a clean matching shadow; if local edits are pending it returns `conflict.local_changes_pending` until sync/resolution supplies a fresh context. It cannot silently overwrite pending content. Writes return the resulting local token and pending status; Cloud ack is a later, distinct event. |
| <a id="rule-no-03"></a>NO-03 | **`CreateDocumentAsync` takes a caller-allocated `DocumentId`**, which makes it idempotent under retry ([ID-04](../data-model/00-data-model-overview.md#rule-id-04)). |
| <a id="rule-no-04"></a>NO-04 | **A write takes and returns the composite local token `(acked_rev, head_local_seq)`** ([RV-C5](../data-model/02-desktop-data-model.md#rule-rv-c5) of the desktop data model), not a bare revision ([RV-C3](../data-model/02-desktop-data-model.md#rule-rv-c3), [RV-C4](../data-model/02-desktop-data-model.md#rule-rv-c4) of the desktop data model), and enqueues a `sync_outbox` row. It does **not** return a Cloud acknowledgement ([PE-04](../data-model/02-desktop-data-model.md#rule-pe-04)): the caller learns the edit is durable on this device, which is a different fact from acknowledged by Cloud. Passing only `acked_rev` would let two local callers overwrite each other between acknowledgements; passing `local_rev` to Cloud would conflict on every second edit. |
| <a id="rule-no-05"></a>NO-05 | **`SearchAsync` searches the hydrated local cache.** Cloud search over the whole workspace is `search.query` on the public surface; the two are separate operations with different completeness, and neither is presented as the other. |
| <a id="rule-no-06"></a>NO-06 | **`SetPropertiesAsync` accepts only declared property definitions with bounded scalar types** from the [ArcNotes property requirements](../../requirements/products/arcnotes.md#7-properties-tags-and-views) and [property storage model](../data-model/02-desktop-data-model.md#property_definition-property_value). There is no formula, relation or rollup evaluation, so no expression reaches this path. |

<a id="notes-query-contract"></a>
**NotesQuery.** Required `profile`, notebook ID, optional saved-view ID/revision, typed filter/sort/projection and referenced definition semantic revisions; optional cursor/page size. [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile) fixes value encodings, operators, limits, ordering and revision behavior. The result includes typed DocumentSummary values, source dataset token, `scope=hydratedLocal` or `acknowledgedCloud`, pending/completeness indicators and next cursor. An ad-hoc query binds current definitions at first evaluation; a saved query validates its persisted bindings. No unknown operator/type is ignored. Expected errors are `validation.invalid_request`, `validation.ast_bounds_exceeded`, `validation.unsupported_version`, `conflict.revision_mismatch` and permission-safe `state.not_found`. A stale cursor instructs restart without a partial success page.

### `IScopeOperations` — ArcScope

| Operation | Risk / approval | Class |
|---|---|---|
| `ListSessionsAsync` / `GetSessionAsync` / `ListCapturesAsync` | `R1`, none | `Q` |
| `GetConfigurationSnapshotAsync(SessionId)` | `R1`, none | `Q` |
| `RunMeasurementAsync(MeasurementRequest)` → `MeasurementResult` | `R2`, `perOperation` | `NI` |
| `RunAnalysisAsync(AnalysisRequest)` → `ProductJobRef` | `R2`, `perOperation` | `NI` |
| `CompareSessionsAsync(CompareRequest)` → `ComparisonRef` | `R2`, none | `NI` |
| `CreateAnnotationAsync` / `CreateFindingAsync` | `R2`, `perOperation` | `CC` |
| `GenerateReportAsync(ReportRequest)` → `ArtifactRef` | `R2`, `perOperation` | `NI` |
| `StartCaptureAsync(CaptureRequest)` → `CaptureRef` | **`R3`, `perOperation`** | `NI` |
| `StopCaptureAsync(CaptureId)` | **`R3`, `perOperation`** | `IW` |
| `GetStructuredContextAsync(ContextRequest)` → `StructuredResultBundle` | `R1`, none | `Q` |

| # | Rule |
|---|---|
| <a id="rule-so-01"></a>SO-01 | **Start and stop capture are `R3` operations with real side effects**, not read-only conveniences ([DC-03](../../requirements/products/arcscope.md#rule-dc-03) in the ArcScope requirements). |
| <a id="rule-so-02"></a>SO-02 | **There is no operation that returns raw capture.** `GetStructuredContextAsync` returns measurements, analysis outputs, decoded event summaries and selected ranges — **raw capture structurally cannot enter it** ([WP-35.01](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01)). |
| <a id="rule-so-03"></a>SO-03 | **There is no device-control operation in V1.** Device control is a separate, later, higher-permission class and does not appear on this interface ([DC-02](../../requirements/products/arcscope.md#rule-dc-02) there). |
| <a id="rule-so-04"></a>SO-04 | **No operation writes raw capture.** ArcScope alone writes it, from its acquisition loop ([WP-35.05](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.05)). |

**MeasurementRequest/MeasurementResult.** Use the [measurement storage projection](../data-model/02-desktop-data-model.md#measurement-storage) and [scope.measurement.v1](../../requirements/products/arcscope.md#measurement-profile) verbatim: frozen source/window/configuration, explicit family set, optional cursor/threshold input, resolved thresholds and per-family status/value/unit/count. A long analysis returns the existing ProductJobRef and the same eventual result shape. Insufficient data is a typed successful result with absent value, not zero or an RPC error. Invalid envelope/config is `validation.invalid_request`, unknown profile is `validation.unsupported_version`; stale requested source revision is `conflict.revision_mismatch`. Structured context and report APIs carry the profile, source bindings, quality and content origin without raw capture.

### `ISlateOperations` — ArcSlate

| Operation | Risk / approval | Class |
|---|---|---|
| `ListProjectsAsync` / `GetSequenceAsync` / `ListMediaAsync` | `R1`, none | `Q` |
| `GetTimelineAsync(SequenceId, TimeRange?)` → `TimelineView` | `R1`, none | `Q` |
| `ListMarkersAsync` / `CreateMarkerAsync` | `R1` / `R2` | `Q` / `CC` |
| `ApplyTimelineEditsAsync(SequenceId, TimelineEdit[], ExpectedRev)` → `Revision` | `R2`, `perOperation` | `IW` |
| `StartRenderAsync(RenderRequest)` → `ProductJobRef` | `R2`, `perOperation` | `NI` |
| `CancelRenderAsync(RenderRequestId)` | `R2`, none | `IW` |
| `ExportAsync(ExportRequest)` → `ArtifactRef` | `R2`, `perOperation`; `egress = declared` | `NI` |
| `GetSequenceContextAsync(ContextRequest)` → `SequenceContextReference` | `R1`, none | `Q` |
| `ImportOtioAsync(OtioImportRequest)` → `OtioImportResult` | `R2`, `perOperation`; `egress = none` | `NI` |
| `PreviewOtioImportAsync(OtioImportRequest)` → `OtioFidelityReport` | `R1`, none | `Q` |
| `ExportOtioAsync(SequenceId, CommittedRev, OtioExportRequest)` → `ArtifactRef` + `OtioFidelityReport` | `R2`, `perOperation`; `egress = declared` | `NI` |
| `RelinkMediaAsync(SequenceId, MediaRelink[])` → `Revision` | `R2`, none | `IW` |

| # | Rule |
|---|---|
| <a id="rule-sl-01"></a>SL-01 | The Slate local contract is published by WP03 with all other local signatures using the fixed wire/timeline/undo profiles. WP39.00 implements and exposes those semantics; it does not first define or create the interface. |
| <a id="rule-sl-02"></a>SL-02 | **`GetSequenceContextAsync` returns structure, markers, ranges, timecodes and metadata — never media** ([WP-39.01](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.01)). |
| <a id="rule-sl-03"></a>SL-03 | **`StartRenderAsync` binds a revision snapshot** and returns a `ProductJobRef`; the render never reads live editor state ([RN-04](../../requirements/products/arcslate.md#rule-rn-04)). |
| <a id="rule-sl-04"></a>SL-04 | **`StartRenderAsync` produces a native Product Job, not a Cloud Agent Task** ([I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485), [CM-04](../09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture). It invokes no model, consumes no AI capacity, and ArcSlate owns its progress and recovery. |
| <a id="rule-sl-05"></a>SL-05 | **OTIO import is staged before commit** ([OT-09](../../requirements/products/arcslate.md#rule-ot-09)). `PreviewOtioImportAsync` returns the fidelity report without mutating the project, so the user reviews retained, approximated and omitted dispositions **before** anything changes ([OT-07](../../requirements/products/arcslate.md#rule-ot-07)). |
| <a id="rule-sl-06"></a>SL-06 | **Import creates ArcSlate-owned canonical objects with provenance; OTIO is never the mutable working store** ([OT-04](../../requirements/products/arcslate.md#rule-ot-04), [I-497](../../requirements/01-normative-glossary-and-invariants.md#rule-i-497)). |
| <a id="rule-sl-07"></a>SL-07 | **Export binds a committed sequence revision** and writes a **separate artifact** carrying the support profile and fidelity information ([OT-04](../../requirements/products/arcslate.md#rule-ot-04)). It cannot export live editor state. |
| <a id="rule-sl-08"></a>SL-08 | **Export writes a temporary destination and publishes atomically** ([OT-10](../../requirements/products/arcslate.md#rule-ot-10)). Failure or cancellation leaves both the project and any existing destination untouched; overwrite requires explicit approval. |
| <a id="rule-sl-09"></a>SL-09 | **A `.otio` file references media; it never collects, uploads or embeds it** ([OT-08](../../requirements/products/arcslate.md#rule-ot-08)). Relative paths resolve only under an explicitly approved base; missing media becomes relinkable Offline Media, which is what `RelinkMediaAsync` addresses. |
| <a id="rule-sl-10"></a>SL-10 | **Parsing is bounded and adapter-free** ([OT-09](../../requirements/products/arcslate.md#rule-ot-09)): bounded size, depth and item count; malformed or unsupported schema rejected; **no arbitrary adapters, no Python plug-ins, no executable content**. Native OTIO use stays behind an owned narrow C ABI and the untrusted-content boundary. |
| <a id="rule-sl-11"></a>SL-11 | **A fidelity report excludes unselected absolute paths and secrets** ([OT-10](../../requirements/products/arcslate.md#rule-ot-10)). |

### `IChatOperations` — ArcChat

| Operation | Risk / approval | Class |
|---|---|---|
| `ListConversationsAsync` / `GetConversationAsync` | `R1`, none | `Q` |
| `CreateConversationAsync(CreateConversation)` → `ConversationRef` | `R2`, none | `CC` |
| `AppendUserMessageAsync(ConversationId, MessageDraft, ExpectedRev)` → `Revision` | `R2`, none | `AP` |
| `StartAgentTurnAsync(TurnRequest)` → `TaskRef` | `R2`+, per the plan's steps | `NI` |
| `SubmitApprovalAsync(ApprovalId, Decision)` | risk of the underlying operation | `IW` |

| # | Rule |
|---|---|
| <a id="rule-ch-01"></a>CH-01 | **`StartAgentTurnAsync` submits the turn to Cloud and returns a `TaskRef` immediately.** It does **not** start a local loop: the Harness is Cloud-only ([LS-02](../17-agent-harness.md#rule-ls-02) of the harness). Generation is durable Cloud execution. |
| <a id="rule-ch-02"></a>CH-02 | The assistant invokes only the current product's typed in-process handlers or authorized same-product Cloud tools; cross-product writes and handoff remain future-only. |
| <a id="rule-ch-03"></a>CH-03 | **A turn submitted with no active paid service term is refused with `entitlement.no_service_term`** before any provider call ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01)). The desktop surfaces the reason and the action; it never retries into a paid path on its own. |
| <a id="rule-ch-04"></a>CH-04 | **Only acknowledged content is submitted as context.** An unsent draft or an unacknowledged local edit is visible to the user, not to the model ([PK-04](../17-agent-harness.md#rule-pk-04) of the harness, [I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124), [I-498](../../requirements/01-normative-glossary-and-invariants.md#rule-i-498)). |

---

## 7. What is deliberately absent from the local surface

| Absent | Why |
|---|---|
| Any network-facing operation | Local RPC is same-machine only ([BR-01](../../planning/work-packages/08-local-ipc-and-registration.md#rule-br-01) of [WP-08](../../planning/work-packages/08-local-ipc-and-registration.md#rule-wp-08)) |
| Any operation Cloud can call | **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** — Cloud never connects to a local endpoint |
| Any operation returning a filesystem path | [RA-01](#rule-ra-01), [I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192) |
| Any operation returning a plaintext secret | Use ≠ Reveal |
| Any whole-document or whole-project replace | [NO-01](#rule-no-01) — it would destroy concurrent edits |
| Any operation that writes raw capture | [SO-04](#rule-so-04) |
| A device-control operation | [SO-03](#rule-so-03) |
| Any cross-product relay operation | Current product ports stay in process; future Cloud collaboration has no active endpoint. |
| Any local model, embedding or inference operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — all inference is Cloud ([C-02](../../requirements/00-product-scope-and-portfolio.md#rule-c-02), [CM-02](../09-ai-and-agent-runtime-architecture.md#rule-cm-02)) |
| Any operation accepting or storing an end-user model-provider key | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — no end-user BYOK ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)) |
| Any local planning, tool-selection or turn-loop operation | The Harness is Cloud-only ([LS-02](../17-agent-harness.md#rule-ls-02)). The desktop executes authorised tools; it does not choose them |
| Any operation delegating to an external agent or sub-agent | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08)) |
| A canvas, whiteboard, frame, slide or presentation operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded from ArcNotes delivery |
| A DOCX, formula, relation or rollup operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded; import is Markdown/text (`§2.1` of the editing architecture) |

---

## 8. Verification

| # | Obligation | Where |
|---|---|---|
| <a id="rule-lv-01"></a>LV-01 | Every typed product operation has an authored record binding and static delegate; only helper/extension methods have RPC registrations | WP03.04 and WP05.03 |
| <a id="rule-lv-02"></a>LV-02 | Parent/helper control works between published AOT binaries; product calls use typed in-process ports | WP06/08 and WP14 |
| <a id="rule-lv-03"></a>LV-03 | Owner-side validation refuses regardless of caller assertion, including a forged approval token | [WP-14.04](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) |
| <a id="rule-lv-04"></a>LV-04 | Every write is idempotent on `CommandId` under retry, disconnection and concurrency | [WP-14.03](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03) |
| <a id="rule-lv-05"></a>LV-05 | Context freezing is provable: a mutation during invocation does not affect the frozen snapshot | [WP-09.04](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.04) |
| <a id="rule-lv-06"></a>LV-06 | Resource previews stay within the declared bounds and no cross-product body relay exists | WP14.05 |
| <a id="rule-lv-07"></a>LV-07 | No interface exposes a path, a secret, or a raw capture read | Contract policy test |
| <a id="rule-lv-08"></a>LV-08 | Each product starts, works and saves with Cloud offline and other products absent | WP14.06 |

## [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012) executable wire and transport binding

Every operation/event above maps to the [numbered wire registry](04-protobuf-wire-registry.md). It fixes requests/results, record fields, enums, exact values, local counterpart preconditions, service names and compatibility. [CF integration](05-cloudflare-integration.md) fixes private Cloud/AI bindings and signed object-transfer exceptions; annex10 owns public output/control framing, state recovery and authorization. New supporting bootstrap, upload-status, automation and conversation-create methods are enumerated there with their authorization/idempotency classes; none is left for endpoint invention during implementation.

## Helper bootstrap and read-channel binding

The [complete local profile 09](09-local-grpc-and-sandbox.md) and numbered registry 04 add Renew, LocalEvents.Poll, ConnectorBroker and every typed ContentSandbox operation. No untyped event, private helper command or unspecified bootstrap proof remains; all are initial WP03 outputs.

The wire registry explicitly adds ILocalBootstrap.Challenge/Confirm and IResourceAccess.ReadChunk and IProductLifecycle.GetJob as transport-support methods. Challenge/Confirm are NI, OS-peer-only, one-use five-second bootstrap before normal owner authorization; they confer no product capability. ReadChunk is Q/R1/AO on the exact immutable owned transfer/version/offset, authorizing each bounded chunk. GetJob is Q/R1/AO on an owned native ProductJob. OpenRead returns LocalTransferTicket, never an HTTP bearer URL. The generated method names omit the C# Async suffix but preserve the catalogued operation's authorization, revision and effect rules.

## Complete Notes and Slate method surface

The [wire registry](04-protobuf-wire-registry.md#notes-structural-and-slate-operation-bindings) adds typed Notes move preview/mapping, full Slate metadata and extraction/transcript-adoption/subtitle import/export operations to this catalogue. Their exact fields, local revision preconditions, risk/class/compatibility, approval and loss semantics are defined there. Apply the same peer/actor/owner checks and generated capability allowlist as existing methods; no raw path, provider credential or generic invocation bypass is introduced.

## Initial producer and broker bindings

Every local signature, capability descriptor and OS broker method is a WP03 producer output. Later product WPs implement these published ports; they do not first define their request/response shape. [Wire local registry](04-protobuf-wire-registry.md#6-local-and-extension-operation-registry) fixes exact semantic Notes/Scope/Slate commands and resource/job transport support. The [native annex](06-native-functional-abi.md) owns helper bulk-buffer handles/lengths/leases and typed native exports; ordinary RPC frames do not carry full pixel/audio buffers. No obsolete IResourceProvider interface or generated-shape/code-first service is part of the current protocol.
