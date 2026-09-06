# WP-51 — ArcScope Deterministic Cloud Simulator

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: H — ArcScope *(sequenced after `33`; numbered `51` because `00`–`50` are allocated and a retired identifier is never reused)*
> Upstream: `21`, `23`, `25`, `33` · Downstream: `50`

> **Goal.** Deliver the deterministic Cloud simulator of `SIM-01`–`SIM-20` as a **real capability running through real Cloud persistence, real object storage and the real native acquisition pipeline**. A preview, a canned response or a test fake does not satisfy this package (`SIM-20`).

---

## 1. Scope and purpose

**In scope.** Cloud-owned simulation definitions and immutable scenario versions; the bounded expression AST and its validator; the generator set; fault profiles; lease-fenced execution inside the single Cloud host; canonical segment publication to object storage with a manifest; durable checkpoints; the authorised client fetch path; and ArcScope's native ingestion of simulated data through its normal session, capture, decoder, measurement and report workflows.

**Out of scope.** Hardware acquisition (`WP-33`), analysis semantics (`WP-34`), AI of any kind — **a `SimulationRun` invokes no model** (`SIM-01`).

**Why this package exists.** P2-006 added the simulator as a delivery obligation. It spans Cloud persistence, storage, lease fencing and native ingestion, so it is neither an ArcScope-only nor a Cloud-only body of work, and folding it into `WP-33` would hide a substantial Cloud dependency inside a native package.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) `§17.1` | `SIM-01`–`SIM-20`, the normative source |
| [`../../architecture/23-simulator-and-interchange.md`](../../architecture/23-simulator-and-interchange.md) `§1` | The execution, determinism, fault and back-pressure design |
| [`../../architecture/data-model/01-cloud-data-model.md`](../../architecture/data-model/01-cloud-data-model.md) `§8.3` | The six simulator tables and their commit ordering |
| [`../../architecture/contracts/01-public-api-operations.md`](../../architecture/contracts/01-public-api-operations.md) `§9.1` | The eleven operations and their rules |
| `WP-21` output | The single host, its hosted services and durable leases |
| `WP-25` output | Object storage, upload and download paths |
| `WP-33` output | The native acquisition pipeline the simulator must feed |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A `SimulationRun` is a product job, not an Agent Run** (`SIM-01`). It invokes no model and debits no AI capacity. |
| BR-02 | **The manifest row is the commit point**, and the checkpoint advances only after it, in the same transaction (`SX-01`, `SX-02`). |
| BR-03 | **Lease fencing, not single-instance deployment**, is what makes N replicas safe (`SX-03`, `RT-04`). |
| BR-04 | **Determinism is scoped to the execution profile** (`SD-01`). Cross-version and cross-CPU floating-point equivalence is never promised. |
| BR-05 | **Preview may decimate; canonical generation may not** (`SF-03`). |
| BR-06 | **Injected faults are labelled as intentional** (`SF-01`), so they cannot be mistaken for real data loss. |
| BR-07 | **Synthetic data is labelled synthetic everywhere it appears** (`SC-06`, `I-496`), and never enters a hardware-evidence path. |
| BR-08 | **No scripting, dynamic compilation, reflection, file access or networking** in scenario evaluation (`SB-01`). |

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
| `tests/ArcScope.Tests.Integration/`, `tests/Cloud.Tests.Integration/` | The `SIM-20` acceptance suite |

**Major types introduced.** `SimulationDefinition`, `ScenarioVersion`, `SimulationRun`, `SimulationSegment`, `SimulationCheckpoint`, `SimulationLease`, `ExecutionProfile`, `ChannelSchema`, `ScenarioExpression`, `FaultProfile`, `CanonicalBatch`, `SegmentManifest`, `SimulatedDataSource`.

---

## 5. Required implementation work

### WP-51.00 — Definitions, versions and bounded evaluation

**What must be fully done.** Definitions and **immutable** scenario versions; the channel schema with stable ids, value types, units, rate and timestamp semantics; the V1 generator set — constant, sine, square, triangle, sawtooth, seeded noise, seeded random walk, pulse, step sequence, CSV replay; the bounded AST over constants, time/tick, channel references, arithmetic, comparison, conditionals and an allowlisted numeric function set, validated for acyclic dependencies and bounds on depth, node count and per-tick operations **before admission**.

**Testing requirements.** A malformed-AST corpus rejected before any side effect; a cyclic-dependency case; each bound exceeded; a definition edit proving existing runs are unaffected; a CSV replay with a bounded parse report; a scenario attempting a URL fetch, a host file read and a cross-workspace reference, each denied.

**Completion gate.** No scenario input reaches evaluation without passing bounds, and an invalid scenario consumes no lease, object or quota.

### WP-51.01 — Deterministic generation and faults

**What must be fully done.** Fixed logical ticks driving canonical data; independently seeded RNG per channel and per fault source; the execution profile pinning numeric semantics, RNG, generator and encoding versions; real-time and bounded accelerated pacing that leave sample values, logical timestamps and hashes unchanged; fault profiles for latency, jitter, drop, duplicate, reorder, disconnect, malformed frame and outlier at explicit logical boundaries, each carrying provenance and counters.

