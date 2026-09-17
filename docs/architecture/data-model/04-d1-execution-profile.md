# D1 Execution, Physical Storage and Recovery Profile

Authority: P2-012. Applies to the complete [Cloud logical model](01-cloud-data-model.md) and its transaction families; it replaces PostgreSQL implementation choices. This is a design specification, not evidence that D1 has been deployed or load tested.

## 1. Authority and deployment unit

One D1 database named `business-<realm>` holds the twenty existing module owners for one deployment realm. Account, workspace, membership, entitlement, credit, task, chat, sync, resource, audit and receipts retain their existing logical ownership. A realm is an existing identity/security/deployment boundary, not an automatically created shard. No current transaction spans two D1 databases. Independent realms use the existing explicit export/migration procedure; transparent account or workspace sharding is not part of this release and must not be improvised in implementation.

C# Native AOT owns authorization, validation, pricing, state transitions and query interpretation. Cloud's Worker owns ingress, Container selection and private access to bindings. The Container accesses the virtual host `storage.internal` through a Cloudflare outbound handler; ordinary Internet egress is disabled and only explicitly configured binding/provider destinations are admitted. The handler accepts generated internal `ExecutePlan` requests, not public SQL. Worker code executes a fixed plan and encodes results; it does not duplicate C# business decisions. The exact blocked-egress/handler configuration is a WP06/21 deployment test.

DOs own only coordination/projections: `ApplicationPresence` by realm/workspace/product/installation, `RunStream` by execution ID/generation, and `EventFeed` by authorized scope. The Container controller DO manages container lifetime, not customer data. Queues carry durable wake hints referencing D1 outbox IDs; duplicate/lost/late deliveries cannot change business truth. KV may cache public/configuration data, never positive authorization or balances. R2 owns object bytes; D1 owns their admitted references, verification/pins/quota and publication. Vectorize is rebuildable search data.

## 2. Physical mapping for every logical table

For every module table in model01, physical name is `<module>_<snake_case_entity>`; dotted SQL schemas become prefixes. Preserve declared columns, ownership keys, unique constraints, FKs, revision and tombstones. The schema generator emits migrations/column-map fixtures from a checked-in physical manifest in Cloud, reviewed against the logical model; the Design model is not an alternate production ORM. No inferred auto schema creation occurs on startup.

| Logical type / rule | D1 representation and boundary |
|---|---|
| UUID / opaque Id | canonical lowercase UUID `TEXT`, validated length/format; owner IDs composite-indexed; no Guid-memory-byte reinterpretation |
| Signed exact64 counters / instants | `INTEGER` where range is signed64; instants are UTC microseconds. JS binds canonical decimal strings with SQL `CAST(? AS INTEGER)` and returns `CAST(column AS TEXT)`; no JS Number conversion. C# validates range before submission. |
| uint64 / Slate exact rational / Notes decimal / monetary decimal | canonical `TEXT` with explicit component columns where specified. C# checked exact arithmetic; SQL never sums/coerces arbitrary decimal text to REAL. Money balances with declared fixed unit may use signed64 only after range proof. |
| Ordering exact decimal / unsigned values | owner-generated canonical sort key as BLOB plus identity tie-breaker; reference comparator vectors define equality/order. Never lexicographic raw decimal text. |
| bool / enum | checked INTEGER0/1; closed enum numeric registry with unknown read preservation where specified |
| bounded structured values | validated JSON `TEXT`, `CHECK(json_valid(...))`; authoritative predicates use typed columns, not arbitrary JSON searches |
| binary / secret hash | BLOB, tagged byte encoding over the private bridge; secret plaintext absent |
| immutable large body or artifact | R2 object/version/hash reference with existing verification/pin/retention rules; bounded metadata only in D1 |
| row ownership / query | every query predicates realm's authenticated account/workspace and, for assistant-derived objects, product scope. No unscoped query followed only by UI filtering. |

