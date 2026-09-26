# ArcScope — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Acquisition and sessions, analysis and reporting, integration and metadata sync.

Tasks: 27 · Owning repositories: ArcScope · Integration owner(s): ArcScope integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [SCOPE.01](#task-scope-01) | DataSource/SourceAdapter contract, connection profiles and lease/busy exclusivity | feature | M | [PLT.01](platform.md#task-plt-01) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [SCOPE.02](#task-scope-02) | Channel, signal, event and time model | feature | M | [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [SCOPE.03](#task-scope-03) | Network and file-replay source adapters (TCP, UDP, file stream) | feature | M | [SCOPE.01](#task-scope-01) (artifact) | not-started |
| [SCOPE.04](#task-scope-04) | Serial and USB instrument adapters | feature | M | [SCOPE.01](#task-scope-01) (artifact), [NAT.13](native.md#task-nat-13) (artifact) | not-started |
| [SCOPE.05](#task-scope-05) | Acquisition pipeline: bounded loop, ring buffer, backpressure and overrun accounting | feature | L | [SCOPE.01](#task-scope-01) (artifact), [SCOPE.02](#task-scope-02) (artifact), [SCOPE.03](#task-scope-03) (artifact) | not-started |
| [SCOPE.06](#task-scope-06) | Session and capture lifecycle: segments, gaps and live observation | feature | L | [SCOPE.05](#task-scope-05) (artifact), [SCOPE.02](#task-scope-02) (artifact) | not-started |
| [SCOPE.07](#task-scope-07) | Durable capture writer, chunked verifiable store and crash recovery | feature | L | [SCOPE.06](#task-scope-06) (artifact), [PLT.06](platform.md#task-plt-06) (artifact) | not-started |
| [SCOPE.08](#task-scope-08) | Replay as a source (capture-level) | feature | M | [SCOPE.07](#task-scope-07) (artifact), [SCOPE.01](#task-scope-01) (artifact) | not-started |
| [SCOPE.09](#task-scope-09) | Long-running capture in the shell | feature | S | [SCOPE.06](#task-scope-06) (artifact), [PLT.32](platform.md#task-plt-32) (artifact) | not-started |
| [SCOPE.10](#task-scope-10) | Reference drift check against Serial-Studio 639daafb | feature | S | none | not-started |
| [SCOPE.11](#task-scope-11) | Owned-artifact verification and real hardware integration | feature | M | [SCOPE.01](#task-scope-01) (artifact), [SCOPE.02](#task-scope-02) (artifact), [SCOPE.03](#task-scope-03) (artifact), [SCOPE.04](#task-scope-04) (artifact), [SCOPE.05](#task-scope-05) (artifact), [SCOPE.06](#task-scope-06) (artifact), [SCOPE.07](#task-scope-07) (artifact), [SCOPE.08](#task-scope-08) (artifact), [SCOPE.09](#task-scope-09) (artifact), [SCOPE.10](#task-scope-10) (artifact), [NAT.24](native.md#task-nat-24) (artifact) | not-started |
| [SCOPE.12](#task-scope-12) | Visualisation: virtualised rendering, downsampling, cursors and markers | feature | L | [SCOPE.02](#task-scope-02) (artifact), [SCOPE.06](#task-scope-06) (artifact) | not-started |
| [SCOPE.13](#task-scope-13) | Triggers with pre/post windows | feature | M | [SCOPE.05](#task-scope-05) (artifact), [SCOPE.06](#task-scope-06) (artifact) | not-started |
| [SCOPE.14](#task-scope-14) | Measurements: scope.measurement.v1 | feature | L | [CON.91](contracts.md#task-con-91) (contract), [SCOPE.02](#task-scope-02) (artifact), [SCOPE.06](#task-scope-06) (artifact) | not-started |
| [SCOPE.15](#task-scope-15) | Decoder framework and first-party protocol decoders | feature | M | [SCOPE.06](#task-scope-06) (artifact) | not-started |
| [SCOPE.16](#task-scope-16) | Analysis definitions and recipes as native ProductJobs | feature | L | [SCOPE.14](#task-scope-14) (artifact), [SCOPE.15](#task-scope-15) (artifact) | not-started |
| [SCOPE.17](#task-scope-17) | Annotations, findings and session/capture comparison | feature | M | [SCOPE.06](#task-scope-06) (artifact) | not-started |
| [SCOPE.18](#task-scope-18) | Reports and reproducibility | feature | L | [SCOPE.14](#task-scope-14) (artifact), [SCOPE.15](#task-scope-15) (artifact), [SCOPE.16](#task-scope-16) (artifact), [SCOPE.17](#task-scope-17) (artifact) | not-started |
| [SCOPE.19](#task-scope-19) | Owned-artifact verification and real integration | feature | M | [SCOPE.12](#task-scope-12) (artifact), [SCOPE.13](#task-scope-13) (artifact), [SCOPE.14](#task-scope-14) (artifact), [SCOPE.15](#task-scope-15) (artifact), [SCOPE.16](#task-scope-16) (artifact), [SCOPE.17](#task-scope-17) (artifact), [SCOPE.18](#task-scope-18) (artifact) | not-started |
| [SCOPE.20](#task-scope-20) | ArcChat capability surface for ArcScope | feature | M | [SCOPE.06](#task-scope-06) (artifact), [CON.02](contracts.md#task-con-02) (contract) | not-started |
| [SCOPE.21](#task-scope-21) | Bounded context provision for AI | feature | M | [SCOPE.14](#task-scope-14) (artifact), [SCOPE.16](#task-scope-16) (artifact), [SCOPE.15](#task-scope-15) (artifact) | not-started |
| [SCOPE.22](#task-scope-22) | Cloud sync scope (metadata, not raw capture) | feature | M | [SCOPE.06](#task-scope-06) (artifact), [SCOPE.18](#task-scope-18) (artifact), [SCOPE.17](#task-scope-17) (artifact) | not-started |
| [SCOPE.23](#task-scope-23) | Explicit per-session raw capture upload | feature | M | [SCOPE.07](#task-scope-07) (artifact), [CLOUD.42](cloud.md#task-cloud-42) (artifact) | not-started |
| [SCOPE.24](#task-scope-24) | Import, export and format fixtures | feature | L | [SCOPE.07](#task-scope-07) (artifact), [SCOPE.14](#task-scope-14) (artifact) | not-started |
| [SCOPE.25](#task-scope-25) | Extension boundary: no third-party raw-capture write path | feature | S | [SCOPE.20](#task-scope-20) (artifact), [SCOPE.07](#task-scope-07) (artifact), [EXT.02](extensions.md#task-ext-02) (artifact) | not-started |
| [SCOPE.26](#task-scope-26) | Owned-artifact verification and real integration | feature | M | [SCOPE.20](#task-scope-20) (artifact), [SCOPE.21](#task-scope-21) (artifact), [SCOPE.22](#task-scope-22) (artifact), [SCOPE.23](#task-scope-23) (artifact), [SCOPE.24](#task-scope-24) (artifact), [SCOPE.25](#task-scope-25) (artifact) | not-started |
| [SCOPE.27](#task-scope-27) | Real ArcScope metadata sync against the deployed Cloud sync engine | integration | M | [SCOPE.22](#task-scope-22) (artifact), [CLOUD.39](cloud.md#task-cloud-39) (artifact), [CLOUD.44](cloud.md#task-cloud-44) (artifact) | not-started |

## Tasks

<a id="task-scope-01"></a>

### SCOPE.01 — DataSource/SourceAdapter contract, connection profiles and lease/busy exclusivity

**Outcome.** A single adapter contract (DataSource/SourceAdapter/Connection) exists with persisted, reusable connection profiles; editing a profile never rewrites a historical session's recorded configuration; a second claimant on the same source is refused with a busy state.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-01` and ledger record `ledger/tasks/scope-01.md` in the Plan repository; task branch `task/scope-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-33.00](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) — shared adapter contract; ConnectionProfile storage/reuse; EffectiveConfigurationSnapshot immutability on profile edit; lease/busy exclusivity model ([BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)..[BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06), [BR-09](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-09)) |
| Provides | scope.source-adapter-contract; scope.connection-profile |
| Start prerequisites | **artifact** [PLT.01](platform.md#task-plt-01) — published store abstraction with the single write path (for ArcScope's own profile/session store). *Why:* connection profiles and effective configuration snapshots are persisted data; [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) requires historical sessions to be structurally immune to later profile edits, which needs the real single-writer store, not an in-memory stub, to prove durability/isolation honestly<br>**contract** [CON.91](contracts.md#task-con-91) — published Contracts records for capture/session identifiers referenced by ConnectionProfile. *Why:* the adapter contract's identifiers must be the real published shapes so downstream ArcScope projects and any future Cloud/AI consumer are wire-compatible from the start, not a locally invented shape that is rewritten later |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.03](#task-scope-03), [SCOPE.04](#task-scope-04), [SCOPE.05](#task-scope-05), [SCOPE.08](#task-scope-08), [SCOPE.11](#task-scope-11), [SIM.06](simulator.md#task-sim-06) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Domain/**`<br>`ArcScope:src/ArcScope/ArcScope.Acquisition/Adapters/Contract/**`<br>`ArcScope:tests/ArcScopePipelineTests/Adapters/**` |
| Shared resources | [RES-arcscope-migrations](../shared-resources.md#res-arcscope-migrations) (append) |
| Validation | offline unit/integration tests only (profile-edit immutability test, exclusivity test with two claimants); no live Cloud or hardware required at this stage |
| Completion evidence | adapter-contract conformance tests, profile immutability test, exclusivity busy-state test |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: ArcScope repo (HEAD 5e68634) contains only the Hello World bootstrap (ArcForges.ArcScope.Core, ArcForges.ArcScope); none of ArcScope.Domain/.Acquisition/.Recording exist yet |
| Notes | Foundational; SCOPE.03 (network/replay adapters) and SCOPE.04 (serial/USB adapters) both implement this contract and can proceed in parallel once it lands. |

<a id="task-scope-02"></a>

### SCOPE.02 — Channel, signal, event and time model

**Outcome.** A precise time model spanning signal samples and discrete events with exact rate representation, explicit conversion between domains, and explicit recorded alignment between sources.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-02` and ledger record `ledger/tasks/scope-02.md` in the Plan repository; task branch `task/scope-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-33.03](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.03) — full |
| Provides | scope.time-channel-model |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — published numeric/time wire types (rate, timestamp, duration) Channel/Signal/EventRecord must serialise as. *Why:* the time model's exactness/conversion guarantees are meaningless if the wire representation is invented locally and later has to be retrofitted to the real numbered wire profile |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.05](#task-scope-05), [SCOPE.06](#task-scope-06), [SCOPE.11](#task-scope-11), [SCOPE.12](#task-scope-12), [SCOPE.14](#task-scope-14) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Domain/Time/**`<br>`ArcScope:src/ArcScope/ArcScope.Domain/Channels/**`<br>`ArcScope:tests/ArcScopePipelineTests/TimeModel/**` |
| Validation | offline unit tests: precision across rate domains, alignment with two sources, conversion exactness — pure math, no external environment |
| Completion evidence | precision/alignment/conversion test results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no Channel/Signal/time types exist in the repo yet |
| Notes | Pure domain/math task with no native or Cloud dependency; runs fully in parallel with SCOPE.01 (different files, same repo) — a clean simultaneous-execution example. |

<a id="task-scope-03"></a>

### SCOPE.03 — Network and file-replay source adapters (TCP, UDP, file stream)

**Outcome.** TCP, UDP and file-stream-replay adapters work over real transports (pure managed sockets/file I/O), pass connect/disconnect/reconnect tests, and share SCOPE.01's profile and exclusivity model.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-03` and ledger record `ledger/tasks/scope-03.md` in the Plan repository; task branch `task/scope-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-33.00](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) — TCP/UDP/file-replay concrete adapters over the shared contract; real-transport connect/disconnect/reconnect tests |
| Provides | scope.adapters.network-file |
| Start prerequisites | **artifact** [SCOPE.01](#task-scope-01) — DataSource/SourceAdapter contract and connection profile model. *Why:* concrete adapters implement the shared contract; cannot be written before it exists |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.05](#task-scope-05), [SCOPE.11](#task-scope-11) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Acquisition/Adapters/Network/**`<br>`ArcScope:src/ArcScope/ArcScope.Acquisition/Adapters/FileReplay/**`<br>`ArcScope:tests/ArcScopePipelineTests/Adapters/Network/**` |
| Validation | real-transport tests using.NET Socket/TcpListener/UdpClient loopback and local files — no native dependency, no emulator/CI restriction applies; proportionate under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | per-adapter real-transport connect/disconnect/reconnect results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no adapters exist yet |
| Notes | This is the implementation-sequence.md §3 'must be real early' item: real serial/TCP/UDP transports must not be mocked. |

<a id="task-scope-04"></a>

### SCOPE.04 — Serial and USB instrument adapters

**Outcome.** Serial and USB adapters work over real hardware transports via the native ArcInstruments ABI, enumerate/open/transfer/cancel correctly, refuse busy/permission conflicts per Tier-1 RID, and record a hot-unplug as an explicit capture gap.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-04` and ledger record `ledger/tasks/scope-04.md` in the Plan repository; task branch `task/scope-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-33.00](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) — serial/USB concrete adapters over the shared contract<br>[WP-33.90](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.90) — generic-USB-V1 body text (enumeration, explicit interface/endpoint open, control/bulk/interrupt transfers, partial writes, cancellation, driver/permission/busy refusal per Tier 1 RID; no automatic kernel-driver detach; hot unplug records an explicit capture gap) — this text sits orphaned between [WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) §6 and §7 in the source doc with no substep id of its own; folded here since it is entirely about the serial/USB adapter, not §33.90's own verify-and-integration content<br>[WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) orphaned 'Generic USB is V1' body text (enumeration/open/transfer/cancel/refusal per Tier-1 RID, no auto kernel-driver detach, hot-unplug=explicit gap) sitting between §6 Impacts and §7 Tests with no substep id — package-level obligation contribution |
| Provides | scope.adapters.serial-usb |
| Start prerequisites | **artifact** [SCOPE.01](#task-scope-01) — DataSource/SourceAdapter contract and connection profile model. *Why:* concrete adapters implement the shared contract<br>**artifact** [NAT.13](native.md#task-nat-13) — published ArcInstrumentsNative package (arc_instruments_* ABI) — at minimum its fixture/simulated-hardware tier build. *Why:* [BR-10](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-10) confines the acquisition loop/lifecycle to C# and restricts native code to transport, device access, timestamps and primitives only; DesktopPlatform HEAD fe8476d has no arc_instruments ABI at all yet (grep for 'instrument' is empty) — this is a genuine not-yet-produced artifact, not a design gap. |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.11](#task-scope-11) |
| Permitted substitutes | [SUB-scope-instruments-fixture](../substitutes.md#sub-scope-instruments-fixture) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Acquisition/Adapters/Instruments/**`<br>`ArcScope: src/ArcScope/ArcScope.Native/**`<br>`ArcScope:tests/ArcScopePipelineTests/Adapters/Instruments/**` |
| Validation | fixture/simulated-hardware unit tests at this task's own gate; real per-RID hardware acceptance deferred to SCOPE.11/[PG-08](../../../assurance/open-gates-register.md#rule-pg-08) per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no device/hardware CI) |
| Completion evidence | enumeration/open/transfer/cancel/refusal results against fixture tier now; real-hardware receipt at SCOPE.11 |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no serial/USB adapter code exists; [WP-13.12](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.12) producer itself not started (DesktopPlatform has no arc_instruments ABI directory) |
| Notes | This is the one [WP-33.00](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) sub-path that genuinely needs a WP13 native family, and only [WP-13.12](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.12) (not the whole WP13 package). It is the correct place to attach [PG-08](../../../assurance/open-gates-register.md#rule-pg-08)'s per-RID USB acceptance text, which the source document places oddly (orphaned paragraph after [WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) §6, before §7) with no substep id. |

<a id="task-scope-05"></a>

### SCOPE.05 — Acquisition pipeline: bounded loop, ring buffer, backpressure and overrun accounting

**Outcome.** A bounded, timestamped acquisition loop with explicit backpressure sustains throughput above the product target with bounded memory; every overrun is counted, timestamped and recorded; hardware timestamps are preserved where available and the timing source/uncertainty is recorded otherwise.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-05` and ledger record `ledger/tasks/scope-05.md` in the Plan repository; task branch `task/scope-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-33.01](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.01) — full |
| Provides | scope.acquisition-pipeline; scope.rolling-buffer |
| Start prerequisites | **artifact** [SCOPE.01](#task-scope-01) — source adapter contract. *Why:* the loop consumes adapters through the shared contract, not a concrete adapter type<br>**artifact** [SCOPE.02](#task-scope-02) — time/channel model. *Why:* timestamping and rate/conversion semantics are the time model's types; the loop cannot record exact timestamps against an undefined model<br>**artifact** [SCOPE.03](#task-scope-03) — at least one real concrete adapter (network) to drive throughput/overrun tests. *Why:* sustained-throughput and induced-overrun acceptance need a real transport; TCP/UDP is the cheapest real one and must be real early regardless, so it is the natural throughput-test source rather than waiting for serial/USB |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.06](#task-scope-06), [SCOPE.11](#task-scope-11), [SCOPE.13](#task-scope-13) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Acquisition/Pipeline/**`<br>`ArcScope:tests/ArcScopePipelineTests/Throughput/**` |
| Validation | sustained-throughput runs with recorded rate/memory/drop counts; induced overrun; timing-source assertions — local, offline, repeatable |
| Completion evidence | throughput/memory/overrun/timing-source results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [WP-13.02](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.02) ('Probe C: high-throughput acquisition', the native and runtime-proof lanes/WP13) is a near-identical early risk proof of the same ring-buffer/throughput/overrun approach, done earlier and cheaper. It validates the approach but ships no reusable package ([BR-10](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-10) keeps the real loop in C# here regardless) — treated as an informative precedent, not a start edge. |

<a id="task-scope-06"></a>

### SCOPE.06 — Session and capture lifecycle: segments, gaps and live observation

**Outcome.** The session/capture lifecycle (armed, running, paused, stopped, finalised, interrupted) is correct; captures are sequences of segments plus explicit gaps; pausing the view never stops recording; a disconnect produces an explicit gap rather than a truncated capture.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-06` and ledger record `ledger/tasks/scope-06.md` in the Plan repository; task branch `task/scope-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-33.02](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.02) — full |
| Provides | scope.session-capture-lifecycle |
| Start prerequisites | **artifact** [SCOPE.05](#task-scope-05) — acquisition pipeline and rolling buffer. *Why:* live observation reads the rolling buffer; record capture consumes the same pipeline output<br>**artifact** [SCOPE.02](#task-scope-02) — time/channel model. *Why:* segments and gaps are time-model objects |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.07](#task-scope-07), [SCOPE.09](#task-scope-09), [SCOPE.11](#task-scope-11), [SCOPE.12](#task-scope-12), [SCOPE.13](#task-scope-13), [SCOPE.14](#task-scope-14), [SCOPE.15](#task-scope-15), [SCOPE.17](#task-scope-17), [SCOPE.20](#task-scope-20), [SCOPE.22](#task-scope-22) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Domain/Session/**`<br>`ArcScope:src/ArcScope/ArcScope.Domain/Capture/**`<br>`ArcScope:tests/ArcScopePipelineTests/Lifecycle/**` |
| Shared resources | [RES-arcscope-migrations](../shared-resources.md#res-arcscope-migrations) (append) |
| Validation | lifecycle coverage including interruption; pause-view-while-recording test; segment/gap integrity after disconnect — offline |
| Completion evidence | lifecycle, pause-view and gap-integrity results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-07"></a>

### SCOPE.07 — Durable capture writer, chunked verifiable store and crash recovery

**Outcome.** Raw capture is written to the chunked verifiable store with per-chunk checksums and an explicit end marker; a finalised capture is structurally immutable; a crash mid-capture recovers to the last committed boundary with an honest end marker and recorded loss.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-07` and ledger record `ledger/tasks/scope-07.md` in the Plan repository; task branch `task/scope-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-33.04](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.04) — full |
| Provides | scope.durable-capture-store |
| Start prerequisites | **artifact** [SCOPE.06](#task-scope-06) — session/capture lifecycle types. *Why:* the writer persists Capture/CaptureSegment objects defined there<br>**artifact** [PLT.06](platform.md#task-plt-06) — published chunked/large-append verifiable store primitive. *Why:* [BR-11](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-11) forbids database blobs for raw capture; this is a real evidence-integrity requirement (immutability, per-chunk checksum, crash-boundary recovery) that a hand-rolled substitute would not honestly prove — the substitute rules treat evidence-integrity storage as a case where a substitute is not acceptable |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.08](#task-scope-08), [SCOPE.11](#task-scope-11), [SCOPE.23](#task-scope-23), [SCOPE.24](#task-scope-24), [SCOPE.25](#task-scope-25) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Recording/**`<br>`ArcScope:src/ArcScope/ArcScope.Infrastructure/CaptureStore/**`<br>`ArcScope:tests/ArcScopePipelineTests/DurableCapture/**` |
| Validation | kill-during-capture at chunk boundaries and mid-chunk; recovered-prefix verification; immutability test — offline, deterministic fault injection, no live environment needed |
| Completion evidence | crash-recovery prefix verification and immutability results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [WP-07.05](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.05) is named precisely (not 'whole WP07') because [WP-07.00](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.00)/.03 (store abstraction, migrations) are consumed earlier by SCOPE.01/06 for ordinary relational state, while raw capture specifically needs the large-append/chunked primitive. |

<a id="task-scope-08"></a>

### SCOPE.08 — Replay as a source (capture-level)

**Outcome.** Replay of a recorded, finalised capture feeds the same pipeline as a labelled ReplaySource, always recording its origin, and never presents device-only fields as measured.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-08` and ledger record `ledger/tasks/scope-08.md` in the Plan repository; task branch `task/scope-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-33.05](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.05) — full |
| Provides | scope.replay-source |
| Start prerequisites | **artifact** [SCOPE.07](#task-scope-07) — durable, finalised captures to replay. *Why:* replay reads a finalised capture from the chunked store; cannot be built before that store and finalisation exist<br>**artifact** [SCOPE.01](#task-scope-01) — source adapter contract. *Why:* replay is implemented as a SourceAdapter feeding the ordinary pipeline ([BR-08](../../../architecture/14-build-packaging-and-release.md#rule-br-08)) |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.11](#task-scope-11) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Acquisition/Adapters/Replay/**`<br>`ArcScope:tests/ArcScopePipelineTests/Replay/**` |
| Validation | replay-equivalence test against a recorded capture; labelling assertion; negative test for absent device-only fields |
| Completion evidence | replay equivalence and labelling results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This is [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34)'s repeatable source ([SD-09](../../../assurance/reference-coverage/distribution-startarcforges.md#rule-sd-09)): once this task lands, [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34)'s reproducibility/analysis tasks can develop and verify against real recorded+replayed captures without any Cloud simulator. |

<a id="task-scope-09"></a>

### SCOPE.09 — Long-running capture in the shell

**Outcome.** Recording state is permanently visible; closing a window during capture always asks with consequences stated, never silently stopping or continuing; background capture persists only while genuine work is active.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-09` and ledger record `ledger/tasks/scope-09.md` in the Plan repository; task branch `task/scope-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-33.06](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.06) — full |
| Provides | scope.capture-shell-integration |
| Start prerequisites | **artifact** [SCOPE.06](#task-scope-06) — capture lifecycle (running/interrupted states) to bind the shell prompt to. *Why:* the close-prompt decision depends on live capture state<br>**artifact** [PLT.32](platform.md#task-plt-32) — published generic shell lifecycle/shutdown-prompt mechanism. *Why:* [WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) §2 lists [WP-10](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10) shell output as a required input; this substep specialises the generic close/shutdown prompt for capture-in-progress rather than inventing a second prompt mechanism |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.56](platform.md#task-plt-56), [SCOPE.11](#task-scope-11) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Presentation/**`<br>`ArcScope:src/ArcScope/ArcScope.Desktop/CaptureLifecycle/**` |
| Validation | window-close-during-capture prompt test; background-residency test; visibility assertion — desktop-GUI-adjacent, kept to the offline/local tier per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no desktop GUI CI; local manual/scripted verification) |
| Completion evidence | window-close, background and visibility results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | The old upstream edge [WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33)<-26 (remote action/tool bridge) does not apply here or anywhere else in WP33: [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) is about remote-triggered tool execution on a running instance (durable target queue, owner reauth, remote approval), and none of WP-33.00-33.07's substep bodies mention it.. |

<a id="task-scope-10"></a>

### SCOPE.10 — Reference drift check against Serial-Studio 639daafb

**Outcome.** A drift report exists comparing the reference against the bound commit, covering changed rows, newly introduced upstream material (mapped to an existing requirement or recorded as an accepted exclusion) and licence re-verification; every changed/new item carries a disposition.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-10` and ledger record `ledger/tasks/scope-10.md` in the Plan repository; task branch `task/scope-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-33.07](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.07) — full |
| Provides | scope.reference-drift-report |
| Start prerequisites | none |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.11](#task-scope-11) |
| Write scope | `Design:docs/assurance/reference-coverage/arcscope-serial-studio.md` |
| Shared resources | [RES-design-evidence](../shared-resources.md#res-design-evidence) (append) |
| Validation | a completeness check that every changed/new item has a disposition; no code build required |
| Completion evidence | drift report: changed rows, newly introduced material with assessment, licence comparison |
| Baseline (unreviewed unless accepted) | not-started The reference matrix is accepted design-stage evidence; the implementation-time drift check itself has not run. |
| Notes | Has no real code dependency on any other SCOPE task; can run at any time, though it is most useful shortly before SCOPE.11/[WP-33.90](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.90) closes so any licence correction lands before the package gate. |

<a id="task-scope-11"></a>

### SCOPE.11 — Owned-artifact verification and real hardware integration

**Outcome.** The [WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) candidate closes: real packaged hardware-path and throughput/overrun/recovery acceptance recorded, no automatic upload of raw acquisition data, [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) and [PG-03](../../../assurance/open-gates-register.md#rule-pg-03) evidence recorded for every producer this package owns.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-11` and ledger record `ledger/tasks/scope-11.md` in the Plan repository; task branch `task/scope-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Package acceptance | Records the [WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-33.90](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.90) — full (excluding the generic-USB-V1 body text folded into SCOPE.04)<br>[WP-33](../../work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required-behavior-and-closure section (acquisition.source/framing/trigger profiles, gap/loss/durable-capture manifests, all accepted serial/network/file/USB sources) — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required-behavior-and-closure section: acquisition.source/framing/trigger profiles, gap/loss/durable-capture manifests, all accepted serial/network/file/USB sources, independent positive/negative vectors, actual owner integration |
| Provides | scope.wp33-accepted-candidate |
| Start prerequisites | **artifact** [SCOPE.01](#task-scope-01) — all WP33 tasks complete to assemble. *Why:* verify task<br>**artifact** [SCOPE.02](#task-scope-02) — as above. *Why:* as above<br>**artifact** [SCOPE.03](#task-scope-03) — as above. *Why:* as above<br>**artifact** [SCOPE.04](#task-scope-04) — as above. *Why:* as above<br>**artifact** [SCOPE.05](#task-scope-05) — as above. *Why:* as above<br>**artifact** [SCOPE.06](#task-scope-06) — as above. *Why:* as above<br>**artifact** [SCOPE.07](#task-scope-07) — as above. *Why:* as above<br>**artifact** [SCOPE.08](#task-scope-08) — as above. *Why:* as above<br>**artifact** [SCOPE.09](#task-scope-09) — as above. *Why:* as above<br>**artifact** [SCOPE.10](#task-scope-10) — drift report disposition (must be clean or corrected per [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001) before dependent work continues). *Why:* a changed licence position must correct affected rows before this package closes<br>**artifact** [NAT.24](native.md#task-nat-24) — published Instruments runtime packages. *Why:* hardware-tier acquisition evidence uses the real native family |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.02](release.md#task-rel-02) |
| Write scope | `ArcScope:docs/wp-33-integration-receipt.md` |
| Validation | real packaged hardware-path and throughput/overrun/recovery acceptance; offline-acceptance-matrix rows (fresh shell, hydrated outage, unavailable content, signout, restart) where applicable; no macOS CI, no device/emulator CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) — evidence is recorded from local/lab runs |
| Completion evidence | owned-artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations, real-vs-fixture status |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-12"></a>

### SCOPE.12 — Visualisation: virtualised rendering, downsampling, cursors and markers

**Outcome.** Time-series and event visualisation meets the responsiveness budget at corpus scale with virtualised rendering and downsampling; the display explicitly discloses when it is downsampled; cursor readings are exact regardless of display resolution.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-12` and ledger record `ledger/tasks/scope-12.md` in the Plan repository; task branch `task/scope-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-34.00](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.00) — full |
| Provides | scope.visualisation |
| Start prerequisites | **artifact** [SCOPE.02](#task-scope-02) — time/channel model. *Why:* plots render Channel/Signal/time-domain data<br>**artifact** [SCOPE.06](#task-scope-06) — session/capture to visualise. *Why:* visualisation reads captures |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.19](#task-scope-19) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Visualization/**`<br>`ArcScope:tests/ArcScopePipelineTests/Visualization/**` |
| Validation | scale-corpus interaction measurements; downsampling-disclosure assertion; downsampled-vs-full-resolution cursor correctness — desktop rendering kept to local/offline tier per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | responsiveness, disclosure and cursor-exactness results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | RESOLVED FINDING, not an edge: the assignment hint suggested this might need the [WP-13.14](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.14) Graphics native family (arc_graphics_* ABI). Checked 12-native-interop-and-media.md (the ArcScope native-interop authority, §8) directly: zero mentions of Graphics; its native surface is device/transport/high-rate acquisition primitives only. The Graphics native family's real consumer is ArcSlate (per the native and runtime-proof lanes' own contracts note: 'used by ArcSlate mainly'). ArcScope already carries Avalonia (Skia-based managed rendering, see ArcScope third-party/Avalonia.LICENSE.txt), which is sufficient for plotting/downsampling in pure C#. |

<a id="task-scope-13"></a>

### SCOPE.13 — Triggers with pre/post windows

**Outcome.** Triggers control capture and mark significant time events with exact pre- and post-trigger windows served by the rolling buffer; samples are provably unmodified; trigger storms are bounded.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-13` and ledger record `ledger/tasks/scope-13.md` in the Plan repository; task branch `task/scope-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-34.01](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.01) — full |
| Provides | scope.triggers |
| Start prerequisites | **artifact** [SCOPE.05](#task-scope-05) — rolling buffer. *Why:* pre/post windows are served from it<br>**artifact** [SCOPE.06](#task-scope-06) — capture lifecycle. *Why:* triggers mark time within a running capture |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.19](#task-scope-19) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Domain/Triggers/**`<br>`ArcScope:tests/ArcScopePipelineTests/Triggers/**` |
| Validation | pre/post-window correctness; data-immutability assertion; trigger-storm bound test — offline |
| Completion evidence | trigger window, immutability and storm-bound results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-14"></a>

### SCOPE.14 — Measurements: scope.measurement.v1

**Outcome.** Every measurement family in scope.measurement.v1 reproduces under its recorded profile/configuration within the declared numerical tolerance, with units and precision stated; independent reference values (including the Pearson r=1/r=-1 vectors and constant-input-unavailable case) pass.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-14` and ledger record `ledger/tasks/scope-14.md` in the Plan repository; task branch `task/scope-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-34.02](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.02) — full, including the required-design-implementation text: every basic family via declared population/sample-weighted formulas, half-open input selection, calibrated units, coverage/status rules, recorded pulse thresholds/interpolation, independent statistical hand-calculation and digital/analog/gap vectors<br>[WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) orphaned §6/§7 body text: 'Pearson independent vectors: x=[1,2,3], y=[2,4,6] gives r=1; y=[3,2,1] gives r=-1. Constant input is unavailable; preserve the declared lag and overlap rules' — a concrete correlation-family acceptance vector with no substep id of its own — orphaned §6/§7 body text: 'Pearson independent vectors: x=[1,2,3], y=[2,4,6] gives r=1; y=[3,2,1] gives r=-1. Constant input is unavailable; preserve the declared lag and overlap rules' — a concrete correlation-family acceptance vector with no substep id of its own; package-level obligation contribution<br>[WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) §8 additional completion requirement: every basic family has its formula/status oracle; reproduction uses the defined tolerance rather than an undefined byte-equality claim — §8 additional completion requirement: every basic family has its formula/status oracle; reproduction uses the defined tolerance rather than an undefined byte-equality claim; package-level obligation contribution |
| Provides | scope.measurements |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — the published scope.measurement.v1 profile (families, formulas, units, coverage/status rules) in Contracts. *Why:* [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) §2 states this is a frozen design input owned by Contracts; the measurement implementation is a direct realisation of that published profile, not a locally re-derived one<br>**artifact** [SCOPE.02](#task-scope-02) — time/channel model. *Why:* measurements operate over signals/events defined there<br>**artifact** [SCOPE.06](#task-scope-06) — capture/configuration snapshot. *Why:* a measurement records the configuration under which it was taken ([BR-05](../../../architecture/14-build-packaging-and-release.md#rule-br-05)) |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.16](#task-scope-16), [SCOPE.18](#task-scope-18), [SCOPE.19](#task-scope-19), [SCOPE.21](#task-scope-21), [SCOPE.24](#task-scope-24), [SIM.06](simulator.md#task-sim-06), [SIM.09](simulator.md#task-sim-09) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Analysis/Measurements/**`<br>`ArcScope:tests/ArcScopePipelineTests/Measurements/**` |
| Validation | reference-value tests per measurement kind; unit-handling test; reproduction-from-recorded-configuration test — offline, deterministic tolerance-based comparison |
| Completion evidence | measurement reference and reproduction results, including the Pearson vectors |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-15"></a>

### SCOPE.15 — Decoder framework and first-party protocol decoders

**Outcome.** A versioned decoder framework produces structured events (never raw channel data); malformed frames, checksum failures and unknown fields are surfaced with counts/locations; no decoder has a device-write path.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-15` and ledger record `ledger/tasks/scope-15.md` in the Plan repository; task branch `task/scope-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-34.03](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.03) — full |
| Provides | scope.decoders |
| Start prerequisites | **artifact** [SCOPE.06](#task-scope-06) — capture/channel data to decode. *Why:* decoders consume captured channel data |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.16](#task-scope-16), [SCOPE.18](#task-scope-18), [SCOPE.19](#task-scope-19), [SCOPE.21](#task-scope-21) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Decoders/**`<br>`ArcScope:tests/ArcScopePipelineTests/Decoders/**` |
| Validation | per-decoder fixture corpora including malformed input; error-visibility assertion; structural no-device-write test — offline |
| Completion evidence | per-decoder fixtures, error visibility and no-write assertion |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Independent of SCOPE.14 (measurements); the two can proceed in parallel. Decoder scope (UART/I2C/SPI) is fixed by the already-frozen analysis.v1 profile in architecture doc 26-product-behavior-profiles.md — note this is the ARCHITECTURE document numbered 26, unrelated to [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) (Remote action and tool bridge); no start edge needed since the design is already frozen, not missing. |

<a id="task-scope-16"></a>

### SCOPE.16 — Analysis definitions and recipes as native ProductJobs

**Outcome.** Versioned analysis definitions compose into recipes; results are derived data reconstructable from evidence plus configuration; long analyses run as long-running product jobs with progress and cancellation; deleting and rebuilding all results matches the profile oracle within tolerance; historical results record their definition version.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-16` and ledger record `ledger/tasks/scope-16.md` in the Plan repository; task branch `task/scope-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-34.04](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.04) — full, including the required-design-implementation text: same profile through native ProductJobs over a frozen committed source; persist request/config hashes, resolved levels, per-family quality; delete-and-rebuild must match the profile oracle within tolerance |
| Provides | scope.analysis-recipes |
| Start prerequisites | **artifact** [SCOPE.14](#task-scope-14) — measurements. *Why:* recipes compose measurements<br>**artifact** [SCOPE.15](#task-scope-15) — decoders. *Why:* recipes compose decoder output |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.18](#task-scope-18), [SCOPE.19](#task-scope-19), [SCOPE.21](#task-scope-21) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Analysis/Recipes/**`<br>`ArcScope:tests/ArcScopePipelineTests/Analysis/**` |
| Validation | reconstruction test deleting all results and rebuilding; long-analysis cancellation; version-change test — offline |
| Completion evidence | result reconstruction and version-recording results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | 'Native ProductJobs' reads as ArcScope's own in-process long-running Task/CancellationToken job pattern ('under their product owner'), not a shared cross-repo service; DesktopPlatform already carries a BuildingBlocks ArcForges.Application.Abstractions package this can reuse. Not modelled as a hard external artifact edge — checked [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) specifically and ruled it out: [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) is local IPC/process registration, not a job-execution abstraction. |

<a id="task-scope-17"></a>

### SCOPE.17 — Annotations, findings and session/capture comparison

**Outcome.** Annotations and findings exist as authored content with identity and history, never written into raw capture; session-to-session and capture-to-capture comparison states its alignment explicitly.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-17` and ledger record `ledger/tasks/scope-17.md` in the Plan repository; task branch `task/scope-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-34.05](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.05) — full |
| Provides | scope.annotations-findings-comparison |
| Start prerequisites | **artifact** [SCOPE.06](#task-scope-06) — session/capture to annotate/compare. *Why:* direct consumer |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.18](#task-scope-18), [SCOPE.19](#task-scope-19), [SCOPE.22](#task-scope-22) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Domain/Annotations/**`<br>`ArcScope:tests/ArcScopePipelineTests/Annotations/**` |
| Validation | structural raw-capture-untouched test; comparison correctness with deliberate misalignment; finding history tests — offline |
| Completion evidence | raw-capture immutability and comparison alignment results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Independent of SCOPE.14/15/16 (measurements/decoders/recipes); can run in parallel with them. |

<a id="task-scope-18"></a>

### SCOPE.18 — Reports and reproducibility

**Outcome.** Reports compose analyses, measurements, findings and visualisations into a portable exported form; every element traces to session, capture, time range, configuration snapshot, decoder version and analysis version; regenerating from recorded sources produces equivalent results.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-18` and ledger record `ledger/tasks/scope-18.md` in the Plan repository; task branch `task/scope-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-34.06](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.06) — full, including both required-design-implementation paragraphs: report/UI/offline-recomputation comparison with rendering/rounding never changing the stored numeric result; report-section origin plus enclosing union; deterministic measurement beside AI narrative never relabelled<br>[WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) §8 additional completion requirement: every basic family has its formula/status oracle; reproduction uses the defined tolerance rather than an undefined byte-equality claim — package-level obligation contribution |
| Provides | scope.reports |
| Start prerequisites | **artifact** [SCOPE.14](#task-scope-14) — measurements. *Why:* reports compose measurement results<br>**artifact** [SCOPE.15](#task-scope-15) — decoders. *Why:* reports trace decoder version<br>**artifact** [SCOPE.16](#task-scope-16) — analysis results. *Why:* reports compose analysis output<br>**artifact** [SCOPE.17](#task-scope-17) — annotations/findings. *Why:* reports compose findings |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.19](#task-scope-19), [SCOPE.22](#task-scope-22), [SIM.09](simulator.md#task-sim-09) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Reporting/**`<br>`ArcScope:tests/ArcScopePipelineTests/Reports/**` |
| Validation | traceability completeness test; regeneration-equivalence test; export fidelity check; content-origin carrier vectors including unknown input and failed publication — offline |
| Completion evidence | traceability completeness and regeneration equivalence results; carrier/propagation/failure vectors with payload and manifest hashes |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Content-origin behavior (requirements/07-security-privacy-and-trust.md) and the carrier schema (requirements/13-data-formats-and-portability.md) are named as frozen design inputs fixed before this package — already satisfied, not a start edge; implement per spec without choosing a different marking mechanism. |

<a id="task-scope-19"></a>

### SCOPE.19 — Owned-artifact verification and real integration

**Outcome.** The [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) candidate closes: scope.measurement.v1 independent expected results, invalid/status cases and reporting references pass; native acceleration does not redefine the result; [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) hardware-based measurement/analysis evidence is recorded.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-19` and ledger record `ledger/tasks/scope-19.md` in the Plan repository; task branch `task/scope-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Package acceptance | Records the [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-34.90](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.90) — full<br>[WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required-behavior-and-closure section (every remaining spectrum/correlation/threshold/event-pattern/decoder analysis profile in architecture 26) — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required-behavior-and-closure section: every remaining spectrum/correlation/threshold/event-pattern/decoder analysis profile in architecture 26, independent numeric and gap/error vectors |
| Provides | scope.wp34-accepted-candidate |
| Start prerequisites | **artifact** [SCOPE.12](#task-scope-12) — all WP34 tasks complete to assemble. *Why:* verify task<br>**artifact** [SCOPE.13](#task-scope-13) — as above. *Why:* as above<br>**artifact** [SCOPE.14](#task-scope-14) — as above. *Why:* as above<br>**artifact** [SCOPE.15](#task-scope-15) — as above. *Why:* as above<br>**artifact** [SCOPE.16](#task-scope-16) — as above. *Why:* as above<br>**artifact** [SCOPE.17](#task-scope-17) — as above. *Why:* as above<br>**artifact** [SCOPE.18](#task-scope-18) — as above. *Why:* as above |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.02](release.md#task-rel-02) |
| Write scope | `ArcScope:docs/wp-34-integration-receipt.md` |
| Validation | scope.measurement.v1 independent expected results, invalid/status cases and reporting references; proportionate under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | owned-artifact and real-integration receipt |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Confirms the design's explicit non-edge: [WP-34](../../work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) does not wait on [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51) (the Cloud simulator); reproducibility is verified via SCOPE.08 replay. |

<a id="task-scope-20"></a>

### SCOPE.20 — ArcChat capability surface for ArcScope

**Outcome.** Query, analysis, authoring and operational capabilities are declared, each with risk level, permission requirement and approval posture; start/stop capture are treated as real-side-effect operations, not read-only conveniences.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-20` and ledger record `ledger/tasks/scope-20.md` in the Plan repository; task branch `task/scope-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-35.00](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.00) — full |
| Provides | scope.capability-surface |
| Start prerequisites | **artifact** [SCOPE.06](#task-scope-06) — session/capture/channel/signal/event domain objects the query capabilities expose. *Why:* capability descriptors wrap real domain types<br>**contract** [CON.02](contracts.md#task-con-02) — the generic capability descriptor shape (risk level, permission requirement, approval posture) established by the Hub/minimal-provider-slice pattern. *Why:* [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) ('Approval at the owner') looks like the origin of the generic owner-side approval posture every product's capability set implements; ArcScope should declare against the same shape ArcNotes's first slice used rather than inventing a second one. |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AST.12](assistant.md#task-ast-12) — real ArcChat security/approval surface actually enforcing these descriptors end to end. *Why:* declaring capabilities does not require ArcChat's enforcement code to exist first; the real cross-product proof is a completion-time integration, and [WP-17.02](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.02) ('Security and approval surface') is the plausible ArcChat-side owner |
| Unblocks | [SCOPE.25](#task-scope-25), [SCOPE.26](#task-scope-26) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.AssistantIntegration/**`<br>`ArcScope:tests/ArcScopePipelineTests/Capabilities/**` |
| Validation | descriptor validation per capability; owner-side refusal tests; operational-capability risk assertion — offline |
| Completion evidence | capability descriptor and refusal results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | The old WP33<-26 edge does not transfer here either: [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) is the remote *execution* bridge, which would consume these capability descriptors as a downstream caller, not produce anything [WP-35.00](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.00) needs to start. |

<a id="task-scope-21"></a>

### SCOPE.21 — Bounded context provision for AI

**Outcome.** ArcScope contributes structured results (measurements, analysis outputs, decoded event summaries, selected ranges) as bounded context; raw capture structurally cannot enter a context payload; oversized context is refused explicitly.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-21` and ledger record `ledger/tasks/scope-21.md` in the Plan repository; task branch `task/scope-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-35.01](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01) — full, including required-design-implementation text: project measurement values with profile, immutable source/configuration binding, counts, coverage and status into bounded context/report references; unknown-profile and insufficient results are never silently rendered as numeric zero<br>[WP-35](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35) §4 content-origin/content-unit binding obligation applying broadly to WP35's changed files — package-level obligation contribution |
| Provides | scope.bounded-context |
| Start prerequisites | **artifact** [SCOPE.14](#task-scope-14) — measurements. *Why:* context projects measurement values<br>**artifact** [SCOPE.16](#task-scope-16) — analysis results. *Why:* context projects analysis outputs<br>**artifact** [SCOPE.15](#task-scope-15) — decoders. *Why:* context projects decoded event summaries |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AST.15](assistant.md#task-ast-15) — real ArcChat 'Ask ArcChat' consumption of the bounded context reference. *Why:* producing the bounded, structurally-raw-capture-free context does not require the real AI consumer to exist first; the end-to-end proof that ArcChat actually receives and uses the reference (never the raw capture) is a completion-time integration. |
| Unblocks | [SCOPE.26](#task-scope-26) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.Application/Context/**`<br>`ArcScope:tests/ArcScopePipelineTests/Context/**` |
| Validation | structural test asserting raw capture cannot enter a context payload; bounding test; visibility test — offline |
| Completion evidence | structural raw-capture exclusion and bounding results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-22"></a>

### SCOPE.22 — Cloud sync scope (metadata, not raw capture)

**Outcome.** The ArcScope sync scope excludes raw capture by default and includes metadata, analysis, annotations, findings, reports and configurations; enabling project sync transfers no raw capture bytes; the policy is visible per project and per session; the included scope converges across devices.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-22` and ledger record `ledger/tasks/scope-22.md` in the Plan repository; task branch `task/scope-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-35.02](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.02) — all work except the parts mapped to SCOPE.27 |
| Provides | scope.cloud-sync-scope |
| Start prerequisites | **artifact** [SCOPE.06](#task-scope-06) — session metadata. *Why:* sync scope includes session metadata<br>**artifact** [SCOPE.18](#task-scope-18) — reports. *Why:* sync scope includes reports<br>**artifact** [SCOPE.17](#task-scope-17) — annotations/findings. *Why:* sync scope includes them |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SCOPE.27](#task-scope-27) — real ArcScope metadata sync against deployed Cloud. *Why:* the sync scope is accepted only with real convergence evidence |
| Unblocks | [SCOPE.26](#task-scope-26), [SCOPE.27](#task-scope-27) |
| Permitted substitutes | [SUB-scope-sync-fixture](../substitutes.md#sub-scope-sync-fixture) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.CloudClient/SyncScope/**`<br>`ArcScope:tests/SyncConflictTests/ArcScope/**` |
| Validation | enable-sync test asserting no raw bytes transferred; policy-visibility test; convergence test across devices for included scope — early development against a contract-bound sync fixture, real convergence at [WP-35.90](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.90) |
| Completion evidence | no-raw-bytes sync assertion and convergence results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-23"></a>

### SCOPE.23 — Explicit per-session raw capture upload

**Outcome.** Raw upload is an explicit per-session act with size/destination/consequence stated, using the chunked upload path with resumption and verification; no automatic trigger path exists anywhere (not from AI, not from enabling sync).

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-23` and ledger record `ledger/tasks/scope-23.md` in the Plan repository; task branch `task/scope-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-35.03](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.03) — full |
| Provides | scope.raw-upload |
| Start prerequisites | **artifact** [SCOPE.07](#task-scope-07) — durable capture to upload. *Why:* direct source of upload bytes<br>**artifact** [CLOUD.42](cloud.md#task-cloud-42) — published blob lifecycle mechanism (chunked upload, resumption, verification). *Why:* explicit large raw-capture upload reuses the real chunked object-storage upload path rather than a bespoke one; resumability/verification over genuinely large captures cannot be honestly proven against a stub |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.26](#task-scope-26) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.CloudClient/RawUpload/**`<br>`ArcScope:tests/SyncConflictTests/ArcScope/RawUpload/**` |
| Validation | explicit-upload flow test; negative test for no automatic trigger path; resumption and verification tests on a large capture |
| Completion evidence | explicit upload, no-auto-trigger and resumption results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-24"></a>

### SCOPE.24 — Import, export and format fixtures

**Outcome.** Native full-fidelity bundle export/import round-trips with equivalence; tabular export carries explicit precision warnings; import enters the unified session model with a recorded origin (never disguised as a live device); every claimed import version has a fixture — satisfying [PG-07](../../../assurance/open-gates-register.md#rule-pg-07) for ArcScope.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-24` and ledger record `ledger/tasks/scope-24.md` in the Plan repository; task branch `task/scope-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-35.04](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04) — full, including required-design-implementation text: native bundles preserve origin, measurement profile/configuration and simulator provenance separately; CSV/JSON/report export publishes required sidecars atomically; structured context carries selected origins and measurement quality, never raw capture<br>[WP-35](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35) §4 content-origin/content-unit binding obligation applying broadly to WP35's changed files — package-level obligation contribution<br>[WP-35](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35) §8 additional completion requirements (measurement meaning/numerical profile survives portability; content-origin carrier vectors) — package-level obligation contribution |
| Provides | scope.import-export-bundle |
| Start prerequisites | **artifact** [SCOPE.07](#task-scope-07) — durable capture format to bundle/export. *Why:* native bundle wraps the real capture format<br>**artifact** [SCOPE.14](#task-scope-14) — measurement profile/configuration to carry in the bundle. *Why:* bundles preserve measurement profile/configuration separately per the required-design text |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.26](#task-scope-26), [SIM.06](simulator.md#task-sim-06), [SIM.09](simulator.md#task-sim-09) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.ImportExport/**`<br>`ArcScope:fixtures/formats/arcscope/**`<br>`ArcScope:tests/ArcScopePipelineTests/ImportExport/**` |
| Shared resources | [RES-arcscope-format-fixtures](../shared-resources.md#res-arcscope-format-fixtures) (append) |
| Validation | bundle round-trip equivalence; precision-warning assertions; origin-recording test; fixture coverage for every claimed version — offline |
| Completion evidence | bundle round-trip, precision warnings, origin and fixture coverage |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This task also carries the bundle-side half of [WP-51](../../work-packages/51-arcscope-cloud-simulator.md#rule-wp-51)'s 'simulator provenance separately' requirement — SIM.06 (ArcScope-side simulator ingestion) depends on this task so simulated captures round-trip through the same bundle format with their synthetic labelling intact. |

<a id="task-scope-25"></a>

### SCOPE.25 — Extension boundary: no third-party raw-capture write path

**Outcome.** No extension-reachable path can write raw capture; extension access to ArcScope is through capabilities with owner-side validation only.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-25` and ledger record `ledger/tasks/scope-25.md` in the Plan repository; task branch `task/scope-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-35.05](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.05) — full |
| Provides | scope.extension-boundary |
| Start prerequisites | **artifact** [SCOPE.20](#task-scope-20) — capability surface. *Why:* extension access must route through the capability descriptors, not a separate path<br>**artifact** [SCOPE.07](#task-scope-07) — raw capture write path to assert exclusion against. *Why:* the structural guarantee is meaningless without the real write path to test against<br>**artifact** [EXT.02](extensions.md#task-ext-02) — published dual capability boundary mechanism. *Why:* [WP-41.02](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.02) ('The dual capability boundary') is the platform's generic owner-side-validation-only extension access pattern; ArcScope's structural no-write guarantee is this pattern applied to raw capture specifically, not a separately invented boundary |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.26](#task-scope-26) |
| Write scope | `ArcScope:src/ArcScope/ArcScope.AssistantIntegration/ExtensionBoundary/**`<br>`ArcScope:tests/ArcScopePipelineTests/ExtensionBoundary/**` |
| Validation | structural test asserting no extension-reachable raw-write path exists; owner-side refusal test from an extension caller — offline |
| Completion evidence | extension no-write structural results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-26"></a>

### SCOPE.26 — Owned-artifact verification and real integration

**Outcome.** The [WP-35](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35) candidate closes: metadata sync and explicit-upload behavior remain distinct; context/report data retain measurement identity and ownership across real service calls; [PG-03](../../../assurance/open-gates-register.md#rule-pg-03) licence/provenance evidence recorded.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/scope-26` and ledger record `ledger/tasks/scope-26.md` in the Plan repository; task branch `task/scope-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Package acceptance | Records the [WP-35](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-35.90](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.90) — full |
| Provides | scope.wp35-accepted-candidate |
| Start prerequisites | **artifact** [SCOPE.20](#task-scope-20) — all WP35 tasks complete to assemble. *Why:* verify task<br>**artifact** [SCOPE.21](#task-scope-21) — as above. *Why:* as above<br>**artifact** [SCOPE.22](#task-scope-22) — as above. *Why:* as above<br>**artifact** [SCOPE.23](#task-scope-23) — as above. *Why:* as above<br>**artifact** [SCOPE.24](#task-scope-24) — as above. *Why:* as above<br>**artifact** [SCOPE.25](#task-scope-25) — as above. *Why:* as above |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.02](release.md#task-rel-02) |
| Write scope | `ArcScope:docs/wp-35-integration-receipt.md` |
| Validation | metadata sync and explicit-upload behavior remain distinct; context/report data retain measurement identity across real service calls — real Cloud integration exercised here, not at earlier SCOPE tasks |
| Completion evidence | owned-artifact and real-integration receipt |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-scope-27"></a>

### SCOPE.27 — Real ArcScope metadata sync against the deployed Cloud sync engine

**Outcome.** ArcScope session and capture metadata sync scopes converge across devices against the deployed Cloud sync engine, replacing the contract-bound sync substitute; raw captures stay local unless explicitly uploaded.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope`; also touches Cloud |
| Claim, branch and ledger | `claims/scope-27` and ledger record `ledger/tasks/scope-27.md` in the Plan repository; task branch `task/scope-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-35.02](../../work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.02) — real-integration evidence: metadata sync scope converges against deployed Cloud authority |
| Provides | ArcScope real metadata sync evidence |
| Start prerequisites | **artifact** [SCOPE.22](#task-scope-22) — ArcScope Cloud sync scope declaration and client. *Why:* the integration exercises the ArcScope client<br>**artifact** [CLOUD.39](cloud.md#task-cloud-39) — deployed guarded publication and convergent bootstrap. *Why:* real convergence needs the real publisher<br>**artifact** [CLOUD.44](cloud.md#task-cloud-44) — multi-device convergence harness. *Why:* convergence is proven with the shared harness |
| Entry condition | [ADOPT.05.arcscope](adoption.md#task-adopt-05-arcscope) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SCOPE.22](#task-scope-22) |
| Write scope | `ArcScope:tests/ArcScope.Tests.Integration/Sync/**` |
| Validation | Local real-integration run against a deployed test environment, recorded once; offline checks in CI; no hosted live-service CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Candidate identities, deployed environment identity, convergence scenario results and untested coverage. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Added during consolidation so the ArcScope sync substitute has a named replacing task. |
