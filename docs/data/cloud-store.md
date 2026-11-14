# V2 Center data model and migration

Status: target PostgreSQL specification, not an executed migration. `AFV2-BASE-01` owns inventory/preflight; `AFV2-CENTER-01` owns the guarded PostgreSQL transition and real fixture qualification; CENTER-02/03/04 respectively own channel, typed control and bounded delivery. `AFV2-ID-01` and `AFV2-HOST-02` add account/commerce state. Final runtime cutover is `AFV2-MIG-01`, followed by live-schema contraction in `AFV2-MIG-02`. The companion [cloud-store.sql](cloud-store.sql) specifies new tables/constraints against the retained Go schema; it is not executable SQLite and does not replace the product's migration runner.

## 1. Baseline and authority

Audited Cloud `main` is `6df33c525fcbc20495e46c9c4c011086146da796`. The Go source embeds migrations `0001` through `0011`. Existing production evidence in the frozen Plan reports schema 10 and Hello-only serving; The historically delivered file-management work's external bridge qualification/publication/successor deployment remains deferred. Therefore the source containing migration 0011 is not evidence that every deployment already applied it.

The existing runner uses a direct migration-role connection, exclusive advisory lock, numbered transactions and SHA-256 checksums. It refuses edited/missing applied migrations and a database ahead of the build. The V2 plan retains those guarantees. Runtime uses the separate pooled least-privilege role. Credentials are never copied to reports, manifests or user-facing examples.

| Existing schema/assets | Decision | V2 responsibility |
|---|---|---|
| `platform.schema_migration`, runtime credential generation/floors and restore admission | KEEP / REWORK | Versioned migration and safe cutover; retain old applied checksum history |
| `platform.command_receipt`, inbox/outbox, job lease | KEEP / REWORK | Account mutations, billing delivery/reconciliation and operation receipts; no user Task scheduler |
| `audit.audit_event`, `audit.chain_head` | KEEP | Content-free security/control audit and tamper-evident append protocol |
| `identity.*`, `device.*` | KEEP / REWORK | Accounts, passkeys, sessions, step-up and device/installation identity |
| `entitlement.*` | KEEP / REWORK | Hosted management service terms/grants; retired products remain historical records |
| `fleet.node`, enrollment flows, signing keys and hub lease | KEEP / REWORK | Node registration/key identity, fenced channel ownership; naming does not imply old task product semantics |
| `identity.mobile_authorization` | REMOVE after migration/retention | No V2 mobile route or runtime writer; revoke pending flows before contract phase |
| `fleet.routed_call`, `routed_file_call`, `routed_file_target`, old command namespace | REMOVE from runtime after cutover; archive/tombstone existing facts | Historical outcomes are never replayed as V2 commands |
| C# D1 module tables/storage bridge | REMOVE from V2 runtime/deploy | Qualified export/archive for any actual retained data; no automatic fiction that D1 contains production business state |

Core Sandbox configuration, Runs, resource limits, output and files stay in the local Node store. Center has no authoritative Sandbox/Run table and stores no command arguments, environment values, terminal output or file contents. A stale dashboard cache never overwrites Node state.

## 2. V2 tables and invariants

### 2.1 Enrollment protocol epoch

`management.node_protocol` binds an existing enrollment/account/Node triple to protocol major 2 and a fresh protocol epoch. Revoking/re-enrolling changes that binding. A unique composite key on the retained enrollment table supports a database-enforced ownership foreign key. This record is not a replacement for session verification, channel proof or local remote grants.

Capabilities and resource telemetry are volatile bounded snapshots. Persisted registry fields retain only version, OS/arch and last-seen information already authorized for device management. Local grant authority stays on Node; any Center/UI summary includes its revision/freshness and cannot authorize a call by itself.

### 2.2 Command namespace and routing result

`management.command_identity` is immutable. `(account_id, command_id)` is unique across V2 management commands and imported V1 tombstones. It binds namespace, enrollment, method, canonical intent digest and creation/replay boundary. V2 identities additionally store the original 16-byte `node_owner_epoch`; the remote-operation foreign key binds that same epoch. This is the durable Node store authority, not the enrollment/protocol/channel epoch. Reusing the ID against another target, method or owner epoch is a conflict. Reconnect and a fresh Handshake cannot rebind an admitted command. Legacy tombstones have no Node owner epoch and cannot be used as V2 operations; migration does not invent an epoch for old commands.

