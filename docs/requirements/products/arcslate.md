# ArcSlate — Product Requirements

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Product identity: `arcslate` · Positioning: **Local-first Professional Non-linear Video Editing Workspace**
> Governing authority: **D-002** (ArcSlate inherits product direction from ArcVideo, not its model), Stage 13 §6 (**ArcSlate is not a technical exception**)
> Companions: [`../12-quality-and-compatibility-contract.md`](../12-quality-and-compatibility-contract.md), [`../13-data-formats-and-portability.md`](../13-data-formats-and-portability.md), [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md)

> **A local-first professional NLE, completely rebuilt in C# and Avalonia.**
> **Preserve the editing ideas. Rebuild the product model. Do not translate the C++ application into C#.**

---

## 1. Reference posture

| # | Requirement |
|---|---|
| RF-01 | **ArcVideo and ArcVideoFoundation are ArcSlate's product and behaviour references** (**D-012** as amended 2026-09-05, `P2-005`), not architecture authorities. They inform product concepts, editing workflows, timeline behaviour, media workflows, the feature set, project behaviour, interaction patterns and existing implementation experience. |
| RF-02 | **Class-to-class translation is prohibited.** A reference class list is **not** a migration checklist. What transfers is **product intent, never implementation shape**. |
| RF-03 | **ArcSlate is not a technical exception** (Stage 13 §6). Its architecture is C#, .NET, Avalonia and Native AOT, with `[LibraryImport]`/P/Invoke to native media libraries where necessary. It is **not** a Qt application, **not** a C++ product with a C# shell, and **not** a C++ worker. |
| RF-04 | **ArcVideo and ArcVideoFoundation are ArcSlate's references** (**D-012** as amended, `P2-005`). Both are **GPL-3.0-only**, so both are **behavioural reference only**: **D-013** prohibits copying, translating or porting from either. Reuse would in any case be licence-gated and provenance-gated with file-level SPDX evidence — the **F-013** gate, closed on the recorded determinations. |
| RF-05 | **The ArcSlate Reference Coverage Matrix is complete** — [`../../assurance/reference-coverage/arcslate-arcvideo.md`](../../assurance/reference-coverage/arcslate-arcvideo.md), 31 item-level rows bound to ArcVideo `caf5651` and ArcVideoFoundation `139eeca`. It is a versioned planning input; `WP-36.07` checks it for drift. **No separate migration matrix from an upstream project is required**, because no upstream checkout is obtained and no material is reused (`RF-04`). |
| RF-06 | **Upstream provenance is preserved.** ArcVideo is a documented fork; its GPL-3.0 obligations, upstream copyright and attribution to the original authors stand, and are recorded wherever inherited material requires them (**D-013**). Removing an upstream project from the reference map never removes its provenance. |

---

## 2. Product definition and level

| # | Requirement |
|---|---|
| PD-01 | **ArcSlate is a focused professional NLE**, not an attempt to be every post-production tool at once. It is not a motion-graphics suite, not a professional DAW, and not a colour-finishing system — while being genuinely professional at editing. |
| PD-02 | **The timeline is the heart of the product.** |
| PD-03 | **AI enhances editing; it never replaces the timeline editor** (`I-486`). |

### 2.1 Product principles

| # | Principle |
|---|---|
| PP-01 | **Non-destructive.** Source media is never modified. |
| PP-02 | **One Media Asset, many Clip instances** (`I-477`). Twenty clips of one asset are twenty instances of one identity. |
| PP-03 | **Preview prioritises real time; final render prioritises correctness and quality** (`I-479`). |
| PP-04 | **Proxy, render cache, thumbnails and waveforms are derived representations** (`I-484`) and are never project authority. |
| PP-05 | **Exact time arithmetic.** Floating-point seconds are never authoritative (`§4`). |

---

## 3. Domain structure

