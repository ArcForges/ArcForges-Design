<a id="rule-wp-33"></a>

# WP-33 — ArcScope Acquisition and Session Core

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: H — ArcScope
> Upstream: `07`, `10`, `13`, `26` · Downstream: `34`, `51`

> **Goal.** Build the evidence layer: sources and adapters, the acquisition pipeline, sessions and captures with segments and gaps, the channel and event time model, and record and replay — with raw capture treated as evidence, immutable once finalised.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcScope; Platform. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Data sources and source adapters over real transports; connection profiles and effective configuration snapshots; the acquisition pipeline with backpressure and overrun reporting; session and capture lifecycle with segments and gaps; the channel, signal and event time model; the rolling buffer and live observation; durable capture writing; and replay as a source.

**Out of scope.** Analysis, measurement, decoding, visualisation and reporting (`34`). Cloud metadata sync and ArcChat integration (`35`). Device control, which is a later, higher-permission capability class.

**Why this package exists.** The [ArcScope implementation map](../../architecture/19-product-implementation-maps.md) and this package fix the order: source and adapter, then acquisition, then session and capture, then the time model, then record and replay. Evidence integrity is established before anything interprets the evidence.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) | The full product model, domain concepts and V1 scope |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) `§8` | The acquisition pipeline architecture and its rules |
| [WP-13.02](13-high-risk-technical-probes.md#rule-wp-13.02) output | The throughput, ring buffer and overrun probe conclusions |
| [`../../assurance/reference-coverage/arcscope-serial-studio.md`](../../assurance/reference-coverage/arcscope-serial-studio.md) | **The completed ArcScope Reference Coverage Matrix** — 31 rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, oracle and owner |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix method and the ten-field provenance record that governs any future reuse |
| [WP-07](07-local-persistence-foundation.md#rule-wp-07), [WP-10](10-design-system-and-desktop-shell.md#rule-wp-10), [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26) output | Persistence, shell and remote task participation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcScope Reference Coverage Matrix is a completed, versioned planning input** — [`../../assurance/reference-coverage/arcscope-serial-studio.md`](../../assurance/reference-coverage/arcscope-serial-studio.md), 31 item-level rows, bound to Serial-Studio at `639daafb`. It was produced before this plan was derived (**[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)**). **This package consumes it and checks it for drift; it does not create it.** |
| BR-02 | **`Device ≠ DataSource`** ([I-466](../../requirements/01-normative-glossary-and-invariants.md#rule-i-466)). The data source is the real entry point; the device is an optional identity. |
| BR-03 | **`Session ≠ Capture`** ([I-467](../../requirements/01-normative-glossary-and-invariants.md#rule-i-467)) and live observation is separate from capture ([I-469](../../requirements/01-normative-glossary-and-invariants.md#rule-i-469)). |
| BR-04 | **Pausing the view never stops recording** ([I-469](../../requirements/01-normative-glossary-and-invariants.md#rule-i-469)). |
| BR-05 | **Raw capture, once finalised, is immutable.** Raw capture is evidence and the source of truth. |
| BR-06 | **Every session records an effective configuration snapshot** — the settings actually in force. Changing a profile never rewrites a historical session. |
| BR-07 | **An acquisition overrun is surfaced, never hidden**: counted, timestamped and recorded as a gap. |
| BR-08 | **Replay never impersonates a real device** ([I-470](../../requirements/01-normative-glossary-and-invariants.md#rule-i-470)), and its origin is always recorded. |
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

<a id="rule-wp-33.00"></a>

### WP-33.00 — Sources, adapters and profiles

**What must be fully done.** First-party adapters for generic transports — serial, TCP, UDP and file replay — behind one adapter contract. Connection profiles are stored and reusable. Editing a profile never alters a historical session's recorded configuration. Exclusive access uses lease and busy semantics.

**Testing requirements.** Real-transport connect, disconnect and reconnect per adapter; a profile-edit test asserting historical sessions are unchanged; an exclusivity test with two claimants.

**Completion gate.** Every adapter works over a real transport, historical configuration is immutable, and a second claimant is refused with a busy state.

<a id="rule-wp-33.01"></a>

### WP-33.01 — Acquisition pipeline

**What must be fully done.** A bounded, timestamped acquisition loop with explicit backpressure. Hardware timestamps preserved where available, with the timing source and its uncertainty recorded otherwise. Overruns counted, timestamped and recorded. Sustained throughput above the product target with bounded memory.

**Testing requirements.** Sustained-throughput runs with recorded rate, memory and drop counts; induced overrun; timing-source recording assertions.

**Completion gate.** Sustained throughput exceeds target with bounded memory, and every overrun is counted, timestamped and visible.

<a id="rule-wp-33.02"></a>

### WP-33.02 — Session, capture, segments and gaps

**What must be fully done.** The session and capture lifecycle: armed, running, paused, stopped, finalised, and interrupted. Captures are sequences of segments plus explicit gaps. Live observation uses the rolling buffer; record creates persistent capture. Pausing the view never stops recording.

**Testing requirements.** Lifecycle coverage including interruption; a pause-view-while-recording test; a segment-and-gap integrity test after a disconnect.

**Completion gate.** Every lifecycle transition is correct, pausing the view never stops recording, and a disconnect produces an explicit gap rather than a truncated capture.

<a id="rule-wp-33.03"></a>

### WP-33.03 — Time and channel model

**What must be fully done.** A precise time model spanning signal samples and discrete events, with exact rate representation and explicit conversion. Channels and signals are modelled distinctly from events. Alignment between sources is explicit and recorded.

**Testing requirements.** Precision tests across rate domains; an alignment test with two sources; a conversion-exactness test.

**Completion gate.** Time is exact within each domain with explicit conversion, and multi-source alignment is recorded rather than assumed.

<a id="rule-wp-33.04"></a>

### WP-33.04 — Durable capture and immutability

**What must be fully done.** Raw capture written to the chunked verifiable store with per-chunk checksums and an explicit end marker. Once finalised, a capture is immutable. A crash mid-capture recovers to the last committed boundary with an honest end marker and a recorded loss.

**Testing requirements.** Kill-during-capture at chunk boundaries and mid-chunk; verification of the recovered prefix; an immutability test asserting a finalised capture cannot be modified.

**Completion gate.** A crash yields a verifiable prefix with recorded loss, and a finalised capture is structurally immutable.

<a id="rule-wp-33.05"></a>

### WP-33.05 — Replay

**What must be fully done.** Replay as a source adapter feeding the same pipeline, always labelled as replay with its origin recorded. A replay adapter never presents device-only fields as measured.

**Testing requirements.** Replay of a recorded capture producing an equivalent session; a labelling assertion; a negative test asserting device-only fields are absent.

**Completion gate.** Replay produces an equivalent session, is always labelled, and never fabricates device-only fields.

<a id="rule-wp-33.06"></a>

### WP-33.06 — Long-running capture in the shell

**What must be fully done.** Capture as a long-running activity with a permanently visible recording state. Closing a window during capture asks with consequences stated, never silently stopping or silently continuing. Background capture persists only while genuine work is active.

**Testing requirements.** Window-close-during-capture prompts; a background-residency test; a recording-visibility assertion.

**Completion gate.** Recording state is always visible, and closing a window during capture never silently stops or continues it.

<a id="rule-wp-33.07"></a>

### WP-33.07 — Reference drift check

> **Not a baseline audit.** The ArcScope matrix is complete and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. This sub-step is **maintenance**, and it is the producer of the drift check the package gate requires.

**What must be fully done.** The reference is compared against its bound commit — Serial-Studio at `639daafb`. Three outputs are produced:

1. **Changed material**: any file behind a matrix row that changed since the bound commit, with the row re-assessed.
2. **Newly introduced material**: capabilities added upstream since the bound commit, each assessed against the accepted ArcScope scope. **A new upstream capability does not become an ArcForges requirement by appearing** — it is mapped to an existing requirement or recorded as an accepted exclusion.
3. **Licence re-verification**: the reference's licence files are re-read. A subtree licence can change upstream, and the disposition of every row depends on it.

**Testing requirements.** A drift report listing changed rows, new material with its assessment, and the licence comparison. A completeness check that every changed or new item has a disposition.

**Completion gate.** The drift report exists, every changed and newly introduced item carries a disposition, and the licence position is re-confirmed or amended with a reason. **If the licence position changed, the affected rows' dispositions are corrected before any dependent work continues** (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**).

---

<a id="rule-wp-33.90"></a>
### WP-33.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Keep capture/decoder/session/recording ownership in C#. Replace product native-source dependencies using selected capability packages and explicit managed/native acquisition boundaries.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Real packaged hardware-path and throughput/overrun/recovery acceptance; no automatic upload of raw acquisition data.

**Completion gate.** Real packaged hardware-path and throughput/overrun/recovery acceptance; no automatic upload of raw acquisition data. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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
| Per-adapter real-transport results, profile immutability, exclusivity | [WP-33.00](#rule-wp-33.00) |
| Throughput, memory, overrun and timing-source results | [WP-33.01](#rule-wp-33.01) |
| Lifecycle, pause-view and gap integrity results | [WP-33.02](#rule-wp-33.02) |
| Precision, alignment and conversion results | [WP-33.03](#rule-wp-33.03) |
| Crash-recovery prefix verification and immutability results | [WP-33.04](#rule-wp-33.04) |
| Replay equivalence and labelling results | [WP-33.05](#rule-wp-33.05) |
| Window-close, background and visibility results | [WP-33.06](#rule-wp-33.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-33.90](#rule-wp-33.90) and all inherited domain-specific gates must pass on the same candidate closure. Real packaged hardware-path and throughput/overrun/recovery acceptance; no automatic upload of raw acquisition data.

**[PG-08](../../assurance/open-gates-register.md#rule-pg-08) evidence:** [WP-33](#rule-wp-33) — Every claimed real hardware result names the maintained device/firmware/driver/lab inventory. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-03](../../assurance/open-gates-register.md#rule-pg-03) evidence:** [WP-33](#rule-wp-33) — Licence/provenance approval for each admitted acquisition native dependency. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**All of the following, with recorded evidence:**

1. **Drift check only**: the reference is compared against its bound commit, and any newly introduced material is assessed against the accepted ArcScope scope. The matrix and its licence audit were completed as design-stage evidence and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. Findings carried in: **F-AS-1** records an **authorship boundary**, not merely a reuse prohibition: the reference’s commercial-only modules — MQTT, XY plotting, 3D visualisation and the activation system — were deliberately **not read**, and no ArcScope capability may derive from their expression.
2. Every adapter works over a real transport; historical configuration is immutable; a second claimant is refused with a busy state.
3. Sustained throughput exceeds the product target with bounded memory; every overrun is counted, timestamped and visible.
4. Every lifecycle transition is correct; pausing the view never stops recording; a disconnect produces an explicit gap.
5. Time is exact within each domain with explicit conversion; multi-source alignment is recorded.
6. **A crash mid-capture yields a verifiable prefix with recorded loss, and a finalised capture is structurally immutable.**
7. Replay produces an equivalent session, is always labelled, and never fabricates device-only fields.
8. Recording state is always visible; closing a window during capture never silently stops or continues it.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [07 local persistence foundation](07-local-persistence-foundation.md#rule-wp-07)
- [10 design system and desktop shell](10-design-system-and-desktop-shell.md#rule-wp-10)
- [13 high risk technical probes](13-high-risk-technical-probes.md#rule-wp-13)
- [26 remote action and tool bridge](26-remote-action-and-tool-bridge.md#rule-wp-26)

**Downstream — consumers of these released outputs.**

- [34 arcscope analysis and reporting](34-arcscope-analysis-and-reporting.md#rule-wp-34)
- [51 arcscope cloud simulator](51-arcscope-cloud-simulator.md#rule-wp-51)

---