`management.remote_operation` contains routing state, monotonic “may have delivered”, delivery count, current hub/channel epoch, result reference/digest and timestamps. It stores no request or response body. The authoritative Core receipt is queried when a full result is needed. For an offline Node, Center may report the last verified outcome/reference but must identify its provenance and freshness rather than fabricate a current Core result.

| Stored state | Integer | Meaning |
|---|---:|---|
| `ACCEPTED` | 1 | Admission committed; after a process crash treat as possibly delivered |
| Reserved | 2 | Never written; preserved numbering prevents ambiguity with old receipts |
| `SUCCEEDED` | 3 | Verified successful Node result |
| `FAILED` | 4 | Verified Core failure with the result's effect classification |
| `REJECTED` | 5 | Node rejected before the requested effect |
| `EXPIRED` | 6 | Delivery/replay validity expired; an earlier unknown effect remains separately indicated |
| `UNKNOWN` | 7 | May have reached the Node, no verified final outcome |
| `NOT_DELIVERED` | 8 | Every delivery so far is proved not to have happened |

Run states such as `DRAINING` or `RECOVERY_REQUIRED` are not routing states. In particular a process root exiting does not prove the managed group empty; the Center reports the Node's state without inferring `EXITED` from a disconnected channel or raw executor exit code.

The implementation migration supplies guards equivalent to the current immutable identity/final-result triggers: command identity never changes, delivery count cannot decrease, `may_have_delivered` never becomes false once true, and a terminal result cannot be overwritten. A request is admitted under the current hub lease fence; loss of the lease prevents later admission and a successor conservatively marks abandoned accepted calls unknown. The SQL document records row-level shape; cross-row transaction/trigger invariants must also be implemented and tested.

`method` is a closed generated route identifier, not a user-provided SQL/function name. The migration-owned `management.method_catalogue` contains only approved V2 remotely callable mutations; local terminal operations never enter it. Runtime has read-only access to the catalogue. C#/Go fixtures bind route, permission and digest rules.

`management.cutover_receipt` is migration-role-only evidence bound to source/target schema, database identity, artifact/backup manifests and retired writer set. Its phases are prepared, writers fenced, schema verified and ready. Readiness for a restored database must be established for that target; copying a source receipt cannot authorize it.

### 2.3 Hosted commerce

The new `commerce` schema is a bounded web-subscription model: `commerce.customer` stores account/provider associations; `commerce.checkout` reserves purchase intent before an external provider call; `commerce.subscription` stores the verified canonical snapshot; `commerce.provider_event` records unique webhook identities/digests; `commerce.billing_entry` records immutable normalized financial facts. They reference the retained account and entitlement store rather than duplicating them. Only the admitted web provider/environment pair can be written; adding a provider requires a later explicit design decision.

Provider event receipts store the event identity/digest, allowlisted event kind and provider resource reference. Processing reconciles the authoritative subscription/transaction through the provider adapter and writes entitlement facts plus outbox/audit atomically. The raw webhook body and card details are not retained. An interrupted reconciler can re-read provider state from the saved reference; where the provider cannot recover required evidence, the event stays pending/manual review and grants no invented term. A normalized billing row contains amounts/currency from verified provider facts; it is not a product price definition.

The companion SQL uses canonical subscription values: 1 `PENDING`, 2 `ACTIVE`, 3 `CANCEL_AT_TERM_END`, 4 `PAYMENT_GRACE`, 5 `EXPIRED`, 6 `REVOKED`, 7 `PROVIDER_UNKNOWN`. `NOT_CONFIGURED` is deployment/catalog state, not a fake customer subscription. Provider event states are 1 `RECEIVED`, 2 `APPLIED`, 3 `RETRY`, 4 `REJECTED`, 5 `OBSOLETE`; all transitions preserve original event identity/digest.

### 2.4 Account recovery, deletion and export

`AFV2-ID-01` owns these additions after the base transition. `identity.account_security_state` supplies a durable account-level authentication/recovery epoch; migration derives a nondecreasing starting value from retained session/proof facts under writer fencing. New sessions and operation-bound proofs bind current epochs. Recovery completion increments the recovery generation and revokes existing session/enrollment authority atomically. Session verification must check current account epochs, not merely return the generation embedded in an old session.