```
ArcSlate Project
 ├── Media Library
 │    └── Bin → MediaAsset → (ManagedMedia | ExternalMediaReference) → MediaStream
 ├── Sequence (many)
 │    ├── SequenceSettings (snapshot)
 │    └── Track (role-typed)
 │         └── TimelineItem → Clip · Transition · GeneratedMedia · Title · SubtitleCue
 ├── ProcessingGraph → ProcessingNode → EffectInstance → EffectParameter → AnimationCurve → Keyframe
 ├── Marker · RangeMarker
 ├── ProxyRepresentation · RenderCache · ThumbnailCache · WaveformCache   [Derived]
 └── ExportPreset · RenderRequest · RenderTaskReference · ProjectCheckpoint
```

| # | Requirement |
|---|---|
| DS-01 | **`Project` = ArcSlate's long-term editing work container.** **`Project ≠ Sequence`** and **`Project ≠ media folder`** (`I-476`). |
| DS-02 | **A project supports multiple sequences** sharing one media library. |
| DS-03 | **`Sequence` = a playable, renderable edit composition with its own timeline, output parameters and edit structure.** |
| DS-04 | **Sequence settings are a stable snapshot.** Changing project defaults does not silently reinterpret an existing sequence. |
| DS-05 | **A sequence may be the source of another sequence** (nested sequence / compound clip). |
| DS-06 | **`Bin` is logical organisation, not a filesystem folder.** It organises the ArcSlate project, not the disk. |

---

## 4. Time model

> **No core timeline time may use floating-point seconds as authoritative time.**

| # | Requirement |
|---|---|
| TM-01 | The authoritative time model is **integer or rational**, with an explicit **time base**. |
| TM-02 | **Video frame precision and audio sample precision must coexist** (`I-478`). Both are exact, in their own rate domains, related by explicit conversion. |
| TM-03 | **Sequence frame rate is rational** — drop-frame and non-integer rates are represented exactly, never approximated. |
| TM-04 | **`SourceTime ≠ TimelineTime`** (`I-478`). A clip carries a source range and a timeline range, and they are separate types. |
| TM-05 | **ArcSlate time is not forced into the general unit system** (`UN-05`). It is a first-class rational time and time-base model. |
| TM-06 | Every arithmetic operation on timeline positions is exact; accumulation drift is structurally impossible, not merely unlikely. |

---

## 5. Media

| # | Requirement |
|---|---|
| MD-01 | **`MediaAsset` = a stable logical identity for a media source usable in ArcSlate.** |
| MD-02 | **`MediaAsset ≠ File`** (`I-477`), and **`AssetId` is never a file path** (`I-192`). |
| MD-03 | **Original media is referenced externally by default** (`AS-02`), and **managed media must also be available** as an explicit choice. |
| MD-04 | **Collect / Consolidate Project** gathers external media into a managed, portable form on request, **without destroying the originals** (`EX-08` in the data requirements). |
| MD-05 | **Offline media is a normal product state, not an error** (`AS-04`). The project still opens, structure is preserved, and edit decisions are retained. |
| MD-06 | **Relink is a first-class capability**, verifying by content — asset identity, expected size, content hash and metadata — not by filename (`AS-05`). |
| MD-07 | **A clip must not know which physical file is currently in use.** It references the `MediaAsset`; the asset resolves to original, managed copy or proxy at runtime (`PX-01`). |
| MD-08 | **The same `MediaAsset` may have different locations on different devices** and remains one logical asset (`§13`). |
| MD-09 | A media asset carries typed **MediaMetadata** — streams, codecs, dimensions, rate, duration, colour metadata, timecode, audio channel layout — and an explicit **MediaAvailability** state. |

---

## 6. Timeline editing