**Testing requirements.** Same seed and profile producing identical canonical hashes; a changed seed producing different data; identical hashes under real-time and accelerated pacing; exact fault positions; a proof that one channel's RNG consumption does not perturb another's.

**Completion gate.** `SIM-07` equality holds within a profile, and every injected fault is distinguishable from unexpected loss.

### WP-51.02 — Lease-fenced execution in the single host

**What must be fully done.** The hosted service claims a run by durable lease with a monotonic fence token, generates in bounded batches, renews while working, and releases cleanly on expiry, pause or terminal state. No unbounded loop exists in a request handler or in the hosted service. A publish carrying a stale fence token is rejected.

**Testing requirements.** Two replicas contending for one run; a killed host with a fenced takeover; a paused generator on an old host attempting to publish after takeover; lease expiry under a stalled batch; a bounded-batch assertion that no single iteration exceeds its budget.

**Completion gate.** N identical replicas run the simulator with no duplicate segment and no unbounded loop.

### WP-51.03 — Canonical publication, checkpoints and recovery

**What must be fully done.** Canonical batches written as immutable objects; manifest entries carrying run and profile identity, sequence, logical range, count, encoding, byte length and hash; the manifest row as the commit point with the checkpoint advanced in the same transaction; incomplete objects invisible and swept; the checkpoint capturing next tick, RNG, generator and replay positions, pending fault state and the committed segment boundary.

**Testing requirements.** Pause/resume producing the same remaining canonical data; host loss and takeover producing no duplicate and no missing logical range; a crash between object write and manifest commit leaving an invisible object that the sweeper removes; a committed manifest row proven never to reference an unverified object.

**Completion gate.** **Recovery produces byte-identical remaining canonical data** across pause/resume, host loss and lease takeover.

### WP-51.04 — Client access and native ingestion

**What must be fully done.** The eleven `simulation.*` operations with durable, idempotent, expected-state commands; authorised manifest listing; resumable hash-verifiable segment fetch over HTTP or object storage; revision- or cursor-based state polling; ArcScope's clearly synthetic `DataSource` feeding the **normal** acquisition pipeline; seed and profile provenance surviving export and copy.

**Testing requirements.** Duplicate, stale and out-of-order commands; a terminal run resisting resurrection; a hash-mismatched segment rejected; **reconnect with realtime disabled entirely, proving the polling path is a complete authoritative fallback**; simulated data flowing through session, capture, decoder, measurement and report unchanged; synthetic labelling surviving export.

**Completion gate.** With realtime disabled, a client reaches the same state, and simulated data is usable in every normal ArcScope workflow while remaining labelled synthetic.

### WP-51.05 — Limits, entitlement and lifecycle

**What must be fully done.** Deployment policy bounding channels, rates, duration, AST work, per-workspace and global concurrency, queue and wait time, storage, egress and retention, enforced before and during execution with capacity reservation where required. Service-entitlement gating independent of AI credits. Product-resource usage accounting for duration, samples, bytes and egress. Term expiry or suspension stopping generation at a durable boundary as `canceled` with the eligibility reason. Retention and deletion exposing their effect on historical runs and native availability.

**Testing requirements.** Quota exhaustion before side effects; cross-workspace denial; a term expiring mid-run; a suspension mid-run; storage exhaustion; a retention pass with active readers; a partial cancellation reporting partial; **a 24-hour bounded-resource soak**.

**Completion gate.** Every limit is enforced before a side effect, expiry cancels at a durable boundary with its reason, and the soak holds within bounds.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Six new tables in the `scope` schema, with the manifest-commit ordering |
| Protocol | Eleven `simulation.*` operations plus one realtime hint |
| UI | Scenario selection, run control, synthetic labelling in ArcScope |
| Security | Workspace-scoped resources only; no URL fetch, host file read or cross-workspace reference |
| Platform | Object storage lifecycle and egress accounting |
| Migration | Scenario version immutability; profile versioning affects `SIM-07` equality |
| Compatibility | The execution profile is part of run identity, so adding a generator or function is a profile version change |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| AST bounds, cyclic-dependency and sandbox-denial results | `WP-51.00` |
| Determinism, pacing-equality and fault-position results | `WP-51.01` |
| Replica contention, fenced takeover and bounded-batch results | `WP-51.02` |
| Recovery equality across pause, host loss and takeover | `WP-51.03` |
| Command idempotency, realtime-disabled fallback and native ingestion results | `WP-51.04` |
| Limit enforcement, entitlement, expiry and 24-hour soak results | `WP-51.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence, against the real Cloud host, real storage and the real native adapter (`SIM-20`):**

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

**Upstream.** `21` (the host, hosted services, leases), `23` (public API), `25` (object storage), `33` (the native acquisition pipeline).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `34` — ArcScope analysis *(benefit, **not** a dependency)* | An **additional** repeatable synthetic source. `WP-34` must not wait for this package: `SD-09` makes **file/replay** a V1 adapter delivered in `WP-33`, and that is `WP-34`'s repeatable source. Making `34` depend on `51` would put native analysis behind Cloud persistence, storage and leases — the same backward dependency `§3` of the implementation sequence forbids |
| `50` — Full-platform release | The simulator acceptance evidence |
