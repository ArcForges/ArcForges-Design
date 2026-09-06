# Reference Coverage Matrix — ArcSlate / ArcVideo + ArcVideoFoundation

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete**
> Governing authority: **D-012** as amended 2026-09-05, **P2-005** (ArcSlate's direct references are ArcVideo and ArcVideoFoundation), **D-013**, **D-002**
> Consuming product: **ArcSlate** — [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md)

---

## 1. Source identity

| Field | ArcVideo | ArcVideoFoundation |
|---|---|---|
| Repository | `github.com/ArcForges/ArcVideo` | `github.com/ArcForges/ArcVideoFoundation` |
| Local path | `C:\MyFile\ArcForges\ArcVideo` | `C:\MyFile\ArcForges\ArcVideoFoundation` |
| Commit | `caf5651` | `139eeca` |
| Commit date | 2026-03-16 | 2026-03-30 |
| Reviewed on | 2026-09-05 | 2026-09-05 |
| Reviewer | Architecture Owner (design stage) | Architecture Owner (design stage) |

> **Reference baseline (`P2-005`, 2026-09-05).** These two repositories are ArcSlate's direct references. **D-012**'s reference map was amended on the same date to remove Olive as a separate required reference: Olive could not be built in the user's environment, and ArcVideo carries the modifications made to get that codebase building. There is no obligation to obtain or independently review an Olive repository, and none is sought.

> **Naming note.** `ArcVideo` and `ArcVideoFoundation` appear here **only** as reference-repository names registered by **D-012**. They are not products: the product baseline is exactly ArcChat, ArcNotes, ArcScope and ArcSlate (**D-002**).

---

## 2. Licence and provenance position

| Repository | Evidence | Finding |
|---|---|---|
| ArcVideo | `LICENSE` — GNU General Public License Version 3 | **GPL-3.0** |
| ArcVideoFoundation | `LICENSE` — GNU General Public License Version 3; `README.md` badge "License: GPL v3" | **GPL-3.0** |
| Subtree exceptions | No differing licence file found under `app/`, `src/`, `include/` or `tests/` | None found in the reviewed scope |
| Upstream provenance | `README.md` line 12: *"A fork of Olive Video Editor"*; line 20 and line 98 confirm the fork relationship and thank the Olive team | **ArcVideo is a downstream fork of Olive** |

| # | Finding |
|---|---|
| LP-01 | **Both are GPL-3.0-only.** Under **D-013**, GPL-only material **must not be copied, translated or ported**. It may be used only as controlled behavioural reference. Every row below is therefore `Reference Only` or an accepted exclusion. |
| LP-02 | **The copyright is not solely ArcForges'.** ArcVideo is a fork of an upstream project; its GPL obligations and upstream attribution run to the Olive authors as well. Reuse would require clearing both chains, which **D-013** already forbids for GPL-only material. |
| LP-03 | **The ArcForges organisation owning a reference repository does not create a licence exemption.** GPL-3.0 is GPL-3.0 regardless of who holds the remote. |
| LP-04 | **GPL-3.0 → AGPL-3.0-only is not a permitted reuse direction here.** Even where the two licences can coexist in a combined work, **D-013**'s instruction is explicit and is followed literally: no copy, no translation, no port. |

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| ArcVideo licence and provenance | `LICENSE`, `README.md`, `SECURITY.md` |
| Timeline model | `app/timeline/**` (12 files) |
| Node graph and compositing | `app/node/**` — `block`, `effect`, `filter`, `color`, `distort`, `keying`, `generator`, `math`, `time`, `input`, `output`, `group`, `gizmo`, `project`, `keyframe`, `param`, `traverser`, `value`, `valuedatabase` |
| Codec and media I/O | `app/codec/**` — `decoder`, `encoder`, `exportcodec`, `exportformat`, `conformmanager`, `frame`, `ffmpeg/` |
| Render pipeline and caches | `app/render/**` — colour processor, colour transform, disk manager, audio playback cache, audio waveform cache, cancel atom, alpha association |
| Audio | `app/audio/**` |
| Task model | `app/task/**` — `conform`, `customcache`, `export`, `precache`, `project`, `render` |
| Undo | `app/undo/**`, `app/timeline/timelineundo*.{h,cpp}`, `app/node/nodeundo.*` |
| Panels | `app/panel/**` (21 panels) |
| Packaging and crash handling | `app/packaging/{windows,macos,linux}`, `app/crashhandler/**` |
| Tests | `tests/{timeline,compositing,general}` |
| CI images | `docker/{ci-arcvideo,ci-common,ci-crashpad,ci-ffmpeg,ci-ocio}` |
| ArcVideoFoundation surface | complete: `include/arcvideo/foundation/**` (17 headers), `src/**` (10 sources), `docs/BUILD_GUIDE.md`, `README.md` |
| Packaged release shape | `StartArcForges/{ArcVideo,ArcVideoFoundation}` — directory listing only, **not executed** |

**Not read, and why:** `app/ts/**` and `app/shaders/**` beyond directory identification — shader and script expression is exactly what GPL-only status makes ineligible for reuse, and their existence suffices for the disposition. `docker/**` image contents — build infrastructure, not product evidence.

### 3.1 Upstream provenance — retained, not audited separately

**`P2-005` removed Olive as a separate required reference. It did not remove Olive's provenance.** The two are different obligations and both positions are held simultaneously.

| Aspect | Position |
|---|---|
| **Reference scope** | ArcVideo and ArcVideoFoundation are the reference baselines. **No Olive checkout is sought, obtained or audited.** No obligation exists to review Olive's independent tests, fixtures, source or licence file |
| **Provenance obligation — retained** | ArcVideo documents itself as a fork of Olive (`README.md` lines 12, 20 and 98). Its **GPL-3.0 obligations, upstream copyright and attribution run to the Olive authors** as well as to ArcForges (`LP-02`) |
| **Where the provenance lives** | In the reference repositories' own licence files, notices and headers, which are read but never modified. Should any inherited material ever be used — which `LP-01` prohibits — the ten-field record of **D-013** would carry both chains |
| **What the *(upstream-derived)* label means** | A row so marked describes a capability ArcVideo inherited from its upstream rather than added. It is an **attribution note**, not a claim about an Olive repository. The evidence is ArcVideo's own tree at `caf5651` |
| **What is deliberately not claimed** | Coverage of Olive capabilities that ArcVideo removed, or of divergence after the fork point. That scope is **out of scope by decision**, not unresolved |

---

## 4. Item-level matrix

| # | Capability / behaviour | Reference | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|---|
| AL-01 | Timeline coordinate model | ArcVideo *(upstream-derived)* | `app/timeline/{timelinecoordinate,timelinecommon}.*` | `products/arcslate.md` §4 time model; `WP-36.01` | Reference Only | Evidence that a timeline needs an explicit coordinate abstraction rather than raw offsets | GPL-3.0-only — no reuse permitted | First-party test: no drift over long durations in any supported rate | Product Owner | Evidence established |
| AL-02 | Rational arithmetic, timecode functions, time range | ArcVideoFoundation *(upstream-derived)* | `include/arcvideo/foundation/util/{rational,timecodefunctions,timerange}.h` + `src/util/{rational,timecodefunctions,timerange}.cpp` | `products/arcslate.md` `TM-02`, `TM-03` (exact rational rates); `WP-36.01` | Evidence that rational time is the right canonical form. **Read 2026-09-07**: `src/util/timecodefunctions.cpp` converts through `double` and derives frame arithmetic from `std::llround(frame_rate)`; `util/rational.h` exposes `fromDouble`/`toDouble`. ArcForges **rejects that for positions** — canonical positions are integer ticks (`TB-01`) — while **accepting rounded-rate arithmetic for drop-frame timecode display only**, where it is correct by definition (`§3.5` of the time model) | **Directly supports `I-478`**: the reference implements rational time as a first-class type with dedicated timecode conversion — confirming exact arithmetic is required, not optional | GPL-3.0-only — no reuse permitted | First-party test: frame–sample conversion round-trips exactly | Architecture Owner | Evidence established |
| AL-03 | Timeline undo — general, pointer, ripple | ArcVideo *(upstream-derived)* | `app/timeline/{timelineundogeneral,timelineundopointer,timelineundoripple,timelineundocommon}.*` | `products/arcslate.md` §undo; `WP-36.05`, `WP-36.06` | Reference Only | Evidence that professional edit operations need per-operation undo semantics, not a generic snapshot | GPL-3.0-only — no reuse permitted | First-party test: undo across composite operations | Product Owner | Evidence established |
| AL-04 | Timeline markers | ArcVideo *(upstream-derived)* | `app/timeline/timelinemarker.*` | `products/arcslate.md` §markers; `WP-36.04` | Reference Only | Evidence on marker model | GPL-3.0-only — no reuse permitted | First-party marker tests | Product Owner | Evidence established |
| AL-05 | Block model — clip, gap, transition, subtitle | ArcVideo *(upstream-derived)* | `app/node/block/{block.*,clip,gap,subtitle,transition}` | `products/arcslate.md` §6 timeline, §8 subtitles; `WP-36.04`, `WP-38.05` | Reference Only | **Confirms subtitle is a distinct block/track role**, matching the accepted ArcSlate model | GPL-3.0-only — no reuse permitted | First-party test: subtitle round-trip with exact timing | Product Owner | Evidence established |
| AL-06 | Node graph — factory, traverser, param, value, value database | ArcVideo *(upstream-derived)* | `app/node/{factory,traverser,param,value,valuedatabase,node}.*` | `products/arcslate.md` §8 processing graph; `WP-37.03` | Reference Only | Evidence that a node graph with a traverser and a value database is the workable shape for a compositing pipeline | GPL-3.0-only — no reuse permitted | First-party test: graph evaluation correct per node kind | Architecture Owner | Evidence established |
| AL-07 | Keyframes and split values | ArcVideo *(upstream-derived)* | `app/node/{keyframe.*,splitvalue.h}` | `products/arcslate.md` `PG-08`, `PG-09` (`Keyframe ≠ current value`; scope-bound keyframe time); `WP-37.03` | Reference Only | **Directly supports `I-483`**: the reference separates keyframes from current parameter values | GPL-3.0-only — no reuse permitted | First-party test: keyframe scope never silently switches | Product Owner | Evidence established |
| AL-08 | Node categories — effect, filter, color, distort, keying, generator, math, time, audio | ArcVideo *(upstream-derived)* | `app/node/{effect,filter,color,distort,keying,generator,math,time,audio}/` | `products/arcslate.md` §8 node kinds; `WP-37.03` | Reference Only | Establishes the expected processing-node vocabulary; ArcSlate's V1 set is a deliberate subset | GPL-3.0-only — no reuse permitted | First-party per-node-kind evaluation tests | Product Owner | Evidence established |
| AL-09 | Gizmo (on-viewer manipulation) | ArcVideo *(upstream-derived)* | `app/node/gizmo/` | `products/arcslate.md` §7 viewer | Reference Only | Evidence on direct manipulation in the viewer | GPL-3.0-only — no reuse permitted | First-party viewer interaction tests | Product Owner | Evidence established |
| AL-10 | Decoder, encoder, export codec and format | ArcVideo *(upstream-derived)* | `app/codec/{decoder,encoder,exportcodec,exportformat}.*`, `app/codec/ffmpeg/` | `products/arcslate.md` §11 runtime, §12 export; `12-native-interop-and-media.md` §7; `WP-37.01`, `WP-38.04` | Reference Only | **Confirms a native media foundation is required** and that codec/format selection is a first-class export concern | GPL-3.0-only — no reuse permitted | First-party test: no native type escapes the media layer; encode conformance against golden fixtures | Architecture Owner | Evidence established |
| AL-11 | Conform manager | ArcVideo *(upstream-derived)* | `app/codec/conformmanager.*`, `app/task/conform/` | `products/arcslate.md` §10 proxies and caches; `WP-37.05` | Reference Only | Evidence that media conforming is a background task distinct from import | GPL-3.0-only — no reuse permitted | First-party test: import completes without waiting on caches | Product Owner | Evidence established |
| AL-12 | Colour processor, colour transform, colour processor cache | ArcVideo *(upstream-derived)* | `app/render/{colorprocessor,colortransform,colorprocessorcache}.*`; `README.md` tech stack names OpenColorIO | `products/arcslate.md` §9 colour; `WP-38.00` | Reference Only | **Supports `CO-05` and the ArcSlate rule that the colour backend must not become domain**: the reference isolates colour transforms behind a processor abstraction | GPL-3.0-only — no reuse permitted | First-party test: viewer display transform never alters export output | Product Owner | Evidence established |
| AL-13 | Alpha association | ArcVideo *(upstream-derived)* | `app/render/alphaassoc.h` | `products/arcslate.md` §9 colour semantics; `WP-38.00` | Reference Only | Evidence that premultiplied/straight alpha must be modelled explicitly, a common correctness defect | GPL-3.0-only — no reuse permitted | First-party colour round-trip tests | Product Owner | Evidence established |
| AL-14 | Audio playback cache, waveform cache, disk manager | ArcVideo *(upstream-derived)* | `app/render/{audioplaybackcache,audiowaveformcache,diskmanager}.*` | `products/arcslate.md` `PX-07` (caches are derived); `WP-37.05` | Reference Only | **Supports `I-484`**: the reference maintains distinct cache kinds with a disk manager, confirming caches are derived infrastructure rather than project data | GPL-3.0-only — no reuse permitted | First-party test: deleting every cache leaves the project intact | Architecture Owner | Evidence established |
| AL-15 | Cancel atom | ArcVideo *(upstream-derived)* | `app/render/cancelatom.h` | `05-ai-and-agent-execution.md` §cancellation; `WP-16.02` | Reference Only | Evidence that long render work needs a first-class cancellation primitive threaded through the pipeline | GPL-3.0-only — no reuse permitted | First-party test: cancellation leaves no complete-looking partial file | Architecture Owner | Evidence established |
| AL-16 | Audio manager, processor, visual waveform | ArcVideo *(upstream-derived)* | `app/audio/{audiomanager,audioprocessor,audiovisualwaveform}.*` | `products/arcslate.md` §8 audio; `WP-37.04` | Reference Only | Evidence on sample-precise audio handling separate from video | GPL-3.0-only — no reuse permitted | First-party test: audio sample-precise and synchronised under load | Product Owner | Evidence established |
| AL-17 | Sample buffer and audio params | ArcVideoFoundation *(upstream-derived)* | `include/arcvideo/foundation/render/{samplebuffer,audioparams,sampleformat}.h` + `src/render/{samplebuffer,audioparams}.cpp` | `products/arcslate.md` §8 audio; `WP-37.04` | Reference Only | Evidence on the audio buffer and format abstraction | GPL-3.0-only — no reuse permitted | First-party mixing reference comparison | Product Owner | Evidence established |
| AL-18 | Pixel format abstraction | ArcVideoFoundation *(upstream-derived)* | `include/arcvideo/foundation/render/pixelformat.h` | `12-native-interop-and-media.md` §4 buffers; `WP-37.01` | Reference Only | Evidence on the pixel-format abstraction a media pipeline needs | GPL-3.0-only — no reuse permitted | First-party buffer accounting tests | Architecture Owner | Evidence established |
| AL-19 | Bezier and colour utilities | ArcVideoFoundation *(upstream-derived)* | `include/.../util/{bezier,color}.h` + sources | `products/arcslate.md` §8 animation curves; `WP-37.03` | Reference Only | Evidence on curve interpolation for keyframe animation | GPL-3.0-only — no reuse permitted | First-party animation curve tests | Product Owner | Evidence established |
| AL-20 | CPU optimisation and SIMD portability shim | ArcVideoFoundation | `include/.../util/{cpuoptimize.h,sse2neon.h}` | `12-native-interop-and-media.md` §2 permitted native surface | Reference Only | **Provenance note**: `sse2neon.h` is a vendored third-party header with its own upstream licence, distinct from the repository's GPL-3.0. Recorded because it is exactly the case **D-013** warns about | GPL-3.0 repository; **vendored header carries its own licence** — not cleared, not needed | — | Licensing and Provenance Owner | Evidence established |
| AL-21 | Task model — render, export, precache, custom cache, project | ArcVideo *(upstream-derived)* | `app/task/{render,export,precache,customcache,project}/`, `app/task/{task.h,taskmanager.*}` | `05-ai-and-agent-execution.md` §unified Task; `products/arcslate.md` `RN-03`; `WP-38.03` | Reference Only | **Confirms render and export are long-running tasks with a manager** — matching ArcForges' decision to route them through the unified execution engine rather than a bespoke queue | GPL-3.0-only — no reuse permitted | First-party test: render is a Task with progress, pause and cancellation | Architecture Owner | Evidence established |
| AL-22 | Panels — timeline, node, curve, viewer, sequence viewer, footage viewer, scope, param, table, history, audio monitor, pixel sampler, multicam, task manager, tool, project | ArcVideo *(upstream-derived)* | `app/panel/**` (21 panels) | `products/arcslate.md` §7 viewer, §9 scopes; `09-shared-desktop-experience.md` §panels; `WP-10.01`, `WP-38.01` | Reference Only | Establishes the expected professional panel vocabulary and confirms scopes are a separate panel concern | GPL-3.0-only — no reuse permitted | First-party layout restore and scope reference-signal tests | Product Owner | Evidence established |
| AL-23 | Multicam | ArcVideo *(upstream-derived)* | `app/panel/multicam/` | **Accepted exclusion** — not in accepted ArcSlate V1 scope | Drop | Multicam editing is additional product scope; recorded as a deliberate choice | GPL-3.0-only — no reuse | — | Product Owner | Accepted exclusion |
| AL-24 | Node-based compositing as the user-facing editing paradigm | ArcVideo *(upstream-derived)* | `app/panel/node/`, `app/node/**`; `README.md` "Node-based compositing system" | **Accepted exclusion as a user-facing paradigm**; retained as internal processing-graph evidence (`AL-06`) | Drop (as UI paradigm); Reference Only (as internal model) | ArcSlate's accepted model is a timeline with a processing graph beneath it, not a node-graph editor as the primary surface. **This is the single largest deliberate divergence from the reference** | GPL-3.0-only — no reuse | First-party test: graph evaluation correct without a node-editor surface | Product Owner | Accepted exclusion |
| AL-25 | OpenTimelineIO interchange | ArcVideo *(upstream-derived)* | `README.md` core features; `native/arcslate-otio-abi` in the implementation repository names the same interchange | `products/arcslate.md` §15 interchange; `WP-39.05` | Reference Only | **Migration evidence**: names the interchange format expected in this category, and the existing implementation repository already anticipates it | GPL-3.0-only — no reuse permitted | Format fixture per claimed interchange version (`PG-07`) | Product Owner | Evidence established |
| AL-26 | Crash handler | ArcVideo | `app/crashhandler/**`; packaged output ships `crashpad_handler.exe` and `arcvideo-crashhandler.exe` | `12-native-interop-and-media.md` `SB-06`; `WP-12.05` | Reference Only | **Confirms `SB-06`**: a native media application ships a separate crash handler process. ArcForges requires the same dump retention plus user approval before upload | GPL-3.0-only — no reuse permitted | First-party test: no report sent without approval | Security and Privacy Owner | Evidence established |
| AL-27 | Packaging per platform | ArcVideo | `app/packaging/{windows,macos,linux}` | `14-build-packaging-and-release.md` §5 | Reference Only | Evidence on per-platform packaging structure for a native media product | GPL-3.0-only — no reuse permitted | Update matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |
| AL-28 | Test approach — timeline, compositing, general | ArcVideo | `tests/{timeline/timeline-tests.cpp,compositing/compositing-tests.cpp,general/common-tests.cpp}`, `tests/testutil.h` | `../testing-and-verification-strategy.md` F-01, F-15, F-18 | Reference Only | **Test evidence**: confirms timeline and compositing are the two areas needing dedicated suites. **Also a scale finding** — three test files for a 787-file application, which is why ArcSlate's own suites cannot be modelled on the reference's coverage | GPL-3.0-only — no reuse permitted | `WP-36`–`WP-38` suite coverage | Quality Owner | Evidence established |
| AL-29 | CI images — FFmpeg, OCIO, crashpad | ArcVideo | `docker/{ci-ffmpeg,ci-ocio,ci-crashpad,ci-common,ci-arcvideo}` | `14-build-packaging-and-release.md` §10; `WP-02.05` | Reference Only | Evidence that native media dependencies need pinned, prebuilt CI images — a dependency-policy consideration for ArcSlate | GPL-3.0-only — no reuse permitted | Dependency policy check (`WP-02.05`) | Release Engineering Owner | Evidence established |
| AL-30 | ArcVideoFoundation's actual extraction state | ArcVideoFoundation | Complete tree: **10 source files and 17 headers**, covering only rational, timecode, timerange, bezier, colour, math, string, value, log, cpuoptimize, sse2neon, samplebuffer, audioparams, sampleformat, pixelformat, tests, foundation.h | Informs `WP-36`, `WP-37` planning assumptions | Reference Only | **Evidence-versus-claim finding**: `README.md` describes a *"fat core"* and *"foundational core library powering ArcVideo"*, but the present tree is a thin utility layer with **no** timeline, media, render-graph or project model. The README overstates the extraction | GPL-3.0-only — no reuse permitted | — | Architecture Owner | Evidence established |
| AL-31 | Packaged release shape | ArcVideo, ArcVideoFoundation | `StartArcForges/ArcVideo` — 47 entries: `arcvideo-editor.exe`, `crashpad_handler.exe`, OpenColorIO/OpenEXR/OpenImageIO/Imath DLLs, **no installer**. `StartArcForges/ArcVideoFoundation` — `include/` and `lib/` only | `10-distribution-update-and-support.md` §1.1; `14-build-packaging-and-release.md` §5 | Reference Only | **Packaging evidence**: a loose native deployment with heavy third-party DLLs and no installer; and the Foundation ships as a library, not a product. Contrast evidence for ArcForges' signed self-contained installer requirement | GPL-3.0 binaries; **not executed** | Update matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 31 rows across all 14 areas |
| Every row carries all nine required fields | **Pass** |
| Every row has exactly one completeness state | **Pass** — 31 rows: 29 evidence established, 2 accepted exclusions (`AL-23`, `AL-24`), **0 unresolved** |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** |
| Licence position determined below the repository root | **Pass** — and `AL-20` records a vendored third-party header with its own licence |
| Any row proposing reuse carries a provenance obligation | **Not applicable** — no row proposes reuse |
| ArcVideoFoundation coverage | **Complete** — the whole 27-file tree was enumerated |
| Reference scope matches the amended **D-012** map | **Pass** — ArcVideo and ArcVideoFoundation, per `P2-005`. Upstream provenance retained (`§3.1`) |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

| # | Finding | Effect |
|---|---|---|
| F-AL-1 | **ArcVideo and ArcVideoFoundation are GPL-3.0-only**, and ArcVideo is a fork carrying upstream copyright. | Neither is reusable. **ArcSlate is an original implementation**, and `RF-01` in `products/arcslate.md` — the reference is a product and behaviour reference, not an architecture authority — is confirmed as the only tenable position. No design change. |
| F-AL-2 | **ArcVideoFoundation is a thin utility layer, not a "fat core"** (`AL-30`). | Any planning assumption that a substantial reusable core exists is unsupported. `WP-36` and `WP-37` correctly plan original implementations; this row is the evidence that they must. **Effect: recorded in `WP-36` inputs so the assumption is not reintroduced.** |
| F-AL-3 | **Neither accessible reference implements the ArcSlate colour-management separation** of viewer display transform versus export transform as a *product* rule — the reference has the transforms but not the invariant. | `WP-38.00`'s separation requirement is an ArcForges-originated rule with reference support for the mechanism only. Recorded so its oracle is first-party. |
| F-AL-4 | **The reference's node-graph editor is its primary editing paradigm** (`AL-24`). | ArcSlate's timeline-first model is a deliberate divergence, not an unimplemented feature. Recorded so it is not later "restored" as a gap. |
| F-AL-5 | **The reference has three test files for a 787-file application** (`AL-28`). | The reference supplies **no usable test-coverage model** for ArcSlate. ArcSlate's suites are first-party by necessity. Recorded so reference test coverage is never cited as adequacy evidence. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | Bound to ArcVideo `caf5651` and ArcVideoFoundation `139eeca`. `WP-36` re-checks both for drift and newly introduced material; it does not re-create this matrix. |
| MT-02 | **`AL-30` is re-checked on drift**: if ArcVideoFoundation grows into the core its README describes, the planning assumption changes. |
| MT-03 | **The reference scope is ArcVideo and ArcVideoFoundation** (`P2-005`). No Olive checkout is sought at any stage. Upstream attribution and licence notices are preserved wherever inherited material requires them (`§3.1`). |
| MT-04 | Packaged binaries are never executed, at any stage. |