| # | Requirement |
|---|---|
| TL-01 | **`Clip` = a non-destructive instantiation of a source or asset on the sequence timeline** (`I-477`). |
| TL-02 | **One asset may have unlimited clips**, each with its own source range, effects and parameters. |
| TL-03 | **`ClipId` is stable** across trims, moves and edits (`BL-01` analogue). |
| TL-04 | **Tracks are role-typed** — video, audio, subtitle, and later others — so behaviour follows role rather than index. |
| TL-05 | **The model is a traditional track-based non-destructive NLE**, familiar to professional editors. |
| TL-06 | The complete basic operation set: insert, overwrite, move, trim (in/out), ripple trim, roll, slip, slide, split/razor, delete, ripple delete, lift, extract, duplicate, group and ungroup, enable/disable, speed/retime, and reorder tracks. |
| TL-07 | **Every one of those is a semantic command**, not a UI coordinate manipulation. This is what makes undo, scripting, agent capability and testing tractable (`§10`). |
| TL-08 | **Snap is a timeline service**, not mouse-cursor logic: it operates on timeline model positions with declared snap targets and tolerances. |
| TL-09 | **Linked audio and video form a link group.** **`Link ≠ shared identity`** (`I-489`): linked items move together by default and remain independent objects that can be unlinked. |
| TL-10 | **`Transition` is a declared timeline relationship and processing element** (`I-481`), never an incidental overlap of two clips. Its essence is realised through the processing graph. |
| TL-11 | **Markers are first-class objects**, not coloured dots: they carry identity, time or range, name, comment, colour, and category — and may be attached to a sequence or to a clip. |

---

## 7. Viewer and playback

| # | Requirement |
|---|---|
| VW-01 | Two logical viewer roles: a **source viewer** for the original media asset, and a **sequence viewer** for the current sequence output. |
| VW-02 | Professional transport is required: play/pause, frame step forward and back, shuttle (JKL-style), in/out marking, go-to-timecode, loop, and playback rate. |
| VW-03 | **Playback and editing are decoupled.** An edit invalidates and re-requests media incrementally; it does not stall the editor. |
| VW-04 | **Realtime playback quality strategy**: drop displayed frames if necessary, but **keep the audio and timeline clock correct**. |
| VW-05 | **`Dropped preview frame ≠ dropped media data`** (`I-480`). Not displaying a frame is a playback quality event, never data loss. |
| VW-06 | **Playback quality state is visible**: realtime, reduced quality, using proxy, dropping frames, or requiring render. |

---

## 8. Processing model

**One typed processing graph, two user-interface surfaces.**

| # | Requirement |
|---|---|
| PG-01 | The long-term authoritative processing model is a **typed processing graph**. |
| PG-02 | The **Effect Stack / Inspector** and the **Advanced Node Graph** are **two surfaces over one engine**. The effect stack must not create a second effect model (`I-482`). |
| PG-03 | **Nodes are typed processing nodes**, implemented in C# and AOT-compatible. |
| PG-04 | Principal graph data types include video frame, audio buffer, mask/matte, transform, colour data and parameter values. |
| PG-05 | **Ports are typed and not arbitrarily connectable.** An invalid connection is a validation error, not a runtime surprise. |
| PG-06 | **The node graph is dataflow, not arbitrary code execution** (`I-483`). Custom processing arrives through the extension platform, out of process, under the schema-described capability protocol. |
| PG-07 | **`EffectDefinition ≠ EffectInstance`** (`I-482`). |
| PG-08 | **Effect parameters can be animated.** **`Keyframe ≠ current parameter value`** (`I-483`). |
| PG-09 | **Keyframe time belongs to its effect's scope** — clip-local time for a clip effect, sequence time for a sequence-level effect — and never silently switches. |
| PG-10 | A **curve editor** exposes interpolation, easing and handles. |
| PG-11 | Effects apply at declared levels: clip, track, adjustment clip/layer, and sequence. |
| PG-12 | **An adjustment clip is a generated/special timeline clip plus a processing graph**, not a separate mechanism. |
| PG-13 | **Generated media** — colour, gradient, counter, test pattern, title — is a first-class timeline source. |
| PG-14 | **Titles are supported at NLE level**, deliberately not attempting to be a motion-graphics application. |

---

## 9. Subtitles, audio and colour

### 9.1 Subtitles

