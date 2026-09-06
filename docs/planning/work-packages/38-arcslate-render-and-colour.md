# WP-38 — ArcSlate Render, Export and Colour Management

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: I — ArcSlate
> Upstream: `37` · Downstream: `39`

> **Goal.** Produce final output that is correct rather than merely fast: colour management as a first-class system, render as a Task bound to an immutable snapshot, export presets, and subtitles — with preview and final render sharing one set of semantics.

---

## 1. Scope and purpose

**In scope.** Colour management — input interpretation, working configuration, viewer display transform and export transform; video scopes as derived views; render requests bound to a revision snapshot; export presets and encoding; subtitle and caption tracks with import and export; and long-export reliability.

**Out of scope.** Integration, capabilities, cloud and portability (`39`). Motion-graphics authoring, explicitly a non-goal.

**Why this package exists.** Colour is where a video product is judged, and it is also where a late change is most expensive: interpretation, working space and output transform must be separated before any export exists, or every rendered file becomes a compatibility liability.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md) `§9`, `§12` | Colour management and the render and export model |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) `§7` | Render path rules, atomic export and plan immutability |
| `WP-37` output | The processing graph and its semantics |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Preview and final render share processing semantics.** Only quality, speed and precision differ. |
| BR-02 | **An override never modifies the original media**; it changes how ArcSlate interprets the source. |
| BR-03 | **Viewer display transform and export transform are separate.** |
| BR-04 | **The colour management backend does not become domain.** The domain holds colour semantic configuration; the backend is infrastructure. |
| BR-05 | **Video scopes are derived views**, never authority, and are distinct from the ArcScope product. |
| BR-06 | **A render task binds a project and sequence revision snapshot.** A render never uses half an old timeline and half a new one. |
| BR-07 | **A render is a native Product Job owned by ArcSlate**, not a Cloud Agent Task (`RN-03` of the ArcSlate requirements, `CM-04` of the runtime architecture, `I-485`). It invokes no model, consumes no AI capacity, and ArcSlate owns its progress, cancellation and recovery. It shares the Product Job lifecycle of `WP-16`; it does not enter `task.task`. |
| BR-08 | **Export writes to a temporary target and commits atomically**; a cancelled or failed render never leaves a file that looks complete. |
| BR-09 | **Proxy render is an explicit, declared choice**, never a silent substitution. |
| BR-10 | **Media analysis output is derived data**, rebuildable and never authority. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcSlate/ArcSlate.Color/` | Colour semantic configuration, interpretation, working configuration, display and export transforms |
| `src/ArcSlate/ArcSlate.Rendering/` | Render planning, execution, atomic commit, progress and cancellation |
| `src/ArcSlate/ArcSlate.Subtitles/` | Subtitle and caption tracks, import and export |
| `src/ArcSlate/ArcSlate.Domain/` | Export preset, render request, render task reference |
| `src/ArcSlate/ArcSlate.Visualization/` | Video scopes as derived views |
| `fixtures/media/golden/` | Golden render fixtures with declared tolerances |
| `tests/ArcSlateMediaTests/` | Colour, render, export, subtitle and long-export suites |

**Major types introduced.** `ColorSemanticConfiguration`, `InputColorInterpretation`, `WorkingColorConfiguration`, `DisplayTransform`, `ExportTransform`, `VideoScope`, `ExportPreset`, `RenderRequest`, `RenderPlan`, `RenderTaskReference`, `SubtitleTrack`, `SubtitleCue`.

---

## 5. Required implementation work

### WP-38.00 — Colour management

**What must be fully done.** Per-asset input colour metadata with an explicit override that never modifies the source. A project and sequence working colour configuration. Separate viewer display transform and export transform. Colour semantics live in the domain; the transform backend is infrastructure behind an interface.

**Testing requirements.** Round-trip colour tests against reference values; an override-non-destructiveness assertion; a separation test asserting a display transform change never alters export output; a domain-purity test on the colour model.

**Completion gate.** Changing a viewer display transform never alters export output, overrides never modify source media, and no backend type appears in the domain.

### WP-38.01 — Video scopes

**What must be fully done.** Waveform, vectorscope, histogram and parade as derived views over the current frame or range, with their measurement point in the pipeline stated explicitly so a reading is interpretable.

**Testing requirements.** Reference-signal tests per scope; a measurement-point disclosure assertion; a performance test at playback rate.

**Completion gate.** Every scope reads correctly against reference signals and states its measurement point.

### WP-38.02 — Render planning and snapshot binding

**What must be fully done.** A render request captures sequence, range, preset, destination and options, and binds an immutable project and sequence revision snapshot. Editing during a render never affects the running render. Proxy render is opt-in and recorded in the output metadata.

**Testing requirements.** An edit-during-render test asserting output is unaffected; a snapshot-binding assertion; a proxy-render disclosure test.

**Completion gate.** Editing during a render never affects its output, and proxy render is explicit and recorded.

### WP-38.03 — Render execution and atomic export

**What must be fully done.** Render as a **native Product Job** with progress, pause, resume and cancellation, owned and recovered by ArcSlate (`BR-07`). Output written to a temporary target and committed atomically. A failure or cancellation leaves no file that looks complete. Long renders survive machine sleep and resume where the platform permits.

**Testing requirements.** Cancellation and failure tests asserting no complete-looking partial file; a long-render soak; a sleep-and-resume test; a disk-full test.

**Completion gate.** No failure or cancellation ever leaves a complete-looking partial file, and a long render survives its soak.

### WP-38.04 — Export presets and encoding

**What must be fully done.** Reusable export presets covering container, codecs, rates, resolution, colour output and audio configuration, with validation that refuses an impossible combination before starting rather than failing midway.

**Testing requirements.** Preset validation negative tests; encode conformance tests per preset against golden fixtures with declared tolerance; a metadata-correctness check on output files.

**Completion gate.** An invalid preset is refused before starting, and every preset produces conformant output within declared tolerance.

### WP-38.05 — Subtitles and captions

**What must be fully done.** Subtitle cues as an independent track role, with import and export in standard formats, timed against the sequence timebase exactly.

**Testing requirements.** Import and export round-trips per supported format; timing exactness tests; a fidelity-statement check for lossy formats.

**Completion gate.** Subtitles round-trip in every supported format with exact timing.

### WP-38.06 — Golden output stability

**What must be fully done.** A golden fixture corpus with declared tolerances, so a codec or backend update cannot silently change output. Any deviation beyond tolerance is a build failure requiring a recorded decision.

**Testing requirements.** Golden comparison across the corpus; a deliberate-change negative test asserting the gate fires.

**Completion gate.** **A change in render output beyond declared tolerance fails the build**, and the corpus covers every supported preset.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Render request and preset storage; snapshot references |
| Protocol | Render capabilities become registrable in `39` |
| UI | Colour, scopes, export and render progress surfaces |
| Security | Output paths validated; no arbitrary write location |
| Platform | Encoder availability and performance per platform |
| Migration | Export preset schema versioning |
| Compatibility | The golden corpus fixes output stability across releases |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Colour round-trip, separation and domain-purity results | `WP-38.00` |
| Scope reference readings and disclosure results | `WP-38.01` |
| Edit-during-render and snapshot binding results | `WP-38.02` |
| Cancellation, failure, soak, sleep and disk-full results | `WP-38.03` |
| Preset validation and encode conformance results | `WP-38.04` |
| Subtitle round-trip and timing results | `WP-38.05` |
| Golden comparison results and the negative gate test | `WP-38.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Changing a viewer display transform never alters export output; overrides never modify source media; no colour backend type appears in the domain.
2. Every video scope reads correctly against reference signals and states its measurement point.
3. Editing during a render never affects its output; proxy render is explicit and recorded in output metadata.
4. **No failure or cancellation ever leaves a complete-looking partial file**, and a long render survives its soak including machine sleep where the platform permits.
5. An invalid export preset is refused before starting; every preset produces conformant output within declared tolerance.
6. Subtitles round-trip in every supported format with exact timing.
7. **A render-output change beyond declared tolerance fails the build**, with the golden corpus covering every supported preset.

---

## 9. Dependencies

**Upstream.** `37` (the processing graph and runtime).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `39` — Integration | Render and export as capabilities and as Tasks |
