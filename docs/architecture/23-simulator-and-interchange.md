# Cloud Simulator, Time Model and OTIO Interchange

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **P2-006**; `§17.1` of the ArcScope requirements (`SIM-01`–`SIM-20`); `§17.1` of the ArcSlate requirements (`OT-01`–`OT-12`)
> Companions: [`05-cloud-architecture.md`](05-cloud-architecture.md) `§2`, [`data-model/01-cloud-data-model.md`](data-model/01-cloud-data-model.md) `§8.3`, [`contracts/01-public-api-operations.md`](contracts/01-public-api-operations.md) `§9.1`, [`12-native-interop-and-media.md`](12-native-interop-and-media.md)

P2-006 adds two capabilities that had no architecture at all: a **real deterministic Cloud simulator** for ArcScope, and **canonical `.otio` import *and* export** for ArcSlate. Both are stated in the requirements as delivery obligations where a scaffold, a dependency entry or a one-direction adapter is explicitly insufficient (`SIM-20`, `OT-01`).

They share one property that makes them worth specifying together: **each produces data that must never be confused with the real thing** — synthetic capture is not hardware evidence (`I-496`), and an interchange file is not a working project (`I-497`).

---

## 1. The deterministic simulator

### 1.1 What determinism actually means here

`SIM-07` promises that identical effective input under the same supported execution profile yields identical canonical content and hashes. That is a narrower and more honest promise than "the simulator is deterministic", and the narrowing is the design.

| Inside the promise | Outside the promise |
|---|---|
| Sample values, logical timestamps, segment boundaries, canonical encoding, content hashes | Wall-clock timestamps, host and run identifiers, pacing, preview decimation |
| One pinned execution profile: numeric semantics, RNG, generator and encoding versions | Cross-version or cross-CPU floating-point equivalence — **never promised** (`SIM-07`) |

| # | Rule |
|---|---|
| SD-01 | **The execution profile is part of the run's identity**, not an ambient property of the host. Two runs with the same seed and different profiles are not expected to match, and the profile is recorded on the run row. |
| SD-02 | **Pacing never changes canonical data** (`SIM-06`). Real-time and bounded accelerated generation produce identical sample values, logical timestamps and hashes; only wall-clock metadata differs. |
| SD-03 | **Every random stream is seeded independently per channel and per fault source** (`SIM-05`). A shared global RNG would make one channel's consumption perturb another's, which would break `SIM-07` in a way that is very hard to diagnose. |
| SD-04 | **Logical ticks drive generation, never elapsed wall-clock time.** A host under load produces the same data more slowly, never different data (`SIM-06`, `SIM-15`). |

### 1.2 Execution inside the single host

The simulator is a **hosted service inside `ArcForges.Cloud.Host`** (`RT-03`, `SIM-10`). N identical replicas may all be running it.

```
claim:    acquire simulation_lease (run_id) with a monotonic fence token   -- SIM-10
loop:     for each bounded batch, while the lease is live:
              generate ticks -> canonical batch
              write object                     (invisible until the manifest row)
              verify object length and hash
              BEGIN
                insert simulation_segment       (guarded by fence token)   -- SIM-11
                advance simulation_checkpoint                              -- SIM-12
              COMMIT
              renew lease; yield                                           -- RT-05
release:  on expiry, loss, pause or terminal state, drop the lease cleanly
```

| # | Rule |
|---|---|
| SX-01 | **The manifest row is the commit point** (`SIM-11`). An object exists before it is visible; visibility is the row. A committed manifest row never references an unverified partial object. |
| SX-02 | **The checkpoint advances only after the manifest row commits** (`SIM-12`), in the same transaction. Reversing that order would let a takeover skip a range that no reader can see. |
| SX-03 | **A publish carrying a stale fence token is rejected** (`SIM-10`). This is what makes N replicas safe: a paused-then-resumed generator on an old host cannot publish over a new one. |
| SX-04 | **Host loss and lease takeover produce the same remaining canonical data**, with no duplicate and no missing logical range (`SIM-12`). This is the simulator's central invariant, and `SIM-20` tests it by killing the host mid-run. |
| SX-05 | **No unbounded generation loop exists** — not in a request handler, and not in the hosted service (`RT-05`, `SIM-10`). Work is claimed in batches and yields between them. |
| SX-06 | **Incomplete objects are cleaned** by a sweeper keyed on the absence of a manifest row (`SIM-11`). |