Foreign keys are enabled. All mandatory owner references and uniqueness follow model01. A physical migration must enumerate its logical rows/constraints/indexes and prove exact read/write round trips in C#/Worker; SQLite passing alone is insufficient. No PostgreSQL extensions, advisory locks, sequence object, stored procedure, LISTEN/NOTIFY or ORM change tracking is required.

## 3. Private named plan protocol

`Cloud.Storage.D1` exposes typed repository methods, not a public SQL connection. Each method maps to a versioned named plan such as `identity.consume-flow.v1`, `chat.commit-turn.v1`, `task.claim.v1`, `commerce.settle.v1` or `sync.publish.v1`. `storage/plans/<owner>/<name>.sql` is reviewed Cloud-owned code. A build step emits the Worker SQL dictionary and C# typed bind/result adapters with one SHA256 plan-manifest identity. No client supplies SQL text or table names. Deploy only a mutually supported plan manifest; unknown plan/version fails before execution.

Internal request fields: `planId`, `planVersion`, `manifestHash`, `requestId`, `recoveryGeneration`, `ownerScope`, typed `arguments`, `deadlineUtc`. Response: `requestId`, `manifestHash`, `rows` with tagged exact scalars, `changes`, `bookmark?`, `failure` from `invalidPlan/staleGeneration/precondition/constraint/overloaded/unavailable/unknownOutcome`. Bounds:256KiB request/result,100 arguments per statement,100 statements per batch and a10s caller deadline; large reads page or return object references. Unknown outcome after a timeout requires receipt lookup, not a new command ID. The binding endpoint is unavailable from public routes and validates the trusted container identity and active deployment generation. Request logging includes plan ID/timing only.

Writes and authorization-sensitive reads use the primary. Initial release uses primary reads throughout; adding read replicas later may use D1 Sessions/bookmarks only for explicitly stale-safe projections. A bookmark cannot turn an expired credential into a valid one. Stream authorization refreshes also read current authority.

## 4. Atomic command algorithm and SQL

All current shared-unit families remain one `D1Database.batch()` invocation: guard current owner authorization/revisions/lease/generation; mutate owned rows; store immutable result/receipt; append sync/event/outbox/change-archive rows; commit. Do not perform a remote call, provider effect or another binding request inside this commit. Pre-read data used by C# calculations is validated again by guarded revisions in the batch. If it changed, discard the calculation and return the existing conflict/retry classification.

The following minimal executable SQL illustrates the required safety mechanism. Actual owner tables use the full model01 schemas.

```sql
CREATE TABLE command_guard (
  command_id TEXT PRIMARY KEY,
  allowed INTEGER NOT NULL CHECK (allowed = 1)
);
CREATE TABLE command_receipt (
  scope TEXT NOT NULL, command_id TEXT NOT NULL, request_hash TEXT NOT NULL,
  result_json TEXT NOT NULL CHECK (json_valid(result_json)),
  PRIMARY KEY(scope, command_id)
);
CREATE TABLE owner_example (
  scope TEXT NOT NULL, id TEXT NOT NULL, revision INTEGER NOT NULL,
  value TEXT NOT NULL, PRIMARY KEY(scope,id)
);
CREATE TABLE event_outbox (
  sequence INTEGER PRIMARY KEY AUTOINCREMENT, scope TEXT NOT NULL,
  command_id TEXT NOT NULL, event_key TEXT NOT NULL,
  payload_json TEXT NOT NULL CHECK (json_valid(payload_json)),
  UNIQUE(scope,command_id,event_key)
);
-- All five statements below are ONE prepared batch; arguments are bound.
INSERT INTO command_guard(command_id,allowed)
SELECT :command_id, CASE WHEN EXISTS (
  SELECT 1 FROM owner_example
  WHERE scope=:scope AND id=:id AND revision=:expected_revision
) THEN 1 ELSE 0 END;
UPDATE owner_example SET value=:value,revision=revision+1
WHERE scope=:scope AND id=:id AND revision=:expected_revision;
INSERT INTO command_receipt VALUES(:scope,:command_id,:hash,:result_json);
INSERT INTO event_outbox(scope,command_id,event_key,payload_json)
VALUES(:scope,:command_id,'owner.changed',:event_json);
DELETE FROM command_guard WHERE command_id=:command_id;
```

