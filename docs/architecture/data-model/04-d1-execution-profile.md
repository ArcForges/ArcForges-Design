# D1 Execution, Physical Storage and Recovery Profile

Authority: [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012). Applies to the complete [Cloud logical model](01-cloud-data-model.md) and its transaction families; it replaces PostgreSQL implementation choices. This is a design specification, not evidence that D1 has been deployed or load tested.

## 1. Authority and deployment unit

One D1 database named `business-<realm>` holds the twenty-one module owners for one deployment realm. Account, workspace ownership, entitlement, credit, task, chat, sync, resource, audit and receipts retain their existing logical ownership. A realm is an existing identity/security/deployment boundary, not an automatically created shard. No current transaction spans two D1 databases. Independent realms use the existing explicit export/migration procedure; transparent account or workspace sharding is not part of this release and must not be improvised in implementation.

C# Native AOT owns authorization, validation, pricing, state transitions and query interpretation. Cloud's Worker owns ingress, Container selection and private access to bindings. The Container accesses the virtual host `storage.internal` through a Cloudflare outbound handler; ordinary Internet egress is disabled and only explicitly configured binding/provider destinations are admitted. The handler accepts generated internal `ExecutePlan` requests, not public SQL. Worker code executes a fixed plan and encodes results; it does not duplicate C# business decisions. The exact blocked-egress/handler configuration is a WP06/21 deployment test.

DOs own only coordination/projections: `ApplicationPresence` by realm/workspace/product/installation, `RunStream` by execution ID/generation, `SimulationPacer` by simulation run/generation, and `EventFeed` by authorized scope. The Container controller DO manages container lifetime, not customer data. Queues carry durable wake hints referencing D1 outbox IDs; duplicate/lost/late deliveries cannot change business truth. KV may cache public/configuration data, never positive authorization or balances. R2 owns object bytes; D1 owns their admitted references, verification/pins/quota and publication. Vectorize is rebuildable search data.

## 2. Physical mapping for every logical table

For every module table in model 01, physical name is `<module>_<snake_case_entity>`; dotted SQL schemas become prefixes. Preserve declared columns, ownership keys, unique constraints, FKs, revision and tombstones. The schema generator emits migrations/column-map fixtures from a checked-in physical manifest in Cloud, reviewed against the logical model; the Design model is not an alternate production ORM. No inferred auto schema creation occurs on startup.

| Logical type / rule | D1 representation and boundary |
|---|---|
| UUID / opaque Id | canonical lowercase UUID `TEXT`, validated length/format; owner IDs composite-indexed; no Guid-memory-byte reinterpretation |
| Signed exact 64 counters / instants | `INTEGER` where range is signed 64; instants are UTC microseconds. JS binds canonical decimal strings with SQL `CAST(? AS INTEGER)` and returns `CAST(column AS TEXT)`; no JS Number conversion. C# validates range before submission. |
| uint64 / Slate exact rational / Notes decimal / monetary decimal | canonical `TEXT` with explicit component columns where specified. C# checked exact arithmetic; SQL never sums/coerces arbitrary decimal text to REAL. Money balances with declared fixed unit may use signed 64 only after range proof. |
| Ordering exact decimal / unsigned values | owner-generated canonical sort key as BLOB plus identity tie-breaker; reference comparator vectors define equality/order. Never lexicographic raw decimal text. |
| bool / enum | checked INTEGER0/1; closed enum numeric registry with unknown read preservation where specified |
| bounded structured values | validated JSON `TEXT`, `CHECK(json_valid(...))`; authoritative predicates use typed columns, not arbitrary JSON searches |
| binary / secret hash | BLOB, tagged byte encoding over the private bridge; secret plaintext absent |
| immutable large body or artifact | R2 object/version/hash reference with existing verification/pin/retention rules; bounded metadata only in D1 |
| row ownership / query | every query predicates realm's authenticated account/workspace and, for assistant-derived objects, product scope. No unscoped query followed only by UI filtering. |