### 1.3 Bounded evaluation

`SIM-04` permits a bounded expression AST and prohibits everything that would make it a scripting engine.

| Permitted | Prohibited |
|---|---|
| Constants, time and tick references, channel references, arithmetic, comparison, conditionals, an allowlisted numeric function set | Arbitrary scripts, dynamic compilation, reflection, file access, networking |

| # | Rule |
|---|---|
| SB-01 | **Validation happens before admission** (`SIM-04`, `SO-09`): acyclic channel dependencies, and bounds on depth, node count and operations per tick. An invalid AST fails **before any lease, object or quota debit**. |
| SB-02 | **The allowlist is closed and versioned with the execution profile.** Adding a function is a profile version change, because it can alter `SIM-07` equality. |
| SB-03 | **CSV replay reads an explicitly uploaded, workspace-owned resource identified by content hash** (`SIM-18`), with a bounded parse report. A scenario cannot fetch a URL, read a host file or cross a workspace boundary. |
| SB-04 | **An exported scenario contains no deployment secret or policy value** (`SIM-18`). |

### 1.4 Faults, preview and back-pressure

| # | Rule |
|---|---|
| SF-01 | **Injected faults carry provenance and counters** (`SIM-05`). An intentional drop is labelled as intentional, so it can never be mistaken for unexpected data loss — which would make the simulator useless as a verification source. |
| SF-02 | **Faults apply at explicit logical boundaries**, not at arbitrary points, so their positions are reproducible under `SIM-07`. |
| SF-03 | **Preview may visibly decimate or throttle; canonical generation may not** (`SIM-15`). Under pressure, canonical generation slows, persists safely, or stops with an explicit partial outcome. **Preview overload never silently drops a canonical sample.** |
| SF-04 | **Memory, queues and temporary storage are bounded** (`SIM-15`), and deployment policy bounds channels, rates, duration, AST work, concurrency, queue time, storage, egress and retention (`SIM-16`). |

### 1.5 Commercial and lifecycle position

| # | Rule |
|---|---|
| SC-01 | **A `SimulationRun` is a product job, not an Agent Run** (`SIM-01`, `CM-04` of the runtime architecture). It invokes no model and debits no AI capacity. |
| SC-02 | **It consumes product-resource quota** — duration, samples, bytes, egress — and its output counts against storage quota (`SIM-17`, `C-09`). |
| SC-03 | **Official simulation requires the active Cloud service entitlement**, independently of AI credits (`SIM-17`). Self-hosting uses operator grants and the same safety limits. |
| SC-04 | **Term expiry or suspension stops generation at a durable boundary** as `canceled` with the explicit eligibility reason (`SIM-17`). Committed output then follows retained-data access rules. |
| SC-05 | **Cancel commits a partial outcome, never success for an incomplete range** (`SIM-08`). |
| SC-06 | **Simulation output is labelled synthetic wherever it appears**, and seed and profile provenance survives export or copy (`SIM-14`, `I-496`). A synthetic capture must never be presented as hardware evidence. |
| SC-07 | **Retention, deletion and exhausted storage expose their effect on historical runs and native availability** (`SIM-19`), and a stored output stays distinguishable from a regenerated one. |

### 1.6 Native consumption

