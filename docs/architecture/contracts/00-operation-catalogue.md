# Operation Catalogue

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Contracts
> Governing authority: **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** (topology), [`../02-contracts-and-protocols.md`](../02-contracts-and-protocols.md)
> Companions: [`01-public-api-operations.md`](01-public-api-operations.md), [`02-local-rpc-operations.md`](02-local-rpc-operations.md), [`03-realtime-and-bridge.md`](03-realtime-and-bridge.md)

The contract architecture states how contracts are *shaped, versioned and generated*. This layer states **which business operations exist**. A generated OpenAPI document describes operations someone decided on; this is where they are decided.

**Why this layer exists.** Without it an implementer inventing an endpoint must also invent its authorization context, its idempotency semantics, its error set and its revision behaviour — and two implementers would invent differently. The result would be a surface that is internally inconsistent in exactly the places that matter under failure.

---

## 1. Documents in this layer

| Document | Covers |
|---|---|
| `00-operation-catalogue.md` (this) | The shared operation contract: shape, authorization, idempotency, errors, cursors, compatibility |
| [`01-public-api-operations.md`](01-public-api-operations.md) | Every cloud HTTP operation |
| [`02-local-rpc-operations.md`](02-local-rpc-operations.md) | Every same-machine RPC interface |
| [`03-realtime-and-bridge.md`](03-realtime-and-bridge.md) | Realtime events, the change feed, and the durable tool bridge |

---

## 2. The shared operation contract

Every operation on every surface — HTTP, local RPC, realtime — obeys the same seven rules. This uniformity supplies one semantic contract for retry/error/conflict behavior. C# and TypeScript have separate generated clients and language-specific adapters, verified by shared conformance vectors; they do not share a compiled client implementation.