Named bindings above are explanatory; generated D1 statements use positional bindings in the same order. A false precondition violates the CHECK, rolling back the entire batch. An affected-row count of zero by itself is never the guard. No transaction can observe a retained successful guard row. Each real plan folds all authorization/current version/lease/capacity predicates into its guard. On guard failure, perform a current diagnostic read and map to the existing typed auth/conflict/capacity refusal; the mutation did not commit. On duplicate receipt-key failure, read that receipt: same hash returns its original result, different hash returns idempotency conflict. Never report unknown-effect as safe retry.

Ledger/credits calculations are performed in checked C# arithmetic against captured balance/version. The batch guards that version and active policy/authorization, writes ledger/debit/entitlement changes and receipt/outbox atomically. No floating-point money or “debit then repair later” adapter is admitted. Authentication flow consume, session rotation and recovery-code consume use the same guarded compare-and-consume. Cross-owner business transitions use the existing module ports to assemble one declared commit plan, not nested commits.

## 5. Claim, publish and reconcile

Claims update `lease_owner`, `lease_until`, `fence` under a guard over due state and expired/current lease; time is a trusted UTC value constrained by the request deadline. Attempts carry monotonically increasing fences. A worker result guards its current fence and state; a stale worker cannot finalize after takeover. Timeouts leave the durable claim/receipt inspectable. ProductJob/Task/SimulationRun meanings remain distinct.

Every successful commit allocates a sequence in its transactional outbox. Event/sync feed publication advances only through committed ordered rows in that scope; no skipped unpublished row can be hidden by a later watermark. Per-scope cursors also carry recovery generation and application scope. A dispatcher publishes wake messages and marks acknowledgements idempotently. Consumer inbox uniqueness is `(consumer, eventId, generation)`; duplicate Queue/Workflow delivery cannot repeat a business effect. DO feeds cache these durable facts; lost DO projection triggers snapshot/backfill.

Cron runs every minute and wakes bounded D1 outbox/schedule scans; Queue consumers call the same Container job endpoints for retries. Each C# job handles at most100 items or20s, checkpoints/commits and returns; further work is rescheduled. All former perpetual hosted-service loops become these bounded entry points in the same C# image. Simulator segments preserve deterministic sequence/checkpoint semantics; process sleep changes wall-clock completion only, never the generated sample values. Schedule occurrence IDs and unique admission rules remain authoritative in D1.

## 6. Migration, load and failure envelope

Migrations run from the gated deployment job, never Container startup. Keep expand → versioned bounded backfill → dirty-range/fence verification → switch → soak → contract. Backfills use guarded owner revision/tombstone comparisons,100-row pages and receipts; stale converted data cannot overwrite a new write. Release manifest pins D1 schema/read/write horizons, C#/Worker plan hashes, DO migrations, Workflow version and Contracts. Rollback retains additive state and restores compatible application versions; irreversible contract requires forward repair or fenced DR.

D1's hard10GB/database capacity is explicit. Alert at60% and70%, forbid new-tenant onboarding at80%, and reserve remaining space for existing customers, receipts, deletion and recovery. At90%, reject growth-heavy admissions with the existing capacity/unavailable reason before accepting content; permit bounded reads, cancellations, exports, deletions and settlement from reserved capacity. This is an operational admission constraint, not loss of existing data. Daily growth forecasts and production-shaped load tests must demonstrate at least30days of headroom and the accepted latency/concurrency budget before paid launch. No “request a larger D1 database” recovery is claimed. Reduce only rebuildable data, export/archive eligible retained records, or execute an explicitly planned realm migration; do not silently split a transaction family. Object quotas remain R2 quotas, not a promise of unlimited relational metadata.