| # | Rule |
|---|---|
| SN-01 | **ArcScope exposes Cloud Simulation as a clearly synthetic `DataSource`** (`SIM-14`) that feeds the **normal** acquisition pipeline — session, capture, decoder, measurement and report workflows are unchanged. |
| SN-02 | **Segments are fetched by manifest, resumable and hash-verified** (`SIM-13`, `SO-03`). A hash mismatch is a rejected segment, not a warning. |
| SN-03 | **Realtime is an optional wakeup or preview hint** (`SIM-13`, `RE-07`). With realtime disabled entirely, polling plus the manifest gives the same access to retained committed data. |
| SN-04 | **Downloaded segments are a verified copy, not a second authority** (`§4` of the data-model overview). Deleting them is a cache operation; the Cloud manifest remains the record. |

---

## 2. OTIO interchange

### 2.1 The position

| # | Rule |
|---|---|
| OA-01 | **Import and export are both required in V1** (`OT-01`). A dependency entry or a one-direction adapter does not satisfy delivery. |
| OA-02 | **OTIO is an interchange format, never the working store** (`OT-04`, `I-497`). Import creates ArcSlate-owned canonical objects with provenance; export binds a **committed** sequence revision and produces a separate artifact. |
| OA-03 | **The support profile is declared**: the pinned library, the supported OTIO schema versions and the supported top-level types (`OT-02`). V1 accepts and emits a Timeline; an unsupported collection or top-level type produces a clear report, never an implicit partial selection. |
| OA-04 | **`.otio` references media; it never collects, uploads or embeds it** (`OT-08`, `I-497`). |

### 2.2 The supported semantic subset

| Supported | Reported, not silently handled |
|---|---|
| Ordered video and audio tracks and stacks; clips; gaps; source ranges; timeline placement; rate-aware times; external and missing media references; names; markers; bounded namespaced metadata; straight cuts; explicitly mapped standard dissolves (`OT-03`) | Other transitions; unsupported effects, titles, generators, nesting, retiming and metadata (`OT-03`, `OT-07`) |

| # | Rule |
|---|---|
| OS-01 | **Every item outside the subset receives an item-level disposition** — retained, approximated or omitted (`OT-07`). Export cannot silently flatten or discard; the user reviews the result or cancels. |
| OS-02 | **Opaque preservation is never advertised as editable support** (`OT-07`). Carrying a construct through is not the same as understanding it, and the report says which one happened. |
| OS-03 | **Rate and range semantics are preserved exactly, including fractional frame rates and audio alignment** (`OT-05`). This is why the schema stores `frame_rate_num`/`frame_rate_den` and no float column. |
| OS-04 | **Rounding, representability limits and unsupported time effects are reported against the affected objects** (`OT-05`). **No silent frame shift is permitted** — a one-frame drift that nobody reports is the defect this rule exists to prevent. |

### 2.3 Round-trip

| # | Rule |
|---|---|
| OR-01 | **Round-trip equality is semantic, not byte-level** (`OT-06`). The comparison is over supported timeline meaning and media references — never byte equality, and never internal ArcSlate identifiers. |
| OR-02 | **Repeated uses of one source retain their placement** (`OT-06`). |
| OR-03 | **Core supported edits survive even when external tooling drops private ArcSlate metadata** (`OT-06`). Fidelity must not depend on a third-party tool preserving our namespace. |
| OR-04 | **Verification uses real fixtures and the pinned official library** (`OT-12`): both directions, mixed rates, gaps and stack ordering, repeated media, missing references, supported dissolves and markers, unsupported-feature reports, malicious paths, malformed input, cancellation and semantic round-trip. **Merely opening JSON is insufficient.** |

### 2.4 Safety

| # | Rule |
|---|---|
| OY-01 | **Parsing is bounded** in size, depth and item count, rejects malformed or unsupported schema and invalid numeric values, and **stages changes before commit** (`OT-09`). |
| OY-02 | **No arbitrary adapters, no Python plug-ins, no executable content** (`OT-09`). This is the single most important safety rule here, because the upstream ecosystem's adapter mechanism is exactly an executable-content path. |
| OY-03 | **Native OTIO use stays behind an owned narrow C ABI and the untrusted-content boundary** (`OT-09`, `§3.2` of the native interop architecture). The slot's obligations are `AD-01`–`AD-08` of the platform matrix. |
| OY-04 | **Relative paths resolve only under an explicitly approved base** (`OT-08`). A file cannot authorise access outside selected roots or initiate a download. |
| OY-05 | **Export writes a temporary destination and publishes atomically after validation** (`OT-10`). Failure or cancellation preserves both the working project and any existing destination; overwrite requires explicit approval. |
| OY-06 | **Reports exclude unselected absolute paths and secrets** (`OT-10`). |

