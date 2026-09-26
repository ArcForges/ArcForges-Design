<a id="rule-wp-36"></a>

# WP-36 — ArcSlate Project, Timeline and Media Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: I — ArcSlate
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Build ArcSlate's domain: project and sequences, the exact time model spanning video frames and audio samples, the media library with assets referenced rather than owned, the timeline with tracks and clips, and non-destructive editing — all in C#, with no native type anywhere near the domain.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcSlate. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Project and sequence model; the exact timebase; media assets, streams, availability and metadata; the media library with bins; the timeline with tracks, items, clips and transitions; non-destructive editing operations; undo and project checkpoints; and project persistence with recovery.

**Out of scope.** Playback and processing runtime (`37`); render, export and colour management (`38`); integration and portability (`39`).

**Why this package exists.** [the current dependency model](../implementation-sequence.md#2-phase-structure) places ArcSlate last because it carries the highest complexity and performance risk — and requires it to follow the phase order strictly. The domain must be exact before any runtime touches it, because a timebase error discovered during rendering is a rewrite.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md) | The full product model, domain concepts and V1 scope |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) `§7` | The media pipeline boundary and the domain-purity rules |
| [WP-13.03](13-high-risk-technical-probes.md#rule-wp-13.03) output | Decode, synchronisation and native safety probe conclusions |
| [`../../assurance/reference-coverage/arcslate-arcvideo.md`](../../assurance/reference-coverage/arcslate-arcvideo.md) | **The completed ArcSlate Reference Coverage Matrix** — 31 rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, oracle and owner |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix method and the ten-field provenance record that governs any future reuse |
| [WP-07](07-local-persistence-foundation.md#rule-wp-07), [WP-10](10-design-system-and-desktop-shell.md#rule-wp-10), [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26) output | Persistence, shell and remote task participation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **The ArcSlate Reference Coverage Matrix is a completed, versioned planning input** — [`../../assurance/reference-coverage/arcslate-arcvideo.md`](../../assurance/reference-coverage/arcslate-arcvideo.md), 31 item-level rows, bound to ArcVideo at `caf5651` and ArcVideoFoundation at `139eeca` — ArcSlate's complete reference set under **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)** as amended ([P2-005](../../decisions/phase-2-specification-decisions.md#rule-p2-005)). It was produced before this plan was derived (**[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)**). **This package consumes it and checks it for drift; it does not create it.** |
| <a id="rule-br-02"></a>BR-02 | **ArcSlate is not a technical exception.** Its architecture is C#, Avalonia and Native AOT with P/Invoke to native media libraries. It is not a Qt application, not a C++ product with a C# shell, and not a C++ worker. |
| <a id="rule-br-03"></a>BR-03 | **Editing is non-destructive.** Source media is never modified. |
| <a id="rule-br-04"></a>BR-04 | **`Project ≠ Sequence`** and **`Project ≠ media folder`** ([I-476](../../requirements/01-normative-glossary-and-invariants.md#rule-i-476)). |
| <a id="rule-br-05"></a>BR-05 | **`MediaAsset ≠ File`** ([I-477](../../requirements/01-normative-glossary-and-invariants.md#rule-i-477)), and an asset identifier is never a file path ([I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)). |
| <a id="rule-br-06"></a>BR-06 | **Video frame precision and audio sample precision coexist** ([I-478](../../requirements/01-normative-glossary-and-invariants.md#rule-i-478)), each exact in its own rate domain with explicit conversion. |
| <a id="rule-br-07"></a>BR-07 | **Sequence frame rate is rational**; drop-frame and non-integer rates are exact, never approximated. |
| <a id="rule-br-08"></a>BR-08 | **Offline media is a normal product state, not an error** ([I-481](../../requirements/01-normative-glossary-and-invariants.md#rule-i-481)). The project opens, structure is preserved, edit decisions are retained. |
| <a id="rule-br-09"></a>BR-09 | **A clip must not know which physical file is in use.** It references the asset; the asset resolves at runtime. |
| <a id="rule-br-10"></a>BR-10 | **No native type, handle, enumeration or error code appears in a domain, contract or persisted type.** |
| <a id="rule-br-11"></a>BR-11 | **The same asset may have different locations on different devices** and remains one logical asset. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

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

<a id="rule-wp-36.00"></a>

### WP-36.00 — Project and sequence model

**What must be fully done.** A project as a long-term editing container holding multiple sequences that share one media library. A sequence is a playable, renderable composition with its own timeline and output parameters. Project and sequence have distinct identities and lifecycles.

**Testing requirements.** Multi-sequence project tests; a shared-library assertion; a distinction test against the media folder concept.

**Completion gate.** A project holds multiple sequences over one media library, with project, sequence and folder structurally distinct.

<a id="rule-wp-36.01"></a>

### WP-36.01 — The exact time model

**What must be fully done.** Implement705600000tick time, exact source rational/grid mapping and sequence interval algebra under architecture 23/26. Use source-PTS ingress, output frame/sample projection, display and interchange conversion boundaries exactly; no blanket four-rounding-site rule.

**Testing requirements.** Independent NTSC/audio/negative/source-inexact/ties-even/half-open and overflow vectors; no intermediate double owner arithmetic.

**Completion gate.** All conversions use their declared profile and no competing rounding authority.

<a id="rule-wp-36.02"></a>

### WP-36.02 — Media assets and availability

**Required design implementation and verification.** Media assets and derived outputs preserve origin on import, relink, proxy, edit and native revision history. A relink verifies bytes before reusing an origin hash; missing imported metadata remains unknown. Test known AI and non-AI assets in the same project without modifying originals.

**What must be fully done.** Deliver the real metadata/read adapter needed here using the approved owned ABI and ContentSandbox; [WP-37](37-arcslate-playback-and-processing.md#rule-wp-37) extends playback rather than being an undeclared prerequisite for this step.  Media assets with stable logical identity, typed metadata (streams, codecs, dimensions, rate, duration, colour metadata, timecode, channel layout) and an explicit availability state. Assets are referenced externally by default with managed copies as an explicit choice. Offline media is a normal state.

**Testing requirements.** Malformed metadata and child crash preserve the native project.  Offline-open test asserting structure and edit decisions survive; relink tests; a per-device location test asserting one logical asset; a structural test asserting no native type is present in the metadata model.

**Completion gate.** Media metadata is real and isolated at this package, with no later runtime assumed.  A project opens fully with all media offline, relinks correctly, and no native type appears in the domain.

<a id="rule-wp-36.03"></a>

### WP-36.03 — Media library

**What must be fully done.** Bins organising assets, with import defaulting to reference-in-place, background analysis after import, and import completing without waiting for all caches. A media indexing failure is not an import failure.

**Testing requirements.** Import completion timing; a failed-indexing test asserting the asset still exists; a large-library performance test.

**Completion gate.** Import completes without waiting on caches, and an indexing failure never fails the import.

<a id="rule-wp-36.04"></a>

### WP-36.04 — Timeline and tracks

**What must be fully done.** Tracks with roles, timeline items, clips referencing assets with in and out points, and transitions. One asset supports many independent clip instances. Track ordering, enabling, locking and soloing.

**Testing requirements.** Many-clips-one-asset independence; track operation coverage; a structural test asserting a clip holds no file path.

**Completion gate.** Many clips reference one asset independently, and no clip holds a file path.

<a id="rule-wp-36.05"></a>

### WP-36.05 — Editing operations

**What must be fully done.** Implement every [TL-06](../../requirements/products/arcslate.md#rule-tl-06) operation using TimelineCommand and slate.edits.v1: links/locks, ripple/roll/slip/slide/split/overwrite/group/duplicate/retime/markers/track state with fixed affected sets and one undo transaction.

**Testing requirements.** Independent operation examples, collision/source handles, reverse/freeze retime, linked-track refusal and undo/restart vectors from 26.

**Completion gate.** All accepted edit operations complete, not only low-level insert/remove/replace.

<a id="rule-wp-36.06"></a>

### WP-36.06 — Undo, checkpoints and recovery

**What must be fully done.** Undo with composite operation grouping; project checkpoints as an explicit user mechanism distinct from undo; crash recovery to the last committed boundary with explicit loss reporting; migration from prior project versions with semantic preservation.

**Testing requirements.** Undo across composite operations; a distinction test between undo, checkpoint and recovery; kill-during-edit recovery; migration semantic comparison.

**Completion gate.** Undo, checkpoint and recovery behave as three distinct mechanisms, and a crash recovers to a committed boundary with honest loss reporting.

<a id="rule-wp-36.07"></a>

### WP-36.07 — Reference drift check

> **Not a baseline audit.** The ArcSlate matrix is complete and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. This sub-step is **maintenance**, and it is the producer of the drift check the package gate requires.

**What must be fully done.** The reference is compared against its bound commit — ArcVideo at `caf5651` and ArcVideoFoundation at `139eeca`. Three outputs are produced:

1. **Changed material**: any file behind a matrix row that changed since the bound commit, with the row re-assessed.
2. **Newly introduced material**: capabilities added upstream since the bound commit, each assessed against the accepted ArcSlate scope. **A new upstream capability does not become an ArcForges requirement by appearing** — it is mapped to an existing requirement or recorded as an accepted exclusion.
3. **Licence re-verification**: the reference's licence files are re-read. A subtree licence can change upstream, and the disposition of every row depends on it.

**Testing requirements.** A drift report listing changed rows, new material with its assessment, and the licence comparison. A completeness check that every changed or new item has a disposition.

**Completion gate.** The drift report exists, every changed and newly introduced item carries a disposition, and the licence position is re-confirmed or amended with a reason. **If the licence position changed, the affected rows' dispositions are corrected before any dependent work continues** (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**).

---

**Required implementation and closure from the final review.** Implement and independently verify [23-simulator-and-interchange](../../architecture/23-simulator-and-interchange.md#5-slate-metadata-render-and-subtitle-profiles). Implement the complete slate.project.v1/graph.v1 model: bins, exact sequence video/audio/colour config, track roles, generators/nesting/adjustment/title/subtitle, graph definition/instance identity and keyframe time scope. Metadata-only cross-device round-trip preserves every edit with Offline Media. Reject graph/nesting cycles and preserve unknown imported effects inert. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-36.90"></a>
### WP-36.90 — Verify the owned artifact and real integration

**What must be fully done.** Keep C# domain, project/timeline/edit/undo and local recovery. Use exact media/rational profiles and native-resource package interfaces without importing another product's domain.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Exact timeline/edit/recovery fixtures remain valid; package and wire boundaries do not round frame/time values.

**Completion gate.** Exact timeline/edit/recovery fixtures remain valid; package and wire boundaries do not round frame/time values. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**Required evidence addition.** [WP-36.02](#rule-wp-36.02) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Multi-sequence and structural distinction results | [WP-36.00](#rule-wp-36.00) |
| Tick-base exactness per supported rate, long-sequence drift, and **within-grid** position→grid→position round-trip results — **not** a frame↔sample round-trip, which the grids make impossible | [WP-36.01](#rule-wp-36.01) |
| Offline-open, relink and no-native-type results | [WP-36.02](#rule-wp-36.02) |
| Import timing and indexing-failure results | [WP-36.03](#rule-wp-36.03) |
| Many-clips-one-asset and no-path results | [WP-36.04](#rule-wp-36.04) |
| Per-operation exactness and non-destructiveness results | [WP-36.05](#rule-wp-36.05) |
| Three-mechanism distinction and recovery results | [WP-36.06](#rule-wp-36.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-36.90](#rule-wp-36.90) |



---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-36.90](#rule-wp-36.90) and all inherited domain-specific gates must pass on the same candidate closure. Exact timeline/edit/recovery fixtures remain valid; package and wire boundaries do not round frame/time values.

**[PG-20](../../assurance/open-gates-register.md#rule-pg-20) evidence:** [WP-36.01](#rule-wp-36.01) — Exact supported grids and adjacent sample ownership; combine with real audio and OTIO boundary evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. **Drift check only**: the reference is compared against its bound commit, and any newly introduced material is assessed against the accepted ArcSlate scope. The matrix and its licence audit were completed as design-stage evidence and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. Findings carried in: **[F-AL-2](../../assurance/reference-coverage/arcslate-arcvideo.md#rule-f-al-2)** records that ArcVideoFoundation is a **thin utility layer of 27 files**, not the “fat core” its README describes — so no substantial reusable core exists. **[P2-005](../../decisions/phase-2-specification-decisions.md#rule-p2-005)** fixes the reference baseline as **ArcVideo and ArcVideoFoundation**; no upstream checkout is sought, and **upstream provenance is preserved** ([RF-06](../../requirements/products/arcslate.md#rule-rf-06) in the ArcSlate requirements).
2. A project holds multiple sequences over one media library, with project, sequence and folder structurally distinct.
3. **No drift accumulates over long durations in any supported rate**; frame↔tick and sample↔tick round-trip exactly on their own grids; an adjacent cut emits every boundary sample exactly once. Frame↔sample round-tripping is **not** claimed ([TG-02](../../architecture/23-simulator-and-interchange.md#rule-tg-02)).
4. A project opens fully with all media offline and relinks correctly; **no native type appears anywhere in the domain, contracts or persisted types**.
5. Import completes without waiting on caches; an indexing failure never fails an import.
6. Many clips reference one asset independently; no clip holds a file path.
7. Every edit operation is **exact on its own grid** — video edits frame-precise, audio edits sample-precise ([TG-03](../../architecture/23-simulator-and-interchange.md#rule-tg-03)) — non-destructive, and routed through the single write path.
8. Undo, checkpoint and recovery are three distinct mechanisms, and a crash recovers to a committed boundary with honest loss reporting.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [SLATE.01](../delivery/lanes/arcslate.md#task-slate-01) | [WP-36.01](36-arcslate-project-and-timeline.md#rule-wp-36.01) (full) | none |
| [SLATE.02](../delivery/lanes/arcslate.md#task-slate-02) | [WP-36.00](36-arcslate-project-and-timeline.md#rule-wp-36.00) (full) | none |
| [SLATE.03](../delivery/lanes/arcslate.md#task-slate-03) | [WP-36.02](36-arcslate-project-and-timeline.md#rule-wp-36.02) (domain types (MediaAsset/MediaStream/MediaMetadata/MediaAvailability) and the relink-by-content-hash algorithm; excludes the real native read/probe adapter) | none |
| [SLATE.04](../delivery/lanes/arcslate.md#task-slate-04) | [WP-36.02](36-arcslate-project-and-timeline.md#rule-wp-36.02) (the real metadata/read adapter using the approved owned ABI and ContentSandbox, and the content-origin carrier/propagation/failure vectors recorded in this substep's evidence row)<br>[WP-36](36-arcslate-project-and-timeline.md#rule-wp-36) Content-origin carrier/propagation/failure vectors ([WP-36.02](36-arcslate-project-and-timeline.md#rule-wp-36.02) required evidence addition; §8 additional completion requirement) (package-level obligation contribution) | [NAT.07](../delivery/lanes/native.md#task-nat-07) (artifact) |
| [SLATE.05](../delivery/lanes/arcslate.md#task-slate-05) | [WP-36.03](36-arcslate-project-and-timeline.md#rule-wp-36.03) (full) | none |
| [SLATE.06](../delivery/lanes/arcslate.md#task-slate-06) | [WP-36.04](36-arcslate-project-and-timeline.md#rule-wp-36.04) (full) | none |
| [SLATE.07](../delivery/lanes/arcslate.md#task-slate-07) | [WP-36.05](36-arcslate-project-and-timeline.md#rule-wp-36.05) (the shared validate->expand-affected-set->one-transaction command pipeline, plus Insert/Overwrite/Move/Trim(in/out)/Split/Delete/Lift/RippleDelete/Extract/Duplicate exactly per slate.edit.v1 (26-product-behavior-profiles.md §4)) | none |
| [SLATE.08](../delivery/lanes/arcslate.md#task-slate-08) | [WP-36.05](36-arcslate-project-and-timeline.md#rule-wp-36.05) (RippleTrim/Roll/Slip/Slide/Group-Ungroup/Link-Unlink/Enable-Disable/ReorderTracks/Transition(create-delete)/Snap/Retime+RetimeCurve/ripple-marker-scope exactly per slate.edit.v1) | none |
| [SLATE.09](../delivery/lanes/arcslate.md#task-slate-09) | [WP-36.06](36-arcslate-project-and-timeline.md#rule-wp-36.06) (undo/redo as a distinct mechanism from checkpoint/recovery: composite operation grouping, explicit commit-boundary (a transient drag/preview is never a committed command)) | none |
| [SLATE.10](../delivery/lanes/arcslate.md#task-slate-10) | [WP-36](36-arcslate-project-and-timeline.md#rule-wp-36) Database impact: ArcSlate project store and its V1 migration baseline (§6) (package-level: §6 Impacts row "Database: the ArcSlate project store and its V1 migration baseline"; §4 ArcSlate.Infrastructure project store/media index/migration set; package-level obligation contribution) | [PLT.01](../delivery/lanes/platform.md#task-plt-01) (artifact), [PLT.04](../delivery/lanes/platform.md#task-plt-04) (artifact) |
| [SLATE.11](../delivery/lanes/arcslate.md#task-slate-11) | [WP-36.06](36-arcslate-project-and-timeline.md#rule-wp-36.06) (project checkpoints as an explicit user mechanism distinct from undo; crash recovery to the last committed boundary with explicit loss reporting; migration from prior project versions with semantic preservation) | [PLT.02](../delivery/lanes/platform.md#task-plt-02) (artifact), [PLT.03](../delivery/lanes/platform.md#task-plt-03) (artifact) |
| [SLATE.12](../delivery/lanes/arcslate.md#task-slate-12) | [WP-36](36-arcslate-project-and-timeline.md#rule-wp-36) Unlabelled final-review closure: complete slate.project.v1/graph.v1 model, generators/nesting/adjustment/title/subtitle, cycle rejection, unknown-effect inert (the unlabelled final-review closure paragraph: "Implement the complete slate.project.v1/graph.v1 model: bins, exact sequence video/audio/colour config, track roles, generators/nesting/adjustment/title/subtitle, graph definition/instance identity and keyframe time scope. Metadata-only cross-device round-trip preserves every edit with Offline Media. Reject graph/nesting cycles and preserve unknown imported effects inert."; package-level obligation contribution) | [CON.06](../delivery/lanes/contracts.md#task-con-06) (contract) |
| [SLATE.13](../delivery/lanes/arcslate.md#task-slate-13) | [WP-36.07](36-arcslate-project-and-timeline.md#rule-wp-36.07) (full) | none |
| [SLATE.14](../delivery/lanes/arcslate.md#task-slate-14) | [WP-36.90](36-arcslate-project-and-timeline.md#rule-wp-36.90) (full) | none |

**Consumers outside this package:** [REL.03](../delivery/lanes/release.md#task-rel-03), [SLATE.15](../delivery/lanes/arcslate.md#task-slate-15), [SLATE.17](../delivery/lanes/arcslate.md#task-slate-17), [SLATE.18](../delivery/lanes/arcslate.md#task-slate-18), [SLATE.20](../delivery/lanes/arcslate.md#task-slate-20), [SLATE.21](../delivery/lanes/arcslate.md#task-slate-21), [SLATE.24](../delivery/lanes/arcslate.md#task-slate-24), [SLATE.26](../delivery/lanes/arcslate.md#task-slate-26), [SLATE.29](../delivery/lanes/arcslate.md#task-slate-29), [SLATE.33](../delivery/lanes/arcslate.md#task-slate-33), [SLATE.34](../delivery/lanes/arcslate.md#task-slate-34), [SLATE.35](../delivery/lanes/arcslate.md#task-slate-35), [SLATE.36](../delivery/lanes/arcslate.md#task-slate-36), [SLATE.37](../delivery/lanes/arcslate.md#task-slate-37), [SLATE.38](../delivery/lanes/arcslate.md#task-slate-38), [SLATE.42](../delivery/lanes/arcslate.md#task-slate-42).

<!-- delivery-graph:end -->

