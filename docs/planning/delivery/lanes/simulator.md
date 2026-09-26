# ArcScope Cloud simulator — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Deterministic Cloud simulator definitions, generation, checkpoints, quota and publication.

Tasks: 10 · Owning repositories: ArcScope, Cloud · Integration owner(s): ArcScope integration owner, Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [SIM.01](#task-sim-01) | Simulation definitions, immutable scenario versions and bounded AST evaluator | service | L | [CLOUD.02](cloud.md#task-cloud-02) (artifact), [CON.21](contracts.md#task-con-21) (contract) | not-started |
| [SIM.02](#task-sim-02) | Deterministic generators, seeded RNG and fault profiles (algorithmic determinism) | service | L | [SIM.01](#task-sim-01) (artifact) | not-started |
| [SIM.03](#task-sim-03) | Fenced slices and SimulationPacer (DO alarm coordinator, bounded Container segments, D1 checkpoint/fence) | service | XL | [SIM.02](#task-sim-02) (artifact), [CLOUD.05](cloud.md#task-cloud-05) (artifact), [CLOUD.06](cloud.md#task-cloud-06) (artifact), [CLOUD.07](cloud.md#task-cloud-07) (artifact) | not-started |
| [SIM.04](#task-sim-04) | Canonical publication, checkpoints and recovery | service | L | [SIM.03](#task-sim-03) (artifact), [CLOUD.42](cloud.md#task-cloud-42) (artifact), [CLOUD.04](cloud.md#task-cloud-04) (artifact), [COM.07](commerce.md#task-com-07) (artifact) | not-started |
| [SIM.05](#task-sim-05) | Cloud-side simulation.* operations, manifest listing and segment fetch | service | M | [SIM.04](#task-sim-04) (artifact), [CLOUD.21](cloud.md#task-cloud-21) (artifact), [CLOUD.24](cloud.md#task-cloud-24) (artifact), [CON.21](contracts.md#task-con-21) (contract) | not-started |
| [SIM.06](#task-sim-06) | ArcScope-side simulated DataSource and native ingestion | service | L | [SIM.05](#task-sim-05) (artifact), [CON.21](contracts.md#task-con-21) (contract), [SCOPE.01](arcscope.md#task-scope-01) (artifact), [SCOPE.14](arcscope.md#task-scope-14) (artifact), [SCOPE.24](arcscope.md#task-scope-24) (artifact) | not-started |
| [SIM.07](#task-sim-07) | Limits, entitlement and lifecycle | service | L | [SIM.03](#task-sim-03) (artifact), [COM.05](commerce.md#task-com-05) (artifact), [COM.07](commerce.md#task-com-07) (artifact), [COM.12](commerce.md#task-com-12) (artifact), [POL.03](policy.md#task-pol-03) (artifact) | not-started |
| [SIM.08](#task-sim-08) | Owned-artifact verification and real integration | service | M | [SIM.01](#task-sim-01) (artifact), [SIM.02](#task-sim-02) (artifact), [SIM.03](#task-sim-03) (artifact), [SIM.04](#task-sim-04) (artifact), [SIM.05](#task-sim-05) (artifact), [SIM.06](#task-sim-06) (artifact), [SIM.07](#task-sim-07) (artifact) | not-started |
| [SIM.09](#task-sim-09) | Real Cloud->R2->ArcScope-native simulator closure: hash/timebase/provenance proof against WP34 measurement/report and WP35 import/portability | integration | M | [SIM.05](#task-sim-05) (artifact), [SIM.06](#task-sim-06) (artifact), [SCOPE.14](arcscope.md#task-scope-14) (artifact), [SCOPE.18](arcscope.md#task-scope-18) (artifact), [SCOPE.24](arcscope.md#task-scope-24) (artifact) | not-started |
| [SIM.10](#task-sim-10) | Real ArcScope simulator admission against deployed capacity/SimulationPacer | integration | M | [CLOUD.07](cloud.md#task-cloud-07) (artifact), [SIM.01](#task-sim-01) (artifact) | not-started |

## Tasks

<a id="task-sim-01"></a>

### SIM.01 — Simulation definitions, immutable scenario versions and bounded AST evaluator

**Outcome.** Definitions and immutable scenario versions exist; the channel schema (stable ids, value types, units, rate, timestamp semantics) and the V1 generator set (constant, sine, square, triangle, sawtooth, seeded noise, seeded random walk, pulse, step sequence, CSV replay) are defined; the bounded AST (constants, time/tick, channel references, arithmetic, comparison, conditionals, allowlisted numeric functions) validates acyclic dependencies and depth/node-count/per-tick-operation bounds before admission, with no scripting/dynamic compilation/reflection/file access/networking possible.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-01` and ledger record `ledger/tasks/sim-01.md` in the Plan repository; task branch `task/sim-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-51.00](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.00) — full |
| Provides | sim.definitions-ast |
| Start prerequisites | **artifact** [CLOUD.02](cloud.md#task-cloud-02) — the module-boundary pattern the other 20 Cloud modules follow ('Twenty-one module boundaries'). *Why:* ArcForges.Cloud.Modules.Scope is a brand-new Cloud module; it needs the real module-registration/boundary mechanism to attach to rather than inventing its own composition path<br>**contract** [CON.21](contracts.md#task-con-21) — published SimulationService definition and scenario-version records. *Why:* simulation definitions are stored and served through the generated records |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.02](#task-sim-02), [SIM.08](#task-sim-08), [SIM.10](#task-sim-10) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Definitions/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Ast/**`<br>`Cloud:tests/Cloud.Tests.Integration/Scope/Ast/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | malformed-AST corpus rejected before any side effect; cyclic-dependency case; each bound exceeded; definition-edit-does-not-affect-existing-runs test; CSV replay with bounded parse report; URL-fetch/host-file-read/cross-workspace-reference each denied — pure in-process unit tests, no D1/R2/host needed yet |
| Completion evidence | AST bounds, cyclic-dependency and sandbox-denial results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo (HEAD ce0a32a) has zero files matching scope/simulat*; this is entirely new |
| Notes | Per producer-artifacts-and-integration.md's WP51 row, this and SIM.02 are exactly the permitted early substitute tier: independent fixed generator vectors, built and proven BEFORE any real D1/R2 integration. The initial simulator execution profile (architecture/23-simulator-and-interchange.md §6, af-sim.v1: generator formulas, RNG spec, AST depth/node/eval limits, duration/batch/concurrency/queue/memory bounds) is already frozen design, not a start edge — implemented directly. |

<a id="task-sim-02"></a>

### SIM.02 — Deterministic generators, seeded RNG and fault profiles (algorithmic determinism)

**Outcome.** Same seed and profile produce identical canonical hashes; a changed seed produces different data; every injected fault carries provenance/counters and is exactly positioned; RNG streams are provably independent across channels and fault sources.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-02` and ledger record `ledger/tasks/sim-02.md` in the Plan repository; task branch `task/sim-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-51.01](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.01) — the pure-algorithmic half: fixed logical ticks driving canonical data; independently seeded RNG per channel and per fault source; the execution profile pinning numeric/RNG/generator/encoding versions; fault profiles (latency, jitter, drop, duplicate, reorder, disconnect, malformed frame, outlier) at explicit logical boundaries with provenance and counters; same-seed-same-hash and changed-seed-different-data tests; exact fault positions; one channel's RNG not perturbing another's |
| Provides | sim.generators-faults |
| Start prerequisites | **artifact** [SIM.01](#task-sim-01) — definitions, channel schema and AST evaluator. *Why:* generators produce values the AST/channel schema consumes; cannot be built before that schema exists |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.03](#task-sim-03), [SIM.08](#task-sim-08) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Generators/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Faults/**`<br>`Cloud:tests/Cloud.Tests.Integration/Scope/Generators/**` |
| Validation | pure in-process determinism tests (hash equality, seed sensitivity, fault-position exactness, RNG-stream independence) — no host/D1/R2 needed for this half |
| Completion evidence | determinism and fault-position results (algorithmic tier) |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [WP-51.01](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.01)'s remaining requirement — identical hashes under real-time vs accelerated pacing, and the SimulationPacer state-diagram/wake/retry/cold-start exercise plus 24h pacing/cost recording — needs the real SimulationPacer and is carried as part of SIM.03's obligations/testing instead, since it cannot be exercised before that component exists. See SIM.03. |

<a id="task-sim-03"></a>

### SIM.03 — Fenced slices and SimulationPacer (DO alarm coordinator, bounded Container segments, D1 checkpoint/fence)

**Outcome.** Deterministic committed samples and restart recovery pass under real DO alarm delivery, Container execution and D1 checkpoint/fence; the proposed 5s latency is measured and recorded, never claimed as hard real time; every SimulationPacer state-diagram race (duplicate alarm, exhausted retry, sleeping Container, pause/cancel race, duplicate segment, delayed catch-up, accelerated mode) passes.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-03` and ledger record `ledger/tasks/sim-03.md` in the Plan repository; task branch `task/sim-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / XL |
| Obligations | [WP-51.02](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.02) — full: architecture-23 DO alarm integration owner plus bounded Container segments, D1 checkpoint/fence/next_due_at, minutely rescue scan; default 1s and 0.25-10s segment bounds; no permanent hosted-service loop<br>[WP-51.01](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.01) — the real-host half: identical hashes under real-time and accelerated pacing; exercise the SimulationPacer state diagram (duplicate/delayed alarm, exhausted automatic retries plus Cron rescue, Container cold start, pause/resume, epoch loss); record 24-hour run cost, alarm/Container/Queue counts and end-to-end pacing distribution against the proposed 5-second target, no hard real-time claim<br>[WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) 'Slice recovery acceptance' body text (between §5 and §6, no substep id): kill the real Container before D1 publication, after the guarded segment/checkpoint/outbox batch, and before/after alarm scheduling; race a duplicate alarm with Cron rescue; assert one committed segment per run/range, deterministic continuation, no lost next-due intent, rejection of stale fences; alarm delivery itself may repeat; use the bounded mechanism in architecture 23 §1.2, never interactive BEGIN/COMMIT or an in-memory continuation loop — 'Slice recovery acceptance' body text (between §5 and §6, no substep id): kill the real Container before D1 publication, after the guarded segment/checkpoint/outbox batch, and before/after alarm scheduling; race a duplicate alarm with Cron rescue; assert one committed segment per run/range, deterministic continuation, no lost next-due intent, rejection of stale fences; alarm delivery itself may repeat; use the bounded mechanism in architecture 23 §1.2, never interactive BEGIN/COMMIT or an in-memory continuation loop; package-level obligation contribution |
| Provides | sim.pacer-fenced-execution |
| Start prerequisites | **artifact** [SIM.02](#task-sim-02) — deterministic generators/faults. *Why:* the pacer drives real generator ticks<br>**artifact** [CLOUD.05](cloud.md#task-cloud-05) — published finite-durable-jobs mechanism (DO alarm scheduling, the generic durable-job abstraction a SimulationRun specialises per [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)). *Why:* SimulationPacer is explicitly built on architecture 23's DO alarm integration owner; this is the real Cloud host primitive it runs on, not a substitutable stand-in — lease/alarm race semantics can only be honestly proven against the real mechanism<br>**artifact** [CLOUD.06](cloud.md#task-cloud-06) — published shared atomic families and claims mechanism (lease fencing). *Why:* [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) [BR-03](../../../architecture/14-build-packaging-and-release.md#rule-br-03) states lease fencing, not single-instance deployment, is what makes N replicas safe; this is the exact primitive [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05) produces<br>**artifact** [CLOUD.07](cloud.md#task-cloud-07) — published capacity and Container/D1 integration producer mechanism. *Why:* [WP-51.02](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.02) explicitly implements 'bounded Container segments, D1 checkpoint/fence' — this looks like the direct generic mechanism [WP-21.06](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) exists to produce; SimulationPacer is architecture 23's specialisation of it, not a separately invented Container/D1 integration |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.04](#task-sim-04), [SIM.07](#task-sim-07), [SIM.08](#task-sim-08) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.BackgroundJobs/SimulationPacer/**`<br>`Cloud:tests/Cloud.Tests.Integration/Scope/Pacer/**` |
| Shared resources | [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | at-least-once alarm, exhausted retry, sleeping Container, pause/cancel race, duplicate segment, delayed catch-up, accelerated mode, and the full slice-recovery Container-kill matrix — this genuinely needs a real (local/dev) Cloud host+D1+Container environment, kept to local/affected-scope per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), not hosted CI |
| Completion evidence | replica contention, fenced takeover, bounded-batch and slice-recovery results; determinism/pacing-equality/fault-position results carried over from [WP-51.01](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.01)'s real-host half |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This is the highest-complexity task in the whole area (XL): it is the first place WP51 genuinely needs the real Cloud host, and it deliberately folds in [WP-51.01](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.01)'s real-pacing half plus the WP51-level 'Slice recovery acceptance' paragraph, none of which can be honestly tested before SimulationPacer itself exists. |

<a id="task-sim-04"></a>

### SIM.04 — Canonical publication, checkpoints and recovery

**Outcome.** Canonical batches are written as immutable objects; manifest entries carry run/profile identity, sequence, logical range, count, encoding, byte length and hash; the manifest row is the commit point with the checkpoint advanced in the same transaction; incomplete objects are invisible and swept; recovery produces byte-identical remaining canonical data across pause/resume, host loss and lease takeover; real Entitlement/Scope/Resource quota is reserved and the current monotonic lease fence is verified in every commit.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-04` and ledger record `ledger/tasks/sim-04.md` in the Plan repository; task branch `task/sim-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-51.03](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.03) — full |
| Provides | sim.canonical-publication |
| Start prerequisites | **artifact** [SIM.03](#task-sim-03) — fenced execution producing ticks to publish. *Why:* publication commits what the pacer generates<br>**artifact** [CLOUD.42](cloud.md#task-cloud-42) — published blob lifecycle mechanism (immutable object write, incomplete-object sweep). *Why:* canonical batches are written as immutable R2 objects with a sweep for incomplete ones — this is the same real object-storage lifecycle mechanism [WP-25.05](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.05) produces for Notes/blob data, reused here rather than re-implemented<br>**artifact** [CLOUD.04](cloud.md#task-cloud-04) — published receipts/outbox/archive transactional-commit pattern. *Why:* 'the manifest row is the commit point, and the checkpoint advances only after it, in the same transaction' ([BR-02](../../../architecture/14-build-packaging-and-release.md#rule-br-02)) is exactly the outbox/transactional-commit shape [WP-21.04](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.04) exists to produce<br>**artifact** [COM.07](commerce.md#task-com-07) — published quota/usage/storage accounting mechanism. *Why:* the substep explicitly requires consuming real Entitlement/Scope/Resource quota reservations at commit time, not a stub counter |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.05](#task-sim-05), [SIM.08](#task-sim-08) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Publication/**`<br>`Cloud:tests/Cloud.Tests.Integration/Scope/Publication/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | stale-holder-resumes-after-takeover; cancellation racing segment promotion and quota release; pause/resume producing same remaining data; host loss/takeover producing no duplicate/no missing range; crash-between-object-write-and-manifest-commit leaving a swept invisible object; committed manifest row never referencing an unverified object — real local Cloud host/D1/R2 environment, local/affected-scope per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | recovery equality across pause, host loss and takeover |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-sim-05"></a>

### SIM.05 — Cloud-side simulation.* operations, manifest listing and segment fetch

**Outcome.** The eleven simulation.* operations are durable, idempotent and expected-state; a client can list authorised manifests and fetch segments resumably with hash verification; state polling works with realtime disabled.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-05` and ledger record `ledger/tasks/sim-05.md` in the Plan repository; task branch `task/sim-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-51.04](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.04) — the Cloud API half: the eleven simulation.* operations as durable, idempotent, expected-state commands; authorised manifest listing; resumable hash-verifiable segment fetch over HTTP or object storage; revision-/cursor-based state polling |
| Provides | sim.cloud-api |
| Start prerequisites | **artifact** [SIM.04](#task-sim-04) — published manifests/checkpoints to expose. *Why:* the API surfaces what SIM.04 commits<br>**artifact** [CLOUD.21](cloud.md#task-cloud-21) — published endpoint mapping and validation pattern. *Why:* the eleven simulation.* operations are new Cloud PublicApi endpoints and should follow the one real endpoint-mapping/validation mechanism, not a bespoke one<br>**artifact** [CLOUD.24](cloud.md#task-cloud-24) — published idempotency and rate-limiting mechanism. *Why:* [WP-51.04](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.04) explicitly requires 'durable, idempotent, expected-state commands' and testing against duplicate/stale/out-of-order commands — this is exactly [WP-23.03](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.03)'s mechanism, reused rather than reinvented per-module<br>**contract** [CON.21](contracts.md#task-con-21) — published SimulationService operations. *Why:* the Cloud-side operations implement the generated service |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.06](#task-sim-06), [SIM.08](#task-sim-08), [SIM.09](#task-sim-09) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Scope/**`<br>`Cloud:tests/Cloud.Tests.Integration/Scope/Api/**` |
| Shared resources | [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | duplicate/stale/out-of-order commands; terminal-run resists resurrection; hash-mismatched segment rejected; reconnect-with-realtime-disabled proves polling is a complete authoritative fallback — real local Cloud host per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | command idempotency and realtime-disabled fallback results (Cloud-side) |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-sim-06"></a>

### SIM.06 — ArcScope-side simulated DataSource and native ingestion

**Outcome.** A SimulatedDataSource adapter feeds the ordinary ArcScope acquisition pipeline; simulated data is usable in every normal ArcScope workflow (session, capture, decoder, measurement, report) while remaining labelled synthetic everywhere, including through export/copy; with realtime disabled, a client reaches the same state via the polling fallback.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/sim-06` and ledger record `ledger/tasks/sim-06.md` in the Plan repository; task branch `task/sim-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-51.04](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.04) — the ArcScope consumer half: feed retained canonical simulator output through the existing Scope measurement/replay consumer using its recorded profile and configuration; simulation labels remain synthetic, separate from AI origin; recompute statistical/pulse fixtures without changing measurement meaning or treating simulation as hardware evidence; ArcScope's clearly synthetic DataSource feeding the normal acquisition pipeline; seed and profile provenance surviving export and copy; simulated data flowing through session/capture/decoder/measurement/report unchanged; synthetic labelling surviving export<br>[WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) §7 required evidence addition (canonical simulator replay retains measurement profile and synthetic provenance) — package-level obligation contribution |
| Provides | sim.arcscope-ingestion |
| Start prerequisites | **artifact** [SIM.05](#task-sim-05) — Cloud-side simulation.* operations and segment fetch. *Why:* the ArcScope adapter calls these operations<br>**contract** [CON.21](contracts.md#task-con-21) — published generated C# SimulationService client and records. *Why:* ArcScope should call the Cloud API through the real generated client, the same mechanism every other cross-repo Cloud consumer uses, not a hand-rolled HTTP client<br>**artifact** [SCOPE.01](arcscope.md#task-scope-01) — the DataSource/SourceAdapter contract. *Why:* SimulatedDataSource is one more adapter behind the same shared contract used by network/serial/replay adapters<br>**artifact** [SCOPE.14](arcscope.md#task-scope-14) — the real measurement/replay consumer. *Why:* [WP-51.04](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.04) explicitly requires feeding the *existing* Scope measurement/replay consumer, not a parallel one<br>**artifact** [SCOPE.24](arcscope.md#task-scope-24) — import/export bundle format with simulator-provenance fields. *Why:* final-review text requires seed/profile provenance to survive export and copy through the same native bundle format |
| Entry condition | [ADOPT.05.simulator](adoption.md#task-adopt-05-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SIM.09](#task-sim-09) — the end-to-end real AOT simulation -> R2 -> native ingest/measurement/report proof. *Why:* this task's own gate is 'simulated data flows through the normal pipeline unchanged and stays labelled synthetic'; the full real-service, real-storage, real-native-adapter proof against [SIM-20](../../../requirements/products/arcscope.md#rule-sim-20) is the dedicated integration task |
| Unblocks | [SIM.08](#task-sim-08), [SIM.09](#task-sim-09) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Acquisition/Adapters/Simulation/**`<br>`ArcScope:src/ArcScope/ArcScope.Desktop/Simulation/**`<br>`ArcScope:tests/ArcScope.Tests.Integration/Simulation/**` |
| Shared resources | [RES-arcscope-format-fixtures](../shared-resources.md#res-arcscope-format-fixtures) (append), [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | simulated data flowing through session/capture/decoder/measurement/report unchanged; synthetic labelling surviving export; realtime-disabled polling fallback proof |
| Completion evidence | native ingestion and synthetic-labelling results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-sim-07"></a>

### SIM.07 — Limits, entitlement and lifecycle

**Outcome.** Deployment policy bounds (channels, rates, duration, AST work, per-workspace/global concurrency, queue/wait time, storage, egress, retention) are enforced before and during execution with capacity reservation; service-entitlement gating is independent of AI credits; term expiry/suspension stops generation at a durable boundary as canceled with reason; a 24-hour bounded-resource soak holds within bounds.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-07` and ledger record `ledger/tasks/sim-07.md` in the Plan repository; task branch `task/sim-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-51.05](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.05) — full |
| Provides | sim.limits-entitlement |
| Start prerequisites | **artifact** [SIM.03](#task-sim-03) — real execution loop to enforce limits against. *Why:* limits are enforced before/during execution, which requires the real pacer/execution loop to exist<br>**artifact** [COM.05](commerce.md#task-com-05) — published entitlement resolver. *Why:* 'service-entitlement gating independent of AI credits' is a direct consumption of [WP-42.04](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.04)'s mechanism<br>**artifact** [COM.07](commerce.md#task-com-07) — published quota/usage/storage accounting. *Why:* 'product-resource usage accounting for duration, samples, bytes and egress' is [WP-42.06](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.06)'s mechanism by name<br>**artifact** [COM.12](commerce.md#task-com-12) — published service term/replenishing capacity mechanism. *Why:* 'term expiry or suspension stopping generation at a durable boundary' is [WP-42.11](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11)'s mechanism<br>**artifact** [POL.03](policy.md#task-pol-03) — published compiled hard limits mechanism. *Why:* 'deployment policy bounding channels, rates, duration, AST work... enforced before and during execution' matches [WP-44.02](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.02)'s compiled-hard-limits mechanism almost exactly; reused rather than re-implemented per-module |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.08](#task-sim-08) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Limits/**`<br>`Cloud:tests/Cloud.Tests.Integration/Scope/Limits/**` |
| Shared resources | [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | quota exhaustion before side effects; cross-workspace denial; term expiring mid-run; suspension mid-run; storage exhaustion; retention pass with active readers; partial-cancellation reporting partial; 24-hour bounded-resource soak — real local Cloud host, local/affected-scope per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (the 24h soak is the one long-running exception explicitly required by this substep) |
| Completion evidence | limit enforcement, entitlement, expiry and 24-hour soak results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-sim-08"></a>

### SIM.08 — Owned-artifact verification and real integration

**Outcome.** Real AOT simulation -> R2 verified publication -> ArcScope ingest/measurement proves deterministic results and failure recovery, with no Workers AI dependency or AI debit; [PG-14b](../../../assurance/open-gates-register.md#rule-pg-14b) evidence recorded, including the 24-hour soak.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-08` and ledger record `ledger/tasks/sim-08.md` in the Plan repository; task branch `task/sim-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Package acceptance | Records the [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-51.90](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.90) — full<br>[WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) §8 additional completion requirement: the simulator remains an optional later source for already-defined measurement semantics, never a prerequisite for the earlier replay-based analysis package (confirms [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) does not wait on [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51)) — §8 additional completion requirement: the simulator remains an optional later source for already-defined measurement semantics, never a prerequisite for the earlier replay-based analysis package (confirms [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) does not wait on [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51)) |
| Provides | sim.wp51-accepted-candidate |
| Start prerequisites | **artifact** [SIM.01](#task-sim-01) — all SIM tasks complete to assemble. *Why:* verify task<br>**artifact** [SIM.02](#task-sim-02) — as above. *Why:* as above<br>**artifact** [SIM.03](#task-sim-03) — as above. *Why:* as above<br>**artifact** [SIM.04](#task-sim-04) — as above. *Why:* as above<br>**artifact** [SIM.05](#task-sim-05) — as above. *Why:* as above<br>**artifact** [SIM.06](#task-sim-06) — as above. *Why:* as above<br>**artifact** [SIM.07](#task-sim-07) — as above. *Why:* as above |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SIM.09](#task-sim-09) — completed end-to-end proof. *Why:* [WP-51.90](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.90)'s own gate is this exact end-to-end chain |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:docs/wp-51-integration-receipt.md` |
| Validation | real AOT simulation -> R2 verified publication -> ArcScope ingest/measurement; no Workers AI dependency; proportionate under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) given this is explicitly a real-service/real-storage/real-native-adapter gate ([PG-14b](../../../assurance/open-gates-register.md#rule-pg-14b) text: 'preview/test fakes are insufficient') |
| Completion evidence | owned-artifact and real-integration receipt covering the full [SIM-01](../../../requirements/products/arcscope.md#rule-sim-01)..[SIM-20](../../../requirements/products/arcscope.md#rule-sim-20) acceptance list |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) executes in Phase J specifically because it needs [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)/[WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)'s real commercial admission, unlike the desktop-only WP33/34 (Phase H). This ordering is already correct in the source design; nothing to change here. |

<a id="task-sim-09"></a>

### SIM.09 — Real Cloud->R2->ArcScope-native simulator closure: hash/timebase/provenance proof against WP34 measurement/report and WP35 import/portability

**Outcome.** A real generated simulation run, published through real R2-verified segments, ingested by ArcScope's real (non-simulator) measurement/report/import-export consumers, with hash/timebase/provenance checked end to end and stale grant/fence attempts refused. No simulator fixture stands in for a hardware claim anywhere in this chain.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-09` and ledger record `ledger/tasks/sim-09.md` in the Plan repository; task branch `task/sim-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-51.04](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.04) — final-review closure paragraph: real service-authorized R2 segments; consume WP34 measurement/report and WP35 import/portability outputs; Cloud->R2->native hash/timebase/provenance check; stale grant/fence refusal<br>[WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) 'Required implementation and closure from the final review' paragraph (real service-authorized R2 segments; consume WP34 measurement/report and WP35 import/portability outputs; Cloud->R2->native hash/timebase/provenance check; stale grant/fence refusal) — package-level obligation contribution |
| Start prerequisites | **artifact** [SIM.05](#task-sim-05) — real, delivered outcome of SIM.05 (Cloud-side simulation.* operations, manifest listing and segment fetch). *Why:* this integration exercises the real cloud-side simulation.* operations, manifest listing and segment fetch instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SIM.06](#task-sim-06) — real, delivered outcome of SIM.06 (ArcScope-side simulated DataSource and native ingestion). *Why:* this integration exercises the real arcScope-side simulated DataSource and native ingestion instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SCOPE.14](arcscope.md#task-scope-14) — real, delivered outcome of SCOPE.14 (Measurements: scope.measurement.v1). *Why:* this integration exercises the real measurements: scope.measurement.v1 instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SCOPE.18](arcscope.md#task-scope-18) — real, delivered outcome of SCOPE.18 (Reports and reproducibility). *Why:* this integration exercises the real reports and reproducibility instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SCOPE.24](arcscope.md#task-scope-24) — real, delivered outcome of SCOPE.24 (Import, export and format fixtures). *Why:* this integration exercises the real import, export and format fixtures instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SIM.06](#task-sim-06), [SIM.08](#task-sim-08) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | A real generated simulation run, published through real R2-verified segments, ingested by ArcScope's real (non-simulator) measurement/report/import-export consumers, with hash/timebase/provenance checked end to end and stale grant/fence attempts refused. No simulator fixture stands in for a hardware claim anywhere in this chain. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-sim-10"></a>

### SIM.10 — Real ArcScope simulator admission against deployed capacity/SimulationPacer

**Outcome.** Simulator admission and SimulationPacer DO infrastructure work against the real deployed capacity harness, not a local-only simulation

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/sim-10` and ledger record `ledger/tasks/sim-10.md` in the Plan repository; task branch `task/sim-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-21.06](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) — SimulationPacer real-consumer integration |
| Start prerequisites | **artifact** [CLOUD.07](cloud.md#task-cloud-07) — real, delivered outcome of CLOUD.07 (Capacity, Container/D1 integration producer and harness). *Why:* this integration exercises the real capacity, Container/D1 integration producer and harness instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SIM.01](#task-sim-01) — real, delivered outcome of SIM.01 (Simulation definitions, immutable scenario versions and bounded AST evaluator). *Why:* this integration exercises the real simulation definitions, immutable scenario versions and bounded AST evaluator instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.07.simulator](adoption.md#task-adopt-07-simulator) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.10](cloud.md#task-cloud-10) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Simulator admission and SimulationPacer DO infrastructure work against the real deployed capacity harness, not a local-only simulation |
| Baseline (unreviewed unless accepted) | not-started |
