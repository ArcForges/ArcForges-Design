<a id="rule-wp-37"></a>

# WP-37 — ArcSlate Playback and Processing Runtime

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: I — ArcSlate
> Upstream: `36` · Downstream: `38`

> **Goal.** Make the timeline play: a decode and processing pipeline behind the native boundary, a processing graph with effects and keyframes, proxies and caches as derived data, and a viewer that keeps the clock correct even when it cannot keep every frame.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcSlate; Platform. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The playback runtime; the native media foundation behind its ABI; the processing graph with effect definitions, instances, parameters and keyframes; adjustment layers and generated media; audio processing; proxies, render caches, thumbnail and waveform caches; the viewer with professional transport; and playback quality state.

**Out of scope.** Final render and export (`38`); colour management as a first-class system (`38`); integration and portability (`39`).

**Why this package exists.** [the current dependency model](../implementation-sequence.md#2-phase-structure) requires ArcSlate to follow its phase order strictly, and [WP-13.03](13-high-risk-technical-probes.md#rule-wp-13.03) already proved decode, synchronisation and the native safety obligations. This package turns that proof into a product runtime.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md) `§7`–`§11` | Viewer, processing graph, proxies, caches and the playback runtime |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) | The native boundary, buffers, threading, GPU and safety obligations |
| [WP-13.03](13-high-risk-technical-probes.md#rule-wp-13.03) output | The decode, synchronisation, sanitiser and fallback conclusions |
| [WP-36](36-arcslate-project-and-timeline.md#rule-wp-36) output | The exact domain and timebase |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **C# is the runtime orchestrator and product authority**; native code decodes, converts and computes only. |
| BR-02 | **A native media foundation must never leak into the domain.** No native type, handle, enumeration or error code appears in a domain, contract or persisted type. |
| BR-03 | **Hardware acceleration is abstract and optional.** Different machines may use different hardware paths; **output must not change because of it**, and a software fallback exists for every operation. |
| BR-04 | **Preview prioritises real time; final render prioritises correctness** — but both share processing semantics. |
| BR-05 | **A dropped preview frame is a playback-quality event, never data loss** ([I-480](../../requirements/01-normative-glossary-and-invariants.md#rule-i-480)). The audio and timeline clock stay correct. |
| BR-06 | **`Effect Definition ≠ Effect Instance`** and **`Keyframe ≠ current parameter value`** ([I-483](../../requirements/01-normative-glossary-and-invariants.md#rule-i-483)). |
| BR-07 | **Keyframe time belongs to its effect's scope** and never silently switches between clip-local and sequence time. |
| BR-08 | **Proxy, render cache, thumbnail and waveform are derived** ([I-484](../../requirements/01-normative-glossary-and-invariants.md#rule-i-484)) and never project authority. Deleting every cache leaves the project intact. |
| BR-09 | **Switching proxy on or off never changes render output**; proxy render is an explicit, declared choice. |
| BR-10 | **Per-frame images never cross a serialization boundary**, and GPU state stays in the process. |
| BR-11 | **Playback quality state is visible**: realtime, reduced quality, using proxy, dropping frames, or requiring render. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcSlate/ArcSlate.Media/` | The managed wrapper over the native foundation: demux, decode, convert, resample |
| `src/ArcSlate/ArcSlate.Native/` | The thin C ABI shim, its loader, safe handles and version negotiation |
| `src/ArcSlate/ArcSlate.Playback/` | The playback engine, clock, scheduler, buffer pools and quality state |
| `src/ArcSlate/ArcSlate.Processing/` | The processing graph, effect definitions and instances, parameters, keyframes, curves |
| `src/ArcSlate/ArcSlate.Audio/` | Audio processing chain, mixing, sample-accurate handling |
| `src/ArcSlate/ArcSlate.Rendering/` | Preview rendering, presentable surfaces, GPU bridge |
| `src/ArcSlate/ArcSlate.Infrastructure/` | Proxy, render cache, thumbnail and waveform stores as derived stores |
| `tests/ArcSlateMediaTests/`, `tests/GraphicsInteropTests/`, `tests/NativeAbiTests/` | Decode, synchronisation, ABI, GPU and cache suites |

**Major types introduced.** `PlaybackEngine`, `PlaybackClock`, `PlaybackQualityState`, `FrameRequest`, `DecodedFrame`, `AudioBuffer`, `ProcessingGraph`, `ProcessingNode`, `EffectDefinition`, `EffectInstance`, `EffectParameter`, `AnimationCurve`, `Keyframe`, `AdjustmentLayer`, `GeneratedMedia`, `ProxyRepresentation`, `RenderCache`, `WaveformCache`, `ThumbnailCache`.

---

## 5. Required implementation work

<a id="rule-wp-37.00"></a>

### WP-37.00 — Native media boundary

**What must be fully done.** The thin C ABI shim with version negotiation at load, safe handles for every native handle, managed input validation before every call, and a sacrificial-process integration suite. Sanitiser builds run in CI. The licence position of every native dependency is recorded.

**Testing requirements.** ABI conformance and version-mismatch rejection; ownership and handle-lifetime tests; sanitiser runs; sacrificial-process crash tests; a domain-purity test asserting no native type escapes.

**Completion gate.** The ABI is version-negotiated, handle lifetime is proven leak-free, sanitiser runs are clean, and no native type escapes the media layer. **This satisfies [PG-03](../../assurance/open-gates-register.md#rule-pg-03) for ArcSlate.**

<a id="rule-wp-37.01"></a>

### WP-37.01 — Decode and buffers

**What must be fully done.** Demux and decode through the boundary into pooled buffers. Buffers are returned on every path including failure. Pool exhaustion is measured and surfaced. Hardware acceleration is discovered at runtime with a proven software fallback, and the chosen path is visible.

**Testing requirements.** Long-run buffer accounting; pool-exhaustion behaviour; forced-software-path equivalence; a decode-capability disclosure test.

**Completion gate.** Buffers are never leaked, exhaustion is surfaced, and the software path produces equivalent output to the accelerated path within declared tolerance.

<a id="rule-wp-37.02"></a>

### WP-37.02 — Playback engine and clock

**What must be fully done.** A playback engine driven by a timeline clock, decoupled from editing so an edit invalidates and re-requests incrementally without stalling. Frames may be dropped; **the audio and timeline clock stay correct**. Playback quality state is computed and visible.

**Testing requirements.** Edit-during-playback tests; audio-video synchronisation measurement under induced load; a drift test over long playback; quality-state coverage.

**Completion gate.** Audio and clock stay correct under load, editing never stalls playback, and quality state reflects reality.

<a id="rule-wp-37.03"></a>

### WP-37.03 — Processing graph

**What must be fully done.** A graph of processing nodes carrying video frames, audio buffers, mattes, transforms, colour data and parameter values. Effect definitions and instances are separate. Parameters are animatable with keyframes and curves, scoped correctly to clip-local or sequence time. Adjustment layers and generated media are first-class.

**Testing requirements.** Graph evaluation correctness per node kind; keyframe scope tests including a clip move; a definition-versus-instance distinction test; adjustment-layer ordering tests.

**Completion gate.** Graph evaluation is correct per node kind, keyframe scope never silently switches, and definitions and instances remain distinct.

<a id="rule-wp-37.04"></a>

### WP-37.04 — Audio

**What must be fully done.** Apply sample ownership per non-overlapping track cut, then mix all track/transition contributions once at each output index; retain filter padding for DSP without emitting padding independently.  Sample-precise audio editing and processing sharing the unified timeline time model. An audio processing chain with clip-level and track-level nodes. Mixing with correct gain staging.

**Testing requirements.** Two mixed tracks, a dissolve, track gap, resampler priming and the NTSC frame-one boundary each produce exactly one mixed output sample at k.  Sample-precision tests; a mixing correctness test against reference output; a synchronisation test with video under load.

**Completion gate.** No global single-clip ownership rule suppresses legal mixing.  Audio is sample-precise, mixes correctly against reference output, and stays synchronised under load.

<a id="rule-wp-37.05"></a>

### WP-37.05 — Proxies and caches

**What must be fully done.** Proxy generation and policy per project and per asset; render cache, waveform cache and thumbnail cache as derived stores. A clip never knows which representation is in use. Deleting every cache leaves the project fully intact. Switching proxies never changes render output.

**Testing requirements.** A proxy-equivalence test comparing output with proxies on and off; a delete-all-caches-and-rebuild test; a clip-ignorance structural test; cache eviction under storage pressure.

**Completion gate.** **Render output is identical with proxies enabled and disabled**, and deleting every cache leaves the project fully intact.

<a id="rule-wp-37.06"></a>

### WP-37.06 — Viewer

**What must be fully done.** Source and sequence viewers with professional transport: play, pause, frame step, shuttle, in and out marking, go-to-timecode, loop and playback rate. Quality state visible. Keyboard-first operation.

**Testing requirements.** Transport coverage; frame-accuracy assertions at step boundaries; keyboard-only operation test.

**Completion gate.** Every transport control is frame-accurate and keyboard-operable, with quality state visible.

---

<a id="rule-wp-37.90"></a>
### WP-37.90 — Verify the owned artifact and real integration

**What must be fully done.** Consume approved native decode/audio/image/color/graphics packages and isolated helper assets. Keep playback clock, processing/proxy and media ownership contracts.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Clean AOT package consumer plus representative decode, synchronization, cancellation, damaged-input and native dependency loading on supported RIDs.

**Completion gate.** Clean AOT package consumer plus representative decode, synchronization, cancellation, damaged-input and native dependency loading on supported RIDs. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Derived cache stores separate from the project store |
| Protocol | None yet; capabilities land in `39` |
| UI | Viewer, timeline playback and quality-state surfaces |
| Security | Untrusted media parsed under the native safety obligations |
| Platform | Hardware acceleration availability and GPU behaviour per platform |
| Migration | Cache formats are derived and freely rebuildable |
| Compatibility | The native ABI version axis becomes live |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| ABI conformance, handle lifetime, sanitiser and sacrificial-process results | [WP-37.00](#rule-wp-37.00) |
| Buffer accounting, exhaustion and software-fallback equivalence | [WP-37.01](#rule-wp-37.01) |
| Synchronisation, drift and quality-state results | [WP-37.02](#rule-wp-37.02) |
| Graph evaluation and keyframe scope results | [WP-37.03](#rule-wp-37.03) |
| Sample precision and mixing reference comparison | [WP-37.04](#rule-wp-37.04) |
| Proxy equivalence and cache-deletion results | [WP-37.05](#rule-wp-37.05) |
| Transport accuracy and keyboard operation results | [WP-37.06](#rule-wp-37.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-37.90](#rule-wp-37.90) and all inherited domain-specific gates must pass on the same candidate closure. Clean AOT package consumer plus representative decode, synchronization, cancellation, damaged-input and native dependency loading on supported RIDs.

**[PG-22](../../assurance/open-gates-register.md#rule-pg-22) evidence:** [WP-37.01](#rule-wp-37.01) — Real packaged hostile media parsing containment and no unrestricted fallback. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-20](../../assurance/open-gates-register.md#rule-pg-20) evidence:** [WP-37.04](#rule-wp-37.04) — Real per-track cut/mix/dissolve/gap ownership and one emitted output sample per index; combine with timeline/OTIO evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-08](../../assurance/open-gates-register.md#rule-pg-08) evidence:** [WP-37](#rule-wp-37) — Playback/processing hardware evidence names device/driver/firmware and lab configuration. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. The native ABI is version-negotiated, handle lifetime is leak-free, sanitiser runs are clean, and **no native type escapes the media layer** — satisfying [PG-03](../../assurance/open-gates-register.md#rule-pg-03) for ArcSlate.
2. Buffers are never leaked; pool exhaustion is surfaced; the software path matches the accelerated path within declared tolerance.
3. Audio and the timeline clock stay correct under load; editing never stalls playback; quality state reflects reality.
4. Graph evaluation is correct per node kind; keyframe scope never silently switches; effect definition and instance remain distinct.
5. Audio is sample-precise and stays synchronised under load.
6. **Render output is identical with proxies enabled and disabled**, and deleting every cache leaves the project fully intact.
7. Every transport control is frame-accurate and keyboard-operable with quality state visible.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [36 arcslate project and timeline](36-arcslate-project-and-timeline.md#rule-wp-36)

**Downstream — consumers of these released outputs.**

- [38 arcslate render and colour](38-arcslate-render-and-colour.md#rule-wp-38)

---