Overload uses bounded jittered retries only for reads or receipt-proven safe operations. No hot infinite polling. Container cold starts return bounded retryable unavailability before command admission if the deadline cannot be met. Health separates ingress, Container readiness, D1, DO feed, R2, Vectorize and AI. Run/stream/queue budgets are measured in WP06/21/24/46; current documentation does not prove cost or throughput.

## 7. Backup and disaster recovery

Retain metadata RPO≤5min, blobs≤15min and critical-service RTO≤4h. Paid D1 Time Travel (30days) is useful for in-place incidents; it does not create a second database and does not by itself satisfy independent disaster recovery. Snapshot/export jobs create a D1 SQL export with its bookmark and a signed schema/plan/object manifest. Exports are promoted only after verification and copied to the existing separate-account AWS S3 COMPLIANCE30day archive. This is the explicit disaster-copy exception to the Cloudflare runtime baseline. R2 remains primary storage.

Every authoritative batch also appends a bounded replay record containing its ordered sequence, schema version, resulting row revisions/after-images and deletion keys, excluding temporary/local-history bodies and credentials. Large eligible canonical bodies use already pinned R2 references. The archive worker copies contiguous committed records at least every minute; it advances a signed backup watermark only after independent storage acknowledges. A daily consistent D1 export provides the base; replay selects records strictly after its captured sequence. The export procedure gates writes briefly to establish a matching sequence/bookmark before initiating the provider-consistent export; measured pause/time and resume behavior must pass WP46. No snapshot assembled from unrelated paginated live reads is accepted. Retain change records until all dependent backups expire.

At4min metadata archive lag (12min blobs), alert and stop new external-effect/content admissions that would violate recovery commitments; continue retry/reconciliation and show incident state. The backup gate fails if actual RPO is exceeded. Restrictive security facts and external dispatch intent still use the independently retained signed safety journal before success/effect dispatch as specified in deployment22. Archive recovery records alone do not substitute for that journal.

For fresh-environment restore: fence old ingress/credentials; allocate a greater independent recovery generation; import a verified base export into a fresh D1 database; replay contiguous change records to the chosen point; restore and verify R2 references; replay restrictive deletion/revocation/intent facts; invalidate sessions, upload grants, cursors, leases and DO projections; reconcile unknown external effects; rebuild search; reopen only after invariants and health pass. In-place Time Travel follows the same generation/journal/fence procedure. Incomplete archive or safety-journal inventory keeps mutation/dispatch closed. Never infer an absent provider attempt did not happen.

## 8. Derived search

D1 FTS5 indexes admitted Cloud text; Vectorize holds the existing versioned1024-dimensional Workers AI embeddings with metadata realm/workspace/product/source/content revision/index generation. Neither is canonical content. The query service resolves candidates, then checks current owner authorization, deletion and revision before exposing snippets/citations. A stale vector cannot reveal another app's source. Exact Notes scalar predicates/order use the fixed scalar evaluator/sort keys, not vector/FTS score. Rebuild new generations beside old, atomically switch the active pointer after completeness checks, then remove old data. Missing Vectorize yields explicitly lexical-only completeness; missing canonical access never yields cached text. Per-application caches and context budgets remain mandatory.

Primary research: [D1 batch](https://developers.cloudflare.com/d1/worker-api/d1-database/#batch), [limits](https://developers.cloudflare.com/d1/platform/limits/), [SQL extensions](https://developers.cloudflare.com/d1/sql-api/sql-statements/), [Time Travel](https://developers.cloudflare.com/d1/reference/time-travel/), [Container bindings](https://developers.cloudflare.com/containers/configuration/workers-connections/). Checked2026-09-16; real provider behavior remains a release gate.