### 2.5 Deliberately not V1

| Not required | Authority |
|---|---|
| EDL, AAF, FCPXML and editor-specific adapters | `OT-11` |
| `.otioz` media bundles | `OT-11` |
| Native project/collect export and rendered media as part of OTIO | `OT-11` — separate deliverables |

---

## 3. The ArcSlate time model

> **Corrected 2026-09-07.** The plan required exact frame *and* sample round trips while storing integer frames in the sequence rate and integer samples in a parallel column set, "converted only through the exact rational conversion". **Those two grids do not map onto each other.** At 30000/1001 fps and 48 kHz one frame spans exactly 48000 × 1001/30000 = **1601.6 samples**, so frame 1 is sample 1601.6 — not an integer — and sample 1000 is frame 625/1001 — not an integer either. Rational *arithmetic* is exact; the *grid mapping* is not, and promising both was a guarantee the storage model could not keep.

### 3.1 One canonical domain, two projections

| Domain | Unit | Role |
|---|---|---|
| **Canonical** | Integer **ticks** at **705 600 000 Hz** | The only domain in which positions are stored, compared, added or persisted |
| Frame grid | Integer frames in the sequence rate | A **projection** for editing, display and timecode |
| Sample grid | Integer samples in the audio rate | A **projection** for audio rendering and waveform addressing |

The tick base is chosen so that every rate the product supports divides it exactly:

| Rate | Ticks | | Rate | Ticks |
|---|---|---|---|---|
| 24 fps | 29 400 000 | | 8 kHz | 88 200 |
| 25 fps | 28 224 000 | | 22.05 kHz | 32 000 |
| 30 fps | 23 520 000 | | 44.1 kHz | 16 000 |
| 24000/1001 fps | 29 429 400 | | 48 kHz | 14 700 |
| 30000/1001 fps | 23 543 520 | | 96 kHz | 7 350 |
| 60000/1001 fps | 11 771 760 | | 192 kHz | 3 675 |

`int64` at this base spans over three million hours, so range is not a constraint.

| # | Rule |
|---|---|
| TB-01 | **Canonical position is an integer tick count.** `timeline_item.start_ticks`, `duration_ticks` and every stored position are ticks. **No stored position is a frame number, a sample index, a float or a `TimeSpan`.** |
| TB-02 | **Every supported rate is an exact integer number of ticks** (table above). A rate that is not is **not a supported rate**, and is rejected at import with a stated reason rather than silently approximated. |
| TB-03 | **Arithmetic is exact and closed.** Adding, subtracting and comparing ticks is integer arithmetic; no conversion occurs, so no rounding occurs. |
| TB-04 | **Frames and samples are projections, computed on demand**, never stored as the position. The parallel integer sample columns of the previous model are removed: two stored grids that cannot agree is the defect itself. |

### 3.2 Where exactness is guaranteed, and where it is not

| Guaranteed exact | Bounded, and the bound is stated |
|---|---|
| Tick arithmetic, and any round trip that stays in ticks | Projecting an arbitrary tick onto the frame grid |
| Frame *n* → ticks → frame *n* for any *n* | Projecting an arbitrary tick onto the sample grid |
| Sample *k* → ticks → sample *k* for any *k* | Frame *n* → sample index, when the rates are not commensurate |
| Any edit point the user placed on the frame grid | Audio alignment of a cut relative to the frame boundary |

