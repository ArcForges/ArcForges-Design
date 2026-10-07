# Application presence stable owner and existing validation closure

This narrow amendment to [the application-presence producer decision](application-presence-epoch-and-progressive-production-2026-10-07.md) binds DEV.01 to its actual implementation and published contracts. It changes no task identifier, prerequisite, outcome, completion obligation, replay duration or permission policy.

## Stable installation partition

The private SQLite Durable Object name is `arcforges.presence.v1:` followed by lowercase SHA256 hex of the UTF-8 JSON array `[realmId, deviceId, installationId, productId]`. IDs use their canonical lowercase GUID-D spelling and the product is the existing closed installation product. This replaces the earlier realm/workspace/product/installation partition sentence only.

User, personal workspace and recovery/auth generations are not namespace selectors: a transition must meet the retained installation owner's fence rather than silently acquire a new counter. The durable row binds exact realm, device, installation, product, user and personal-workspace IDs. A different user/workspace refuses; current higher recovery/auth generations invalidate previous eligibility under the existing owner rules and retain the counter and command fences. Old authority refuses. No workspace transfer, migration/reset, membership table or permission from a hash is introduced. Fresh raw session, device/install and active single-owner workspace validation remains mandatory before every public operation and after a dispatched operation before disclosure.

## Exact existing source registration

The existing DEV.01 `DevicesModule.cs` supporting registration means the actual `Cloud:src/ArcForges.Cloud.Modules.Devices/DevicesModule.cs`. Append only its real presence service factory; preserve all existing Devices readers, participants, signatures and query registrations. The existing actual WorkspaceModule/current-owner read scope is unchanged.

## Already published shape-validation producer

Add only `ArcForges.Contracts.Validation` version `1.0.0-ci.287.1` to the existing Cloud host and its central version file. The locally available published package records Contracts source `ca45f36cccbdd31380f76b8f6cdecc958fdcb430`, Apache-2.0, and dependencies on Events/Foundation/PublicApi/Sdk.Contracts at the same 287.1 cohort, Google.Protobuf3.36.1 and Grpc.Core.Api2.84.0. Consume its actual generated method-specific validation; do not copy validators/DTOs, infer a newer schema, upgrade the whole cohort or suppress a version warning.

Supporting files are the exact central props, host project, affected generated host/Cloud.Tests/Cloud.Consumer/ArchitectureTests locks, existing licence-boundary registry if its actual checker requires an additional binding, and the already-owned immutable dependency/provenance successor. Regenerate only actually affected lock rows under the retained pins, record the evaluated closure and legal/source receipt, retain historical records and all denial gates. The existing source/project inventory support protocol applies. No npm dependency/tool change is admitted.

Actual component proof remains separate from deployment: real SQLite counter/replay/restart/overflow and signed private bridge tests plus actual generated ingress validation and current owner positives/negatives are required. Applicable CI, independent review, ordinary publication/deployment and the original C13/C11/C21/C29 completion requirements remain mandatory. Missing real authority is typed unavailable; workers.dev remains disabled and existing routes/data are preserved.