`identity.lifecycle_operation` holds the stable recovery/deletion/export identity, intent/plan revision, proof linkage, state and bounded temporary export metadata. Kind values are 1 recovery, 2 deletion, 3 export; states are 1 awaiting proof, 2 confirmed, 3 processing, 4 completed, 5 failed, 6 expired, 7 revoked. One live deletion plan exists per account. Extend the existing typed one-use flow/proof storage through a new migration without reinterpreting its old kind values; linkage and completion validate account, operation, expiry, generation and proof use in the same transaction. No raw proof/token or export body is stored in the new receipt.

Deletion uses the existing account states 4 pending deletion and 5 deleted, with non-personal retained identity tombstones where reference/replay retention still requires them. It revokes remote authority before asynchronous provider/retention cleanup and never sends local stop/delete. Export artifact IDs are opaque application identifiers, never caller-provided host paths; protected temporary content is bounded and expires. The lifecycle acceptance covers duplicate confirmation, proof replay, revoke races, epoch mismatch, cleanup/provider failure and export authorization/expiry.

## 3. Transactions, concurrency and privilege

Use the existing `store.DB` bounded transaction wrapper and parameterized SQL. The route adapter never supplies SQL/table names. Each transaction has a deadline and bounded serialization-conflict retry only when retrying the database transaction cannot repeat an external effect. External Node sends and provider calls occur outside an open database transaction and are reconciled through their durable identity.

Mutation admission commits command reservation and its audit before a send. A send is tied to its current transport generation. Settlement verifies the original identity and may-have-delivered state; a failed settlement leaves a conservative accepted/unknown row. Concurrent same-command calls join/reconcile the same operation; they do not each open a new Run.

The migration role owns DDL, method catalogue, credential provisioning and retention purge. Runtime has only enumerated `SELECT`, `INSERT` and necessary guarded `UPDATE`; no broad schema ownership, role management, `DELETE`, `TRUNCATE`, trigger or function privileges. Provider event processing/entitlement writing is an explicit participant of one transaction, not arbitrary cross-module writes. Audit append follows the existing chain/lock protocol.

## 4. Retention and erasure

No routine background sweep deletes a deduplication key while an authorized sender could still replay it. After a verified terminal result's replay boundary, compact the payload-free routing result if allowed, retaining a small command identity tombstone for the live enrollment. If the configured receipt storage budget is exhausted, reject new remote mutations with a precise resource limit; do not free space by forgetting executable command identities.

An unknown outcome cannot be compacted as successful or not delivered. It remains reconcilable until Node evidence or an explicitly audited operator disposition establishes the retained outcome. Disposition never authorizes rerunning the old command under a new ID automatically.

Once an enrollment is revoked and every signed-call/replay validity boundary has passed, its tombstones may be purged only under the documented retention policy, after confirming that old credentials/epochs can no longer be admitted. Delete child operation/tombstone rows before the revoked enrollment. Account erasure preserves only justified financial/security records under approved policy and irreversibly removes remote authority; it never deletes local Sandbox data automatically.

Existing flow/receipt/audit retention policies must be carried into the new acceptance register with exact configured periods and tests. A setting marked TBD is a production activation prerequisite, not a hidden unbounded retention promise. The old source's comments about future sweeps are not evidence a sweep already exists.

## 5. Finite migration sequence

`AFV2-BASE-01` first records actual deployment identities, schema versions, checksums, runtime credential generations, available backup/restore evidence, and whether retained D1 data exists. `AFV2-CENTER-01` implements and qualifies the guarded transition on isolated fresh/schema10/schema11 databases; it does not depend on the late runtime-removal task. The cutover procedure below is executed only after its real admission prerequisites, with final old-route/consumer retirement in `AFV2-MIG-01` and live-schema contraction in `AFV2-MIG-02`. No production probing or modification is authorized by this documentation task.

### 5.1 Common preparation