| # | Rule |
|---|---|
| TG-01 | **A round trip through the canonical domain is lossless.** Frame → tick → frame and sample → tick → sample are exact for every supported rate, because each grid point is an integer multiple of the tick. |
| TG-02 | **A round trip through the *other* grid is not, and is never claimed.** Frame → sample → frame can move by up to half a frame at incommensurate rates. Nothing in the design depends on it. |
| TG-03 | **Edit points are frame-grid points by construction.** The user places cuts on frames; the tick value stored is the exact tick of that frame, so the edit is exact and stays exact. |
| TG-04 | **Audio is rendered from ticks, not from a frame-derived sample index.** The renderer converts the clip's tick range to samples once, at render time, with a single declared rounding — so a cut lands within **at most one sample** of its canonical position, and never accumulates across clips. |
| TG-05 | **Rounding is declared and directional, never incidental.** Range starts round toward the start of the range and range ends round toward the end, so a projected range always **covers** its canonical range and adjacent clips never leave a one-sample hole. |
| TG-06 | **Error never accumulates.** Every projection is computed from the canonical value, never from a previous projection. This is why sequential clips cannot drift. |

### 3.3 Source media, PTS and conform

Source media has its own time base, which is generally neither the sequence rate nor the audio rate.

| # | Rule |
|---|---|
| SM-01 | **A source's own time base is recorded as a rational** (`frame_rate_num`/`frame_rate_den`, `sample_rate`, and the container's PTS time base), and is never assumed equal to the sequence's. |
| SM-02 | **A source PTS converts to canonical ticks exactly where the source base divides the tick base, and with a declared rounding where it does not.** The conversion result is recorded with the media reference, so decode targets are reproducible rather than recomputed differently by two code paths. |
| SM-03 | **A source whose base does not divide the tick base is supported**, with its per-sample rounding recorded in the conform report. **It is not rejected** — real media includes such sources — but the approximation is stated rather than hidden. |
| SM-04 | **Conform never rewrites the source.** It records a mapping; the media file is untouched (`MP-01` of the native interop architecture). |
| SM-05 | **Retiming composes rationals, then projects once.** A speed change multiplies the canonical range by an exact rational and projects to the source's grid at the end — never a chain of grid-to-grid conversions, which is how retiming drift is normally introduced. |

### 3.4 Consequences for the surrounding designs

| Area | What follows |
|---|---|
| **Playback** | The audio clock is the master (`MP-04`); video presentation times are projected from ticks, so a dropped video frame cannot shift audio |
| **OTIO** | `RationalTime` maps to ticks exactly where the rate is supported; where a file carries an unsupported rate the import report records it (`OS-04`, `OT-05`). **`OS-03`'s "no silent frame shift" is now achievable**, because the canonical value is preserved and only projections round |
| **Export** | The render plan carries canonical ticks; the encoder's own grid is a projection with `TG-05`'s directional rounding |
| **Proxy and cache** | Cache keys use canonical ticks, so a proxy generated at one preview rate is valid for another (`MP-06`) |
| **Data model** | `timeline_item` stores ticks; the parallel sample columns are removed (`TB-04`) |

### 3.5 The reference is evidence, not an oracle

ArcVideo and ArcVideoFoundation are `Reference Only` (`§6.2` of the implementation maps), and their time handling is **evaluated, not inherited**.

**Evidence, read 2026-09-07 at ArcVideoFoundation `139eeca`.** `src/util/timecodefunctions.cpp` converts through `double` throughout — `time_dbl`, `std::floor(time_dbl)`, `std::llround((time_dbl - total_seconds) * 1000)` — and derives its frame arithmetic from a **rounded** frame rate: `int rounded_frame_rate = std::llround(frame_rate)`, with the drop-frame calculation then running on that value (`std::llround(frame_rate * 600)`, `std::llround(frame_rate * (2.0/30.0))`). `include/arcvideo/foundation/util/rational.h` exposes `fromDouble`, `toDouble` and a `toRationalTime(double framerate)` overload.

