# ArcSlate — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Project and timeline, playback and processing, render and colour, integration and portability.

Tasks: 41 · Owning repositories: ArcSlate · Integration owner(s): ArcSlate integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [SLATE.01](#task-slate-01) | Exact time model: canonical ticks, rational rates, frame/sample time, half-open ranges | feature | M | none | not-started |
| [SLATE.02](#task-slate-02) | Project and sequence domain model | feature | M | [SLATE.01](#task-slate-01) (artifact) | not-started |
| [SLATE.03](#task-slate-03) | Media asset/stream/metadata domain model and content-based relink algorithm | feature | M | [SLATE.01](#task-slate-01) (artifact) | not-started |
| [SLATE.04](#task-slate-04) | Native media metadata/probe read adapter (real import path) | feature | L | [NAT.07](native.md#task-nat-07) (artifact), [SLATE.03](#task-slate-03) (artifact) | not-started |
| [SLATE.05](#task-slate-05) | Media library: bins, reference-in-place import, background analysis | feature | M | [SLATE.02](#task-slate-02) (artifact), [SLATE.03](#task-slate-03) (artifact) | not-started |
| [SLATE.06](#task-slate-06) | Timeline structural model: tracks, items, clips, transitions, markers | feature | L | [SLATE.02](#task-slate-02) (artifact), [SLATE.03](#task-slate-03) (artifact), [SLATE.01](#task-slate-01) (artifact) | not-started |
| [SLATE.07](#task-slate-07) | Edit command pipeline and placement operations | feature | XL | [SLATE.06](#task-slate-06) (artifact) | not-started |
| [SLATE.08](#task-slate-08) | Relationship and retiming edit operations | feature | L | [SLATE.07](#task-slate-07) (artifact) | not-started |
| [SLATE.09](#task-slate-09) | Undo/redo stack and composite command grouping | feature | M | [SLATE.07](#task-slate-07) (artifact) | not-started |
| [SLATE.10](#task-slate-10) | Project persistence and store infrastructure (V1 migration baseline) | feature | M | [PLT.01](platform.md#task-plt-01) (artifact), [PLT.04](platform.md#task-plt-04) (artifact), [SLATE.02](#task-slate-02) (artifact), [SLATE.06](#task-slate-06) (artifact) | not-started |
| [SLATE.11](#task-slate-11) | Project checkpoints, crash recovery and project-version migration | feature | L | [PLT.02](platform.md#task-plt-02) (artifact), [PLT.03](platform.md#task-plt-03) (artifact), [SLATE.09](#task-slate-09) (artifact), [SLATE.10](#task-slate-10) (artifact) | not-started |
| [SLATE.12](#task-slate-12) | Slate.project.v1/graph.v1 wire projection: bins, generators, nesting, adjustment, title/subtitle, cycle rejection | feature | L | [SLATE.06](#task-slate-06) (artifact), [SLATE.08](#task-slate-08) (artifact), [CON.06](contracts.md#task-con-06) (contract) | not-started |
| [SLATE.13](#task-slate-13) | ArcSlate reference-coverage drift check (maintenance) | acceptance | S | none | not-started |
| [SLATE.14](#task-slate-14) | Closure: owned-artifact and real-integration receipt | acceptance | S | [SLATE.01](#task-slate-01) (artifact), [SLATE.11](#task-slate-11) (artifact), [SLATE.12](#task-slate-12) (artifact), [SLATE.13](#task-slate-13) (artifact), [SLATE.04](#task-slate-04) (artifact), [SLATE.05](#task-slate-05) (artifact) | not-started |
| [SLATE.15](#task-slate-15) | Native media boundary consumption (ArcSlate.Media wrapper and safety suite) | feature | L | [NAT.06](native.md#task-nat-06) (artifact), [NAT.07](native.md#task-nat-07) (artifact), [NAT.08](native.md#task-nat-08) (artifact), [SLATE.04](#task-slate-04) (artifact) | not-started |
| [SLATE.16](#task-slate-16) | Decode and pooled buffers | feature | L | [SLATE.15](#task-slate-15) (artifact) | not-started |
| [SLATE.17](#task-slate-17) | Playback engine, clock and scheduler | feature | L | [SLATE.16](#task-slate-16) (artifact), [SLATE.01](#task-slate-01) (artifact) | not-started |
| [SLATE.18](#task-slate-18) | Processing graph and keyframe engine (pure evaluation) | feature | L | [SLATE.06](#task-slate-06) (artifact) | not-started |
| [SLATE.19](#task-slate-19) | Native-backed processing nodes (convert, scale, transform, colour-adjustment execution) | feature | M | [SLATE.18](#task-slate-18) (artifact), [SLATE.15](#task-slate-15) (artifact), [NAT.08](native.md#task-nat-08) (artifact), [NAT.15](native.md#task-nat-15) (artifact) | not-started |
| [SLATE.20](#task-slate-20) | Audio processing chain and sample-accurate mixing | feature | XL | [SLATE.01](#task-slate-01) (artifact), [SLATE.18](#task-slate-18) (artifact), [SLATE.16](#task-slate-16) (artifact), [NAT.08](native.md#task-nat-08) (artifact) | not-started |
| [SLATE.21](#task-slate-21) | Proxies and derived caches | feature | L | [SLATE.03](#task-slate-03) (artifact), [SLATE.16](#task-slate-16) (artifact), [NAT.08](native.md#task-nat-08) (artifact), [NAT.11](native.md#task-nat-11) (artifact), [PLT.07](platform.md#task-plt-07) (artifact) | not-started |
| [SLATE.22](#task-slate-22) | Viewer: source and sequence, professional transport | feature | M | [SLATE.17](#task-slate-17) (artifact), [NAT.15](native.md#task-nat-15) (artifact), [PLT.27](platform.md#task-plt-27) (artifact), [PLT.28](platform.md#task-plt-28) (artifact) | not-started |
| [SLATE.23](#task-slate-23) | Closure: owned-artifact and real-integration receipt | acceptance | S | [SLATE.15](#task-slate-15) (artifact), [SLATE.22](#task-slate-22) (artifact), [SLATE.18](#task-slate-18) (artifact), [SLATE.19](#task-slate-19) (artifact), [SLATE.20](#task-slate-20) (artifact), [SLATE.21](#task-slate-21) (artifact) | not-started |
| [SLATE.24](#task-slate-24) | Colour management: input interpretation, working config, display/export transform separation | feature | L | [SLATE.18](#task-slate-18) (artifact), [SLATE.03](#task-slate-03) (artifact), [NAT.10](native.md#task-nat-10) (artifact) | not-started |
| [SLATE.25](#task-slate-25) | Video scopes (waveform, vectorscope, histogram, parade) | feature | M | [SLATE.19](#task-slate-19) (artifact), [NAT.15](native.md#task-nat-15) (artifact), [PLT.27](platform.md#task-plt-27) (artifact) | not-started |
| [SLATE.26](#task-slate-26) | Render planning and immutable snapshot binding | feature | M | [SLATE.06](#task-slate-06) (artifact), [SLATE.09](#task-slate-09) (artifact), [SLATE.10](#task-slate-10) (artifact) | not-started |
| [SLATE.27](#task-slate-27) | Export presets and encoding validation | feature | M | [SLATE.24](#task-slate-24) (artifact), [NAT.08](native.md#task-nat-08) (artifact) | not-started |
| [SLATE.28](#task-slate-28) | Render execution engine and atomic export (native Product Job) | feature | XL | [SLATE.26](#task-slate-26) (artifact), [SLATE.27](#task-slate-27) (artifact), [SLATE.19](#task-slate-19) (artifact), [SLATE.20](#task-slate-20) (artifact), [NAT.08](native.md#task-nat-08) (artifact), [EXE.01](execution.md#task-exe-01) (artifact) | not-started |
| [SLATE.29](#task-slate-29) | Subtitles and captions: authored tracks, SRT/WebVTT import/export | feature | M | [SLATE.06](#task-slate-06) (artifact), [SLATE.01](#task-slate-01) (artifact) | not-started |
| [SLATE.30](#task-slate-30) | Local transcription extraction ProductJob and TranscriptRecord adoption | feature | L | [SLATE.29](#task-slate-29) (artifact), [SLATE.16](#task-slate-16) (artifact), [EXE.01](execution.md#task-exe-01) (artifact) | not-started |
| [SLATE.31](#task-slate-31) | Golden output stability corpus | feature | M | [SLATE.28](#task-slate-28) (artifact), [SLATE.27](#task-slate-27) (artifact) | not-started |
| [SLATE.32](#task-slate-32) | Closure: owned-artifact and real-integration receipt | acceptance | S | [SLATE.24](#task-slate-24) (artifact), [SLATE.31](#task-slate-31) (artifact), [HAR.91](harness.md#task-har-91) (artifact), [SLATE.25](#task-slate-25) (artifact), [SLATE.29](#task-slate-29) (artifact), [SLATE.30](#task-slate-30) (artifact) | not-started |
| [SLATE.33](#task-slate-33) | Capability surface: query, edit, render and export capabilities | feature | L | [SLATE.07](#task-slate-07) (artifact), [SLATE.08](#task-slate-08) (artifact), [SLATE.28](#task-slate-28) (artifact) | not-started |
| [SLATE.34](#task-slate-34) | Bounded context provision | feature | M | [SLATE.06](#task-slate-06) (artifact) | not-started |
| [SLATE.35](#task-slate-35) | Collect, consolidate and the portable project package | feature | L | [SLATE.04](#task-slate-04) (artifact), [SLATE.05](#task-slate-05) (artifact), [PLT.06](platform.md#task-plt-06) (artifact) | not-started |
| [SLATE.36](#task-slate-36) | Cross-device resolution and relink | feature | M | [SLATE.03](#task-slate-03) (artifact), [SLATE.04](#task-slate-04) (artifact), [SLATE.05](#task-slate-05) (artifact) | not-started |
| [SLATE.37](#task-slate-37) | Cloud sync scope declaration | feature | M | [SLATE.10](#task-slate-10) (artifact), [CON.09](contracts.md#task-con-09) (contract) | not-started |
| [SLATE.38](#task-slate-38) | OTIO interchange: import | feature | L | [SLATE.06](#task-slate-06) (artifact), [SLATE.01](#task-slate-01) (artifact), [NAT.06](native.md#task-nat-06) (artifact), [NAT.12](native.md#task-nat-12) (artifact) | not-started |
| [SLATE.39](#task-slate-39) | OTIO interchange: export | feature | M | [SLATE.38](#task-slate-38) (artifact), [SLATE.26](#task-slate-26) (artifact), [NAT.12](native.md#task-nat-12) (artifact) | not-started |
| [SLATE.40](#task-slate-40) | Closure: owned-artifact and real-integration receipt | acceptance | S | [SLATE.33](#task-slate-33) (artifact), [SLATE.39](#task-slate-39) (artifact), [SLATE.34](#task-slate-34) (artifact), [SLATE.36](#task-slate-36) (artifact) | not-started |
| [SLATE.42](#task-slate-42) | Real multi-device ArcSlate project convergence against the deployed Cloud sync engine | integration | M | [SLATE.37](#task-slate-37) (artifact), [CLOUD.39](cloud.md#task-cloud-39) (artifact), [CLOUD.44](cloud.md#task-cloud-44) (artifact), [SLATE.12](#task-slate-12) (artifact), [SLATE.35](#task-slate-35) (artifact) | not-started |

## Tasks

<a id="task-slate-01"></a>

### SLATE.01 — Exact time model: canonical ticks, rational rates, frame/sample time, half-open ranges

**Outcome.** RationalRate, FrameTime, SampleTime, TimeRange and the 705,600,000 Hz tick domain exist with exact frame<->tick and sample<->tick round-trip on every supported rate, half-open range algebra ([BO-01](../../../architecture/10-web-architecture.md#rule-bo-01)), and the five enumerated rounding sites ([RP-02](../../../architecture/01-solution-and-project-layout.md#rule-rp-02)) as the only places a position rounds; a policy test asserts no other code path rounds.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-01` and ledger record `ledger/tasks/slate-01.md` in the Plan repository; task branch `task/slate-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-36.01](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01) — full |
| Provides | slate.time.ticks; slate.time.rational; slate.time.range |
| Start prerequisites | none |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.02](#task-slate-02), [SLATE.03](#task-slate-03), [SLATE.06](#task-slate-06), [SLATE.14](#task-slate-14), [SLATE.17](#task-slate-17), [SLATE.20](#task-slate-20), [SLATE.29](#task-slate-29), [SLATE.38](#task-slate-38) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Domain/Time/**`<br>`ArcSlate:tests/ArcForges.ArcSlate.Tests.Unit/Time/**` |
| Validation | Offline unit tests only: NTSC/audio/negative/source-inexact/ties-even/half-open/overflow vectors per [WP-36.01](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01); no runtime/device dependency; AOT-compatible pure C#. |
| Completion evidence | Per-rate round-trip table (frame->tick->frame, sample->tick->sample), long-sequence drift measurement showing zero drift, boundary-sample fixture proving no duplicated/missing sample at a cut. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: ArcSlate repo currently contains only the WP00 to WP02 Hello World/AOT bootstrap (src/ArcForges.ArcSlate, src/ArcForges.ArcSlate.Core) and build/licence/provenance/dependency-policy tests; no Domain project exists yet. |
| Notes | No cross-area start blocker: this is pure C# arithmetic against a frozen architecture-23 spec (§3, §3.10 [OB-01](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-01)..05) and the frozen slate.edit.v1/keyframe profile (26§4). It needs no persistence, no UI, no native ABI and no published Contracts wire type to begin. It is the least-blocked, most-parallelizable task in the whole area and should start immediately alongside repository bootstrap for the other lanes. |

<a id="task-slate-02"></a>

### SLATE.02 — Project and sequence domain model

**Outcome.** Project (multi-sequence container) and Sequence (playable/renderable composition with its own SequenceSettings snapshot and output grids) exist as structurally distinct types over one shared MediaLibrary; Project != Sequence != media folder is asserted structurally.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-02` and ledger record `ledger/tasks/slate-02.md` in the Plan repository; task branch `task/slate-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-36.00](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.00) — full |
| Provides | slate.domain.project; slate.domain.sequence |
| Start prerequisites | **artifact** [SLATE.01](#task-slate-01) — RationalRate/TimeRange types for SequenceSettings video/audio output grids. *Why:* a sequence's output grid must be validated as exactly representable in ticks ([SG-02](../../../architecture/02-contracts-and-protocols.md#rule-sg-02)) before the sequence type can be constructed at all |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.05](#task-slate-05), [SLATE.06](#task-slate-06), [SLATE.10](#task-slate-10) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Domain/Project/**`<br>`ArcSlate:src/ArcForges.ArcSlate.Domain/Sequence/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append) |
| Validation | Offline unit tests: multi-sequence-over-one-library assertion, project/sequence/folder distinction test. |
| Completion evidence | Multi-sequence project fixture; structural-distinction test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-03"></a>

### SLATE.03 — Media asset/stream/metadata domain model and content-based relink algorithm

**Outcome.** MediaAsset (stable logical identity, never a file path), MediaMetadata (streams/codecs/dimensions/rate/duration/colour/timecode/channel layout), MediaAvailability, and a relink algorithm that verifies asset identity/size/content-hash/metadata before reusing an origin hash all exist as pure domain types with no native type present.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-03` and ledger record `ledger/tasks/slate-03.md` in the Plan repository; task branch `task/slate-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-36.02](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) — domain types (MediaAsset/MediaStream/MediaMetadata/MediaAvailability) and the relink-by-content-hash algorithm; excludes the real native read/probe adapter |
| Provides | slate.domain.mediaasset; slate.domain.relink-algorithm |
| Start prerequisites | **artifact** [SLATE.01](#task-slate-01) — source-stream time base rational types for MediaMetadata.rate/duration. *Why:* metadata must record the source's own rational time base ([SM-01](../../../architecture/06-data-persistence-and-formats.md#rule-sm-01)), which reuses the canonical rational type |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.04](#task-slate-04), [SLATE.05](#task-slate-05), [SLATE.06](#task-slate-06), [SLATE.21](#task-slate-21), [SLATE.24](#task-slate-24), [SLATE.36](#task-slate-36) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Domain/Media/**` |
| Validation | Offline unit tests: offline-open structure/edit-decision preservation, relink verification and mismatch reporting, per-device-location-one-logical-asset test, structural no-native-type test. |
| Completion evidence | Offline-open fixture; relink match/mismatch vectors; multi-device-location-one-asset fixture. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Deliberately split from the native read adapter (SLATE.04): everything here is pure domain logic testable against synthetic MediaMetadata, matching [WP-36.02](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02)'s own text that [WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) (full playback) is explicitly NOT an undeclared prerequisite for this step. |

<a id="task-slate-04"></a>

### SLATE.04 — Native media metadata/probe read adapter (real import path)

**Outcome.** Importing a real media file populates MediaMetadata through the owned arc_media_probe ABI running behind the ContentSandbox boundary; malformed metadata and a child crash both preserve the native project (structure and edit decisions intact); content-origin is captured on import per the frozen carrier schema.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-04` and ledger record `ledger/tasks/slate-04.md` in the Plan repository; task branch `task/slate-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-36.02](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) — the real metadata/read adapter using the approved owned ABI and ContentSandbox, and the content-origin carrier/propagation/failure vectors recorded in this substep's evidence row<br>[WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) Content-origin carrier/propagation/failure vectors ([WP-36.02](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) required evidence addition; §8 additional completion requirement) — package-level obligation contribution |
| Provides | slate.media.probe-adapter |
| Start prerequisites | **artifact** [NAT.07](native.md#task-nat-07) — published arc_media_probe / arc_media_reader_stream export in the ArcForges.Native.Media package (managed MediaProbe wrapper). *Why:* populating real MediaMetadata on import requires the actual probe function; only the three version/build/error probe exports exist in DesktopPlatform today (ArcForges.Native.Media/MediaAbi.cs is 33 lines: GetAbiVersion/GetBuildInfo/GetLastError only)<br>**artifact** [SLATE.03](#task-slate-03) — MediaAsset/MediaMetadata domain types to populate. *Why:* the adapter's output type is owned by SLATE.03 |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NAT.14](native.md#task-nat-14) — production ContentSandbox.Runtime.<rid> parser composition (hostile-media containment). *Why:* [WP-36.02](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02)'s testing requirement is that malformed metadata and a child crash preserve the native project; that containment only exists once [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) composes the real parser into the signed helper, not from [WP-11](../../work-packages/11-security-foundation.md#rule-wp-11)'s earlier hostile-test-parser fixture |
| Unblocks | [SLATE.05](#task-slate-05), [SLATE.14](#task-slate-14), [SLATE.15](#task-slate-15), [SLATE.35](#task-slate-35), [SLATE.36](#task-slate-36) |
| Permitted substitutes | [SUB-media-probe-fixture](../substitutes.md#sub-media-probe-fixture) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Infrastructure/Media/ProbeAdapter/**` |
| Validation | Local only; sacrificial-process/child-crash test requires the [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) sandbox on the existing environment; offline unit tests against the fixture substitute are the default CI path per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no live hostile-parsing CI). |
| Completion evidence | Malformed-metadata-preserves-project run; child-crash-preserves-project run; content-origin carrier/propagation/failure vectors with payload and manifest hashes ([WP-36.02](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02) required evidence addition). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-05"></a>

### SLATE.05 — Media library: bins, reference-in-place import, background analysis

**Outcome.** Bins organise assets; import defaults to reference-in-place and completes without waiting for background analysis/caches; an indexing failure never fails the import (the asset still exists, degraded and retryable).

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-05` and ledger record `ledger/tasks/slate-05.md` in the Plan repository; task branch `task/slate-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-36.03](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.03) — full |
| Provides | slate.domain.medialibrary |
| Start prerequisites | **artifact** [SLATE.02](#task-slate-02) — Project/MediaLibrary container. *Why:* bins organise the project's media library, not the disk<br>**artifact** [SLATE.03](#task-slate-03) — MediaAsset identity. *Why:* a bin holds asset references |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SLATE.04](#task-slate-04) — real probe-populated metadata for a fully real import, as opposed to import against the SUB-media-probe-fixture. *Why:* import functionally completes against the fixture, but real evidence that a failed real probe still yields a usable asset is only available once SLATE.04 lands |
| Unblocks | [SLATE.14](#task-slate-14), [SLATE.35](#task-slate-35), [SLATE.36](#task-slate-36) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Domain/Media/Bin/**`<br>`ArcSlate:src/ArcForges.ArcSlate.Application/Import/**` |
| Validation | Offline unit tests: import-completion-timing test, failed-indexing-still-imports test, large-library performance measurement (local, once). |
| Completion evidence | Import timing results; indexing-failure-does-not-fail-import result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-06"></a>

### SLATE.06 — Timeline structural model: tracks, items, clips, transitions, markers

**Outcome.** Role-typed Track, TimelineItem, Clip (in/out points referencing a MediaAsset, never a file path), Transition and Marker/RangeMarker exist; one asset supports unlimited independent clip instances; track ordering/enable/lock/solo exist.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-06` and ledger record `ledger/tasks/slate-06.md` in the Plan repository; task branch `task/slate-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-36.04](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.04) — full |
| Provides | slate.domain.timeline |
| Start prerequisites | **artifact** [SLATE.02](#task-slate-02) — Sequence to hold tracks. *Why:* tracks belong to a sequence's timeline<br>**artifact** [SLATE.03](#task-slate-03) — MediaAsset reference type. *Why:* a clip references an asset by stable identity, never a path<br>**artifact** [SLATE.01](#task-slate-01) — TimeRange for clip in/out and timeline placement. *Why:* clip source range and timeline range are separate typed ranges over the canonical tick domain |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.07](#task-slate-07), [SLATE.10](#task-slate-10), [SLATE.12](#task-slate-12), [SLATE.18](#task-slate-18), [SLATE.26](#task-slate-26), [SLATE.29](#task-slate-29), [SLATE.34](#task-slate-34), [SLATE.38](#task-slate-38) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Domain/Timeline/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append) |
| Validation | Offline unit tests: many-clips-one-asset independence, track operation coverage, structural no-file-path-in-clip test. |
| Completion evidence | Many-clips-one-asset fixture; no-path structural test result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-07"></a>

### SLATE.07 — Edit command pipeline and placement operations

**Outcome.** TimelineCommand infrastructure exists (expand link/group scope, validate locks/handles/overlaps/bounds, commit one undoable transaction, failure changes nothing, caller-supplied IDs replay identically) together with the placement-operation family, each exact per its declared semantics (e.g. Overwrite trims/splits only the target track interval; RippleDelete processes disjoint intervals latest-first so shift occurs once).

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-07` and ledger record `ledger/tasks/slate-07.md` in the Plan repository; task branch `task/slate-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / XL |
| Obligations | [WP-36.05](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.05) — the shared validate->expand-affected-set->one-transaction command pipeline, plus Insert/Overwrite/Move/Trim(in/out)/Split/Delete/Lift/RippleDelete/Extract/Duplicate exactly per slate.edit.v1 (26-product-behavior-profiles.md §4) |
| Provides | slate.edit.pipeline; slate.edit.core-ops |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — Track/TimelineItem/Clip model to operate on. *Why:* every edit command mutates the timeline structural model |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.08](#task-slate-08), [SLATE.09](#task-slate-09), [SLATE.33](#task-slate-33) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Timeline/**`<br>`ArcSlate:src/ArcForges.ArcSlate.Application/Editing/**` |
| Shared resources | [RES-arcslate-registries](../shared-resources.md#res-arcslate-registries) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline unit tests: independent operation examples, collision/source-handle tests, undo/restart vectors, per-command exactness on its own grid (video frame-precise, audio sample-precise, [TG-03](../../../architecture/23-simulator-and-interchange.md#rule-tg-03)). |
| Completion evidence | Per-operation exactness and non-destructiveness results; one-transaction-or-nothing failure vectors. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Sized XL deliberately: 10 commands sharing one pipeline is one coherent reviewable outcome (the pipeline's affected-set/validation/transaction contract), not ten unrelated features; splitting further would fragment review of the shared contract. |

<a id="task-slate-08"></a>

### SLATE.08 — Relationship and retiming edit operations

**Outcome.** The remaining [TL-06](../../../requirements/products/arcslate.md#rule-tl-06) operations exist on the same command pipeline: Roll adjusts a shared cut with both source handles; Slide trims outer neighbours to keep the combined boundary fixed; Link!=shared-identity is enforced; RetimeCurve composes rationals and projects once at the decode boundary with a reported inexact mapping; Snap converts pointer tolerance to ticks once and previews before commit.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-08` and ledger record `ledger/tasks/slate-08.md` in the Plan repository; task branch `task/slate-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-36.05](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.05) — RippleTrim/Roll/Slip/Slide/Group-Ungroup/Link-Unlink/Enable-Disable/ReorderTracks/Transition(create-delete)/Snap/Retime+RetimeCurve/ripple-marker-scope exactly per slate.edit.v1 |
| Provides | slate.edit.advanced-ops |
| Start prerequisites | **artifact** [SLATE.07](#task-slate-07) — the shared command pipeline (validate/affected-set/transaction) and the placement operations these compose with (e.g. Roll needs two adjacent clips already placed). *Why:* these operations extend, and in several cases (Roll/Slide/Transition) directly interact with, the placement operations' handle and collision logic rather than duplicating it |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.12](#task-slate-12), [SLATE.33](#task-slate-33) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Timeline/**` |
| Shared resources | [RES-arcslate-registries](../shared-resources.md#res-arcslate-registries) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline unit tests: reverse/freeze retime, linked-track refusal, collision/source-handle vectors, snap tie-priority (playhead>marker>clip>grid>earlier-tick). |
| Completion evidence | Per-operation exactness results; retime no-drift-across-a-chain-of-speed-changes vector ([TV-06](../../../architecture/13-observability-and-operations.md#rule-tv-06)). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-09"></a>

### SLATE.09 — Undo/redo stack and composite command grouping

**Outcome.** Every edit command produces one undo transaction; a complex multi-command user gesture groups into one composite undo step; undo is demonstrably a different mechanism from checkpoint and crash recovery.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-09` and ledger record `ledger/tasks/slate-09.md` in the Plan repository; task branch `task/slate-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-36.06](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.06) — undo/redo as a distinct mechanism from checkpoint/recovery: composite operation grouping, explicit commit-boundary (a transient drag/preview is never a committed command) |
| Provides | slate.undo |
| Start prerequisites | **artifact** [SLATE.07](#task-slate-07) — the command pipeline's one-transaction-per-command contract. *Why:* undo records the inverse of exactly what the pipeline committed; it cannot be designed independently of that commit boundary |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.11](#task-slate-11), [SLATE.26](#task-slate-26) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Application/Undo/**` |
| Validation | Offline unit tests: undo-across-composite-operations, undo-is-not-recovery distinction test. |
| Completion evidence | Composite-undo fixture; three-mechanism distinction test contribution (paired with SLATE.11's checkpoint/recovery evidence). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-10"></a>

### SLATE.10 — Project persistence and store infrastructure (V1 migration baseline)

**Outcome.** ArcSlate.Infrastructure persists Project/Sequence/Timeline/MediaLibrary through the platform's single write path; fixtures/formats/arcslate/v1/ exists as the V1 project fixture; the storage schema version equals the highest applied migration.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-10` and ledger record `ledger/tasks/slate-10.md` in the Plan repository; task branch `task/slate-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) Database impact: ArcSlate project store and its V1 migration baseline (§6) — package-level: §6 Impacts row "Database: the ArcSlate project store and its V1 migration baseline"; §4 ArcSlate.Infrastructure project store/media index/migration set; package-level obligation contribution |
| Provides | slate.persistence.store |
| Start prerequisites | **artifact** [PLT.01](platform.md#task-plt-01) — published store abstraction with the single transactional write path (validate->authorize->begin->apply->journal->advance revision->commit->notify). *Why:* the project store must use the one real write path; a bespoke ArcSlate-local persistence path would violate [WP-07.00](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.00)'s policy-tested single-write-path rule and hide recovery defects<br>**artifact** [PLT.04](platform.md#task-plt-04) — published migration runner (numbered, transactional-per-step, idempotent, resumable). *Why:* the V1 migration baseline is the first entry in this runner's numbered sequence; ArcSlate cannot invent its own migration mechanism<br>**artifact** [SLATE.02](#task-slate-02) — Project/Sequence domain types to persist. *Why:* the store maps domain aggregates to storage<br>**artifact** [SLATE.06](#task-slate-06) — Timeline/Track/Clip domain types to persist. *Why:* the store maps the full domain graph, not just the project header |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.11](#task-slate-11), [SLATE.26](#task-slate-26), [SLATE.37](#task-slate-37) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Infrastructure/Store/**`<br>`ArcSlate:fixtures/formats/arcslate/v1/**` |
| Shared resources | [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append) |
| Validation | Offline unit tests only; no live database service. |
| Completion evidence | Migration-forward-from-V1 fixture result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-11"></a>

### SLATE.11 — Project checkpoints, crash recovery and project-version migration

**Outcome.** A checkpoint is an explicit user action distinct from both undo and autosave; a kill mid-edit recovers to the last committed boundary and reports what was lost; a prior-version project migrates forward with semantic (not merely structural) preservation.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-11` and ledger record `ledger/tasks/slate-11.md` in the Plan repository; task branch `task/slate-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-36.06](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.06) — project checkpoints as an explicit user mechanism distinct from undo; crash recovery to the last committed boundary with explicit loss reporting; migration from prior project versions with semantic preservation |
| Provides | slate.checkpoint; slate.recovery |
| Start prerequisites | **artifact** [PLT.02](platform.md#task-plt-02) — published append-only journal with durable-before-acknowledged commits. *Why:* checkpoint/recovery cannot be built as a second, ArcSlate-private recovery story; it must ride the one real journal<br>**artifact** [PLT.03](platform.md#task-plt-03) — published snapshot/recovery mechanism with typed outcomes (clean / recovered-with-loss / unrecoverable-with-evidence). *Why:* honest loss reporting requires the platform's typed recovery outcome, not an ArcSlate-invented one<br>**artifact** [SLATE.09](#task-slate-09) — the undo mechanism this task must remain distinct from. *Why:* the completion gate requires demonstrating undo, checkpoint and recovery are three different mechanisms, which presupposes undo exists<br>**artifact** [SLATE.10](#task-slate-10) — the project store to checkpoint/recover. *Why:* checkpoints are snapshots of the persisted project |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.14](#task-slate-14) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Application/Recovery/**` |
| Shared resources | [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append) |
| Validation | Offline unit tests: kill-during-edit recovery run (local process-kill simulation), migration semantic-comparison test. |
| Completion evidence | Kill-during-edit recovery result; three-mechanism distinction result; migration semantic-preservation comparison. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-12"></a>

### SLATE.12 — Slate.project.v1/graph.v1 wire projection: bins, generators, nesting, adjustment, title/subtitle, cycle rejection

**Outcome.** The full slate.project.v1/graph.v1 wire projection round-trips metadata-only (no media bytes) with every edit and Offline Media preserved; nested-sequence and graph cycles are rejected; an unknown imported effect definition is retained and stays inert rather than silently activated.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-12` and ledger record `ledger/tasks/slate-12.md` in the Plan repository; task branch `task/slate-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) Unlabelled final-review closure: complete slate.project.v1/graph.v1 model, generators/nesting/adjustment/title/subtitle, cycle rejection, unknown-effect inert — the unlabelled final-review closure paragraph: "Implement the complete slate.project.v1/graph.v1 model: bins, exact sequence video/audio/colour config, track roles, generators/nesting/adjustment/title/subtitle, graph definition/instance identity and keyframe time scope. Metadata-only cross-device round-trip preserves every edit with Offline Media. Reject graph/nesting cycles and preserve unknown imported effects inert."; package-level obligation contribution |
| Provides | slate.wire.projection |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — Timeline/Track/TimelineItem structural model to project. *Why:* the wire form mirrors the domain model<br>**artifact** [SLATE.08](#task-slate-08) — nested-sequence and adjustment-layer semantics from the edit operation set. *Why:* nesting/cycle rejection is a property of how sequences can reference each other, defined alongside the edit operations<br>**contract** [CON.06](contracts.md#task-con-06) — published slate.project.v1 / slate.graph.v1 generated records in ArcForges.Contracts.LocalRpc.Slate (wire keys per 26-product-behavior-profiles.md §4: transform/crop/opacity/colourAdjustment/audioGain/pan/composite/audioMix, generated-source keys colour/gradient/counter/testPattern/title). *Why:* this task implements the frozen wire shape, not a new one; without the published Contracts package there is no record to project into |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.14](#task-slate-14), [SLATE.42](#task-slate-42) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Infrastructure/Wire/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline unit tests: metadata-only cross-device round-trip fixture, cycle-rejection negative test, unknown-effect-preserved-inert test. |
| Completion evidence | Round-trip-with-Offline-Media fixture; cycle-rejection vectors; unknown-effect inertness proof. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-13"></a>

### SLATE.13 — ArcSlate reference-coverage drift check (maintenance)

**Outcome.** ArcVideo (caf5651) and ArcVideoFoundation (139eeca) are re-diffed against their bound commits; changed rows are reassessed, newly introduced upstream material gets a disposition (mapped or excluded, never auto-adopted), and the licence position is re-confirmed.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-13` and ledger record `ledger/tasks/slate-13.md` in the Plan repository; task branch `task/slate-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Obligations | [WP-36.07](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.07) — full |
| Provides | slate.drift-report |
| Start prerequisites | none |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.14](#task-slate-14) |
| Write scope | `Design:docs/assurance/reference-coverage/arcslate-arcvideo.md` |
| Validation | Design-stage comparison only; no build/test involved. Reads two reference repositories read-only (never executed, per [MT-04](../../../architecture/05-cloud-architecture.md#rule-mt-04)). |
| Completion evidence | Drift report: changed-file list with row reassessment, new-material list with disposition, licence re-verification statement. |
| Baseline (unreviewed unless accepted) | not-started The reference matrix is accepted design-stage evidence; the implementation-time drift check itself has not run. |
| Notes | Not blocked by anything else in this area and touches no ArcSlate source; can run in parallel with all other SLATE tasks. Its only real prerequisite is that the two reference repositories (C:\MyFile\ArcForges\ArcVideo, C:\MyFile\ArcForges\ArcVideoFoundation per the matrix's local paths) remain available read-only. |

<a id="task-slate-14"></a>

### SLATE.14 — Closure: owned-artifact and real-integration receipt

**Outcome.** One recorded receipt (source commit, candidate hashes, actual runtime/OS/provider, scenario, result, real-versus-fixture status per field) demonstrates that the exact timeline/edit/recovery fixtures from SLATE.01-12 remain valid and that no package or wire boundary rounds a frame/time value.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-14` and ledger record `ledger/tasks/slate-14.md` in the Plan repository; task branch `task/slate-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-36.90](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.90) — full |
| Provides | slate.wp36.closure |
| Start prerequisites | **artifact** [SLATE.01](#task-slate-01) — all [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) tasks complete. *Why:* this is a consolidated regression/evidence pass, not new functionality<br>**artifact** [SLATE.11](#task-slate-11) — all [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) tasks complete. *Why:* same<br>**artifact** [SLATE.12](#task-slate-12) — all [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) tasks complete. *Why:* same<br>**artifact** [SLATE.13](#task-slate-13) — drift report exists. *Why:* the completion gate requires the drift check to have run<br>**artifact** [SLATE.04](#task-slate-04) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.05](#task-slate-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.03](release.md#task-rel-03) |
| Write scope | `ArcSlate:docs/evidence/wp36-90-receipt.md` |
| Validation | Re-run of SLATE.01-12's existing offline unit suites plus a policy test that no rounding site outside [RP-02](../../../architecture/01-solution-and-project-layout.md#rule-rp-02)'s five exists. |
| Completion evidence | The consolidated receipt itself. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-15"></a>

### SLATE.15 — Native media boundary consumption (ArcSlate.Media wrapper and safety suite)

**Outcome.** ArcSlate.Media consumes the exact published ArcForges.Native.Media/.Colour/.Image/.Otio/.Graphics packages with managed input validation, safe handles and a sacrificial-process integration suite; sanitiser builds run in CI; every native dependency's licence position is recorded; no native type escapes the media layer. Satisfies [PG-03](../../../assurance/open-gates-register.md#rule-pg-03) for ArcSlate.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-15` and ledger record `ledger/tasks/slate-15.md` in the Plan repository; task branch `task/slate-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L · early risk proof |
| Obligations | [WP-37.00](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.00) — full |
| Provides | slate.media.abi-boundary |
| Start prerequisites | **artifact** [NAT.06](native.md#task-nat-06) — the compiled common ABI/preamble/pack-8 record layer all family wrappers build on. *Why:* every family-specific export (media/colour/image/otio/graphics) is declared against this common layer; nothing else can compile without it<br>**artifact** [NAT.07](native.md#task-nat-07) — published functional arc_media_reader_*/probe exports in ArcForges.Native.Media (beyond the current 3-function version/build/error probe). *Why:* the boundary-consumption task must exercise a real function, not only the probe triad; DesktopPlatform's MediaAbi.cs today is exactly 33 lines covering only GetAbiVersion/GetBuildInfo/GetLastError<br>**artifact** [NAT.08](native.md#task-nat-08) — published arc_media_writer_*/convert/resample exports. *Why:* domain-purity and handle-lifetime tests must cover the writer path too, not only decode<br>**artifact** [SLATE.04](#task-slate-04) — native media metadata and probe adapter. *Why:* the native boundary consumption replaces the probe fixture used by the adapter |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.16](#task-slate-16), [SLATE.19](#task-slate-19), [SLATE.23](#task-slate-23) |
| Permitted substitutes | [SUB-no-op-media-adapter](../substitutes.md#sub-no-op-media-adapter) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Media/**`<br>`ArcSlate:src/ArcForges.ArcSlate.Native/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | ABI conformance and version-mismatch rejection tests, ownership/handle-lifetime tests, sanitiser runs, sacrificial-process crash tests, domain-purity test -- all local, once, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no hosted native CI). |
| Completion evidence | ABI version-negotiation result; leak-free handle-lifetime proof; clean sanitiser run; sacrificial-process crash-containment result; [PG-03](../../../assurance/open-gates-register.md#rule-pg-03) licence-position record. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform's native/ tree has real ABI header/shim scaffolding (native/arcmedia-ffmpeg-abi, native/arcslate-color-abi, native/arcslate-otio-abi, native/shared) and managed wrapper stubs (src/Native/ArcForges.Native.{Media,Colour,Otio,Image}), but every managed wrapper currently exports only the 3-function version/build/error probe triad (33 lines each); no functional export exists yet. |
| Notes | First real ArcSlate-side exercise of the native P/Invoke boundary; [WP-13.03](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.03) (Probe D) already proved decode+sync feasibility in isolation, but this task is where ArcSlate's own AOT-published, sanitiser-clean, sacrificial-process-tested consumption is proven for the first time. A failure here (ABI mismatch, handle leak, AOT trimming of a marshalled type) invalidates SLATE.16 through SLATE.31. |

<a id="task-slate-16"></a>

### SLATE.16 — Decode and pooled buffers

**Outcome.** Demux and decode run through the boundary into pooled buffers; buffers return on every path including failure; pool exhaustion is measured and surfaced; hardware acceleration is discovered at runtime with a proven software fallback whose output matches within declared tolerance.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-16` and ledger record `ledger/tasks/slate-16.md` in the Plan repository; task branch `task/slate-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L · early risk proof |
| Obligations | [WP-37.01](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01) — full |
| Provides | slate.media.decode |
| Start prerequisites | **artifact** [SLATE.15](#task-slate-15) — the ABI boundary/wrapper this decode path calls through. *Why:* decode is the first real workload over that boundary |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NAT.14](native.md#task-nat-14) — production ContentSandbox.Runtime.<rid> parser composition. *Why:* [WP-37.01](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01) is the named [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) evidence anchor: 'real packaged hostile media parsing containment and no unrestricted fallback' cannot be satisfied by the earlier [WP-11](../../work-packages/11-security-foundation.md#rule-wp-11) test-parser fixture |
| Unblocks | [SLATE.17](#task-slate-17), [SLATE.20](#task-slate-20), [SLATE.21](#task-slate-21), [SLATE.30](#task-slate-30) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Media/Decode/**` |
| Shared resources | [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Long-run buffer accounting, pool-exhaustion behaviour, forced-software-path equivalence, decode-capability disclosure -- local, once, on the existing environment. |
| Completion evidence | Buffer-leak-free soak result; pool-exhaustion surfaced result; software-vs-hardware equivalence-within-tolerance result; [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) hostile-input containment result. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) anchor for ArcSlate: this is where hostile-media containment is proven for the whole product, not merely for PDF/Notes. |

<a id="task-slate-17"></a>

### SLATE.17 — Playback engine, clock and scheduler

**Outcome.** The playback engine is driven by the timeline clock, decoupled from editing so an edit invalidates and re-requests incrementally without stalling playback; frames may drop but the audio/timeline clock stays correct; playback quality state (realtime/reduced/proxy/dropping/requires-render) is computed and visible.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-17` and ledger record `ledger/tasks/slate-17.md` in the Plan repository; task branch `task/slate-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L · early risk proof |
| Obligations | [WP-37.02](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.02) — full |
| Provides | slate.playback.engine |
| Start prerequisites | **artifact** [SLATE.16](#task-slate-16) — decoded frames/audio buffers to schedule. *Why:* the clock schedules already-decoded content<br>**artifact** [SLATE.01](#task-slate-01) — the exact tick/grid time model. *Why:* [TV-04](../../../architecture/13-observability-and-operations.md#rule-tv-04)/[TV-05](../../../architecture/13-observability-and-operations.md#rule-tv-05) require the audio clock projected from canonical ticks with zero drift over a long sequence; this cannot be retrofitted onto an approximate clock |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.22](#task-slate-22) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Playback/**` |
| Validation | Edit-during-playback tests, A/V synchronisation measurement under induced load, long-playback drift test, quality-state coverage -- local, once. |
| Completion evidence | Sync-under-load measurement; long-run drift measurement (must show zero); quality-state coverage matrix. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This is where [WP-13.03](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.03)'s (Probe D) isolated decode+sync proof becomes a real, editable-while-playing product runtime under load -- the specific risk [ND-04](../../implementation-sequence.md#rule-nd-04) in implementation-sequence.md names ('ArcSlate does not meet... synchronisation... problems for the first time at work package 36'). A narrow A/V-sync-under-load spike is worth running before building the full quality-state UI on top. |

<a id="task-slate-18"></a>

### SLATE.18 — Processing graph and keyframe engine (pure evaluation)

**Outcome.** A typed acyclic ProcessingGraph evaluates per node kind with typed, non-arbitrarily-connectable ports; EffectDefinition and EffectInstance are distinct; keyframe time is pinned to its declared clip-local-or-sequence scope and never silently switches, including across a clip move; bezier evaluation uses the exact cubic-Hermite tangent contract.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-18` and ledger record `ledger/tasks/slate-18.md` in the Plan repository; task branch `task/slate-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-37.03](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.03) — graph topology/ports/EffectDefinition-vs-Instance/keyframe-scope/curve-evaluation engine, including the built-in definitions and formulas of 26-product-behavior-profiles.md §5 (transform/crop/opacity/colourAdjustment/audioGain/pan, hold/linear/bezier keyframe evaluation, RetimeCurve); excludes execution of any node that requires a native pixel/sample operation |
| Provides | slate.processing.graph-engine |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — TimelineItem/Clip/Track to attach graphs and adjustment layers to. *Why:* an adjustment clip is a generated/special timeline clip plus a processing graph ([PG-12](../../../assurance/open-gates-register.md#rule-pg-12)), so the graph engine composes with the timeline model |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.19](#task-slate-19), [SLATE.20](#task-slate-20), [SLATE.23](#task-slate-23), [SLATE.24](#task-slate-24) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Processing/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append) |
| Validation | Offline unit tests: per-node-kind evaluation correctness, keyframe-scope-across-a-clip-move test, definition-vs-instance distinction test, adjustment-layer ordering test. |
| Completion evidence | Per-node-kind evaluation results; keyframe-scope-never-switches result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-19"></a>

### SLATE.19 — Native-backed processing nodes (convert, scale, transform, colour-adjustment execution)

**Outcome.** Transform/crop/composite/generated-source nodes actually produce pixel output through the native convert path when evaluated, matching the CPU reference formulas within the declared 1e-5 tolerance; the CPU graph definition remains the oracle for any optional GPU acceleration.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-19` and ledger record `ledger/tasks/slate-19.md` in the Plan repository; task branch `task/slate-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-37.03](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.03) — execution of graph nodes that require a real pixel/sample operation (video convert/scale/transform), and generated media (colour/gradient/counter/test-pattern/title per 26§5) |
| Provides | slate.processing.native-nodes |
| Start prerequisites | **artifact** [SLATE.18](#task-slate-18) — the graph/port/keyframe engine these nodes plug into. *Why:* a native node is one ProcessingNode implementation inside that engine<br>**artifact** [SLATE.15](#task-slate-15) — the ABI boundary. *Why:* these nodes call arc_media_video_convert<br>**artifact** [NAT.08](native.md#task-nat-08) — published arc_media_video_convert export. *Why:* scale/format-convert nodes need the real convert function<br>**artifact** [NAT.15](native.md#task-nat-15) — published ArcGraphicsNative CPU surface. *Why:* generated-source/title rendering needs the portable CPU raster surface |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.23](#task-slate-23), [SLATE.25](#task-slate-25), [SLATE.28](#task-slate-28) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Processing/NativeNodes/**` |
| Shared resources | [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Reference-vector comparison at 1e-5 per-channel tolerance before quantisation; identity-operation exactness check. |
| Completion evidence | Per-formula reference-vector results (exposure/contrast/saturation/composite/crop/transform). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-20"></a>

### SLATE.20 — Audio processing chain and sample-accurate mixing

**Outcome.** Per-non-overlapping-track-cut sample ownership is assigned (never rounded) per [BO-02](../../../architecture/10-web-architecture.md#rule-bo-02), all track/transition contributions are summed once at each output index ([BO-02](../../../architecture/10-web-architecture.md#rule-bo-02)/[BO-03](../../../architecture/10-web-architecture.md#rule-bo-03)), filter/resampler padding primes DSP without being emitted independently, and gain/pan/dissolve/crossfade use the exact formulas of 26§5 (10^(dB/20) gain, equal-power pan/crossfade). Satisfies the [PG-20](../../../assurance/open-gates-register.md#rule-pg-20) per-track-cut-ownership evidence for ArcSlate.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-20` and ledger record `ledger/tasks/slate-20.md` in the Plan repository; task branch `task/slate-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / XL · early risk proof |
| Obligations | [WP-37.04](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.04) — full |
| Provides | slate.audio.mixing |
| Start prerequisites | **artifact** [SLATE.01](#task-slate-01) — the sample grid and half-open range algebra this mixing rule is defined over. *Why:* [BO-01](../../../architecture/10-web-architecture.md#rule-bo-01)..[BO-05](../../../architecture/10-web-architecture.md#rule-bo-05) is a time-model rule, not an audio-DSP convention; it cannot be implemented independently of the canonical tick/sample projection<br>**artifact** [SLATE.18](#task-slate-18) — the processing graph's audio-buffer port type and node composition. *Why:* audio clip/track effects run through the same processing graph as audio nodes ([AU-03](../../../architecture/02-contracts-and-protocols.md#rule-au-03))<br>**artifact** [SLATE.16](#task-slate-16) — decoded audio buffers to mix. *Why:* mixing operates on real decoded samples<br>**artifact** [NAT.08](native.md#task-nat-08) — published resampler push/drain exports with retained delay. *Why:* sample-accurate mixing requires the pinned resampler's exact delay/drain accounting; an approximate resampler would reintroduce the exact defect [BO-03](../../../architecture/10-web-architecture.md#rule-bo-03)/[BO-04](../../../architecture/10-web-architecture.md#rule-bo-04) exist to prevent |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.23](#task-slate-23), [SLATE.28](#task-slate-28) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Audio/**` |
| Shared resources | [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Two-mixed-tracks/dissolve/track-gap/resampler-priming/NTSC-frame-one-boundary vectors, each asserting exactly one mixed output sample at index k; mixing-against-reference-output test; sync-under-load test with video. |
| Completion evidence | The [TV-08](../../../architecture/13-observability-and-operations.md#rule-tv-08) fixture (a cut at frame 1 of 30000/1001 fps @ 48 kHz emits sample 1601 exactly once and 1602 exactly once); mixing-vs-reference results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | The design doc devotes a full worked example (23-simulator-and-interchange.md §3.4) to exactly the boundary-duplication defect this task must avoid (directional outward rounding on both sides of a cut double-emits the boundary sample). This is a subtle, easy-to-get-wrong correctness area that also anchors [PG-20](../../../assurance/open-gates-register.md#rule-pg-20); worth a narrow proof against the [TV-08](../../../architecture/13-observability-and-operations.md#rule-tv-08) fixture before building the full mixing/gain-staging UI on top. |

<a id="task-slate-21"></a>

### SLATE.21 — Proxies and derived caches

**Outcome.** Proxy generation/policy per project and per asset, plus render/thumbnail/waveform caches, all exist as derived stores; a clip never knows which representation is in use; deleting every cache leaves the project fully intact; render output is identical with proxies enabled and disabled.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-21` and ledger record `ledger/tasks/slate-21.md` in the Plan repository; task branch `task/slate-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-37.05](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.05) — full |
| Provides | slate.proxy-cache |
| Start prerequisites | **artifact** [SLATE.03](#task-slate-03) — MediaAsset identity for cache keys. *Why:* cache keys are keyed by asset + canonical tick range, never by file path<br>**artifact** [SLATE.16](#task-slate-16) — decode to generate proxy/thumbnail source frames. *Why:* a proxy is a cheaper decode of the same source<br>**artifact** [NAT.08](native.md#task-nat-08) — published media writer to encode proxy media. *Why:* proxy generation writes a real portable-profile file<br>**artifact** [NAT.11](native.md#task-nat-11) — published still-image codec export (PNG) for thumbnails. *Why:* thumbnail cache entries are images, not video files<br>**artifact** [PLT.07](platform.md#task-plt-07) — published derived-store abstraction with rebuild semantics and storage-pressure eviction. *Why:* proxy/render/thumbnail/waveform caches must be modelled as the platform's one derived-store kind, not four ArcSlate-private ad hoc eviction policies, or [PX-08](../../../requirements/products/arcslate.md#rule-px-08) (deleting every cache leaves the project intact) becomes four separate things to get right |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.23](#task-slate-23) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Infrastructure/DerivedCaches/**` |
| Shared resources | [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append) |
| Validation | Proxy-equivalence test (output identical with proxies on/off), delete-all-caches-and-rebuild test, clip-ignorance structural test, cache eviction under storage pressure -- local, once. |
| Completion evidence | Proxy-on/off output-identity result; delete-all-caches-leaves-project-intact result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-22"></a>

### SLATE.22 — Viewer: source and sequence, professional transport

**Outcome.** Source and sequence viewers exist with play/pause/frame-step/shuttle/in-out-marking/go-to-timecode/loop/rate, fully keyboard-operable, with playback quality state visible.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-22` and ledger record `ledger/tasks/slate-22.md` in the Plan repository; task branch `task/slate-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-37.06](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.06) — full |
| Provides | slate.viewer |
| Start prerequisites | **artifact** [SLATE.17](#task-slate-17) — the playback engine/clock/quality-state this viewer displays and controls. *Why:* the viewer is a UI over the playback engine, not an independent implementation<br>**artifact** [NAT.15](native.md#task-nat-15) — published ArcGraphicsNative presentable-surface exports. *Why:* the viewer presents decoded frames via a presentable surface/bitmap, never a raw GPU handle<br>**artifact** [PLT.27](platform.md#task-plt-27) — published windows/panels/layout foundation. *Why:* the viewer is hosted as a panel inside the shared dock/panel shell, not a bespoke window system<br>**artifact** [PLT.28](platform.md#task-plt-28) — published command system. *Why:* keyboard-first transport controls are commands routed through the shared command system, not ad hoc key handlers |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.56](platform.md#task-plt-56), [SLATE.23](#task-slate-23) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Presentation/Viewer/**`<br>`ArcSlate:src/ArcForges.ArcSlate.Desktop/Viewer/**` |
| Validation | Transport coverage, frame-accuracy-at-step-boundary assertions, keyboard-only operation test. |
| Completion evidence | Frame-accurate transport results; keyboard-only operability result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-23"></a>

### SLATE.23 — Closure: owned-artifact and real-integration receipt

**Outcome.** A clean AOT package consumer plus representative decode, synchronisation, cancellation, damaged-input and native dependency loading pass on every supported RID; the receipt records exact artifacts and real-versus-fixture status per field.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-23` and ledger record `ledger/tasks/slate-23.md` in the Plan repository; task branch `task/slate-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-37.90](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.90) — full<br>[WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) Unlabelled final-review closure: consume actual Platform media packages, portable baseline codec/graph/audio-grid verification, unsupported-capability-cannot-be-advertised, font/colour/source identity affects render snapshot — the unlabelled final-review closure paragraph: consume actual Platform media packages, test portable baseline render codecs/graph-source semantics/audio-grid mixing together, confirm unsupported native capabilities cannot be advertised, and that font/colour/source identity affects the render snapshot (the last clause is jointly satisfied here and at SLATE.26); package-level obligation contribution |
| Provides | slate.wp37.closure |
| Start prerequisites | **artifact** [SLATE.15](#task-slate-15) — all [WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) tasks complete. *Why:* consolidated evidence pass<br>**artifact** [SLATE.22](#task-slate-22) — all [WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) tasks complete. *Why:* same<br>**artifact** [SLATE.18](#task-slate-18) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.19](#task-slate-19) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.20](#task-slate-20) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.21](#task-slate-21) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.03](release.md#task-rel-03) |
| Write scope | `ArcSlate:docs/evidence/wp37-90-receipt.md` |
| Validation | Clean AOT publish + representative decode/sync/cancellation/damaged-input/dependency-loading run on every admitted RID, local, once. |
| Completion evidence | The consolidated receipt. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-24"></a>

### SLATE.24 — Colour management: input interpretation, working config, display/export transform separation

**Outcome.** Per-asset input colour metadata with a non-destructive override, a project/sequence working colour configuration, and strictly separate viewer-display and export transforms all exist; the colour domain holds only semantic configuration, with the OCIO backend fully behind an infrastructure interface.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-24` and ledger record `ledger/tasks/slate-24.md` in the Plan repository; task branch `task/slate-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-38.00](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.00) — full |
| Provides | slate.colour.management |
| Start prerequisites | **artifact** [SLATE.18](#task-slate-18) — the processing graph's colour-data port type. *Why:* colour transforms are graph data, per [PG-04](../../../assurance/open-gates-register.md#rule-pg-04)<br>**artifact** [SLATE.03](#task-slate-03) — MediaAsset input colour metadata. *Why:* colour interpretation starts from the asset's own recorded colour metadata<br>**artifact** [NAT.10](native.md#task-nat-10) — published arc_color_config_open/arc_color_processor_create/arc_color_apply exports (immutable OCIO config/processor). *Why:* real colour management needs the actual pinned OCIO asset bundle and processor, not a placeholder transform |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.27](#task-slate-27), [SLATE.32](#task-slate-32) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Color/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Round-trip colour tests against reference values, override-non-destructiveness assertion, display-transform-never-alters-export test, domain-purity test on the colour model. |
| Completion evidence | Round-trip colour results; display/export separation proof; domain-purity result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-25"></a>

### SLATE.25 — Video scopes (waveform, vectorscope, histogram, parade)

**Outcome.** Waveform/vectorscope/histogram/parade all read correctly against reference signals as derived views over the current frame or range, each stating its measurement point in the pipeline explicitly.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-25` and ledger record `ledger/tasks/slate-25.md` in the Plan repository; task branch `task/slate-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-38.01](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.01) — full |
| Provides | slate.scopes |
| Start prerequisites | **artifact** [SLATE.19](#task-slate-19) — processed frame buffers to measure. *Why:* a scope reads the pipeline's actual output at a declared point<br>**artifact** [NAT.15](native.md#task-nat-15) — published graphics CPU surface. *Why:* scope rendering is itself a raster surface<br>**artifact** [PLT.27](platform.md#task-plt-27) — published panel foundation. *Why:* scopes are their own dockable panel, distinct from the ArcScope product panel vocabulary |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.32](#task-slate-32) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Visualization/**` |
| Validation | Reference-signal tests per scope, measurement-point disclosure assertion, performance test at playback rate. |
| Completion evidence | Per-scope reference-signal results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-26"></a>

### SLATE.26 — Render planning and immutable snapshot binding

**Outcome.** A RenderRequest captures sequence/range/preset/destination/options and binds an immutable project+sequence revision snapshot including font/colour/source-hash identities; editing during a render never affects that running render; proxy render is opt-in and recorded in output metadata.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-26` and ledger record `ledger/tasks/slate-26.md` in the Plan repository; task branch `task/slate-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-38.02](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.02) — full<br>[WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) final-review closure clause: font/colour/source identity affects the render snapshot (the snapshot-binding half; the native-package-consumption half is SLATE.23) — final-review closure clause: font/colour/source identity affects the render snapshot (the snapshot-binding half; the native-package-consumption half is SLATE.23)<br>[WP-37](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) Unlabelled final-review closure: consume actual Platform media packages, portable baseline codec/graph/audio-grid verification, unsupported-capability-cannot-be-advertised, font/colour/source identity affects render snapshot — package-level obligation contribution |
| Provides | slate.render.plan |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — the timeline structure to snapshot. *Why:* a render plan is a frozen copy of the timeline<br>**artifact** [SLATE.09](#task-slate-09) — the undo/revision concept this snapshot binds to. *Why:* [RN-04](../../../architecture/18-editing-and-rich-content.md#rule-rn-04) requires binding a project/sequence revision, reusing the same revision notion as undo/checkpoint<br>**artifact** [SLATE.10](#task-slate-10) — the project store, to read a committed revision. *Why:* the snapshot must be read from durable committed state, never live editor memory |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.28](#task-slate-28), [SLATE.39](#task-slate-39) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Rendering/Planning/**`<br>`ArcSlate:src/ArcForges.ArcSlate.Domain/Render/**` |
| Validation | Edit-during-render test asserting output is unaffected; snapshot-binding assertion; proxy-render disclosure test. |
| Completion evidence | Edit-during-render-unaffected result; snapshot-binding proof. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-27"></a>

### SLATE.27 — Export presets and encoding validation

**Outcome.** Reusable ExportPresets cover container/codec/rate/resolution/colour-output/audio configuration; an invalid combination is refused before a ProductJob starts, never failing mid-render; the three portable baseline profiles (matroska-ffv1-pcm, wav-pcm, mp4-mpeg4-aac) validate exactly per the declared bounds (even dimensions 16-8192, sequence-representable rate, etc.).

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-27` and ledger record `ledger/tasks/slate-27.md` in the Plan repository; task branch `task/slate-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-38.04](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.04) — full |
| Provides | slate.export.presets |
| Start prerequisites | **artifact** [SLATE.24](#task-slate-24) — colour-output configuration the preset references. *Why:* a preset names a colour output target, which the colour-management task owns<br>**artifact** [NAT.08](native.md#task-nat-08) — the exact three writer profile identities (matroska-ffv1-pcm/wav-pcm/mp4-mpeg4-aac). *Why:* validation checks against the profiles the real writer actually supports; a preset that validates against an imagined profile the writer cannot produce is a defect the whole point of pre-validation exists to prevent |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.28](#task-slate-28), [SLATE.31](#task-slate-31) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Domain/Render/ExportPreset.cs`<br>`ArcSlate:src/ArcForges.ArcSlate.Rendering/Encoding/**` |
| Shared resources | [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Preset validation negative tests; encode conformance tests per preset against golden fixtures with declared tolerance; metadata-correctness check on output files. |
| Completion evidence | Invalid-preset-refused-before-start results; per-preset conformance results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-28"></a>

### SLATE.28 — Render execution engine and atomic export (native Product Job)

**Outcome.** Render runs as a native Product Job (progress, pause, resume, cancellation) owned and recovered by ArcSlate, never entering task.task or consuming AI capacity; output writes to a temporary target and commits atomically so a crash/cancel/missing marker never exposes a complete-looking file; a long render survives machine sleep and resumes where the platform permits.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-28` and ledger record `ledger/tasks/slate-28.md` in the Plan repository; task branch `task/slate-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / XL |
| Obligations | [WP-38.03](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.03) — full<br>[WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) Security impact: output paths validated, no arbitrary write location (§6) — package-level obligation contribution<br>[WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) Additional completion requirement: content-origin vectors on render/subtitle output paths, including unknown input and failed publication (§8) — package-level obligation contribution |
| Provides | slate.render.execution |
| Start prerequisites | **artifact** [SLATE.26](#task-slate-26) — the render plan/snapshot this executes. *Why:* execution consumes an already-bound immutable plan<br>**artifact** [SLATE.27](#task-slate-27) — the validated export preset. *Why:* execution never starts against an unvalidated preset<br>**artifact** [SLATE.19](#task-slate-19) — the native-backed graph evaluator to produce pixels. *Why:* render evaluates the same processing graph as preview, per [MP-03](../../../architecture/12-native-interop-and-media.md#rule-mp-03)/[BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)<br>**artifact** [SLATE.20](#task-slate-20) — sample-accurate mixing for the rendered audio track. *Why:* render output audio must follow the same [BO-01](../../../architecture/10-web-architecture.md#rule-bo-01)..[BO-05](../../../architecture/10-web-architecture.md#rule-bo-05) ownership rules as preview<br>**artifact** [NAT.08](native.md#task-nat-08) — published writer open/write/finish/abort with commit-only-after-complete semantics. *Why:* atomic export is only as atomic as the underlying writer's finish/abort contract<br>**artifact** [EXE.01](execution.md#task-exe-01) — the published native ProductJob engine (ProductJobId/ProductJobRecord/JobStep/JobAttempt/ExecutionState/Checkpoint/CompensationAction/ApprovalGate/ResourcePermit/ProgressReport/ExecutionOutcome/ExecutionTrace). *Why:* [WP-38.03](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.03)'s own text says render 'shares the Product Job lifecycle of [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16)'; render cannot invent a second, ArcSlate-private job-lifecycle model without duplicating exactly the recovery/checkpoint/compensation machinery [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) exists to give every product once |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.31](#task-slate-31), [SLATE.33](#task-slate-33) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Rendering/Execution/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append), [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Cancellation and failure tests asserting no complete-looking partial file; long-render soak; sleep-and-resume test; disk-full test -- local, once, on the existing environment. |
| Completion evidence | No-complete-looking-partial-file results; soak survival result; sleep/resume result. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38)'s own dependency header lists only 'Upstream: 37', omitting [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) even though [WP-38.03](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.03)'s body text explicitly requires [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16)'s Product Job lifecycle. |

<a id="task-slate-29"></a>

### SLATE.29 — Subtitles and captions: authored tracks, SRT/WebVTT import/export

**Outcome.** SubtitleTrack/SubtitleCue exist as an independent track role (never a text-overlay effect); imported millisecond timestamps convert exactly to ticks; export rounds each endpoint once to nearest millisecond (ties-to-even) and reports maximum endpoint error and any collapsed-cue extension/refusal; exported files carry the content-origin carrier/sidecar.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-29` and ledger record `ledger/tasks/slate-29.md` in the Plan repository; task branch `task/slate-29` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-38.05](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.05) — authored subtitles and SRT/WebVTT import/export: exact canonical ticks, declared nearest-ms bounded loss on export (<=0.5ms), explicit collapsed-interval handling, retained sidecar/origin<br>[WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) Additional completion requirement: content-origin vectors on render/subtitle output paths, including unknown input and failed publication (§8) — package-level obligation contribution<br>[WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) Unlabelled final-review closure: SRT/WebVTT preview/import/export plus local extraction ProductJob/TranscriptRecord adoption — package-level obligation contribution |
| Provides | slate.subtitles |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — the track-role model subtitle tracks are a role of. *Why:* [SB-01](../../../architecture/12-native-interop-and-media.md#rule-sb-01): subtitle is an independent track role, part of the same timeline structural model<br>**artifact** [SLATE.01](#task-slate-01) — the tick<->millisecond conversion boundary. *Why:* subtitle millisecond interchange is one of the five enumerated rounding sites ([RP-02](../../../architecture/01-solution-and-project-layout.md#rule-rp-02)) |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.30](#task-slate-30), [SLATE.32](#task-slate-32) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Subtitles/**` |
| Shared resources | [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Independent sub-ms/negative/out-of-range/overlap/collapse vectors and a round-trip fidelity report; no blanket byte/time identity claim for lossy standard formats. |
| Completion evidence | Round-trip fidelity report per format; <=0.5ms max-endpoint-error result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-30"></a>

### SLATE.30 — Local transcription extraction ProductJob and TranscriptRecord adoption

**Outcome.** A local isolated ProductJob freezes the selected sequence revision/range, extracts mono PCM16 WAV in <=30s/1MiB chunks, and records exact sample counts/hashes/conform mapping without auto-uploading; adoption previews derived segments as authored subtitle cues, binds NativeContentRev, requires explicit partial-output acceptance where applicable, and commits one undoable edit carrying AI content-origin.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-30` and ledger record `ledger/tasks/slate-30.md` in the Plan repository; task branch `task/slate-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-38.05](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.05) — the final-review closure clause: local extraction ProductJob and TranscriptRecord review/adoption under expectedNative/undo/origin (slate.transcribe.v1)<br>[WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) Additional completion requirement: content-origin vectors on render/subtitle output paths, including unknown input and failed publication (§8) — package-level obligation contribution<br>[WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) Unlabelled final-review closure: SRT/WebVTT preview/import/export plus local extraction ProductJob/TranscriptRecord adoption — package-level obligation contribution |
| Provides | slate.transcription.extraction |
| Start prerequisites | **artifact** [SLATE.29](#task-slate-29) — the SubtitleTrack/Cue model adoption writes into. *Why:* adoption commits ordinary subtitle-track edits<br>**artifact** [SLATE.16](#task-slate-16) — decode to extract PCM audio. *Why:* extraction reads real decoded audio<br>**artifact** [EXE.01](execution.md#task-exe-01) — the native ProductJob engine (local isolated job). *Why:* this extraction is explicitly a local ProductJob, sharing the same lifecycle machinery as render (SLATE.28) |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [HAR.91](harness.md#task-har-91) — real Cloud Workers AI whisper-large-v3-turbo output reconciled end to end. *Why:* this task's own scope explicitly uses published ASR-output fixtures; [WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) supplies the real model output and [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) closes the paid end-to-end path, so the extraction/adoption logic here is complete against a fixture but the product capability is not commercially real until that integration lands |
| Unblocks | [HAR.91](harness.md#task-har-91), [SLATE.32](#task-slate-32) |
| Permitted substitutes | [SUB-slate-asr-fixture](../substitutes.md#sub-slate-asr-fixture) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Application/Transcription/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Local extraction/adoption tests against the SUB-slate-asr-fixture only; no live AI dispatch in this task's own CI (that belongs to [WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43)/[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)'s no-real-inference-CI rule). |
| Completion evidence | Extraction-artifact exact-sample-count/hash result; adoption-commits-one-undoable-edit result; partial-output-acceptance result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-31"></a>

### SLATE.31 — Golden output stability corpus

**Outcome.** A golden fixture corpus with declared tolerances covers every supported export preset; a codec or backend update that changes output beyond tolerance fails the build and requires a recorded decision.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-31` and ledger record `ledger/tasks/slate-31.md` in the Plan repository; task branch `task/slate-31` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-38.06](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.06) — full |
| Provides | slate.golden-corpus |
| Start prerequisites | **artifact** [SLATE.28](#task-slate-28) — real render execution to produce the corpus outputs. *Why:* the corpus is generated by actually rendering, not synthesised<br>**artifact** [SLATE.27](#task-slate-27) — every supported preset to cover. *Why:* the completeness requirement is 'covers every supported preset' |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.32](#task-slate-32) |
| Write scope | `ArcSlate:fixtures/media/golden/**` |
| Shared resources | [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Golden comparison across the corpus; a deliberate-change negative test asserting the gate fires -- local, once. |
| Completion evidence | Full-corpus comparison result; negative-gate-fires proof. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Golden media fixture acquisition/licensing is a cross-cutting logistical risk: SLATE.16 (decode), SLATE.20 (audio mixing), SLATE.27/28 (encode conformance) and SLATE.38/39 (OTIO round-trip) all need real, licence-clear test media before their own real-integration evidence can be recorded, not only this task. |

<a id="task-slate-32"></a>

### SLATE.32 — Closure: owned-artifact and real-integration receipt

**Outcome.** Independent render/range/colour/output checks and cancel/failure/atomic-publish recovery pass, with the receipt confirming no CF Harness or AI budget is required for native render execution.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-32` and ledger record `ledger/tasks/slate-32.md` in the Plan repository; task branch `task/slate-32` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-38.90](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.90) — full |
| Provides | slate.wp38.closure |
| Start prerequisites | **artifact** [SLATE.24](#task-slate-24) — all [WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) tasks complete. *Why:* consolidated evidence pass<br>**artifact** [SLATE.31](#task-slate-31) — all [WP-38](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38) tasks complete. *Why:* same<br>**artifact** [HAR.91](harness.md#task-har-91) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.25](#task-slate-25) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.29](#task-slate-29) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.30](#task-slate-30) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.03](release.md#task-rel-03) |
| Write scope | `ArcSlate:docs/evidence/wp38-90-receipt.md` |
| Validation | Consolidated re-run of SLATE.24-31's suites, local, once. |
| Completion evidence | The consolidated receipt. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-33"></a>

### SLATE.33 — Capability surface: query, edit, render and export capabilities

**Outcome.** Query capabilities (projects/sequences/tracks/clips/markers/media/transcripts/render-state), edit capabilities (semantic timeline operations, marker/subtitle operations, effect application) and render/export capabilities (ProductJobHandle-returning) are all registered, each declaring risk/side-effect-class/reversibility/approval-posture with owner-side validation; the contract is provably frozen only after timeline/command/undo semantics stabilised.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-33` and ledger record `ledger/tasks/slate-33.md` in the Plan repository; task branch `task/slate-33` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-39.00](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.00) — full |
| Provides | slate.capabilities |
| Start prerequisites | **artifact** [SLATE.07](#task-slate-07) — the stable semantic edit-command set to expose. *Why:* [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)/the stability gate explicitly requires timeline/command/undo semantics to be stable before capabilities are frozen<br>**artifact** [SLATE.08](#task-slate-08) — the remaining edit-command set. *Why:* same<br>**artifact** [SLATE.28](#task-slate-28) — render execution to expose as a capability returning a ProductJobHandle. *Why:* the render capability wraps real render execution |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [DEV.03](device-bridge.md#task-dev-03) — published owner reauthorization (Device.Runtime invoking typed in-process product handlers after grant/resource/revision/egress checks). *Why:* capability execution goes through this exact reauthorization path, per [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39)'s own binding rule that capabilities never bypass owner-side validation |
| Unblocks | [SLATE.40](#task-slate-40) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.AssistantIntegration/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append), [RES-arcslate-registries](../shared-resources.md#res-arcslate-registries) (append) |
| Validation | Descriptor validation, owner-side refusal test, idempotency-per-write-capability test, stability assertion (contract frozen only after semantics stabilised). |
| Completion evidence | Risk/approval-posture declaration coverage; owner-side-validation-always proof. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This is the REAL landing point for [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) (Application Presence and One-Application Tool Bridge), not [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36). [WP-36](../../work-packages/36-arcslate-project-and-timeline.md#rule-wp-36)'s header lists 07/10/13/26 as upstream, but nothing in WP-36.00-36.07's actual scope (project/timeline/media domain model) touches remote application presence or the tool bridge; [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26)'s substeps (ApplicationService, ToolRequest queue, owner reauthorization, remote approval) are about exposing an already-running desktop instance to Cloud-driven remote invocation, which is exactly [WP-39.00](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.00)'s capability-surface scope. |

<a id="task-slate-34"></a>

### SLATE.34 — Bounded context provision

**Outcome.** Context providers expose sequence structure, markers, selected ranges, timecodes and metadata; raw media structurally cannot enter a context payload; oversized context is refused explicitly and visibly.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-34` and ledger record `ledger/tasks/slate-34.md` in the Plan repository; task branch `task/slate-34` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-39.01](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.01) — full |
| Provides | slate.ai-context |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — the timeline structure to project into context. *Why:* context is a read-only structural projection of the timeline model |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.40](#task-slate-40) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.AssistantIntegration/Context/**` |
| Shared resources | [RES-arcslate-registries](../shared-resources.md#res-arcslate-registries) (append) |
| Validation | Structural test asserting media data cannot enter a context payload (type-level, not merely a runtime check); bounding and visibility tests. |
| Completion evidence | Media-cannot-enter-context structural proof; oversized-context-refused result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-35"></a>

### SLATE.35 — Collect, consolidate and the portable project package

**Outcome.** Collect/Consolidate gathers external media into a managed portable form on request, reports exactly what was gathered/skipped and why, never destroys originals; the portable package (project data plus managed media) re-imports with equivalence.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-35` and ledger record `ledger/tasks/slate-35.md` in the Plan repository; task branch `task/slate-35` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-39.02](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.02) — full<br>[WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) Security impact: media path handling, no path leakage through references (§6) — package-level obligation contribution |
| Provides | slate.portable-package |
| Start prerequisites | **artifact** [SLATE.04](#task-slate-04) — the real relink/asset-resolution adapter. *Why:* collect must resolve each asset's current location before copying it<br>**artifact** [SLATE.05](#task-slate-05) — the media library to enumerate. *Why:* collect walks the project's bins/assets<br>**artifact** [PLT.06](platform.md#task-plt-06) — published chunked verifiable large-append store. *Why:* copying large media into a managed portable form is exactly the large-data-copy case that store exists for, with honest truncation semantics on failure |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.42](#task-slate-42) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.ImportExport/CollectConsolidate/**` |
| Validation | Collect with mixed available/offline media, originals-untouched assertion, package round-trip equivalence, large-project performance measurement -- local, once. |
| Completion evidence | Originals-untouched result; round-trip equivalence result; honest skipped-item report. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-36"></a>

### SLATE.36 — Cross-device resolution and relink

**Outcome.** MediaResolutionStrategy resolves per-device asset locations; the relink workflow handles moved/renamed/partially-available media; a project opens with all media offline and relinks without altering any edit decision.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-36` and ledger record `ledger/tasks/slate-36.md` in the Plan repository; task branch `task/slate-36` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-39.03](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.03) — full<br>[WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) Security impact: media path handling, no path leakage through references (§6) — package-level obligation contribution |
| Provides | slate.relink |
| Start prerequisites | **artifact** [SLATE.03](#task-slate-03) — the content-based relink algorithm. *Why:* this task is the workflow/UI wrapper around SLATE.03's verification algorithm, per-device<br>**artifact** [SLATE.04](#task-slate-04) — the real read adapter to re-verify content hash on relink. *Why:* relink verifies bytes before reusing an origin hash, which requires the real probe<br>**artifact** [SLATE.05](#task-slate-05) — the media library. *Why:* relink operates over the library's assets |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.40](#task-slate-40) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.Application/Relink/**` |
| Shared resources | [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append) |
| Validation | Open-with-all-offline test, relink-after-path-change test, partial-relink test, edit-decisions-survive-every-relink-path test. |
| Completion evidence | Offline-open-and-full-relink result; edit-decision-preservation proof. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-37"></a>

### SLATE.37 — Cloud sync scope declaration

**Outcome.** Project data/sequences/markers/presets/metadata sync by default; heavyweight media follows an explicit escalation policy, never swept in by enabling sync; derived data (proxies/caches/analysis) never syncs as authority; big media never traverses the application runtime.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-37` and ledger record `ledger/tasks/slate-37.md` in the Plan repository; task branch `task/slate-37` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-39.04](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.04) — all work except the parts mapped to SLATE.42 |
| Provides | slate.sync-scope |
| Start prerequisites | **artifact** [SLATE.10](#task-slate-10) — the project store to declare a sync scope over. *Why:* sync scope is a policy over what the store already persists<br>**contract** [CON.09](contracts.md#task-con-09) — published SyncService/ResourceService records for project-metadata sync scopes. *Why:* the sync scope declaration uses the generated sync records; real convergence is proven by the integration task |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SLATE.42](#task-slate-42) — real multi-device project convergence against the deployed Cloud sync engine. *Why:* this task's own scope is the ArcSlate-side scope declaration and exclusion rules; 'projects converge across devices' can only be proven against the real [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) Cloud store, not a fixture |
| Unblocks | [SLATE.42](#task-slate-42) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.CloudClient/**` |
| Shared resources | [RES-arcslate-migrations](../shared-resources.md#res-arcslate-migrations) (append) |
| Validation | Enable-sync test asserting no heavyweight media transferred implicitly; derived-data-exclusion assertion; application-service-no-body assertion (the app runtime itself never carries big media) -- local, once, against [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25)'s real environment where available. |
| Completion evidence | No-implicit-heavy-media-transfer result; derived-data-never-syncs-as-authority result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-38"></a>

### SLATE.38 — OTIO interchange: import

**Outcome.** Importing a real.otio file (through the pinned official library, behind the narrow C ABI, no adapters/plug-ins/executable content) decodes each finite double via its exact binary rational, normalises only within one ULP of a declared standard rate, stages the result with a fidelity report the user reviews or cancels, and never silently drops timeline structure.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-38` and ledger record `ledger/tasks/slate-38.md` in the Plan repository; task branch `task/slate-38` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L · early risk proof |
| Obligations | [WP-39.05](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) — import direction: [OB-01](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-01)..[OB-05](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-05) numeric boundary, staged-before-commit import creating ArcSlate-owned canonical objects with provenance, item-level retained/approximated/omitted dispositions, media relink for Offline Media<br>[WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) Completion gate item 6: every claimed interchange version has a fixture and states fidelity before writing -- satisfies [PG-07](../../../assurance/open-gates-register.md#rule-pg-07) for ArcSlate (§8) — package-level obligation contribution |
| Provides | slate.otio.import |
| Start prerequisites | **artifact** [SLATE.06](#task-slate-06) — the timeline structural model import populates. *Why:* import creates ArcSlate-owned canonical objects in this model<br>**artifact** [SLATE.01](#task-slate-01) — the canonical tick domain the [OB-01](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-01)..05 numeric boundary converts into. *Why:* the entire point of the OTIO numeric boundary is converting external doubles into the same canonical ticks everything else in the product already uses<br>**artifact** [NAT.06](native.md#task-nat-06) — the common ABI layer. *Why:* arc_otio_read is declared against it<br>**artifact** [NAT.12](native.md#task-nat-12) — published arc_otio_read export (official OTIO0.18.1 read/upgrade under the schema allowlist). *Why:* real OTIO parsing needs the actual pinned-library wrapper; DesktopPlatform's OtioAbi.cs today is the same 33-line version/build/error probe triad as Media/Colour |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.39](#task-slate-39) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.ImportExport/Otio/Import/**` |
| Shared resources | [RES-arcslate-build-config](../shared-resources.md#res-arcslate-build-config) (append), [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Finite/nonfinite/large/fractional-value vectors, standard-30000/1001-vs-decimal-29.97 vector, metadata-stripped-external-file vector -- against real fixtures and the pinned official library, local, once. |
| Completion evidence | Per-vector numeric-boundary results; no-silent-frame-shift proof; malicious-path-denied and malformed-input-rejected-before-commit results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [OB-01](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-01)..[OB-05](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-05)'s exact-binary-rational-decode-then-normalise-only-within-one-ULP rule is intricate and gates [PG-15](../../../assurance/open-gates-register.md#rule-pg-15)/[PG-20](../../../assurance/open-gates-register.md#rule-pg-20)/[PG-03](../../../assurance/open-gates-register.md#rule-pg-03) simultaneously. A narrow numeric-adapter proof (the finite/NaN/overflow/ULP vectors alone, before building the full staged-import/fidelity-report UI) is worth doing first, since a wrong approach here invalidates broad downstream evidence, matching the same class of risk the design doc's own worked example (23-simulator-and-interchange.md §3.10) calls out. |

<a id="task-slate-39"></a>

### SLATE.39 — OTIO interchange: export

**Outcome.** Export binds a committed sequence revision (reusing the same immutable-snapshot pattern as render), writes to a temporary destination, and publishes atomically after validation; failure/cancellation leaves the project and any existing destination untouched; reports exclude unselected absolute paths and secrets.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-39` and ledger record `ledger/tasks/slate-39.md` in the Plan repository; task branch `task/slate-39` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-39.05](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) — export direction: binds a committed sequence revision, writes a temporary destination and publishes atomically, item-level dispositions for everything outside the supported subset<br>[WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) Completion gate item 6: every claimed interchange version has a fixture and states fidelity before writing -- satisfies [PG-07](../../../assurance/open-gates-register.md#rule-pg-07) for ArcSlate (§8) — package-level obligation contribution |
| Provides | slate.otio.export |
| Start prerequisites | **artifact** [SLATE.38](#task-slate-38) — the shared [OB-01](../../../architecture/07-sync-conflict-and-backup.md#rule-ob-01)..05 numeric adapter and FidelityEntry plumbing. *Why:* export reuses the same numeric boundary and fidelity-report machinery import already built, rather than a second implementation<br>**artifact** [SLATE.26](#task-slate-26) — the committed-revision-snapshot pattern. *Why:* [OA-02](../../../architecture/13-observability-and-operations.md#rule-oa-02)/[OT-04](../../../requirements/products/arcslate.md#rule-ot-04) require export to bind a committed sequence revision the same way render does<br>**artifact** [NAT.12](native.md#task-nat-12) — published arc_otio_write export. *Why:* real OTIO writing needs the actual pinned-library wrapper |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.40](#task-slate-40) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate.ImportExport/Otio/Export/**` |
| Shared resources | [RES-arcslate-golden-media](../shared-resources.md#res-arcslate-golden-media) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Mixed/fractional-rate round trip, gaps/stack ordering, repeated-media-retains-placement, missing-references-become-relinkable-Offline-Media, supported-dissolves/markers, unsupported-feature-reports, export-cancellation-leaves-project-untouched -- against real fixtures and the pinned official library, local, once. |
| Completion evidence | Both-directions-against-real-fixtures result (paired with SLATE.38); semantic-round-trip (meaning/references, not bytes/internal-IDs) result; cancellation-leaves-nothing-touched result. Together with SLATE.38, satisfies [PG-15](../../../assurance/open-gates-register.md#rule-pg-15), contributes to [PG-20](../../../assurance/open-gates-register.md#rule-pg-20) and [PG-03](../../../assurance/open-gates-register.md#rule-pg-03) (OTIO bridge licence/provenance), and [PG-07](../../../assurance/open-gates-register.md#rule-pg-07) for ArcSlate. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-40"></a>

### SLATE.40 — Closure: owned-artifact and real-integration receipt

**Outcome.** OTIO round-trip/projection and relocation fixtures, the package boundary, explicit R2 upload and missing-external-reference behaviour are all recorded with real artifacts and provider identity; the receipt confirms no DTO version-skew can truncate a native project before sync.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/slate-40` and ledger record `ledger/tasks/slate-40.md` in the Plan repository; task branch `task/slate-40` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-39.90](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.90) — full<br>[WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) Unlabelled final-review closure: Cloud data-model round-trip of complete Slate metadata/archive, managed asset uploads, exact grids, graph scopes, fonts/colour, ASR references, anti-truncation — the unlabelled final-review closure paragraph: Cloud data-model round-trip of complete Slate metadata/archive with originals absent, explicit managed asset uploads, exact grids, graph scopes, titles/subtitles/fonts/colour and ASR source/artifact references; an older DTO cannot truncate the native project before sync; package-level obligation contribution |
| Provides | slate.wp39.closure |
| Start prerequisites | **artifact** [SLATE.33](#task-slate-33) — all [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) tasks complete. *Why:* consolidated evidence pass<br>**artifact** [SLATE.39](#task-slate-39) — all [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) tasks complete. *Why:* same<br>**artifact** [SLATE.34](#task-slate-34) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SLATE.36](#task-slate-36) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SLATE.42](#task-slate-42) — real Cloud replica round-trip of complete Slate project metadata/archive against [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25)'s deployed store. *Why:* the final-review closure text requires this proven against the real Cloud data model, not a fixture |
| Unblocks | [REL.03](release.md#task-rel-03) |
| Write scope | `ArcSlate:docs/evidence/wp39-90-receipt.md` |
| Validation | Consolidated re-run of SLATE.33-39's suites plus the real Cloud round-trip, local/available-environment, once. |
| Completion evidence | The consolidated receipt; DTO-version-skew-cannot-truncate-project proof. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-slate-42"></a>

### SLATE.42 — Real multi-device ArcSlate project convergence against the deployed Cloud sync engine

**Outcome.** Two devices editing/opening the same ArcSlate project through the real Cloud sync engine converge correctly, with heavyweight media never implicitly transferred and derived data never syncing as authority.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate`; also touches Cloud |
| Claim, branch and ledger | `claims/slate-42` and ledger record `ledger/tasks/slate-42.md` in the Plan repository; task branch `task/slate-42` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-39.04](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.04) — testing requirement: 'multi-device project convergence'<br>[WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) unlabelled final-review closure paragraph (01-cloud-data-model.md structural-move-and-complete-media-replica-constraints) — unlabelled final-review closure paragraph (01-cloud-data-model.md structural-move-and-complete-media-replica-constraints) |
| Start prerequisites | **artifact** [SLATE.37](#task-slate-37) — real, delivered outcome of SLATE.37 (Cloud sync scope declaration). *Why:* this integration exercises the real cloud sync scope declaration instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.39](cloud.md#task-cloud-39) — real, delivered outcome of CLOUD.39 (Guarded publication and convergent bootstrap). *Why:* this integration exercises the real guarded publication and convergent bootstrap instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.44](cloud.md#task-cloud-44) — real, delivered outcome of CLOUD.44 (Multi-device convergence harness). *Why:* this integration exercises the real multi-device convergence harness instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SLATE.12](#task-slate-12) — real, delivered outcome of SLATE.12 (Slate.project.v1/graph.v1 wire projection: bins, generators, nesting, adjustment, title/subtitle, cycle rejection). *Why:* this integration exercises the real slate.project.v1/graph.v1 wire projection: bins, generators, nesting, adjustment, title/subtitle, cycle rejection instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SLATE.35](#task-slate-35) — real, delivered outcome of SLATE.35 (Collect, consolidate and the portable project package). *Why:* this integration exercises the real collect, consolidate and the portable project package instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.06.arcslate](adoption.md#task-adopt-06-arcslate) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SLATE.37](#task-slate-37), [SLATE.40](#task-slate-40) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Two devices editing/opening the same ArcSlate project through the real Cloud sync engine converge correctly, with heavyweight media never implicitly transferred and derived data never syncing as authority. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as SLATE.43. |