Foreign keys are enabled. All mandatory owner references and uniqueness follow model 01. A physical migration must enumerate its logical rows/constraints/indexes and prove exact read/write round trips in C#/Worker; SQLite passing alone is insufficient. No PostgreSQL extensions, advisory locks, sequence object, stored procedure, LISTEN/NOTIFY or ORM change tracking is required.

## 3. Private named plan protocol

`Cloud.Storage.D1` exposes typed repository methods, not a public SQL connection. Each method maps to a versioned named plan such as `identity.consume-flow.v1`, `chat.commit-turn.v1`, `task.claim.v1`, `commerce.settle.v1` or `sync.publish.v1`. `storage/plans/<owner>/<name>.sql` is reviewed Cloud-owned code. A build step emits the Worker SQL dictionary and C# typed bind/result adapters with one SHA256 plan-manifest identity. No client supplies SQL text or table names. Deploy only a mutually supported plan manifest; unknown plan/version fails before execution.

Internal request fields: `planId`, `planVersion`, `manifestHash`, `requestId`, `recoveryGeneration`, `ownerScope`, typed `arguments`, `deadlineUtc`. Response: `requestId`, `manifestHash`, `rows` with tagged exact scalars, `changes`, `bookmark?`, `failure` from `invalidPlan/staleGeneration/precondition/constraint/overloaded/unavailable/unknownOutcome`. Bounds:256 KiB request/result,100 arguments per statement,100 statements per batch and a10s caller deadline; large reads page or return object references. Unknown outcome after a timeout requires receipt lookup, not a new command ID. The binding endpoint is unavailable from public routes and validates the trusted container identity and active deployment generation. Request logging includes plan ID/timing only.

Writes and authorization-sensitive reads use the primary. Initial release uses primary reads throughout; adding read replicas later may use D1 Sessions/bookmarks only for explicitly stale-safe projections. A bookmark cannot turn an expired credential into a valid one. Stream authorization refreshes also read current authority.

## 4. Atomic command algorithm and SQL

All current shared-unit families remain one `D1Database.batch()` invocation: guard current owner authorization/revisions/lease/generation; mutate owned rows; store immutable result/receipt; append sync/event/outbox/change-archive rows; commit. Do not perform a remote call, provider effect or another binding request inside this commit. Pre-read data used by C# calculations is validated again by guarded revisions in the batch. If it changed, discard the calculation and return the existing conflict/retry classification.

The following minimal executable SQL illustrates the required safety mechanism. Actual owner tables use the full model 01 schemas.

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

### Bootstrap and two-writer proof

Create a bootstrap_id record and retention pin with W=the current primary publication watermark and recovery generation in one guarded batch. Enumerate authorized roots/tombstones ordered by immutable `(kind,id)` using primary reads, fixed upper key bound and pages≤100/256 KiB. Copy rows with their actual owner revision to staged bootstrap pages; record each page hash and next key. Never page by updated_at/offset. Publication of the manifest requires all pages and the still-live pin; capture completion watermark H. Client applies each row only if its Cloud revision is newer, then replays feed `(W,H]` and continues normally. Preserve pending local edits separately. Pin expires after 15 minutes or 100 MiB metadata; purge pages after expiry/completion. Hard deletion cannot remove a tombstone while the corresponding pin/feed retention can require it.

Example: W=40; page reads A@5. A becomes 6 and publishes 41 before a later page. Replay 41 replaces 5 with 6. If the page instead read 6 first, replay 41 is idempotent. B created with a key below the current page cursor after W is obtained from its publication above W; deleted B is a tombstone above W. A commit not yet published when H is read appears in normal feed continuation after H, never silently excluded. This is convergence, not a claim that all pages describe one instant.

