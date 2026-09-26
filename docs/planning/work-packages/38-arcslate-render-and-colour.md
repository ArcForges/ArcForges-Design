<a id="rule-wp-38"></a>

# WP-38 — ArcSlate Render, Export and Colour Management

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: I — ArcSlate
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Produce final output that is correct rather than merely fast: colour management as a first-class system, render as a Task bound to an immutable snapshot, export presets, and subtitles — with preview and final render sharing one set of semantics.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcSlate; Platform. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Colour management — input interpretation, working configuration, viewer display transform and export transform; video scopes as derived views; render requests bound to a revision snapshot; export presets and encoding; subtitle and caption tracks with import and export; and long-export reliability.

**Out of scope.** Integration, capabilities, cloud and portability (`39`). Motion-graphics authoring, explicitly a non-goal.

**Why this package exists.** Colour is where a video product is judged, and it is also where a late change is most expensive: interpretation, working space and output transform must be separated before any export exists, or every rendered file becomes a compatibility liability.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md) `§9`, `§12` | Colour management and the render and export model |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) `§7` | Render path rules, atomic export and plan immutability |
| [WP-37](37-arcslate-playback-and-processing.md#rule-wp-37) output | The processing graph and its semantics |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Preview and final render share processing semantics.** Only quality, speed and precision differ. |
| <a id="rule-br-02"></a>BR-02 | **An override never modifies the original media**; it changes how ArcSlate interprets the source. |
| <a id="rule-br-03"></a>BR-03 | **Viewer display transform and export transform are separate.** |
| <a id="rule-br-04"></a>BR-04 | **The colour management backend does not become domain.** The domain holds colour semantic configuration; the backend is infrastructure. |
| <a id="rule-br-05"></a>BR-05 | **Video scopes are derived views**, never authority, and are distinct from the ArcScope product. |
| <a id="rule-br-06"></a>BR-06 | **A render task binds a project and sequence revision snapshot.** A render never uses half an old timeline and half a new one. |
| <a id="rule-br-07"></a>BR-07 | **A render is a native Product Job owned by ArcSlate**, not a Cloud Agent Task ([RN-03](../../requirements/products/arcslate.md#rule-rn-03) of the ArcSlate requirements, [CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture, [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). It invokes no model, consumes no AI capacity, and ArcSlate owns its progress, cancellation and recovery. It shares the Product Job lifecycle of [WP-16](16-unified-execution-engine.md#rule-wp-16); it does not enter `task.task`. |
| <a id="rule-br-08"></a>BR-08 | **Export writes to a temporary target and commits atomically**; a cancelled or failed render never leaves a file that looks complete. |
| <a id="rule-br-09"></a>BR-09 | **Proxy render is an explicit, declared choice**, never a silent substitution. |
| <a id="rule-br-10"></a>BR-10 | **Media analysis output is derived data**, rebuildable and never authority. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcSlate/ArcSlate.Color/` | Colour semantic configuration, interpretation, working configuration, display and export transforms |
| `src/ArcSlate/ArcSlate.Rendering/` | Render planning, execution, atomic commit, progress and cancellation |
| `src/ArcSlate/ArcSlate.Subtitles/` | Subtitle and caption tracks, import and export |
| `src/ArcSlate/ArcSlate.Domain/` | Export preset, render request, render task reference |
| `src/ArcSlate/ArcSlate.Visualization/` | Video scopes as derived views |
| `fixtures/media/golden/` | Golden render fixtures with declared tolerances |
| `tests/ArcSlateMediaTests/` | Colour, render, export, subtitle and long-export suites |

**Major types introduced.** `ColorSemanticConfiguration`, `InputColorInterpretation`, `WorkingColorConfiguration`, `DisplayTransform`, `ExportTransform`, `VideoScope`, `ExportPreset`, `RenderRequest`, `RenderPlan`, `ProductJobRef`, `SubtitleTrack`, `SubtitleCue`.

---

## 5. Required implementation work

<a id="rule-wp-38.00"></a>

### WP-38.00 — Colour management

**What must be fully done.** Per-asset input colour metadata with an explicit override that never modifies the source. A project and sequence working colour configuration. Separate viewer display transform and export transform. Colour semantics live in the domain; the transform backend is infrastructure behind an interface.

**Testing requirements.** Round-trip colour tests against reference values; an override-non-destructiveness assertion; a separation test asserting a display transform change never alters export output; a domain-purity test on the colour model.

**Completion gate.** Changing a viewer display transform never alters export output, overrides never modify source media, and no backend type appears in the domain.

<a id="rule-wp-38.01"></a>

### WP-38.01 — Video scopes

**What must be fully done.** Waveform, vectorscope, histogram and parade as derived views over the current frame or range, with their measurement point in the pipeline stated explicitly so a reading is interpretable.

**Testing requirements.** Reference-signal tests per scope; a measurement-point disclosure assertion; a performance test at playback rate.

**Completion gate.** Every scope reads correctly against reference signals and states its measurement point.

<a id="rule-wp-38.02"></a>

### WP-38.02 — Render planning and snapshot binding

**What must be fully done.** A render request captures sequence, range, preset, destination and options, and binds an immutable project and sequence revision snapshot. Editing during a render never affects the running render. Proxy render is opt-in and recorded in the output metadata.

**Testing requirements.** An edit-during-render test asserting output is unaffected; a snapshot-binding assertion; a proxy-render disclosure test.

**Completion gate.** Editing during a render never affects its output, and proxy render is explicit and recorded.

<a id="rule-wp-38.03"></a>

### WP-38.03 — Render execution and atomic export

**Required design implementation and verification.** The frozen render snapshot includes contributing origin kinds. Publish rendered media/subtitles with required hash-bound sidecar as one staged bundle; crash/cancel/missing marker never exposes a complete-looking file. Retrying marking reuses the same render payload; proxy toggling cannot strip provenance.

**What must be fully done.** Render as a **native Product Job** with progress, pause, resume and cancellation, owned and recovered by ArcSlate ([BR-07](#rule-br-07)). Output written to a temporary target and committed atomically. A failure or cancellation leaves no file that looks complete. Long renders survive machine sleep and resume where the platform permits.

**Testing requirements.** Cancellation and failure tests asserting no complete-looking partial file; a long-render soak; a sleep-and-resume test; a disk-full test.

**Completion gate.** No failure or cancellation ever leaves a complete-looking partial file, and a long render survives its soak.

<a id="rule-wp-38.04"></a>

### WP-38.04 — Export presets and encoding

**What must be fully done.** Reusable export presets covering container, codecs, rates, resolution, colour output and audio configuration, with validation that refuses an impossible combination before starting rather than failing midway.

**Testing requirements.** Preset validation negative tests; encode conformance tests per preset against golden fixtures with declared tolerance; a metadata-correctness check on output files.

**Completion gate.** An invalid preset is refused before starting, and every preset produces conformant output within declared tolerance.

<a id="rule-wp-38.05"></a>

### WP-38.05 — Subtitles and captions

**What must be fully done.** Implement authored subtitles and SRT/WebVTT import/export under architecture 23, exact canonical internal ticks and declared nearest-ms bounded loss. Preview <=0.5ms conversion, explicit collapsed-interval adjustment/refusal and retained sidecar/origin.

**Testing requirements.** Independent sub-ms/negative/out-of-range/overlap/collapse cases and round-trip fidelity report; no blanket byte/time identity claim for lossy standard formats.

**Completion gate.** Export obeys the fixed representable profile with acknowledged losses.

<a id="rule-wp-38.06"></a>

### WP-38.06 — Golden output stability

**What must be fully done.** A golden fixture corpus with declared tolerances, so a codec or backend update cannot silently change output. Any deviation beyond tolerance is a build failure requiring a recorded decision.

**Testing requirements.** Golden comparison across the corpus; a deliberate-change negative test asserting the gate fires.

**Completion gate.** **A change in render output beyond declared tolerance fails the build**, and the corpus covers every supported preset.

---

**Required implementation and closure from the final review.** Implement and independently verify [23-simulator-and-interchange](../../architecture/23-simulator-and-interchange.md#5-slate-metadata-render-and-subtitle-profiles). Implement SRT/WebVTT preview/import/export, visible endpoint/style loss reports and collapsed-cue refusal, independent subtitle tracks and explicit burn-in choice. Implement local extraction ProductJob and TranscriptRecord review/adoption under expectedNative/undo/origin. ASR output uses published fixtures here; WP43 provides real model output and WP52 closes the paid end-to-end path. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-38.90"></a>
### WP-38.90 — Verify the owned artifact and real integration

**What must be fully done.** Preserve render snapshot, color/subtitle/output and publication rules. State explicitly that local rendering is a ProductJob, correcting ambiguous generic Task wording; integrate package versions.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Independent render/range/color/output checks and cancel/failure/atomic-publish recovery. No CF Harness or AI budget is required for native render execution.

**Completion gate.** Independent render/range/color/output checks and cancel/failure/atomic-publish recovery. No CF Harness or AI budget is required for native render execution. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**Required evidence addition.** [WP-38.03](#rule-wp-38.03) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Colour round-trip, separation and domain-purity results | [WP-38.00](#rule-wp-38.00) |
| Scope reference readings and disclosure results | [WP-38.01](#rule-wp-38.01) |
| Edit-during-render and snapshot binding results | [WP-38.02](#rule-wp-38.02) |
| Cancellation, failure, soak, sleep and disk-full results | [WP-38.03](#rule-wp-38.03) |
| Preset validation and encode conformance results | [WP-38.04](#rule-wp-38.04) |
| Subtitle round-trip and timing results | [WP-38.05](#rule-wp-38.05) |
| Golden comparison results and the negative gate test | [WP-38.06](#rule-wp-38.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-38.90](#rule-wp-38.90) |



---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-38.90](#rule-wp-38.90) and all inherited domain-specific gates must pass on the same candidate closure. Independent render/range/color/output checks and cancel/failure/atomic-publish recovery. No CF Harness or AI budget is required for native render execution.

**[PG-08](../../assurance/open-gates-register.md#rule-pg-08) evidence:** [WP-38](#rule-wp-38) — Render/colour hardware results bind the lab inventory and software fallback comparison. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

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

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [SLATE.24](../delivery/lanes/arcslate.md#task-slate-24) | [WP-38.00](38-arcslate-render-and-colour.md#rule-wp-38.00) (full) | [SLATE.18](../delivery/lanes/arcslate.md#task-slate-18) (artifact), [SLATE.03](../delivery/lanes/arcslate.md#task-slate-03) (artifact), [NAT.10](../delivery/lanes/native.md#task-nat-10) (artifact) |
| [SLATE.25](../delivery/lanes/arcslate.md#task-slate-25) | [WP-38.01](38-arcslate-render-and-colour.md#rule-wp-38.01) (full) | [SLATE.19](../delivery/lanes/arcslate.md#task-slate-19) (artifact), [NAT.15](../delivery/lanes/native.md#task-nat-15) (artifact), [PLT.27](../delivery/lanes/platform.md#task-plt-27) (artifact) |
| [SLATE.26](../delivery/lanes/arcslate.md#task-slate-26) | [WP-38.02](38-arcslate-render-and-colour.md#rule-wp-38.02) (full) | [SLATE.06](../delivery/lanes/arcslate.md#task-slate-06) (artifact), [SLATE.09](../delivery/lanes/arcslate.md#task-slate-09) (artifact), [SLATE.10](../delivery/lanes/arcslate.md#task-slate-10) (artifact) |
| [SLATE.27](../delivery/lanes/arcslate.md#task-slate-27) | [WP-38.04](38-arcslate-render-and-colour.md#rule-wp-38.04) (full) | [NAT.08](../delivery/lanes/native.md#task-nat-08) (artifact) |
| [SLATE.28](../delivery/lanes/arcslate.md#task-slate-28) | [WP-38.03](38-arcslate-render-and-colour.md#rule-wp-38.03) (full)<br>[WP-38](38-arcslate-render-and-colour.md#rule-wp-38) Security impact: output paths validated, no arbitrary write location (§6) (package-level obligation contribution)<br>[WP-38](38-arcslate-render-and-colour.md#rule-wp-38) Additional completion requirement: content-origin vectors on render/subtitle output paths, including unknown input and failed publication (§8) (package-level obligation contribution) | [SLATE.19](../delivery/lanes/arcslate.md#task-slate-19) (artifact), [SLATE.20](../delivery/lanes/arcslate.md#task-slate-20) (artifact), [NAT.08](../delivery/lanes/native.md#task-nat-08) (artifact), [EXE.01](../delivery/lanes/execution.md#task-exe-01) (artifact) |
| [SLATE.29](../delivery/lanes/arcslate.md#task-slate-29) | [WP-38.05](38-arcslate-render-and-colour.md#rule-wp-38.05) (authored subtitles and SRT/WebVTT import/export: exact canonical ticks, declared nearest-ms bounded loss on export (<=0.5ms), explicit collapsed-interval handling, retained sidecar/origin)<br>[WP-38](38-arcslate-render-and-colour.md#rule-wp-38) Additional completion requirement: content-origin vectors on render/subtitle output paths, including unknown input and failed publication (§8) (package-level obligation contribution)<br>[WP-38](38-arcslate-render-and-colour.md#rule-wp-38) Unlabelled final-review closure: SRT/WebVTT preview/import/export plus local extraction ProductJob/TranscriptRecord adoption (package-level obligation contribution) | [SLATE.06](../delivery/lanes/arcslate.md#task-slate-06) (artifact), [SLATE.01](../delivery/lanes/arcslate.md#task-slate-01) (artifact) |
| [SLATE.30](../delivery/lanes/arcslate.md#task-slate-30) | [WP-38.05](38-arcslate-render-and-colour.md#rule-wp-38.05) (the final-review closure clause: local extraction ProductJob and TranscriptRecord review/adoption under expectedNative/undo/origin (slate.transcribe.v1))<br>[WP-38](38-arcslate-render-and-colour.md#rule-wp-38) Additional completion requirement: content-origin vectors on render/subtitle output paths, including unknown input and failed publication (§8) (package-level obligation contribution)<br>[WP-38](38-arcslate-render-and-colour.md#rule-wp-38) Unlabelled final-review closure: SRT/WebVTT preview/import/export plus local extraction ProductJob/TranscriptRecord adoption (package-level obligation contribution) | [SLATE.16](../delivery/lanes/arcslate.md#task-slate-16) (artifact), [EXE.01](../delivery/lanes/execution.md#task-exe-01) (artifact) |
| [SLATE.31](../delivery/lanes/arcslate.md#task-slate-31) | [WP-38.06](38-arcslate-render-and-colour.md#rule-wp-38.06) (full) | none |
| [SLATE.32](../delivery/lanes/arcslate.md#task-slate-32) | [WP-38.90](38-arcslate-render-and-colour.md#rule-wp-38.90) (full) | none |
| [HAR.91](../delivery/lanes/harness.md#task-har-91) | [WP-38.05](38-arcslate-render-and-colour.md#rule-wp-38.05) (the ASR real-provider closure named explicitly: 'WP43 provides real model output and WP52 closes the paid end-to-end path') | [HAR.06](../delivery/lanes/harness.md#task-har-06) (artifact), [AIR.09](../delivery/lanes/ai-routing.md#task-air-09) (artifact), [AIR.08](../delivery/lanes/ai-routing.md#task-air-08) (artifact) |

**Consumers outside this package:** [HAR.90](../delivery/lanes/harness.md#task-har-90), [REL.03](../delivery/lanes/release.md#task-rel-03), [SLATE.33](../delivery/lanes/arcslate.md#task-slate-33), [SLATE.39](../delivery/lanes/arcslate.md#task-slate-39).

<!-- delivery-graph:end -->

## [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure

Verify native real encode/decode, pixel-tile/color/audio/loudness/analysis output and existing render/subtitle profiles together; byte-identical encoding across libraries is not promised. The referenced normative profile and producer stage matrix are binding inputs. Record independent positive/negative vectors and actual owner integration at this WP's assigned stage; a mock cannot close a real-provider/device requirement.