| # | Requirement |
|---|---|
| SB-01 | **Subtitle/caption is an independent track role**, not a text overlay effect. |
| SB-02 | **Subtitle import and export** in standard formats is supported. |
| SB-03 | **`Transcript ≠ Subtitle`** (`I-486`). A transcript is derived machine text; a subtitle is authored, timed, styled display text. |
| SB-04 | **AI transcription may generate a subtitle track**, which is then editable as ordinary authored content. |
| SB-05 | Transcript editing and subtitle editing may be separate surfaces over related data. |

### 9.2 Audio

| # | Requirement |
|---|---|
| AU-01 | **Audio is core, not an accessory.** |
| AU-02 | **Audio and video share one timeline time model**, with audio editing at **sample precision** (`TM-02`). |
| AU-03 | Audio clip effects run through the same processing graph as audio nodes. |
| AU-04 | **A professional DAW is not the target.** ArcSlate provides editorial audio: levels, pan, fades, basic processing, mixing and monitoring. |
| AU-05 | Third-party audio plug-in hosting is **not a V1 requirement** and, if ever added, follows the out-of-process extension model (`EX-01`–`EX-03` in the extension requirements). |

### 9.3 Colour

| # | Requirement |
|---|---|
| CO-01 | **Colour management is first-class from the beginning**, not retrofitted. |
| CO-02 | **An asset carries its own input colour metadata**, and the user may **override interpretation**. |
| CO-03 | **An override never modifies the original media** (`PP-01`). It changes how ArcSlate interprets the source. |
| CO-04 | The **project/sequence working colour configuration** is an explicit processing policy. |
| CO-05 | **Viewer display transform and export transform are separate.** |
| CO-06 | **The colour-management backend must not leak into the domain** (`§12` of the architecture). The domain holds colour semantic configuration; the backend is infrastructure. |
| CO-07 | **Video scopes** — waveform, vectorscope, histogram, parade — are supported as **derived views**. **They are colour scopes, unrelated to the ArcScope product**; the naming must never be conflated. |
| CO-08 | Media analysis output — scene detection, loudness, motion — is **derived data**. |

---

## 10. Proxies, caches and ingest

| # | Requirement |
|---|---|
| PX-01 | **`Proxy` = an alternative low-cost editorial representation of a media asset** (`I-484`). |
| PX-02 | **Switching proxy on or off must never change render output** (`I-484`). Final render uses the original unless the user explicitly permits proxy render. |
| PX-03 | **Proxy render is an explicit, declared choice**, never a silent substitution. |
| PX-04 | **Proxy policy is configurable** per project and per asset: when to generate, at what quality, where to store, and when to evict. |
| PX-05 | **A proxy is a derived asset with no business identity** — it is not a `MediaAsset` in its own right. |
| PX-06 | **`Proxy ≠ Render Cache`** (`I-484`). A proxy is a cheaper source decode; a render cache is a stored result of timeline processing. |
| PX-07 | **`Render Cache ≠ project authority`** (`I-484`). Thumbnail and waveform caches are likewise derived. |
| PX-08 | **A cache is never the only fact of a project.** Deleting every cache must leave the project fully intact (`IX-01`). |
| PX-09 | **Import references in place by default** (`MD-03`), with managed import as an explicit choice. |
| PX-10 | **Background analysis follows import.** **Import must not wait for all caches to be generated before completing.** |
| PX-11 | **A media indexing failure is not an import failure.** The asset exists; indexing is degraded and retryable (`IP-03`). |

---

## 11. Playback and render runtime

| # | Requirement |
|---|---|
| RT-01 | **C# is the runtime orchestrator and product authority.** Domain, business rules, timeline semantics, task management and state ownership are C# (Technical Exception C in `§8.1` of the product scope). |
| RT-02 | **A native media foundation is a reasonable infrastructure choice and must never leak into the domain.** It lives behind the native/infrastructure boundary with a narrow, versioned ABI (`§13` of the architecture). |
| RT-03 | **Hardware acceleration is abstracted.** Different machines may take different hardware paths. |
| RT-04 | **The output must not change because a different hardware path was used** — beyond declared, measurable tolerance. |
| RT-05 | **On hardware acceleration failure, a software path is available**, and the fallback is visible (`PM-06` in the quality contract). |
| RT-06 | **Preview and final render share processing semantics.** Effect semantics and colour semantics must be consistent; only quality, speed and precision differ (`PP-03`). |

