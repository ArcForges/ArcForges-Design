<a id="rule-wp-51"></a>

# WP-51 — ArcScope Deterministic Cloud Simulator

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Integration after real Cloud prerequisites
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Deliver the deterministic Cloud simulator of [SIM-01](../../requirements/products/arcscope.md#rule-sim-01)–[SIM-20](../../requirements/products/arcscope.md#rule-sim-20) as a **real capability running through real Cloud persistence, real object storage and the real native acquisition pipeline**. A preview, a canned response or a test fake does not satisfy this package ([SIM-20](../../requirements/products/arcscope.md#rule-sim-20)).

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud C#; ArcScope consumer. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**Selected execution input.** [The initial simulator profile](../../architecture/23-simulator-and-interchange.md#6-initial-simulator-execution-profile) and [numbered wire/segment registry](../../architecture/contracts/04-protobuf-wire-registry.md) fix generator formulas, seeded RNG, AST, CSV, fault ordering, encoding and limits before coding. Implement and verify that profile; internal evaluator organization remains an implementation choice.

**In scope.** Cloud-owned simulation definitions and immutable scenario versions; the bounded expression AST and its validator; the generator set; fault profiles; lease-fenced execution inside the single Cloud host; canonical segment publication to object storage with a manifest; durable checkpoints; the authorised client fetch path; and ArcScope's native ingestion of simulated data through its normal session, capture, decoder, measurement and report workflows.

**Out of scope.** Hardware acquisition ([WP-33](33-arcscope-acquisition-and-session.md#rule-wp-33)), analysis semantics ([WP-34](34-arcscope-analysis-and-reporting.md#rule-wp-34)), AI of any kind — **a `SimulationRun` invokes no model** ([SIM-01](../../requirements/products/arcscope.md#rule-sim-01)).

**Why this package exists.** [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) added the simulator as a delivery obligation. It spans Cloud persistence, storage, lease fencing and native ingestion, so it is neither an ArcScope-only nor a Cloud-only body of work, and folding it into [WP-33](33-arcscope-acquisition-and-session.md#rule-wp-33) would hide a substantial Cloud dependency inside a native package.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [scope.measurement.v1](../../requirements/products/arcscope.md#measurement-profile)

The official simulator consumes real paid-term and quota enforcement from [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) and policy activation from [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44). Desktop replay/analysis does not depend on it. It therefore executes in J rather than claiming real commercial admission in H.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) `§17.1` | [SIM-01](../../requirements/products/arcscope.md#rule-sim-01)–[SIM-20](../../requirements/products/arcscope.md#rule-sim-20), the normative source |
| [`../../architecture/23-simulator-and-interchange.md`](../../architecture/23-simulator-and-interchange.md) `§1` | The execution, determinism, fault and back-pressure design |
| [`../../architecture/data-model/01-cloud-data-model.md`](../../architecture/data-model/01-cloud-data-model.md) `§8.3` | The six simulator tables and their commit ordering |
| [`../../architecture/contracts/01-public-api-operations.md`](../../architecture/contracts/01-public-api-operations.md) `§9.1` | The eleven operations and their rules |
| [WP-21](21-cloud-host-and-persistence.md#rule-wp-21) output | The single host, its hosted services and durable leases |
| [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25) output | Object storage, upload and download paths |
| [WP-33](33-arcscope-acquisition-and-session.md#rule-wp-33) output | The native acquisition pipeline the simulator must feed |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **A `SimulationRun` is a product job, not an Agent Run** ([SIM-01](../../requirements/products/arcscope.md#rule-sim-01)). It invokes no model and debits no AI capacity. |
| <a id="rule-br-02"></a>BR-02 | **The manifest row is the commit point**, and the checkpoint advances only after it, in the same transaction ([SX-01](../../architecture/23-simulator-and-interchange.md#rule-sx-01), [SX-02](../../architecture/23-simulator-and-interchange.md#rule-sx-02)). |
| <a id="rule-br-03"></a>BR-03 | **Lease fencing, not single-instance deployment**, is what makes N replicas safe ([SX-03](../../architecture/23-simulator-and-interchange.md#rule-sx-03), [RT-04](../../architecture/05-cloud-architecture.md#rule-rt-04)). |
| <a id="rule-br-04"></a>BR-04 | **Determinism is scoped to the execution profile** ([SD-01](../../architecture/23-simulator-and-interchange.md#rule-sd-01)). Cross-version and cross-CPU floating-point equivalence is never promised. |
| <a id="rule-br-05"></a>BR-05 | **Preview may decimate; canonical generation may not** ([SF-03](../../architecture/23-simulator-and-interchange.md#rule-sf-03)). |
| <a id="rule-br-06"></a>BR-06 | **Injected faults are labelled as intentional** ([SF-01](../../architecture/23-simulator-and-interchange.md#rule-sf-01)), so they cannot be mistaken for real data loss. |
| <a id="rule-br-07"></a>BR-07 | **Synthetic data is labelled synthetic everywhere it appears** ([SC-06](../../architecture/23-simulator-and-interchange.md#rule-sc-06), [I-496](../../requirements/01-normative-glossary-and-invariants.md#rule-i-496)), and never enters a hardware-evidence path. |
| <a id="rule-br-08"></a>BR-08 | **No scripting, dynamic compilation, reflection, file access or networking** in scenario evaluation ([SB-01](../../architecture/23-simulator-and-interchange.md#rule-sb-01)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Scope/` | Definitions, scenario versions, runs, AST validator, generators, fault profiles |
| `src/Cloud/ArcForges.Cloud.BackgroundJobs/` | The simulator hosted service, lease acquisition, batch generation loop |
| `src/Cloud/ArcForges.Cloud.PublicApi/` | The eleven `simulation.*` operations |
| `src/Cloud/ArcForges.Cloud.Migrations/` | The six simulator tables |
| `src/ArcScope/ArcScope.Acquisition/` | The Cloud Simulation `DataSource` adapter and segment fetcher |
| `src/ArcScope/ArcScope.Desktop/` | Scenario selection, run control, synthetic labelling |
| `tests/ArcScope.Tests.Integration/`, `tests/Cloud.Tests.Integration/` | The [SIM-20](../../requirements/products/arcscope.md#rule-sim-20) acceptance suite |

**Major types introduced.** `SimulationDefinition`, `ScenarioVersion`, `SimulationRun`, `SimulationSegment`, `SimulationCheckpoint`, `SimulationLease`, `ExecutionProfile`, `ChannelSchema`, `ScenarioExpression`, `FaultProfile`, `CanonicalBatch`, `SegmentManifest`, `SimulatedDataSource`.

---

## 5. Required implementation work

<a id="rule-wp-51.00"></a>

### WP-51.00 — Definitions, versions and bounded evaluation

**What must be fully done.** Definitions and **immutable** scenario versions; the channel schema with stable ids, value types, units, rate and timestamp semantics; the V1 generator set — constant, sine, square, triangle, sawtooth, seeded noise, seeded random walk, pulse, step sequence, CSV replay; the bounded AST over constants, time/tick, channel references, arithmetic, comparison, conditionals and an allowlisted numeric function set, validated for acyclic dependencies and bounds on depth, node count and per-tick operations **before admission**.

**Testing requirements.** A malformed-AST corpus rejected before any side effect; a cyclic-dependency case; each bound exceeded; a definition edit proving existing runs are unaffected; a CSV replay with a bounded parse report; a scenario attempting a URL fetch, a host file read and a cross-workspace reference, each denied.

**Completion gate.** No scenario input reaches evaluation without passing bounds, and an invalid scenario consumes no lease, object or quota.

<a id="rule-wp-51.01"></a>

### WP-51.01 — Deterministic generation and faults

**What must be fully done.** Fixed logical ticks driving canonical data; independently seeded RNG per channel and per fault source; the execution profile pinning numeric semantics, RNG, generator and encoding versions; real-time and bounded accelerated pacing that leave sample values, logical timestamps and hashes unchanged; fault profiles for latency, jitter, drop, duplicate, reorder, disconnect, malformed frame and outlier at explicit logical boundaries, each carrying provenance and counters.

**Testing requirements.** Same seed and profile producing identical canonical hashes; a changed seed producing different data; identical hashes under real-time and accelerated pacing; exact fault positions; a proof that one channel's RNG consumption does not perturb another's. Exercise the architecture 23 SimulationPacer state diagram: duplicate/delayed alarm, exhausted automatic retries plus Cron rescue, Container cold start, pause/resume and epoch loss. Record a 24-hour run cost, alarm/Container/Queue counts and end-to-end pacing distribution against the proposed 5-second target; no hard real-time claim.

**Completion gate.** [SIM-07](../../requirements/products/arcscope.md#rule-sim-07) equality holds within a profile, and every injected fault is distinguishable from unexpected loss. Deterministic hashes survive wake/retry and the measured pacing/cost envelope is recorded and approved before launch.

<a id="rule-wp-51.02"></a>

### WP-51.02 — Fenced slices and SimulationPacer

**What must be fully done.** Implement arch 23 DO alarm coordinator plus bounded Container segments, D1 checkpoint/fence/next_due_at and minutely rescue scan. Default 1s and 0.25–10s segment bounds; no permanent hosted-service loop.

**Testing requirements.** At-least-once alarm, exhausted retry, sleeping Container, pause/cancel race, duplicate segment, delayed catch-up and accelerated mode.

**Completion gate.** Deterministic committed samples and restart recovery pass; proposed5s latency is separately measured, not claimed as hard real time.

<a id="rule-wp-51.03"></a>

### WP-51.03 — Canonical publication, checkpoints and recovery

**What must be fully done.** Consume real Entitlement/Scope/Resource quota reservations and verify the current monotonic lease fence in every segment/checkpoint commit.  Canonical batches written as immutable objects; manifest entries carrying run and profile identity, sequence, logical range, count, encoding, byte length and hash; the manifest row as the commit point with the checkpoint advanced in the same transaction; incomplete objects invisible and swept; the checkpoint capturing next tick, RNG, generator and replay positions, pending fault state and the committed segment boundary.

**Testing requirements.** Stale holder resumes after takeover; cancellation races a segment promotion and quota release.  Pause/resume producing the same remaining canonical data; host loss and takeover producing no duplicate and no missing logical range; a crash between object write and manifest commit leaving an invisible object that the sweeper removes; a committed manifest row proven never to reference an unverified object.

**Completion gate.** No stale or duplicate range publishes and no cleanup frees bytes still retained.  **Recovery produces byte-identical remaining canonical data** across pause/resume, host loss and lease takeover.

<a id="rule-wp-51.04"></a>

### WP-51.04 — Client access and native ingestion

**Required design implementation and verification.** Feed retained canonical simulator output through the existing Scope measurement/replay consumer using its recorded profile and configuration. Simulation labels remain synthetic, separate from AI origin. Recompute the statistical/pulse fixtures without changing measurement meaning or treating simulation as hardware evidence.

**What must be fully done.** Reserve bounded duration/samples/bytes/egress and recheck effective term at durable boundaries without AI tokens.  The eleven `simulation.*` operations with durable, idempotent, expected-state commands; authorised manifest listing; resumable hash-verifiable segment fetch over HTTP or object storage; revision- or cursor-based state polling; ArcScope's clearly synthetic `DataSource` feeding the **normal** acquisition pipeline; seed and profile provenance surviving export and copy.

**Testing requirements.** Exhaust each quota independently across concurrent workspaces/replicas; expire term and retry cleanup.  Duplicate, stale and out-of-order commands; a terminal run resisting resurrection; a hash-mismatched segment rejected; **reconnect with realtime disabled entirely, proving the polling path is a complete authoritative fallback**; simulated data flowing through session, capture, decoder, measurement and report unchanged; synthetic labelling surviving export.

**Completion gate.** Each limit has an atomic admission/settlement path with measured units.  With realtime disabled, a client reaches the same state, and simulated data is usable in every normal ArcScope workflow while remaining labelled synthetic.

<a id="rule-wp-51.05"></a>

### WP-51.05 — Limits, entitlement and lifecycle

**What must be fully done.** Deployment policy bounding channels, rates, duration, AST work, per-workspace and global concurrency, queue and wait time, storage, egress and retention, enforced before and during execution with capacity reservation where required. Service-entitlement gating independent of AI credits. Product-resource usage accounting for duration, samples, bytes and egress. Term expiry or suspension stopping generation at a durable boundary as `canceled` with the eligibility reason. Retention and deletion exposing their effect on historical runs and native availability.

**Testing requirements.** Quota exhaustion before side effects; cross-workspace denial; a term expiring mid-run; a suspension mid-run; storage exhaustion; a retention pass with active readers; a partial cancellation reporting partial; **a 24-hour bounded-resource soak**.

**Completion gate.** Every limit is enforced before a side effect, expiry cancels at a durable boundary with its reason, and the soak holds within bounds.

---

**Required implementation and closure from the final review.** Implement and independently verify [05-cloudflare-integration](../../architecture/contracts/05-cloudflare-integration.md#9-job-authorized-objects-control-inventory-and-resource-budgets). Use real service-authorized R2 segments and consume WP34 measurement/report and WP35 import/portability outputs. Check segment hashes/timebase/provenance through Cloud→R2→native analysis/report, and stale grant/fence refusal; no simulator fixture may stand in for a hardware claim. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-51.90"></a>
### WP-51.90 — Verify the owned artifact and real integration

**What must be fully done.** Keep deterministic SimulationRun, quota/admission and segmentation in the AOT host. Use proto for control/results and R2 for verified segments; retain product measurement/input identity.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Real AOT simulation → R2 verified publication → ArcScope ingest/measurement proves deterministic results and failure recovery. No Workers AI dependency or AI debit.

**Completion gate.** Real AOT simulation → R2 verified publication → ArcScope ingest/measurement proves deterministic results and failure recovery. No Workers AI dependency or AI debit. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Slice recovery acceptance.** Kill the real Container before D1 publication, after the guarded segment/checkpoint/outbox batch, and before/after alarm scheduling. Race a duplicate alarm with Cron rescue; assert one committed segment per run/range, deterministic continuation, no lost next-due intent and rejection of stale fences. Alarm delivery itself may repeat. Use the bounded mechanism in architecture23 §1.2, never interactive BEGIN/COMMIT or an in-memory continuation loop.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Six new tables in the `scope` schema, with the manifest-commit ordering |
| Protocol | Eleven `simulation.*` operations plus one realtime hint |
| UI | Scenario selection, run control, synthetic labelling in ArcScope |
| Security | Workspace-scoped resources only; no URL fetch, host file read or cross-workspace reference |
| Platform | Object storage lifecycle and egress accounting |
| Migration | Scenario version immutability; profile versioning affects [SIM-07](../../requirements/products/arcscope.md#rule-sim-07) equality |
| Compatibility | The execution profile is part of run identity, so adding a generator or function is a profile version change |

---

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-51.90](#rule-wp-51.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

**Required evidence addition.** Canonical simulator replay retains measurement profile and synthetic provenance.

| Evidence | Produced by |
|---|---|
| AST bounds, cyclic-dependency and sandbox-denial results | [WP-51.00](#rule-wp-51.00) |
| Determinism, pacing-equality and fault-position results | [WP-51.01](#rule-wp-51.01) |
| Replica contention, fenced takeover and bounded-batch results | [WP-51.02](#rule-wp-51.02) |
| Recovery equality across pause, host loss and takeover | [WP-51.03](#rule-wp-51.03) |
| Command idempotency, realtime-disabled fallback and native ingestion results | [WP-51.04](#rule-wp-51.04) |
| Limit enforcement, entitlement, expiry and 24-hour soak results | [WP-51.05](#rule-wp-51.05) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-51.90](#rule-wp-51.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-51.90](#rule-wp-51.90) and all inherited domain-specific gates must pass on the same candidate closure. Real AOT simulation → R2 verified publication → ArcScope ingest/measurement proves deterministic results and failure recovery. No Workers AI dependency or AI debit.

**[PG-14b](../../assurance/open-gates-register.md#rule-pg-14b) evidence:** [WP-51](#rule-wp-51) — All real-host/storage/native-adapter simulator scenarios in this completion gate, including 24-hour soak; preview/test fakes are insufficient. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** The simulator remains an optional later source for already defined measurement semantics, never a prerequisite for the earlier replay-based analysis package.

**All of the following, with recorded evidence, against the real Cloud host, real storage and the real native adapter ([SIM-20](../../requirements/products/arcscope.md#rule-sim-20)):**

1. Same seed and profile produce identical canonical hashes; a changed seed produces different data.
2. Fault positions are exact, and every injected fault is labelled intentional.
3. Pause/resume, a killed host and a fenced takeover each produce the same remaining canonical data, with no duplicate and no missing logical range.
4. Duplicate, stale and out-of-order commands create no second run and cannot resurrect a terminal run.
5. Malformed AST and malformed CSV fail before any lease, object or quota debit.
6. Quota exhaustion and cross-workspace access are denied; term expiry cancels at a durable boundary with its reason.
7. Reconnect with realtime disabled preserves access to all retained committed data.
8. Partial cancellation reports partial, never success.
9. A 24-hour soak holds within bounded memory, queue and storage.
10. **Simulated data is labelled synthetic through session, export and copy, and never enters a hardware-evidence path.**

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [SIM.01](../delivery/lanes/simulator.md#task-sim-01) | [WP-51.00](51-arcscope-cloud-simulator.md#rule-wp-51.00) (full) | [CLOUD.02](../delivery/lanes/cloud.md#task-cloud-02) (artifact), [CON.21](../delivery/lanes/contracts.md#task-con-21) (contract) |
| [SIM.02](../delivery/lanes/simulator.md#task-sim-02) | [WP-51.01](51-arcscope-cloud-simulator.md#rule-wp-51.01) (the pure-algorithmic half: fixed logical ticks driving canonical data; independently seeded RNG per channel and per fault source; the execution profile pinning numeric/RNG/generator/encoding versions; fault profiles (latency, jitter, drop, duplicate, reorder, disconnect, malformed frame, outlier) at explicit logical boundaries with provenance and counters; same-seed-same-hash and changed-seed-different-data tests; exact fault positions; one channel's RNG not perturbing another's) | none |
| [SIM.03](../delivery/lanes/simulator.md#task-sim-03) | [WP-51.02](51-arcscope-cloud-simulator.md#rule-wp-51.02) (full: architecture-23 DO alarm integration owner plus bounded Container segments, D1 checkpoint/fence/next_due_at, minutely rescue scan; default 1s and 0.25-10s segment bounds; no permanent hosted-service loop)<br>[WP-51.01](51-arcscope-cloud-simulator.md#rule-wp-51.01) (the real-host half: identical hashes under real-time and accelerated pacing; exercise the SimulationPacer state diagram (duplicate/delayed alarm, exhausted automatic retries plus Cron rescue, Container cold start, pause/resume, epoch loss); record 24-hour run cost, alarm/Container/Queue counts and end-to-end pacing distribution against the proposed 5-second target, no hard real-time claim)<br>[WP-51](51-arcscope-cloud-simulator.md#rule-wp-51) 'Slice recovery acceptance' body text (between §5 and §6, no substep id): kill the real Container before D1 publication, after the guarded segment/checkpoint/outbox batch, and before/after alarm scheduling; race a duplicate alarm with Cron rescue; assert one committed segment per run/range, deterministic continuation, no lost next-due intent, rejection of stale fences; alarm delivery itself may repeat; use the bounded mechanism in architecture 23 §1.2, never interactive BEGIN/COMMIT or an in-memory continuation loop ('Slice recovery acceptance' body text (between §5 and §6, no substep id): kill the real Container before D1 publication, after the guarded segment/checkpoint/outbox batch, and before/after alarm scheduling; race a duplicate alarm with Cron rescue; assert one committed segment per run/range, deterministic continuation, no lost next-due intent, rejection of stale fences; alarm delivery itself may repeat; use the bounded mechanism in architecture 23 §1.2, never interactive BEGIN/COMMIT or an in-memory continuation loop; package-level obligation contribution) | [CLOUD.05](../delivery/lanes/cloud.md#task-cloud-05) (artifact), [CLOUD.06](../delivery/lanes/cloud.md#task-cloud-06) (artifact), [CLOUD.07](../delivery/lanes/cloud.md#task-cloud-07) (artifact) |
| [SIM.04](../delivery/lanes/simulator.md#task-sim-04) | [WP-51.03](51-arcscope-cloud-simulator.md#rule-wp-51.03) (full) | [CLOUD.42](../delivery/lanes/cloud.md#task-cloud-42) (artifact), [CLOUD.04](../delivery/lanes/cloud.md#task-cloud-04) (artifact), [COM.07](../delivery/lanes/commerce.md#task-com-07) (artifact) |
| [SIM.05](../delivery/lanes/simulator.md#task-sim-05) | [WP-51.04](51-arcscope-cloud-simulator.md#rule-wp-51.04) (the Cloud API half: the eleven simulation.* operations as durable, idempotent, expected-state commands; authorised manifest listing; resumable hash-verifiable segment fetch over HTTP or object storage; revision-/cursor-based state polling) | [CLOUD.21](../delivery/lanes/cloud.md#task-cloud-21) (artifact), [CLOUD.24](../delivery/lanes/cloud.md#task-cloud-24) (artifact), [CON.21](../delivery/lanes/contracts.md#task-con-21) (contract) |
| [SIM.06](../delivery/lanes/simulator.md#task-sim-06) | [WP-51.04](51-arcscope-cloud-simulator.md#rule-wp-51.04) (the ArcScope consumer half: feed retained canonical simulator output through the existing Scope measurement/replay consumer using its recorded profile and configuration; simulation labels remain synthetic, separate from AI origin; recompute statistical/pulse fixtures without changing measurement meaning or treating simulation as hardware evidence; ArcScope's clearly synthetic DataSource feeding the normal acquisition pipeline; seed and profile provenance surviving export and copy; simulated data flowing through session/capture/decoder/measurement/report unchanged; synthetic labelling surviving export)<br>[WP-51](51-arcscope-cloud-simulator.md#rule-wp-51) §7 required evidence addition (canonical simulator replay retains measurement profile and synthetic provenance) (package-level obligation contribution) | [CON.21](../delivery/lanes/contracts.md#task-con-21) (contract), [SCOPE.01](../delivery/lanes/arcscope.md#task-scope-01) (artifact), [SCOPE.14](../delivery/lanes/arcscope.md#task-scope-14) (artifact), [SCOPE.24](../delivery/lanes/arcscope.md#task-scope-24) (artifact) |
| [SIM.07](../delivery/lanes/simulator.md#task-sim-07) | [WP-51.05](51-arcscope-cloud-simulator.md#rule-wp-51.05) (full) | [COM.05](../delivery/lanes/commerce.md#task-com-05) (artifact), [COM.07](../delivery/lanes/commerce.md#task-com-07) (artifact), [COM.12](../delivery/lanes/commerce.md#task-com-12) (artifact), [POL.03](../delivery/lanes/policy.md#task-pol-03) (artifact) |
| [SIM.08](../delivery/lanes/simulator.md#task-sim-08) | [WP-51.90](51-arcscope-cloud-simulator.md#rule-wp-51.90) (full)<br>[WP-51](51-arcscope-cloud-simulator.md#rule-wp-51) §8 additional completion requirement: the simulator remains an optional later source for already-defined measurement semantics, never a prerequisite for the earlier replay-based analysis package (confirms [WP-34](34-arcscope-analysis-and-reporting.md#rule-wp-34) does not wait on [WP-51](51-arcscope-cloud-simulator.md#rule-wp-51)) (§8 additional completion requirement: the simulator remains an optional later source for already-defined measurement semantics, never a prerequisite for the earlier replay-based analysis package (confirms [WP-34](34-arcscope-analysis-and-reporting.md#rule-wp-34) does not wait on [WP-51](51-arcscope-cloud-simulator.md#rule-wp-51))) | none |
| [SIM.09](../delivery/lanes/simulator.md#task-sim-09) | [WP-51.04](51-arcscope-cloud-simulator.md#rule-wp-51.04) (final-review closure paragraph: real service-authorized R2 segments; consume WP34 measurement/report and WP35 import/portability outputs; Cloud->R2->native hash/timebase/provenance check; stale grant/fence refusal)<br>[WP-51](51-arcscope-cloud-simulator.md#rule-wp-51) 'Required implementation and closure from the final review' paragraph (real service-authorized R2 segments; consume WP34 measurement/report and WP35 import/portability outputs; Cloud->R2->native hash/timebase/provenance check; stale grant/fence refusal) (package-level obligation contribution) | [SCOPE.14](../delivery/lanes/arcscope.md#task-scope-14) (artifact), [SCOPE.18](../delivery/lanes/arcscope.md#task-scope-18) (artifact), [SCOPE.24](../delivery/lanes/arcscope.md#task-scope-24) (artifact) |

**Consumers outside this package:** [REL.06](../delivery/lanes/release.md#task-rel-06), [SIM.10](../delivery/lanes/simulator.md#task-sim-10).

<!-- delivery-graph:end -->

