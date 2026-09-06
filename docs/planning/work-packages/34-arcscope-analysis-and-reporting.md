# WP-34 — ArcScope Visualisation, Analysis and Reporting

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: H — ArcScope
> Upstream: `33` · Downstream: `35`

> **Goal.** Turn evidence into findings without ever altering the evidence: visualisation, triggers, measurements, decoders, analysis, annotations, comparison and reports — every result reproducible from a recorded configuration.

---

## 1. Scope and purpose

**In scope.** Visualisation with downsampling and saved analysis views; triggers with pre- and post-trigger windows; measurements; protocol and format decoders; analysis definitions and recipes; annotations and findings; session and capture comparison; and report generation with full source traceability.

**Out of scope.** Device control, which remains a later, higher-permission capability class. Cloud sync and ArcChat integration (`35`).

**Why this package exists.** `I2 §III.9` places visualisation, triggers, measurement, decoding, analysis, annotation, comparison and reporting after the evidence layer, so that every interpretation is anchored to immutable evidence and a recorded configuration.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) | Visualisation, triggers, decoders, analysis, comparison and reporting requirements |
| `WP-33` output | Sessions, captures, the time model and effective configuration snapshots — **including the file/replay adapter, which is this package's repeatable source** (`SD-09`) |
| — | **The Cloud simulator (`WP-51`) is not required here.** Reproducibility is verified against replay of a recorded capture; the simulator adds a second synthetic source later and closes `PG-14b`, which is an ArcScope *Cloud-simulation* claim, not an analysis claim |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) | Responsiveness and scale budgets for visualisation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A trigger never modifies data.** It controls capture and marks time; samples are unchanged. |
| BR-02 | **A decoder interprets data; it never commands hardware.** |
| BR-03 | **Decoder errors are displayed, not silently dropped**: malformed frames, checksum failures and unknown fields are visible with counts and locations. |
| BR-04 | **Analysis output is derived data**, fully reconstructable from evidence plus a recorded configuration. |
| BR-05 | **Reproducibility is a core product value**: a result is reconstructable from session, capture, configuration snapshot, decoder version and configuration, analysis definition and version, alignment and calibration version. |
| BR-06 | **A saved analysis view is work content; panel layout is device-local.** |
| BR-07 | **A report traces every source** back to session, capture, time range, configuration snapshot and analysis version. |
| BR-08 | **Visualisation downsampling never changes the underlying data**, and the display states when it is showing a downsampled view. |
| BR-09 | **An annotation or finding is authored content** with its own identity and history; it is never written into raw capture. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcScope/ArcScope.Visualization/` | Plots, downsampling, cursors, markers, saved analysis views |
| `src/ArcScope/ArcScope.Analysis/` | Measurements, analysis definitions, recipes, comparison |
| `src/ArcScope/ArcScope.Decoders/` | Decoder framework and first-party decoders |
| `src/ArcScope/ArcScope.Reporting/` | Report composition, templates and export |
| `src/ArcScope/ArcScope.Domain/` | Trigger, measurement, analysis result, annotation, finding, report |
| `tests/ArcScopePipelineTests/` | Trigger, decoder, analysis, reproducibility and comparison suites |

**Major types introduced.** `Trigger`, `TriggerWindow`, `Measurement`, `MeasurementResult`, `Decoder`, `DecoderConfiguration`, `DecodedFrame`, `AnalysisDefinition`, `AnalysisResult`, `Recipe`, `Annotation`, `Finding`, `Comparison`, `Report`, `SavedAnalysisView`.

---

## 5. Required implementation work

### WP-34.00 — Visualisation

**What must be fully done.** Time-series and event visualisation with virtualised rendering and downsampling that keeps interaction responsive at corpus scale. Cursors, markers, zoom and pan. The display states explicitly when it is showing a downsampled representation.

**Testing requirements.** Scale corpus interaction measurements; a downsampling-disclosure assertion; a correctness test comparing downsampled and full-resolution readings at a cursor.

**Completion gate.** Visualisation meets responsiveness budget at corpus scale, discloses downsampling, and cursor readings are exact regardless of display resolution.

### WP-34.01 — Triggers

**What must be fully done.** Triggers controlling capture and marking significant time events, with pre- and post-trigger windows served by the rolling buffer. A trigger never modifies samples.

**Testing requirements.** Pre- and post-window correctness; a data-immutability assertion; a trigger-storm bound test.

**Completion gate.** Trigger windows are exact, samples are provably unmodified, and trigger storms are bounded.

### WP-34.02 — Measurements

**What must be fully done.** A measurement set over signals and events with units, precision and uncertainty stated. A measurement records the configuration under which it was taken so it can be reproduced.

**Testing requirements.** Reference-value tests per measurement kind; a unit-handling test; a reproduction test from recorded configuration.

**Completion gate.** Every measurement reproduces exactly from its recorded configuration, with units and precision stated.

### WP-34.03 — Decoders

**What must be fully done.** A decoder framework with versioned decoder definitions and configurations. Decoder output is structured events, not raw channel data. Errors — malformed frames, checksum failures, unknown fields — are surfaced with counts and locations. A decoder cannot write to a device.

**Testing requirements.** Per-decoder fixture corpora including malformed input; an error-visibility assertion; a structural test asserting no device write path exists from a decoder.

**Completion gate.** Decoders produce structured events, surface every error class with counts and locations, and structurally cannot command hardware.

### WP-34.04 — Analysis and recipes

**What must be fully done.** Versioned analysis definitions composable into recipes. Results are derived data, reconstructable from evidence plus configuration. Long analyses run as Tasks under the execution engine with progress and cancellation.

**Testing requirements.** Reconstruction tests deleting all results and rebuilding; long-analysis cancellation; a version-change test asserting historical results record their definition version.

**Completion gate.** Deleting every analysis result and rebuilding produces identical output, and historical results record their definition version.

### WP-34.05 — Annotations, findings and comparison

**What must be fully done.** Annotations and findings as authored content with identity and history, never written into raw capture. Session-to-session and capture-to-capture comparison with alignment stated explicitly.

**Testing requirements.** A structural test asserting raw capture is untouched by annotation; comparison correctness with deliberate misalignment; history tests on findings.

**Completion gate.** Raw capture is provably untouched by authoring, and comparison states its alignment explicitly.

### WP-34.06 — Reports and reproducibility

**What must be fully done.** Report composition from analyses, measurements, findings and visualisations, exported to a portable form. Every element traces to session, capture, time range, configuration snapshot, decoder version and analysis version. A reproducibility check regenerates a report's results from its recorded sources.

**Testing requirements.** A traceability completeness test; a regeneration test producing equivalent results; an export fidelity check.

**Completion gate.** **Every report element traces to its sources, and regenerating from those sources produces equivalent results.**

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Analysis results, annotations, findings and reports as separate stores from raw capture |
| Protocol | Analysis and reporting capabilities become registrable |
| UI | Visualisation, analysis, annotation, comparison and report surfaces |
| Security | Analysis never grants device access; reports carry no more than their sources allow |
| Platform | Rendering performance per platform |
| Migration | Analysis and report schema versioning |
| Compatibility | Decoder and analysis versions recorded on every result |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Scale responsiveness, downsampling disclosure and cursor exactness | `WP-34.00` |
| Trigger window, immutability and storm-bound results | `WP-34.01` |
| Measurement reference and reproduction results | `WP-34.02` |
| Per-decoder fixtures, error visibility and no-write assertion | `WP-34.03` |
| Result reconstruction and version-recording results | `WP-34.04` |
| Raw-capture immutability and comparison alignment results | `WP-34.05` |
| Traceability completeness and regeneration equivalence | `WP-34.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Visualisation meets responsiveness budget at corpus scale, discloses downsampling, and cursor readings are exact.
2. Trigger windows are exact; samples are provably unmodified; trigger storms are bounded.
3. Every measurement reproduces exactly from its recorded configuration with units and precision stated.
4. Decoders produce structured events, surface every error class with counts and locations, and structurally cannot command hardware.
5. Deleting every analysis result and rebuilding produces identical output; historical results record their definition version.
6. Raw capture is provably untouched by annotation and finding authoring; comparison states its alignment.
7. **Every report element traces to session, capture, time range, configuration snapshot, decoder version and analysis version, and regeneration produces equivalent results.**

---

## 9. Dependencies

**Upstream.** `33` (evidence, sessions and the time model).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `35` — Integration | Analysis results and reports as the sync and AI-context payload |