---

## 12. Render and export

| # | Requirement |
|---|---|
| RN-01 | **`ExportPreset`** holds reusable output settings. |
| RN-02 | **`RenderRequest`** captures what to render: sequence, range, preset, destination and options. |
| RN-03 | **A render is a Task under the unified execution model** (`§1` of the AI/agent requirements), **owned by ArcSlate** (`OW-01`). |
| RN-04 | **A render task binds a project/sequence revision snapshot.** A render must never use half an old timeline and half a new one (`EX-05`). |
| RN-05 | **This makes render genuinely repeatable**: the same request against the same revision produces the same output. |
| RN-06 | **Render range** is explicit: whole sequence, in/out range, or selected items. |
| RN-07 | A **render queue** supports several queued renders with priority and progress. |
| RN-08 | **The render queue and ArcChat tasks are not two task systems** (`I-485`). A render is an ArcSlate-owned task; ArcChat sees a `TaskHandle` and a task projection. |
| RN-09 | **Batch export produces multiple traceable render tasks** under a batch parent. |
| RN-10 | **A failed render retains completed output state** and reports partial success (`ST-06` in the AI requirements). |
| RN-11 | **Render must never overwrite existing output without prompting.** |
| RN-12 | **`Rendered Artifact ≠ ArcSlate Project`** (`I-485`). The output is an artifact with provenance; ArcChat may hold an `ArtifactRef`. |

---

## 13. Undo, save and recovery

| # | Requirement |
|---|---|
| UN-01 | **Undo/redo is a core capability** and every edit operation is undoable. |
| UN-02 | **Undo commands are semantic edits** (`UR-01`), never UI snapshots. |
| UN-03 | **A complex edit becomes a compound command** so it undoes as one user-meaningful step. |
| UN-04 | **An undo transaction is never held open indefinitely.** A preview or transient drag is not a committed command; the commit boundary is explicit (`SV-04`). |
| UN-05 | **`Undo ≠ Revision`** (`I-201`). |
| UN-06 | **Autosave exists and is a durable local save** (`SV-01`–`SV-03`). |
| UN-07 | **An explicit Save command still exists**, meaning "force a checkpoint and confirm durable state" (`SV-06`). |
| UN-08 | **Crash recovery restores to the last durable commit** with a recovery report; a damaged cache never yields "project corrupt" (`CR-04`, `CR-05` in the quality contract). |
| UN-09 | **A project checkpoint is created before any large-scale agent edit** (`CK-02`). |

---

## 14. AI and ArcChat integration

| # | Requirement |
|---|---|
| AI-01 | **Agent edits use semantic timeline capabilities, never UI coordinates** (`TL-07`). This is one of the largest benefits of the rewrite. |
| AI-02 | **An agent edit preview is a timeline diff**, reviewable before commit, for anything beyond a small reversible change. |
| AI-03 | **A simple agent edit does not require heavy approval every time**: an R1 reversible operation proceeds inside an authorised scope; higher-risk operations require approval (`§4` of the security requirements). |
| AI-04 | **AI media understanding applies data minimisation** (`AS-08`): the model receives transcripts, metadata, timecodes, detected scenes and selected frames — **not raw video** (`I-161`, `I-487`). |
| AI-05 | **Local AI may analyse local proxies and frames directly** as a free local path. |
| AI-06 | **Managed AI follows the credit, scope and budget model** (`§11` of the AI requirements), and media costs are estimated in media units (`CO-05` there). |
| AI-07 | **AI transcription is a natural ArcSlate capability**, producing searchable transcript metadata as **derived data**. |
| AI-08 | **Scene/shot detection, silence detection and highlight detection are derived analysis**, presented as suggestions. |
| AI-09 | **AI analysis results and actual edits are layered** (`I-486`): an analysis proposes; an edit is an explicit, undoable, semantic command. |

