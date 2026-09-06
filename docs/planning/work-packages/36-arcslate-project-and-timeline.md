# WP-36 — ArcSlate Project, Timeline and Media Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: I — ArcSlate
> Upstream: `07`, `10`, `13`, `26` · Downstream: `37`

> **Goal.** Build ArcSlate's domain: project and sequences, the exact time model spanning video frames and audio samples, the media library with assets referenced rather than owned, the timeline with tracks and clips, and non-destructive editing — all in C#, with no native type anywhere near the domain.

---

## 1. Scope and purpose

**In scope.** Project and sequence model; the exact timebase; media assets, streams, availability and metadata; the media library with bins; the timeline with tracks, items, clips and transitions; non-destructive editing operations; undo and project checkpoints; and project persistence with recovery.

**Out of scope.** Playback and processing runtime (`37`); render, export and colour management (`38`); integration and portability (`39`).

**Why this package exists.** `I2 §III.10` places ArcSlate last because it carries the highest complexity and performance risk — and requires it to follow the phase order strictly. The domain must be exact before any runtime touches it, because a timebase error discovered during rendering is a rewrite.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md) | The full product model, domain concepts and V1 scope |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) `§7` | The media pipeline boundary and the domain-purity rules |
| `WP-13.03` output | Decode, synchronisation and native safety probe conclusions |
| [`../../assurance/reference-coverage/arcslate-arcvideo.md`](../../assurance/reference-coverage/arcslate-arcvideo.md) | **The completed ArcSlate Reference Coverage Matrix** — 31 rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, oracle and owner |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix method and the ten-field provenance record that governs any future reuse |
| `WP-07`, `WP-10`, `WP-26` output | Persistence, shell and remote task participation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcSlate Reference Coverage Matrix is a completed, versioned planning input** — [`../../assurance/reference-coverage/arcslate-arcvideo.md`](../../assurance/reference-coverage/arcslate-arcvideo.md), 31 item-level rows, bound to ArcVideo at `caf5651` and ArcVideoFoundation at `139eeca` — ArcSlate's complete reference set under **D-012** as amended (`P2-005`). It was produced before this plan was derived (**D-019**). **This package consumes it and checks it for drift; it does not create it.** |
| BR-02 | **ArcSlate is not a technical exception.** Its architecture is C#, Avalonia and Native AOT with P/Invoke to native media libraries. It is not a Qt application, not a C++ product with a C# shell, and not a C++ worker. |
| BR-03 | **Editing is non-destructive.** Source media is never modified. |
| BR-04 | **`Project ≠ Sequence`** and **`Project ≠ media folder`** (`I-476`). |
| BR-05 | **`MediaAsset ≠ File`** (`I-477`), and an asset identifier is never a file path (`I-192`). |
| BR-06 | **Video frame precision and audio sample precision coexist** (`I-478`), each exact in its own rate domain with explicit conversion. |
| BR-07 | **Sequence frame rate is rational**; drop-frame and non-integer rates are exact, never approximated. |
| BR-08 | **Offline media is a normal product state, not an error** (`I-481`). The project opens, structure is preserved, edit decisions are retained. |
| BR-09 | **A clip must not know which physical file is in use.** It references the asset; the asset resolves at runtime. |
| BR-10 | **No native type, handle, enumeration or error code appears in a domain, contract or persisted type.** |
| BR-11 | **The same asset may have different locations on different devices** and remains one logical asset. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcSlate/ArcSlate.Domain/` | Project, sequence, timebase, media asset, stream, bin, track, timeline item, clip, transition, marker |
| `src/ArcSlate/ArcSlate.Timeline/` | Timeline operations: trim, ripple, roll, slip, slide, insert, overwrite, split, group |
| `src/ArcSlate/ArcSlate.Application/` | Editing application services shared by UI and RPC |
| `src/ArcSlate/ArcSlate.Infrastructure/` | Project store, media index, migration set |
| `src/ArcSlate/ArcSlate.Presentation/`, `.Desktop/` | Timeline, media library and project surfaces |
| `fixtures/formats/arcslate/v1/` | The V1 project fixture |
| `tests/ArcSlate.Tests.Unit/` | Timebase, timeline operation and non-destructiveness suites |

**Major types introduced.** `Project`, `Sequence`, `RationalRate`, `FrameTime`, `SampleTime`, `TimeRange`, `MediaAsset`, `MediaStream`, `MediaMetadata`, `MediaAvailability`, `Bin`, `Track`, `TrackRole`, `TimelineItem`, `Clip`, `Transition`, `Marker`, `ProjectCheckpoint`.

---

## 5. Required implementation work

### WP-36.00 — Project and sequence model

**What must be fully done.** A project as a long-term editing container holding multiple sequences that share one media library. A sequence is a playable, renderable composition with its own timeline and output parameters. Project and sequence have distinct identities and lifecycles.

**Testing requirements.** Multi-sequence project tests; a shared-library assertion; a distinction test against the media folder concept.

**Completion gate.** A project holds multiple sequences over one media library, with project, sequence and folder structurally distinct.

### WP-36.01 — The exact time model

**What must be fully done.** Rational frame rates including drop-frame and non-integer rates, represented exactly. Sample-precise audio time. Explicit, exact conversion between the two domains. Timecode display and parsing that never introduces drift.

**Testing requirements.** Exactness tests across every supported rate including drop-frame; long-duration accumulation tests asserting zero drift; conversion round-trip tests between frame and sample domains.

**Completion gate.** **No drift accumulates over long durations in any supported rate**, and frame–sample conversion round-trips exactly.

### WP-36.02 — Media assets and availability

**What must be fully done.** Media assets with stable logical identity, typed metadata (streams, codecs, dimensions, rate, duration, colour metadata, timecode, channel layout) and an explicit availability state. Assets are referenced externally by default with managed copies as an explicit choice. Offline media is a normal state.

**Testing requirements.** Offline-open test asserting structure and edit decisions survive; relink tests; a per-device location test asserting one logical asset; a structural test asserting no native type is present in the metadata model.

**Completion gate.** A project opens fully with all media offline, relinks correctly, and no native type appears in the domain.

### WP-36.03 — Media library

**What must be fully done.** Bins organising assets, with import defaulting to reference-in-place, background analysis after import, and import completing without waiting for all caches. A media indexing failure is not an import failure.

**Testing requirements.** Import completion timing; a failed-indexing test asserting the asset still exists; a large-library performance test.

**Completion gate.** Import completes without waiting on caches, and an indexing failure never fails the import.

### WP-36.04 — Timeline and tracks

**What must be fully done.** Tracks with roles, timeline items, clips referencing assets with in and out points, and transitions. One asset supports many independent clip instances. Track ordering, enabling, locking and soloing.

**Testing requirements.** Many-clips-one-asset independence; track operation coverage; a structural test asserting a clip holds no file path.

**Completion gate.** Many clips reference one asset independently, and no clip holds a file path.

### WP-36.05 — Editing operations

**What must be fully done.** The professional edit operation set — insert, overwrite, trim, ripple, roll, slip, slide, split, group and ungroup — each exact at frame and sample precision, each non-destructive, and each a command through the single write path.

**Testing requirements.** Exactness tests per operation at boundary conditions; a non-destructiveness assertion on source media; a write-path assertion.

**Completion gate.** Every edit operation is frame- and sample-exact, non-destructive, and routed through the single write path.

### WP-36.06 — Undo, checkpoints and recovery

**What must be fully done.** Undo with composite operation grouping; project checkpoints as an explicit user mechanism distinct from undo; crash recovery to the last committed boundary with explicit loss reporting; migration from prior project versions with semantic preservation.

**Testing requirements.** Undo across composite operations; a distinction test between undo, checkpoint and recovery; kill-during-edit recovery; migration semantic comparison.

**Completion gate.** Undo, checkpoint and recovery behave as three distinct mechanisms, and a crash recovers to a committed boundary with honest loss reporting.

### WP-36.07 — Reference drift check

> **Not a baseline audit.** The ArcSlate matrix is complete and closed `PG-01` and `F-013` before this package began. This sub-step is **maintenance**, and it is the producer of the drift check the package gate requires.

**What must be fully done.** The reference is compared against its bound commit — ArcVideo at `caf5651` and ArcVideoFoundation at `139eeca`. Three outputs are produced:

1. **Changed material**: any file behind a matrix row that changed since the bound commit, with the row re-assessed.
2. **Newly introduced material**: capabilities added upstream since the bound commit, each assessed against the accepted ArcSlate scope. **A new upstream capability does not become an ArcForges requirement by appearing** — it is mapped to an existing requirement or recorded as an accepted exclusion.
3. **Licence re-verification**: the reference's licence files are re-read. A subtree licence can change upstream, and the disposition of every row depends on it.

**Testing requirements.** A drift report listing changed rows, new material with its assessment, and the licence comparison. A completeness check that every changed or new item has a disposition.

**Completion gate.** The drift report exists, every changed and newly introduced item carries a disposition, and the licence position is re-confirmed or amended with a reason. **If the licence position changed, the affected rows' dispositions are corrected before any dependent work continues** (**D-001**).

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The ArcSlate project store and its V1 migration baseline |
| Protocol | ArcSlate capabilities become registrable in `39` |
| UI | Timeline, media library and project surfaces |
| Security | Media reference handling; no path leakage through references |
| Platform | File reference resolution per platform |
| Migration | ArcSlate project format version 1 and its fixture |
| Compatibility | The V1 project format enters the compatibility window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Multi-sequence and structural distinction results | `WP-36.00` |
| Exactness, drift and conversion round-trip results | `WP-36.01` |
| Offline-open, relink and no-native-type results | `WP-36.02` |
| Import timing and indexing-failure results | `WP-36.03` |
| Many-clips-one-asset and no-path results | `WP-36.04` |
| Per-operation exactness and non-destructiveness results | `WP-36.05` |
| Three-mechanism distinction and recovery results | `WP-36.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. **Drift check only**: the reference is compared against its bound commit, and any newly introduced material is assessed against the accepted ArcSlate scope. The matrix and its licence audit were completed as design-stage evidence and closed `PG-01` and `F-013` before this package began. Findings carried in: **F-AL-2** records that ArcVideoFoundation is a **thin utility layer of 27 files**, not the “fat core” its README describes — so no substantial reusable core exists. **`P2-005`** fixes the reference baseline as **ArcVideo and ArcVideoFoundation**; no upstream checkout is sought, and **upstream provenance is preserved** (`RF-06` in the ArcSlate requirements).
2. A project holds multiple sequences over one media library, with project, sequence and folder structurally distinct.
3. **No drift accumulates over long durations in any supported rate**; frame–sample conversion round-trips exactly.
4. A project opens fully with all media offline and relinks correctly; **no native type appears anywhere in the domain, contracts or persisted types**.
5. Import completes without waiting on caches; an indexing failure never fails an import.
6. Many clips reference one asset independently; no clip holds a file path.
7. Every edit operation is frame- and sample-exact, non-destructive, and routed through the single write path.
8. Undo, checkpoint and recovery are three distinct mechanisms, and a crash recovers to a committed boundary with honest loss reporting.

---

## 9. Dependencies

**Upstream.** `07` (persistence), `10` (shell), `13` (probe conclusions), `26` (remote task participation).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `37` — Playback and processing | An exact domain to render from |
| `38` — Render and colour | The sequence and timebase model |
| `39` — Integration | The project model for capabilities, sync and portability |
