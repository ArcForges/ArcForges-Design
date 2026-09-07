# ArcScope — Product Requirements
> Current scope amendment: **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Product identity: `arcscope` · Positioning: **Local-first Professional Data Acquisition, Observation & Telemetry Analysis Workspace**
> Governing authority: **[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)** (ArcScope is an independently defined product, **not** a rename or continuation of ArcImage)
> Companions: [`../12-quality-and-compatibility-contract.md`](../12-quality-and-compatibility-contract.md), [`../13-data-formats-and-portability.md`](../13-data-formats-and-portability.md), [`arcchat.md`](arcchat.md), [`arcnotes.md`](arcnotes.md)

> **A local-first professional acquisition and analysis workbench: Session as the working context, Capture as the original evidence, supporting both Signal and Event, performing real-time observation, recording, decoding, measurement, analysis, comparison and reporting around a timeline.**

---

## 1. Scope and identity

| # | Requirement |
|---|---|
| ID-01 | **ArcScope is an independently defined product.** It is **not** a rename or continuation of ArcImage, and the ArcImage domain vocabulary — Canvas, Layer, Mask, Filter, image editing — **must never be migrated into it** (**[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)**). |
| ID-02 | **ArcScope must not be locked to one industry.** Not "a serial monitor", not "an oscilloscope", not "an IoT dashboard". Its core is **time-related data**. |
| ID-03 | The product's real core is **Signal + Event over time**, with acquisition, observation, recording, decoding, measurement, analysis, annotation, comparison and reporting built around it. |
| <a id="rule-id-04"></a>ID-04 | **V1 is observation-first**: read, acquire, analyse. **Device control is a separate, later, higher-permission capability class** (§13). |

---

## 2. Top-level domain relationships

```
ArcScope Project
 ├── DataSource (definition)  ── ConnectionProfile ── Connection (live)
 ├── Session
 │    └── Capture
 │         └── Capture Segment  (+ Gap)
 ├── Channel → Signal / Event → Derived Signal
 ├── Measurement · Analysis · Decoder output
 ├── Annotation · Finding
 ├── Comparison
 └── Report
```