### 14.1 Capabilities exposed to ArcChat

**Context providers** (current project, sequence, selection, playhead, selected clips and range), **query capabilities** (list projects, sequences, tracks, clips, markers, media, transcripts, render state), **edit capabilities** (the semantic timeline operations, marker and subtitle operations, effect application), and **render capabilities** (start a render returning a `TaskHandle`, query render state, cancel).

**Exposing an edit capability does not grant the agent permission to use it** (`§2` of the security requirements).

---

## 15. Cross-product integration

| # | Requirement |
|---|---|
| XP-01 | **ArcNotes integration** is by reference: an ArcSlate project or rendered output may be referenced from an ArcNotes document, and an ArcNotes document may be referenced from an ArcSlate project, by `ResourceRef`. **Databases are never shared directly** (`P-10`). |
| XP-02 | **An edit decision list or report may be produced** as an artifact and, on request, materialised as an ArcNotes document — a copy/import creating a new ArcNotes-owned object (`§4.2` of the product scope). |
| XP-03 | **Large media never crosses the Hub** (Stage 13 §26). Only identity, metadata and controlled access cross boundaries. |

---

## 16. Cloud and multi-device

| # | Requirement |
|---|---|
| CL-01 | **`Project Sync ≠ original media upload`** (`I-487`). |
| CL-02 | **External originals are never uploaded by default.** A large external library must never begin uploading because sync was enabled (`AS-03`). |
| CL-03 | **Project metadata sync** is the default level: project, sequences, timeline, edit decisions, markers, text and subtitles, effect configuration and small assets (`§4.1` of the cloud requirements). |
| CL-04 | Escalation levels are explicit: `Project Only` → `Project + Managed Proxies` → `Project + Selected Originals` → `Full Managed Media`. |
| CL-05 | **Opening a project on another device works metadata-first**: the project opens, the timeline is intact, and media resolves per availability. |
| CL-06 | **Missing external media on another device is Offline Media**, a normal state with relink and download options (`MD-05`). |
| CL-07 | **A cloud proxy is not the original** (`I-484`). It supports rough editing; final render requires the original unless proxy render was explicitly permitted. |
| CL-08 | **Cloud render is not a hidden V1 capability** (`§18` of the cloud requirements). V1 renders locally. |

---

## 17. Project format

| # | Requirement |
|---|---|
| PF-01 | **ArcSlate has its own canonical native project format.** **An external tool's project format is never ArcSlate's authoritative format.** |
| PF-02 | **The native project format is versioned** (`FV-01`–`FV-09`). |
| PF-03 | **The project format contains no regenerable cache** (`EX-04` in the data requirements) — but it does contain everything required for correctness, including effect configuration, keyframes and colour configuration. |
| PF-04 | **The project is separated from large media** (`WS-02`). A project bundle is a directory-backed working store; export may produce a single archive. |
| PF-05 | **An importer for a third-party editor project format**, where one is offered, is an ordinary import adapter producing ArcSlate canonical data (`IM-01`–`IM-08` in the data requirements). Every claimed import version requires a fixture (`PG-07`). |
| PF-06 | **No bidirectional external-project compatibility is promised.** Import is one-way. |
| PF-07 | **Any unmappable imported feature generates an import report entry** (`IM-05` in the data requirements). **Silent loss is prohibited.** |
| PF-08 | **An unknown effect or missing plug-in is preserved and bypassed**, clearly marked, so the project opens and the state can be restored if the plug-in returns (`LC-06`, `LC-07` in the extension requirements). |

---

## 18. Workspace and interface

| # | Requirement |
|---|---|
| WS-01 | ArcSlate is a **compact, panel-heavy professional workspace** built on the shared dock/panel foundation (`LY-02`). |
| WS-02 | **Not every panel is visible at once.** Named layouts are provided: Editing, Effects, Colour and Audio. |
| WS-03 | **`ArcSlate layout ≠ ArcForges Workspace`** (glossary §8). The word for a panel arrangement is **Layout**. |
| WS-04 | Project browser search covers bins, assets, metadata and markers; **timeline search** covers clips, markers, text and subtitles. |
| WS-05 | The command palette and context menus are highly context-sensitive, built on the shared command system (`CM-02`, `MN-03`). |

