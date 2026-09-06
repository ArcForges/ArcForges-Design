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
| ID-02 | **`identity.refreshSession` rotates.** Presenting a superseded generation revokes the whole family and raises a security audit event — the stolen-token detection of `identity.session`. |
| ID-03 | **Account deletion never touches local data** (`ED-05`), and the response says so explicitly so the client can show it. |

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
| DV-01 | **`device.setRemoteEnabled` refuses without trust**, so remote capability can never be reached by a single mis-click (`WP-22.03`). |
| DV-02 | **`device.revoke` cascades to sessions and push registrations in one transaction**, so a revoked device cannot act during a partial cascade. |

---

## 3. Entitlement

Owned by the **Entitlement** module, independent of Commerce (`EO-01`).

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `entitlement.getSnapshot` | Effective entitlement with per-capability reasons and its version | `R1` | `Q` | — | `AO` |
| `entitlement.listGrants` | Grant history with sources | `R1` | `Q` | — | `AO` |
| `entitlement.getUsage` | Quota, usage and period boundary | `R1` | `Q` | — | `AO` |
| `entitlement.check` | Batch capability check, for a client about to offer an action | `R1` | `Q` | — | `AO` |

| # | Rule |
|---|---|
| EN-01 | **There is no public grant-issuing operation.** Grants are issued through the module API by Commerce or by an operator path, never over the public surface (`EO-03`). |
| EN-02 | **`getSnapshot` always returns `entitlementVersion`**, and clients cache against it. Realtime is a refresh hint, never authority (`ED-02`). |
| EN-03 | **`check` exists so a client can grey an action rather than offering and failing it.** It is a UX affordance; the enforcement is still server-side at the operation (`ED-04`). |

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
| CO-01 | **No operation accepts a payment instrument.** There is no card field anywhere in the surface (`PU-05`). |
| CO-02 | **`commerce.getPurchaseState` is the only thing a post-checkout redirect may call.** A redirect grants nothing (`PU-01`). |
| CO-03 | **`commerce.providerWebhook` persists before processing** and returns quickly (`EI-01`, `EI-04`). It is isolated, rate-limited and signature-gated (`SR-03`). |
| CO-04 | **`getCredits` never returns a summed balance** (`CD-06`). Allowance and purchased lots are separate fields because they expire differently. |

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
| SY-03 | **`sync.cursor_expired` instructs a full resync explicitly** rather than returning a silently incomplete delta (`WP-25.02`). |
| SY-04 | **`sync.pushChange` carries the originating `deviceId`**, so the feed can suppress a device's own echo. |
| SY-05 | **A conflict is never auto-resolved by the client.** The server applies the scope's policy; where the policy defers to the user, `listConflicts` surfaces it and the discarded version stays recoverable (`WP-25.03`). |

---

## 6. Resource transfer

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `resource.beginUpload` | Server-issued upload ticket and storage key | `R2` | `CC` | `entitlement.quota_exceeded` | `FR` |
| `resource.uploadChunk` | One chunk, resumable | `R2` | `IW` | `resource.integrity_failed` | `FR` |
| `resource.completeUpload` | Verify hash and commit | `R2` | `IW` | `resource.integrity_failed` | `FR` |
| `resource.getDownloadTicket` | Short-lived download authorisation | `R1` | `NI` | `perm.resource_denied`, `state.not_found` | `FR` |
| `resource.getMetadata` | Size, hash, type, availability | `R1` | `Q` | `state.not_found` | `AO` |
| `resource.release` | Release one reference | `R2` | `IW` | — | `FR` |

| # | Rule |
|---|---|
| RS-01 | **The client never chooses a storage key** (`BR-10` of `WP-23`). `beginUpload` issues it. |
| RS-02 | **Permission is checked at ticket issue and again at consumption** (`WP-23.04`). A ticket is not a bearer capability that outlives a revocation. |
| RS-03 | **`completeUpload` is the only transition to `committed`**, and it verifies the hash. A reference is never published before it (`XS-05`). |
| RS-04 | **A denied download returns `state.not_found`** where existence itself is sensitive (`ER-01`). |

---