| Reference behaviour | ArcForges position |
|---|---|
| Positions and conversions pass through `double` | **Rejected for positions.** Canonical positions are integer ticks (`TB-01`); no position path touches floating point |
| Frame arithmetic derived from `std::llround(frame_rate)` — 29.97 becomes 30 | **Rejected for arithmetic.** Rates are exact rationals, and every supported rate is an exact tick count (`TB-02`) |
| The same rounded rate drives **drop-frame timecode** | **Adopted for display only.** Drop-frame timecode is *defined* against the nominal integer rate, so rounding there is correct — but it is a **presentation** projection and never a stored position (`TB-04`) |
| `rational::fromDouble` / `toDouble` as ordinary conversions | **Not used on any position path.** A double round trip is where drift enters |

The distinction matters because the reference is not simply wrong: its timecode rounding is right *for timecode*. What would be wrong is carrying that convention into position storage, which is exactly what `TB-01` prevents. **Inheriting a rounding convention without evaluating where it applies is how a subtle drift becomes permanent behaviour.**

---

## 4. Verification

| # | Obligation | Where |
|---|---|---|
| SV-01 | Same seed and profile produce identical canonical hashes; a changed seed produces different data | `WP-33.06` |
| SV-02 | Fault positions are exact and reproducible, and every injected fault is labelled as intentional | `WP-33.06` |
| SV-03 | Pause and resume, and **a killed host with a fenced takeover**, produce the same remaining canonical data with no duplicate or missing range | `WP-33.06`, `WP-21.05` |
| SV-04 | Duplicate start, stale and out-of-order commands create no second run and cannot resurrect a terminal run | `WP-33.06` |
| SV-05 | Malformed AST and malformed CSV fail before any lease, object or quota debit | `WP-33.06` |
| SV-06 | Quota exhaustion and cross-workspace access are denied; a term expiry cancels at a durable boundary with its reason | `WP-33.06`, `WP-42.11` |
| SV-07 | Reconnect with realtime disabled preserves access to all retained committed data | `WP-33.06`, `WP-24.05` |
| SV-08 | Partial cancellation reports partial, never success, and a 24-hour bounded-resource soak holds | `WP-33.06` |
| SV-09 | Simulated data is labelled synthetic through session, export and copy, and never enters a hardware-evidence path | `WP-33.06`, `WP-34.04` |
| OV-01 | OTIO import and export both work against real fixtures and the pinned official library, in both directions | `WP-39.05` |
| OV-02 | Mixed rates, gaps, stack ordering, repeated media and missing references survive semantic round-trip | `WP-39.05` |
| OV-03 | Every unsupported feature produces an item-level disposition; nothing is silently flattened or dropped | `WP-39.05` |
| OV-04 | Fractional frame rates round-trip with no frame shift, and any rounding is reported against its object | `WP-39.05` |
| OV-05 | Malicious paths, malformed input and oversized documents are rejected before commit; no adapter or plug-in loads | `WP-39.05`, `WP-11.05` |
| OV-06 | Export cancellation leaves the project and any existing destination untouched | `WP-39.05` |
| TV-01 | Frame → tick → frame and sample → tick → sample round-trip exactly for every supported rate | `WP-36.02` |
| TV-02 | No stored position is a frame number, a sample index, a float or a `TimeSpan`; a policy test asserts it | `WP-05`, `WP-36.02` |
| TV-03 | A rate that is not an exact integer number of ticks is rejected at import with a stated reason, never approximated | `WP-36.02`, `WP-39.05` |
| TV-04 | Sequential clips at 30000/1001 fps and 48 kHz show **no cumulative drift** over a long sequence, and each cut lands within one sample of its canonical position | `WP-37.02` |
| TV-05 | A projected range covers its canonical range; adjacent clips leave no one-sample hole | `WP-37.02` |
| TV-06 | Retiming composes rationals and projects once; a chain of speed changes introduces no drift | `WP-37.02` |
| TV-07 | A source whose time base does not divide the tick base imports with its rounding recorded in the conform report | `WP-36.02` |
