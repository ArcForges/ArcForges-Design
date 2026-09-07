# Public API Operations

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Contracts
> Governing authority: [`00-operation-catalogue.md`](00-operation-catalogue.md), [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§6`
> Companions: [`../data-model/01-cloud-data-model.md`](../data-model/01-cloud-data-model.md)

Every cloud HTTP operation. Columns follow `§2` of the catalogue: each operation names its capability, risk, approval posture, idempotency class, its primary errors beyond the universal set, and its compatibility class.

**Universal errors** omitted from each row: `auth.unauthenticated`, `auth.session_expired`, `validation.invalid_request`, `capacity.rate_limited`, `internal.unexpected`.

**Notation** — `Q` pure query · `IW` idempotent write · `CC` create-with-client-id · `AP` append · `NI` non-idempotent · `EX` external side effect · `DE` destructive. Compatibility: `AO` additive-open · `AC` additive-closed · `FR` frozen.

---

## 1. Identity and session

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `identity.beginPasskeyRegistration` | Start credential creation | session, `R2`, step-up if adding to an existing account | `NI` | — | `FR` |
| `identity.completePasskeyRegistration` | Finish and store the credential | session, `R2` | `IW` | `conflict.duplicate_identifier` | `FR` |
| `identity.beginAuthentication` | Issue a challenge | **anonymous** | `NI` | — | `FR` |
| `identity.completeAuthentication` | Verify and issue a session | **anonymous** | `NI` | `perm.capability_denied` | `FR` |
| `identity.requestEmailCode` | Send a one-time code | **anonymous**, rate-limited per address **and** per source | `NI` | `capacity.rate_limited` | `FR` |
| `identity.redeemEmailCode` | Verify a code | **anonymous** | `NI` | `state.invalid_transition` | `FR` |
| `identity.refreshSession` | Rotate the refresh token | refresh token | `NI` | `auth.session_expired` | `FR` |
| `identity.revokeSession` | End one session | session, `R2` | `DE` | `state.not_found` | `FR` |
| `identity.revokeAllSessions` | End every session but the caller's | session, `R3`, step-up | `DE` | — | `FR` |
| `identity.listAuthIdentities` | The user's credentials | session, `R1` | `Q` | — | `AO` |
| `identity.removeAuthIdentity` | Remove a credential | session, `R3`, step-up | `DE` | `identity.last_credential` | `FR` |
| `identity.beginStepUp` / `identity.completeStepUp` | Satisfy a step-up challenge | session | `NI` | `auth.step_up_required` | `FR` |
| `identity.beginRecovery` / `identity.completeRecovery` | Account recovery | **anonymous**, heavily rate-limited, fully audited | `NI` | `capacity.rate_limited` | `FR` |
| `identity.requestAccountDeletion` | Start the grace period | session, `R4`, step-up | `IW` | — | `FR` |
| `identity.cancelAccountDeletion` | Stop it within grace | session, `R3`, step-up | `IW` | `state.invalid_transition` | `FR` |

| # | Rule |
|---|---|
| ID-01 | **`identity.removeAuthIdentity` refuses the last usable credential** (`identity.last_credential`), because succeeding would lock the user out irrecoverably. |
| ID-02 | **Native identity.refreshSession rotates.** Reusing a superseded generation revokes its bearer family and raises a security audit event. BrowserCookie sessions use the separate adopted opaque-cookie lifecycle and never call this refresh endpoint. |
| ID-03 | **Account deletion never touches local data** ([ED-05](../16-billing-and-commerce-architecture.md#rule-ed-05)), and the response says so explicitly so the client can show it. |

---

<a id="browser-session-operations"></a>

### 1.1 Browser session transport operations

These C# endpoint mappings live inside the existing Cloud host, exposed through the Account/Chat same-origin edge. They share Identity application services and do not duplicate native authentication logic or other business operations. Their generated baseline is `contracts/browser-session/v1/openapi.json`; normal business endpoints still consume the same public API DTOs. Native bearer issuance/refresh endpoints are absent from the browser edge allowlist. Browser authentication and recovery use the same underlying Identity services with cookie-only response shaping; they cannot accidentally return a native token response. The native `identity.refreshSession` operation is not a browser refresh route.

| OperationId / verb and path | Auth/input | Output and effect |
|---|---|---|
| `browser.bootstrap` · GET `/session/v1/bootstrap` | Anonymous or live cookie session; exact configured origin | No-store CSRF request token, authenticated flag and safe session/expiry/profile projection. Pre-auth material is bounded/expiring; no bearer/session secret in JSON |
| `browser.beginAuthentication` · POST `/session/v1/authentication/begin` | Pre-auth flow + CSRF/Origin; existing passkey/email policy | Expiring, rate-limited challenge bound to method/origin/RP/flow; no user-existence leak |
| `browser.completeAuthentication` · POST `/session/v1/authentication/complete` | One-use challenge response + CSRF/Origin | Creates lowest-trust browser device/session, Set-Cookie only, safe session projection; invalidate pre-auth flow |
| `browser.logout` · POST `/session/v1/logout` | Cookie + CSRF/Origin; replay against already-ended session is harmless | Revoke before cookie deletion; no-store result; never logout by GET |

Step-up, credential management, recovery, revoking other sessions and workspace selection use the existing public Identity/Workspace operations through the cookie-auth adapter with the same authorization and idempotency rules. WebSocket origin validation and negotiation antiforgery are explicit transport requirements, not new business operations. No endpoint accepts a caller-supplied forwarding URL.

**Errors and compatibility.** Reuse the existing auth/validation/rate-limit error vocabulary; unauthenticated/expired reads return an HTTP auth error, not an HTML redirect or a fake empty workspace. CSRF/origin failure executes no business handler. One-use authentication challenges are not ordinary retryable business commands; existing [NI](#ni-auth-note) semantics apply. Schema generation includes cookie/CSRF requirements, Set-Cookie/no-store metadata and safe response shapes. [Web session storage](../data-model/01-cloud-data-model.md#browser-session-storage) is the storage authority.

<a id="ni-auth-note"></a>
Authentication challenge creation/completion uses the catalogue's NI classification: no blind automatic retry; duplicate consumed challenge is rejected safely and a fresh login starts a new bounded flow.

---



## 2. Workspace and device

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `workspace.list` | The caller's workspaces | session, `R1` | `Q` | — | `AO` |
| `workspace.get` | One workspace with its settings | `R1` | `Q` | `state.not_found` | `AO` |
| `workspace.updateSettings` | Name, protection profile | `R2` | `IW` | `conflict.revision_mismatch` | `AC` |
| `device.register` | Register this device and installation | session, `R2` | `CC` | — | `FR` |
| `device.list` | The user's devices with trust and presence | `R1` | `Q` | — | `AO` |
| `device.rename` | User-visible name | `R1` | `IW` | — | `AC` |
| `device.setTrust` | Raise or lower trust | `R3`, **step-up** | `IW` | `auth.step_up_required` | `FR` |
| `device.setRemoteEnabled` | Enable remote work to this device | `R3`, **step-up**; requires `trust = trusted` | `IW` | `state.invalid_transition` | `FR` |
| `device.revoke` | Revoke a device and cascade | `R3`, step-up | `DE` | — | `FR` |
| `device.heartbeat` | Presence keepalive | session, `R0` | `NI` | — | `AO` |

| # | Rule |
|---|---|
| DV-01 | **`device.setRemoteEnabled` refuses without trust**, so remote capability can never be reached by a single mis-click ([WP-22.03](../../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22.03)). |
| DV-02 | **`device.revoke` cascades to sessions and push registrations in one transaction**, so a revoked device cannot act during a partial cascade. |

---

## 3. Entitlement

Owned by the **Entitlement** module, independent of Commerce ([EO-01](../16-billing-and-commerce-architecture.md#rule-eo-01)).

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `entitlement.getSnapshot` | Effective entitlement with per-capability reasons and its version | `R1` | `Q` | — | `AO` |
| `entitlement.getServiceTerm` | The effective paid service term: kind, interval, grace end, and whether AI is admissible **now** | `R1` | `Q` | — | `AO` |
| `entitlement.getCapacity` | Included capacity: available, held, burst, recovery rate, and a server-calculated `recoveryAt` | `R1` | `Q` | — | `AO` |
| `entitlement.listGrants` | Grant history with sources | `R1` | `Q` | — | `AO` |
| `entitlement.getUsage` | Quota, usage and period boundary | `R1` | `Q` | — | `AO` |
| `entitlement.check` | Batch capability check, for a client about to offer an action | `R1` | `Q` | — | `AO` |
| `commerce.authoriseExtraUsage` | Opt in to spending purchased credits, **with a maximum budget** | `R2`, step-up per policy | `IW` | `entitlement.no_service_term` | `FR` |
| `commerce.revokeExtraUsage` | Withdraw that authorisation | `R2` | `IW` | `state.not_found` | `FR` |
| `commerce.explainCharge` | Why a request waited, stopped or charged, and which pool funded it | `R1` | `Q` | `state.not_found` | `AO` |

| # | Rule |
|---|---|
| <a id="rule-ec-01"></a>EC-01 | **`entitlement.getServiceTerm` and `entitlement.getCapacity` are separate operations** because they answer different questions and change on different schedules ([I-493](../../requirements/01-normative-glossary-and-invariants.md#rule-i-493)). A client must not infer one from the other. |
| <a id="rule-ec-02"></a>EC-02 | **A client never computes admission.** These operations exist to explain and to enable affordances; the decision is server-side and atomic ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01), [AD-02](../16-billing-and-commerce-architecture.md#rule-ad-02)). |
| <a id="rule-ec-03"></a>EC-03 | **`recoveryAt` is server-calculated** ([AC-06](../../requirements/04-commerce-entitlement-and-credits.md#rule-ac-06)). A client never derives it from a rate and a clock. |
| <a id="rule-ec-04"></a>EC-04 | **`commerce.explainCharge` satisfies [AC-10](../../requirements/04-commerce-entitlement-and-credits.md#rule-ac-10)**: capacity consumption, purchased-credit consumption, compensation, supplier cost and revenue remain separately queryable, and a user can see which pool funded a request. |
| <a id="rule-ec-05"></a>EC-05 | **No operation accepts a provider key, a model endpoint or a customer credential** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)), asserted as a contract policy test. |

| # | Rule |
|---|---|
| <a id="rule-en-01"></a>EN-01 | **There is no public grant-issuing operation.** Grants are issued through the module API by Commerce or by an operator path, never over the public surface ([EO-03](../16-billing-and-commerce-architecture.md#rule-eo-03)). |
| EN-02 | **`getSnapshot` always returns `entitlementVersion`**, and clients cache against it. Realtime is a refresh hint, never authority ([ED-02](../16-billing-and-commerce-architecture.md#rule-ed-02)). |
| EN-03 | **`check` exists so a client can grey an action rather than offering and failing it.** It is a UX affordance; the enforcement is still server-side at the operation ([ED-04](../16-billing-and-commerce-architecture.md#rule-ed-04)). |

---

## 4. Commerce

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `commerce.getCatalogue` | Offers and price versions for the caller's region | `R1` | `Q` | — | `AO` |
| `commerce.createPurchaseIntent` | Allocate the idempotency anchor | `R2` | `CC` | `entitlement.not_entitled` | `FR` |
| `commerce.createCheckoutAttempt` | Obtain a provider-hosted checkout session | `R2` | `EX` | `provider.declined`, `state.invalid_transition` | `FR` |
| `commerce.getPurchaseState` | The confirming state after redirect | `R1` | `Q` | — | `FR` |
| `commerce.getSubscription` | Normalised subscription state | `R1` | `Q` | — | `AO` |
| `commerce.cancelSubscription` | Cancel at period end | `R3`, step-up | `IW` | `state.invalid_transition` | `FR` |
| `commerce.reactivateSubscription` | Undo a pending cancellation | `R2` | `IW` | `state.invalid_transition` | `FR` |
| `commerce.getCredits` | Allowance and purchased balances, **presented separately** | `R1` | `Q` | — | `FR` |
| `commerce.listBillingHistory` | Orders, payments, invoices | `R1` | `Q` | — | `AO` |
| `commerce.requestRefund` | Open a refund request | `R3`, step-up | `EX` | `state.invalid_transition` | `FR` |
| `commerce.exportEvidence` | Commercial evidence for a period | `R3`, step-up | `NI` | — | `FR` |
| `commerce.providerWebhook` | **Provider-facing**, signature-gated, not a customer operation | signature only | `AP` | `validation.invalid_request` | `FR` |

| # | Rule |
|---|---|
| <a id="rule-co-01"></a>CO-01 | **No operation accepts a payment instrument.** There is no card field anywhere in the surface ([PU-05](../16-billing-and-commerce-architecture.md#rule-pu-05)). |
| CO-02 | **`commerce.getPurchaseState` is the only thing a post-checkout redirect may call.** A redirect grants nothing ([PU-01](../16-billing-and-commerce-architecture.md#rule-pu-01)). |
| CO-03 | **`commerce.providerWebhook` persists before processing** and returns quickly ([EI-01](../16-billing-and-commerce-architecture.md#rule-ei-01), [EI-04](../16-billing-and-commerce-architecture.md#rule-ei-04)). It is isolated, rate-limited and signature-gated ([SR-03](../16-billing-and-commerce-architecture.md#rule-sr-03)). |
| CO-04 | **`getCredits` never returns a summed balance** ([CD-07](../16-billing-and-commerce-architecture.md#rule-cd-07) of the commerce architecture). Replenishing included capacity and purchased lots are separate fields: only the former recovers; purchased credits do not expire with time or cancellation. |

---

## 5. Sync

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `sync.listScopes` | Configured scopes with their exclusions | `R1` | `Q` | — | `AO` |
| `sync.setScope` | Enable, disable or adjust a scope | `R2` | `IW` | `conflict.revision_mismatch` | `AC` |
| `sync.pullChanges` | The change feed from a cursor | `R1` | `Q` | `sync.cursor_expired` | `FR` |
| `sync.pushChange` | Submit one local aggregate change | `R2` | `IW` | `conflict.revision_mismatch`, `entitlement.quota_exceeded` | `FR` |
| `sync.pushBatch` | Submit several, applied **individually** | `R2` | `IW` | per-item results | `FR` |
| `sync.getAggregate` | Authoritative state of one aggregate | `R1` | `Q` | `state.gone` | `AO` |
| `sync.listConflicts` | Unresolved conflicts needing a decision | `R1` | `Q` | — | `AO` |
| `sync.resolveConflict` | Apply a user decision | `R2` | `IW` | `state.invalid_transition` | `FR` |
| `sync.requestFullResync` | After cursor expiry | `R2` | `NI` | — | `FR` |

| # | Rule |
|---|---|
| SY-01 | **`sync.pushBatch` returns a per-item result.** A batch is a transport optimisation, never a transaction — one item's conflict must not roll back the rest. |
| SY-02 | **`sync.pullChanges` returns `(changes, nextCursor, hasMore)`** and never a partial page presented as complete. |
| SY-03 | **`sync.cursor_expired` instructs a full resync explicitly** rather than returning a silently incomplete delta ([WP-25.02](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.02)). |
| SY-04 | **`sync.pushChange` carries the authenticated originating `deviceId` and immutable batch receipt identity.** Own-origin feed records still reconcile revisions/receipts; only duplicate UI notification may be suppressed. |
| SY-05 | **A conflict is never auto-resolved by the client.** The server applies the scope's policy; where the policy defers to the user, `listConflicts` surfaces it and the discarded version stays recoverable ([WP-25.03](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.03)). |
| SY-06 | **Pull/apply uses the Cloud model's §9.2 protocol.** Pages are durably staged before cursor advance; per-aggregate revisions only advance; bootstrap manifests have a fixed snapshot, lower-bound cursor and bounded pin. Dependencies crossing pages are resolved by canonical reads, not assumed publication order. |
| SY-07 | **`sync.getAggregate` accepts `minRevision`.** It returns a canonical version at least that new, including an explicit tombstone, or an expired-history/resync response. The request is scope-checked and never exposes a pending device edit. |
| SY-08 | **Conflict replacement has a new batch identity and explicit lineage.** The original receipt is stable; an acknowledged no-content-change resolution may settle a local range without incrementing Cloud content revision. |

---

## 5.1 Cloud Notes structure, history and export operations

The typed requests use the canonical Notes schema in [the Cloud data model](../data-model/01-cloud-data-model.md#84-cloud-notes-canonical-model). The module owns folders inside a notebook and blocks inside a document. Direct HTTP, sync batches and an authorised Cloud tool invoke the same domain validator/write service; none invents a second set of mutations.

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `notes.listNotebooks` / `notes.listFolders` / `notes.getDocument` | Bounded owner-filtered hierarchy/content at an acknowledged revision | `R1` | `Q` | `state.not_found` | `AO` |
| `notes.createNotebook` / `notes.createFolder` | Caller-stable ID, notebook expected revision, nullable folder parent and sibling order | `R2` | `CC` | `conflict.revision_mismatch`, `validation.invalid_request` | `FR` |
| `notes.renameFolder` / `notes.moveFolder` / `notes.reorderFolder` | Validate notebook revision, cycle/parent and deterministic order | `R2` | `IW` | `conflict.revision_mismatch`, `validation.invalid_request` | `FR` |
| `notes.moveDocument` | Atomically validate source/destination notebook revisions and document revision; preserve document/history IDs | `R2` | `IW` | `conflict.revision_mismatch`, `state.not_found` | `FR` |
| `notes.trashFolder` / `notes.restoreFolder` | Ancestor visibility, preserving each descendant's independent trash state | `R3` | `IW` | `conflict.revision_mismatch` | `FR` |
| `notes.listRevisions` / `notes.getRevision` | Bounded immutable history including attachment references | `R1` | `Q` | `state.not_found`, `state.gone` | `AO` |
| `notes.createCheckpoint` / `notes.restoreRevision` | Named revision pin or a new current revision derived from a retained revision; never rewrite history | `R2` / `R3` | `IW` | `conflict.revision_mismatch`, `resource.unavailable` | `FR` |
| `notes.requestExport` / `chat.requestExport` | Snapshot acknowledged scope and return a bounded export-job reference | `R1` + data-export permission | `CC` | `entitlement.quota_exceeded`, `state.not_found` | `FR` |
| `export.getStatus` / `export.cancel` / `export.getDownload` | Owner-filtered progress, idempotent cancel and an expiring verified artifact | `R1` (cancel requires owning actor) | `Q` / `IW` | `state.not_found`, `resource.unavailable` | `AO` |

Structural writes return the new revisions of **all** affected roots and the immutable command receipt. A cross-notebook folder move is a bounded explicit move plan, not an unbounded recursive transaction; the V1 `moveFolder` operation stays within its notebook. A nonempty folder is not physically removed by the simple mutation API: trash changes visibility, and separately tracked retention/purge uses the deletion lifecycle. `restoreRevision` promotes a new current revision after revalidating resources and quota; old revisions remain immutable. Export manifests pin their inputs through bounded completion/retention and exclude pending local work.

## 6. Resource transfer

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `resource.beginUpload` | Server-issued upload ticket and storage key | `R2` | `CC` | `entitlement.quota_exceeded` | `FR` |
| `resource.uploadChunk` | One chunk, resumable | `R2` | `IW` | `resource.integrity_failed` | `FR` |
| `resource.completeUpload` | Verify hash/length/type and return a provisionally pinned verified object | `R2` | `IW` | `resource.integrity_failed` | `FR` |
| `resource.getDownloadTicket` | Short-lived download authorisation | `R1` | `NI` | `perm.resource_denied`, `state.not_found` | `FR` |
| `resource.getMetadata` | Size, hash, type, availability | `R1` | `Q` | `state.not_found` | `AO` |
| `resource.release` | Release one reference | `R2` | `IW` | — | `FR` |

| # | Rule |
|---|---|
| RS-01 | **The client never chooses a storage key** ([BR-10](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-br-10) of [WP-23](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23)). `beginUpload` issues it. |
| RS-02 | **Permission is checked at ticket issue and again at consumption** ([WP-23.04](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.04)). A ticket is not a bearer capability that outlives a revocation. |
| RS-03 | **`completeUpload` transitions staged to verified, never to committed.** The referencing owner transaction promotes a verified object, converts its quota reservation and adds its reference atomically. Only then is it downloadable through that owner. Completion and promotion are independently idempotent; verification alone does not publish a reference. |
| RS-04 | **A denied download returns `state.not_found`** where existence itself is sensitive ([ER-01](00-operation-catalogue.md#rule-er-01)). |

---

## 7. Task, approval and remote work

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `task.list` | Tasks across products with state and reason | `R1` | `Q` | — | `AO` |
| `task.get` | One task with its runs, steps and attempts | `R1` | `Q` | `state.not_found` | `AO` |
| `task.create` | Create a Cloud task; each Step declares its tool locality ([TO-02](../data-model/00-data-model-overview.md#rule-to-02)) | `R2`+ (the invoked capability's risk) | `CC` | `entitlement.credits_exhausted`, `perm.approval_required` | `FR` |
| `task.cancel` | Request cancellation | `R2` | `IW` | `state.invalid_transition` | `FR` |
| `task.pause` / `task.resume` | Suspend and continue | `R2` | `IW` | `state.invalid_transition` | `AC` |
| `task.retryAttempt` | Retry a failed attempt | `R2` | `NI` | `state.invalid_transition` | `FR` |
| `task.readStream` | In-progress turn output from a byte offset; `streamId` optional and resolves the current attempt | session, read on the task | `Q` | `state.not_found` | `AO` |
| `task.steer` | Adjust a running task — **grants nothing** | `R1` | `AP` | `state.invalid_transition` | `AC` |
| `approval.list` | Pending approvals | `R1` | `Q` | — | `AO` |
| `approval.decide` | Approve or reject | risk of the underlying operation; **`localPresence` where the operation requires it** | `IW` | `perm.approval_expired`, `auth.local_presence_required` | `FR` |
| `bridge.pullRequests` | **Desktop pulls** pending tool requests | device session, `R2` | `Q` | — | `FR` |
| `bridge.submitResult` | Desktop answers | device session, `R2` | `IW` | `state.invalid_transition` | `FR` |
| `bridge.getRequestState` | Requester checks queue state and expiry | `R1` | `Q` | — | `AO` |

| # | Rule |
|---|---|
| TK-01 | **`task.create` records no placement.** The field is retired: a Task is always Cloud-owned ([TO-01](../data-model/00-data-model-overview.md#rule-to-01)), the surface it came from is provenance only ([TK-04](../data-model/01-cloud-data-model.md#rule-tk-04) of the Cloud data model), and **locality is declared per Step** as `toolLocality ∈ {cloud, device}` ([TO-02](../data-model/00-data-model-overview.md#rule-to-02), [TO-06](../data-model/00-data-model-overview.md#rule-to-06)). One Task may mix both. A Step declared `device` is never silently satisfied by a cloud approximation; with no eligible device online the Task waits in `waitingDevice` and says so. |
| TK-02 | **`approval.decide` inherits the underlying operation's requirements**, including local presence. An operation needing local presence **cannot** be approved from mobile or web ([AZ-01](00-operation-catalogue.md#rule-az-01)). |
| TK-03 | **`task.steer` is an append, not an authorization.** It can never escalate ([WP-16.05](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.05)). |
| TK-04 | **`bridge.pullRequests` is the only direction.** There is no cloud-to-device push of work (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**), and no operation in this catalogue lets Cloud initiate one. |
| TK-05 | **`bridge.submitResult` is idempotent on `(taskId, attemptId)`**, so a lost response is recoverable by re-submission without duplicating the effect ([WP-26.03](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03)). |

---

### 7.1 The Task state a client is given

`task.list`, `task.get` and every realtime task event carry this set, and [STR-04](#rule-str-04) sends clients here. **These are the wire values**, matching `task.task.state` in the Cloud data model exactly. Requirements prose uses the domain spelling for the same states — `WaitingForDevice` in `§` remote task of the mobile and web requirements is this table's `waitingDevice`, not a second state ([WP-00.01](../../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01) exports the term-space mapping).

| State | Meaning to a client |
|---|---|
| `created` | Accepted and recorded; not yet queued |
| `queued` | Waiting for the Harness to pick it up |
| `running` | A turn is executing |
| `waitingApproval` | Blocked on a human decision (`approval.list`) |
| `waitingDevice` | Blocked on a `device` Step with no eligible device online ([TO-06](../data-model/00-data-model-overview.md#rule-to-06)). **Not a failure**; the client says which device is needed |
| `waitingCapacity` | Admitted but unfunded: no capacity and no authorised extra credits. Carries `recoveryAt` where capacity replenishes ([AD-03](../16-billing-and-commerce-architecture.md#rule-ad-03) of the commerce architecture). **Not a failure** |
| `paused` | Suspended by `task.pause` |
| `unknownEffect` | Dispatched with no recorded outcome. **Not terminal and not a failure**: it resolves through the ladder in `§6.4` of the harness — declared idempotency, an owner status operation, the provider's record, the deadline, or a user decision ([UR-01](../17-agent-harness.md#rule-ur-01)–[UR-04](../17-agent-harness.md#rule-ur-04)). A client presents it as *outcome not yet established*, never as done and never as failed |
| `succeeded`, `failed`, `cancelled` | Terminal |

| # | Rule |
|---|---|
| <a id="rule-ts-01"></a>TS-01 | **A client must render an unrecognised state as an unknown non-terminal state**, showing the accompanying reason text, and must never treat it as failed, terminal or absent. Clients version independently of the Cloud host ([CD-06](../22-deployment-and-release-execution.md#rule-cd-06) of the deployment architecture), so a client older than the host **will** receive a state it does not know — `waitingDevice` and `waitingCapacity` were both added to an existing enum this way. |
| TS-02 | **Only `succeeded`, `failed` and `cancelled` are terminal**, and terminality is never inferred from an unrecognised value. A client that stops polling on an unknown state strands the Task. |
| TS-03 | **`waitingDevice` and `waitingCapacity` are waiting states with a stated cause and, where one exists, a stated recovery time.** Presenting either as an error is a defect — the work is still going to happen. |

---

| # | Rule |
|---|---|
| STR-01 | `task.readStream` returns the bounded text + stream-state + authoritative Task-state contract in [Harness §7.2](../17-agent-harness.md#72-client-read-contract), including attempt, successor stream, durable output/final-message reference or no-answer reason. `truncated` is distinct from `completed`. |
| STR-02 | Stream state answers presentation availability; Task state answers execution progress. Empty/missing chunks never imply completion. Expired stream metadata falls back to Task/attempt authority, and only an existing final-message reference is fetched as an answer. |
| STR-03 | **Any replica serves any read**, because the buffer is in the shared database ([SB-04](../17-agent-harness.md#rule-sb-04)). There is no affinity requirement and no sticky routing. |
| <a id="rule-str-04"></a>STR-04 | **`evicted` does not imply the turn ended.** A client checks the Task's own state to distinguish *the answer is ready* from *live presentation was lost while work continues* ([SR-04](../17-agent-harness.md#rule-sr-04) of the harness). |
| STR-05 | **Polling with `retryAfter` is equivalent to realtime**, and a client with realtime disabled reaches identical output ([SR-01](../17-agent-harness.md#rule-sr-01) of the harness, [RE-07](03-realtime-and-bridge.md#rule-re-07)). |

---

## 8. Chat, agent and knowledge

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `chat.listConversations` | Cloud replica listing, for mobile and web | `R1` | `Q` | — | `AO` |
| `chat.getConversation` | Messages in a branch, paginated | `R1` | `Q` | `state.not_found` | `AO` |
| `chat.appendMessage` | Add a user message and optionally its linked Task atomically | `R2` | `AP` | `conflict.revision_mismatch` | `FR` |
| `chat.createBranch` | Branch from a message | `R2` | `CC` | `state.invalid_transition` | `AC` |
| `agent.listModels` | Available providers and models, with availability reasons | `R1` | `Q` | — | `AO` |
| `agent.listProfiles` | Agent profiles | `R1` | `Q` | — | `AO` |
| `agent.getUsage` | AI usage and cost with the locked tariff | `R1` | `Q` | — | `FR` |
| `search.query` | Cloud search over synced content | `R1`, entitlement-gated | `Q` | `entitlement.not_entitled` | `AO` |

| # | Rule |
|---|---|
| CH-01 | **`chat.appendMessage` atomically appends the user turn and creates its linked Task where requested**, with one retained command result. It runs no model. AI admission happens afterwards in the Harness; a refusal leaves the accepted message and a visible Task reason, not a missing Task. |
| CH-02 | **`agent.listModels` returns availability with a reason.** A withdrawn model degrades explicitly rather than vanishing ([WP-43.05](../../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05)). |
| CH-03 | **`search.query` failing never affects local search** ([WP-40.06](../../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.06)). |

---

## 9. Policy, notification and support

| Operation | Purpose | Auth | Class | Compat |
|---|---|---|---|---|
| `policy.getBundle` | The current bundle for this installation and scope | `R1` | `Q` | `FR` |
| `notification.list` | Notifications with durability class | `R1` | `Q` | `AO` |
| `notification.acknowledge` | Mark a durable item resolved | `R1` | `IW` | `AC` |
| `notification.registerPush` | Register a push token | `R2` | `IW` | `FR` |
| `notification.unregisterPush` | Remove one | `R2` | `DE` | `FR` |
| `support.createCase` | Open a case with a **diagnostic reference, never content** | `R2` | `CC` | `AC` |
| `support.listCases` / `support.appendMessage` | Case interaction | `R1` / `R2` | `Q` / `AP` | `AO` |
| `data.requestExport` | Full user-data export | `R3`, step-up | `NI` | `FR` |
| `data.getExportState` | Progress and download ticket | `R1` | `Q` | `AO` |

| # | Rule |
|---|---|
| PN-01 | **`policy.getBundle` is validated wholesale by the client and applied atomically or rejected** ([WP-44.01](../../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01)). A partially applied bundle is impossible. |
| PN-02 | **A push token is never an authorization.** `notification.registerPush` grants nothing ([PD-03](../11-mobile-architecture.md#rule-pd-03)). |
| PN-03 | **`data.requestExport` remains available with a lapsed subscription** where the data is the user's own ([BR-08](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-br-08) of [WP-46](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46)). |

---

## 9.1 ArcScope Cloud simulator

[SIM-01](../../requirements/products/arcscope.md#rule-sim-01)–[SIM-20](../../requirements/products/arcscope.md#rule-sim-20). The simulator is a **product job**, so these operations are entitlement-gated on the service term and product-resource quota, **never on AI credits** ([SIM-17](../../requirements/products/arcscope.md#rule-sim-17)).

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `simulation.listDefinitions` | The workspace's scenario definitions | `R1` | `Q` | — | `AO` |
| `simulation.getDefinition` | One definition with its versions | `R1` | `Q` | `state.not_found` | `AO` |
| `simulation.createDefinition` | Create a definition | `R2` | `CC` | `validation.failed` | `FR` |
| `simulation.publishScenarioVersion` | Freeze an **immutable** version; validates the channel schema, AST bounds and CSV reference | `R2` | `CC` | `validation.failed`, `validation.ast_bounds_exceeded` | `FR` |
| `simulation.startRun` | Start a run against a scenario version, seed and execution profile | `R2` | `CC` | `entitlement.no_service_term`, `entitlement.quota_exceeded`, `capacity.rate_limited` | `FR` |
| `simulation.pauseRun` / `simulation.resumeRun` | Pause and resume at a durable boundary | `R2` | `IW` | `state.invalid_transition` | `FR` |
| `simulation.cancelRun` | Cancel; commits a **partial** outcome | `R2` | `IW` | `state.invalid_transition` | `FR` |
| `simulation.getRun` | State, terminal reason and **complete-or-partial extent** | `R1` | `Q` | `state.not_found` | `AO` |
| `simulation.listSegments` | The authorised manifest: sequence, logical range, count, encoding, byte length, hash | `R1` | `Q` | `state.not_found` | `AO` |
| `simulation.getSegmentTicket` | A short-lived, resumable, range-capable download authorisation for one segment | `R1` | `NI` | `perm.capability_denied`, `state.gone` | `FR` |
| `simulation.pollState` | Revision- or cursor-based state and event polling | `R1` | `Q` | — | `AO` |

| # | Rule |
|---|---|
| SO-01 | **Start, pause, resume and cancel are durable, authorised, idempotent commands carrying expected state and revision** ([SIM-09](../../requirements/products/arcscope.md#rule-sim-09)). A stale command is refused; a duplicate start creates no second run and cannot resurrect a terminal run. |
| SO-02 | **`simulation.getRun` distinguishes complete from partial** ([SIM-08](../../requirements/products/arcscope.md#rule-sim-08)). A cancelled run reports `canceled` with its committed extent — never `succeeded` for an incomplete range. |
| <a id="rule-so-03"></a>SO-03 | **The manifest is the authority; the object is not.** `listSegments` returns only committed rows, and an incomplete object is invisible ([SIM-11](../../requirements/products/arcscope.md#rule-sim-11)). |
| <a id="rule-so-04"></a>SO-04 | **Bulk data never flows over realtime.** Segments are fetched by HTTP or object storage with a hash the client verifies; SignalR is an optional wakeup or preview hint ([SIM-13](../../requirements/products/arcscope.md#rule-sim-13)). |
| <a id="rule-so-05"></a>SO-05 | **Disabling realtime entirely must not reduce access to retained committed data** ([SIM-13](../../requirements/products/arcscope.md#rule-sim-13)). `pollState` plus `listSegments` is a complete authoritative fallback, and this is verified rather than assumed. |
| SO-06 | **A scenario cannot fetch a URL, read a host file or cross a workspace boundary** ([SIM-18](../../requirements/products/arcscope.md#rule-sim-18)). CSV replay reads an explicitly uploaded, workspace-owned resource identified by content hash. |
| SO-07 | **An exported scenario contains no deployment secret or policy value** ([SIM-18](../../requirements/products/arcscope.md#rule-sim-18)). |
| SO-08 | **Term expiry or suspension stops generation at a durable boundary** as `canceled` with the explicit eligibility reason; committed output then follows retained-data access rules ([SIM-17](../../requirements/products/arcscope.md#rule-sim-17)). |
| <a id="rule-so-09"></a>SO-09 | **Unauthorised or impossible requests fail before any side effect** ([SIM-16](../../requirements/products/arcscope.md#rule-sim-16)) — before a lease, before an object, before a quota debit. |

---

## 10. What is deliberately absent

| Absent | Why |
|---|---|
| Any operation that lets Cloud call a device | **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** |
| Any operation carrying a payment instrument | [CO-01](#rule-co-01) |
| Any operation that grants entitlement over the public surface | [EN-01](#rule-en-01) |
| Any operation returning a plaintext secret | [BR-04](../../planning/work-packages/11-security-foundation.md#rule-br-04) of [WP-11](../../planning/work-packages/11-security-foundation.md#rule-wp-11) — Use ≠ Reveal |
| Any operation performing a `localPresence` action remotely | [AZ-01](00-operation-catalogue.md#rule-az-01) |
| A public share-link operation | No public share links in V1 ([CS-07](../10-web-architecture.md#rule-cs-07) of the web architecture) |
| A cross-workspace query | [MT-03](../data-model/00-data-model-overview.md#rule-mt-03) — operator paths are separate and audited |
| A bulk-delete-everything operation | Destructive scope is explicit and bounded per operation |
| Any membership, invitation, role or seat operation | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — workspaces are single-owner ([WO-01](../data-model/01-cloud-data-model.md#rule-wo-01)–[WO-05](../data-model/01-cloud-data-model.md#rule-wo-05)); no collaboration-only surface exists |
| Any operation accepting a customer provider key, model endpoint or credential | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — no end-user BYOK in any form ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [EC-05](#rule-ec-05)) |
| Any operation delegating work to an external agent, agent team or sub-agent | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08)); an integration contributes tools, never a planner |
| An operation that admits AI on credit balance alone | **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — an active paid service term is the gate ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01), `entitlement.no_service_term`) |
| A client-side operation that computes admission, capacity recovery or a charge | Admission is server-side and atomic ([EC-02](#rule-ec-02), [EC-03](#rule-ec-03)) |
| An unauthenticated configuration upload or reload endpoint | [DC-11](../../requirements/11-policy-and-configuration.md#rule-dc-11) — emergency reload is operator-triggered and authenticated |

---

## 11. Verification

| # | Obligation | Where |
|---|---|---|
| PV-01 | Every operation here has a generated contract artifact, and every artifact traces to a row here | [WP-03.05](../../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05), [WP-23.00](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.00) |
| PV-02 | Every `localPresence` operation is absent from the mobile and web surfaces | [WP-31.06](../../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31.06), [WP-49.02](../../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49.02) |
| PV-03 | Every mutating operation is exactly-once under duplicate submission and lost response | [WP-23.03](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.03) |
| PV-04 | `bridge.submitResult` is idempotent on `(taskId, attemptId)` | [WP-26.03](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) |
| PV-05 | A denied resource returns `state.not_found` and discloses nothing by timing or shape | [WP-23.01](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.01) |
| PV-06 | No operation accepts a payment instrument field | [WP-42.02](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.02) scan |
| PV-07 | Entitlement operations resolve with the `commerce` schema absent | [WP-42.00](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.00) |