| # | Requirement |
|---|---|
| DM-01 | **`ArcScope.Project ≠ ArcForges Workspace`** ([I-465](../01-normative-glossary-and-invariants.md#rule-i-465)). |
| DM-02 | **Project = a long-term professional container for a related set of observations, captures, analyses and reports.** |
| DM-03 | **Quick capture must not be sacrificed to the project model.** A **Quick Session** may exist unfiled and be filed into a project later. |

---

## 3. Sources, connections and devices

| # | Requirement |
|---|---|
| <a id="rule-sd-01"></a>SD-01 | **`Device ≠ DataSource`** ([I-466](../01-normative-glossary-and-invariants.md#rule-i-466)). A device is an **optional identity** describing physical or logical hardware; **the DataSource is ArcScope's real data entry point**. |
| SD-02 | **`DataSource` = a logical source that can provide time-related data, events or raw streams to ArcScope.** |
| SD-03 | **File replay is a DataSource.** The pipeline is always `Source → Session → Analysis`, whether the source is live hardware or a recorded file. |
| SD-04 | **`ConnectionProfile ≠ Connection`** ([I-466](../01-normative-glossary-and-invariants.md#rule-i-466)). A profile is reusable stored configuration; a connection is a live, transient link. |
| <a id="rule-sd-05"></a>SD-05 | **Changing a connection profile must never rewrite a historical session.** Every session records an **Effective Configuration Snapshot** — the settings actually in force at the time. Knowing that a capture genuinely ran at a particular rate is essential evidence. |
| SD-06 | **`Session ≠ Connection`** ([I-467](../01-normative-glossary-and-invariants.md#rule-i-467)). A session may involve several data sources and may outlive individual connections. |
| SD-07 | **A source disconnect must not close the session** (`§4`). The session survives; the interruption is recorded as an explicit gap. |
| <a id="rule-sd-08"></a>SD-08 | **The same source must not be silently claimed by two captures.** Exclusive access is coordinated by the capability owner with lease/busy semantics ([CC-05](../05-ai-and-agent-execution.md#rule-cc-05)). |
| <a id="rule-sd-09"></a>SD-09 | V1 adapters cover serial, TCP, UDP, file/replay and Cloud Simulation (§17.1). Device-specific SDKs remain later; simulation is a real product capability, not a mock hardware driver. |
| <a id="rule-sd-10"></a>SD-10 | **Replay must never impersonate a real device.** Replayed data is explicitly labelled as replay, with its origin. |

---

## 4. Session, capture and evidence

| # | Requirement |
|---|---|
| SE-01 | **`Session` = a complete unit of work with a common observation goal, temporal context and analysis context.** |
| SE-02 | **`Session ≠ Capture`** ([I-467](../01-normative-glossary-and-invariants.md#rule-i-467)). One session may contain several captures. |
| SE-03 | **Capture segments exist** because acquisition is interrupted, paused, resumed and triggered. A capture is a sequence of segments plus explicit gaps. |
| <a id="rule-se-04"></a>SE-04 | **Live observation and capture are separate** ([I-469](../01-normative-glossary-and-invariants.md#rule-i-469)). Live view uses a rolling buffer; **Record** creates persistent capture. |
| <a id="rule-se-05"></a>SE-05 | **`Pause View ≠ Pause Capture`** ([I-469](../01-normative-glossary-and-invariants.md#rule-i-469)). Freezing the display must never stop recording. |
| SE-06 | Capture lifecycle: `Armed → Running → Paused → Stopped → Finalized`, plus `Interrupted`. |
| SE-07 | **`Interrupted` is not `Failed`.** Interrupted data that was durably written **is valid data** and must be preserved and presented as such. |
| SE-08 | **Recorded data must never be discarded during crash recovery** ([CR-04](../12-quality-and-compatibility-contract.md#rule-cr-04) in the quality contract). Recovery restores to the last durably committed boundary. |
| <a id="rule-se-09"></a>SE-09 | **A disconnect and reconnect must produce an explicit Gap.** |
| <a id="rule-se-10"></a>SE-10 | **No silent data loss.** Any data loss that cannot be confirmed as recorded **must be explicitly indicated** — a gap, an overflow marker, a dropped-sample count. |
| SE-11 | **If acquisition cannot keep up**, the condition is surfaced explicitly with its policy — drop, buffer, back-pressure the source, or stop — never hidden. |
| <a id="rule-se-12"></a>SE-12 | **Raw capture, once finalised, is immutable by default.** **Raw Capture = evidence = source of truth.** |
| SE-13 | **Trim is non-destructive by default.** Trimming produces a derived view or a new managed representation; the original is not silently reduced. |
| <a id="rule-se-14"></a>SE-14 | **Raw capture uses chunked, verifiable large-scale storage**, not database blobs ([LD-01](../13-data-formats-and-portability.md#rule-ld-01)–[LD-05](../13-data-formats-and-portability.md#rule-ld-05)). |

---

## 5. Time model

The time model is a product-level design, not an implementation detail.

| # | Requirement |
|---|---|
| TM-01 | ArcScope retains at least three time semantics: **source time** (as reported by the source), **host time** (when ArcScope received it), and **session time** (relative to the session origin). |
| TM-02 | **Source time must never be forced to equal host time.** Their relationship is a recorded clock mapping. |
| <a id="rule-tm-03"></a>TM-03 | **Multi-source sessions support time alignment**, and **alignment never overwrites raw timestamps** ([I-472](../01-normative-glossary-and-invariants.md#rule-i-472) family) — it is an analysis and view transformation. |
| TM-04 | **Time accuracy and trustworthiness are expressible**: resolution, known offset, drift, synchronisation quality and confidence. |
| TM-05 | Storage is a stable instant plus source semantics; display is localised ([TZ-01](../12-quality-and-compatibility-contract.md#rule-tz-01)–[TZ-03](../12-quality-and-compatibility-contract.md#rule-tz-03)). |

---

## 6. Channels, signals and events

| # | Requirement |
|---|---|
| CS-01 | **`Channel` = a logical data channel exposed by a DataSource** — a source-level concept. |
| CS-02 | **`Signal` = a temporal value with type, time and semantics.** |
| CS-03 | **`Channel ≠ Signal`** ([I-468](../01-normative-glossary-and-invariants.md#rule-i-468)). One channel may yield several signals; a signal may be composed from several channels. |
| CS-04 | **`Signal ≠ Event`** ([I-468](../01-normative-glossary-and-invariants.md#rule-i-468)). **`Event` = a discrete, timestamped, structured occurrence.** |
| CS-05 | **Decoder output — packets, frames, records — is modelled as structured events**, not as raw channel data. |
| CS-06 | **Signals are not floating-point only.** Integer, unsigned, boolean/digital, enumerated and string-valued signals are all supported. |
| CS-07 | **Sample rate must not be assumed constant.** Irregular, event-driven and burst sampling are first-class. |
| CS-08 | **Units are first-class signal metadata** ([UN-01](../12-quality-and-compatibility-contract.md#rule-un-01)–[UN-04](../12-quality-and-compatibility-contract.md#rule-un-04)). |
| CS-09 | **Display unit conversion never changes the raw value** ([I-470](../01-normative-glossary-and-invariants.md#rule-i-470), [UN-01](../12-quality-and-compatibility-contract.md#rule-un-01)). A converted value shown in the interface is a display conversion; producing a converted series is a **Derived Signal**. |
| CS-10 | **`Raw Signal ≠ Derived Signal`** ([I-468](../01-normative-glossary-and-invariants.md#rule-i-468)). Any series produced by a decoder, transform, analysis or maths expression is derived, reproducible, and never raw authority. |
| CS-11 | **Derived signals can be recomputed**, and their definition is retained so they can be. |

---

## 7. Visualisation

| # | Requirement |
|---|---|
| VZ-01 | Live visualisation supports at minimum: time-series plots, digital/logic tracks, event timelines, event tables, and multi-signal views. |
| VZ-02 | **One view may display several signals**, and **signals of incompatible dimensions do not silently share one axis** ([UN-04](../12-quality-and-compatibility-contract.md#rule-un-04)). |
| VZ-03 | **`View ≠ Signal ownership`** ([I-475](../01-normative-glossary-and-invariants.md#rule-i-475)). Removing a signal from a view does not delete data. |
| VZ-04 | **Display decimation is strictly separated from real data** ([I-470](../01-normative-glossary-and-invariants.md#rule-i-470)). **Measurement and analysis operate on canonical data, never on screen-sampled pixels.** |
| VZ-05 | **An approximate measurement must be labelled approximate**, with the reason. |
| VZ-06 | **Zoom and pan are core capabilities**, at professional precision, including keyboard navigation. |
| VZ-07 | **Cursors are core to professional analysis**: single, dual, delta, and value readouts with units. |
| VZ-08 | **Selection is the core of ArcScope agent context**: a **stable selected time range** (and signal set) that can be passed as a durable context reference ([IB-01](../05-ai-and-agent-execution.md#rule-ib-01)). |
| VZ-09 | **Multi-signal selection is supported.** |
| VZ-10 | **Live follow** (auto-scroll) is a view mode, independent of recording state ([SE-05](#rule-se-05)). |
| VZ-11 | Panel layout is device-local; **Saved Analysis Views are session/project work content**, not window geometry ([LY-03](../09-shared-desktop-experience.md#rule-ly-03), `§17`). |

---

## 8. Triggers

| # | Requirement |
|---|---|
| TG-01 | **`Trigger` = a rule that controls capture, or generates significant time events, based on data or event conditions.** |
| TG-02 | The trigger family is extensible; V1 provides at minimum **manual** and **basic threshold/edge** triggers. |
| TG-03 | **Triggered capture supports pre-trigger and post-trigger windows**, served by the rolling buffer. |
| TG-04 | **`TriggerDefinition ≠ TriggerOccurrence`** ([I-471](../01-normative-glossary-and-invariants.md#rule-i-471) family). |
| <a id="rule-tg-05"></a>TG-05 | **A trigger must never modify data.** It controls capture and marks time; samples are unchanged. |
| TG-06 | **Trigger presets are reusable**, and each occurrence records the **effective trigger snapshot** in force at the time. |

---

## 9. Measurement and analysis

| # | Requirement |
|---|---|
| MA-01 | **`Measurement ≠ Analysis`** ([I-471](../01-normative-glossary-and-invariants.md#rule-i-471)). A measurement is a quantified reading; an analysis is an interpretation. |
| MA-02 | Measurements are of two kinds: **transient** (a live readout) and **persisted** (repeatable, placeable in a report). |
| MA-03 | **Every measurement records its scope**: signals, time range, alignment, source revision and configuration. |
| <a id="rule-ma-04"></a>MA-04 | Basic measurement family: minimum, maximum, mean, RMS, peak-to-peak, standard deviation, count, duration, frequency, duty cycle, rise/fall time, delta between cursors, and event counts. |
| MA-05 | **Every measurement result carries a unit** ([UN-01](../12-quality-and-compatibility-contract.md#rule-un-01)). |
| MA-06 | Basic analysis family: statistics over ranges, thresholds and violations, edge and pulse analysis, spectral analysis, correlation between signals, event sequence analysis, and protocol decode summaries. |
| MA-07 | **Analysis is non-destructive** ([I-472](../01-normative-glossary-and-invariants.md#rule-i-472)). |
| <a id="rule-ma-08"></a>MA-08 | **Analysis is reproducible**: the definition, inputs, source revision, configuration snapshot and version are retained so the result can be recomputed. |
| MA-09 | **`AnalysisRecipe` = a reusable set of analysis and measurement configurations**, applicable to another session and shareable with automation, community packages and ArcChat. |
| MA-10 | **A recipe stores the process definition, not old results.** |

---

## 10. Decoders

| # | Requirement |
|---|---|
| DE-01 | **`Decoder` = a semantic processor converting raw channel or event streams into structured events, fields and signals.** |
| DE-02 | **Decoder output is derived data** ([I-471](../01-normative-glossary-and-invariants.md#rule-i-471)) and may be retained, but never becomes raw authority. |
| DE-03 | **Decoders are versioned**, and every decoded result records the decoder version and its **configuration snapshot**. |
| DE-04 | **Decoder chains are supported** — the output of one decoder feeding another. |
| DE-05 | **Decoder errors are displayed**, not silently dropped: malformed frames, checksum failures and unknown fields are visible with counts and locations. |
| <a id="rule-de-06"></a>DE-06 | **A decoder is not device control** ([ID-04](#rule-id-04)). It interprets data; it does not command hardware. |

---

## 11. Annotation and findings

| # | Requirement |
|---|---|
| AN-01 | **Annotation is first-class ArcScope data.** |
| AN-02 | Basic annotation types: **marker** (a point in time), **region annotation** (a time range), **note**, and **finding**. |
| AN-03 | **`Finding`** is an owned, structured conclusion with severity, evidence references and status. |
| AN-04 | **Annotations may be created by a human or an agent**, and the **actor is always recorded**. |
| AN-05 | **An agent-created finding must never impersonate a user conclusion** ([AC-02](../02-identity-account-and-workspace.md#rule-ac-02)). It is labelled as agent-produced, with its task and evidence. |
| AN-06 | **Annotation never changes raw data** ([I-472](../01-normative-glossary-and-invariants.md#rule-i-472)). It is an overlay and semantic layer. |

---

## 12. Comparison and baselines

| # | Requirement |
|---|---|
| CM-01 | **Comparison is a core professional capability**: session-to-session and capture-to-capture. |
| CM-02 | **`Comparison ≠ Merge`** ([I-472](../01-normative-glossary-and-invariants.md#rule-i-472)). Comparison never produces a combined authoritative dataset. |
| CM-03 | **Alignment is first-class configuration** — by absolute time, by trigger, by event, or by manual offset — and is retained with the comparison. |
| CM-04 | **Alignment never modifies the compared sessions** ([TM-03](#rule-tm-03)). |
| CM-05 | **Signals with incompatible units do not compare automatically** ([UN-04](../12-quality-and-compatibility-contract.md#rule-un-04)); an explicit conversion or an explicit acknowledgement is required. |
| CM-06 | **Baseline is a reference**, not an authority: a designated session or analysis result used for comparison, which never rewrites what it is compared against. |
| CM-07 | **A comparison may be re-run with new analysis**, and the older result retains its own source and configuration. |

---

## 13. Device control (later, higher permission)

| # | Requirement |
|---|---|
| DC-01 | **Observation and control are different capability classes** ([ID-04](#rule-id-04)). |
| <a id="rule-dc-02"></a>DC-02 | **Device control carries stricter permission than capture**, because it has real physical or system side effects. It is an R3-or-above capability with explicit approval, and typically local presence. |
| <a id="rule-dc-03"></a>DC-03 | Start capture and stop capture may be exposed as capabilities, and are treated as operations with real side effects — not as read-only conveniences. |

---

## 14. Reports

| # | Requirement |
|---|---|
| RP-01 | **`ArcScope Report` = a structured, traceable technical analysis result.** |
| RP-02 | **`ArcScope Report ≠ ArcNotes Document`** ([I-029](../01-normative-glossary-and-invariants.md#rule-i-029), [I-471](../01-normative-glossary-and-invariants.md#rule-i-471)). It is not an alias. |
| RP-03 | A report may contain: session and configuration provenance, measurements, analysis results, charts, annotations, findings and narrative. |
| RP-04 | **A chart in a report is best stored as a reproducible view definition**, so it can be regenerated from data — with an exported report additionally able to carry a static snapshot. |
| RP-05 | **Sources must be traceable from a report** back to session, capture, time range, configuration snapshot and analysis version. |
| RP-06 | **The ArcScope → ArcNotes relationship is a copy/import**, creating a **new ArcNotes-owned document** with retained ArcScope provenance ([CP-03](arcnotes.md#rule-cp-03) in the ArcNotes requirements). **Two products never share one writable object** (`§4.2` of the product scope). |

---

## 15. Import, export and replay

Export is in four classes:

| Class | Purpose |
|---|---|
| **Native full-fidelity** | Complete ArcScope project/session bundle for migration |
| **Data export** | CSV, JSON and tabular/event formats for external tools |
| **Report export** | Structured report output |
| **Presentation export** | Charts and images for consumption |

| # | Requirement |
|---|---|
| IE-01 | **CSV export must not lose precision without telling the user.** An export warning or manifest declares the representation used and any loss ([EX-02](../13-data-formats-and-portability.md#rule-ex-02) in the data requirements). |
| IE-02 | **Native export is the complete data migration format** ([EX-01](../13-data-formats-and-portability.md#rule-ex-01) in the data requirements). |
| IE-03 | **Import and replay are first-class**, and imported data enters the **unified session model** with a recorded **origin** — it becomes an ArcScope session and capture, not a foreign object. |
| IE-04 | Generic import adapters cover common tabular and event formats; more are added through the same adapter contract. |
| IE-05 | **Replay never disguises itself as a live device** ([SD-10](#rule-sd-10)). |
| IE-06 | **Collect Investigation Bundle** gathers a project, its managed assets and, on request, its external references into a portable bundle without destroying originals ([EX-08](../13-data-formats-and-portability.md#rule-ex-08) in the data requirements). |

---

## 16. AI in ArcScope

**Core principle: numerical grounding.**

| # | Requirement |
|---|---|
| AI-01 | **Deterministic tools produce numbers; the model provides understanding and orchestration.** A model must never be the authority for a precise numerical result. |
| <a id="rule-ai-02"></a>AI-02 | **AI does not process an entire raw capture.** It receives necessary structured results — measurements, analysis outputs, decoded event summaries, selected ranges ([CP-03](../06-knowledge-search-and-retrieval.md#rule-cp-03) in the knowledge requirements). |
| AI-03 | **When AI states a number it must cite its source** — measurement, analysis result, range and revision ([EC-09](../06-knowledge-search-and-retrieval.md#rule-ec-09)). |
| AI-04 | Internal AI actions are selection- and result-scoped: explain this range, summarise these findings, suggest a measurement, draft a report section. |
| AI-05 | ArcScope has no agent harness. AI actions and orchestration use the single Cloud harness; ArcChat supplies the shared chat/task surface and local authorization bridge. |
| AI-06 | **"Ask ArcChat" passes a bounded context reference** — session, range, signals, results — never the raw capture. |
| AI-07 | **The user must see the scope the AI used** ([RT-03](../06-knowledge-search-and-retrieval.md#rule-rt-03) in the knowledge requirements). |
| <a id="rule-ai-08"></a>AI-08 | **A local-only capture must not be uploaded because an AI button was pressed** ([I-182](../01-normative-glossary-and-invariants.md#rule-i-182)). |
| AI-09 | **AI-generated analysis must be reproducible** like any other analysis ([MA-08](#rule-ma-08)), or clearly marked as narrative. |
| AI-10 | **`AI Summary ≠ Measurement Result`** ([I-163](../01-normative-glossary-and-invariants.md#rule-i-163)). Summary is narrative; analysis result is evidence. |
| AI-11 | All AI uses the subscribed Cloud service and actual-usage metering. Deterministic local measurement and analysis are ordinary product computation, not local AI. |

### 16.1 Capabilities exposed to ArcChat

Query capabilities (list projects, sessions, captures, channels, signals, events; read measurements and analysis results; read annotations and findings; read configuration snapshots), analysis capabilities (run a measurement, run an analysis, apply a recipe, compare sessions), authoring capabilities (create annotation, create finding, create report), and operational capabilities (start/stop capture, and later device control) — each with its risk level, permission requirement and approval posture.

---

## 17. Cloud behaviour

| # | Requirement |
|---|---|
| CL-01 | **`Cloud Sync ≠ Raw Capture Upload`** ([I-474](../01-normative-glossary-and-invariants.md#rule-i-474)). |
| CL-02 | Default sync covers project, session metadata, annotations, findings, analysis results, reports and configurations. Hardware capture is local by default. Simulator output originates in Cloud under [SIM-01](#rule-sim-01)–[SIM-20](#rule-sim-20) and is labelled synthetic. |
| CL-03 | **Enabling project cloud sync does not upload raw capture.** Raw upload is an explicit per-session act. |
| CL-04 | **The raw-capture cloud policy is explicit and visible** per project and per session. |
| CL-05 | **Cloud metadata present with raw data missing locally is a normal state**, clearly presented — **never "corrupted"** ([AS-04](../03-cloud-services-and-sync.md#rule-as-04)). |
| CL-06 | Hardware acquisition and analysis of local captures remain native. Cloud orchestrates authorized desktop tools through ArcChat; the Cloud simulator runs server-side without an online desktop. |
| CL-07 | A remote agent may use an online desktop ArcScope to run analyses, subject to the full remote authorization model. |

---

### 17.1 Deterministic Cloud simulator — V1

The simulator supplies repeatable signal/event data through real Cloud persistence and client acquisition paths without attached hardware. It is a user-facing capability and a verification source; canned test responses do not discharge this requirement.

| # | Requirement |
|---|---|
| <a id="rule-sim-01"></a>SIM-01 | Cloud owns SimulationDefinition, immutable ScenarioVersion, SimulationRun, SimulationSegment and SimulationEvent. ArcScope owns the native observation/session projection and downloaded capture. A SimulationRun is a product job, not an Agent Run, and invokes no model. |
| <a id="rule-sim-02"></a>SIM-02 | A run binds the owner workspace, scenario version, seed, channel schema, duration/tick budget, clock mode, generator version and deterministic execution/encoding profile. Definition edits affect future runs only. |
| <a id="rule-sim-03"></a>SIM-03 | Channels have stable IDs, value types, units, rate/timestamp semantics and encoding. V1 generators include constant, sine, square, triangle, sawtooth, seeded noise, seeded random walk, pulse, step sequence and uploaded CSV replay. Numeric, digital and event cases feed the normal native acquisition pipeline. |
| <a id="rule-sim-04"></a>SIM-04 | V1 supports a bounded expression AST over constants, time/tick, channel references, arithmetic, comparison, conditionals and allowlisted numeric functions. Acyclic channel dependencies and limits on depth, nodes and operations per tick are validated before admission. Arbitrary scripts, dynamic compilation, reflection, file access and networking are prohibited. |
| <a id="rule-sim-05"></a>SIM-05 | Optional fault profiles cover latency, jitter, drop, duplicate, reorder, disconnect, malformed frame and outlier injection at explicit logical boundaries. Seeded random streams are independent per channel/fault source. Intentional faults carry provenance and counters; they never hide unexpected data loss. |
| <a id="rule-sim-06"></a>SIM-06 | Fixed logical ticks drive canonical data. Real-time-paced and bounded accelerated generation are supported; pacing, preview refresh and wall-clock timestamps do not change sample values, logical timestamps or canonical hashes. |
| <a id="rule-sim-07"></a>SIM-07 | Identical effective input under the same supported execution/encoding profile yields identical canonical segment content and hashes. The profile pins numeric semantics, RNG, generator and encoding versions; arbitrary cross-version/CPU floating-point equivalence is not promised. Host/run IDs and wall-clock metadata are outside the reproducible payload. |
| <a id="rule-sim-08"></a>SIM-08 | Lifecycle is Queued → Starting → Running, with Pausing → Paused → Running, Stopping → Canceled, and terminal Succeeded or Failed. Success means the requested finite logical range completed. Cancel preserves committed segments and records a partial outcome, never success for an incomplete range. |
| <a id="rule-sim-09"></a>SIM-09 | Start, pause, resume and cancel are durable, authorized, idempotent commands with expected state/revision. Stale commands and duplicate starts cannot create another run or resurrect a terminal run. Terminal reason and complete/partial extent are queryable. |
| <a id="rule-sim-10"></a>SIM-10 | The single ASP.NET Core Cloud host executes bounded simulator work internally. Durable leases with fencing prevent replicas from publishing the same logical segment; request handlers do not run an unbounded generation loop. |
| <a id="rule-sim-11"></a>SIM-11 | Canonical batches become immutable object-storage segments. Each manifest entry contains run/profile identity, sequence, logical range, count, encoding, byte length and hash. Publication, manifest visibility and checkpoint advancement are recoverable: incomplete objects stay invisible and are cleaned; a committed manifest never references an unverified partial object. |
| <a id="rule-sim-12"></a>SIM-12 | A durable checkpoint includes next tick, RNG/generator/replay positions, pending fault/reorder state and committed segment boundary. Pause/resume or host loss and lease takeover produce the same remaining canonical data without duplicate or missing logical ranges. |
| <a id="rule-sim-13"></a>SIM-13 | Clients obtain an authorized manifest and resumable, hash-verifiable segments through HTTP/object storage, plus revision/cursor-based state/event polling. SignalR is an optional wakeup/preview hint, never the authoritative raw sample stream. Reconnect and disabled realtime preserve access to retained committed data. |
| <a id="rule-sim-14"></a>SIM-14 | ArcScope exposes Cloud Simulation as a clearly synthetic DataSource. Users start/select a scenario, observe, pause/cancel, download and replay committed data in normal session, capture, decoder, measurement and report workflows. Seed/profile provenance survives export or copy. |
| <a id="rule-sim-15"></a>SIM-15 | Memory, queues and temporary storage are bounded. Preview may visibly decimate or throttle. Canonical generation instead slows, persists safely or stops with an explicit partial outcome; preview overload cannot silently drop canonical samples. |
| <a id="rule-sim-16"></a>SIM-16 | Deployment policy bounds channels/rates/duration, AST work, per-workspace/global concurrency, queue/wait time, storage/egress and retention. Limits are enforced before and during execution, with capacity reservation where required. Unauthorized or impossible requests fail before side effects. |
| <a id="rule-sim-17"></a>SIM-17 | Official simulation requires the configured active Cloud service entitlement, independently of AI credits. Duration, samples, bytes and egress are product-resource usage, never model tokens. No simulator per-run AI debit or separate pay-per-use sale is required. Self-hosting uses operator grants and the same safety limits. Term expiry/suspension stops further generation at a durable boundary as Canceled with the explicit eligibility reason; committed output follows retained-data access rules. |
| <a id="rule-sim-18"></a>SIM-18 | CSV replay reads explicitly uploaded, workspace-owned resources with a content hash, schema and bounded parse report. Scenarios cannot fetch arbitrary URLs, read host files or cross workspace boundaries. Exported scenarios contain no deployment secrets or policy values. |
| <a id="rule-sim-19"></a>SIM-19 | Retention, deletion and exhausted storage expose their effect on historical runs and native availability. Active leases/readers are handled safely. Stored outputs remain distinguishable from regenerating a new run. |
| <a id="rule-sim-20"></a>SIM-20 | Acceptance runs against the real Cloud host, storage and native adapter: same seed/profile hashes; changed seed; precise fault positions; pause/resume; killed host and fenced takeover; duplicate commands; malformed AST/CSV; quota exhaustion; cross-workspace denial; reconnect with realtime disabled; partial cancellation; and a 24-hour bounded-resource soak. A preview or test fake is insufficient. |

---

## 18. Library, metadata and reproducibility

| # | Requirement |
|---|---|
| LB-01 | ArcScope has a searchable library over projects, sessions, captures, findings and reports, with filters by time, source, tag and metadata. |
| LB-02 | Simple **tags** organise sessions and projects. |
| LB-03 | **Session metadata is moderately structured**, including custom user metadata fields. |
| <a id="rule-lb-04"></a>LB-04 | **Reproducibility is a core product value.** A result must be reconstructable from: session, capture, configuration snapshot, decoder version and configuration, analysis definition and version, alignment, and calibration version. |
| LB-05 | **A session configuration snapshot is indispensable** ([SD-05](#rule-sd-05)). |
| LB-06 | **Calibration is modelled as a traceable transform**, not as a mutation of raw data, and its **version is part of provenance**. |

---

## 19. Long-running work and safety-critical UI

| # | Requirement |
|---|---|
| LR-01 | Capture, decode, analysis, import and export are product Activity/Job operations in the shared activity surface. SimulationRun is a Cloud-owned product job. None creates a second AI scheduler. |
| LR-02 | **Capture is a special long-running activity with a permanently visible recording state.** |
| LR-03 | **The recording indicator is safety-critical UI.** It must be unmistakable, always visible while recording, and must never be obscured or ambiguous. |
| LR-04 | **Closing a window during capture must not silently stop or silently continue.** The user is asked, with the consequences stated ([LF-04](../09-shared-desktop-experience.md#rule-lf-04)). |
| LR-05 | **Background capture is not permanent background residency** ([LF-02](../09-shared-desktop-experience.md#rule-lf-02)). It persists only while genuine work is active. |
| LR-06 | **Several windows on one session share one authority** ([WN-04](../09-shared-desktop-experience.md#rule-wn-04)). |

---

## 20. Extension points

Reserved contribution points: **source adapters**, **decoders**, **measurement kinds**, **analysis kinds**, **visualisation kinds**, **exporters and importers**, and **report sections**.

| # | Requirement |
|---|---|
| <a id="rule-ep-01"></a>EP-01 | **A third-party extension can never write raw capture arbitrarily.** Raw capture is written by ArcScope alone. |
| EP-02 | **V1 does not admit arbitrary scripting for the sake of extensibility** (`§13` of the extension requirements). Extension goes through typed extension points and the schema-described capability protocol, out of process. |

---

## 21. Non-goals

ArcScope is **not**: a general-purpose BI tool; a long-term knowledge base (that is ArcNotes); an agent runtime (the single runtime lives in Cloud); a device management or configuration console; a SCADA/control system; an image editor; or a data warehouse.

**The architecture is always Raw immutable + Derived analysis.**

---

## 22. Domain model

```
ArcScopeProject
DataSource · SourceAdapter · Device · ConnectionProfile · Connection
Session · Capture · CaptureSegment · Gap
Clock · TimeMapping
Channel · Signal · DerivedSignal · Event · DecodedRecord · Unit
SourceConfigurationSnapshot
DecoderDefinition · DecoderConfigurationSnapshot
TriggerDefinition · TriggerOccurrence
MeasurementDefinition · MeasurementResult
AnalysisDefinition · AnalysisResult · AnalysisRecipe
Annotation · Marker · RegionAnnotation · Finding
SavedAnalysisView · Comparison · Alignment · BaselineReference
ArcScopeReport
ImportOrigin · ImportJob · ExportJob
SimulationDefinition · ScenarioVersion · SimulationRun · SimulationSegment · SimulationEvent
```

---

## 23. V1 scope

| Area | V1 |
|---|---|
| **Sources** | Reusable source definitions, connect/disconnect, generic first-party adapters (serial, TCP, UDP), file/replay |
| **Session / Capture** | Session, live observation, record, multiple capture segments, disconnect and gap, recovery |
| **Data** | Channel, numeric signal, digital/boolean signal, events, units, timestamps |
| **Visualisation** | Time-series, digital track, event timeline and table, zoom and pan, cursor, range selection, live follow |
| **Trigger** | Manual, basic threshold/edge (architecture supports more) |
| **Measurement** | The basic family: min/max/mean and the rest of [MA-04](#rule-ma-04) |
| **Analysis** | A first analysis family with reproducibility and recipes |
| **Annotation** | Marker, region, note, finding |
| **Comparison** | Session comparison with explicit alignment |
| **Report** | Structured report with traceable sources |
| **Import/Export** | Generic data import, CSV/JSON export with precision warnings, native export, collect bundle |
| **AI** | Grounded internal actions, Ask ArcChat with bounded context, ArcChat query and analysis capabilities |
| **Cloud** | Project/metadata sync, explicit hardware-capture upload, Cloud-orchestrated native analysis and deterministic Cloud simulation ([SIM-01](#rule-sim-01)–[SIM-20](#rule-sim-20)) |

---

## 24. Reference relationship

**Serial-Studio is the ArcScope reference** (**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**) — a source of features, behaviour, tests and possibly reusable material, **never an architecture authority or a parity commitment**.

| # | Requirement |
|---|---|
| RF-01 | **Its licence must be re-verified against the local repository baseline with file-level SPDX evidence**, not against a repository-root licence or an external page — the **[F-013](../../assurance/open-gates-register.md#rule-f-013)** gate (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). |
| RF-02 | An **ArcScope Reference Coverage Matrix** is required before ArcScope implementation planning is finalised, mapping each feature to Copy / Rewrite / Improve / Replace / Reference Only / Drop, to a target ArcScope module and path, to temporary/permanent/replacement status, to V1 or later, and to a test and completion gate. |
| RF-03 | **Protocol, transport and format areas — messaging protocols, fieldbus and CAN handling, measurement data formats, reporting, database logging, and 3D/XY/waterfall visualisation — are audited file by file for licence and origin.** Licence analysis must not silently abandon a confirmed reuse strategy, and commercial release must close NOTICE, source records, retained content and mandatory-replacement obligations. |
| RF-04 | **The target runtime architecture is ArcForges' own** — C#, Avalonia, Native AOT, its own domain model, acquisition pipeline and visualisation system. |

---

## 25. Acceptance scenarios

**Source and connection** — a stored profile connects and disconnects; a profile edit does not change a historical session's recorded configuration; a disconnect leaves the session open with an explicit gap; a second capture cannot silently seize an exclusive source.

**Capture** — pausing the view does not stop recording; an interrupted capture retains its durable data and is marked interrupted, not failed; a crash mid-capture recovers to the last committed boundary with an honest end marker; an acquisition overrun is surfaced rather than hidden.

**Evidence** — a finalised raw capture cannot be silently modified; a trim creates a derived representation; a decoder result never overwrites raw data.

**Time** — source and host time are both retained; multi-source alignment changes views without changing raw timestamps; time uncertainty is expressible.

**Signals and events** — boolean, integer and enumerated signals all work; irregular sampling works; a display unit change does not alter the stored value; producing a converted series creates a derived signal.

**Visualisation** — incompatible dimensions do not share an axis by default; measurements use canonical data, not decimated screen data; an approximate measurement is labelled; a range selection is a stable, passable context.

**Trigger** — a threshold trigger captures pre- and post-windows; a trigger occurrence records the effective definition; the trigger changes no samples.

**Measurement and analysis** — every result carries units and scope; an analysis is reproducible from its stored definition and inputs; a recipe applies to another session.

**Decoder** — a decoder chain works; malformed frames are reported with counts; a decoder version change does not rewrite past results.

**Annotation** — an agent-created finding is labelled as agent-produced with its task and evidence; annotations change no data.

**Comparison** — alignment is explicit and stored; comparison produces no merged authoritative dataset; incompatible units block automatic comparison.

**Report** — sources are traceable to session, range, configuration and analysis version; sending a report to ArcNotes creates a new ArcNotes-owned document with provenance, and the ArcScope report remains.

**Export** — CSV precision loss is declared; native export round-trips; a collect bundle is portable and non-destructive.

**AI** — a numeric claim carries a citation; the raw capture is never sent to a model; a local-only capture is not uploaded by pressing an AI button; the scope used is visible.

**Cloud** — enabling project sync uploads no raw capture; a session with cloud metadata and missing local raw data presents clearly, not as corruption; remote analysis runs on the desktop rather than uploading the data.

**Simulator** — [SIM-20](#rule-sim-20) exercises the actual host, storage and native source adapter. Reproducing simulated faults requires no physical hardware, AI access or always-online desktop.

**Safety UI** — the recording indicator is unmistakable; closing a window during capture asks; background capture ends when work ends.

---

## 26. Traceability

| Current document | Relationship |
|---|---|
| [Native Interoperability and Media Architecture](../../architecture/12-native-interop-and-media.md) | Defines native acquisition and evidence boundaries |
| [Cloud Simulator, Time Model and OTIO Interchange](../../architecture/23-simulator-and-interchange.md) | Defines deterministic Cloud simulation |
| [Reference Coverage Matrix — ArcScope / Serial-Studio](../../assurance/reference-coverage/arcscope-serial-studio.md) | Records source dispositions, licence boundaries and verification oracles |
| **[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)** | ArcScope is independently defined; ArcImage concepts must not migrate into it |
| **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** | Serial-Studio as a licence-gated reference with a required file-level audit |
