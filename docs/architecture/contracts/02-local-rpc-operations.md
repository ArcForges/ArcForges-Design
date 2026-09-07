# Local RPC Operations

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Contracts
> Governing authority: [`00-operation-catalogue.md`](00-operation-catalogue.md), [`../03-local-ipc-and-process-model.md`](../03-local-ipc-and-process-model.md), **[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)**
> Companions: [`../02-contracts-and-protocols.md`](../02-contracts-and-protocols.md), [`../data-model/02-desktop-data-model.md`](../data-model/02-desktop-data-model.md)

The same-machine surface. Every interface here is a source-generated RPC contract carrying the generated-shape attribute with public instance methods included (**[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)**), hosted over a named pipe or Unix domain socket, never over a network.

**Every method is task-returning and cancellation-aware** ([BR-09](../../planning/work-packages/08-local-ipc-and-registration.md#rule-br-09) of [WP-08](../../planning/work-packages/08-local-ipc-and-registration.md#rule-wp-08)). Signatures below omit the trailing cancellation token for brevity; it is present on all of them.

---

## 1. Interface map

| Interface | Hosted by | Consumed by |
|---|---|---|
| `IHubRegistry` | ArcChat Hub | Every product |
| `IHubRouting` | ArcChat Hub | Every product |
| `ICapabilityProvider` | Every product | Hub, on behalf of callers |
| `IContextProvider` | Every product | ArcChat |
| `IArtifactHandler` | Every product | ArcChat |
| `IResourceAccess` | Every product | Any authorised peer |
| `IProductLifecycle` | Every product | Hub |
| `IDeepLinkTarget` | Every product | Hub |
| `INotesOperations`, `IScopeOperations`, `ISlateOperations`, `IChatOperations` | The owning product | Hub, on behalf of callers |
| `IExtensionHost` | Product process | Extension process *(the protocol of [`../15-extension-platform-architecture.md`](../15-extension-platform-architecture.md), listed here for completeness)* |

---

## 2. Registration and routing

### `IHubRegistry`

```
RegisterAsync(RegistrationRequest)        → ArcResult<RegistrationLease>
RenewLeaseAsync(LeaseId)                  → ArcResult<RegistrationLease>
DeregisterAsync(LeaseId)                  → ArcResult<Unit>
ReportHealthAsync(LeaseId, HealthReport)  → ArcResult<Unit>
```

`RegistrationRequest` carries `AppIdentity`, `InstallationId`, `InstanceId`, the contract set version, the contributed `CapabilityDescriptor[]`, `ActionDescriptor[]`, context-provider kinds, artifact kinds and deep-link patterns.

| # | Rule |
|---|---|
| RG-01 | **Registration is idempotent.** Re-registering the same instance renews rather than duplicating ([WP-08.02](../../planning/work-packages/08-local-ipc-and-registration.md#rule-wp-08.02)). |
| RG-02 | **A lease expires without renewal**, so a killed provider disappears without the Hub polling. |
| RG-03 | **Re-registration after a Hub restart is automatic**, driven by the provider's reconnect loop, and requires no user action. |
| RG-04 | **A provider that cannot reach the Hub continues to work fully.** Registration failure degrades ecosystem features only ([BR-01](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-br-01) of [WP-14](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14)). |

### `IHubRouting`

```
ResolveCapabilityAsync(CapabilityKey, ResolutionContext) → ArcResult<CapabilityBinding>
ListContributionsAsync(ContributionFilter)               → ArcResult<Page<ContributionSummary>>
GetHealthAsync(AppIdentity?)                             → ArcResult<AggregateHealth>
```

| # | Rule |
|---|---|
| RT-01 | **Resolution is deterministic and explainable** — `CapabilityBinding` carries *why* this provider was chosen ([WP-09.02](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.02)). |
| <a id="rule-rt-02"></a>RT-02 | **The Hub routes; it never relays a payload body** ([BR-03](../../planning/work-packages/08-local-ipc-and-registration.md#rule-br-03) of [WP-08](../../planning/work-packages/08-local-ipc-and-registration.md#rule-wp-08)). A binding names an endpoint; the caller connects to it. |

---

## 3. Capability invocation

### `ICapabilityProvider`

```
DescribeAsync()                              → ArcResult<CapabilityDescriptor[]>
EvaluateAvailabilityAsync(ActionKey, FrozenContext)
                                             → ArcResult<AvailabilityResult>
InvokeAsync(InvocationRequest)               → ArcResult<InvocationOutcome>
```

`InvocationRequest` = `{ InvocationId, CommandId, CapabilityKey, FrozenContext, Arguments (structured value), ActorChain, ApprovalToken?, LeaseToken?, ExpectedVersion? }`.

| # | Rule |
|---|---|
| CI-01 | **`EvaluateAvailabilityAsync` is side-effect free** and cheap enough to run on UI enumeration ([WP-09.03](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03)). |
| CI-02 | **`InvokeAsync` performs owner-side final validation regardless of what the caller asserts** ([BR-02](../../planning/work-packages/20-first-cross-product-workflow.md#rule-br-02) of [WP-20](../../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20)). An `ApprovalToken` is evidence, never authority. |
| CI-07 | **`InvokeAsync` is the boundary, not a product contract.** It decodes into a generated typed request and calls the product's typed operation (`§3.1`). The structured value never travels past the decode step, so [AC-02](../00-architecture-overview.md#rule-ac-02)'s prohibition on a catch-all first-party call holds where it matters — in the product's own contracts. |
| CI-03 | **Context is frozen by the caller and immutable in transit** ([WP-09.04](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.04)). The provider never re-reads live context mid-invocation. |
| CI-04 | **The outcome carries the resulting authority-specific version**, so the caller can chain without re-reading. |
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
| DP-01 | **The structured value model is permitted at exactly one place: the boundary dispatch contract** (`ICapabilityProvider`). It appears in no domain type, no application service signature, no product operation interface and no persisted schema. |
| <a id="rule-dp-02"></a>DP-02 | **[XT-05](../15-extension-platform-architecture.md#rule-xt-05) is scoped accordingly**: the containment test asserts the structured value type is absent from every **domain, application and product-operation** assembly, and permitted **only** in the boundary dispatch assembly. A test that simply forbade it everywhere would fail against the boundary the design requires, which is why the previous unscoped wording was a defect rather than a stricter rule. |
| DP-03 | **The decoder is generated, never hand-written and never reflective.** A source generator reads each product operation's request record and emits: the descriptor's schema, the allowlist entry, and the decode function. Adding an operation therefore cannot forget to update any of the three ([CF-01](../15-extension-platform-architecture.md#rule-cf-01) of the extension architecture). |
| <a id="rule-dp-04"></a>DP-04 | **`CapabilityKey` resolves through a closed generated allowlist**, not a dictionary lookup at runtime and not a name-to-type map. An unknown key is a typed protocol error before any validation ([RC-02](../17-agent-harness.md#rule-rc-02) of the harness). |
| DP-05 | **Decode failure is a typed protocol error attributed to the caller** ([L2-05](../15-extension-platform-architecture.md#rule-l2-05)), never a host exception and never a partially applied operation. Validation completes before the typed request is constructed. |
| DP-06 | **AOT holds because nothing is discovered at runtime**: the allowlist, the schemas and the decoders are all generated at compile time, so there is no reflection, no `MakeGenericType` and no assembly scanning on the invocation path ([AC-04](../00-architecture-overview.md#rule-ac-04)). |
| DP-07 | **Versioning lives on the typed request record.** The schema is generated from it, so a field added to the record is a schema change by construction, and the compatibility class of the operation governs whether that addition is permitted (`§6` of the operation catalogue). The schema is never edited independently of the record. |
| DP-08 | **The same decode step serves a model tool call and an extension invocation.** There is one boundary, not two, which is what keeps the security pipeline, the validation rules and the audit trail identical for both. |

| # | Rule |
|---|---|
| DP-09 | **A product operation is never reachable except through its typed interface.** The boundary calls `INotesOperations`, `IScopeOperations`, `ISlateOperations` or `IChatOperations`; it never touches an application service or a repository directly, and an architecture test asserts it ([WP-05](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05)). |
| DP-10 | **`ResourceRef` and `ArtifactRef` cross the boundary by identity**; large payloads never travel inside the structured value ([CI-05](#rule-ci-05)). |

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
| CX-01 | **Oversized context is refused explicitly**, never silently truncated ([WP-20.00](../../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.00)). The refusal names what was requested and what the budget allows. |
| CX-02 | **A contribution states its size before it is used**, so the user can see what is being shared ([WP-20.00](../../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.00)). |
| CX-03 | **Raw evidence never enters a contribution** where the product's rules forbid it — ArcScope raw capture and ArcSlate media are structurally excluded ([WP-35.01](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01), [WP-39.01](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.01)). |

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
| AR-01 | **`ResolveAsync` re-checks permission at access** ([WP-14.05](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05)), never trusting that the reference was obtained legitimately. |
| AR-02 | **A stale or deleted target is reported honestly** — `state.gone` rather than a plausible-looking empty result ([WP-20.04](../../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.04)). |
| AR-03 | **`RenderPreviewAsync` returns a bounded presentable form**, never the underlying body (`§4` of the rich-content architecture). |
| AR-04 | **`OpenAsync` is rich handoff**: it activates the owning product on the right object, and works whether or not that product is already running ([WP-17.06](../../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.06)). |

---

## 5. Resource access and lifecycle

### `IResourceAccess`

```
GetMetadataAsync(ResourceId)                    → ArcResult<ResourceRef>
OpenReadAsync(ResourceId, RangeRequest?)        → ArcResult<TransferChannel>
BeginTransferAsync(TransferRequest)             → ArcResult<TransferTicket>
ReleaseAsync(ResourceId, ReferrerRef)           → ArcResult<Unit>
```

| # | Rule |
|---|---|
| <a id="rule-ra-01"></a>RA-01 | **A path is never returned.** `TransferChannel` and `TransferTicket` carry controlled access; `LocalResourceLocator` is resolved by the owner and is not a user-visible path ([XS-01](../data-model/00-data-model-overview.md#rule-xs-01), [I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)). |
| RA-02 | **Range, checksum, cancellation and rate limiting are all supported** (`I3 §14.2`). |
| RA-03 | **The Hub carries no body** ([WP-14.05](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05)), and a test asserts it. |

### `IProductLifecycle` and `IDeepLinkTarget`

```
GetStateAsync()                          → ArcResult<ProductState>
PrepareForShutdownAsync(ShutdownReason)  → ArcResult<ShutdownDecision>
HandleDeepLinkAsync(DeepLink)            → ArcResult<DeepLinkOutcome>
```

| # | Rule |
|---|---|
| LC-01 | **`PrepareForShutdownAsync` may refuse with a reason** — running capture, unsaved work, active render — and the shell surfaces the consequence rather than proceeding ([LF-04](../../requirements/09-shared-desktop-experience.md#rule-lf-04)). |
| LC-02 | **A deep link is untrusted input carrying no secret** ([DL-02](../../requirements/09-shared-desktop-experience.md#rule-dl-02), [DL-03](../../requirements/09-shared-desktop-experience.md#rule-dl-03)), and `HandleDeepLinkAsync` validates before acting. |

---

## 6. Product operation interfaces

These are the domain operations each product exposes as capabilities. They are the concrete answer to *what can an agent, another product, or a remote surface actually do*.

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
| <a id="rule-no-01"></a>NO-01 | **`ApplyBlockEditsAsync` takes a typed edit list**, not a document body. A whole-document replace is not offered, because it would destroy concurrent edits and defeat per-block sync. |
| <a id="rule-no-02"></a>NO-02 | **Local Notes edits use LocalNotesVersion(acked_rev, head_local_seq).** A Cloud tool with only an acknowledged revision requires a clean matching shadow; if local edits are pending it returns `conflict.local_changes_pending` until sync/resolution supplies a fresh context. It cannot silently overwrite pending content. Writes return the resulting local token and pending status; Cloud ack is a later, distinct event. |
| NO-03 | **`CreateDocumentAsync` takes a caller-allocated `DocumentId`**, which makes it idempotent under retry ([ID-04](../data-model/00-data-model-overview.md#rule-id-04)). |
| NO-04 | **A write takes and returns the composite local token `(acked_rev, head_local_seq)`** ([RV-C5](../data-model/02-desktop-data-model.md#rule-rv-c5) of the desktop data model), not a bare revision ([RV-C3](../data-model/02-desktop-data-model.md#rule-rv-c3), [RV-C4](../data-model/02-desktop-data-model.md#rule-rv-c4) of the desktop data model), and enqueues a `sync_outbox` row. It does **not** return a Cloud acknowledgement ([PE-04](../data-model/02-desktop-data-model.md#rule-pe-04)): the caller learns the edit is durable on this device, which is a different fact from acknowledged by Cloud. Passing only `acked_rev` would let two local callers overwrite each other between acknowledgements; passing `local_rev` to Cloud would conflict on every second edit. |
| <a id="rule-no-05"></a>NO-05 | **`SearchAsync` searches the hydrated local cache.** Cloud search over the whole workspace is `search.query` on the public surface; the two are separate operations with different completeness, and neither is presented as the other. |
| <a id="rule-no-06"></a>NO-06 | **`SetPropertiesAsync` accepts only declared property definitions with bounded scalar types** (`§2.1` of the editing architecture). There is no formula, relation or rollup evaluation, so no expression reaches this path. |

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
| SO-01 | **Start and stop capture are `R3` operations with real side effects**, not read-only conveniences ([DC-03](../../requirements/products/arcscope.md#rule-dc-03) in the ArcScope requirements). |
| SO-02 | **There is no operation that returns raw capture.** `GetStructuredContextAsync` returns measurements, analysis outputs, decoded event summaries and selected ranges — **raw capture structurally cannot enter it** ([WP-35.01](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01)). |
| <a id="rule-so-03"></a>SO-03 | **There is no device-control operation in V1.** Device control is a separate, later, higher-permission class and does not appear on this interface ([DC-02](../../requirements/products/arcscope.md#rule-dc-02) there). |
| <a id="rule-so-04"></a>SO-04 | **No operation writes raw capture.** ArcScope alone writes it, from its acquisition loop ([WP-35.05](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.05)). |

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
| SL-01 | **The capability contract was frozen only after timeline, command and undo semantics stabilised** (`I2 §III.10`, [WP-39.00](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.00)). This interface does not exist before [WP-39](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39). |
| SL-02 | **`GetSequenceContextAsync` returns structure, markers, ranges, timecodes and metadata — never media** ([WP-39.01](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.01)). |
| SL-03 | **`StartRenderAsync` binds a revision snapshot** and returns a `ProductJobRef`; the render never reads live editor state ([RN-04](../../requirements/products/arcslate.md#rule-rn-04)). |
| SL-04 | **`StartRenderAsync` produces a native Product Job, not a Cloud Agent Task** ([I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485), [CM-04](../09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture). It invokes no model, consumes no AI capacity, and ArcSlate owns its progress and recovery. |
| SL-05 | **OTIO import is staged before commit** ([OT-09](../../requirements/products/arcslate.md#rule-ot-09)). `PreviewOtioImportAsync` returns the fidelity report without mutating the project, so the user reviews retained, approximated and omitted dispositions **before** anything changes ([OT-07](../../requirements/products/arcslate.md#rule-ot-07)). |
| SL-06 | **Import creates ArcSlate-owned canonical objects with provenance; OTIO is never the mutable working store** ([OT-04](../../requirements/products/arcslate.md#rule-ot-04), [I-497](../../requirements/01-normative-glossary-and-invariants.md#rule-i-497)). |
| SL-07 | **Export binds a committed sequence revision** and writes a **separate artifact** carrying the support profile and fidelity information ([OT-04](../../requirements/products/arcslate.md#rule-ot-04)). It cannot export live editor state. |
| SL-08 | **Export writes a temporary destination and publishes atomically** ([OT-10](../../requirements/products/arcslate.md#rule-ot-10)). Failure or cancellation leaves both the project and any existing destination untouched; overwrite requires explicit approval. |
| SL-09 | **A `.otio` file references media; it never collects, uploads or embeds it** ([OT-08](../../requirements/products/arcslate.md#rule-ot-08)). Relative paths resolve only under an explicitly approved base; missing media becomes relinkable Offline Media, which is what `RelinkMediaAsync` addresses. |
| SL-10 | **Parsing is bounded and adapter-free** ([OT-09](../../requirements/products/arcslate.md#rule-ot-09)): bounded size, depth and item count; malformed or unsupported schema rejected; **no arbitrary adapters, no Python plug-ins, no executable content**. Native OTIO use stays behind an owned narrow C ABI and the untrusted-content boundary. |
| SL-11 | **A fidelity report excludes unselected absolute paths and secrets** ([OT-10](../../requirements/products/arcslate.md#rule-ot-10)). |

### `IChatOperations` — ArcChat

| Operation | Risk / approval | Class |
|---|---|---|
| `ListConversationsAsync` / `GetConversationAsync` | `R1`, none | `Q` |
| `CreateConversationAsync(CreateConversation)` → `ConversationRef` | `R2`, none | `CC` |
| `AppendUserMessageAsync(ConversationId, MessageDraft, ExpectedRev)` → `Revision` | `R2`, none | `AP` |
| `StartAgentTurnAsync(TurnRequest)` → `TaskRef` | `R2`+, per the plan's steps | `NI` |
| `SubmitApprovalAsync(ApprovalId, Decision)` | risk of the underlying operation | `IW` |
| `HandoffAsync(HandoffRequest)` | `R1`, none | `NI` |

| # | Rule |
|---|---|
| <a id="rule-ch-01"></a>CH-01 | **`StartAgentTurnAsync` submits the turn to Cloud and returns a `TaskRef` immediately.** It does **not** start a local loop: the Harness is Cloud-only ([LS-02](../17-agent-harness.md#rule-ls-02) of the harness). Generation is durable Cloud execution. |
| CH-02 | **ArcChat exposes no operation that writes another product's state.** It invokes their capabilities ([BR-01](../../planning/work-packages/20-first-cross-product-workflow.md#rule-br-01) of [WP-20](../../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20)). |
| CH-03 | **A turn submitted with no active paid service term is refused with `entitlement.no_service_term`** before any provider call ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01)). The desktop surfaces the reason and the action; it never retries into a paid path on its own. |
| CH-04 | **Only acknowledged content is submitted as context.** An unsent draft or an unacknowledged local edit is visible to the user, not to the model ([PK-04](../17-agent-harness.md#rule-pk-04) of the harness, [I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124), [I-498](../../requirements/01-normative-glossary-and-invariants.md#rule-i-498)). |

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
| A relay operation on the Hub | [RT-02](#rule-rt-02) — the Hub carries no body |
| Any local model, embedding or inference operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — all inference is Cloud ([C-02](../../requirements/00-product-scope-and-portfolio.md#rule-c-02), [CM-02](../09-ai-and-agent-runtime-architecture.md#rule-cm-02)) |
| Any operation accepting or storing a provider key | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — no end-user BYOK ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)) |
| Any local planning, tool-selection or turn-loop operation | The Harness is Cloud-only ([LS-02](../17-agent-harness.md#rule-ls-02)). The desktop executes authorised tools; it does not choose them |
| Any operation delegating to an external agent or sub-agent | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08)) |
| A canvas, whiteboard, frame, slide or presentation operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded from ArcNotes delivery |
| A DOCX, formula, relation or rollup operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded; import is Markdown/text (`§2.1` of the editing architecture) |

---

## 8. Verification

| # | Obligation | Where |
|---|---|---|
| LV-01 | Every interface carries the generated-shape attribute; a non-conforming interface fails the build | [WP-03.04](../../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.04), [WP-05.03](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.03) |
| LV-02 | Bidirectional invocation works between two published AOT binaries with generated proxies | [WP-06.01](../../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.01) |
| LV-03 | Owner-side validation refuses regardless of caller assertion, including a forged approval token | [WP-14.04](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) |
| LV-04 | Every write is idempotent on `CommandId` under retry, disconnection and concurrency | [WP-14.03](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03) |
| LV-05 | Context freezing is provable: a mutation during invocation does not affect the frozen snapshot | [WP-09.04](../../planning/work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.04) |
| LV-06 | The Hub demonstrably carries no payload body | [WP-14.05](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05) |
| LV-07 | No interface exposes a path, a secret, or a raw capture read | Contract policy test |
| LV-08 | Every product starts, works and saves with the Hub absent | [WP-14.06](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.06) |
