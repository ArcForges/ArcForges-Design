# Contract reuse map

Baseline: ArcForges/Contracts main `b774c322` (2026-10-11). Classes follow [reuse/inventory-and-classification.md](../reuse/inventory-and-classification.md): **Reuse** (unchanged), **Adapt** (additive changes), **Retain** (kept, unused by the flagship), **Supersede** (no longer the direction).

## 1. Reused unchanged

These **contracts** are reused unchanged. At Cloud main `92ba1dc9` most of their services have no implementation yet, so the endpoints are new work in the named tasks ([10](../architecture/10-cloud.md) §2).

| Contract | Elements | Used by |
|---|---|---|
| `arcforges.foundation.v1` | `Id`, `Revision`, `Instant`, `RequestMeta`, `ResponseMeta`, `ArcError`, `ErrorCategory`, `EffectCertainty`, `RetryMode`, `RetryAdvice`, `ErrorDetails` (+ `RevisionConflict`, `LimitFailure`, `VersionFailure`, `StateFailure`), `Receipt`, `PageRequest`, `PageState`, `AggregateRef`, `TimeRangeUtc` | Every new package |
| `arcforges.publicapi.v1.IdentityService` | Passkeys, e-mail codes, sessions, step-up (`BeginStepUp`/`CompleteStepUp`), recovery, account deletion, profile, security activity | Web Account profile; Android sign-in by Custom Tab; fleet step-up |
| `arcforges.publicapi.v1.EntitlementService` | `GetSnapshot`, `Check`, `ListGrants` | Web and Android subscription pages; the C# host's entitlement checks |
| `arcforges.publicapi.v1.CommerceService` | `GetCatalogue`, `CreateCheckoutAttempt`, `GetPurchaseState`, `GetSubscription`, `CancelSubscription`, `ReactivateSubscription`, `ListBillingHistory`, `RequestRefund` | Web checkout by redirect (Paddle) and subscription management |
| `arcforges.publicapi.v1.SupportService` | `CreateCase`, `ListCases`, `AppendMessage`, `DecideAccess` | Web Support; node bundle upload attaches to cases (the C# host links the R2 object) |
| `arcforges.publicapi.v1.NotificationService` | `List`, `Acknowledge`, `RegisterPush`, `UnregisterPush` | Android push registration; in-app notification history |
| `arcforges.publicapi.v1.DataService` | `RequestExport`, `GetExportState` | Account data export (R-OPS-004) |
| `arcforges.operator.v1.OperatorService` (internal) | Cases, consented diagnostic access, configuration staging/approval/activation, kill switches, break-glass, two-person actions, entitlement grant/revoke, compensation, refund decisions | Operations profile ([14](../architecture/14-commercial-operations.md) §1) |

## 2. Adapted (additive)

| Contract | Change | Task |
|---|---|---|
| `arcforges.publicapi.v1.DeviceService` (in `publicapi/v1/identity.proto`) | **No schema change.** `Register` already takes `product` and `platform` as strings, and `DeviceView` lists installed products. The flagship uses product values `arcforges-node` and `arcforges-mobile` (data), with one device record per node, including each WSL guest (cloud-store §2). Node details (`node_id`, role, host node) come from `fleet.v1.FleetService.ListNodes`, keyed by the same device. `Revoke` cascades to node certificates and relay tokens (behaviour). | AF-ID-02 (endpoints), AF-CLD-02 (cascade) |
| `arcforges.publicapi.v1` | New service `SupportAccessService` in a new file `support_access.proto` (`ListAccessRequests`, `GetAccessRequest`), so the owner can read an operator's access request, including its proposal hash, before deciding it with the reused `SupportService.DecideAccess`. `SupportService` is unchanged. | AF-SUP-01 |
| `arcforges.operator.v1` (internal) | New service `OperatorReadService` in a new file `operator_read.proto` (`ListAuditEvents`, `GetOperatingBudgets`, `GetMonthlyReport`); `OperatorService` is unchanged. Same C# namespace as the package (`ArcForges.Contracts.CloudInternal.Operator.V1`). | AF-OPS-01 |
| `arcforges.publicapi.v1.NotificationService` | New push kinds `node.task_failed`, `node.task_finished`, `node.approval_needed`, `node.offline`, `node.finding` (string values; no schema change) | AF-CLD-06 |
| `arcforges.publicapi.v1.EntitlementService` | Feature keys `lan.placement`, `lan.accept`, `lan.cache`, `remote.view`, `remote.control`, `push` (configuration data; no schema change) | AF-CLD-03 |

## 3. New

| Package | Notes |
|---|---|
| `arcforges.node.v1` | Replaces nothing. The retained local/desktop packages (`arcforges.local.*`, `publicapi.v1` task, workspace, policy and approval services) belong to the earlier multi-application product and are not used by the flagship. Service simple names such as `TaskService` repeat across packages, but the fully qualified gRPC names and C# namespaces differ (`ArcForges.Contracts.Node.V1` against `ArcForges.Contracts.PublicApi.V1`), so neither the wire nor generated code conflicts. Flagship code imports only `Node.V1`. |
| `arcforges.peer.v1` | New internal package |
| `arcforges.fleet.v1` | New public package. It uses Identity sessions and step-up and the Entitlement checks (reused contracts; endpoints AF-ID-01 and AF-CLD-03). |
| `arcforges.relay.v1` | New internal package. The Worker and DO adapter decode only frame headers (`frame_version`, the oneof case) and token claims. |

## 4. Retained, not used by the flagship

`publicapi.v1` chat, content, connector, scope, sync, transfer, application and descriptors; `events.v1` (`ExecutionService`, `EventService`; its `StreamPosition` shape is mirrored); `catalog.v1`; `extensions.v1`; `simulation.v1`; `hello.v1`; internal `cf.*` and `local.*`.

- **Status.** Their published packages stay published and immutable (never unpublished or deprecated by this plan).
- **Changes.** No change is planned. A later product decision may supersede them.

## 5. Conflicts

| ID | Conflict | Resolution |
|---|---|---|
| C-03 | The `ArcForges.Cli` .NET tool package (published from Contracts) declares tool command `arcforges`, which collides with the product CLI on PATH | The next `ArcForges.Cli` version renames its command to `arcforges-contracts`. Already-published versions stay immutable. Flagship installers never install the tool, and the doctor reports a PATH shadowing conflict ([reuse/conflicts.md](../reuse/conflicts.md)). |
| C-04 | The legacy `publicapi.v1` `TaskService` and `ApprovalService` share simple names with `node.v1` services | No change (different packages); documentation and import guidance only |