Publisher example: P and Q read watermark 40/rev 7/fence 3 and select C,D. P's batch guards watermark and both rows, assigns 41/42, advances watermark 42/rev 8. Q's guard fails and rolls back completely; it rereads before selecting. If C's predecessor is not yet published, neither publisher may select its successor first. A newly committed unrelated E does not invalidate C/D selection; it receives a later sequence. Lost acknowledgement rereads selected row sequence and watermark; it does not number them again. Bound selected rows so guard parameters and all statement/response limits remain within §3. These interleavings are executable SQLite transaction-vector tests plus separate real D1 integration evidence in WP21/25.

Cron runs every minute and wakes bounded D1 outbox/schedule scans; Queue consumers call the same Container job endpoints for retries. Each C# job handles at most 100 items or 20s, checkpoints/commits and returns; further work is rescheduled. All former perpetual hosted-service loops become these bounded entry points in the same C# image. Simulator segments preserve deterministic sequence/checkpoint semantics; process sleep changes wall-clock completion only, never the generated sample values. Schedule occurrence IDs and unique admission rules remain authoritative in D1.

## 6. Migration, load and failure envelope

Migrations run from the gated deployment job, never Container startup. Keep expand → versioned bounded backfill → dirty-range/fence verification → switch → soak → contract. Backfills use guarded owner revision/tombstone comparisons,100-row pages and receipts; stale converted data cannot overwrite a new write. Release manifest pins D1 schema/read/write horizons, C#/Worker plan hashes, DO migrations, Workflow version and Contracts. Rollback retains additive state and restores compatible application versions; irreversible contract requires forward repair or fenced DR.

D1's hard 10 GB/database capacity is explicit. Alert at 60% and 70%, forbid new-tenant onboarding at 80%, and reserve remaining space for existing customers, receipts, deletion and recovery. At 90%, reject growth-heavy admissions with the existing capacity/unavailable reason before accepting content; permit bounded reads, cancellations, exports, deletions and settlement from reserved capacity. This is an operational admission constraint, not loss of existing data. Daily growth forecasts and production-shaped load tests must demonstrate at least 30 days of headroom and the accepted latency/concurrency budget before paid launch. No “request a larger D1 database” recovery is claimed. Reduce only rebuildable data, export/archive eligible retained records, or execute an explicitly planned realm migration; do not silently split a transaction family. Object quotas remain R2 quotas, not a promise of unlimited relational metadata.

<a id="launch-capacity-profile-v1--proposed-acceptance-target"></a>
### Launch capacity profile v1