| # | Rule |
|---|---|
| OC-01 | **An operation is a named business action**, not a resource-shaped CRUD verb. `chat.appendMessage` is an operation; "PATCH conversation" is not. The name is stable and is what appears in telemetry, audit and the command log. |
| OC-02 | **Every mutating operation carries a `CommandId`** allocated by the caller, and is exactly-once in effect ([TX-01](../data-model/00-data-model-overview.md#rule-tx-01)–[TX-06](../data-model/00-data-model-overview.md#rule-tx-06)). |
| OC-03 | **Every mutating operation on a versioned aggregate carries `expectedRev`**, and returns the resulting revision. `expectedRev = 0` means create. |
| OC-04 | **Every operation returns `ArcResult<T>`** — success with a payload, or a typed `ArcError`. Business failure is a value; transport and protocol failure is an exception (`ErrorCategory`). |
| OC-05 | **Every operation declares its authorization requirement** as a capability, a risk level and an approval posture — never "authenticated" alone. |
| OC-06 | **Every list operation is cursor-paginated** with an opaque, scope-bound cursor. |
| OC-07 | **Every operation declares its compatibility class** (`§7`), which determines what may change without a version bump. |

**Wire projection for TypeScript.** SQL/C# bigint and decimal names below describe logical values. Their public JSON representation follows [Web exact-value rules](../25-web-toolchain-and-sdk.md#31-exact-wire-values): 64-bit integers and decimals are canonical strings, int32 counters remain numbers, and null/absence are not silently conflated. Existing authentication NI exceptions remain distinct from idempotent business commands.


### 2.1 The request envelope

Every mutating request carries, in addition to its own payload:

| Field | Type | Purpose |
|---|---|---|
| `commandId` | `id` | Idempotency anchor |
| `expectedRev` | `rev?` | Optimistic concurrency; absent for non-versioned operations |
| `correlationId` | `id` | Propagated across every hop ([CR-01](../13-observability-and-operations.md#rule-cr-01)) |
| `workspaceId` | `id?` | Required for workspace-scoped operations; validated against **`workspace.owner_user_id`** ([WO-02](../data-model/01-cloud-data-model.md#rule-wo-02)). There is no membership lookup |

### 2.2 The response envelope

| Field | Type | Purpose |
|---|---|---|
| `resultRev` | `rev?` | The aggregate revision after the change |
| `entitlementVersion` | `bigint?` | Returned on any operation that could change entitlement, so a client refreshes without polling |
| `warnings` | `ReasonCode[]` | Non-fatal conditions the caller should surface — approaching quota, degraded capability, stale policy |

---

## 3. The error model

`ArcError` is already established in the implementation conventions: a stable machine `Code`, a localisation `MessageKey` (never the message), an optional non-leaking `Detail`, and a `CorrelationId`. This layer fixes the **code namespace**.

### 3.1 Code structure

`<domain>.<condition>` — lowercase, dot-separated, **stable for life** once published, because callers branch on it and stored records keep it.

### 3.2 The closed condition set

Every operation's failures map into these. An operation may not invent a condition outside this set without extending it here.

| Code | Meaning | Retryable? | Effect certainty |
|---|---|---|---|
| `auth.unauthenticated` | No valid session | No — re-authenticate | Did not happen |
| `auth.session_expired` | Session past expiry | No — refresh | Did not happen |
| `auth.step_up_required` | Operation class needs step-up | No — challenge | Did not happen |
| `auth.local_presence_required` | Risk class needs local presence | No | Did not happen |
| `perm.capability_denied` | Caller lacks the capability grant | No | Did not happen |
| `perm.resource_denied` | Capability held, this resource refused | No | Did not happen |
| `perm.egress_denied` | Read allowed, outbound transfer refused | No | Did not happen |
| `perm.approval_required` | Awaiting a human decision | No — approval flow | Did not happen |
| `perm.approval_expired` | The approval window elapsed | No — re-request | Did not happen |
| `perm.lease_expired` | A delegated capability lease ended | No | Did not happen |
| `entitlement.no_service_term` | **No active paid service term.** Returned before any capacity or credit evaluation ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01), [C-03](../../requirements/00-product-scope-and-portfolio.md#rule-c-03)) | No — subscribe, or activate a Cloud Pass. A credit balance does not resolve it | Did not happen |
| `entitlement.not_entitled` | No grant covers this capability | No — purchase or grant | Did not happen |
| `entitlement.quota_exceeded` | Quota reservation would exceed a named limit | After the stated remedy: release storage/holds, change plan, or a defined period reset; storage gauges do not reset | Did not happen |
| `entitlement.capacity_exhausted` | Included capacity is spent | **Yes, after `recoveryAt`** — the response carries a server-calculated time ([AD-05](../16-billing-and-commerce-architecture.md#rule-ad-05)) | Did not happen |
| `entitlement.extra_credits_required` | Capacity is spent and purchased credits exist, but extra usage is not authorised | No — the user must opt in with a maximum budget ([AC-06](../../requirements/04-commerce-entitlement-and-credits.md#rule-ac-06)) | Did not happen |
| `entitlement.credits_exhausted` | Authorised extra credits are also spent — a **hard stop** | No — purchase, or wait for capacity recovery | Did not happen |
| `validation.invalid_request` | Failed boundary validation | No | Did not happen |
| `validation.ast_bounds_exceeded` | Typed query/simulator AST exceeds declared structural or size bounds; reject before handler, lease, object creation or quota debit | No — reduce complexity | Did not happen |
| `identity.last_credential` | Removing this credential would leave no usable authentication credential | No — establish another usable credential first | Did not happen |
| `validation.unsupported_version` | Contract version outside the window | No | Did not happen |
| `conflict.revision_mismatch` | `expectedRev` did not match | Yes, after re-reading | Did not happen |
| `conflict.local_changes_pending` | Cloud-derived tool context cannot overwrite pending local Notes edits | Synchronise/resolve, then refresh context and authorisation | Did not happen |
| `conflict.duplicate_identifier` | Identifier already exists with different content | No | Did not happen |
| `command.reused_identifier` | Same `CommandId`, different request | No | Did not happen |
| `state.not_found` | Absent, **or present and refused** — deliberately indistinguishable | No | Did not happen |
| `state.invalid_transition` | The state machine refuses | No | Did not happen |
| `state.gone` | Existed, now tombstoned | No | Did not happen |
| `resource.unavailable` | Offline media, unreachable external reference | Yes | Did not happen |
| `resource.integrity_failed` | Hash mismatch | No | Did not happen |
| `capacity.rate_limited` | Per-identity or per-class limit | Yes, after `retryAfter` | Did not happen |
| `capacity.busy` | Exclusive resource held elsewhere | Yes | Did not happen |
| `dependency.unavailable` | A required dependency is down | Only if no effect occurred or declared idempotency/status proves replay safe | **Unknown** unless the dispatch barrier proves no effect |
| `dependency.timeout` | No answer within budget | Yes **only if idempotent** | **Unknown** |
| `provider.declined` | An upstream provider refused | Depends on the provider reason | Did not happen |
| `internal.unexpected` | Unclassified | Bounded only after idempotency/status or no-effect proof | **Unknown** |
| `validation.invalid_offset` | Stream cursor is not a returned UTF-8 boundary or exceeds the range | Re-read the declared current/reset range | Did not happen |
| `sync.cursor_expired` | Cursor/filter generation is outside retained history | Bootstrap with pending work preserved | Did not happen |
| `sync.bootstrap_expired` | Snapshot pages/pin exceeded TTL or bound | Restart bootstrap; preserve pending local work | Did not happen |
| `resource.upload_expired` | Upload/provisional pin expired | Begin a new bounded session after cleanup status | Did not happen |
| `entitlement.request_too_large` | Bound can never fit the authorised capacity/Run limit | Reduce request or explicitly authorise a feasible budget | Did not happen |
| `commerce.supplier_budget_exhausted` | Supplier exposure/remaining budget cannot admit another attempt | Operator recovery or declared budget period; uncertainty is not erased | Did not happen |
| `security.isolation_unavailable` | Required OS profile is absent or not enforceable | Repair/install a supported profile; no unsafe fallback | Did not happen |
| `resource.parser_failed` | Isolated parser crashed, timed out or returned invalid content | Only a declared safe retry or a different input | No parent-domain mutation; failed child work may have occurred |
| `media.time_not_representable` | Invalid/unrepresentable output grid or interchange precision/range | Select a supported grid or explicit reported fidelity disposition | Did not happen |
| `state.stale_fence` | A former lease owner attempted to publish | Re-read current owner/state; never replay the stale effect | Did not happen for the rejected publication |

| # | Rule |
|---|---|
| <a id="rule-er-01"></a>ER-01 | **`state.not_found` is used for both absence and refusal** where distinguishing them would let a caller enumerate what it cannot see. This is deliberate, and `Detail` carries nothing that reverses it. |
| ER-02 | **Effect certainty is part of the contract**, not an inference. A caller retrying an `unknown` failure on a non-idempotent operation is a defect the engine prevents ([WP-16.02](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.02)). |
| ER-03 | **`retryAfter` is present on every retryable capacity failure**, and clients honour it rather than choosing their own backoff. |
| ER-04 | **A new producer code is registered here before use.** Author-time operation/implementation baselines reject unregistered emitted codes. Readers remain additive-compatible: an unknown future code uses a safe generic failure display and preserves correlation/effect certainty; it is never success or an automatic retry of an unknown effect. |

---

## 4. Authorization declaration

Every operation carries this block. It is the contract's half of the security pipeline (`§12` of the security requirements); the owner-side final validation is the other half and is never skipped.

| Field | Values |
|---|---|
| `capability` | The capability key the caller must hold |
| `risk` | `R0` … `R4` |
| `approval` | `none` \| `perOperation` \| `perSession` \| `perScope` |
| `stepUp` | `no` \| `yes` |
| `localPresence` | `no` \| `yes` — `yes` makes the operation **unreachable from mobile or web** ([BR-06](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-br-06) of [WP-26](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26)) |
| `egress` | `none` \| `declared` — a separate authorization from read ([BR-05](../../planning/work-packages/11-security-foundation.md#rule-br-05) of [WP-11](../../planning/work-packages/11-security-foundation.md#rule-wp-11)) |
| `actorKinds` | Which of human, agent, automation, extension, operator, service may invoke it |

| # | Rule |
|---|---|
| <a id="rule-az-01"></a>AZ-01 | **An operation with `localPresence = yes` has no remote path at all.** It is not merely refused remotely; the remote surface does not offer it. |
| <a id="rule-az-02"></a>AZ-02 | **An operation invocable by `agent` declares it explicitly.** Absence of `agent` in `actorKinds` means an agent can never reach it, whatever capability it holds. |
| AZ-03 | **`egress = declared` operations name the destination class**, and the egress decision is recorded separately from the operation's own audit row. |

---

## 5. Idempotency and retry semantics per operation class

| Class | Example | Idempotency mechanism | Safe to auto-retry on unknown effect? |
|---|---|---|---|
| **Pure query** | `chat.getConversation` | Naturally idempotent | Yes |
| **Idempotent write** | `notes.setDocumentTitle` | `CommandId` + `expectedRev` | Yes |
| **Create with client identifier** | `notes.createDocument` | Caller-allocated id makes re-issue a no-op | Yes |
| **Append** | `chat.appendMessage` | `CommandId` — a duplicate returns the original message | Yes |
| **Non-idempotent effect** | `slate.startRender`, `scope.startCapture` | `CommandId` **plus** a live-instance constraint | **No** — surfaces a decision |
| **External side effect** | `commerce.createCheckout`, capability invocation with egress | `CommandId` **plus** provider-side idempotency where available | **No** |
| **Destructive** | `notes.purgeDocument`, `identity.revokeDevice` | `CommandId`; the second call reports already-done rather than failing | Yes — but never without the original approval |

| # | Rule |
|---|---|
| IR-01 | **Every operation declares its class.** The class determines the client's retry behaviour, and the client does not decide it locally. |
| IR-02 | **A non-idempotent operation that fails with unknown effect surfaces a decision to the user or the engine** rather than silently retrying ([WP-16.02](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.02)). |
| IR-03 | **A duplicate destructive call reports the already-done state**, so a retried delete after a lost response does not look like a failure. |

---

## 6. Cursors and pagination

| # | Rule |
|---|---|
| CP-01 | **A cursor is opaque, signed and scope-bound.** A client cannot construct or mutate one to escape its scope ([WP-23.02](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.02)). |
| CP-02 | **A cursor encodes the sort key, not an offset.** The operation declares its concurrent-mutation behavior. [Notes scalar queries](../../requirements/products/arcnotes.md#notes-scalar-query-profile) bind a dataset token and explicitly restart on a changed source set, so successful pages never silently mix revisions or duplicate/omit rows. |
| CP-03 | **A cursor carries the query shape's fingerprint.** Presenting it with different filters is rejected rather than silently reinterpreted. |
| CP-04 | **A cursor expires**, and an expired cursor returns `validation.unsupported_version` with an instruction to restart the listing — never a partial result presented as complete. |
| CP-05 | **Every list declares a maximum page size**, and a larger request is clamped with a warning rather than refused. |

---

## 7. Compatibility classes

| Class | May change without a version bump | Example |
|---|---|---|
| **Additive-open** | New optional response field; new enum member the client must tolerate | Adding `warnings` |
| **Additive-closed** | New optional request field only | Adding an optional filter |
| **Frozen** | Nothing. Any change is a new version | Anything with `localPresence`, anything financial |

| # | Rule |
|---|---|
| CC-01 | **Every operation declares its class** in the catalogue, and the contract baseline check enforces it. |
| CC-02 | **A closed enum's new member is a breaking change** unless the operation is `additive-open` **and** the client contract requires tolerating unknown members. Which enums are open is declared per enum, not assumed. |
| CC-03 | **Removing or renaming a field is always breaking**, in every class. |
| CC-04 | **Financial and security operations are `frozen`.** The cost of a subtle compatibility break there is unrecoverable. |
| CC-05 | **The supported window is bidirectional** — previous client against current server, current client against minimum server — and both directions are tested ([WP-23.06](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.06)). |

---

## 8. Which surface owns which operations

| Surface | Owns | Never carries |
|---|---|---|
| **Cloud HTTP** | Identity, workspace, device, entitlement, commerce, sync, resource transfer, cloud task, policy, notification, support | Anything requiring local presence; any local file access; realtime delivery |
| **Local RPC** | Product domain operations, capability invocation, context provision, artifact resolution, local resource access | Anything network-facing; anything Cloud initiates (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**) |
| **Realtime** | Change notification, task progress, approval arrival, presence, entitlement-changed hints | **Authoritative state**, command results, object bodies |
| **Tool bridge** | Durable remote work requests and results | Anything synchronous; anything Cloud initiates toward a device |

| # | Rule |
|---|---|
| SO-01 | **An operation appears on exactly one surface.** Where a workflow needs two, they are two operations with two names, not one operation with two transports. |
| <a id="rule-so-02"></a>SO-02 | **Realtime never carries an authoritative result** ([BR-02](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-br-02) of [WP-24](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24)). A client that needs the fact re-reads it. |
| SO-03 | **Cloud never initiates toward a device** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). The bridge is pull-and-answer. |

---

## 9. Verification

| # | Obligation | Where |
|---|---|---|
| OV-01 | Every operation in `01`–`03` declares all seven contract elements: name, class, authorization block, idempotency class, error set, compatibility class, surface | Contract baseline check ([WP-03.05](../../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.05)) |
| OV-02 | Every error an implementation returns exists in `§3.2` | [WP-23.01](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.01) |
| OV-03 | Every `localPresence = yes` operation is absent from the mobile and web client surfaces | [WP-31.06](../../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31.06), [WP-49.02](../../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49.02) |
| OV-04 | Every mutating operation is exactly-once under duplicate submission and lost response | [WP-23.03](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.03) |
| OV-05 | A forged or cross-scope cursor is refused | [WP-23.02](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.02) |
| OV-06 | The bidirectional compatibility matrix passes and catches a deliberate break | [WP-23.06](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.06) |
| OV-07 | No operation appears on two surfaces | Contract policy test |