---

## 19. Rewrite plan

**First principle: rebuild the domain and behavioural contract, then rebuild the interface.**

| Phase | Content |
|---|---|
| **0 — Product archaeology** | Study the reference product's behaviour and workflows; produce **behavioural golden scenarios**, not a class inventory |
| **1 — Domain and time constitution** | The exact time model, project/sequence/track/clip identities, semantic command set |
| **2 — Media runtime vertical slice** | Decode, display one frame, audio/video synchronisation, native boundary, AOT publish proof |
| **3 — Project and media library** | Project persistence, bins, import, offline and relink |
| **4 — Single-sequence timeline MVP** | A genuinely usable editor for one sequence |
| **5 — Professional timeline editing** | The complete operation set, linked A/V, markers, snapping |
| **6 — Persistence, autosave, recovery** | Durable commit, undo, revisions, checkpoints, crash recovery |
| **7 — Processing graph and inspector** | The typed graph plus both surfaces |
| **8 — Proxy, cache, performance** | Proxy policy, caches, playback performance to budget |
| **9 — Audio, colour, subtitle** | The three professional pillars |
| **10 — Render and export** | End-to-end professional NLE |
| **11 — ArcChat agent integration** | Semantic capabilities, context providers, artifact handling |
| **12 — Cloud and multi-device** | Project sync, media policies, multi-device open |

| # | Requirement |
|---|---|
| RW-01 | **Cloud is not an afterthought.** Placing it late in the implementation order does not delay designing its boundary; the format, identity and sync semantics are settled from phase 1. |
| RW-02 | **Behavioural golden scenarios are the acceptance instrument**, not feature-count parity. |

---

## 20. V1 scope

| Area | V1 |
|---|---|
| **Project / Media** | Project, bins, import/reference, offline and relink, media metadata, save and reopen |
| **Sequence** | Multiple sequences, resolution, frame rate, audio configuration |
| **Timeline** | Video and audio tracks, insert/overwrite, move, trim, split, delete/ripple, basic roll/slip/slide, linked A/V, markers, snapping |
| **Viewer** | Source viewer, sequence viewer, playback, frame stepping, in/out |
| **Processing** | Effect stack with the typed graph beneath, basic effects, keyframes |
| **Audio** | Levels, pan, fades, basic processing, sample-accurate editing |
| **Colour** | Input interpretation, working configuration, viewer and export transforms, scopes |
| **Subtitle** | Subtitle track, import and export, AI transcription to subtitles |
| **Proxy / Cache** | Proxy generation and policy, render/thumbnail/waveform caches |
| **Render** | Presets, requests, revision-bound tasks, queue, ranges, artifacts |
| **Reliability** | Autosave, undo, revisions, checkpoints, crash recovery |
| **ArcChat** | Context providers, query, semantic edit, render capabilities |
| **Cloud** | Project-only sync by default, escalation levels, metadata-first open |

### 20.1 Not V1 blockers — but not blocked by the domain either

Multicam, compound clips beyond nested sequences, advanced adjustment-layer workflows, advanced motion graphics, third-party audio plug-in hosting, cloud render, and collaborative editing are **not V1 requirements**.

**The domain must not preclude them**: multicam, compound clips and adjustment layers must all be expressible in the existing model — a nested sequence, a generated/special clip plus a processing graph — rather than requiring a later structural change.

---

## 21. Non-goals

ArcSlate is **not**: a motion-graphics application; a professional DAW; a dedicated colour-finishing suite; a media asset manager for an organisation; a transcoding farm; a collaborative editing platform in V1; or a Qt or C++ product wearing a C# shell.

---

## 22. Domain model

