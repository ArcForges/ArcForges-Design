# WP-33 — ArcScope Acquisition and Session Core

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: H — ArcScope
> Upstream: `07`, `10`, `13`, `26` · Downstream: `34`

> **Goal.** Build the evidence layer: sources and adapters, the acquisition pipeline, sessions and captures with segments and gaps, the channel and event time model, and record and replay — with raw capture treated as evidence, immutable once finalised.

---

## 1. Scope and purpose

**In scope.** Data sources and source adapters over real transports; connection profiles and effective configuration snapshots; the acquisition pipeline with backpressure and overrun reporting; session and capture lifecycle with segments and gaps; the channel, signal and event time model; the rolling buffer and live observation; durable capture writing; and replay as a source.

**Out of scope.** Analysis, measurement, decoding, visualisation and reporting (`34`). Cloud metadata sync and ArcChat integration (`35`). Device control, which is a later, higher-permission capability class.

**Why this package exists.** `I2 §III.9` fixes the order: source and adapter, then acquisition, then session and capture, then the time model, then record and replay. Evidence integrity is established before anything interprets the evidence.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) | The full product model, domain concepts and V1 scope |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) `§8` | The acquisition pipeline architecture and its rules |
| `WP-13.02` output | The throughput, ring buffer and overrun probe conclusions |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The ArcScope Reference Coverage Matrix and licence audit |
| `WP-07`, `WP-10`, `WP-26` output | Persistence, shell and remote task participation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcScope Reference Coverage Matrix and licence audit are complete before this package begins** (`DC-02`). |
| BR-02 | **`Device ≠ DataSource`** (`I-466`). The data source is the real entry point; the device is an optional identity. |
| BR-03 | **`Session ≠ Capture`** (`I-467`) and live observation is separate from capture (`I-469`). |
| BR-04 | **Pausing the view never stops recording** (`I-469`). |
| BR-05 | **Raw capture, once finalised, is immutable.** Raw capture is evidence and the source of truth. |
| BR-06 | **Every session records an effective configuration snapshot** — the settings actually in force. Changing a profile never rewrites a historical session. |
| BR-07 | **An acquisition overrun is surfaced, never hidden**: counted, timestamped and recorded as a gap. |
| BR-08 | **Replay never impersonates a real device** (`I-470`), and its origin is always recorded. |
| BR-09 | **The same source is never silently claimed by two captures**; exclusive access uses lease and busy semantics. |
| BR-10 | **The acquisition loop, capture lifecycle and trigger semantics are C#**; native code supplies transport, device access, timestamps and primitives only. |
| BR-11 | **Raw capture uses the chunked verifiable store**, never database blobs. |
| BR-12 | **A crash mid-capture recovers to the last committed boundary with an honest end marker.** |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcScope/ArcScope.Domain/` | Project, session, capture, segment, gap, channel, signal, event, configuration snapshot |
| `src/ArcScope/ArcScope.Acquisition/` | Source adapters, the acquisition loop, rolling buffer, backpressure, overrun accounting |
| `src/ArcScope/ArcScope.Recording/` | Durable capture writer over the chunked verifiable store |
| `src/ArcScope/ArcScope.Native/` | Transport and device primitives behind the C ABI where required |
| `src/ArcScope/ArcScope.Infrastructure/` | Store schema, capture storage layout, migration set |
| `src/ArcScope/ArcScope.Presentation/`, `.Desktop/` | Session, capture and live observation surfaces |
| `tests/ArcScopePipelineTests/` | Throughput, overrun, gap, recovery and exclusivity suites |

**Major types introduced.** `DataSource`, `SourceAdapter`, `ConnectionProfile`, `Connection`, `EffectiveConfigurationSnapshot`, `Session`, `Capture`, `CaptureSegment`, `Gap`, `Channel`, `Signal`, `EventRecord`, `RollingBuffer`, `AcquisitionStats`, `CaptureWriter`, `ReplaySource`.

---

## 5. Required implementation work

### WP-33.00 — Sources, adapters and profiles

**What must be fully done.** First-party adapters for generic transports — serial, TCP, UDP and file replay — behind one adapter contract. Connection profiles are stored and reusable. Editing a profile never alters a historical session's recorded configuration. Exclusive access uses lease and busy semantics.

**Testing requirements.** Real-transport connect, disconnect and reconnect per adapter; a profile-edit test asserting historical sessions are unchanged; an exclusivity test with two claimants.

**Completion gate.** Every adapter works over a real transport, historical configuration is immutable, and a second claimant is refused with a busy state.

### WP-33.01 — Acquisition pipeline

**What must be fully done.** A bounded, timestamped acquisition loop with explicit backpressure. Hardware timestamps preserved where available, with the timing source and its uncertainty recorded otherwise. Overruns counted, timestamped and recorded. Sustained throughput above the product target with bounded memory.

**Testing requirements.** Sustained-throughput runs with recorded rate, memory and drop counts; induced overrun; timing-source recording assertions.

**Completion gate.** Sustained throughput exceeds target with bounded memory, and every overrun is counted, timestamped and visible.

### WP-33.02 — Session, capture, segments and gaps

**What must be fully done.** The session and capture lifecycle: armed, running, paused, stopped, finalised, and interrupted. Captures are sequences of segments plus explicit gaps. Live observation uses the rolling buffer; record creates persistent capture. Pausing the view never stops recording.

**Testing requirements.** Lifecycle coverage including interruption; a pause-view-while-recording test; a segment-and-gap integrity test after a disconnect.

**Completion gate.** Every lifecycle transition is correct, pausing the view never stops recording, and a disconnect produces an explicit gap rather than a truncated capture.

### WP-33.03 — Time and channel model

**What must be fully done.** A precise time model spanning signal samples and discrete events, with exact rate representation and explicit conversion. Channels and signals are modelled distinctly from events. Alignment between sources is explicit and recorded.

**Testing requirements.** Precision tests across rate domains; an alignment test with two sources; a conversion-exactness test.

**Completion gate.** Time is exact within each domain with explicit conversion, and multi-source alignment is recorded rather than assumed.

### WP-33.04 — Durable capture and immutability

**What must be fully done.** Raw capture written to the chunked verifiable store with per-chunk checksums and an explicit end marker. Once finalised, a capture is immutable. A crash mid-capture recovers to the last committed boundary with an honest end marker and a recorded loss.

**Testing requirements.** Kill-during-capture at chunk boundaries and mid-chunk; verification of the recovered prefix; an immutability test asserting a finalised capture cannot be modified.

**Completion gate.** A crash yields a verifiable prefix with recorded loss, and a finalised capture is structurally immutable.

### WP-33.05 — Replay

**What must be fully done.** Replay as a source adapter feeding the same pipeline, always labelled as replay with its origin recorded. A replay adapter never presents device-only fields as measured.

**Testing requirements.** Replay of a recorded capture producing an equivalent session; a labelling assertion; a negative test asserting device-only fields are absent.

**Completion gate.** Replay produces an equivalent session, is always labelled, and never fabricates device-only fields.

### WP-33.06 — Long-running capture in the shell

**What must be fully done.** Capture as a long-running activity with a permanently visible recording state. Closing a window during capture asks with consequences stated, never silently stopping or silently continuing. Background capture persists only while genuine work is active.

**Testing requirements.** Window-close-during-capture prompts; a background-residency test; a recording-visibility assertion.

**Completion gate.** Recording state is always visible, and closing a window during capture never silently stops or continues it.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The ArcScope schema plus the chunked capture store layout |
| Protocol | Capture and session capabilities become registrable |
| UI | Live observation, session and capture surfaces with recording state |
| Security | Exclusive source access; capture as evidence with integrity |
| Platform | Real transport behaviour and timing per platform |
| Migration | ArcScope schema version 1 and capture format version 1 |
| Compatibility | The capture format enters the compatibility window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Per-adapter real-transport results, profile immutability, exclusivity | `WP-33.00` |
| Throughput, memory, overrun and timing-source results | `WP-33.01` |
| Lifecycle, pause-view and gap integrity results | `WP-33.02` |
| Precision, alignment and conversion results | `WP-33.03` |
| Crash-recovery prefix verification and immutability results | `WP-33.04` |
| Replay equivalence and labelling results | `WP-33.05` |
| Window-close, background and visibility results | `WP-33.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The ArcScope Reference Coverage Matrix and licence audit are complete.
2. Every adapter works over a real transport; historical configuration is immutable; a second claimant is refused with a busy state.
3. Sustained throughput exceeds the product target with bounded memory; every overrun is counted, timestamped and visible.
4. Every lifecycle transition is correct; pausing the view never stops recording; a disconnect produces an explicit gap.
5. Time is exact within each domain with explicit conversion; multi-source alignment is recorded.
6. **A crash mid-capture yields a verifiable prefix with recorded loss, and a finalised capture is structurally immutable.**
7. Replay produces an equivalent session, is always labelled, and never fabricates device-only fields.
8. Recording state is always visible; closing a window during capture never silently stops or continues it.

---

## 9. Dependencies

**Upstream.** `07` (persistence), `10` (shell), `13` (probe conclusions), `26` (remote task participation).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `34` — Analysis and reporting | Sessions, captures and the time model to analyse |
| `35` — Integration | Capabilities and metadata for cloud sync and ArcChat |