## 7. Task, approval and remote work

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `task.list` | Tasks across products with state and reason | `R1` | `Q` | — | `AO` |
| `task.get` | One task with its runs, steps and attempts | `R1` | `Q` | `state.not_found` | `AO` |
| `task.create` | Create a task with an explicit placement | `R2`+ (the invoked capability's risk) | `CC` | `entitlement.credits_exhausted`, `perm.approval_required` | `FR` |
| `task.cancel` | Request cancellation | `R2` | `IW` | `state.invalid_transition` | `FR` |
| `task.pause` / `task.resume` | Suspend and continue | `R2` | `IW` | `state.invalid_transition` | `AC` |
| `task.retryAttempt` | Retry a failed attempt | `R2` | `NI` | `state.invalid_transition` | `FR` |
| `task.steer` | Adjust a running task — **grants nothing** | `R1` | `AP` | `state.invalid_transition` | `AC` |
| `approval.list` | Pending approvals | `R1` | `Q` | — | `AO` |
| `approval.decide` | Approve or reject | risk of the underlying operation; **`localPresence` where the operation requires it** | `IW` | `perm.approval_expired`, `auth.local_presence_required` | `FR` |
| `bridge.pullRequests` | **Desktop pulls** pending tool requests | device session, `R2` | `Q` | — | `FR` |
| `bridge.submitResult` | Desktop answers | device session, `R2` | `IW` | `state.invalid_transition` | `FR` |
| `bridge.getRequestState` | Requester checks queue state and expiry | `R1` | `Q` | — | `AO` |

| # | Rule |
|---|---|
| TK-01 | **`task.create` records placement once and it never changes** (`TO-06`). A `local`-declared task cannot be created with `cloud` placement. |
| TK-02 | **`approval.decide` inherits the underlying operation's requirements**, including local presence. An operation needing local presence **cannot** be approved from mobile or web (`AZ-01`). |
| TK-03 | **`task.steer` is an append, not an authorization.** It can never escalate (`WP-16.05`). |
| TK-04 | **`bridge.pullRequests` is the only direction.** There is no cloud-to-device push of work (**D-010**), and no operation in this catalogue lets Cloud initiate one. |
| TK-05 | **`bridge.submitResult` is idempotent on `(taskId, attemptId)`**, so a lost response is recoverable by re-submission without duplicating the effect (`WP-26.03`). |

---

## 8. Chat, agent and knowledge

| Operation | Purpose | Auth | Class | Key errors | Compat |
|---|---|---|---|---|---|
| `chat.listConversations` | Cloud replica listing, for mobile and web | `R1` | `Q` | — | `AO` |
| `chat.getConversation` | Messages in a branch, paginated | `R1` | `Q` | `state.not_found` | `AO` |
| `chat.appendMessage` | Add a user message | `R2` | `AP` | `entitlement.credits_exhausted` | `FR` |
| `chat.createBranch` | Branch from a message | `R2` | `CC` | `state.invalid_transition` | `AC` |
| `agent.listModels` | Available providers and models, with availability reasons | `R1` | `Q` | — | `AO` |
| `agent.listProfiles` | Agent profiles | `R1` | `Q` | — | `AO` |
| `agent.getUsage` | AI usage and cost with the locked tariff | `R1` | `Q` | — | `FR` |
| `search.query` | Cloud search over synced content | `R1`, entitlement-gated | `Q` | `entitlement.not_entitled` | `AO` |

| # | Rule |
|---|---|
| CH-01 | **`chat.appendMessage` does not run the model.** It appends the user turn and, where the profile requires it, creates a Task. Response generation is the harness's ([`../17-agent-harness.md`](../17-agent-harness.md)), reported over realtime and read back authoritatively. |
| CH-02 | **`agent.listModels` returns availability with a reason.** A withdrawn model degrades explicitly rather than vanishing (`WP-43.05`). |
| CH-03 | **`search.query` failing never affects local search** (`WP-40.06`). |

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
| PN-01 | **`policy.getBundle` is validated wholesale by the client and applied atomically or rejected** (`WP-44.01`). A partially applied bundle is impossible. |
| PN-02 | **A push token is never an authorization.** `notification.registerPush` grants nothing (`PD-03`). |
| PN-03 | **`data.requestExport` remains available with a lapsed subscription** where the data is the user's own (`BR-08` of `WP-46`). |

---

## 10. What is deliberately absent

| Absent | Why |
|---|---|
| Any operation that lets Cloud call a device | **D-010** |
| Any operation carrying a payment instrument | `CO-01` |
| Any operation that grants entitlement over the public surface | `EN-01` |
| Any operation returning a plaintext secret | `BR-04` of `WP-11` — Use ≠ Reveal |
| Any operation performing a `localPresence` action remotely | `AZ-01` |
| A public share-link operation | No public share links in V1 (`CS-07` of the web architecture) |
| A cross-workspace query | `MT-03` — operator paths are separate and audited |
| A bulk-delete-everything operation | Destructive scope is explicit and bounded per operation |

---

## 11. Verification

| # | Obligation | Where |
|---|---|---|
| PV-01 | Every operation here has a generated contract artifact, and every artifact traces to a row here | `WP-03.05`, `WP-23.00` |
| PV-02 | Every `localPresence` operation is absent from the mobile and web surfaces | `WP-31.06`, `WP-49.02` |
| PV-03 | Every mutating operation is exactly-once under duplicate submission and lost response | `WP-23.03` |
| PV-04 | `bridge.submitResult` is idempotent on `(taskId, attemptId)` | `WP-26.03` |
| PV-05 | A denied resource returns `state.not_found` and discloses nothing by timing or shape | `WP-23.01` |
| PV-06 | No operation accepts a payment instrument field | `WP-42.02` scan |
| PV-07 | Entitlement operations resolve with the `commerce` schema absent | `WP-42.00` |
