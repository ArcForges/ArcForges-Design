# Protobuf Wire Registry and Cross-Language Profile

> Authoritative [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) specification. Stable operation semantics, risks, idempotency and registered errors remain in catalogues 00–03; this companion fixes the complete initial schema and encoding. [WP-03](../../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) implements these tables as handwritten proto in ArcForges-Contracts, with generated C#/TypeScript outputs. Design contains no second production .proto tree.

## 1. Ownership, names and field allocation

Public proto lives at public/proto/arcforges/{domain}/v1/*.proto, package arcforges.<domain>.v1, Apache-2.0. Foundation records use arcforges.foundation.v1. Public SDK extension protocol uses arcforges.extensions.v1 (Apache). Local first-party product/Hub proto lives internal/proto/arcforges/local/{owner}/v1, package arcforges.local.<owner>.v1, AGPL-3.0-only. Internal AI JSON schemas are separate in internal/ai-http/v1; public AI/object/browser JSON schemas in public/http/v1. Internal schemas import public definitions; reverse imports are forbidden. Cloud consumes public and CloudInternal contracts, never local product packages.

Each mapped operation below is unary. A method named M on service S has a unique SMRequest and SMResponse in that service package; request tag 1=RequestMeta, tags 2–9 reserved, method fields start at 10 as listed. Response tag 1=ResponseMeta; oneof outcome uses tag 2=SMValue and tag 3=ArcError and tag 4=EncodedBodyRef for read projections; tags 5–9 reserved; SMValue contains the listed result fields starting at 10. An empty successful result is still a present empty SMValue. Each record table fixes tags from 1 by listed order, unless #n explicitly fixes a oneof tag. CamelCase design names become lower_snake_case proto fields, with json_name set to the shown name. Do not reuse tags, removed names or operation names. Reserve removed fields immediately, including their names.

Protobuf message presence is mandatory where shown without ?. Required scalar values outside a oneof use proto optional plus validation; a oneof scalar uses the oneof presence bit, so default zero is not confused with absent input. ? means optional presence; [] repeated, empty is meaningful. Explicit null is a oneof null variant in ScalarValue/StructuredValue. Patch absent means unchanged; a nullable owner patch uses set/clear oneof, never accidental scalar defaults. RequestMeta expectedRev/expectedLocal/expectedNative are mutually exclusive and owner operation rules select the required kind. Repeated sets are normalized under their own profile; ordered lists retain their order.

No generic Invoke replaces domain services. CapabilityArguments/Result is the existing closed extension doorway only, with generated schema IDs and an immediate typed decoder. It is prohibited in domain entities. The aggregate and product records are public projections, not automatically serialized database rows. Secrets/hashes/private columns not listed never enter projection.

## 2. Exact values, canonical identity and evolution

ID bytes follow canonical UUID network ordering, never platform Guid memory layout. int64/uint64 are C# long/ulong and TS bigint; JSON projections are canonical base10 strings, never Number. Decimal uses its canonical string and checked fixed-scale arithmetic. Binary64 is allowed only for finite scientific/configuration values, bounded simulator expressions, declared extension numeric arguments and non-authoritative rankings; exact finance/Notes decimals and counters never use it. Integer measurement counts remain uint64, never double. Slate canonical positions use signed ticks at 705600000 Hz; source frame/sample rates are reduced Rational. MediaTime.rate is that canonical time base for stored edit positions; only declared ingress/egress boundaries convert it. Display conversion cannot alter owner identity or fingerprint.

Canonical semantic hashing uses versioned UTF-8 JSON with ASCII property names sorted ordinal, no insignificant whitespace, canonical exact integer/decimal strings, booleans/null literals, lower-case UUID/hash and unpadded base64url bytes, NFC only where the owner profile requires normalization. Escape strings per JSON, preserve other text scalars; reject duplicate keys, unpaired surrogate and nonfinite input. A field omitted, a field set null and an empty array have distinct meaning. Canonical command input includes operation ID, realm/workspace/actor derived by server, revision kind/value and all semantic fields, excluding requestId/correlationId/auth secrets. An existing owner canonical content format and content-origin payload hashing are unchanged; protobuf bytes are never used as a universal canonical hash.

Compatibility tests compare descriptors and independent semantic vectors, not only byte-for-byte regenerated outputs. Unknown protobuf fields are retained inert in stored/re-emitted records; older writers that cannot preserve required content-origin/profile semantics refuse mutation. Unknown response enum/error values render a safe unknown/read-only state and continue authoritative reconciliation. Unknown request enum/action/profile refuses. Financial/security FR changes require a new major service or explicit compatible migration; additive read fields preserve current and previous supported contract major for at least90 days. No existing production client is presumed deployed by this documentation task.

gRPC OK with an outcome.error is an acknowledged domain refusal/outcome; transport failures are exceptions without a fabricated ArcResult. INVALID_ARGUMENT (malformed frame/schema), UNAUTHENTICATED, PERMISSION_DENIED (transport auth), RESOURCE_EXHAUSTED (framing/admission infrastructure), UNAVAILABLE, DEADLINE_EXCEEDED and CANCELLED preserve whether dispatch might have happened. A client cancellation/timeout after sending a mutation reconciles command/result state. It never turns a transport status into didNotHappen. Domain errors retain the45-code registry and structured effect/retry data.

Independent minimum vectors: int64 9007199254740993 survives C#→TS→C#; int64 max 9223372036854775807 and uint64 max 18446744073709551615; reject overflow/leading zero/+1/1e3 for integer JSON; Decimal 0.000000001 retains nine places; UUID00112233-4455-6677-8899-aabbccddeeff encodes bytes 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff; UTF-8 A中😀 ends at offsets1/4/8; canonical command hash unchanged by proto field order but changes on explicit null or owner revision change. Reuse complete independent vectors for arcforges.content-origin.v1, notes.scalar.v1 and scope.measurement.v1, rather than replacing them with narrower wire examples.

## 3. Primitive aliases and enums


Aliases Name/Text/Email/SecretText/Key/CountryCode/Cursor/ReasonCode/Hash use proto string. Name <=256 Unicode scalars; Text <=256 KiB UTF-8; Email <=320 ASCII-normalized address bytes with display form separate; Key is case-sensitive ASCII [A-Za-z0-9._:/-]{1,128}; ModelId is a separate string alias, either Key or @cf/[a-z0-9._-]+/[a-zA-Z0-9._/-]+ with total length <=256 and exact membership in the activated model catalogue; CountryCode two uppercase ISO letters; Cursor <=4096 bytes; Hash exactly 64 lowercase hex; SecretText <=8192 bytes and never logged. Bytes = bytes <=64 KiB except explicitly specified file frames. Int32/int32, Int64/int64, UInt64/uint64 and Bool/bool are scalar aliases, not alternate encodings.
AuthMethod = passkey, email, password, oidc; AuthPurpose = authenticate, enroll, stepUp, recover, cancelDeletion. Password/OIDC require an enabled self-host provider; the official realm advertises only passkey/email.
ProtectionProfile = Standard only (retired E2EE numeric identifier2 and its name remain reserved).
TrustLevel = untrusted, trusted, revoked. ToolLocality = cloud, device.
TaskState = created, queued, running, waitingApproval, waitingDevice, waitingCapacity, paused, unknownEffect, succeeded, failed, cancelled.
EffectCertainty = didNotHappen, happened, unknown; RetryMode = never, sameCommand, afterTime, reconcile.
ApprovalDecision = approve, reject; ReconciliationDecision = retryAuthorized, acceptOwnerOutcome, abandonUnresolved; unknown external effect stays recorded when abandoned.
OpenIntent = view, edit, reveal; ResourcePurpose = attachment, export, simulatorSegment, aiOutput, diagnostic, managedAsset.
ResourceAvailability = AlwaysKeep, AvailableOffline, OnDemand, CloudOnly, MissingExternal; names are public vocabulary projections of the existing resource lifecycle, not new persistence states.
ErrorCategory = validation, authentication, authorization, entitlement, conflict, state, resource, execution, internal. Each existing code maps by its catalogue meaning; unknown future code preserves the received category for safe display. Other Key-backed vocabularies are the named closed owner-profile registries, never arbitrary code/classes; unknown response keys preserve display/read-only behavior, unknown request keys fail validation.
These named enums are proto enums: zero UNSPECIFIED (invalid request), followed by listed values starting at 1, in listed order, with a type prefix; never renumber. ReasonCode remains an open string registry to preserve additive error compatibility.

## 4. Shared record field registry

| Record | Numbered fields | Validation / semantics |
|---|---|---|
| `Id` | `1 value:bytes` | Exactly 16 bytes in canonical UUID order; nonzero; no Guid.ToByteArray layout. |
| `Revision` | `1 value:int64` | Positive committed revision; zero allowed only for an explicitly absent/new root. |
| `LocalNotesVersion` | `1 ackedRev:Revision`; `2 headLocalSeq:uint64` | Composite optimistic token, never interchangeable with Revision. |
| `NativeContentRev` | `1 value:uint64` | Product-owned content version, unrelated to Cloud revision. |
| `Instant` | `1 unixSeconds:sint64`; `2 nanos:uint32` | UTC; nanos 0..999999999; no leap second; years 0001..9999. |
| `Decimal` | `1 value:string` | Canonical exact decimal, up to 28 significant digits and 9 fractional places; per-field tighter scale/range remains binding. |
| `Rational` | `1 numerator:sint64`; `2 denominator:uint64` | Reduced, denominator positive; checked arbitrary-width intermediate arithmetic. |
| `MediaTime` | `1 ticks:sint64`; `2 rate:Rational` | Exact time-base profile in architecture 23; half-open ranges. |
| `MediaRange` | `1 start:MediaTime`; `2 duration:MediaTime` | Nonnegative duration; one compatible time base. |
| `ByteRange` | `1 offset:uint64`; `2 length:uint64` | Nonzero length, checked sum within object length; no unbounded suffix. |
| `TimeRangeUtc` | `1 from:Instant`; `2 until:Instant` | Half-open, from <= until. |
| `AggregateRef` | `1 kind:string`; `2 id:Id` | Registered aggregate kind only. |
| `ResourceRef` | `1 realmId:Id`; `2 workspaceId:Id?`; `3 ownerAppId:Key`; `4 resourceKind:Key`; `5 resourceId:Id`; `6 displayHint:Name?`; `7 availability:ResourceAvailability`; `8 holdingDeviceId:Id?` | Stable owner-scoped address, not a blob, snapshot or permission. No hash/bytes/path/credential payload. |
| `ArtifactRef` | `1 artifactId:Id`; `2 kind:Key`; `3 owner:AggregateRef`; `4 resource:ResourceRef?`; `5 jobId:Id?`; `6 origin:ContentOrigin?`; `7 producingTaskId:Id?`; `8 producingRunId:Id?`; `9 actor:ActorChain`; `10 createdAt:Instant`; `11 availability:Key`; `12 provenance:VersionedRef[]` | Owned artifact identity/provenance distinct from underlying resource; pending job has no readable final resource. |
| `Receipt` | `1 commandId:Id`; `2 resultRevision:Revision?`; `3 effect:EffectCertainty` | Commit receipt, not acknowledgement of an uncommitted downstream effect. |
| `PageRequest` | `1 cursor:Cursor?`; `2 limit:int32?` | Absent uses default 50; explicit value must be positive, maximum200 with declared clamp warning. NotesQuery uses its own default 100/max 500. No zero-as-absent coercion. |
| `PageState` | `1 nextCursor:Cursor?`; `2 hasMore:bool` | Cursor binds realm/workspace/actor/recoveryGeneration/filter/sort/schema/snapshot; 15-minute validity unless profile specifies shorter. |
| `RequestMeta` | `1 commandId:Id?`; `2 expectedRev:Revision?`; `3 correlationId:Id`; `4 workspaceId:Id?`; `5 expectedLocal:LocalNotesVersion?`; `6 expectedNative:NativeContentRev?`; `7 recoveryGeneration:uint64?` | Exactly the declared revision kind; commands require stable commandId. Cloud authenticated requests require current recoveryGeneration; bootstrap/auth flow identity supplies it before a session exists. Local-only operations omit it. |
| `ResponseMeta` | `1 resultRev:Revision?`; `2 entitlementVersion:int64?`; `3 warnings:ReasonCode[]`; `4 correlationId:Id`; `5 recoveryGeneration:uint64?` | Cloud responses expose current generation; a mismatch is a recovery boundary, never automatic mutation retry. |
| `EncodedBodyRef` | `1 resource:ResourceVersionRef`; `2 messageType:Key`; `3 descriptorHash:Hash`; `4 byteLength:uint64`; `5 snapshotToken:Cursor`; `6 expiresAt:Instant` | Exact serialized SMValue for that read operation, immutable and owner-authorized. No recursive external reply or arbitrary type activation. |
| `ArcError` | `1 code:ReasonCode`; `2 category:ErrorCategory`; `3 messageKey:Key`; `4 retry:RetryAdvice`; `5 effect:EffectCertainty`; `6 correlationId:Id`; `7 details:ErrorDetails?` | Code registry remains contracts/00; no English exception text as protocol. |
| `RetryAdvice` | `1 mode:RetryMode`; `2 retryAt:Instant?`; `3 reconciliationOperation:Key?` | No automatic retry after possible external effect unless declared safe. |
| `ErrorDetails` | `1 revision:RevisionConflict`; `2 limit:LimitFailure`; `3 upgrade:VersionFailure`; `4 state:StateFailure` | oneof; unknown variant rendered safely, not cast to success. |
| `RevisionConflict` | `1 expected:Revision?`; `2 actual:Revision?`; `3 conflictId:Id?` | Local/native conflicts carry tokens in StateFailure context, not fabricated Cloud revs. |
| `LimitFailure` | `1 limitName:Key`; `2 maximum:Decimal?`; `3 available:Decimal?`; `4 recoveryAt:Instant?` | Exact accounting quantities. |
| `VersionFailure` | `1 minReadable:Key`; `2 minWritable:Key`; `3 received:Key` | Older writers refuse without dropping unknown fields. |
| `StateFailure` | `1 state:Key`; `2 reason:ReasonCode`; `3 resource:AggregateRef?`; `4 local:LocalNotesVersion?`; `5 native:NativeContentRev?` | No owner-private row contents. |
| `InstallationClaim` | `1 installationId:Id`; `2 product:Key`; `3 platform:Key`; `4 appVersion:Key` | Server derives device trust; client cannot claim it. |
| `AuthChallenge` | `1 flowId:Id`; `2 method:AuthMethod`; `3 challenge:bytes`; `4 rpId:Key?`; `5 expiresAt:Instant`; `6 options:WebAuthnOptions?`; `7 providerId:Key?`; `8 redirectUrl:string?` | Challenge <=32 bytes; no secret in email/password challenge. OIDC redirect is generated from configured issuer plus server flow, never caller URL. |
| `WebAuthnOptions` | `1 rpId:Key`; `2 userHandle:bytes?`; `3 allowedCredentials:bytes[]`; `4 excludedCredentials:bytes[]`; `5 userVerification:Key`; `6 algorithms:sint32[]` | Only ES256 (-7), UV required; request fields follow W3C bounded WebAuthn. |
| `WebAuthnCreation` | `1 credentialId:bytes`; `2 clientDataJson:bytes`; `3 attestationObject:bytes`; `4 transports:Key[]` | Binary WebAuthn standard exception embedded as bounded bytes; total <=64 KiB, none attestation. |
| `WebAuthnAssertion` | `1 credentialId:bytes`; `2 clientDataJson:bytes`; `3 authenticatorData:bytes`; `4 signature:bytes`; `5 userHandle:bytes?` | No parsing as a generic business payload; standard verification. |
| `AuthProof` | `1 passkey:WebAuthnAssertion`; `2 emailCode:string`; `3 recoveryCode:string`; `4 password:SecretText`; `5 providerReceipt:SecretText` | oneof; 64 KiB overall; flow binds method/provider/purpose. providerReceipt is a one-use C# callback result, never an IdP token. |
| `NativeSession` | `1 sessionId:Id`; `2 accessToken:SecretText`; `3 accessExpiresAt:Instant`; `4 refreshToken:SecretText`; `5 refreshExpiresAt:Instant`; `6 device:DeviceView`; `7 recoveryGeneration:uint64`; `8 purpose:AuthPurpose` | Native route only; never returned on browser cookie authentication. |
| `SessionView` | `1 sessionId:Id`; `2 expiresAt:Instant`; `3 idleExpiresAt:Instant?`; `4 userId:Id`; `5 deviceId:Id`; `6 workspaceIds:Id[]`; `7 recoveryGeneration:uint64`; `8 purpose:AuthPurpose` | Safe browser projection; no session secret. |
| `CredentialSummary` | `1 credentialId:Id`; `2 kind:Key`; `3 displayName:Name`; `4 createdAt:Instant`; `5 lastUsedAt:Instant?` | No public key, secret or email proof hash. |
| `StepUpEvidence` | `1 operationClass:Key`; `2 expiresAt:Instant` | Server also records evidence; a client echo grants nothing. |
| `DeletionStatus` | `1 deletionId:Id`; `2 state:Key`; `3 graceEndsAt:Instant`; `4 purgeAfter:Instant?` | Commercial record retention is separate. |
| `AccountProfile` | `1 displayName:Name`; `2 avatar:ResourceVersionRef?`; `3 primaryEmail:Email?`; `4 locale:Key`; `5 timezone:Key`; `6 revision:Revision` | Owned avatar only; locale BCP47/timezone IANA; absent email permitted in self-host. |
| `ProfileUpdate` | `1 displayName:Name?`; `2 avatar:ResourceVersionRef`; `3 clearAvatar:bool`; `4 locale:Key?`; `5 timezone:Key?` | avatar/clearAvatar oneof; clearAvatar must be true. Email changes use proof flow. |
| `AuthProviderView` | `1 providerId:Key`; `2 method:AuthMethod`; `3 name:Name`; `4 enrollment:bool` | Public configured capability, no secret; provider ID is not a dynamic type name. |
| `SessionSummary` | `1 sessionId:Id`; `2 deviceId:Id`; `3 product:Key`; `4 createdAt:Instant`; `5 lastUsedAt:Instant?`; `6 expiresAt:Instant`; `7 current:bool`; `8 revision:Revision` | No credential/hash, owner only. |
| `ApiTokenView` | `1 tokenId:Id`; `2 name:Name`; `3 scopes:Key[]`; `4 workspaceId:Id`; `5 expiresAt:Instant`; `6 lastUsedAt:Instant?`; `7 revokedAt:Instant?`; `8 revision:Revision` | Explicit registered capability subset; never a master key. |
| `RecoveryCodeSet` | `1 setId:Id`; `2 codes:SecretText[]`; `3 createdAt:Instant` | Ten independent 128-bit random one-use codes, shown once only. No replayable plaintext response cache. |
| `RemoteCapabilityPolicy` | `1 deviceId:Id`; `2 allowedCapabilities:Key[]`; `3 requireLocalConfirmation:Key[]`; `4 revision:Revision` | Empty initially. Intersection with current grants/trust/remoteEnabled/owner policy; cannot authorize remote R4. |
| `SecurityActivity` | `1 eventId:Id`; `2 kind:Key`; `3 occurredAt:Instant`; `4 deviceId:Id?`; `5 actor:ActorChain`; `6 reason:ReasonCode?` | Existing audited security event classes, no content or secret. |
| `DataDeletionPreview` | `1 snapshotHash:Hash`; `2 publicationWatermark:uint64`; `3 counts:DeletionCount[]`; `4 activeJobCount:uint64`; `5 expiresAt:Instant` | Bounded counts by registered content kind; complete manifest retained server-side, no unbounded root array. |
| `DeletionCount` | `1 kind:Key`; `2 count:uint64`; `3 bytes:uint64` | At most one row per registered content kind, owner-filtered exact counters. |
| `WorkspaceHealth` | `1 workspaceId:Id`; `2 state:Key`; `3 recoveryGeneration:uint64`; `4 lastBackupAt:Instant?`; `5 storage:QuotaUsage[]`; `6 pendingJobs:Id[]`; `7 reason:ReasonCode?` | Owner-safe data health; jobs paged separately if >200, never operator internals. |
| `DataDeletionView` | `1 deletionId:Id`; `2 state:Key`; `3 counts:DeletionCount[]`; `4 createdAt:Instant`; `5 completedAt:Instant?`; `6 revision:Revision` | Workspace content purge job, identity/subscription/security/legal retention separate. |
| `DeviceSsoChallenge` | `1 flowId:Id`; `2 target:InstallationClaim`; `3 challenge:bytes`; `4 expiresAt:Instant` | 32 random bytes, 60-second one-use flow, server-bound source session/device. |
| `WorkspaceView` | `1 workspaceId:Id`; `2 ownerUserId:Id`; `3 name:Name`; `4 protection:ProtectionProfile`; `5 revision:Revision` | Only Standard profile. |
| `DeviceView` | `1 deviceId:Id`; `2 name:Name`; `3 platform:Key`; `4 trust:TrustLevel`; `5 remoteEnabled:bool`; `6 revokedAt:Instant?`; `7 presence:Key`; `8 revision:Revision` | No public key or refresh handles. |
| `InstancePresence` | `1 instanceId:Id`; `2 product:Key`; `3 capabilityVersion:Key`; `4 eligible:bool` | Heartbeat cannot elevate trust. |
| `PresenceLease` | `1 expiresAt:Instant`; `2 nextHeartbeatSeconds:int32` | Server clock authoritative. |
| `Availability` | `1 capability:Key`; `2 allowed:bool`; `3 reasons:ReasonCode[]`; `4 recoveryAt:Instant?` | Preflight, not a reservation or authorization token. |
| `EntitlementSnapshot` | `1 version:int64`; `2 capabilities:Availability[]`; `3 serviceTerm:ServiceTerm`; `4 quotas:QuotaUsage[]` | Owner-filtered immutable projection. |
| `ServiceTerm` | `1 kind:Key`; `2 startsAt:Instant`; `3 endsAt:Instant`; `4 graceEndsAt:Instant?`; `5 aiAdmissible:bool` | Preserves existing effective-term rules. |
| `Capacity` | `1 available:uint64`; `2 held:uint64`; `3 burst:uint64`; `4 recoveryRate:Rational`; `5 recoveryAt:Instant?`; `6 version:Key` | Integer microcredits; refill rational carry stays canonical server state. |
| `Grant` | `1 grantId:Id`; `2 capability:Key`; `3 source:Key`; `4 startsAt:Instant`; `5 endsAt:Instant?`; `6 revokedAt:Instant?` | No fabricated perpetual entitlement. |
| `QuotaUsage` | `1 kind:Key`; `2 used:uint64`; `3 held:uint64`; `4 limit:uint64`; `5 period:TimeRangeUtc?` | Storage/rate period semantics retained. |
| `SpendBudget` | `1 authorisationId:Id`; `2 maximum:uint64`; `3 spent:uint64`; `4 held:uint64`; `5 expiresAt:Instant`; `6 revokedAt:Instant?` | Integer microcredits, only explicit purchased-credit spending. |
| `ChargeExplanation` | `1 logicalRequestId:Id`; `2 state:Key`; `3 reason:ReasonCode?`; `4 capacityDebit:uint64`; `5 compensationDebit:uint64`; `6 purchasedDebit:uint64`; `7 tariffVersion:Key`; `8 supplierVersion:Key`; `9 attempts:AttemptCharge[]` | Three funding sources remain distinct; no supplier-secret payload. |
| `AttemptCharge` | `1 attemptId:Id`; `2 modelId:ModelId`; `3 usage:ModelUsage?`; `4 supplierCost:Decimal?`; `5 customerDebit:uint64`; `6 certainty:EffectCertainty` | USD supplier Decimal; customer debit integer microcredits; absent usage never zero. |
| `Offer` | `1 offerId:Id`; `2 priceVersion:Key`; `3 kind:Key`; `4 currency:Key`; `5 amount:Decimal`; `6 interval:Key?`; `7 entitlements:Key[]`; `8 region:CountryCode` | Tax/checkout settlement remains Paddle authority. |
| `PurchaseView` | `1 purchaseIntentId:Id`; `2 state:Key`; `3 offerId:Id`; `4 orderId:Id?`; `5 reason:ReasonCode?` | Redirect is not payment evidence. |
| `CheckoutView` | `1 checkoutAttemptId:Id`; `2 purchaseIntentId:Id`; `3 url:string`; `4 expiresAt:Instant?` | HTTPS allowlisted Paddle URL, no arbitrary return URL. |
| `SubscriptionView` | `1 subscriptionId:Id`; `2 state:Key`; `3 currentPeriod:TimeRangeUtc`; `4 cancelAtPeriodEnd:bool`; `5 revision:Revision` | Empty account uses absent success value, not invented subscription. |
| `CreditPool` | `1 available:uint64`; `2 held:uint64`; `3 lots:CreditLot[]` | Integer microcredits; included capacity is not a credit lot. |
| `CreditLot` | `1 lotId:Id`; `2 kind:Key`; `3 amount:uint64`; `4 remaining:uint64`; `5 expiresAt:Instant?`; `6 sourceOrderId:Id?` | purchased has no expiry; compensation declared expiry; original lot identity for refunds. |
| `BillingItem` | `1 itemId:Id`; `2 kind:Key`; `3 state:Key`; `4 amount:Decimal`; `5 currency:Key`; `6 occurredAt:Instant`; `7 documentUrl:string?` | Authorized provider document URL only. |
| `RefundView` | `1 refundId:Id`; `2 state:Key`; `3 paymentId:Id`; `4 amount:Decimal?`; `5 reason:ReasonCode?` | Async provider reconciliation remains authoritative. |
| `SyncScope` | `1 scopeId:Id`; `2 kind:Key`; `3 enabled:bool`; `4 exclusions:Key[]`; `5 revision:Revision` | Owner-filtered. |
| `SyncChange` | `1 root:AggregateRef`; `2 revision:Revision`; `3 schemaVersion:Key`; `4 tombstone:bool`; `5 originDeviceId:Id?`; `6 publicationSequence:uint64` | Body read through getAggregate, no hint-only content commit. |
| `ChangeProposal` | `1 root:AggregateRef`; `2 baseRev:Revision`; `3 localSequence:uint64`; `4 commandId:Id`; `5 schemaVersion:Key`; `6 body:AggregateBody`; `7 contentHash:Hash` | Per-item command identity and semantic fingerprint. |
| `ChangeReceipt` | `1 commandId:Id`; `2 accepted:AggregateView`; `3 error:ArcError` | oneof accepted/error; item result independent in pushBatch. |
| `AggregateView` | `1 root:AggregateRef`; `2 revision:Revision`; `3 schemaVersion:Key`; `4 body:AggregateBody?`; `5 tombstone:bool`; `6 contentHash:Hash` | Tombstone forbids body; unknown schema retained read-only. |
| `AggregateBody` | `1 notes:NotesDocument`; `2 chat:ConversationBody`; `3 scopeMetadata:ScopeMetadata`; `4 slateMetadata:SlateMetadata`; `5 notebook:NotebookBody`; `6 propertyDefinition:PropertyDefinition`; `7 savedView:SavedViewRecord`; `8 tag:TagRecord`; `9 agentProfile:AgentProfile`; `10 skill:SkillRecord`; `11 chatProject:ChatProjectRecord`; `12 preferences:PreferenceRecord`; `13 task:TaskSnapshot`; `14 automation:AutomationView`; `15 memory:MemoryRecord`; `16 externalBody:ResourceVersionRef` | oneof body, every field; kind selects exactly one. externalBody is a verified immutable encoded owner projection with schema/hash, not untyped JSON or an authorization bypass. |
| `ConflictView` | `1 conflictId:Id`; `2 root:AggregateRef`; `3 baseRev:Revision`; `4 currentRev:Revision`; `5 proposal:ChangeProposal`; `6 state:Key` | Authorized losing proposal preserved. |
| `ConflictResolution` | `1 choice:Key`; `2 mergedBody:AggregateBody?`; `3 sourceProposalHash:Hash` | choice keepCurrent/applyProposal/merge; merge requires body; new command/revision. |
| `BootstrapManifest` | `1 bootstrapId:Id`; `2 scopeId:Id`; `3 snapshotToken:Cursor`; `4 expiresAt:Instant`; `5 resumeCursor:Cursor` | 15-minute immutable snapshot; restart bootstrap on expiry, retain local pending work. |
| `NotebookView` | `1 notebookId:Id`; `2 name:Name`; `3 revision:Revision`; `4 trashedAt:Instant?` | Hierarchy version owns folders/order. |
| `FolderView` | `1 folderId:Id`; `2 notebookId:Id`; `3 parentId:Id?`; `4 name:Name`; `5 orderKey:string`; `6 trashedAt:Instant?`; `7 notebookRev:Revision` | Server assigns order key; beforeSiblingId is mutation input. |
| `DocumentRef` | `1 documentId:Id`; `2 notebookId:Id`; `3 folderId:Id?`; `4 revision:Revision`; `5 localVersion:LocalNotesVersion?` | Local version only on local surface. |
| `DocumentProjection` | `1 body:bool`; `2 properties:bool`; `3 links:bool` | Defaults false; explicit body opt-in within limits. |
| `DocumentView` | `1 document:DocumentRef`; `2 title:Name`; `3 body:NotesDocument?`; `4 properties:PropertyValue[]`; `5 completeness:Key`; `6 pending:bool` | Acknowledged Cloud reads never pretend to include pending local edits. |
| `RevisionView` | `1 documentId:Id`; `2 revision:Revision`; `3 createdAt:Instant`; `4 body:ResourceVersionRef`; `5 parentRev:Revision?`; `6 checkpoints:CheckpointView[]` | Immutable retained body with blob hash; authorized versioned read. |
| `CheckpointView` | `1 checkpointId:Id`; `2 revision:Revision`; `3 name:Name`; `4 createdAt:Instant` | Never edits history. |
| `ExportRequest` | `1 scope:AggregateRef[]`; `2 format:Key`; `3 includeManagedAssets:bool`; `4 acknowledgedOnly:bool` | Formats from owner export profile, <=200 roots; Cloud forces acknowledgedOnly. |
| `ExportJob` | `1 exportId:Id`; `2 state:Key`; `3 progress:int32?`; `4 snapshotRefs:VersionedRef[]`; `5 artifact:ArtifactRef?`; `6 expiresAt:Instant?`; `7 reason:ReasonCode?` | queued/running/succeeded/failed/cancelled; artifact only when verified. |
| `VersionedRef` | `1 root:AggregateRef`; `2 revision:Revision`; `3 sha256:Hash?` | Immutable source identity. |
| `TransferTicket` | `1 ticketId:Id`; `2 url:string`; `3 expiresAt:Instant`; `4 resourceId:Id`; `5 range:ByteRange?`; `6 maxPartBytes:uint32` | Opaque route to object facade; bound to current session and allowed verb; never R2 credentials. |
| `UploadTicket` | `1 uploadId:Id`; `2 resourceId:Id`; `3 ticket:TransferTicket`; `4 partBytes:uint32`; `5 uploaded:PartReceipt[]` | Initial partBytes=8 MiB, final part may be shorter. |
| `PartReceipt` | `1 partNumber:uint32`; `2 size:uint64`; `3 sha256:Hash`; `4 etag:string` | ETag opaque storage receipt, not a content hash. |
| `TaskFilter` | `1 states:TaskState[]`; `2 conversationId:Id?`; `3 created:TimeRangeUtc?` | Owner scope imposed by server. |
| `TaskSnapshot` | `1 taskId:Id`; `2 state:TaskState`; `3 reason:ReasonCode?`; `4 revision:Revision`; `5 runId:Id?`; `6 currentStreamId:Id?`; `7 finalMessage:VersionedRef?`; `8 recoveryAt:Instant?` | Only succeeded/failed/cancelled terminal. |
| `RunView` | `1 runId:Id`; `2 taskId:Id`; `3 state:Key`; `4 configVersion:Key`; `5 startedAt:Instant?`; `6 endedAt:Instant?`; `7 iteration:uint32` | No execution secret. |
| `StepView` | `1 stepId:Id`; `2 runId:Id`; `3 ordinal:uint32`; `4 capability:Key`; `5 locality:ToolLocality`; `6 state:Key`; `7 dependencies:Id[]` | DAG immutable identity. |
| `AttemptView` | `1 attemptId:Id`; `2 stepId:Id`; `3 state:Key`; `4 effect:EffectCertainty`; `5 startedAt:Instant?`; `6 endedAt:Instant?`; `7 reason:ReasonCode?` | No private model prompt. |
| `TurnInput` | `1 message:MessageDraft?`; `2 context:ContextRef[]`; `3 instructions:string?` | User-origin input only, never system authority. |
| `TurnOptions` | `1 taskId:Id`; `2 profileId:Id`; `3 maxBudget:uint64?` | Integer microcredits, cannot enlarge policy. |
| `StepSpec` | `1 stepId:Id`; `2 capability:Key`; `3 locality:ToolLocality`; `4 targetDeviceId:Id?`; `5 arguments:CapabilityArguments`; `6 dependencies:Id[]` | Arguments typed by capability descriptor; no executable code. |
| `ApprovalView` | `1 approvalId:Id`; `2 taskId:Id`; `3 proposalHash:Hash`; `4 risk:Key`; `5 state:Key`; `6 expiresAt:Instant`; `7 context:ContextRef[]` | pending/approved/rejected/expired/withdrawn, single-use bound proposal. |
| `PresenceEvidence` | `1 deviceId:Id`; `2 challengeId:Id`; `3 signature:bytes` | OS/device-side evidence bound to proposal; browser/RN cannot fabricate local desktop presence. |
| `ToolRequest` | `1 toolRequestId:Id`; `2 taskId:Id`; `3 runId:Id`; `4 stepId:Id`; `5 attemptId:Id`; `6 commandId:Id`; `7 targetDeviceId:Id`; `8 capability:Key`; `9 arguments:CapabilityArguments`; `10 context:ContextRef[]`; `11 actor:ActorChain`; `12 approvalId:Id?`; `13 expiresAt:Instant`; `14 state:Key` | queued/delivered/answered/expired/refused; sender never selects effective actor. |
| `ToolResult` | `1 invocationId:Id`; `2 effect:EffectCertainty`; `3 success:CapabilityResult`; `4 error:ArcError`; `5 artifacts:ArtifactRef[]` | oneof success/error; command/effect receipt bound to owner. |
| `ConversationView` | `1 conversationId:Id`; `2 branchId:Id`; `3 title:Name`; `4 revision:Revision`; `5 lastMessageAt:Instant?` | Immutable branch ancestry. |
| `MessageDraft` | `1 parts:MessagePart[]`; `2 context:ContextRef[]` | User role enforced by operation, <=256 KiB inline. |
| `MessagePart` | `1 text:string`; `2 resource:ResourceRef`; `3 toolProposal:ToolProposal`; `4 toolResult:ToolResult`; `5 origin:ContentOrigin?` | oneof content; untrusted client cannot submit assistant/tool role. |
| `MessageView` | `1 messageId:Id`; `2 conversationId:Id`; `3 branchId:Id`; `4 role:Key`; `5 parts:MessagePart[]`; `6 state:Key`; `7 revision:Revision`; `8 taskId:Id?` | complete/interrupted semantics and content-origin.v1 retained. |
| `ModelView` | `1 modelId:ModelId`; `2 supplier:Key`; `3 contextTokens:uint32`; `4 outputTokens:uint32`; `5 capabilities:Key[]`; `6 availability:Availability` | Only selected Workers AI IDs. ASR reports contextTokens=0/outputTokens=0 and capability audio.transcribe; those zeros mean inapplicable token limits, never missing model admission bounds. |
| `AgentProfile` | `1 profileId:Id`; `2 name:Name`; `3 modelId:ModelId`; `4 instructions:Text`; `5 skillIds:Id[]`; `6 revision:Revision`; `7 context:ContextRef[]`; `8 capabilities:Key[]` | Declarative capability preferences confer no permission; models restricted to the effective CF catalogue. |
| `ModelUsage` | `1 inputTokens:uint64?`; `2 outputTokens:uint64?`; `3 cachedInputTokens:uint64?`; `4 measuredAt:Instant`; `5 source:Key`; `6 audioMilliseconds:uint64?` | Absent is unknown, never zero. Audio units use the selected metering profile and source receipt, not token estimates. |
| `SearchHit` | `1 source:VersionedRef`; `2 title:Name`; `3 excerpt:string?`; `4 score:double?`; `5 citation:ContextRef`; `6 properties:PropertyValue[]` | Finite score only; permission before counts/results. |
| `NotesDataset` | `1 profile:Key`; `2 token:Cursor`; `3 scope:Key`; `4 completeness:Key`; `5 pending:bool` | notes.scalar.v1 ordering and pinned dataset semantics. |
| `PolicyBundle` | `1 version:Key`; `2 issuedAt:Instant`; `3 expiresAt:Instant`; `4 body:bytes`; `5 signature:bytes`; `6 keyId:Key` | Canonical signed bounded policy format, no credentials/private tariffs. |
| `NotificationView` | `1 notificationId:Id`; `2 kind:Key`; `3 durability:Key`; `4 messageKey:Key`; `5 target:AggregateRef?`; `6 state:Key`; `7 createdAt:Instant` | Hints do not replace durable notification rows. |
| `SupportCase` | `1 caseId:Id`; `2 subject:Name`; `3 state:Key`; `4 messages:SupportMessage[]`; `5 revision:Revision`; `6 category:Key`; `7 relatedActionId:Id?`; `8 messagePage:PageState?` | support/bug/communityReport/appeal/security; authorized owner only, messages paginated; state transitions remain Support/TrustSafety-owned. |
| `SupportMessage` | `1 messageId:Id`; `2 actorKind:Key`; `3 text:string`; `4 createdAt:Instant`; `5 diagnostic:ResourceRef?` | Explicit support text, no auto-uploaded document/prompt body. |
| `SimulationDefinition` | `1 definitionId:Id`; `2 name:Name`; `3 revision:Revision` | Scenario versions immutable. |
| `ScenarioVersion` | `1 scenarioVersionId:Id`; `2 definitionId:Id`; `3 schemaVersion:Key`; `4 scenario:ScenarioSpec`; `5 sha256:Hash` | AST/channel constraints architecture23. |
| `SimulationRun` | `1 runId:Id`; `2 scenarioVersionId:Id`; `3 state:Key`; `4 reason:ReasonCode?`; `5 revision:Revision`; `6 committedSequence:int64`; `7 extent:Key`; `8 logicalEnd:uint64` | canceled spelling belongs to simulator; complete/partial explicit. |
| `SimulationSegment` | `1 runId:Id`; `2 sequence:int64`; `3 start:uint64`; `4 count:uint64`; `5 encoding:Key`; `6 resource:ResourceVersionRef`; `7 events:ResourceVersionRef?`; `8 executionProfile:Key` | Manifest includes immutable blob hash/length via resource; only committed entries readable. |
| `SimulationProfile` | `1 sampleCount:uint64`; `2 batchSamples:uint32`; `3 rate:Rational`; `4 executionProfile:Key`; `5 encodingProfile:Key`; `6 clockMode:Key`; `7 generatorVersion:Key` | af-sim.v1/af-segment.v1; realTime/accelerated; default batch4096, max 65536; finite bounded requested range. |
| `AutomationSpec` | `1 name:Name`; `2 trigger:TriggerSpec`; `3 input:TurnInput`; `4 profileId:Id`; `5 perRunBudget:uint64`; `6 periodBudget:uint64`; `7 budgetPeriod:TimeRangeUtc`; `8 concurrency:Key`; `9 misfire:Key`; `10 catchUpCount:uint32`; `11 catchUpWindowSeconds:uint32`; `12 grants:Id[]`; `13 targetDeviceId:Id?` | Integer microcredits; preserve trigger families and grants; SkipIfRunning/RunOnceWhenAvailable defaults. |
| `ScheduleSpec` | `1 kind:Key`; `2 expression:string`; `3 zone:string`; `4 startsAt:Instant`; `5 endsAt:Instant?`; `6 dstGap:Key`; `7 dstOverlap:Key` | once/cron/interval; IANA zone, gap skip, overlap earlier default; explicit later/both supported. |
| `AutomationView` | `1 automationId:Id`; `2 definition:AutomationSpec`; `3 enabled:bool`; `4 revision:Revision`; `5 nextOccurrence:Instant?` | One occurrence identity per definition revision/scheduled UTC instant. |
| `ContextRef` | `1 source:AggregateRef`; `2 revision:Revision?`; `3 resource:ResourceRef?`; `4 selector:string?`; `5 origin:ContentOrigin?` | Owner-defined bounded selector, not SQL/path/code. |
| `ActorChain` | `1 initiator:Id`; `2 owner:Id`; `3 actorKind:Key`; `4 delegationId:Id?`; `5 deviceId:Id?` | Validated provenance, never trusted from arbitrary client claims. |
| `ToolProposal` | `1 proposalId:Id`; `2 capability:Key`; `3 arguments:CapabilityArguments`; `4 sourceAttemptId:Id` | Model proposal grants no permission. |
| `Registration` | `1 appId:Key`; `2 installationId:Id`; `3 instanceId:Id`; `4 version:Key`; `5 contracts:Key[]`; `6 capabilities:CapabilityDescriptor[]`; `7 contributions:Contribution[]`; `8 endpoint:LocalEndpoint` | Bound to OS peer identity, not self-asserted executable path. |
| `LocalEndpoint` | `1 transport:Key`; `2 address:string`; `3 instanceId:Id` | pipe/uds only, derived private namespace; never network host. |
| `LocalLease` | `1 leaseId:Id`; `2 expiresAt:Instant`; `3 renewAfterSeconds:uint32`; `4 negotiatedContracts:Key[]` | 30-second lease, renew every 10 seconds. |
| `HealthReport` | `1 appId:Key`; `2 instanceId:Id`; `3 status:Key`; `4 reasons:ReasonCode[]`; `5 observedAt:Instant` | No content, process secrets or unbounded stack traces. |
| `ResolutionContext` | `1 owner:AggregateRef?`; `2 preferredInstanceId:Id?`; `3 resourceId:Id?` | Affinity owner overrides user preference where required. |
| `CapabilityBinding` | `1 capability:Key`; `2 instanceId:Id`; `3 endpoint:LocalEndpoint`; `4 leaseId:Id`; `5 contractVersion:Key`; `6 reasons:ReasonCode[]` | Resolve only, caller then directly invokes provider. |
| `ContributionFilter` | `1 kind:Key?`; `2 capability:Key?`; `3 appId:Key?` | Bounded query. |
| `Contribution` | `1 contributionId:Key`; `2 kind:Key`; `3 titleKey:Key`; `4 capability:Key?`; `5 pattern:string?`; `6 schemaId:Key?` | Only registered action/context/artifact/deeplink/extension point kinds. |
| `CapabilityDescriptor` | `1 key:Key`; `2 version:Key`; `3 requestSchema:Key`; `4 responseSchema:Key`; `5 risk:Key`; `6 locality:ToolLocality`; `7 idempotency:Key`; `8 statusOperation:Key?`; `9 reads:Key[]`; `10 writes:Key[]`; `11 exclusive:bool`; `12 egress:Key`; `13 approval:Key` | External effect requires declared idempotency or status; generated first-party input/output schemas. |
| `FrozenContext` | `1 sources:ContextRef[]`; `2 actor:ActorChain`; `3 profileVersion:Key`; `4 permissionsVersion:Key` | Snapshot is evidence, not a grant. |
| `Invocation` | `1 invocationId:Id`; `2 commandId:Id`; `3 capability:Key`; `4 context:FrozenContext`; `5 arguments:CapabilityArguments`; `6 approvalId:Id?`; `7 leaseId:Id?`; `8 expectedRev:Revision?`; `9 expectedLocal:LocalNotesVersion?`; `10 expectedNative:NativeContentRev?` | One precondition kind, owner rechecks all evidence. |
| `CapabilityArguments` | `1 schemaId:Key`; `2 value:StructuredValue` | Only declared boundary gateway; first-party decoder immediately produces method-specific request. |
| `CapabilityResult` | `1 schemaId:Key`; `2 value:StructuredValue` | Validate output before delivery. |
| `StructuredValue` | `1 null:bool`; `2 boolean:bool`; `3 integer:sint64`; `4 decimal:Decimal`; `5 text:string`; `6 instant:Instant`; `7 resource:ResourceRef`; `8 list:ValueList`; `9 record:ValueRecord`; `10 number:double` | oneof value, every field; finite number only for schemas declaring binary64. Exact accounting never goes through number. |
| `ValueList` | `1 items:StructuredValue[]` | At most 200 items, depth <=16. |
| `ValueRecord` | `1 entries:ValueEntry[]` | Unique ASCII keys sorted ordinal, <=200; schema rejects unknown keys unless explicitly declared. |
| `ValueEntry` | `1 name:Key`; `2 value:StructuredValue` | No duplicate keys. |
| `ContextRequest` | `1 kind:Key`; `2 selector:ContextRef`; `3 maxItems:uint32`; `4 maxBytes:uint32` | Defaults 50/65536, max 200/262144; never raw capture or full media. |
| `ContextContribution` | `1 sources:ContextRef[]`; `2 items:ContextItem[]`; `3 truncated:bool`; `4 reasons:ReasonCode[]` | content-origin and permission applied before counts. |
| `ContextItem` | `1 source:ContextRef`; `2 text:string?`; `3 measurement:MeasurementResult?`; `4 timeline:TimelineView?` | Exactly one content projection, never raw object body. |
| `PreviewRequest` | `1 maxWidth:uint32`; `2 maxHeight:uint32`; `3 page:uint32?` | Dimension <=4096, helper output pixel bound remains tighter. |
| `TransferRequest` | `1 resourceId:Id`; `2 destinationInstanceId:Id`; `3 range:ByteRange?` | Requires owner and receiving-peer grants. |
| `ProductState` | `1 instanceId:Id`; `2 state:Key`; `3 dirtyRoots:AggregateRef[]`; `4 jobs:ProductJobRef[]` | Bounded; shutdown may refuse to lose pending work. |
| `ProductJobRef` | `1 jobId:Id`; `2 kind:Key`; `3 state:Key`; `4 ownerInstanceId:Id`; `5 progress:uint32?`; `6 artifact:ArtifactRef?`; `7 reason:ReasonCode?` | Native job persisted by product; no AI debit or Cloud Task identity. |
| `Block` | `1 blockId:Id`; `2 parentId:Id?`; `3 orderKey:string`; `4 kind:Key`; `5 body:BlockBody`; `6 origin:ContentOrigin?`; `7 properties:BlockProperties?` | Accepted registered Notes kinds only; properties validated by kind; hierarchy uses stable IDs. |
| `BlockBody` | `1 text:RichText`; `2 code:CodeBlock`; `3 resource:ResourceRef`; `4 link:LinkSpec`; `5 table:TableBlock`; `6 math:MathContent`; `7 empty:bool` | oneof content, every field. Divider uses empty=true; no arbitrary editor JSON. |
| `RichText` | `1 text:string`; `2 spans:TextSpan[]`; `3 atoms:InlineAtom[]` | NFC UTF-8 <=256 KiB; offsets are UTF-16 code units in this text, never inside a surrogate pair. Each atom occupies one U+FFFC. Lossless transport projection of owner InlineContent, not a replacement storage model. |
| `TextSpan` | `1 from:uint32`; `2 until:uint32`; `3 marks:Key[]`; `4 link:LinkSpec?`; `5 origin:ContentOrigin?` | Half-open UTF-16 boundaries. Marks: bold/italic/strikethrough/underline/code/superscript/subscript and highlight:<colorToken>/textColor:<colorToken> from the design-system token set. No executable markup; origin retains its independent content-origin profile. |
| `CodeBlock` | `1 text:string`; `2 language:Key?`; `3 wrap:bool` | Plain text only; optional languageId and explicit wrap, no marks or execution. |
| `TableBlock` | `1 rows:TableRow[]` | <=200 rows/200 cells total per mutation; no formulas. |
| `TableRow` | `1 rowId:Id`; `2 cells:RichText[]` | Deterministic cell order. |
| `BlockEdit` | `1 insert:Block`; `2 replace:Block`; `3 remove:Id`; `4 move:BlockMove` | oneof; batch validates whole root before commit. |
| `BlockMove` | `1 blockId:Id`; `2 parentId:Id?`; `3 beforeSiblingId:Id?` | No cycles. |
| `LinkSpec` | `1 kind:Key`; `2 targetId:Id?`; `3 url:string?`; `4 label:string?` | Internal or external, exactly one target, validate supported schemes. |
| `PropertyValue` | `1 propertyId:Id`; `2 value:ScalarValue` | notes.scalar.v1 definitions decide allowed kind, null/missing and normalization. |
| `ScalarValue` | `1 null:bool`; `2 text:string`; `3 boolean:bool`; `4 number:Decimal`; `5 date:string`; `6 select:Id`; `7 multiSelect:IdList`; `8 dateTime:Instant`; `9 url:string` | oneof value, every field. null sentinel true represents missing stored value, invalid predicate literal. dateTime nanos multiple100; canonical owner JSON UTC seven digits; URL remains unfetched ordinal text. |
| `IdList` | `1 items:Id[]` | Set semantics only where owner profile says so. |
| `NotesQuery` | `1 profile:Key`; `2 notebookId:Id`; `3 savedViewId:Id?`; `4 savedViewRev:Revision?`; `5 filter:NotesFilter?`; `6 sorts:NotesSort[]`; `7 projection:Id[]`; `8 page:PageRequest`; `9 datasetToken:Cursor?`; `10 definitionVersions:PropertyDefinitionVersion[]`; `11 selectors:NotesSelectors?` | notes.scalar.v1; default 100/max 500 page,8 sort/64 projection,128 total AST nodes/depth8/query64 KiB; profile overrides generic page maximum. Failed cursor/profile never returns partial success. |
| `NotesFilter` | `1 group:FilterGroup`; `2 predicate:ScalarPredicate` | oneof expression={group,predicate}; total128 nodes/depth8, not a separate64-predicate cap. |
| `FilterGroup` | `1 operator:Key`; `2 children:NotesFilter[]` | all/any have1..32 children; not exactly 1. No and/or aliases. |
| `ScalarPredicate` | `1 propertyId:Id`; `2 operator:Key`; `3 operands:ScalarValue[]` | Operator/operand arity follows notes.scalar.v1; invalid type is error, not false. |
| `NotesSort` | `1 propertyId:Id`; `2 descending:bool` | Stable document UUID final tie-break. |
| `PropertyDefinitionVersion` | `1 propertyId:Id`; `2 semanticRevision:Revision` | Reject stale definition, never reinterpret stored values. |
| `NotesDocument` | `1 documentId:Id`; `2 notebookId:Id`; `3 folderId:Id?`; `4 title:Name`; `5 blocks:Block[]`; `6 properties:PropertyValue[]`; `7 tags:Id[]`; `8 links:LinkSpec[]`; `9 origin:ContentOrigin?` | Owner revision and local pending layers remain separate. |
| `ConversationBody` | `1 conversation:ConversationView`; `2 messages:MessageView[]` | Immutable messages/branches, no streaming projection. |
| `ScopeMetadata` | `1 sessionId:Id`; `2 name:Name`; `3 captures:CaptureMetadata[]`; `4 annotations:ScopeAnnotation[]`; `5 findings:ScopeFinding[]`; `6 projectId:Id`; `7 configuration:ScopeConfiguration`; `8 analyses:ResourceVersionRef[]`; `9 reports:ArtifactRef[]`; `10 tags:Id[]`; `11 metadata:MetadataEntry[]` | Metadata sync never uploads raw bytes; finite typed custom metadata only, no host paths. |
| `CaptureMetadata` | `1 captureId:Id`; `2 sampleCount:uint64`; `3 channels:ChannelDefinition[]`; `4 contentHash:Hash?`; `5 resource:ResourceRef?` | Metadata replica, Resource only after consent and commit. |
| `ScopeAnnotation` | `1 annotationId:Id`; `2 range:SampleRange`; `3 text:string`; `4 origin:ContentOrigin?` | Original measurement/source preserved. |
| `ScopeFinding` | `1 findingId:Id`; `2 result:ResourceVersionRef`; `3 text:string`; `4 origin:ContentOrigin?`; `5 severity:Key`; `6 status:Key`; `7 evidence:ContextRef[]`; `8 actor:ActorChain` | info/warning/critical; open/accepted/dismissed; actor derived by owner; AI narrative never becomes measurement. |
| `SlateMetadata` | `1 projectId:Id`; `2 name:Name`; `3 sequences:SequenceView[]`; `4 media:MediaView[]`; `5 timelines:TimelineView[]`; `6 bins:MediaBin[]`; `7 presets:RenderPreset[]`; `8 transcripts:ResourceVersionRef[]`; `9 smallAssets:ResourceVersionRef[]`; `10 contentRev:NativeContentRev`; `11 profile:Key` | slate.project.v1 complete metadata snapshot. Every sequence has one matching full timeline; originals/external paths, caches and editor UI state excluded. Resource refs preserve explicit availability and upload consent. |
| `ScopeSession` | `1 sessionId:Id`; `2 name:Name`; `3 revision:NativeContentRev`; `4 configuration:ScopeConfiguration`; `5 captures:CaptureMetadata[]` | Frozen configuration per capture. |
| `ScopeConfiguration` | `1 configurationId:Id`; `2 channels:ChannelDefinition[]`; `3 parserProfile:Key`; `4 revision:NativeContentRev` | Typed parser configuration profile, no arbitrary executable expressions. |
| `ChannelDefinition` | `1 channelId:Id`; `2 name:Name`; `3 unit:Key`; `4 sampleType:Key`; `5 rate:Rational`; `6 calibration:Calibration?` | Samples exact under scope.measurement.v1. |
| `Calibration` | `1 scale:double`; `2 offset:double`; `3 unit:Key` | Finite coefficients, immutable input revision. |
| `CaptureView` | `1 captureId:Id`; `2 sessionId:Id`; `3 state:Key`; `4 sampleCount:uint64`; `5 configuration:ScopeConfiguration`; `6 resource:ResourceRef?` | Incomplete capture marked partial. |
| `SampleRange` | `1 from:uint64`; `2 count:uint64` | Half-open checked range. |
| `MeasurementRequest` | `1 profile:Key`; `2 source:MeasurementSource`; `3 sourceRevision:NativeContentRev`; `4 channels:Id[]`; `5 window:MeasurementWindow`; `6 families:Key[]`; `7 thresholds:MeasurementThreshold[]`; `8 configuration:ScopeConfiguration`; `9 alignment:AlignmentSpec`; `10 cursors:CursorSpec[]`; `11 referenceLevels:MeasurementThreshold[]` | scope.measurement.v1 verbatim; source revision/hash/channel/config match; no raw bytes in context. Optional pulse defaults resolved and returned, not implicit output. |
| `MeasurementThreshold` | `1 family:Key`; `2 name:Key`; `3 value:double`; `4 unit:Key` | Finite, declared per-family names and bounds only. |
| `MeasurementResult` | `1 profile:Key`; `2 inputHash:Hash`; `3 families:FamilyResult[]`; `4 warnings:ReasonCode[]`; `5 configuration:ScopeConfiguration`; `6 finiteCount:uint64`; `7 excludedCount:uint64`; `8 runCount:uint64`; `9 requestedDuration:ScopeTime`; `10 coveredDuration:ScopeTime`; `11 timingUncertainty:ScopeTime`; `12 source:MeasurementSource`; `13 resolvedThresholds:MeasurementThreshold[]`; `14 cursor:CursorResult?` | Per-channel results; all counts exact, family statuses/tolerance/profile preserved. Source bindings survive reporting/rebuild. |
| `FamilyResult` | `1 family:Key`; `2 status:Key`; `3 values:MeasurementValue[]`; `4 validCount:uint64`; `5 invalidCount:uint64`; `6 reason:ReasonCode?`; `7 channelId:Id` | ok/insufficient/invalid; missing values on insufficiency; integer count/eventCount use count variant. |
| `MeasurementValue` | `1 name:Key`; `2 value:double`; `3 unit:Key`; `4 count:uint64` | oneof result={value,count}; no NaN/Infinity; count/eventCount are exact uint64. |
| `AnalysisRequest` | `1 measurement:MeasurementRequest`; `2 analysisKind:Key` | Accepted analysis algorithms only. |
| `CompareRequest` | `1 left:MeasurementRequest`; `2 right:MeasurementRequest` | Compatibility/unit alignment required before comparison. |
| `ReportRequest` | `1 sources:ResourceVersionRef[]`; `2 format:Key`; `3 title:Name` | Immutable measured inputs with source/profile hashes, explicit output. |
| `CaptureRequest` | `1 sessionId:Id`; `2 deviceId:Key`; `3 configuration:ScopeConfiguration`; `4 maxSamples:uint64?` | No remote arbitrary hardware control. |
| `SlateProject` | `1 projectId:Id`; `2 name:Name`; `3 revision:NativeContentRev` | Independent product working store. |
| `SequenceView` | `1 sequenceId:Id`; `2 projectId:Id`; `3 name:Name`; `4 revision:NativeContentRev`; `5 duration:MediaTime`; `6 videoRate:Rational`; `7 sampleRate:uint32`; `8 width:uint32`; `9 height:uint32`; `10 channelLayout:Key`; `11 colour:ColourConfiguration` | Exact sequence output grids and render semantics, never inferred from source or current device defaults. |
| `MediaView` | `1 mediaId:Id`; `2 source:ResourceRef?`; `3 availability:ResourceAvailability`; `4 duration:MediaTime?`; `5 streams:MediaStream[]` | External source path local-only, never exposed through Cloud/RPC. |
| `MediaStream` | `1 index:uint32`; `2 kind:Key`; `3 codec:Key`; `4 rate:Rational?`; `5 channels:uint32?` | Metadata verified in isolated helper. |
| `TimelineView` | `1 sequence:SequenceView`; `2 tracks:TimelineTrack[]`; `3 markers:MarkerView[]`; `4 graph:ProcessingGraph` | Full metadata snapshot or explicitly requested range; encodedBody handles large reads. Sequence graph scope is sequence time. |
| `TimelineTrack` | `1 trackId:Id`; `2 kind:Key`; `3 order:uint32`; `4 clips:TimelineClip[]`; `5 transitions:TransitionSpec[]`; `6 enabled:bool`; `7 name:Name`; `8 locked:bool`; `9 graph:ProcessingGraph` | video/audio/subtitle; graph scope sequence time. Subtitle is an independent role; ordered positive-duration half-open items. |
| `TimelineClip` | `1 clipId:Id`; `2 mediaId:Id?`; `3 timeline:MediaRange`; `4 source:MediaRange?`; `5 playbackRate:Rational`; `6 effects:EffectSpec[]`; `7 origin:ContentOrigin?`; `8 kind:Key`; `9 enabled:bool`; `10 nestedSequenceId:Id?`; `11 generated:GeneratedSource?`; `12 text:TimedText?`; `13 graph:ProcessingGraph`; `14 name:Name` | clip/gap/title/subtitleCue/generatedMedia/nestedSequence/adjustment. kind fixes exactly the applicable payload; title requires generated.kind=title/text and omits item.text, subtitleCue requires item.text and omits generated; media/source only for a media clip, nested sequence same project and acyclic. effects is a derived stack projection of graph nodes (empty for a non-stack graph), never a second owner; inconsistent nonempty projections refuse. |
| `EffectSpec` | `1 kind:Key`; `2 parameters:EffectParameter[]`; `3 instanceId:Id`; `4 definitionVersion:Key`; `5 scope:Key`; `6 enabled:bool`; `7 retainedDefinition:Bytes?` | Registered definition separate from instance; scope clipLocal/sequence. Unknown imported definition is preserved inert/bypassed, cannot be newly invoked as an arbitrary kind. |
| `EffectParameter` | `1 name:Key`; `2 decimal:Decimal`; `3 boolean:bool`; `4 text:string`; `5 keyframes:KeyframeList`; `6 rational:Rational` | oneof value={decimal,boolean,text,keyframes,rational}; exact type from definition. Rational is used for generator rate; unknown name/type refuses. |
| `MarkerView` | `1 markerId:Id`; `2 sequenceId:Id`; `3 range:MediaRange`; `4 label:string`; `5 origin:ContentOrigin?` | Exact range/provenance. |
| `TimelineEdit` | `1 insert:ClipPlacement`; `2 remove:Id`; `3 replace:ClipPlacement`; `4 track:TimelineTrack` | oneof edit, every field; remove is clip ID, track replaces that track; moving a clip atomically removes old placement. ExpectedNative guards whole sequence; no partial application. |
| `RenderRequest` | `1 sequenceId:Id`; `2 revision:NativeContentRev`; `3 range:MediaRange`; `4 preset:RenderPreset`; `5 destination:ResourceRef?` | Product reserves immutable render snapshot; output location brokered. |
| `RenderPreset` | `1 container:Key`; `2 videoCodec:Key?`; `3 audioCodec:Key?`; `4 width:uint32?`; `5 height:uint32?`; `6 rate:Rational?`; `7 colourSpace:Key`; `8 sampleRate:uint32?`; `9 channelLayout:Key?`; `10 profile:Key`; `11 audioBitrate:uint32?`; `12 videoBitrate:uint64?`; `13 subtitleMode:Key` | Selected render profile; subtitleMode none/burnIn/sidecar, reviewed before render. No arbitrary encoder flags or silent substitution. |
| `OtioImportRequest` | `1 resource:ResourceVersionRef`; `2 projectId:Id`; `3 sequenceId:Id`; `4 acceptedLosses:Key[]` | Preview and commit bind exact input hash/profile and accepted loss entries. |
| `OtioExportRequest` | `1 artifactId:Id`; `2 profile:Key`; `3 acceptLossy:bool` | otio-0.18.1 Timeline profile, canonical source revision mandatory. |
| `OtioFidelityReport` | `1 profile:Key`; `2 entries:FidelityEntry[]`; `3 canCommit:bool`; `4 sourceHash:Hash` | Unsupported top-level refuses; no silent field loss. |
| `FidelityEntry` | `1 path:string`; `2 code:ReasonCode`; `3 disposition:Key`; `4 detailKey:Key` | exact/converted/unsupported/missingMedia. |
| `MediaRelink` | `1 mediaId:Id`; `2 replacement:ResourceRef`; `3 expectedHash:Hash?` | Validate identity, streams and ranges before atomic relink. |
| `ColourConfiguration` | `1 workingSpace:Key`; `2 displaySpace:Key`; `3 ocioConfig:ResourceVersionRef?`; `4 inputAssignments:MediaColourAssignment[]` | Built-in Rec709/sRGB or pinned OCIO configuration plus explicit source assignments; config hash participates in render/cache identity. |
| `MediaColourAssignment` | `1 mediaId:Id`; `2 inputSpace:Key` | Explicit override, never rewrite source metadata. |
| `MediaBin` | `1 binId:Id`; `2 parentId:Id?`; `3 name:Name`; `4 mediaIds:Id[]`; `5 sequenceIds:Id[]`; `6 order:uint32` | Same project, no cycles; stable identity, no filesystem path. |
| `ProcessingGraph` | `1 nodes:EffectSpec[]`; `2 edges:ProcessingEdge[]`; `3 outputNodeId:Id?`; `4 profile:Key` | slate.graph.v1, empty identity graph allowed; statically declared typed ports, acyclic; preserved unknown nodes remain bypassed. |
| `ProcessingEdge` | `1 sourceNodeId:Id`; `2 sourcePort:Key`; `3 targetNodeId:Id`; `4 targetPort:Key` | Both ports exist in definitions and have the same type; no implicit conversion or script. |
| `GeneratedSource` | `1 kind:Key`; `2 parameters:EffectParameter[]`; `3 text:TimedText?` | colour/gradient/counter/testPattern/title; title requires text and no numeric parameters, other kinds forbid text. Closed parameter profile, no external code. |
| `TimedText` | `1 text:Text`; `2 language:Key?`; `3 fontFamily:Name`; `4 fontAsset:ResourceVersionRef?`; `5 size:Decimal`; `6 colour:Key`; `7 alignment:Key`; `8 origin:ContentOrigin?` | NLE title or authored subtitle; plain Unicode text, explicit style/fallback; item's exact timeline range owns timing. |
| `TranscriptionRequest` | `1 taskId:Id`; `2 projectId:Id`; `3 sequenceId:Id`; `4 sourceRevision:NativeContentRev`; `5 range:MediaRange`; `6 audio:AudioChunk[]`; `7 language:Key?`; `8 maximumBudget:uint64?` | Explicit selected and uploaded audio only, slate.transcribe.v1; immutable ordered contiguous chunks cover the exact extracted range. |
| `AudioChunk` | `1 resource:ResourceVersionRef`; `2 sequenceRange:MediaRange`; `3 sampleCount:uint64`; `4 sha256:Hash` | Mono PCM16 WAV at 16000 Hz, <=30 seconds/1 MiB; hash and decoded sample count verified before admission. |
| `TranscriptRecord` | `1 transcriptId:Id`; `2 projectId:Id`; `3 sequenceId:Id`; `4 sourceRevision:NativeContentRev`; `5 range:MediaRange`; `6 segments:TranscriptSegment[]`; `7 modelId:ModelId`; `8 taskId:Id`; `9 complete:bool`; `10 origin:ContentOrigin` | Derived AI output, immutable artifact; partial result explicitly identifies missing ranges, never silently adopted. |
| `TranscriptSegment` | `1 range:MediaRange`; `2 text:Text`; `3 language:Key?`; `4 missing:bool` | Model-estimated timing mapped to canonical ticks once; missing forbids invented text. |
| `SubtitleInterchange` | `1 resource:ResourceVersionRef`; `2 format:Key`; `3 sequenceId:Id`; `4 acceptedLosses:Key[]` | srt/webvtt; preview binds immutable input and fidelity report. |
| `ScenarioSpec` | `1 channels:ChannelDefinition[]`; `2 expressions:ScenarioExpression[]`; `3 csv:ResourceVersionRef?`; `4 duration:ScopeTime`; `5 generators:GeneratorSpec[]`; `6 faults:FaultSpec[]`; `7 csvSchema:CsvReplaySchema?`; `8 executionProfile:Key` | All channel sources specified exactly once; fixed versioned AST/generators; no arbitrary code or URL. |
| `ScenarioExpression` | `1 channelId:Id`; `2 root:AstNode` | All referenced channels declared, cycle check. |
| `AstNode` | `1 constant:double`; `2 variable:Key`; `3 unary:UnaryExpression`; `4 binary:BinaryExpression`; `5 function:FunctionExpression` | oneof expression, every field; closed syntax/operator/function allowlist from simulator design, finite constants. |
| `UnaryExpression` | `1 operator:Key`; `2 operand:AstNode` | Bounded AST depth. |
| `BinaryExpression` | `1 operator:Key`; `2 left:AstNode`; `3 right:AstNode` | Checked deterministic math and explicit failure. |
| `FunctionExpression` | `1 function:Key`; `2 arguments:AstNode[]` | No external I/O or state outside seeded simulator profile. |
| `ContentOrigin` | `1 profile:Key`; `2 originId:Id`; `3 contentUnitId:Id`; `4 kinds:Key[]`; `5 payloadSha256:Hash`; `6 producerKind:Key`; `7 createdAt:Instant?`; `8 parentOriginIds:Id[]`; `9 omittedParentCount:uint32` | Exactly arcforges.content-origin.v1; kinds ordered aiGenerated/aiManipulated/nonAi/unknown, <=32 canonical-ID-sorted parents; no task/user/device/prompt metadata in exported carrier. |
| `TriggerSpec` | `1 manual:bool`; `2 schedule:ScheduleSpec`; `3 event:EventTrigger` | oneof; external integration event remains deferred. |
| `EventTrigger` | `1 kind:Key`; `2 source:AggregateRef?`; `3 predicate:NotesFilter?` | App/Cloud/Device durable registered event kinds only; authorization before occurrence creation. |
| `ResourceVersionRef` | `1 resource:ResourceRef`; `2 cloud:Revision`; `3 native:NativeContentRev`; `4 local:LocalNotesVersion`; `5 contentHash:Hash?`; `6 blob:BlobRef?` | oneof revision={cloud,native,local}; read pins require the owning revision and hash; immutable bytes require blob. |
| `BlobRef` | `1 blobId:Id`; `2 contentHash:Hash`; `3 sizeBytes:uint64` | Exact immutable bytes; not owner permission or a path. |
| `ResourceMetadata` | `1 resource:ResourceRef`; `2 version:ResourceVersionRef?`; `3 blob:BlobRef?`; `4 mediaType:string?`; `5 transferState:Key?`; `6 origin:ContentOrigin?` | Floating address, version and bytes remain distinct. |
| `UploadStatus` | `1 uploadId:Id`; `2 state:Key`; `3 parts:PartReceipt[]`; `4 resource:ResourceRef?`; `5 provisionalPin:Id?`; `6 expiresAt:Instant`; `7 reason:ReasonCode?`; `8 partsPage:PageState?` | staging/verifying/verified/expired/failed; at most200 receipts per page; verified exposes resource/pin, not owner publication. |
| `ClassificationMap` | `1 properties:PropertyMove[]`; `2 tags:TagMove[]` | Every used source classification has one disposition; no implicit label matching. |
| `PropertyMove` | `1 sourceId:Id`; `2 destinationId:Id?`; `3 remove:bool`; `4 options:OptionMove[]`; `5 destinationSemanticRev:Revision?` | Exactly one destination/remove=true. Same scalar type/scale; select options mapped completely and uniquely. |
| `OptionMove` | `1 sourceId:Id`; `2 destinationId:Id` | Explicit existing target option, no lossy scalar conversion. |
| `TagMove` | `1 sourceId:Id`; `2 destinationId:Id?`; `3 remove:bool` | Exactly one destination/remove=true, validated destination notebook. |
| `LocalRootVersion` | `1 root:AggregateRef`; `2 version:LocalNotesVersion` | Local composite token for one affected Notes root, never a Cloud acknowledgement. |
| `NotesMovePreview` | `1 proposalHash:Hash`; `2 unmapped:Id[]`; `3 removed:Id[]`; `4 canCommit:bool` | Hash binds document/notebook revisions, mapping and target semantic revisions. |
| `NotebookBody` | `1 notebook:NotebookView`; `2 folders:FolderView[]`; `3 documentOrder:Id[]` | Folder hierarchy/order included in notebook revision; validate cycles and membership before commit. |
| `PropertyDefinition` | `1 propertyId:Id`; `2 notebookId:Id`; `3 name:Name`; `4 type:Key`; `5 profile:Key`; `6 semanticRevision:Revision`; `7 revision:Revision`; `8 options:SelectOption[]`; `9 numberScale:uint32?`; `10 trashedAt:Instant?` | notes.scalar.v1 types/config/option limits and impact/refusal rules; no formulas/member relations. |
| `SelectOption` | `1 optionId:Id`; `2 label:Name`; `3 order:uint32` | At most1000; label edits do not change semanticRevision. |
| `SavedViewRecord` | `1 viewId:Id`; `2 notebookId:Id`; `3 name:Name`; `4 layout:Key`; `5 query:NotesQuery`; `6 revision:Revision`; `7 trashedAt:Instant?` | list/table only; persisted query has no page cursor/dataset token, no savedViewId self-reference; binds definition semantic revisions. |
| `TagRecord` | `1 tagId:Id`; `2 notebookId:Id`; `3 name:Name`; `4 colour:Key?`; `5 revision:Revision`; `6 trashedAt:Instant?` | Stable identity and revision; bounded declared palette. |
| `SkillRecord` | `1 skillId:Id`; `2 name:Name`; `3 instructions:Text`; `4 resources:ResourceVersionRef[]`; `5 capabilities:Key[]`; `6 revision:Revision`; `7 enabled:bool` | Declarative user skill, no executable script or permanent grant. |
| `ChatProjectRecord` | `1 projectId:Id`; `2 name:Name`; `3 conversationIds:Id[]`; `4 context:ContextRef[]`; `5 revision:Revision`; `6 trashedAt:Instant?` | Ordered conversation membership, current owner permission on every context use. |
| `PreferenceRecord` | `1 preferenceId:Id`; `2 ownerAppId:Key`; `3 values:MetadataEntry[]`; `4 revision:Revision` | Only declared syncable user preference keys; never paths, credentials, device-only layout or policy authority. |
| `MemoryRecord` | `1 memoryId:Id`; `2 text:Text`; `3 sources:ContextRef[]`; `4 revision:Revision`; `5 enabled:bool`; `6 origin:ContentOrigin?` | User-visible/editable personal memory, permission-filtered; no secret hidden long-term system instruction. |
| `NotesSelectors` | `1 documentId:Id?`; `2 folderId:Id?`; `3 tagIds:Id[]`; `4 text:string?`; `5 blockKinds:Key[]`; `6 hasAttachment:Bool?`; `7 modified:TimeRangeUtc?`; `8 linkedTo:Id?` | Typed additional accepted selectors; all restrictions conjunctive, text ordinal full-text matching under owner search profile, no expression in a literal. |
| `SearchQuery` | `1 notes:NotesQuery`; `2 general:GeneralSearchQuery` | oneof mode={notes,general}. Notes saved views use exact profile; general preserves keyword/metadata/semantic/hybrid search. |
| `GeneralSearchQuery` | `1 text:string`; `2 mode:Key`; `3 products:Key[]`; `4 sources:AggregateRef[]`; `5 tags:Id[]`; `6 changed:TimeRangeUtc?`; `7 page:PageRequest`; `8 datasetToken:Cursor?`; `9 notes:NotesSelectors?`; `10 budget:RetrievalBudget?` | keyword/metadata/semantic/hybrid; <=4096 text scalars/200 source roots; current permissions before candidates/counts. Semantic/hybrid needs Cloud eligibility; keyword stays available without AI. |
| `BlockProperties` | `1 headingLevel:uint32?`; `3 checked:bool?`; `4 calloutKind:Key?`; `9 listStyle:Key?`; `10 altText:string?`; `11 imageLayout:ImageLayout?`; `12 attachmentPresentation:Key?`; `13 embedRenderMode:Key?` | heading requires level1..6; list requires bulleted/numbered/checklist, checked required only for checklist; callout tone info/warning/error/success. Image requires altText (may be empty) and layout; attachment requires chip/card/pdfViewer; embed requires inline/card. All irrelevant fields refused. Reserved tags/names: 2/listStart,5/collapsed,6/caption,7/pdfPage,8/targetBlockId. |
| `InlineAtom` | `1 offset:uint32`; `2 mention:LinkSpec`; `3 math:MathContent`; `4 footnote:LinkSpec`; `5 origin:ContentOrigin?` | oneof content={mention,math,footnote}; unique offset pointing at U+FFFC. Stable document/block targets, no forged user membership. |
| `MathContent` | `1 tex:string`; `2 display:bool` | Bounded4096-scalar declarative math; render only, no file/network/macros executing code. |
| `ScopeTime` | `1 ticks:sint64`; `2 rate:Rational` | Exact capture timebase, independent of Slate tick rate. rate=ticks/second, positive; compare with checked rational intermediates. |
| `MeasurementWindow` | `1 start:ScopeTime`; `2 end:ScopeTime` | Half-open start<end; exact timebase conversion; sample indexes are optional access hints, never window authority. |
| `MeasurementSource` | `1 capture:ResourceVersionRef`; `2 channelId:Id`; `3 committedPrefix:uint64`; `4 configuration:ResourceVersionRef`; `5 decoder:ResourceVersionRef?`; `6 timeMapping:ResourceVersionRef?`; `7 eventSet:ResourceVersionRef?` | Immutable source/config/calibration/timebase/decoder/alignment inputs and byte hash; active capture pins a committed prefix. |
| `AlignmentSpec` | `1 kind:Key`; `2 leftAnchor:ScopeTime?`; `3 rightAnchor:ScopeTime?`; `4 offset:ScopeTime?`; `5 eventId:Id?` | absoluteTime/trigger/event/manualOffset; require relevant anchors. Never changes source bytes. |
| `CursorSpec` | `1 channelId:Id`; `2 segmentId:Id`; `3 time:ScopeTime` | Exactly two per requested cursor-delta family, within pinned window; nearest finite sample, earlier tie. |
| `SelectedSample` | `1 captureId:Id`; `2 channelId:Id`; `3 segmentId:Id`; `4 sampleIndex:uint64`; `5 time:ScopeTime`; `6 value:double` | Finite canonical calibrated sample, not display-decimated. |
| `CursorResult` | `1 a:SelectedSample`; `2 b:SelectedSample`; `3 deltaTime:ScopeTime`; `4 deltaValue:double` | Signed B-A; selected identities are exact; absent when cursorUnavailable. |
| `ClipPlacement` | `1 trackId:Id`; `2 beforeClipId:Id?`; `3 clip:TimelineClip` | Track exists; insertion/replacement/move validates source/destination and entire sequence at expectedNative. beforeClipId sets ordered position; absent appends. |
| `TransitionSpec` | `1 transitionId:Id`; `2 leftClipId:Id`; `3 rightClipId:Id`; `4 kind:Key`; `5 inOffset:MediaTime`; `6 outOffset:MediaTime` | Adjacent same-track clips; dissolve/audioCrossfade supported in V1; nonnegative handles within both sources; unsupported imported transitions follow OTIO loss report. |
| `KeyframeList` | `1 items:Keyframe[]` | Strictly increasing canonical times; bounded200 per RPC mutation; owner snapshot handles larger collections. |
| `Keyframe` | `1 time:MediaTime`; `2 value:Decimal`; `3 interpolation:Key`; `4 inTangent:Rational?`; `5 outTangent:Rational?`; `6 scope:Key` | hold/linear/bezier; scope must equal owning effect clipLocal/sequence; tangents are value per canonical second, finite checked rational; no silent scope conversion. |
| `LocalTransferTicket` | `1 transferId:Id`; `2 endpoint:LocalEndpoint`; `3 resource:ResourceVersionRef`; `4 allowedRange:ByteRange`; `5 expiresAt:Instant`; `6 nonce:Bytes` | Private local peer/lease bound,10-minute transfer renewed by reauthorization; not an HTTPS or R2 URL. |
| `LocalChunk` | `1 bytes:bytes`; `2 offset:uint64`; `3 nextOffset:uint64`; `4 eof:bool`; `5 sha256:Hash` | <=64 KiB exact bytes, whole-object hash on versioned source; no pointer/file descriptor on wire. |
| `GeneratorSpec` | `1 channelId:Id`; `2 kind:Key`; `3 offset:double?`; `4 amplitude:double?`; `5 frequencyHz:double?`; `6 phaseCycles:double?`; `7 dutyRatio:double?`; `8 walkStep:double?`; `9 pulses:PulseSpec[]`; `10 steps:StepPoint[]` | constant/sine/square/triangle/sawtooth/noise/randomWalk/pulse/stepSequence/csv; finite parameters; duty in(0,1); Only parameters applicable to kind may be present; required-by-kind values are validated. Empty pulses/steps are allowed for other kinds. |
| `PulseSpec` | `1 start:ScopeTime`; `2 duration:ScopeTime`; `3 value:double` | Sorted nonoverlapping half-open pulses; otherwise offset; finite value. |
| `StepPoint` | `1 at:ScopeTime`; `2 value:double` | Strictly increasing; right-continuous; initial offset. |
| `FaultSpec` | `1 faultId:Id`; `2 kind:Key`; `3 channelId:Id?`; `4 window:MeasurementWindow`; `5 everyTicks:uint64`; `6 probabilityPpm:uint32`; `7 delayTicks:uint64?`; `8 amount:double?`; `9 reorderWindow:uint32?` | latency/jitter/drop/duplicate/reorder/disconnect/malformed/outlier; explicit logical tick boundary; everyTicks>=1; probability0..1000000; kind-specific delay/amount/window only, reorder1..1024. |
| `CsvReplaySchema` | `1 encoding:Key`; `2 delimiter:string`; `3 hasHeader:bool`; `4 timestampColumn:uint32?`; `5 columns:CsvColumn[]`; `6 timestampUnit:Key?` | UTF-8, comma/tab/semicolon only; bounded4096-byte field/4096 columns; explicit row/time parse rejects malformed data. |
| `CsvColumn` | `1 column:uint32`; `2 channelId:Id`; `3 type:Key`; `4 unit:Key` | Declared numeric/digital/event field; finite canonical parse, no locale coercion. |
| `SimulationEvent` | `1 eventId:Id`; `2 channelId:Id`; `3 start:ScopeTime`; `4 duration:ScopeTime?`; `5 kind:Key`; `6 fields:MetadataEntry[]`; `7 faultId:Id?` | Stable event identity derived from scenario/channel/logical ordinal; duplicates preserve ID; intentional fault provenance. |
| `SimulationDataSegment` | `1 encodingProfile:Key`; `2 executionProfile:Key`; `3 startTick:uint64`; `4 tickCount:uint64`; `5 records:SimulationSample[]`; `6 events:SimulationEvent[]`; `7 gaps:SimulationGap[]` | Canonical af-segment.v1 payload; ordered by delivered ordinal; no run/host ID or wall clock. Metadata manifest holds those identities. |
| `SimulationSample` | `1 channelId:Id`; `2 tick:uint64`; `3 deliveredOrdinal:uint64`; `4 time:ScopeTime`; `5 numeric:double`; `6 digital:bool`; `7 eventId:Id`; `8 faultIds:Id[]` | oneof value={numeric,digital,eventId}; finite numeric; duplicates retain channel/tick/event identity and differ only in delivery ordinal/fault markers. |
| `SimulationGap` | `1 channelId:Id?`; `2 startTick:uint64`; `3 tickCount:uint64`; `4 faultId:Id`; `5 kind:Key` | Intentional drop/disconnect/malformed markers, not missing committed manifests. |
| `ConfigurationDocument` | `1 schemaVersion:Key`; `2 canonicalJson:bytes`; `3 documentHash:Hash`; `4 parentVersion:Key`; `5 createdAt:Instant` | Internal schema only, <=1 MiB; exact closed deployment configuration schema, secret references not values. |
| `OperatorAccess` | `1 accessId:Id`; `2 operatorId:Id`; `3 caseId:Id?`; `4 workspaceId:Id`; `5 resources:AggregateRef[]`; `6 purpose:Text`; `7 expiresAt:Instant`; `8 state:Key`; `9 consentRef:Id?`; `10 secondOperatorId:Id?`; `11 revision:Revision` | Internal only; one workspace, fixed purpose/resources, maximum15-minute access, required owner/second-operator approval. |
| `OperatorAction` | `1 actionId:Id`; `2 proposerId:Id`; `3 approverId:Id?`; `4 target:AggregateRef`; `5 action:Key`; `6 proposalHash:Hash`; `7 reason:Text`; `8 state:Key`; `9 expiresAt:Instant?`; `10 revision:Revision` | Internal only; existing closed enforcement/kill action registry; dual operator binds exact proposal. |
| `ConfigValidation` | `1 configId:Id`; `2 configHash:Hash`; `3 schemaVersion:Key`; `4 problems:ArcError[]`; `5 workerAcknowledgement:Hash?`; `6 compatible:bool`; `7 revision:Revision` | Internal only; validation receipt binds exact document/parent and selected worker/model/profile readiness. |
| `ExtensionLease` | `1 leaseId:Id`; `2 expiresAt:Instant`; `3 renewAfterSeconds:uint32`; `4 negotiatedContracts:Key[]` | Public extension-only endpoint-free lease, 30 seconds/renew10; never imports an internal LocalLease. |
| `ImageLayout` | `1 widthRatio:double`; `2 alignment:Key` | Finite widthRatio in(0,1], relative to available content width; start/center/end alignment. Default image insertion freezes ratio1/center; this is document presentation, not viewport/zoom state. |
| `MetadataScalar` | `1 text:string`; `2 boolean:bool`; `3 integer:sint64`; `4 number:double`; `5 decimal:Decimal`; `6 instant:Instant`; `7 resource:ResourceRef` | oneof value, every field; finite binary64 only. Closed first-party scalar metadata, with no recursive list/record or executable payload; no authority/policy/credential fields. |
| `MetadataEntry` | `1 name:Key`; `2 value:MetadataScalar` | Unique keys sorted ordinal, <=200 entries and <=64 KiB per owning field. Owner declares each permitted key/type; custom Scope/event metadata remains data, never parser/dispatch configuration. |
| `RetrievalBudget` | `1 candidates:uint32`; `2 evidence:uint32`; `3 contextTokens:uint32`; `4 contextBytes:uint32`; `5 perSource:uint32`; `6 graphDepth:uint32`; `7 graphEdges:uint32` | Selected defaults/hard bounds and packing order are in the derived-store retrieval profile. The caller may narrow active policy, never widen its limit. Graph depth0 disables expansion; other counts positive. |

The owner-profile payload constraints compose with these fields: blocks, property types/definitions, all supported timeline transitions and named measurement families retain their accepted formats and bounds. Oversize bodies use the already specified immutable ResourceVersionRef/BlobRef, never a silent truncated body. Optional backing resources do not grant a caller permission.

**Resource shapes remain distinct.** The numbered records above govern. Every immutable reader validates the pinned owner revision and BlobRef/hash; a floating ResourceRef is never silently treated as immutable bytes.

## 5. Public business operation registry

For every inherited operation, authorization/class/error/compatibility is the corresponding row in 01-public-api-operations.md. The new supporting operations below close existing workflows: sync.getBootstrapPage is Q/R1/FR; chat.createConversation is CC/R2/FR; automation list/get are Q/R1/AO; create is CC/R2/FR; update/setEnabled/delete are IW/IW/DE with expectedRev and R2/FR; runNow is CC/R2/FR with one caller occurrenceId; resolveMissed is IW/R2/FR; submitEvent is AP/R2/FR restricted to authenticated registered device/app event owners. All require the workspace's current owner/session, applicable service term and capability scope; automation declarations grant no permanent authority. No new human/team role.

| Stable operation ID | Proto service.method | Request fields (meta at 1) | Success value fields |
|---|---|---|---|
| `identity.beginPasskeyRegistration` | `IdentityService.BeginPasskeyRegistration` | `10 displayName:Name` | `10 challenge:AuthChallenge` |
| `identity.completePasskeyRegistration` | `IdentityService.CompletePasskeyRegistration` | `10 flowId:Id`; `11 credential:WebAuthnCreation` | `10 credential:CredentialSummary` |
| `identity.beginAuthentication` | `IdentityService.BeginAuthentication` | `10 method:AuthMethod`; `11 loginHint:Email?`; `12 installation:InstallationClaim`; `13 providerId:Key?`; `14 purpose:AuthPurpose` | `10 challenge:AuthChallenge` |
| `identity.completeAuthentication` | `IdentityService.CompleteAuthentication` | `10 flowId:Id`; `11 proof:AuthProof` | `10 session:NativeSession` |
| `identity.requestEmailCode` | `IdentityService.RequestEmailCode` | `10 purpose:AuthPurpose`; `11 email:Email`; `12 flowId:Id?` | `10 challenge:AuthChallenge` |
| `identity.redeemEmailCode` | `IdentityService.RedeemEmailCode` | `10 flowId:Id`; `11 code:SecretText` | `10 session:NativeSession` |
| `identity.refreshSession` | `IdentityService.RefreshSession` | `10 refreshToken:SecretText`; `11 installationId:Id` | `10 session:NativeSession` |
| `identity.revokeSession` | `IdentityService.RevokeSession` | `10 sessionId:Id` | `10 receipt:Receipt` |
| `identity.revokeAllSessions` | `IdentityService.RevokeAllSessions` | — | `10 receipt:Receipt` |
| `identity.listAuthIdentities` | `IdentityService.ListAuthIdentities` | `10 page:PageRequest` | `10 items:CredentialSummary[]`; `11 page:PageState` |
| `identity.removeAuthIdentity` | `IdentityService.RemoveAuthIdentity` | `10 credentialId:Id` | `10 receipt:Receipt` |
| `identity.beginStepUp` | `IdentityService.BeginStepUp` | `10 operationClass:Key` | `10 challenge:AuthChallenge` |
| `identity.completeStepUp` | `IdentityService.CompleteStepUp` | `10 flowId:Id`; `11 proof:AuthProof` | `10 evidence:StepUpEvidence` |
| `identity.beginRecovery` | `IdentityService.BeginRecovery` | `10 email:Email` | `10 challenge:AuthChallenge` |
| `identity.completeRecovery` | `IdentityService.CompleteRecovery` | `10 flowId:Id`; `11 proof:AuthProof`; `12 replacement:WebAuthnCreation` | `10 receipt:Receipt` |
| `identity.requestAccountDeletion` | `IdentityService.RequestAccountDeletion` | — | `10 deletion:DeletionStatus` |
| `identity.cancelAccountDeletion` | `IdentityService.CancelAccountDeletion` | `10 deletionId:Id` | `10 deletion:DeletionStatus` |
| `identity.getProfile` | `IdentityService.GetProfile` | — | `10 profile:AccountProfile` |
| `identity.updateProfile` | `IdentityService.UpdateProfile` | `10 patch:ProfileUpdate` | `10 profile:AccountProfile` |
| `identity.listAuthProviders` | `IdentityService.ListAuthProviders` | — | `10 providers:AuthProviderView[]` |
| `identity.beginEmailChange` | `IdentityService.BeginEmailChange` | `10 email:Email` | `10 challenge:AuthChallenge` |
| `identity.completeEmailChange` | `IdentityService.CompleteEmailChange` | `10 flowId:Id`; `11 code:SecretText` | `10 profile:AccountProfile` |
| `identity.renameAuthIdentity` | `IdentityService.RenameAuthIdentity` | `10 credentialId:Id`; `11 name:Name` | `10 credential:CredentialSummary` |
| `identity.generateRecoveryCodes` | `IdentityService.GenerateRecoveryCodes` | — | `10 set:RecoveryCodeSet` |
| `identity.listSessions` | `IdentityService.ListSessions` | `10 page:PageRequest` | `10 sessions:SessionSummary[]`; `11 page:PageState` |
| `identity.listApiTokens` | `IdentityService.ListApiTokens` | `10 page:PageRequest` | `10 tokens:ApiTokenView[]`; `11 page:PageState` |
| `identity.createApiToken` | `IdentityService.CreateApiToken` | `10 tokenId:Id`; `11 name:Name`; `12 workspaceId:Id`; `13 scopes:Key[]`; `14 expiresAt:Instant` | `10 token:ApiTokenView`; `11 secret:SecretText?` |
| `identity.revokeApiToken` | `IdentityService.RevokeApiToken` | `10 tokenId:Id` | `10 receipt:Receipt` |
| `identity.listSecurityActivity` | `IdentityService.ListSecurityActivity` | `10 page:PageRequest` | `10 events:SecurityActivity[]`; `11 page:PageState` |
| `identity.getAccountDeletion` | `IdentityService.GetAccountDeletion` | — | `10 deletion:DeletionStatus?` |
| `identity.beginDeviceSso` | `IdentityService.BeginDeviceSso` | `10 target:InstallationClaim` | `10 challenge:DeviceSsoChallenge` |
| `identity.completeDeviceSso` | `IdentityService.CompleteDeviceSso` | `10 flowId:Id`; `11 deviceSignature:Bytes` | `10 session:NativeSession` |
| `identity.changePassword` | `IdentityService.ChangePassword` | `10 password:SecretText` | `10 receipt:Receipt` |
| `workspace.getHealth` | `WorkspaceService.GetHealth` | — | `10 health:WorkspaceHealth` |
| `workspace.requestDataDeletion` | `WorkspaceService.RequestDataDeletion` | `10 deletionId:Id`; `11 previewHash:Hash` | `10 deletion:DataDeletionView` |
| `workspace.previewDataDeletion` | `WorkspaceService.PreviewDataDeletion` | — | `10 preview:DataDeletionPreview` |
| `workspace.getDataDeletion` | `WorkspaceService.GetDataDeletion` | `10 deletionId:Id` | `10 deletion:DataDeletionView` |
| `device.signOut` | `DeviceService.SignOut` | `10 deviceId:Id` | `10 receipt:Receipt` |
| `device.getRemotePolicy` | `DeviceService.GetRemotePolicy` | `10 deviceId:Id` | `10 policy:RemoteCapabilityPolicy` |
| `device.setRemotePolicy` | `DeviceService.SetRemotePolicy` | `10 policy:RemoteCapabilityPolicy` | `10 policy:RemoteCapabilityPolicy` |
| `workspace.list` | `WorkspaceService.List` | `10 page:PageRequest` | `10 items:WorkspaceView[]`; `11 page:PageState` |
| `workspace.get` | `WorkspaceService.Get` | `10 workspaceId:Id` | `10 workspace:WorkspaceView` |
| `workspace.updateSettings` | `WorkspaceService.UpdateSettings` | `10 name:Name?`; `11 protection:ProtectionProfile?` | `10 workspace:WorkspaceView` |
| `device.register` | `DeviceService.Register` | `10 deviceId:Id`; `11 installationId:Id`; `12 product:Key`; `13 platform:Key`; `14 name:Name`; `15 publicKey:Bytes` | `10 device:DeviceView` |
| `device.list` | `DeviceService.List` | `10 page:PageRequest` | `10 items:DeviceView[]`; `11 page:PageState` |
| `device.rename` | `DeviceService.Rename` | `10 deviceId:Id`; `11 name:Name` | `10 device:DeviceView` |
| `device.setTrust` | `DeviceService.SetTrust` | `10 deviceId:Id`; `11 trust:TrustLevel` | `10 device:DeviceView` |
| `device.setRemoteEnabled` | `DeviceService.SetRemoteEnabled` | `10 deviceId:Id`; `11 enabled:Bool` | `10 device:DeviceView` |
| `device.revoke` | `DeviceService.Revoke` | `10 deviceId:Id` | `10 receipt:Receipt` |
| `device.heartbeat` | `DeviceService.Heartbeat` | `10 deviceId:Id`; `11 installationId:Id`; `12 instances:InstancePresence[]` | `10 lease:PresenceLease` |
| `entitlement.getSnapshot` | `EntitlementService.GetSnapshot` | — | `10 snapshot:EntitlementSnapshot` |
| `entitlement.getServiceTerm` | `EntitlementService.GetServiceTerm` | — | `10 term:ServiceTerm` |
| `entitlement.getCapacity` | `EntitlementService.GetCapacity` | — | `10 capacity:Capacity` |
| `entitlement.listGrants` | `EntitlementService.ListGrants` | `10 page:PageRequest` | `10 items:Grant[]`; `11 page:PageState` |
| `entitlement.getUsage` | `EntitlementService.GetUsage` | `10 period:TimeRangeUtc` | `10 usage:QuotaUsage[]` |
| `entitlement.check` | `EntitlementService.Check` | `10 capabilities:Key[]` | `10 items:Availability[]` |
| `commerce.authoriseExtraUsage` | `CommerceService.AuthoriseExtraUsage` | `10 authorisationId:Id`; `11 maxBudget:UInt64`; `12 expiresAt:Instant` | `10 budget:SpendBudget` |
| `commerce.revokeExtraUsage` | `CommerceService.RevokeExtraUsage` | `10 authorisationId:Id` | `10 receipt:Receipt` |
| `commerce.explainCharge` | `CommerceService.ExplainCharge` | `10 logicalRequestId:Id` | `10 explanation:ChargeExplanation` |
| `commerce.getCatalogue` | `CommerceService.GetCatalogue` | `10 region:CountryCode` | `10 items:Offer[]`; `11 catalogueVersion:Key` |
| `commerce.createPurchaseIntent` | `CommerceService.CreatePurchaseIntent` | `10 purchaseIntentId:Id`; `11 offerId:Id`; `12 priceVersion:Key`; `13 region:CountryCode` | `10 purchase:PurchaseView` |
| `commerce.createCheckoutAttempt` | `CommerceService.CreateCheckoutAttempt` | `10 purchaseIntentId:Id`; `11 checkoutAttemptId:Id`; `12 returnRoute:Key` | `10 checkout:CheckoutView` |
| `commerce.getPurchaseState` | `CommerceService.GetPurchaseState` | `10 purchaseIntentId:Id` | `10 purchase:PurchaseView` |
| `commerce.getSubscription` | `CommerceService.GetSubscription` | — | `10 subscription:SubscriptionView?` |
| `commerce.cancelSubscription` | `CommerceService.CancelSubscription` | `10 subscriptionId:Id` | `10 subscription:SubscriptionView` |
| `commerce.reactivateSubscription` | `CommerceService.ReactivateSubscription` | `10 subscriptionId:Id` | `10 subscription:SubscriptionView` |
| `commerce.getCredits` | `CommerceService.GetCredits` | — | `10 capacity:Capacity`; `11 compensation:CreditLot[]`; `12 purchased:CreditPool` |
| `commerce.listBillingHistory` | `CommerceService.ListBillingHistory` | `10 period:TimeRangeUtc`; `11 page:PageRequest` | `10 items:BillingItem[]`; `11 page:PageState` |
| `commerce.requestRefund` | `CommerceService.RequestRefund` | `10 refundId:Id`; `11 paymentId:Id`; `12 reason:Text` | `10 refund:RefundView` |
| `commerce.exportEvidence` | `CommerceService.ExportEvidence` | `10 period:TimeRangeUtc` | `10 job:ExportJob` |
| `sync.listScopes` | `SyncService.ListScopes` | `10 page:PageRequest` | `10 items:SyncScope[]`; `11 page:PageState` |
| `sync.setScope` | `SyncService.SetScope` | `10 scopeId:Id`; `11 enabled:Bool`; `12 exclusions:Key[]` | `10 scope:SyncScope` |
| `sync.pullChanges` | `SyncService.PullChanges` | `10 scopeId:Id`; `11 cursor:Cursor?`; `12 limit:Int32` | `10 changes:SyncChange[]`; `11 nextCursor:Cursor`; `12 hasMore:Bool` |
| `sync.pushChange` | `SyncService.PushChange` | `10 change:ChangeProposal` | `10 result:ChangeReceipt` |
| `sync.pushBatch` | `SyncService.PushBatch` | `10 changes:ChangeProposal[]` | `10 results:ChangeReceipt[]` |
| `sync.getAggregate` | `SyncService.GetAggregate` | `10 root:AggregateRef`; `11 minRevision:Revision?` | `10 aggregate:AggregateView` |
| `sync.listConflicts` | `SyncService.ListConflicts` | `10 scopeId:Id?`; `11 page:PageRequest` | `10 items:ConflictView[]`; `11 page:PageState` |
| `sync.resolveConflict` | `SyncService.ResolveConflict` | `10 conflictId:Id`; `11 resolution:ConflictResolution` | `10 result:ChangeReceipt` |
| `sync.requestFullResync` | `SyncService.RequestFullResync` | `10 scopeId:Id` | `10 bootstrap:BootstrapManifest` |
| `sync.getBootstrapPage` | `SyncService.GetBootstrapPage` | `10 bootstrapId:Id`; `11 cursor:Cursor?` | `10 items:AggregateView[]`; `11 page:PageState`; `12 resumeCursor:Cursor` |
| `notes.listNotebooks` | `NotesService.ListNotebooks` | `10 page:PageRequest` | `10 items:NotebookView[]`; `11 page:PageState` |
| `notes.listFolders` | `NotesService.ListFolders` | `10 notebookId:Id`; `11 includeTrash:Bool`; `12 page:PageRequest` | `10 items:FolderView[]`; `11 page:PageState` |
| `notes.getDocument` | `NotesService.GetDocument` | `10 documentId:Id`; `11 projection:DocumentProjection` | `10 document:DocumentView` |
| `notes.createNotebook` | `NotesService.CreateNotebook` | `10 notebookId:Id`; `11 name:Name` | `10 notebook:NotebookView` |
| `notes.createFolder` | `NotesService.CreateFolder` | `10 folderId:Id`; `11 notebookId:Id`; `12 parentId:Id?`; `13 name:Name`; `14 beforeSiblingId:Id?` | `10 folder:FolderView` |
| `notes.renameFolder` | `NotesService.RenameFolder` | `10 folderId:Id`; `11 name:Name` | `10 folder:FolderView` |
| `notes.moveFolder` | `NotesService.MoveFolder` | `10 folderId:Id`; `11 parentId:Id?`; `12 beforeSiblingId:Id?` | `10 folder:FolderView` |
| `notes.reorderFolder` | `NotesService.ReorderFolder` | `10 folderId:Id`; `11 beforeSiblingId:Id?` | `10 folder:FolderView` |
| `notes.previewMoveDocument` | `NotesService.PreviewMoveDocument` | `10 documentId:Id`; `11 destinationNotebookId:Id`; `12 destinationFolderId:Id?`; `13 classificationMap:ClassificationMap` | `10 preview:NotesMovePreview` |
| `notes.moveDocument` | `NotesService.MoveDocument` | `10 documentId:Id`; `11 destinationNotebookId:Id`; `12 destinationFolderId:Id?`; `13 sourceNotebookRev:Revision`; `14 destinationNotebookRev:Revision`; `15 classificationMap:ClassificationMap`; `16 previewHash:Hash` | `10 document:DocumentRef`; `11 changedRoots:VersionedRef[]` |
| `notes.trashFolder` | `NotesService.TrashFolder` | `10 folderId:Id` | `10 folder:FolderView` |
| `notes.restoreFolder` | `NotesService.RestoreFolder` | `10 folderId:Id` | `10 folder:FolderView` |
| `notes.listRevisions` | `NotesService.ListRevisions` | `10 documentId:Id`; `11 page:PageRequest` | `10 items:RevisionView[]`; `11 page:PageState` |
| `notes.getRevision` | `NotesService.GetRevision` | `10 documentId:Id`; `11 revision:Revision` | `10 revision:RevisionView` |
| `notes.createCheckpoint` | `NotesService.CreateCheckpoint` | `10 documentId:Id`; `11 revision:Revision`; `12 name:Name` | `10 checkpoint:CheckpointView` |
| `notes.restoreRevision` | `NotesService.RestoreRevision` | `10 documentId:Id`; `11 sourceRevision:Revision` | `10 document:DocumentRef` |
| `notes.requestExport` | `NotesService.RequestExport` | `10 exportId:Id`; `11 request:ExportRequest` | `10 job:ExportJob` |
| `export.getStatus` | `ExportService.GetStatus` | `10 exportId:Id` | `10 job:ExportJob` |
| `export.cancel` | `ExportService.Cancel` | `10 exportId:Id` | `10 job:ExportJob` |
| `export.getDownload` | `ExportService.GetDownload` | `10 exportId:Id` | `10 ticket:TransferTicket` |
| `resource.beginUpload` | `ResourceService.BeginUpload` | `10 uploadId:Id`; `11 resourceId:Id`; `12 size:UInt64`; `13 sha256:Hash`; `14 mediaType:string`; `15 purpose:ResourcePurpose`; `16 owner:AggregateRef` | `10 ticket:UploadTicket` |
| `resource.completeUpload` | `ResourceService.CompleteUpload` | `10 uploadId:Id`; `11 parts:PartReceipt[]` | `10 status:UploadStatus` |
| `resource.getDownloadTicket` | `ResourceService.GetDownloadTicket` | `10 resourceId:Id`; `11 range:ByteRange?`; `12 version:ResourceVersionRef?` | `10 ticket:TransferTicket` |
| `resource.getMetadata` | `ResourceService.GetMetadata` | `10 resourceId:Id` | `10 metadata:ResourceMetadata` |
| `resource.release` | `ResourceService.Release` | `10 resourceId:Id`; `11 referrer:AggregateRef` | `10 receipt:Receipt` |
| `task.list` | `TaskService.List` | `10 filter:TaskFilter`; `11 page:PageRequest` | `10 items:TaskSnapshot[]`; `11 page:PageState` |
| `task.get` | `TaskService.Get` | `10 taskId:Id` | `10 task:TaskSnapshot`; `11 runs:RunView[]`; `12 steps:StepView[]`; `13 attempts:AttemptView[]` |
| `task.create` | `TaskService.Create` | `10 taskId:Id`; `11 conversationId:Id?`; `12 profileId:Id`; `13 input:TurnInput`; `14 steps:StepSpec[]` | `10 task:TaskSnapshot` |
| `task.cancel` | `TaskService.Cancel` | `10 taskId:Id` | `10 task:TaskSnapshot` |
| `task.pause` | `TaskService.Pause` | `10 taskId:Id` | `10 task:TaskSnapshot` |
| `task.resume` | `TaskService.Resume` | `10 taskId:Id` | `10 task:TaskSnapshot` |
| `task.retryAttempt` | `TaskService.RetryAttempt` | `10 taskId:Id`; `11 attemptId:Id`; `12 reconciliationDecision:ReconciliationDecision` | `10 task:TaskSnapshot` |
| `task.steer` | `TaskService.Steer` | `10 taskId:Id`; `11 text:Text`; `12 context:ContextRef[]` | `10 receipt:Receipt` |
| `approval.list` | `ApprovalService.List` | `10 taskId:Id?`; `11 page:PageRequest` | `10 items:ApprovalView[]`; `11 page:PageState` |
| `approval.decide` | `ApprovalService.Decide` | `10 approvalId:Id`; `11 decision:ApprovalDecision`; `12 proposalHash:Hash`; `13 localEvidence:PresenceEvidence?` | `10 approval:ApprovalView` |
| `bridge.pullRequests` | `BridgeService.PullRequests` | `10 deviceId:Id`; `11 cursor:Cursor?`; `12 limit:Int32` | `10 requests:ToolRequest[]`; `11 nextCursor:Cursor` |
| `bridge.submitResult` | `BridgeService.SubmitResult` | `10 toolRequestId:Id`; `11 attemptId:Id`; `12 commandId:Id`; `13 result:ToolResult` | `10 receipt:Receipt` |
| `bridge.getRequestState` | `BridgeService.GetRequestState` | `10 toolRequestId:Id` | `10 request:ToolRequest` |
| `chat.listConversations` | `ChatService.ListConversations` | `10 page:PageRequest` | `10 items:ConversationView[]`; `11 page:PageState` |
| `chat.getConversation` | `ChatService.GetConversation` | `10 conversationId:Id`; `11 branchId:Id?`; `12 page:PageRequest` | `10 conversation:ConversationView`; `11 messages:MessageView[]`; `12 page:PageState` |
| `chat.appendMessage` | `ChatService.AppendMessage` | `10 conversationId:Id`; `11 messageId:Id`; `12 draft:MessageDraft`; `13 startTurn:TurnOptions?` | `10 message:MessageView`; `11 task:TaskSnapshot?` |
| `chat.createBranch` | `ChatService.CreateBranch` | `10 branchId:Id`; `11 conversationId:Id`; `12 fromMessageId:Id` | `10 conversation:ConversationView` |
| `chat.requestExport` | `ChatService.RequestExport` | `10 exportId:Id`; `11 request:ExportRequest` | `10 job:ExportJob` |
| `task.startTranscription` | `TaskService.StartTranscription` | `10 request:TranscriptionRequest` | `10 task:TaskSnapshot` |
| `agent.listModels` | `AgentService.ListModels` | — | `10 models:ModelView[]`; `11 configVersion:Key` |
| `agent.listProfiles` | `AgentService.ListProfiles` | — | `10 profiles:AgentProfile[]` |
| `agent.getUsage` | `AgentService.GetUsage` | `10 period:TimeRangeUtc`; `11 page:PageRequest` | `10 items:ChargeExplanation[]`; `11 page:PageState` |
| `search.query` | `SearchService.Query` | `10 query:SearchQuery` | `10 items:SearchHit[]`; `11 page:PageState`; `12 dataset:NotesDataset` |
| `policy.getBundle` | `PolicyService.GetBundle` | `10 installationId:Id`; `11 lastVersion:Key?` | `10 bundle:PolicyBundle` |
| `notification.list` | `NotificationService.List` | `10 page:PageRequest` | `10 items:NotificationView[]`; `11 page:PageState` |
| `notification.acknowledge` | `NotificationService.Acknowledge` | `10 notificationId:Id` | `10 receipt:Receipt` |
| `notification.registerPush` | `NotificationService.RegisterPush` | `10 installationId:Id`; `11 platform:Key`; `12 token:SecretText` | `10 registrationId:Id` |
| `notification.unregisterPush` | `NotificationService.UnregisterPush` | `10 registrationId:Id` | `10 receipt:Receipt` |
| `support.createCase` | `SupportService.CreateCase` | `10 caseId:Id`; `11 subject:Name`; `12 message:Text`; `13 diagnostic:ResourceRef?`; `14 category:Key`; `15 relatedActionId:Id?` | `10 case:SupportCase` |
| `support.listCases` | `SupportService.ListCases` | `10 page:PageRequest` | `10 items:SupportCase[]`; `11 page:PageState` |
| `support.appendMessage` | `SupportService.AppendMessage` | `10 caseId:Id`; `11 messageId:Id`; `12 text:Text` | `10 case:SupportCase` |
| `data.requestExport` | `DataService.RequestExport` | `10 exportId:Id` | `10 job:ExportJob` |
| `data.getExportState` | `DataService.GetExportState` | `10 exportId:Id` | `10 job:ExportJob` |
| `simulation.listDefinitions` | `SimulationService.ListDefinitions` | `10 page:PageRequest` | `10 items:SimulationDefinition[]`; `11 page:PageState` |
| `simulation.getDefinition` | `SimulationService.GetDefinition` | `10 definitionId:Id` | `10 definition:SimulationDefinition`; `11 versions:ScenarioVersion[]` |
| `simulation.createDefinition` | `SimulationService.CreateDefinition` | `10 definitionId:Id`; `11 name:Name` | `10 definition:SimulationDefinition` |
| `simulation.publishScenarioVersion` | `SimulationService.PublishScenarioVersion` | `10 scenarioVersionId:Id`; `11 definitionId:Id`; `12 scenario:ScenarioSpec` | `10 version:ScenarioVersion` |
| `simulation.startRun` | `SimulationService.StartRun` | `10 runId:Id`; `11 scenarioVersionId:Id`; `12 seed:Int64`; `13 profile:SimulationProfile` | `10 run:SimulationRun` |
| `simulation.pauseRun` | `SimulationService.PauseRun` | `10 runId:Id` | `10 run:SimulationRun` |
| `simulation.resumeRun` | `SimulationService.ResumeRun` | `10 runId:Id` | `10 run:SimulationRun` |
| `simulation.cancelRun` | `SimulationService.CancelRun` | `10 runId:Id` | `10 run:SimulationRun` |
| `simulation.getRun` | `SimulationService.GetRun` | `10 runId:Id` | `10 run:SimulationRun` |
| `simulation.listSegments` | `SimulationService.ListSegments` | `10 runId:Id`; `11 page:PageRequest` | `10 segments:SimulationSegment[]`; `11 page:PageState` |
| `simulation.getSegmentTicket` | `SimulationService.GetSegmentTicket` | `10 runId:Id`; `11 segmentSequence:Int64`; `12 range:ByteRange?` | `10 ticket:TransferTicket` |
| `simulation.pollState` | `SimulationService.PollState` | `10 runId:Id`; `11 knownRevision:Revision?` | `10 run:SimulationRun`; `11 hasChanged:Bool` |
| `automation.list` | `AutomationService.List` | `10 page:PageRequest` | `10 items:AutomationView[]`; `11 page:PageState` |
| `automation.get` | `AutomationService.Get` | `10 automationId:Id` | `10 automation:AutomationView` |
| `automation.create` | `AutomationService.Create` | `10 automationId:Id`; `11 definition:AutomationSpec` | `10 automation:AutomationView` |
| `automation.update` | `AutomationService.Update` | `10 automationId:Id`; `11 definition:AutomationSpec` | `10 automation:AutomationView` |
| `automation.setEnabled` | `AutomationService.SetEnabled` | `10 automationId:Id`; `11 enabled:Bool` | `10 automation:AutomationView` |
| `automation.delete` | `AutomationService.Delete` | `10 automationId:Id` | `10 receipt:Receipt` |
| `automation.runNow` | `AutomationService.RunNow` | `10 automationId:Id`; `11 occurrenceId:Id` | `10 task:TaskSnapshot` |
| `automation.submitEvent` | `AutomationService.SubmitEvent` | `10 eventId:Id`; `11 kind:Key`; `12 source:AggregateRef`; `13 sourceRevision:Revision`; `14 causation:Id[]` | `10 receipt:Receipt` |
| `automation.resolveMissed` | `AutomationService.ResolveMissed` | `10 automationId:Id`; `11 occurrenceKeys:Key[]`; `12 decision:Key` | `10 receipt:Receipt` |
| `chat.createConversation` | `ChatService.CreateConversation` | `10 conversationId:Id`; `11 title:Name` | `10 conversation:ConversationView` |
| `resource.getUploadStatus` | `ResourceService.GetUploadStatus` | `10 uploadId:Id`; `11 page:PageRequest` | `10 status:UploadStatus` |
| `resource.renewUploadTicket` | `ResourceService.RenewUploadTicket` | `10 uploadId:Id` | `10 ticket:TransferTicket` |
| `agent.putProfile` | `AgentService.PutProfile` | `10 value:AgentProfile` | `10 value:AgentProfile` |
| `agent.deleteProfile` | `AgentService.DeleteProfile` | `10 id:Id` | `10 receipt:Receipt` |
| `agent.putSkill` | `AgentService.PutSkill` | `10 value:SkillRecord` | `10 value:SkillRecord` |
| `agent.deleteSkill` | `AgentService.DeleteSkill` | `10 id:Id` | `10 receipt:Receipt` |
| `chat.putProject` | `ChatService.PutProject` | `10 value:ChatProjectRecord` | `10 value:ChatProjectRecord` |
| `chat.deleteProject` | `ChatService.DeleteProject` | `10 id:Id` | `10 receipt:Receipt` |
| `chat.putMemory` | `ChatService.PutMemory` | `10 value:MemoryRecord` | `10 value:MemoryRecord` |
| `chat.deleteMemory` | `ChatService.DeleteMemory` | `10 id:Id` | `10 receipt:Receipt` |
| `preference.put` | `PreferenceService.Put` | `10 value:PreferenceRecord` | `10 value:PreferenceRecord` |
| `support.decideAccess` | `SupportService.DecideAccess` | `10 accessId:Id`; `11 proposalHash:Hash`; `12 approve:bool` | `10 receipt:Receipt` |

Resource upload status is owner-authorized Q/R1/AO; renewal is NI/R1/FR transport authorization, safe to repeat only as a new ticket for the same still-valid upload, never a data mutation. Renewal issues a fresh ten-minute transport ticket only while the original 24-hour upload session/reservation remains valid; it does not extend that session, restart bytes or publish content. GetUploadStatus pages accepted receipts. CompleteUpload seals the immutable manifest, returns verifying, and is reconciled by status until verified/failed.


## 6. Local and extension operation registry

Existing catalogue02 authorization and expected revision rules apply. C# Async suffixes are adapter naming only and do not enter proto service names. Hub uses local.hub; Notes/Scope/Slate/Chat each own their domain service; common provider/resource/lifecycle services use local.platform. IExtensionHost alone is the public extensions package. Calls in both directions use each process's own unary server; there is no symmetric-call assumption on one gRPC channel.

| Stable interface.method | Proto service.method | Request fields (meta at 1) | Success value fields |
|---|---|---|---|
| `IHubRegistry.Register` | `HubRegistryService.Register` | `10 registration:Registration` | `10 lease:LocalLease` |
| `IHubRegistry.RenewLease` | `HubRegistryService.RenewLease` | `10 leaseId:Id` | `10 lease:LocalLease` |
| `IHubRegistry.Deregister` | `HubRegistryService.Deregister` | `10 leaseId:Id` | `10 receipt:Receipt` |
| `IHubRegistry.ReportHealth` | `HubRegistryService.ReportHealth` | `10 leaseId:Id`; `11 health:HealthReport` | `10 receipt:Receipt` |
| `IHubRouting.ResolveCapability` | `HubRoutingService.ResolveCapability` | `10 capability:Key`; `11 context:ResolutionContext` | `10 binding:CapabilityBinding` |
| `IHubRouting.ListContributions` | `HubRoutingService.ListContributions` | `10 filter:ContributionFilter`; `11 page:PageRequest` | `10 items:Contribution[]`; `11 page:PageState` |
| `IHubRouting.GetHealth` | `HubRoutingService.GetHealth` | `10 appId:Key?` | `10 health:HealthReport[]` |
| `ICapabilityProvider.Describe` | `CapabilityProviderService.Describe` | — | `10 capabilities:CapabilityDescriptor[]` |
| `ICapabilityProvider.EvaluateAvailability` | `CapabilityProviderService.EvaluateAvailability` | `10 action:Key`; `11 context:FrozenContext` | `10 availability:Availability` |
| `ICapabilityProvider.Invoke` | `CapabilityProviderService.Invoke` | `10 invocation:Invocation` | `10 result:ToolResult` |
| `IContextProvider.DescribeContextKinds` | `ContextProviderService.DescribeContextKinds` | — | `10 kinds:Key[]` |
| `IContextProvider.ProvideContext` | `ContextProviderService.ProvideContext` | `10 request:ContextRequest` | `10 contribution:ContextContribution` |
| `IArtifactHandler.DescribeArtifactKinds` | `ArtifactHandlerService.DescribeArtifactKinds` | — | `10 kinds:Key[]` |
| `IArtifactHandler.Resolve` | `ArtifactHandlerService.Resolve` | `10 artifact:ArtifactRef` | `10 artifact:ArtifactRef` |
| `IArtifactHandler.RenderPreview` | `ArtifactHandlerService.RenderPreview` | `10 artifact:ArtifactRef`; `11 request:PreviewRequest` | `10 preview:ResourceRef` |
| `IArtifactHandler.Open` | `ArtifactHandlerService.Open` | `10 artifact:ArtifactRef`; `11 intent:OpenIntent` | `10 receipt:Receipt` |
| `IResourceAccess.GetMetadata` | `ResourceAccessService.GetMetadata` | `10 resourceId:Id` | `10 metadata:ResourceMetadata` |
| `IResourceAccess.OpenRead` | `ResourceAccessService.OpenRead` | `10 resourceId:Id`; `11 range:ByteRange?`; `12 version:ResourceVersionRef?` | `10 channel:LocalTransferTicket` |
| `IResourceAccess.BeginTransfer` | `ResourceAccessService.BeginTransfer` | `10 request:TransferRequest` | `10 ticket:LocalTransferTicket` |
| `IResourceAccess.Release` | `ResourceAccessService.Release` | `10 resourceId:Id`; `11 referrer:AggregateRef` | `10 receipt:Receipt` |
| `IProductLifecycle.GetState` | `ProductLifecycleService.GetState` | — | `10 state:ProductState` |
| `IProductLifecycle.PrepareForShutdown` | `ProductLifecycleService.PrepareForShutdown` | `10 reason:Key` | `10 ready:bool`; `11 reasons:ReasonCode[]` |
| `IDeepLinkTarget.HandleDeepLink` | `DeepLinkTargetService.HandleDeepLink` | `10 link:string` | `10 receipt:Receipt` |
| `INotesOperations.Search` | `NotesOperationsService.Search` | `10 query:SearchQuery` | `10 items:DocumentView[]`; `11 page:PageState`; `12 dataset:NotesDataset` |
| `INotesOperations.GetDocument` | `NotesOperationsService.GetDocument` | `10 documentId:Id`; `11 projection:DocumentProjection` | `10 document:DocumentView` |
| `INotesOperations.CreateDocument` | `NotesOperationsService.CreateDocument` | `10 documentId:Id`; `11 notebookId:Id`; `12 folderId:Id?`; `13 title:Name`; `14 blocks:Block[]` | `10 document:DocumentRef` |
| `INotesOperations.AppendBlocks` | `NotesOperationsService.AppendBlocks` | `10 documentId:Id`; `11 blocks:Block[]` | `10 version:LocalNotesVersion` |
| `INotesOperations.ApplyBlockEdits` | `NotesOperationsService.ApplyBlockEdits` | `10 documentId:Id`; `11 edits:BlockEdit[]` | `10 version:LocalNotesVersion` |
| `INotesOperations.SetProperties` | `NotesOperationsService.SetProperties` | `10 documentId:Id`; `11 values:PropertyValue[]` | `10 version:LocalNotesVersion` |
| `INotesOperations.AddTags` | `NotesOperationsService.AddTags` | `10 documentId:Id`; `11 tagIds:Id[]` | `10 version:LocalNotesVersion` |
| `INotesOperations.RemoveTags` | `NotesOperationsService.RemoveTags` | `10 documentId:Id`; `11 tagIds:Id[]` | `10 version:LocalNotesVersion` |
| `INotesOperations.CreateLink` | `NotesOperationsService.CreateLink` | `10 documentId:Id`; `11 link:LinkSpec` | `10 version:LocalNotesVersion` |
| `INotesOperations.TrashDocument` | `NotesOperationsService.TrashDocument` | `10 documentId:Id` | `10 version:LocalNotesVersion` |
| `INotesOperations.Export` | `NotesOperationsService.Export` | `10 exportId:Id`; `11 request:ExportRequest` | `10 artifact:ArtifactRef` |
| `INotesOperations.ListNotebooks` | `NotesOperationsService.ListNotebooks` | `10 page:PageRequest` | `10 items:NotebookView[]`; `11 page:PageState` |
| `INotesOperations.ListFolders` | `NotesOperationsService.ListFolders` | `10 notebookId:Id`; `11 includeTrash:Bool`; `12 page:PageRequest` | `10 items:FolderView[]`; `11 page:PageState` |
| `INotesOperations.CreateNotebook` | `NotesOperationsService.CreateNotebook` | `10 notebookId:Id`; `11 name:Name` | `10 notebook:NotebookView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.CreateFolder` | `NotesOperationsService.CreateFolder` | `10 folderId:Id`; `11 notebookId:Id`; `12 parentId:Id?`; `13 name:Name`; `14 beforeSiblingId:Id?` | `10 folder:FolderView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.RenameFolder` | `NotesOperationsService.RenameFolder` | `10 folderId:Id`; `11 name:Name` | `10 folder:FolderView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.MoveFolder` | `NotesOperationsService.MoveFolder` | `10 folderId:Id`; `11 parentId:Id?`; `12 beforeSiblingId:Id?` | `10 folder:FolderView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.ReorderFolder` | `NotesOperationsService.ReorderFolder` | `10 folderId:Id`; `11 beforeSiblingId:Id?` | `10 folder:FolderView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.PreviewMoveDocument` | `NotesOperationsService.PreviewMoveDocument` | `10 documentId:Id`; `11 destinationNotebookId:Id`; `12 destinationFolderId:Id?`; `13 classificationMap:ClassificationMap` | `10 preview:NotesMovePreview` |
| `INotesOperations.MoveDocument` | `NotesOperationsService.MoveDocument` | `10 documentId:Id`; `11 destinationNotebookId:Id`; `12 destinationFolderId:Id?`; `13 sourceNotebookVersion:LocalNotesVersion`; `14 destinationNotebookVersion:LocalNotesVersion`; `15 classificationMap:ClassificationMap`; `16 previewHash:Hash` | `10 document:DocumentRef`; `11 version:LocalNotesVersion`; `12 pending:bool`; `13 changedRoots:LocalRootVersion[]` |
| `INotesOperations.TrashFolder` | `NotesOperationsService.TrashFolder` | `10 folderId:Id` | `10 folder:FolderView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.RestoreFolder` | `NotesOperationsService.RestoreFolder` | `10 folderId:Id` | `10 folder:FolderView`; `11 version:LocalNotesVersion`; `12 pending:bool` |
| `INotesOperations.ListRevisions` | `NotesOperationsService.ListRevisions` | `10 documentId:Id`; `11 page:PageRequest` | `10 items:RevisionView[]`; `11 page:PageState` |
| `INotesOperations.GetRevision` | `NotesOperationsService.GetRevision` | `10 documentId:Id`; `11 revision:Revision` | `10 revision:RevisionView` |
| `INotesOperations.CreateCheckpoint` | `NotesOperationsService.CreateCheckpoint` | `10 documentId:Id`; `11 revision:Revision`; `12 name:Name` | `10 checkpoint:CheckpointView` |
| `INotesOperations.RestoreRevision` | `NotesOperationsService.RestoreRevision` | `10 documentId:Id`; `11 sourceRevision:Revision` | `10 document:DocumentRef` |
| `IScopeOperations.ListSessions` | `ScopeOperationsService.ListSessions` | `10 page:PageRequest` | `10 items:ScopeSession[]`; `11 page:PageState` |
| `IScopeOperations.GetSession` | `ScopeOperationsService.GetSession` | `10 sessionId:Id` | `10 session:ScopeSession` |
| `IScopeOperations.ListCaptures` | `ScopeOperationsService.ListCaptures` | `10 sessionId:Id`; `11 page:PageRequest` | `10 items:CaptureView[]`; `11 page:PageState` |
| `IScopeOperations.GetConfigurationSnapshot` | `ScopeOperationsService.GetConfigurationSnapshot` | `10 sessionId:Id` | `10 configuration:ScopeConfiguration` |
| `IScopeOperations.RunMeasurement` | `ScopeOperationsService.RunMeasurement` | `10 request:MeasurementRequest` | `10 measurement:MeasurementResult` |
| `IScopeOperations.RunAnalysis` | `ScopeOperationsService.RunAnalysis` | `10 request:AnalysisRequest` | `10 job:ProductJobRef` |
| `IScopeOperations.CompareSessions` | `ScopeOperationsService.CompareSessions` | `10 request:CompareRequest` | `10 comparison:ArtifactRef` |
| `IScopeOperations.CreateAnnotation` | `ScopeOperationsService.CreateAnnotation` | `10 annotationId:Id`; `11 sessionId:Id`; `12 range:SampleRange`; `13 text:Text` | `10 revision:NativeContentRev` |
| `IScopeOperations.CreateFinding` | `ScopeOperationsService.CreateFinding` | `10 findingId:Id`; `11 sessionId:Id`; `12 result:ResourceRef`; `13 text:Text` | `10 revision:NativeContentRev` |
| `IScopeOperations.GenerateReport` | `ScopeOperationsService.GenerateReport` | `10 request:ReportRequest` | `10 artifact:ArtifactRef` |
| `IScopeOperations.StartCapture` | `ScopeOperationsService.StartCapture` | `10 captureId:Id`; `11 request:CaptureRequest` | `10 capture:CaptureView` |
| `IScopeOperations.StopCapture` | `ScopeOperationsService.StopCapture` | `10 captureId:Id` | `10 capture:CaptureView` |
| `IScopeOperations.GetStructuredContext` | `ScopeOperationsService.GetStructuredContext` | `10 request:ContextRequest` | `10 contribution:ContextContribution` |
| `ISlateOperations.ListProjects` | `SlateOperationsService.ListProjects` | `10 page:PageRequest` | `10 items:SlateProject[]`; `11 page:PageState` |
| `ISlateOperations.GetSequence` | `SlateOperationsService.GetSequence` | `10 sequenceId:Id` | `10 sequence:SequenceView` |
| `ISlateOperations.ListMedia` | `SlateOperationsService.ListMedia` | `10 projectId:Id`; `11 page:PageRequest` | `10 items:MediaView[]`; `11 page:PageState` |
| `ISlateOperations.GetTimeline` | `SlateOperationsService.GetTimeline` | `10 sequenceId:Id`; `11 range:MediaRange?` | `10 timeline:TimelineView` |
| `ISlateOperations.ListMarkers` | `SlateOperationsService.ListMarkers` | `10 sequenceId:Id`; `11 page:PageRequest` | `10 items:MarkerView[]`; `11 page:PageState` |
| `ISlateOperations.CreateMarker` | `SlateOperationsService.CreateMarker` | `10 marker:MarkerView` | `10 revision:NativeContentRev` |
| `ISlateOperations.ApplyTimelineEdits` | `SlateOperationsService.ApplyTimelineEdits` | `10 sequenceId:Id`; `11 edits:TimelineEdit[]` | `10 revision:NativeContentRev` |
| `ISlateOperations.PrepareTranscription` | `SlateOperationsService.PrepareTranscription` | `10 sequenceId:Id`; `11 range:MediaRange`; `12 jobId:Id` | `10 job:ProductJobRef` |
| `ISlateOperations.AdoptTranscript` | `SlateOperationsService.AdoptTranscript` | `10 transcript:ResourceVersionRef`; `11 sequenceId:Id`; `12 trackId:Id`; `13 acceptedPartial:bool` | `10 revision:NativeContentRev` |
| `ISlateOperations.ImportSubtitles` | `SlateOperationsService.ImportSubtitles` | `10 request:SubtitleInterchange`; `11 trackId:Id` | `10 revision:NativeContentRev`; `11 fidelity:OtioFidelityReport` |
| `ISlateOperations.ExportSubtitles` | `SlateOperationsService.ExportSubtitles` | `10 sequenceId:Id`; `11 trackId:Id`; `12 format:Key`; `13 acceptLossy:bool` | `10 artifact:ArtifactRef`; `11 fidelity:OtioFidelityReport` |
| `ISlateOperations.StartRender` | `SlateOperationsService.StartRender` | `10 renderId:Id`; `11 request:RenderRequest` | `10 job:ProductJobRef` |
| `ISlateOperations.CancelRender` | `SlateOperationsService.CancelRender` | `10 renderId:Id` | `10 job:ProductJobRef` |
| `ISlateOperations.Export` | `SlateOperationsService.Export` | `10 exportId:Id`; `11 request:ExportRequest` | `10 artifact:ArtifactRef` |
| `ISlateOperations.GetSequenceContext` | `SlateOperationsService.GetSequenceContext` | `10 request:ContextRequest` | `10 contribution:ContextContribution` |
| `ISlateOperations.ImportOtio` | `SlateOperationsService.ImportOtio` | `10 request:OtioImportRequest` | `10 sequence:SequenceView`; `11 fidelity:OtioFidelityReport` |
| `ISlateOperations.PreviewOtioImport` | `SlateOperationsService.PreviewOtioImport` | `10 request:OtioImportRequest` | `10 fidelity:OtioFidelityReport` |
| `ISlateOperations.ExportOtio` | `SlateOperationsService.ExportOtio` | `10 sequenceId:Id`; `11 committedRev:NativeContentRev`; `12 request:OtioExportRequest` | `10 artifact:ArtifactRef`; `11 fidelity:OtioFidelityReport` |
| `ISlateOperations.RelinkMedia` | `SlateOperationsService.RelinkMedia` | `10 sequenceId:Id`; `11 relinks:MediaRelink[]` | `10 revision:NativeContentRev` |
| `IChatOperations.ListConversations` | `ChatOperationsService.ListConversations` | `10 page:PageRequest` | `10 items:ConversationView[]`; `11 page:PageState` |
| `IChatOperations.GetConversation` | `ChatOperationsService.GetConversation` | `10 conversationId:Id`; `11 branchId:Id?`; `12 page:PageRequest` | `10 conversation:ConversationView`; `11 messages:MessageView[]`; `12 page:PageState` |
| `IChatOperations.CreateConversation` | `ChatOperationsService.CreateConversation` | `10 conversationId:Id`; `11 title:Name` | `10 conversation:ConversationView` |
| `IChatOperations.AppendUserMessage` | `ChatOperationsService.AppendUserMessage` | `10 conversationId:Id`; `11 messageId:Id`; `12 draft:MessageDraft` | `10 receipt:Receipt`; `11 pending:bool` |
| `IChatOperations.StartAgentTurn` | `ChatOperationsService.StartAgentTurn` | `10 taskId:Id`; `11 conversationId:Id`; `12 input:TurnInput`; `13 options:TurnOptions` | `10 task:TaskSnapshot` |
| `IChatOperations.SubmitApproval` | `ChatOperationsService.SubmitApproval` | `10 approvalId:Id`; `11 decision:ApprovalDecision`; `12 proposalHash:Hash` | `10 approval:ApprovalView` |
| `IChatOperations.Handoff` | `ChatOperationsService.Handoff` | `10 artifact:ArtifactRef`; `11 targetAppId:Key`; `12 intent:OpenIntent` | `10 receipt:Receipt` |
| `IExtensionHost.Handshake` | `ExtensionHostService.Handshake` | `10 packageId:Key`; `11 packageVersion:Key`; `12 protocolVersions:Key[]`; `13 installationId:Id`; `14 nonce:bytes`; `15 contributions:Contribution[]` | `10 lease:ExtensionLease` |
| `IExtensionHost.Invoke` | `ExtensionHostService.Invoke` | `10 invocation:Invocation` | `10 result:ToolResult` |
| `IExtensionHost.RenewLease` | `ExtensionHostService.RenewLease` | `10 leaseId:Id` | `10 lease:ExtensionLease` |
| `IExtensionHost.Stop` | `ExtensionHostService.Stop` | `10 leaseId:Id`; `11 reason:Key` | `10 receipt:Receipt` |
| `IResourceAccess.ReadChunk` | `ResourceAccessService.ReadChunk` | `10 transferId:Id`; `11 offset:UInt64`; `12 length:UInt64` | `10 chunk:LocalChunk` |
| `IProductLifecycle.GetJob` | `ProductLifecycleService.GetJob` | `10 jobId:Id` | `10 job:ProductJobRef` |
| `ILocalBootstrap.Challenge` | `LocalBootstrapService.Challenge` | `10 instanceId:Id`; `11 challenge:Bytes` | `10 challengeId:Id`; `11 serverChallenge:Bytes`; `12 expiresAt:Instant` |
| `ILocalBootstrap.Confirm` | `LocalBootstrapService.Confirm` | `10 challengeId:Id`; `11 proof:Bytes` | `10 peerNonce:Bytes`; `11 expiresAt:Instant` |

INotesOperations.Export returns ArtifactRef(jobId) for the Cloud export accepted-snapshot workflow, not immediate local bytes. All local Notes structural operations use expectedLocal composite tokens; moveDocument additionally supplies source/destination notebook local tokens (same positions as the Cloud revision fields, local message types differ). Raw captures/media never enter ContextContribution. StartRender/RunAnalysis/Export return durable ProductJob/artifact handles before long work. Local operation names preserve their existing risk/idempotency class: declaring them unary does not make a non-idempotent effect safe to retry.

## 7. Event and exception registries

EventService.Poll request meta1 plus10 subscriptionKey:Key,11 cursor:Cursor?,12 limit:uint32?; success10 events:Event[],11 nextCursor:Cursor,12 resetRequired:bool. Default limit50/max 200 and max 256 KiB. Event = tags 1 subscriptionKey,2 seq:uint64,3 workspaceId:Id,4 occurredAt:Instant,5 correlationId:Id; oneof payload tags 10 onward in the following order. Payload fields start1 in listed order. Poll checks subscription ownership; resetRequired causes authoritative snapshot/cursor repair. Events contain only hints and stable IDs, never user content or an execution credential.

| Event ID | Typed payload fields |
|---|---|
| `sync.changed` | `1 root:AggregateRef`; `2 revision:Revision`; `3 originDeviceId:Id?` |
| `sync.conflictRaised` | `1 conflictId:Id`; `2 root:AggregateRef` |
| `task.stateChanged` | `1 taskId:Id`; `2 state:TaskState`; `3 reason:ReasonCode?`; `4 revision:Revision` |
| `task.progress` | `1 taskId:Id`; `2 runId:Id`; `3 progress:uint32`; `4 stepOrdinal:uint32` |
| `task.outputAppended` | `1 taskId:Id`; `2 streamId:Id`; `3 nextOffset:uint64` |
| `approval.raised` | `1 approvalId:Id`; `2 taskId:Id`; `3 risk:Key`; `4 expiresAt:Instant` |
| `approval.resolved` | `1 approvalId:Id`; `2 decision:ApprovalDecision` |
| `entitlement.changed` | `1 entitlementVersion:int64` |
| `device.presenceChanged` | `1 deviceId:Id`; `2 connectionState:Key`; `3 eligible:bool` |
| `bridge.requestAvailable` | `1 count:uint32` |
| `notification.raised` | `1 notificationId:Id`; `2 durability:Key` |
| `policy.bundleAvailable` | `1 version:Key` |
| `resource.committed` | `1 resourceId:Id`; `2 sha256:Hash` |
| `capacity.changed` | `1 recoveryAt:Instant?` |
| `serviceTerm.changed` | `1 workspaceId:Id` |
| `simulation.stateChanged` | `1 runId:Id`; `2 state:Key`; `3 committedSequence:int64` |
| `config.revisionActivated` | `1 configId:Id` |

| Existing exception | Transport and schema authority | Contract |
|---|---|---|
| browser.bootstrap/beginAuthentication/completeAuthentication/logout | The four core same-origin HTTP routes plus provider callback/enrollment exceptions specified by the security profile; public/http/v1/browser.schema.json | Request/response AuthChallenge/AuthProof/SessionView plus CSRF token; session secret only Set-Cookie, never NativeSession |
| commerce.providerWebhook | Paddle HTTP signature/raw body; verified event normalized by Commerce | Persist original provider event ID, body hash and inbox receipt before acknowledgement; first-party proto does not replace provider schema |
| resource.uploadChunk | PUT /objects/v1/{ticketId}/parts/{partNumber} | Bytes + PartReceipt; bounded and authenticated per contracts05 |
| task.readStream | GET /ai/v1/tasks/{taskId}/stream | Precise bounded StreamRead in contracts05; C# Task.get remains business authority |
| MCP/device protocols | Standard MCP/device transport at declared owner adapter | Generated capability projection; no new first-party wire authority |
| content helper/macOS XPC and C ABI | Isolation/native authorities | Typed bounded private control; no forced gRPC/pointer serialization |

## 8. Transport and generation acceptance

C# uses Grpc.Tools 2.83.0, Google.Protobuf 3.36.1, Grpc.AspNetCore/Grpc.Net.Client/Grpc.AspNetCore.Web2.83.0. Generated registration is explicit, no runtime service discovery or reflection serialization. Browser uses @bufbuild/protobuf and protoc-gen-es2.14.1 plus @connectrpc/connect/connect-web2.2.0 createGrpcWebTransport. The committed Grpc.Tools package supplies protoc for both generators, ensuring one compiler rather than independently downloaded protoc. Contract generation runs locked restore → protoc C#/grpc plus protoc-gen-es TS → descriptor validation → compatibility check against released descriptor → generated validator/tool-schema projection → C#/TS fixtures → pack. Generated descriptor sets and package integrity hashes are published; a second generation must produce no diff.

RN uses the same generated descriptors with the first-party Apache unary gRPC-Web fetch transport in Contracts. It sends binary application/grpc-web+proto, a single five-byte-header data frame (flag0, big-endian uint32 length), and consumes a bounded arrayBuffer response with data frames followed by exactly one trailer frame(flag0x80). Validate declared lengths before allocation, reject compression/unknown flags, missing/duplicate/nonzero grpc-status trailers and extra unary messages; decode grpc-message safely. HTTP transport success alone is not gRPC success. No ReadableStream/browser-only streaming dependency or native gRPC module. Request/response max 4 MiB; list/event bodies remain <=256 KiB. Timeout AbortController does not prove an effect absent. Production React and Hermes tests use actual framed success/error/trailer/truncated fixtures and a real AOT C# service.

Native Cloud TLS HTTP/2 endpoint is /arcforges.<domain>.v1.<Service>/<Method>; same-origin browser/RN /rpc routing preserves that gRPC path. Local Kestrel listens HTTP/2 over Named Pipe/UDS, Grpc.Net.Client uses ConnectCallback; no public TCP listener or local TLS required inside authenticated OS IPC. Each process exposes its own server, starts it before Hub registration and rebuilds channels after peer restart. OS peer PID/user/code signature, private directory ACL and nonce challenge establish identity; registration lease then grants only its declared peer scope.

Default unary deadline10s (owner-approved synchronous measurement max 30s), concurrency16 per peer/session, queue 64, local message max 4 MiB; return typed busy/resource limit before dispatch when full. Large results use ResourceRef/handle, not larger arbitrary frames. Named pipe current-user ACL/asynchronous; UDS directory0700/socket0600, path<=100 UTF-8 bytes; nonce bootstrap uses OS-verified peer with short-lived32-byte credential held only in memory, lease30s/renew10s. Hub absence does not prevent a professional product starting or synchronizing directly to Cloud. Resource affinity and existing resolution order remain unchanged.

References: [gRPC-Web framing](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md), [Connect protocol selection](https://connectrpc.com/docs/web/choosing-a-protocol/), [gRPC IPC](https://learn.microsoft.com/en-us/aspnet/core/grpc/interprocess?view=aspnetcore-10.0), [noncanonical protobuf serialization](https://protobuf.dev/programming-guides/serialization-not-canonical/). Protocol selection is a design; published-artifact proof remains [WP-06](../../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)/23/24/30.

## 9. Operator control and separate identity boundary

OperatorService uses internal/proto/arcforges/operator/v1 (AGPL), served only through the separate operator origin and operator Identity scheme. It shares the same generated message/value/error rules; it never accepts a customer cookie or customer entitlement as operator authority. The operator React build is AGPL and may consume its internal generated SDK, while public Web and RN cannot import it.

| Method | Request fields after meta1 (starting10) | Success fields starting10 |
|---|---|---|
| ListCases | page:PageRequest, state:Key? | cases:SupportCase[], page:PageState |
| GetCase | caseId:Id | case:SupportCase |
| RequestAccess | accessId:Id, caseId:Id, workspaceId:Id, resources:AggregateRef[], reason:Text, until:Instant | access:OperatorAccess |
| ApproveAccess | accessId:Id, proposalHash:Hash, approve:bool | access:OperatorAccess |
| EndAccess | accessId:Id | receipt:Receipt |
| ReadDiagnostic | accessId:Id, resourceId:Id | ticket:TransferTicket |
| ProposeEnforcement | actionId:Id, caseId:Id, userId:Id, action:Key, reason:Text, until:Instant? | action:OperatorAction |
| DecideEnforcement | actionId:Id, proposalHash:Hash, approve:bool | action:OperatorAction |
| GetAppeal | appealId:Id | case:SupportCase, action:OperatorAction |
| ResolveAppeal | appealId:Id, actionId:Id, decision:Key, reason:Text | action:OperatorAction |
| StageConfiguration | configId:Id, parentVersion:Key, document:ConfigurationDocument | validation:ConfigValidation |
| ValidateConfiguration | configId:Id | validation:ConfigValidation |
| ApproveConfiguration | configId:Id, validationHash:Hash, approve:bool, reason:Text | approvalId:Id, expiresAt:Instant |
| ActivateConfiguration | configId:Id, validationHash:Hash, secondApprovalId:Id | activeVersion:Key |
| GetConfiguration | configId:Id? | document:ConfigurationDocument, validation:ConfigValidation |
| SetKillSwitch | actionId:Id, mode:Key, scope:AggregateRef?, reason:Text, until:Instant | action:OperatorAction |
| StartBreakGlass | accessId:Id, incidentId:Id, resources:AggregateRef[], reason:Text | access:OperatorAccess |
| EndBreakGlass | accessId:Id, outcome:Text | receipt:Receipt |

OperatorAccess, OperatorAction and ConfigValidation use the numbered internal-only records in §4, including revision in responses for IW preconditions. Operator request/result fields in each table cell are numbered from 10 in the listed order.

Queries are Q; caller-stable create IDs CC; decision/activation/ending IW with expected revision. Support read access expires at most15 minutes and requires owner consent when content rather than diagnostics is involved. Destructive customer-data/entitlement/enforcement/config changes bind a second distinct authorized operator to the exact proposal hash before owner execution. Action names are the existing enforcement ladder, kill modes and configuration keys, not a new remote script facility. Break-glass uses the existing separately alarmed incident path with15-minute limit, immediate alert/audit and mandatory post-review. Audit is appended by the operation owner; no generic “write audit rows” API. Customer appeals and community reports use support.createCase with the existing case category and action reference; internal operator methods cannot be called through the public support session.

Operator identity selects Microsoft Entra ID OIDC Authorization Code+PKCE with server-side exchange, pinned tenant/client/audience and issuer, MFA/conditional access; separate opaque operator session cookie and CSRF binding, no JS bearer or personal Microsoft account fallback. Roles Reader/Support/Operator/SecurityAdmin/ConfigAdmin restrict the above actions; all role assignments are operator-directory inputs, never public user claims. OIDC redirect/code and external incident/status systems are explicit standard-protocol exceptions. JWKS rotation validates keys, issuer/audience/nonce/time and never accepts an arbitrary discovery URL. AOT implementation uses explicit JwtBearer10.0.12/JWT validation metadata, typed HTTP exchange and server session adapter; WP06 proves its actual publish path, WP45 its access/dual-approval/incident behavior.

## 10. Owner bodies, mutation admission and schema composition

All record fields have explicit tags in §4. oneof membership is the set named in the validation cell; if that cell says every field, it means all listed fields. ErrorDetails uses all four fields; ChangeReceipt uses accepted/error only; MessagePart uses text/resource/toolProposal/toolResult, leaving origin outside; ToolResult uses success/error, leaving identities/effect/artifacts outside. Exactly one declared variant must be present. No repeated field is placed directly in a oneof; use the listed wrapper records. Field bounds compose with owner profiles and transport byte limits.

Common identity/revision/error/value/resource/origin records are public foundation; domain projections live in their public domain package. Registration/LocalEndpoint/LocalLease/LocalTransferTicket/LocalChunk/bootstrap records live under internal local.platform; Hub-specific routing records under local.hub. Public extension messages use public equivalents of endpoint-free lease/descriptor/invocation/result, never import local-only records. Local product services may import public domain projections but public proto never imports internal packages. Internal operator/configuration records stay AGPL. Generated code follows this import graph.

Sync accepts client-origin writes only for NotebookBody/NotesDocument/PropertyDefinition/SavedViewRecord/TagRecord and authorized ScopeMetadata/SlateMetadata under their normal owner transactions and expected revisions. An externalBody resolves to that same permitted typed body before validation; object indirection cannot bypass the allowlist. TaskSnapshot, AutomationView, ConversationBody, AgentProfile, SkillRecord, ChatProjectRecord, MemoryRecord and PreferenceRecord are Cloud-authored feed/read projections. Client writes use their named public commands; no assistant/tool message, usage, grant or Task state is accepted through sync. Agent/profile/skill/project/memory/preference put/delete operations are IW/DE, R2/FR, current owner scope and expectedRev; absent-root create requires expectedRev=0 and stable ID. They publish owner revision, command receipt and Sync change in the existing shared transaction. Delete revokes future participation while retaining referenced immutable history until normal retention; it does not alter a running snapshot or grant authority.

Notes owner sync validators apply the frozen property semantic-revision, option-reference and saved-view invalidation rules before committing. Local edits use composite local tokens; Cloud commands use Cloud revisions. Local folder/notebook results include the resulting LocalNotesVersion and pending status, never claim Cloud acknowledgement. These fields are local envelopes, not changes to public acknowledged history.

Support access consent is IW/R2/FR, restricted to the case's current workspace owner, exact proposal hash and unexpired requested resource scope. Consent records permission for that scope only; operator access still needs its separate role/approval. Case category/action reference cannot select an arbitrary privileged operation. GetCase and support list results paginate messages before byte limits.

Local bootstrap authenticates both OS peers before any credential exchange. Challenge returns a fresh server challenge bound to both connection identities; Confirm echoes that challenge as proof of channel possession, returns a random per-peer nonce, and consumes the challenge once (five seconds). It is not a cryptographic substitute for OS identity. Send the nonce only in local gRPC metadata x-af-peer on later calls, bind it to peer identity/lease and invalidate at disconnect/expiry. No credential is stored in a manifest. Local reads authorize each <=64 KiB chunk and checked offset; same transfer/offset repeats return identical immutable bytes. GetJob is Q/R1/AO on an owned ProductJob.

EventService.Poll itself establishes one of the four existing subscription scopes; no Subscribe RPC or negotiation route. With absent cursor it returns an empty page and signed current cursor with resetRequired=true; client performs its authoritative snapshot before continuing. PostgreSQL holds bounded non-authoritative hint envelopes per subscription (24-hour TTL, latest10,000 events). Publishing advances a row-locked per-subscription sequence with the inserted hint; missing/expired intervals or a changed auth epoch produce resetRequired, never a successful incomplete page. A positive empty poll advances only to the observed committed head. Every call rechecks scope/owner/device, and byte-limit paging returns the last delivered cursor. Loss of the entire hint store still converges through the established authoritative reads.

General search retains each source's ranked/full-text behavior and complete citation. A local Notes call permits keyword/metadata and hydrated Notes selectors; semantic/hybrid routes to the Cloud service through its explicit authorized action, never a local model. For Notes saved views the exact profile is authoritative over generic PageRequest defaults. No wire schema can weaken its query limit, missing-value truth table or dataset cursor validation.

Owner projections exceeding the normal RPC bound are encoded as the same declared protobuf message in verified immutable object storage, with descriptor/schema identity and digest pinned. A reader validates the declared size before bounded parsing and refuses unsupported profiles; it does not load arbitrary JSON or truncate silently. Mutations remain bounded batches and never raise the transport cap just to accept a larger body.


Internal ConfigurationDocument tags 1..5 are schemaVersion:Key, canonicalJson:bytes, documentHash:Hash, parentVersion:Key, createdAt:Instant. It is the complete closed configuration schema in the existing policy architecture, <=1 MiB, with exact numeric strings and no secret values (secret reference IDs only). It is never the public signed PolicyBundle projection. Stage/Validate execute full schema/cross-field/secret-reference/Workers-model readiness checks; ApproveConfiguration is IW with expectedRev and binds a distinct authorized operator to validationHash for 15 minutes. Activate requires that receipt, unchanged parent/config and worker acknowledgement, then uses the existing atomic configuration family. Invalidating any input invalidates approval.


The public profile includes every owner record reachable from AggregateBody; internal-only ConfigurationDocument and operator records remain in the internal dependency graph even though listed together for field review. Module/API generation is from that explicit placement, never from Markdown section location.

For new simulator semantic hashes, finite binary64 values encode as a 16-lowercase-hex-digit IEEE754 bit word in big-endian byte order, preserving signed zero; nonfinite values refuse. af-segment.v1 serializes SimulationDataSegment as canonical UTF-8 JSON under this field/value profile, with explicit oneof field presence and every ordered repeated field present even when empty. Integral fields use the exact string mapping; IDs use lower-case UUID; object fields sort ordinal. That canonical JSON is the immutable segment body, not arbitrary protobuf encoder output. Segment length/hash cover those bytes. Existing product-native canonical formats retain their own authority.



Block.kind maps exactly to [the thirteen accepted owner kinds](../18-editing-and-rich-content.md#21-block-content): paragraph/heading/list/quote/callout/toggle use text; code uses code; math uses math with display=true; divider uses empty=true; table uses table; image/attachment use resource; embed uses link to a document/block/saved view identity. The required kind-specific BlockProperties above complete that body. PDF is attachment with pdfViewer, checklist is list with checklist style, and toggle children remain parent-linked Block rows. Collapse, PDF page/zoom and scroll are device-local, never sync content. Unsupported writable kinds or incompatible bodies refuse; unknown persisted kinds remain inert under the owner evolution rules.

RichText is a reversible wire projection of InlineContent: concatenate NFC text runs, encode LineBreak as LF, and place U+FFFC for each mention/inline-math/footnote atom. Flatten marks, non-nested links and origin fragments into bounded spans/atoms; links may contain differently marked text. Convert owner run-relative UTF-16 offsets to absolute wire UTF-16 offsets by checked prefix sums, and reverse at span/atom boundaries on decode. Merge adjacent identical marked runs as the owner already requires; preserve unknown read-only marks inert. Atom content uses the declared oneof, with math display=false. For A中😀, UTF-16 boundaries are0/1/2/4; byte boundaries0/1/4/8 remain specific to CF stream offsets. Do not substitute one offset unit for the other. No HTML/Markdown string becomes canonical Notes content.

## Large read projection profile

Only read/query responses may use outcome.encodedBody (tag 4). The referenced bytes encode that operation's exact generated SMValue under the pinned descriptor; check messageType, descriptorHash, byteLength and ResourceVersionRef SHA-256 before decode. This covers DocumentView, TimelineView, Task snapshots and large aggregate reads, not only Sync AggregateBody. Freeze the owner revision or multi-owner snapshot before encoding; snapshotToken binds that revision set, caller, realm, generation and projection. Pin bytes for the 15-minute reference lifetime. Renew by a fresh authorized read; never splice bytes from different snapshots.

Cloud uses the R2 authorized range facade. A local reply uses the same descriptor/hash contract with owner-scoped temporary resource access under local RPC catalogue; no absolute path becomes ambient access. Cloud transfers are bounded to 8 MiB ranges and local transfers to 64 KiB chunks, projections to 64 MiB encoded, and at most one large decode per client. A larger projection must use its paged owner operation (bounded pages may themselves reference bodies); explicitly selected document/project content over 64 MiB returns a typed limit and an export artifact path, preserving the full source. Command responses remain small receipts/handles; the caller reconciles a lost command acknowledgement before any new command. Standard frames remain 4 MiB and event/list inline pages 256 KiB. Independent fixtures include >4 MiB Notes, Slate and Task projections and permission revocation between ranges.

## Account operation semantics

The new identity/workspace/device operations above use the existing error registry. Read/list/preview operations are Q/R1/AO; listAuthProviders is anonymous, bounded and no-store. Profile and credential rename are IW/R2/FR with expectedRev. Email change and recovery/password/SSO proof flows are NI/FR, rate-limited and one-use, never automatically retried. Generating recovery codes is NI/R3/FR with fresh step-up; losing the response requires generating a new set that atomically invalidates the previous one. API token creation is CC/R3/FR with fresh step-up and caller tokenId; a duplicate returns its safe summary with secret absent, never redisplays the secret (the success secret field is optional). Token revocation and device sign-out are DE/R3/FR; reducing one's current device access requires no step-up, but increasing remote authority does. setRemotePolicy is IW/R3/FR with expectedRev and step-up for any expansion. Data deletion is CC/R4/FR with current previewHash and step-up. It does not cancel a paid subscription or delete the account. Deletion status/cancellation accepts only fresh purpose=cancelDeletion sessions during grace; cancellation is IW with the deletion revision carried by ResponseMeta. Old ordinary sessions remain revoked after cancellation; normal login is required.

Browser begin/complete authentication mirrors providerId/purpose and returns SessionView plus Set-Cookie only. Recovery, email change and all secret-returning account management responses are no-store and never placed in telemetry/cache; a PAT secret may be displayed once in its explicit creation UI but is not used as the browser's session credential. Native Device SSO is unavailable on a browser. Its separate target bootstrap flow uses the signed device challenge and bound installation, not an ordinary caller bearer minted for a different app. [Security architecture](../08-security-architecture.md#account-and-provider-closure) fixes the remaining owner state transitions.

## Notes structural and Slate operation bindings

Notes previewMoveDocument is Q/R1/FR; commit remains IW/R2/FR. Same-notebook moves use an empty classificationMap; cross-notebook moves require a complete mapping and preview hash. Local preview binds all composite local tokens, Cloud preview all committed revisions. Move success returns exact resulting tokens for the document and every changed source/destination notebook (at most three unique roots), including unchanged notebook tokens when placement does not mutate that root; the outbox acknowledgement applies this returned set atomically. An offline preview is revalidated against the same frozen target semantic definitions at Cloud submission; changes refuse with preserved pending state. Sync body replacement may create a new document at a validated initial placement, but cannot change an existing document's placement or bypass the named structural commands.

task.startTranscription is CC/R3/FR, current owner/session, explicit source-upload consent and the normal paid Task admission/extra-usage policy; Task/Resource admission records and source pins use the existing shared families. The sole RunWorkflow executes the fixed ASR stage. PrepareTranscription is local CC/R2/FR with expectedNative, producing an extraction ProductJob and audio-manifest artifact without uploading. AdoptTranscript is local IW/R3/FR with expectedNative, a reviewed timeline diff and ordinary local approval/undo. The current sequence revision must match the preview; a transcript from an older source can be adopted only after an explicit new review against the current timeline, never guessed retiming. ImportSubtitles is IW/R2/FR with expectedNative and acknowledged loss report; ExportSubtitles is CC/R2/FR with caller commandId and pinned expectedNative. Large transcript/project payloads use immutable body references. These operations enter the generated capability/schema registry and the existing local transport classes, not a generic Invoke escape hatch.