```
ArcSlateProject · MediaLibrary · Bin
MediaAsset · MediaSourceReference · ManagedMedia · ExternalMediaReference
MediaStream · MediaMetadata · MediaAvailability
Sequence · SequenceSettings · Track · TrackRole · TimelineItem
Clip · LinkGroup · Transition · Marker · RangeMarker
GeneratedMedia · Title · SubtitleCue
ProcessingGraph · ProcessingNode
EffectDefinition · EffectInstance · EffectParameter · AnimationCurve · Keyframe
TimeValue · TimeBase · SourceRange · TimelineRange
ProxyRepresentation · RenderCache · ThumbnailCache · WaveformCache
SavedLayout · EditView
ExportPreset · RenderRequest · RenderTaskReference
ProjectCheckpoint · MediaRelink · ImportOrigin · ArcSlateArtifactReference
```

---

## 23. Acceptance scenarios

**Time** — a long timeline at a non-integer frame rate accumulates no drift; audio sample positions and video frame positions convert exactly; a clip's source and timeline ranges are never confused.

**Media** — importing references in place; making an asset managed is explicit; moving a file offline leaves the project openable with structure intact; relink verifies by content and reports a mismatch; one asset with twenty clips remains one identity.

**Timeline** — every basic operation is a semantic command with correct undo; ripple delete adjusts downstream correctly; roll, slip and slide behave professionally; linked audio and video move together and can be unlinked; snapping operates on model positions.

**Viewer** — playback holds the audio clock while dropping display frames under load, and says so; frame stepping is exact; dropped preview frames never mean data loss.

**Processing** — the effect stack and node graph show one model; an invalid port connection is rejected; keyframes animate parameters with correct scope; a missing effect is preserved and bypassed with the project still opening.

**Colour** — an input interpretation override changes nothing about the source file; viewer and export transforms are separate; scopes derive from the processing result.

**Proxy** — enabling proxies changes the edit experience and **not** the render output; permitting proxy render is an explicit choice; deleting every cache leaves the project intact.

**Render** — a render binds a revision snapshot and is repeatable; a queued batch produces traceable tasks; a failed render retains completed output; an existing output is never overwritten silently; the artifact carries provenance.

**Reliability** — killing the process mid-edit recovers to the last durable commit; a corrupted render cache never produces "project corrupt"; an agent bulk edit is preceded by a checkpoint.

**AI** — an agent edit uses semantic commands, previews as a timeline diff, and is undoable; raw video is never sent to a model; transcription produces derived data and an editable subtitle track.

**Cloud** — enabling project sync uploads no originals; opening on a second device shows the timeline before media resolves; missing external media is Offline Media with recovery options; a cloud proxy never silently becomes the render source.

**Import** — an external project import produces ArcSlate canonical data with a report of everything unmapped; nothing is silently lost.

---

## 24. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 20` | The complete ArcSlate specification: reference posture, product definition and principles, domain structure, time model, media, timeline, viewer, processing graph, subtitles, audio, colour, proxy and cache, runtime, render, undo and recovery, AI integration, cloud boundary, project format, workspace, the twelve-phase rewrite plan, V1 scope, non-goals and domain model |
| `I2 §II` | The reference reuse posture. **The migration-matrix obligation it describes is discharged by the completed Reference Coverage Matrix** (`RF-05`); no separate upstream migration matrix is required (`P2-005`) |
| `I4 §Stage 13 §6`, `§24–26` | ArcSlate is not a technical exception; its owned state; large media never crossing the Hub |
| `I4 §Stage 22 §34–39`, `§197` | ArcSlate storage strategy, working store versus portable package, local structure |
| `I3 §14`, `§15` | Large-data path, media frames and GPU staying in-process, native ABI discipline |
| **D-002** | ArcSlate inherits product direction from ArcVideo, not its model |
| **D-008** | Native AOT desktop deliverable with trim/AOT-safe dependencies |
| **D-012** (as amended 2026-09-05), **D-013**, **P2-005** | ArcVideo and ArcVideoFoundation as ArcSlate's licence-gated references; upstream provenance retained |