Status: selected implementation target under [P2-014](../../decisions/phase-2-specification-decisions.md#rule-p2-014). [D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020) performance/cost approval and measured [L-16](../../assurance/release-gates.md#rule-l-16) evidence remain required before paid launch; selecting this design is not a recorded production approval. Model 500 paid accounts, each≤8 MiB live relational metadata plus a1 GiB shared ledger/audit/receipt allowance (about 4.91 GiB total before index/allocator overhead); the measured database including indexes must remain below 6 GiB. Canonical bodies >16 KiB live in verified R2 objects. Exported audit records older than 90 days move to immutable retention storage only after hash/inventory verification; retain current query keys and safety/accounting references. Legal/accounting retention is unchanged. Limits are an operator launch envelope, not a secretly reduced purchased storage quota.

Metadata allocation for that synthetic corpus, per account: identity/device/config ≤0.5 MiB; Notes/Scope/Slate live metadata ≤3 MiB; Cloud assistant history/index pointers ≤2 MiB; active sync/tombstone/command receipts ≤1.5 MiB; execution/notification metadata ≤1 MiB. The shared 1 GiB allowance covers retained accounting/audit/safety references. These are load-fixture budgets, not new entitlement quotas; body/object references and indexes are measured separately. A workload exceeding the envelope requires the stated capacity gate, not content deletion.

**Container allocation.** `instance_type=standard-2` (1 vCPU, 6 GiB memory, 12 GB ephemeral disk); four fixed named slots per realm and `max_instances=4` are a global deployment ceiling, not four per region or a provider autoscaling promise. Worker routes to one of those four controller IDs; no per-user instance creation. Start on demand, `sleepAfter=10m`, no always-warm minimum and no synthetic keepalive solely to evade idle sleep. Active finite requests renew controller activity; close/drain streams under annex10 before ordinary idle stop. Ephemeral disk stores no authoritative data. This allocation gives explicit AOT/buffer headroom; only real [L-16](../../assurance/release-gates.md#rule-l-16) measurements can prove sufficiency.

Per instance: at most 64 open output streams, 16 admitted unary calls, 32 queued calls, eight bounded jobs and two separately reserved control/health slots. Global stream target is served within these limits; bursts may receive bounded pre-admission refusal, not unbounded buffering or silently lost accepted work. Control slots remain available for health/cancellation; current authorization still applies. D1/simulator admission is globally fenced. Slow consumers reconnect by cursor after bounded disconnection. Fixed-slot routing selects an alternate only if readiness failed before forwarding the business request; a timeout after forwarding reconciles the original command, never blindly dispatches it elsewhere.

Idle-to-first-response objective is P95<=10 seconds including Container readiness; keep the existing warm admitted-command P95<=2 seconds. Worker readiness wait is at most eight seconds, bounded by the caller's deadline. If not ready, return gRPC UNAVAILABLE before forwarding, effect=didNotHappen, with two-second retry guidance. Read-only/receipt-proven-safe clients use the declared bounded jitter policy; a possibly forwarded mutation follows ordinary uncertainty recovery. UI shows “Connecting to service” after one second, retains draft/context, and shows retryable unavailable by the ten-second first-request deadline. Local startup budgets remain independent. No user-visible first request waits indefinitely for a sleeping instance.

Operations changes slot count/class/sleep/budgets only through a reviewed deployment/configuration revision with capacity and price revalidation. The source Hello World lite/one-instance configuration is a bootstrap observation, not this launch profile. Provider quotas, placement, D1 serialization and readiness remain real test inputs; increasing instance count cannot make one D1 database execute concurrent transactions.

#### Vectorize and R2 allocation

“Per account” below means an ArcForges customer account, not the Cloudflare billing account. These are engineering/load-fixture allocations; they neither create an entitlement quota nor override a purchased storage promise. Effective paid offers must fit the activated envelope and measured cost model before sale. An oversized offer cannot be silently cut to a fixture allocation.

| Dimension | Per-account planning allocation | Realm operating budget (500-account fixture plus equal reserve) | Accounting rule |
|---|---|---|---|
| Vectorize live vectors | 2,000 | 2,000,000 per selected index | Count live vectors plus held pending inserts; rebuild old/new overlap consumes reserve |
| Vectorize namespaces | 4 | 4,000 per selected index | Current product scope partitions; count tombstone/retiring namespaces until deletion is confirmed |
| R2 stored bytes | 20 GiB | 20,000 GiB | All current versions, incomplete uploads, temporary/export artifacts and retained operational bytes consume capacity; purchased quota remains its separate authority |
| R2 object versions | 2,000 | 2,000,000 | Count admitted versions and bounded pending object reservations, not just visible references |
| R2 Class A operations | 2,000 per UTC day | 2,000,000 per UTC day | Include retries, multipart calls, publication and recovery; compare measured actuals with provider billing classification |
| R2 Class B operations | 20,000 per UTC day | 20,000,000 per UTC day | Include range reads, existence/verification calls and retries |
| Served object bytes | 5 GiB per UTC day | 5,000 GiB per UTC day | Operational load/abuse metric, not a claim that R2 charges Internet egress; associated Worker/network costs remain separate |

Account attribution uses the existing owner workspace; shared backups/catalog/operational jobs use a separate platform allocation from the realm reserve. For each stored-size/count budget, 60% alerts, 70% opens a capacity/cost action, 80% stops new customer onboarding/capacity sales, and 90% refuses new growth-heavy upload/index admission with `capacity.busy` and retry guidance before any new charge or mutation. Existing reads, exports, cancellation, deletion and financial settlement keep reserved capacity. Storage is a gauge and never resets at midnight. Admission is a guarded reservation, not a stale metrics check; telemetry reconciles reservations against actual inventories and unexplained drift blocks further growth admission. Per-account outliers trigger attribution/investigation, not an undisclosed customer quota or deletion.

Daily operation/served-byte budgets are engineering expenditure alerts: 60/70% alert/action, 80% suspend optional rebuild/prewarm/background work and new onboarding, 90% incident action and bounded scheduling/rate control. Do not silently disable already purchased read/export access at a billing counter boundary. Essential cleanup/settlement/restore work is separately accounted from reserve; any forecast beyond the complete budget requires recorded operator funding or a disclosed capacity incident. Provider hard failure still returns typed unavailability. UTC rollover resets only completed daily counters; outstanding reservations/effects carry forward. Raw bodies and personal identifiers never enter public metrics.

The Cloud `launch-capacity.v1` manifest has exact fields profileId, realmId, instanceType, instanceSlots, sleepAfterSeconds, readinessTimeoutMs, firstResponseDeadlineMs, perInstance{outputStreams,unaryCalls,queuedCalls,jobs,controlSlots}, accountPlanning{vectors,namespaces,r2Bytes,r2Objects,classAPerDay,classBPerDay,servedBytesPerDay}, realmBudgets with the same keys, thresholdsPercent=[60,70,80,90], workloadHash and sourceSnapshotHash. Integers use exact uint64 decimal JSON strings where they exceed int32; sizes are bytes. Selected constants are the tables above. Configuration validation rejects absent/negative/inconsistent limits, planning totals greater than the non-reserved allocation, runtime budgets beyond verified provider limits, or offers that cannot honor their admitted capacity. Record private per-account attribution and realm gauges without exposing operator budgets as customer entitlements.

Primary sources checked 2026-09-18: [Container types](https://developers.cloudflare.com/containers/platform/limits/), [fixed-slot routing](https://developers.cloudflare.com/containers/configuration/scaling-and-routing/), [idle/activity control](https://developers.cloudflare.com/containers/reference/container-class/), [Vectorize limits](https://developers.cloudflare.com/vectorize/platform/limits/) and [R2 pricing dimensions](https://developers.cloudflare.com/r2/pricing/). These establish capabilities/limits, not achieved throughput. WP21/40/46 measure the actual binding inventory and budget accounting; WP50 verifies the approved artifact and workload under [L-16](../../assurance/release-gates.md#rule-l-16)/[PG-26](../../assurance/open-gates-register.md#rule-pg-26).

Load target:100 concurrent foreground sessions,200 open finite streams,20 admitted commands/s plus 50 primary reads/s for 60 minutes,2× bursts for 60 seconds,10 simultaneous sync bootstraps and 10 simulator runs. Measure command P95≤2s and bounded cold-start P95≤10s with no acknowledged-loss, skipped feed sequence or duplicate debit. One-minute queue/backup lag, index catch-up and peak reserved growth must remain inside their existing limits. Use production-sized metadata/large R2 bodies and replay fail/retry/cold-start scenarios. Targets do not promise provider capacity; failure blocks [L-16](../../assurance/release-gates.md#rule-l-16) or requires an explicit approved capacity/deployment redesign.

Forecast >60% within 180 days triggers an Architecture/Operations partitioning decision before further capacity sales; at 80% stop new-tenant onboarding. A future partition design must preserve each shared unit in one database or explicitly redesign its transaction; coding cannot improvise sharding. The launch test uses actual paid D1/Container limits and archives measurements/configuration/cost, not extrapolation from SQLite.

Overload uses bounded jittered retries only for reads or receipt-proven safe operations. No hot infinite polling. Container cold starts return bounded retryable unavailability before command admission if the deadline cannot be met. Health separates ingress, Container readiness, D1, DO feed, R2, Vectorize and AI. Run/stream/queue budgets are measured in WP06/21/24/46; current documentation does not prove cost or throughput.

## 7. Backup and disaster recovery

Retain metadata RPO≤5min, blobs≤15min and critical-service RTO≤4h. Paid D1 Time Travel (30 days) is useful for in-place incidents; it does not create a second database and does not by itself satisfy independent disaster recovery. Snapshot/export jobs create a D1 SQL export with its bookmark and a signed schema/plan/object manifest. Exports are promoted only after verification and copied to the existing separate-account AWS S3 COMPLIANCE 30 day archive. This is the explicit disaster-copy exception to the Cloudflare runtime baseline. R2 remains primary storage.

Every authoritative batch also appends a bounded replay record containing its ordered sequence, schema version, resulting row revisions/after-images and deletion keys, excluding temporary/local-history bodies and credentials. Large eligible canonical bodies use already pinned R2 references. The archive worker copies contiguous committed records at least every minute; it advances a signed backup watermark only after independent storage acknowledges. A daily consistent D1 export provides the base; replay selects records strictly after its captured sequence. The export procedure gates writes briefly to establish a matching sequence/bookmark before initiating the provider-consistent export; measured pause/time and resume behavior must pass WP46. No snapshot assembled from unrelated paginated live reads is accepted. Retain change records until all dependent backups expire.

At 4min metadata archive lag (12min blobs), alert and stop new external-effect/content admissions that would violate recovery commitments; continue retry/reconciliation and show incident state. The backup gate fails if actual RPO is exceeded. Restrictive security facts and external dispatch intent still use the independently retained signed safety journal before success/effect dispatch as specified in deployment 22. Archive recovery records alone do not substitute for that journal.

For fresh-environment restore: fence old ingress/credentials; allocate a greater independent recovery generation; import a verified base export into a fresh D1 database; replay contiguous change records to the chosen point; restore and verify R2 references; replay restrictive deletion/revocation/intent facts; invalidate sessions, upload grants, cursors, leases and DO projections; reconcile unknown external effects; rebuild search; reopen only after invariants and health pass. In-place Time Travel follows the same generation/journal/fence procedure. Incomplete archive or safety-journal inventory keeps mutation/dispatch closed. Never infer an absent provider attempt did not happen.

## 8. Derived search

D1 FTS5 text is logically partitioned by realm/workspace/product and always queried through an authenticated scope predicate; candidate filtering after an unbounded global search is forbidden. Vectorize uses one physical index per embedding model/dimension generation, namespace = lower-case workspace UUID (≤64 bytes), mandatory realm/product metadata filters and explicit source/index-generation filters. Index name encodes realm/model-generation; namespace cannot be chosen by a client. The same candidate set then undergoes current D1 owner/deletion/revision authorization before snippets/citations leave C#. Product filter is applied before topK, avoiding foreign-product starvation. Up to 10 metadata indexes and current paid limits (50,000 namespaces/index,20 million vectors/index) bound admission; monitor and stop growth before capacity exhaustion, never fall back to an unfiltered query.

The selected embedding dimension remains 1024. Separate generations are rebuilt beside active data; switch the generation pointer only after completeness/revision checks, then retire old vectors. Exact scalar Notes filtering/sorting uses its declared evaluator, never vector score. Unavailable Vectorize yields explicitly lexical-only completeness; unavailable canonical authority never yields cached content. Local application keyword indexes remain independent.

Sources checked 2026-09-17: [D1 limits](https://developers.cloudflare.com/d1/platform/limits/), [Time Travel](https://developers.cloudflare.com/d1/reference/time-travel/), [Vectorize limits](https://developers.cloudflare.com/vectorize/platform/limits/). D1 paid database hard limit is 10 GB, maximum row/string/blob2 MB,100 bound parameters/statement and 30-second query limit. The stricter internal bounds above apply. Time Travel restores in place; fresh database recovery needs an independent export/import and replay. No provider-limit citation constitutes measured capacity.
