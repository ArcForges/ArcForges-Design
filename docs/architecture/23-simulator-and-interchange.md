# Cloud Simulator, Time Model and OTIO Interchange

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**; `§17.1` of the ArcScope requirements ([SIM-01](../requirements/products/arcscope.md#rule-sim-01)–[SIM-20](../requirements/products/arcscope.md#rule-sim-20)); `§17.1` of the ArcSlate requirements ([OT-01](../requirements/products/arcslate.md#rule-ot-01)–[OT-12](../requirements/products/arcslate.md#rule-ot-12))
> Companions: [`05-cloud-architecture.md`](05-cloud-architecture.md) `§2`, [`data-model/01-cloud-data-model.md`](data-model/01-cloud-data-model.md) `§8.3`, [`contracts/01-public-api-operations.md`](contracts/01-public-api-operations.md) `§9.1`, [`12-native-interop-and-media.md`](12-native-interop-and-media.md)

[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) adds two capabilities that had no architecture at all: a **real deterministic Cloud simulator** for ArcScope, and **canonical `.otio` import *and* export** for ArcSlate. Both are stated in the requirements as delivery obligations where a scaffold, a dependency entry or a one-direction adapter is explicitly insufficient ([SIM-20](../requirements/products/arcscope.md#rule-sim-20), [OT-01](../requirements/products/arcslate.md#rule-ot-01)).

They share one property that makes them worth specifying together: **each produces data that must never be confused with the real thing** — synthetic capture is not hardware evidence ([I-496](../requirements/01-normative-glossary-and-invariants.md#rule-i-496)), and an interchange file is not a working project ([I-497](../requirements/01-normative-glossary-and-invariants.md#rule-i-497)).

---

## 1. The deterministic simulator

### 1.1 What determinism actually means here

[SIM-07](../requirements/products/arcscope.md#rule-sim-07) promises that identical effective input under the same supported execution profile yields identical canonical content and hashes. That is a narrower and more honest promise than "the simulator is deterministic", and the narrowing is the design.

| Inside the promise | Outside the promise |
|---|---|
| Sample values, logical timestamps, segment boundaries, canonical encoding, content hashes | Wall-clock timestamps, host and run identifiers, pacing, preview decimation |
| One pinned execution profile: numeric semantics, RNG, generator and encoding versions | Cross-version or cross-CPU floating-point equivalence — **never promised** ([SIM-07](../requirements/products/arcscope.md#rule-sim-07)) |

| # | Rule |
|---|---|
| <a id="rule-sd-01"></a>SD-01 | **The execution profile is part of the run's identity**, not an ambient property of the host. Two runs with the same seed and different profiles are not expected to match, and the profile is recorded on the run row. |
| SD-02 | **Pacing never changes canonical data** ([SIM-06](../requirements/products/arcscope.md#rule-sim-06)). Real-time and bounded accelerated generation produce identical sample values, logical timestamps and hashes; only wall-clock metadata differs. |
| SD-03 | **Every random stream is seeded independently per channel and per fault source** ([SIM-05](../requirements/products/arcscope.md#rule-sim-05)). A shared global RNG would make one channel's consumption perturb another's, which would break [SIM-07](../requirements/products/arcscope.md#rule-sim-07) in a way that is very hard to diagnose. |
| SD-04 | **Logical ticks drive generation, never elapsed wall-clock time.** A host under load produces the same data more slowly, never different data ([SIM-06](../requirements/products/arcscope.md#rule-sim-06), [SIM-15](../requirements/products/arcscope.md#rule-sim-15)). |

### 1.2 Execution inside the single host

The simulator is a **hosted service inside `ArcForges.Cloud.Host`** ([RT-03](05-cloud-architecture.md#rule-rt-03), [SIM-10](../requirements/products/arcscope.md#rule-sim-10)). N identical replicas may all be running it.

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
| <a id="rule-sx-01"></a>SX-01 | **The manifest row is the commit point** ([SIM-11](../requirements/products/arcscope.md#rule-sim-11)). An object exists before it is visible; visibility is the row. A committed manifest row never references an unverified partial object. |
| <a id="rule-sx-02"></a>SX-02 | **The checkpoint advances only after the manifest row commits** ([SIM-12](../requirements/products/arcscope.md#rule-sim-12)), in the same transaction. Reversing that order would let a takeover skip a range that no reader can see. |
| <a id="rule-sx-03"></a>SX-03 | **A publish carrying a stale fence token is rejected** ([SIM-10](../requirements/products/arcscope.md#rule-sim-10)). This is what makes N replicas safe: a paused-then-resumed generator on an old host cannot publish over a new one. |
| SX-04 | **Host loss and lease takeover produce the same remaining canonical data**, with no duplicate and no missing logical range ([SIM-12](../requirements/products/arcscope.md#rule-sim-12)). This is the simulator's central invariant, and [SIM-20](../requirements/products/arcscope.md#rule-sim-20) tests it by killing the host mid-run. |
| SX-05 | **No unbounded generation loop exists** — not in a request handler, and not in the hosted service ([RT-05](05-cloud-architecture.md#rule-rt-05), [SIM-10](../requirements/products/arcscope.md#rule-sim-10)). Work is claimed in batches and yields between them. |
| SX-06 | **Incomplete objects are cleaned** by a sweeper keyed on the absence of a manifest row ([SIM-11](../requirements/products/arcscope.md#rule-sim-11)). |

### 1.3 Bounded evaluation

[SIM-04](../requirements/products/arcscope.md#rule-sim-04) permits a bounded expression AST and prohibits everything that would make it a scripting engine.

| Permitted | Prohibited |
|---|---|
| Constants, time and tick references, channel references, arithmetic, comparison, conditionals, an allowlisted numeric function set | Arbitrary scripts, dynamic compilation, reflection, file access, networking |

| # | Rule |
|---|---|
| <a id="rule-sb-01"></a>SB-01 | **Validation happens before admission** ([SIM-04](../requirements/products/arcscope.md#rule-sim-04), [SO-09](contracts/01-public-api-operations.md#rule-so-09)): acyclic channel dependencies, and bounds on depth, node count and operations per tick. An invalid AST fails **before any lease, object or quota debit**. |
| SB-02 | **The allowlist is closed and versioned with the execution profile.** Adding a function is a profile version change, because it can alter [SIM-07](../requirements/products/arcscope.md#rule-sim-07) equality. |
| SB-03 | **CSV replay reads an explicitly uploaded, workspace-owned resource identified by content hash** ([SIM-18](../requirements/products/arcscope.md#rule-sim-18)), with a bounded parse report. A scenario cannot fetch a URL, read a host file or cross a workspace boundary. |
| SB-04 | **An exported scenario contains no deployment secret or policy value** ([SIM-18](../requirements/products/arcscope.md#rule-sim-18)). |

### 1.4 Faults, preview and back-pressure

| # | Rule |
|---|---|
| <a id="rule-sf-01"></a>SF-01 | **Injected faults carry provenance and counters** ([SIM-05](../requirements/products/arcscope.md#rule-sim-05)). An intentional drop is labelled as intentional, so it can never be mistaken for unexpected data loss — which would make the simulator useless as a verification source. |
| SF-02 | **Faults apply at explicit logical boundaries**, not at arbitrary points, so their positions are reproducible under [SIM-07](../requirements/products/arcscope.md#rule-sim-07). |
| <a id="rule-sf-03"></a>SF-03 | **Preview may visibly decimate or throttle; canonical generation may not** ([SIM-15](../requirements/products/arcscope.md#rule-sim-15)). Under pressure, canonical generation slows, persists safely, or stops with an explicit partial outcome. **Preview overload never silently drops a canonical sample.** |
| SF-04 | **Memory, queues and temporary storage are bounded** ([SIM-15](../requirements/products/arcscope.md#rule-sim-15)), and deployment policy bounds channels, rates, duration, AST work, concurrency, queue time, storage, egress and retention ([SIM-16](../requirements/products/arcscope.md#rule-sim-16)). |

### 1.5 Commercial and lifecycle position

| # | Rule |
|---|---|
| SC-01 | **A `SimulationRun` is a product job, not an Agent Run** ([SIM-01](../requirements/products/arcscope.md#rule-sim-01), [CM-04](09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture). It invokes no model and debits no AI capacity. |
| SC-02 | **It consumes product-resource quota** — duration, samples, bytes, egress — and its output counts against storage quota ([SIM-17](../requirements/products/arcscope.md#rule-sim-17), [C-09](../requirements/00-product-scope-and-portfolio.md#rule-c-09)). |
| SC-03 | **Official simulation requires the active Cloud service entitlement**, independently of AI credits ([SIM-17](../requirements/products/arcscope.md#rule-sim-17)). Self-hosting uses operator grants and the same safety limits. |
| SC-04 | **Term expiry or suspension stops generation at a durable boundary** as `canceled` with the explicit eligibility reason ([SIM-17](../requirements/products/arcscope.md#rule-sim-17)). Committed output then follows retained-data access rules. |
| SC-05 | **Cancel commits a partial outcome, never success for an incomplete range** ([SIM-08](../requirements/products/arcscope.md#rule-sim-08)). |
| <a id="rule-sc-06"></a>SC-06 | **Simulation output is labelled synthetic wherever it appears**, and seed and profile provenance survives export or copy ([SIM-14](../requirements/products/arcscope.md#rule-sim-14), [I-496](../requirements/01-normative-glossary-and-invariants.md#rule-i-496)). A synthetic capture must never be presented as hardware evidence. |
| SC-07 | **Retention, deletion and exhausted storage expose their effect on historical runs and native availability** ([SIM-19](../requirements/products/arcscope.md#rule-sim-19)), and a stored output stays distinguishable from a regenerated one. |

### 1.6 Native consumption

| # | Rule |
|---|---|
| SN-01 | **ArcScope exposes Cloud Simulation as a clearly synthetic `DataSource`** ([SIM-14](../requirements/products/arcscope.md#rule-sim-14)) that feeds the **normal** acquisition pipeline — session, capture, decoder, measurement and report workflows are unchanged. |
| SN-02 | **Segments are fetched by manifest, resumable and hash-verified** ([SIM-13](../requirements/products/arcscope.md#rule-sim-13), [SO-03](contracts/01-public-api-operations.md#rule-so-03)). A hash mismatch is a rejected segment, not a warning. |
| SN-03 | **Realtime is an optional wakeup or preview hint** ([SIM-13](../requirements/products/arcscope.md#rule-sim-13), [RE-07](contracts/03-realtime-and-bridge.md#rule-re-07)). With realtime disabled entirely, polling plus the manifest gives the same access to retained committed data. |
| SN-04 | **Downloaded segments are a verified copy, not a second authority** (`§4` of the data-model overview). Deleting them is a cache operation; the Cloud manifest remains the record. |

---

## 2. OTIO interchange

### 2.1 The position

| # | Rule |
|---|---|
| OA-01 | **Import and export are both required in V1** ([OT-01](../requirements/products/arcslate.md#rule-ot-01)). A dependency entry or a one-direction adapter does not satisfy delivery. |
| OA-02 | **OTIO is an interchange format, never the working store** ([OT-04](../requirements/products/arcslate.md#rule-ot-04), [I-497](../requirements/01-normative-glossary-and-invariants.md#rule-i-497)). Import creates ArcSlate-owned canonical objects with provenance; export binds a **committed** sequence revision and produces a separate artifact. |
| OA-03 | **The support profile is declared**: the pinned library, the supported OTIO schema versions and the supported top-level types ([OT-02](../requirements/products/arcslate.md#rule-ot-02)). V1 accepts and emits a Timeline; an unsupported collection or top-level type produces a clear report, never an implicit partial selection. |
| OA-04 | **`.otio` references media; it never collects, uploads or embeds it** ([OT-08](../requirements/products/arcslate.md#rule-ot-08), [I-497](../requirements/01-normative-glossary-and-invariants.md#rule-i-497)). |

### 2.2 The supported semantic subset

| Supported | Reported, not silently handled |
|---|---|
| Ordered video and audio tracks and stacks; clips; gaps; source ranges; timeline placement; rate-aware times; external and missing media references; names; markers; bounded namespaced metadata; straight cuts; explicitly mapped standard dissolves ([OT-03](../requirements/products/arcslate.md#rule-ot-03)) | Other transitions; unsupported effects, titles, generators, nesting, retiming and metadata ([OT-03](../requirements/products/arcslate.md#rule-ot-03), [OT-07](../requirements/products/arcslate.md#rule-ot-07)) |

| # | Rule |
|---|---|
| OS-01 | **Every item outside the subset receives an item-level disposition** — retained, approximated or omitted ([OT-07](../requirements/products/arcslate.md#rule-ot-07)). Export cannot silently flatten or discard; the user reviews the result or cancels. |
| OS-02 | **Opaque preservation is never advertised as editable support** ([OT-07](../requirements/products/arcslate.md#rule-ot-07)). Carrying a construct through is not the same as understanding it, and the report says which one happened. |
| OS-03 | **Rate and range semantics are preserved exactly, including fractional frame rates and audio alignment** ([OT-05](../requirements/products/arcslate.md#rule-ot-05)). This is why the schema stores `frame_rate_num`/`frame_rate_den` and no float column. |
| OS-04 | **Rounding, representability limits and unsupported time effects are reported against the affected objects** ([OT-05](../requirements/products/arcslate.md#rule-ot-05)). **No silent frame shift is permitted** — a one-frame drift that nobody reports is the defect this rule exists to prevent. |

### 2.3 Round-trip

| # | Rule |
|---|---|
| OR-01 | **Round-trip equality is semantic, not byte-level** ([OT-06](../requirements/products/arcslate.md#rule-ot-06)). The comparison is over supported timeline meaning and media references — never byte equality, and never internal ArcSlate identifiers. |
| OR-02 | **Repeated uses of one source retain their placement** ([OT-06](../requirements/products/arcslate.md#rule-ot-06)). |
| OR-03 | **Core supported edits survive even when external tooling drops private ArcSlate metadata** ([OT-06](../requirements/products/arcslate.md#rule-ot-06)). Fidelity must not depend on a third-party tool preserving our namespace. |
| OR-04 | **Verification uses real fixtures and the pinned official library** ([OT-12](../requirements/products/arcslate.md#rule-ot-12)): both directions, mixed rates, gaps and stack ordering, repeated media, missing references, supported dissolves and markers, unsupported-feature reports, malicious paths, malformed input, cancellation and semantic round-trip. **Merely opening JSON is insufficient.** |

### 2.4 Safety

| # | Rule |
|---|---|
| OY-01 | **Parsing is bounded** in size, depth and item count, rejects malformed or unsupported schema and invalid numeric values, and **stages changes before commit** ([OT-09](../requirements/products/arcslate.md#rule-ot-09)). |
| OY-02 | **No arbitrary adapters, no Python plug-ins, no executable content** ([OT-09](../requirements/products/arcslate.md#rule-ot-09)). This is the single most important safety rule here, because the upstream ecosystem's adapter mechanism is exactly an executable-content path. |
| OY-03 | **Native OTIO use stays behind an owned narrow C ABI and the untrusted-content boundary** ([OT-09](../requirements/products/arcslate.md#rule-ot-09), `§3.2` of the native interop architecture). The slot's obligations are [AD-01](21-platform-and-dependency-matrix.md#rule-ad-01)–[AD-08](21-platform-and-dependency-matrix.md#rule-ad-08) of the platform matrix. |
| OY-04 | **Relative paths resolve only under an explicitly approved base** ([OT-08](../requirements/products/arcslate.md#rule-ot-08)). A file cannot authorise access outside selected roots or initiate a download. |
| OY-05 | **Export writes a temporary destination and publishes atomically after validation** ([OT-10](../requirements/products/arcslate.md#rule-ot-10)). Failure or cancellation preserves both the working project and any existing destination; overwrite requires explicit approval. |
| OY-06 | **Reports exclude unselected absolute paths and secrets** ([OT-10](../requirements/products/arcslate.md#rule-ot-10)). |

### 2.5 Deliberately not V1

| Not required | Authority |
|---|---|
| EDL, AAF, FCPXML and editor-specific adapters | [OT-11](../requirements/products/arcslate.md#rule-ot-11) |
| `.otioz` media bundles | [OT-11](../requirements/products/arcslate.md#rule-ot-11) |
| Native project/collect export and rendered media as part of OTIO | [OT-11](../requirements/products/arcslate.md#rule-ot-11) — separate deliverables |

---

## 3. The ArcSlate time model

> **Corrected 2026-09-07.** The plan required exact frame *and* sample round trips while storing integer frames in the sequence rate and integer samples in a parallel column set, "converted only through the exact rational conversion". **Those two grids do not map onto each other.** At 30000/1001 fps and 48 kHz one frame spans exactly 48000 × 1001/30000 = **1601.6 samples**, so frame 1 is sample 1601.6 — not an integer — and sample 1000 is frame 625/1001 — not an integer either. Rational *arithmetic* is exact; the *grid mapping* is not, and promising both was a guarantee the storage model could not keep.

### 3.1 One canonical domain; every grid is a projection

| Domain | Unit | Role |
|---|---|---|
| **Canonical** | Integer **ticks** at **705 600 000 Hz** | The only domain in which positions are stored, compared, added or persisted |
| Sequence video grid | Integer frames in the sequence's output rate | A **projection** for video editing, display and timecode |
| Sequence audio grid | Integer samples in the sequence's output rate | A **projection** for audio editing and render sample addressing |
| Source stream grid | The stream's own rate and PTS base | A **projection** for decode targets and conform (`§5` of the desktop data model) |

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
| <a id="rule-tb-01"></a>TB-01 | **Canonical position is an integer tick count.** `timeline_item.start_ticks`, `duration_ticks` and every stored position are ticks. **No stored position is a frame number, a sample index, a float or a `TimeSpan`.** |
| <a id="rule-tb-02"></a>TB-02 | Sequence output grids must be exact integer tick counts. This restriction applies to grids ArcSlate creates; source PTS and interchange import use the explicitly reported conversion rules in §3.5 and §3.10. An inexact source time base is not grounds for rejecting otherwise supported media. |
| TB-03 | **Arithmetic is exact and closed.** Adding, subtracting and comparing ticks is integer arithmetic; no conversion occurs, so no rounding occurs. |
| <a id="rule-tb-04"></a>TB-04 | **Frames and samples are projections, computed on demand**, never stored as the position. The parallel integer sample columns of the previous model are removed: two stored grids that cannot agree is the defect itself. |

### 3.2 Three grids, and which is authoritative for what

A sequence has **two output grids**; each source stream has **its own**. Conflating them is the defect this section prevents.

| Grid | Owner | Used for |
|---|---|---|
| **Canonical ticks** | The project | Every stored position; all arithmetic and comparison |
| Sequence **video** grid | The sequence (`frame_rate_num/den`) | Video edit points, display, timecode |
| Sequence **audio** grid | The sequence (`sample_rate`) | Audio edit points, render sample addressing |
| Source **stream** grid | Each `media_stream` | Decode targets, PTS mapping, conform |

| # | Rule |
|---|---|
| <a id="rule-sg-01"></a>SG-01 | **A sequence has one output video grid and one output audio grid; a source stream has its own.** They are separate columns on separate tables (`§5` of the desktop data model), because one sequence routinely contains sources with several different stream bases. |
| <a id="rule-sg-02"></a>SG-02 | **Both sequence grids must be exactly representable in ticks**, and the exact divisors are materialised on the row. A sequence whose grid is not exactly representable cannot be created. |
| <a id="rule-sg-03"></a>SG-03 | **Changing a sequence's output grid reprojects; it never rewrites a stored position.** That is what makes a rate change non-destructive. |

### 3.3 Where exactness is guaranteed

| Guaranteed exact | Bounded, and the bound is stated |
|---|---|
| Tick arithmetic, and any round trip that stays in ticks | Projecting an arbitrary tick onto **either** sequence grid |
| Video frame *n* → ticks → frame *n*, for the sequence's video grid | Projecting a video-grid point onto the audio grid, or the reverse |
| Audio sample *k* → ticks → sample *k*, for the sequence's audio grid | Mapping a source PTS whose base does not divide the tick base ([SM-03](#rule-sm-03)) |
| Any edit point placed on **its own** grid | Retiming to an arbitrary rational speed |

| # | Rule |
|---|---|
| <a id="rule-tg-01"></a>TG-01 | **A round trip through the canonical domain is lossless** for each grid separately: frame↔tick and sample↔tick are exact for every representable grid. |
| <a id="rule-tg-02"></a>TG-02 | **A round trip through the *other* grid is not, and is never claimed.** At 30000/1001 fps and 48 kHz one frame is 1601.6 samples, so frame↔sample cannot round-trip. Nothing depends on it. |
| <a id="rule-tg-03"></a>TG-03 | **Video edits snap to the sequence video grid; audio edits snap to the sequence audio grid.** Both are exact **on their own grid** — an audio edit is sample-precise and a video edit is frame-precise, and neither is forced onto the other's grid. A cut that is both (a clip boundary carrying picture and sound) stores **one canonical tick** and is projected to each grid independently. |
| <a id="rule-tg-04"></a>TG-04 | **Error never accumulates.** Every projection is computed from the canonical value, never from a previous projection. |

### 3.4 Boundary ownership — no duplicated and no missing sample

Directional outward rounding on both sides of a shared boundary **duplicates** the boundary sample. At the frame-1 boundary of a 30000/1001 fps sequence with 48 kHz audio, the boundary falls at sample 1601.6: rounding clip A's end up gives 1602 and clip B's start down gives 1601, so **sample 1601 is emitted twice**.

Output sample ownership is therefore assigned, not rounded.

| # | Rule |
|---|---|
| BO-01 | **A rendered range is half-open in ticks: `[start, end)`.** Adjacency means `A.end == B.start` exactly, in ticks. |
| <a id="rule-bo-02"></a>BO-02 | For adjacent non-overlapping clips **on one track**, sample k contributes from the clip whose half-open range contains `k·T`; a gap contributes silence. This is a per-track cut rule. Multiple tracks and a dissolve intentionally supply multiple weighted contributions at k; the mixer sums them into **one emitted output sample**, rather than selecting one clip globally. |
| BO-03 | Decoder padding primes resamplers/filters and may affect valid output through their kernels. Padding samples are not independently emitted as timeline contributions. After DSP, each contribution is evaluated on its permitted track/transition range, then mixed once at each output index. |
| <a id="rule-bo-04"></a>BO-04 | **[TG-05](../requirements/products/arcscope.md#rule-tg-05)'s outward rounding is retained only for *coverage* requests** — deciding what to decode — and is explicitly **not** used to decide what to emit. |
| <a id="rule-bo-05"></a>BO-05 | **The boundary sample is verified, not assumed.** A fixture at 30000/1001 fps and 48 kHz asserts that a cut at frame 1 emits sample 1601 exactly once and sample 1602 exactly once, across the join ([TV-08](#rule-tv-08)). |

### 3.5 Representability — three different rules

[TB-02](#rule-tb-02) and [SM-03](#rule-sm-03) are not in conflict once the subject of each is named.

| Subject | Rule | Rationale |
|---|---|---|
| **Sequence output grid** | **Must** be exactly representable; a non-representable rate cannot be chosen ([SG-02](#rule-sg-02)) | ArcForges controls this; an inexact output grid would make every stored edit approximate |
| **Source stream timestamps** | **Need not** be. A source whose PTS base does not divide the tick base is **imported**, with its mapping rounded and the rounding reported ([SM-03](#rule-sm-03)) | ArcForges does not control real media, and rejecting it would be a product failure |
| **Interchange (`.otio`)** | A file whose timeline rate is not representable is **imported into a representable sequence grid**, with the substitution stated in the fidelity report; **export refuses to claim** a rate the sequence does not have | Neither silent approximation nor refusal to open |

| # | Rule |
|---|---|
| Output-grid application | [TB-02](#rule-tb-02) forbids creating an inexact **sequence output grid**, without forbidding import/conform of an inexact source base. |
| <a id="rule-sm-03"></a>SM-03 | **A source stream whose base does not divide the tick base is supported**, with per-sample rounding recorded in the conform report. **It is never rejected** — real media includes such sources. |
| <a id="rule-rp-01"></a>RP-01 | **Retiming composes rationals and projects once** ([SM-05](#rule-sm-05)). A non-unit speed generally produces source positions off the source grid; the projection rounds once, at the decode boundary, and the fidelity report records any speed whose mapping is inexact. |
| <a id="rule-rp-02"></a>RP-02 | **Every rounding site is enumerated**: source PTS mapping ([SM-03](#rule-sm-03)), retiming projection ([RP-01](#rule-rp-01)), output-grid projection for display ([TG-01](#rule-tg-01)), encoder-grid projection at export, and the controlled OTIO floating-point boundary (§3.10). **No other code path rounds a position**, and a policy test asserts it ([TV-02](#rule-tv-02)). |

### 3.6 Timecode presentation is not position arithmetic

| # | Rule |
|---|---|
| TC-01 | **Drop-frame timecode is a display convention**, defined against the nominal integer rate. Its rounding is correct *for timecode* and is never applied to a position. |
| TC-02 | **A timecode string is produced from a canonical tick and never parsed back into one for storage.** Round-tripping a position through a timecode string is prohibited, because timecode is lossy by construction at fractional rates. |

### 3.7 Source media, PTS and conform

Source media has its own time base, which is generally neither the sequence rate nor the audio rate.

| # | Rule |
|---|---|
| SM-01 | **A source's own time base is recorded as a rational** (`frame_rate_num`/`frame_rate_den`, `sample_rate`, and the container's PTS time base), and is never assumed equal to the sequence's. |
| <a id="rule-sm-02"></a>SM-02 | **A source PTS converts to canonical ticks exactly where the source base divides the tick base, and with a declared rounding where it does not.** The conversion result is recorded with the media reference, so decode targets are reproducible rather than recomputed differently by two code paths. |
| Source-conform application | Apply [SM-03](#rule-sm-03) from §3.5; the same rule is not redefined here. |
| SM-04 | **Conform never rewrites the source.** It records a mapping; the media file is untouched ([MP-01](12-native-interop-and-media.md#rule-mp-01) of the native interop architecture). |
| <a id="rule-sm-05"></a>SM-05 | **Retiming composes rationals, then projects once.** A speed change multiplies the canonical range by an exact rational and projects to the source's grid at the end — never a chain of grid-to-grid conversions, which is how retiming drift is normally introduced. |

### 3.8 Consequences for the surrounding designs

| Area | What follows |
|---|---|
| **Playback** | The audio clock is the master ([MP-04](12-native-interop-and-media.md#rule-mp-04)); video presentation times are projected from ticks, so a dropped video frame cannot shift audio |
| **OTIO** | The official `RationalTime` contains double value/rate fields. The isolated adapter validates and converts them once under §3.10; canonical edit arithmetic remains integer/rational. Every rate substitution or precision loss is reported. |
| **Export** | The render plan carries canonical ticks; the encoder's grid is a projection, and **emitted samples follow [BO-02](#rule-bo-02) ownership** — outward rounding decides only what to decode ([BO-04](#rule-bo-04)) |
| **Proxy and cache** | Cache keys use canonical ticks, so a proxy generated at one preview rate is valid for another ([MP-06](12-native-interop-and-media.md#rule-mp-06)) |
| **Data model** | `timeline_item` stores ticks; the parallel sample columns are removed ([TB-04](#rule-tb-04)) |

### 3.9 The reference is evidence, not an oracle

ArcVideo and ArcVideoFoundation are `Reference Only` (`§6.2` of the implementation maps), and their time handling is **evaluated, not inherited**.

**Evidence, read 2026-09-07 at ArcVideoFoundation `139eeca`.** `src/util/timecodefunctions.cpp` converts through `double` throughout — `time_dbl`, `std::floor(time_dbl)`, `std::llround((time_dbl - total_seconds) * 1000)` — and derives its frame arithmetic from a **rounded** frame rate: `int rounded_frame_rate = std::llround(frame_rate)`, with the drop-frame calculation then running on that value (`std::llround(frame_rate * 600)`, `std::llround(frame_rate * (2.0/30.0))`). `include/arcvideo/foundation/util/rational.h` exposes `fromDouble`, `toDouble` and a `toRationalTime(double framerate)` overload.

| Reference behaviour | ArcForges position |
|---|---|
| Positions and conversions pass through `double` | **Rejected for positions.** Canonical positions are integer ticks ([TB-01](#rule-tb-01)); only the explicitly bounded OTIO ingress/egress adapter touches external floating-point fields |
| Frame arithmetic derived from `std::llround(frame_rate)` — 29.97 becomes 30 | **Rejected for arithmetic.** Rates are exact rationals, and every supported rate is an exact tick count ([TB-02](#rule-tb-02)) |
| The same rounded rate drives **drop-frame timecode** | **Adopted for display only.** Drop-frame timecode is *defined* against the nominal integer rate, so rounding there is correct — but it is a **presentation** projection and never a stored position ([TB-04](#rule-tb-04)) |
| `rational::fromDouble` / `toDouble` as ordinary conversions | **Not used for canonical position arithmetic.** The official OTIO boundary has the single explicitly tested conversion in §3.10 |

The distinction matters because the reference is not simply wrong: its timecode rounding is right *for timecode*. What would be wrong is carrying that convention into position storage, which is exactly what [TB-01](#rule-tb-01) prevents. **Inheriting a rounding convention without evaluating where it applies is how a subtle drift becomes permanent behaviour.**

---

### 3.10 The official OTIO numeric boundary

The official [`RationalTime` API](https://raw.githubusercontent.com/AcademySoftwareFoundation/OpenTimelineIO/main/src/opentime/rationalTime.h) stores `value` and `rate` as `double`; its validity helper is not a complete finite/range check. This is an external representation, not ArcSlate's canonical rational type.

| # | Rule |
|---|---|
| <a id="rule-ob-01"></a>OB-01 | The OTIO adapter alone accepts/emits finite IEEE-754 value/rate pairs. Reject NaN, infinity, non-positive rate, overflow and impossible negative duration before committing any domain object. Preserve original numeric fields as provenance, not authoritative edit positions. |
| OB-02 | Decode the exact binary rational of each finite double using its sign/exponent/significand. Normalise a rate to a declared standard n/d only when it is within one ULP of that standard's binary encoding; record the normalisation. Decimal 29.97 is not silently relabelled 30000/1001. Compute value/rate × tick-base with checked integer/rational arithmetic and round once, nearest ties-to-even. |
| OB-03 | Choose a representable sequence output grid and report any substitution. Video/audio projections use their own grids. A source/interchange rate need not itself divide the tick base; bounded conversion error is recorded per item, with maximum error and fidelity level. Invalid values fail the import transaction; valid inexact values receive an explicit conform disposition. |
| OB-04 | Export prefers a reduced exact `(value, rate)` pair whose integers fit binary64's exact-integer range, or an exactly represented frame/sample value with the declared normalised standard rate. Re-import through the same boundary must recover the intended canonical value for an exact claim. If the actual pair cannot, quantify the error and declare a lossy disposition before export; never silently claim lossless. A supported grid-aligned interchange must preserve frame/sample addressing. Optional namespaced exact-tick metadata is supplementary, never the only way the core interchange remains meaningful. |
| <a id="rule-ob-05"></a>OB-05 | Precision/range refusal affects that import/export operation, not the native project. No repeated double→rational→double conversions are permitted inside edit, retime, cache or render calculations. Test both directions against the pinned official library, including files with ArcSlate metadata removed. |

## 4. Verification

| # | Obligation | Where |
|---|---|---|
| SV-01 | Same seed and profile produce identical canonical hashes; a changed seed produces different data | [WP-51.01](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.01) |
| SV-02 | Fault positions are exact and reproducible, and every injected fault is labelled as intentional | [WP-51.02](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.02) |
| SV-03 | Pause and resume, and **a killed host with a fenced takeover**, produce the same remaining canonical data with no duplicate or missing range | [WP-51.03](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.03), [WP-21.05](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05) |
| SV-04 | Duplicate start, stale and out-of-order commands create no second run and cannot resurrect a terminal run | [WP-51.03](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.03) |
| SV-05 | Malformed AST and malformed CSV fail before any lease, object or quota debit | [WP-51.02](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.02) |
| SV-06 | Quota exhaustion and cross-workspace access are denied; a term expiry cancels at a durable boundary with its reason | [WP-51.04](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.04), [WP-42.11](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) |
| SV-07 | Reconnect with realtime disabled preserves access to all retained committed data | [WP-51.05](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.05), [WP-24.05](../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.05) |
| SV-08 | Partial cancellation reports partial, never success, and a 24-hour bounded-resource soak holds | [WP-51.05](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.05) |
| SV-09 | Simulated data is labelled synthetic through session, export and copy, and never enters a hardware-evidence path | [WP-51.05](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.05), [WP-34.04](../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.04) |
| OV-01 | OTIO import and export both work against real fixtures and the pinned official library, in both directions | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| OV-02 | Mixed rates, gaps, stack ordering, repeated media and missing references survive semantic round-trip | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| OV-03 | Every unsupported feature produces an item-level disposition; nothing is silently flattened or dropped | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| OV-04 | Fractional frame rates round-trip with no frame shift, and any rounding is reported against its object | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| OV-05 | Malicious paths, malformed input and oversized documents are rejected before commit; no adapter or plug-in loads | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05), [WP-11.05](../planning/work-packages/11-security-foundation.md#rule-wp-11.05) |
| OV-06 | Export cancellation leaves the project and any existing destination untouched | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| TV-01 | Frame → tick → frame and sample → tick → sample round-trip exactly for every supported rate | [WP-36.02](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) |
| <a id="rule-tv-02"></a>TV-02 | No stored position is a frame number, a sample index, a float or a `TimeSpan`; a policy test asserts it | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-36.02](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) |
| TV-03 | Creating an inexact output grid is refused; an inexact source/interchange base imports through the declared conform rules with fidelity evidence | [WP-36.02](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02), [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| TV-04 | Sequential clips at 30000/1001 fps and 48 kHz show **no cumulative drift** over a long sequence, and each cut lands within one sample of its canonical position | [WP-37.02](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.02) |
| TV-05 | A projected range covers its canonical range; adjacent clips leave no one-sample hole | [WP-37.02](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.02) |
| TV-06 | Retiming composes rationals and projects once; a chain of speed changes introduces no drift | [WP-37.02](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.02) |
| TV-07 | A source whose time base does not divide the tick base imports with its rounding recorded in the conform report | [WP-36.02](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) |
| <a id="rule-tv-08"></a>TV-08 | **A cut at frame 1 of a 30000/1001 fps sequence with 48 kHz audio emits sample 1601 exactly once and 1602 exactly once** across the join — no duplicated and no missing sample ([BO-02](#rule-bo-02), [BO-05](#rule-bo-05)) | [WP-37.04](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.04) |
| TV-09 | Video edits are frame-precise and audio edits sample-precise **on their own grids**, and neither is forced onto the other's ([TG-03](#rule-tg-03)) | [WP-36.01](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01), [WP-37.04](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.04) |
| <a id="rule-tv-10"></a>TV-10 | A sequence output grid that is not exactly representable **cannot be created**, while a source stream with an inexact PTS base **imports successfully** with its rounding reported ([TB-02](#rule-tb-02), [SM-03](#rule-sm-03)) | [WP-36.01](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01), [WP-36.02](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) |
| TV-11 | A `.otio` timeline whose rate is not representable imports into a representable sequence grid with the substitution stated in the fidelity report; export never claims a rate the sequence does not have | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| <a id="rule-tv-12"></a>TV-12 | Every rounding site is one of the five enumerated in [RP-02](#rule-rp-02); a policy test asserts no other code path rounds a position | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-36.01](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01) |
| TV-13 | Two simultaneous audio tracks sum at k; a dissolve applies both weights; a track gap supplies silence; adjacent cuts and filter padding do not duplicate emitted samples | [WP-37.04](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.04) |
| TV-14 | Official OTIO value/rate doubles cover standard rational rates, decimal non-standard rates, large values, fractional values, NaN/infinity and both exact/lossy export dispositions without silent drift | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