1. Freeze new V1 remote submissions and record unresolved V1 routed outcomes. Do not convert an old Task into a new Run or replay it through MXC.
2. Produce a restore-tested backup with source database/cluster identity, migration checksums, runtime-generation inventory and schema/row-count manifest. Preserve old data under the reviewed backup access boundary.
3. Build and qualify an exact V2 transition artifact on the native gates, using the existing protected candidate/provenance path. The artifact has a bounded migration role and no implicit activation of product surfaces.
4. Drain legacy Center writers/channels, fence all legacy runtime credentials/role memberships and terminate or prove absence of their open writer sessions. A password rotation or a role-name string alone is not proof that old writers cannot return.
5. Under the migration lock and required table locks, establish the cutover/restore-admission receipt bound to the verified artifact, database identity, backup and retired credential generations. Apply versioned SQL without editing any previously applied file.
6. Create V2 protocol epochs and import legacy command identities as non-executable tombstones. Reconcile counts/hashes and retain unresolved outcomes. Do not insert old task/file results as successful V2 operations.
7. Provision fresh least-privilege V2 runtime credentials, register V2 methods, deploy the verified Go/Worker/Blazor cohort with V1 routes removed and V2 surfaces dark. Nodes must negotiate V2 and require fresh local grants.
8. After V2 restore/rollback and consumer-cutover acceptance, contract old runtime tables/branches in a new numbered migration. Retained archive files/migration checksums are historical data, not an executable dual product.

### 5.2 Starting-state matrix

| Starting database | Required path | Forbidden shortcut |
|---|---|---|
| Truly fresh | Existing fresh-bootstrap checks; immutable `0001..0011`; V2 expansion; new role/epoch issuance | Calling an existing database “fresh” because a few tables were emptied |
| Schema 10 or earlier retained Go deployment | Qualify a published V2 security successor/transition path; prove retirement of old writers; satisfy the current 0011 guard/floor invariants, then expand to V2 | Append 0012 and assume 0011 will pass; manually insert migration records; remove the hard stop; reuse the stale legacy bridge |
| Schema 11 with valid admission | Verify existing credential floor/restore admission and backup identity; fence its writers; apply V2 expansion and new epoch | Assuming a copied/restored schema-11 database inherits the source's ready admission |
| Incomplete/unknown or ahead-of-build schema | Refuse writes; inspect with migration status; restore or use a separately reviewed forward migration | Force mode, checksum rewrite, arbitrary SQL or downgrade of applied schema |
| Historical D1 data actually present | Explicit allowlisted identity/entitlement import or owner-approved archive, with no token/key transplant; verify reference and audit relationships | Blindly copying all old AI/Task/Commerce tables into PostgreSQL |

Current source `RequireCTR06SecurityBridge()` returns `ErrCTR06SecurityBridgeUnbound`; the hosted/public old proof is refused. This is an implementation blocker for an existing schema-10 upgrade until the new transition artifact is qualified. `AFV2-CENTER-01` must replace the exact obsolete artifact binding through reviewed engineering, preserving proof of writer retirement and restore admission. A CLI `--force`, user-supplied assertion or edited checksum is not an acceptable replacement. The Plan must make this a prerequisite of deployment, not an unexplained future research item.

### 5.3 Rollback boundaries

Before any V2 effect: stop the candidate, restore the qualified backup in isolation, verify its admission/credential state and deploy the exact compatible earlier artifact through the guarded rollback process. Never re-enable a legacy writer against a contracted V2 schema.

After a V2 command, credential or commercial event has been committed: application rollback is only to a build that understands the expanded V2 schema/receipts. Otherwise keep service offline and repair forward. A full restore requires a reviewed recovery of post-backup outcomes and external payment facts; losing those facts and replaying commands is unacceptable. A backup is not an authorization to duplicate a Run or a charge.

After contract/destructive migration: old V1 binaries are permanently incompatible with the serving schema. Retire the temporary transition executable and rollback deployment branch after its documented acceptance point. Preserve the restore procedure and archive identity, not live old Task/Execution services.

## 6. Schema acceptance

Run the real PostgreSQL migration chain, not SQLite emulation. Test fresh, schema-10, schema-11 and interrupted transition fixtures; changed/missing migration refusal; concurrent migrations; runtime role least privilege; old-writer rejection including open sessions/membership paths; copied-backup admission; backup restore; cross-account foreign keys; duplicate command/different intent; unknown settlement; immutable terminal results; receipt compaction replay rejection; revoked epoch; and provider event concurrency/out-of-order recovery.

The document checker may validate PostgreSQL schema structure and references, but must label that as static validation. Only the real PostgreSQL fixture tests satisfy SQL execution/migration acceptance. Both native repository gates remain required; designated-host or external evidence that is unavailable stays `NOT PROVEN` with a named owner.
