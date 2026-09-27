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
| `IScopeOperations`, `IChatOperations` | The owning product | owning application composition, for its authorized callers |
| `IExtensionHost` | Product process | Extension process *(the protocol of [`../15-extension-platform-architecture.md`](../15-extension-platform-architecture.md), listed here for completeness)* |

---

<a id="rule-rt-02"></a>
## 2. Registration and routing

`IHubRegistry` and `IHubRouting` are reserved historical names, excluded from current generated server registration and runtime. There is no application-to-application discovery or routing.

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
        |  RunMeasurementRequest  (a generated record)
        v
  IScopeOperations.RunMeasurementAsync(...)                typed, compile-time checked
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
| <a id="rule-dp-09"></a>DP-09 | **A product operation is never reachable except through its typed interface.** The boundary calls `IScopeOperations` or `IChatOperations`; it never touches an application service or a repository directly, and an architecture test asserts it ([WP-05](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05)). |
| <a id="rule-dp-10"></a>DP-10 | **`ResourceRef` and `ArtifactRef` cross the boundary by identity**; large payloads never travel inside the structured value ([CI-05](#rule-ci-05)). |

---

<a id="closed-in-process-authorization-profiles"></a>
## 3.2 Closed in-process authorization export profiles

These two profiles describe the already required owner-side boundaries under [AZ-04](00-operation-catalogue.md#rule-az-04). They admit no arbitrary derived expression, new transport or caller authority. The generated operation export and its policy checker must reject use of either profile by another operation or on another surface.

`ICapabilityProvider.Invoke` alone uses `in-process-invocation`, with scope and surface `in-process`. `authorization.capability` is `{"from":"admittedCapability.operationId"}`. Each of `risk`, `approval`, `stepUp`, `localPresence`, `egress` and `actorKinds` is `{"from":"admittedCapability.<same field name>"}`; `patEligible=false`; `idempotency={"from":"admittedCapability.idempotency"}`. Its `delegation` object is exactly `{"intersectOriginalActor":true,"requireCurrentGrant":true,"denyHumanOnly":true,"requireRegisteredProductHandler":true}`. The host resolves the admitted descriptor to its statically registered current-product handler, preserves frozen human/actor provenance, intersects permitted actors and current grants, applies effective-risk modifiers and performs owner-final validation. Missing or mismatched handler, descriptor, original actor or grant, and any human-only target, fail closed. No launch role, endpoint, public registration or ambient service credential is supplied by this profile. `IExtensionHost.Invoke` retains its distinct `private-helper` `delegated-invocation` profile and `requireLaunchRole=true` under [annex 09](09-local-grpc-and-sandbox.md#extension-operation-authorization-metadata).

`IChatOperations.SubmitApproval` alone uses `human-approval-decision`, with scope and surface `in-process`, `capability=null`, `actorKinds=[human]`, `patEligible=false`, `idempotency=IW`, `approval=foregroundProposal` and `egress=none`. Its only derived fields are `risk={"from":"verifiedApprovalProposal.effectiveRisk"}`, `stepUp={"from":"verifiedApprovalProposal.stepUp"}` and `localPresence={"from":"verifiedApprovalProposal.localPresence"}`. These closed sources are owner-resolved decision requirements of the exact pending action snapshot, never caller values or an approval reference treated as authority. For the first decision, resolve `approvalId` and `proposalHash` against the same verified human/current product, action, target, revision and unexpired pending proposal; enforce foreground and the required step-up/local-presence evidence before recording a one-use decision. Changed, expired, missing or mismatched proposals fail closed. Current stricter owner policy may raise requirements but never lower them. Preserve the actual effective risk, including higher runtime classification, rather than replacing it with fixed R1 or R3. This retains [the security approval rules](../../requirements/07-security-privacy-and-trust.md#3-approval) and the existing duplicate-command `IW` semantics. Under the same verified caller boundary, the same command and canonical input return the same recorded decision even after that proposal is consumed or expires; replay creates neither a fresh grant nor a second decision or execution. A conflicting input or new command cannot revive the consumed/expired proposal.

Approval submission grants neither a persistent permission nor automatic execution: the later underlying operation still performs owner-final validation. Agent, automation, extension and PAT actors, public/private-helper surfaces and arbitrary derived expressions are rejected for this approval-decision profile. The decision profile has no capability delegation object. Contract policy tests must include exact positive rows and wrong-operation/surface/actor/PAT/derived-source/binding negatives; metadata admission is not proof that a runtime owner has implemented these checks.

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
| <a id="rule-cx-03"></a>CX-03 | **Raw evidence never enters a contribution** where the product's rules forbid it — ArcScope raw capture is structurally excluded ([WP-35.01](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01)). |

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

<a id="ordinary-in-process-authorization-metadata"></a>
### 5.1 Ordinary in-process infrastructure metadata

The following closed table supplies the operation export for the seventeen ordinary infrastructure methods already registered in registry 04 and manifest 11. It does not add a method, tool, listener or private-helper binding. Every row has scope and surface `in-process`, profile `product-handler`, `capability=null`, `actorKinds=[human,product-handler]`, `patEligible=false`, baseline `risk=R1`, `approval=none`, `stepUp=false` and `localPresence=false`. The owning product handler preserves its verified human and actor provenance; these infrastructure ports are not directly model-callable capabilities. An agent, automation or extension can reach only an admitted product operation through the separate invocation boundary, never acquire this infrastructure identity from a claimed actor kind.

| Exact operation ID | Idempotency | Egress |
|---|---|---|
| `ICapabilityProvider.Describe` | `Q` | `none` |
| `ICapabilityProvider.EvaluateAvailability` | `Q` | `none` |
| `IContextProvider.DescribeContextKinds` | `Q` | `none` |
| `IContextProvider.ProvideContext` | `Q` | `ownedContent` |
| `IArtifactHandler.DescribeArtifactKinds` | `Q` | `none` |
| `IArtifactHandler.Resolve` | `Q` | `ownedContent` |
| `IArtifactHandler.RenderPreview` | `Q` | `ownedContent` |
| `IArtifactHandler.Open` | `NI` | `ownedContent` |
| `IResourceAccess.GetMetadata` | `Q` | `none` |
| `IResourceAccess.OpenRead` | `Q` | `ownedContent` |
| `IResourceAccess.Release` | `IW` | `none` |
| `IResourceAccess.ReadChunk` | `Q` | `ownedContent` |
| `IProductLifecycle.GetState` | `Q` | `none` |
| `IProductLifecycle.PrepareForShutdown` | `NI` | `none` |
| `IProductLifecycle.GetJob` | `Q` | `none` |
| `IDeepLinkTarget.HandleDeepLink` | `NI` | `none` |
| `ILocalEvents.Poll` | `Q` | `none` |

`ownedContent` denotes exactly the receiving owned application/helper/resource/AI context in [catalogue 00's egress table](00-operation-catalogue.md#4-authorization-declaration): the owner checks source version, bounded range, purpose and destination grant before returning content. It is not unrestricted external egress or implicit AI consent; raw Scope capture remains excluded from context. `none` authorizes no additional external destination and never removes response access checks or redaction. `Q` describes an authorized read, not permission to retry under a revoked grant or changed immutable transfer; each access rechecks the current owner conditions. Opening a transfer may allocate a new bounded ticket, but it does not mutate the underlying resource or grant additional access. `Release` is `IW` only for the same owned resource/referrer and command/input; replay cannot decrement another reference or trigger an unrelated deletion.

The table declares the infrastructure baseline, not a ceiling on effective risk or a promise that a sensitive read is safe. Existing source/owner policy and runtime risk modifiers may require stronger approval, step-up or local presence and must be enforced before the affected access/effect. These ports do not authorize a later capability effect. `Open` and `HandleDeepLink` navigate within the owning application; a deep link remains untrusted and opens an interface with a prefilled intent, never invisibly executes a side-effecting command under [DL-01](../../requirements/09-shared-desktop-experience.md#rule-dl-01). `PrepareForShutdown` may refuse and does not authorize forced shutdown or loss of unsaved/capture state. The three `NI` rows are not automatically replayed after an unknown outcome. `Poll` returns bounded hints only and remains an in-process port in this operation set; it does not register a peer endpoint.

---

## 6. Product operation interfaces

These are the domain operations each product exposes as capabilities. They are the concrete answer to *what can an authorized assistant or companion do within this application*.

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

### `IChatOperations` — ArcChat

| Operation | Risk / approval | Class |
|---|---|---|
| `ListConversationsAsync` / `GetConversationAsync` | `R1`, none | `Q` |
| `CreateConversationAsync(CreateConversation)` → `ConversationRef` | `R2`, none | `CC` |
| `AppendUserMessageAsync(ConversationId, MessageDraft, ExpectedRev)` → `Revision` | `R2`, none | `AP` |
| `StartAgentTurnAsync(TurnRequest)` → `TaskRef` | `R2`+, per the plan's steps | `NI` |
| `SubmitApprovalAsync(ApprovalId, Decision)` | risk of the underlying operation | `IW` |
| `OpenArtifactAsync(ArtifactRef, OpenIntent)` | `R1`, none; `ownedContent` egress | `NI` |

`StartAgentTurn`'s exported `R2` and `approval=perPlanStep` classify submission of the durable Cloud task, not every action the eventual plan may request. This is the existing `R2`+ posture: compute effective risk with current modifiers at submission, then evaluate every planned step against its own admitted capability, scope, egress and approval requirements before execution. Returning a TaskRef grants no blanket R2 approval, standing permission or local agent loop. `NI` preserves unknown-effect reconciliation; a lost response is not permission to submit another paid task automatically.

`IChatOperations.OpenArtifact` retains its existing generated first-party tool eligibility under registry 04. Its export uses `tool-delegation`, exact capability `IChatOperations.OpenArtifact`, `actorKinds=[human,agent,automation,extension]`, `patEligible=false`, baseline `stepUp=false` and `localPresence=false`, with the risk/approval/idempotency and `ownedContent` egress above. The target remains the current application's authorized artifact owner; navigation does not grant cross-product access or authority to execute the artifact's suggested actions. Both rows retain stricter current owner policy and all original-actor/current-grant checks; neither can reach the human-only approval-decision path.

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
| Any operation that writes raw capture | [SO-04](#rule-so-04) |
| A device-control operation | [SO-03](#rule-so-03) |
| Any cross-product relay operation | Current product ports stay in process; future Cloud collaboration has no active endpoint. |
| Any local model, embedding or inference operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — all inference is Cloud ([C-02](../../requirements/00-product-scope-and-portfolio.md#rule-c-02), [CM-02](../09-ai-and-agent-runtime-architecture.md#rule-cm-02)) |
| Any operation accepting or storing an end-user model-provider key | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — no end-user BYOK ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)) |
| Any local planning, tool-selection or turn-loop operation | The Harness is Cloud-only ([LS-02](../17-agent-harness.md#rule-ls-02)). The desktop executes authorised tools; it does not choose them |
| Any operation delegating to an external agent or sub-agent | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08)) |

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

## Initial producer and broker bindings

Every local signature, capability descriptor and OS broker method is a WP03 producer output. Later product WPs implement these published ports; they do not first define their request/response shape. [Wire local registry](04-protobuf-wire-registry.md#6-local-and-extension-operation-registry) fixes exact semantic Scope commands and resource/job transport support. The [native annex](06-native-functional-abi.md) owns helper bulk-buffer handles/lengths/leases and typed native exports; ordinary RPC frames do not carry full pixel buffers. No obsolete IResourceProvider interface or generated-shape/code-first service is part of the current protocol.
