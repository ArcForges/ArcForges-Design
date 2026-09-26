# Native producers and probes — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Technical probes and the functional native families with their managed wrappers and RID runtime packages.

Tasks: 25 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [NAT.01](#task-nat-01) | Probe A: device tool execution under Native AOT | producer | M | [PLT.18](platform.md#task-plt-18) (artifact), [PLT.09](platform.md#task-plt-09) (artifact), [PRF.04](runtime-proofs.md#task-prf-04) (artifact) | not-started |
| [NAT.02](#task-nat-02) | Probe B: block editor, store, undo and recovery | producer | M | [PLT.01](platform.md#task-plt-01) (artifact) | not-started |
| [NAT.03](#task-nat-03) | Probe C: high-throughput acquisition over a real transport | producer | M | none | not-started |
| [NAT.04](#task-nat-04) | Probe D: native decode and audio/video synchronisation | producer | L | [PRF.01](runtime-proofs.md#task-prf-01) (artifact) | not-started |
| [NAT.05](#task-nat-05) | Probe evidence, licence positions, conclusions and hardware-lab inventory seed | producer | S | [NAT.01](#task-nat-01) (artifact), [NAT.02](#task-nat-02) (artifact), [NAT.03](#task-nat-03) (artifact), [NAT.04](#task-nat-04) (artifact) | not-started |
| [NAT.06](#task-nat-06) | Common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers | producer | L | none | not-started |
| [NAT.07](#task-nat-07) | Media family: reader, probe, frame and seek (arc_media_reader_*) | producer | L | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.08](#task-nat-08) | Media family: convert, resample and media writer | producer | M | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.09](#task-nat-09) | Media family: audio devices (miniaudio) | producer | M | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.10](#task-nat-10) | Colour family: OCIO transforms | producer | M | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.11](#task-nat-11) | Image family: still-image codecs (PNG/TIFF/EXR) | producer | M | [NAT.06](#task-nat-06) (artifact), [PLT.45](platform.md#task-plt-45) (artifact) | not-started |
| [NAT.12](#task-nat-12) | Otio family: OTIO0.18.1 interchange | producer | L | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.13](#task-nat-13) | Instruments family: serial and USB devices (NEW library) | producer | M | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.14](#task-nat-14) | Pdf family: PDFium and production parser containment in the WP11 helper (NEW library) | producer | L | [PLT.45](platform.md#task-plt-45) (artifact), [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.15](#task-nat-15) | Graphics family: portable CPU surface and optional OS backends (NEW library) | producer | M | [NAT.06](#task-nat-06) (artifact) | not-started |
| [NAT.20](#task-nat-20) | Media package production: all 6 RIDs | producer | M | [NAT.07](#task-nat-07) (artifact), [NAT.08](#task-nat-08) (artifact), [NAT.09](#task-nat-09) (artifact) | not-started |
| [NAT.21](#task-nat-21) | Colour package production: all 6 RIDs | producer | S | [NAT.10](#task-nat-10) (artifact) | not-started |
| [NAT.22](#task-nat-22) | Image package production: all 6 RIDs | producer | S | [NAT.11](#task-nat-11) (artifact) | not-started |
| [NAT.23](#task-nat-23) | Otio package production: all 6 RIDs | producer | S | [NAT.12](#task-nat-12) (artifact) | not-started |
| [NAT.24](#task-nat-24) | Instruments package production: all 6 RIDs | producer | S | [NAT.13](#task-nat-13) (artifact) | not-started |
| [NAT.25](#task-nat-25) | Pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition | producer | M | [NAT.14](#task-nat-14) (artifact), [PLT.45](platform.md#task-plt-45) (artifact) | not-started |
| [NAT.26](#task-nat-26) | Graphics package production: all 6 RIDs | producer | S | [NAT.15](#task-nat-15) (artifact) | not-started |
| [NAT.28](#task-nat-28) | Dependency adoption receipts and hardware-lab closure | producer | M | [NAT.20](#task-nat-20) (artifact), [NAT.21](#task-nat-21) (artifact), [NAT.22](#task-nat-22) (artifact), [NAT.23](#task-nat-23) (artifact), [NAT.24](#task-nat-24) (artifact), [NAT.25](#task-nat-25) (artifact), [NAT.26](#task-nat-26) (artifact) | not-started |
| [NAT.29](#task-nat-29) | Verify the owned WP06 artifact set and real cross-runtime integration | integration | M | [PRF.01](runtime-proofs.md#task-prf-01) (artifact), [PRF.02](runtime-proofs.md#task-prf-02) (artifact), [PRF.03](runtime-proofs.md#task-prf-03) (artifact), [PRF.04](runtime-proofs.md#task-prf-04) (artifact), [PRF.05](runtime-proofs.md#task-prf-05) (artifact), [PRF.06](runtime-proofs.md#task-prf-06) (artifact), [PRF.07](runtime-proofs.md#task-prf-07) (artifact), [PRF.08](runtime-proofs.md#task-prf-08) (artifact), [PRF.09](runtime-proofs.md#task-prf-09) (artifact), [PRF.10](runtime-proofs.md#task-prf-10) (artifact) | not-started |
| [NAT.30](#task-nat-30) | Verify the complete native producer set as one immutable candidate | integration | M | [NAT.06](#task-nat-06) (artifact), [NAT.07](#task-nat-07) (artifact), [NAT.08](#task-nat-08) (artifact), [NAT.09](#task-nat-09) (artifact), [NAT.10](#task-nat-10) (artifact), [NAT.11](#task-nat-11) (artifact), [NAT.12](#task-nat-12) (artifact), [NAT.13](#task-nat-13) (artifact), [NAT.14](#task-nat-14) (artifact), [NAT.15](#task-nat-15) (artifact), [NAT.20](#task-nat-20) (artifact), [NAT.21](#task-nat-21) (artifact), [NAT.22](#task-nat-22) (artifact), [NAT.23](#task-nat-23) (artifact), [NAT.24](#task-nat-24) (artifact), [NAT.25](#task-nat-25) (artifact), [NAT.26](#task-nat-26) (artifact), [NAT.28](#task-nat-28) (artifact), [NAT.01](#task-nat-01) (artifact), [NAT.02](#task-nat-02) (artifact), [NAT.03](#task-nat-03) (artifact), [NAT.04](#task-nat-04) (artifact), [NAT.05](#task-nat-05) (artifact), [PLT.54](platform.md#task-plt-54) (artifact) | not-started |

## Tasks

<a id="task-nat-01"></a>

### NAT.01 — Probe A: device tool execution under Native AOT

**Outcome.** Inside a published Native AOT desktop binary, a stub ToolRequest is pulled, re-authorised locally, resolved through the generated allowlist to a CapabilityKey, decoded into a typed product request, invoked and returns an idempotent result -- with an AOT publish log showing zero diagnostics and a negative test proving no reflection-based registration/decode path compiles or exists.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-01` and ledger record `ledger/tasks/nat-01.md` in the Plan repository; task branch `task/nat-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M · early risk proof |
| Obligations | [WP-13.00](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.00) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution |
| Provides | probe-a-device-tool-aot-proof |
| Start prerequisites | **artifact** [PLT.18](platform.md#task-plt-18) — generated CapabilityKey allowlist and static registration mechanism (Capabilities package). *Why:* 13.00 explicitly resolves through 'the generated allowlist'; a fixture allowlist would not test the real static-registration/AOT risk this probe exists to retire<br>**artifact** [PLT.09](platform.md#task-plt-09) — local RPC structured-argument decode path ([DP-02](../../../architecture/contracts/02-local-rpc-operations.md#rule-dp-02) boundary dispatch assembly). *Why:* the probe decodes structured arguments per SS3.1 of the local RPC contract; this is the exact mechanism [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) publishes<br>**artifact** [PRF.04](runtime-proofs.md#task-prf-04) — a working pattern for AOT desktop <-> AOT desktop local RPC (from [WP-06.01](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.01)). *Why:* 13.00 runs 'inside a published Native AOT desktop binary' using the same local-RPC AOT posture 06.01 first proves; reusing an unproven pattern here would duplicate, not retire, risk |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.03](app-composition.md#task-app-03), [NAT.05](#task-nat-05), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:benchmarks/probes/agent-aot/**` |
| Validation | AOT publish log zero diagnostics; end-to-end ToolRequest->decode->typed invocation->result run inside the published binary; containment test confirming the structured value type appears only in the boundary dispatch assembly |
| Completion evidence | AOT publish log and in-binary device tool request decode/execute trace; explicit note that the model loop itself is NOT probed here (it is the CF Workflow, [LS-02](../../../architecture/17-agent-harness.md#rule-ls-02)/[V-03](../../../assurance/phase-1-official-verification.md#rule-v-03)) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: benchmarks/ directory does not exist yet in DesktopPlatform; this substep has zero scaffolding. |
| Notes | One of WP13's four canonical early risk proofs (package goal: 'retire the four early technical risks'). Parallel with NAT.02/03/04 (disjoint write scopes). |

<a id="task-nat-02"></a>

### NAT.02 — Probe B: block editor, store, undo and recovery

**Outcome.** A minimal block editor over the local store demonstrates create/edit/reorder, undo/redo across a composite operation, and recovery from a hard process kill mid-edit that returns to the last committed boundary with uncommitted work explicitly reported as loss -- proving undo, revision, checkpoint and journal are four distinct mechanisms.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-02` and ledger record `ledger/tasks/nat-02.md` in the Plan repository; task branch `task/nat-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M · early risk proof |
| Obligations | [WP-13.01](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.01) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution |
| Provides | probe-b-editor-recovery-proof |
| Start prerequisites | **artifact** [PLT.01](platform.md#task-plt-01) — the real local persistence single-writer journal/checkpoint mechanism. *Why:* the probe's recovery claim is meaningless against anything but the real journal; a fake store would hide exactly the recovery defects this probe exists to surface |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.05](#task-nat-05), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:benchmarks/probes/editor-store/**` |
| Validation | Kill-during-edit recovery run; undo-across-composite-operation test; explicit test that undo history is not crash recovery ([QI-09](../../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)) |
| Completion evidence | Kill-during-edit recovery and undo-distinction results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no benchmarks/probes/editor-store scaffolding found. |
| Notes | Parallel with NAT.01/03/04. |

<a id="task-nat-03"></a>

### NAT.03 — Probe C: high-throughput acquisition over a real transport

**Outcome.** Sustained acquisition from a real transport (at least one real TCP/UDP/serial configuration, not an in-memory generator, per [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06)) runs above the intended product target through a ring buffer with responsive plot downsampling; overrun is counted and timestamped, pausing the view never stops recording, and disconnect leaves an explicit gap.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-03` and ledger record `ledger/tasks/nat-03.md` in the Plan repository; task branch `task/nat-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M · early risk proof |
| Obligations | [WP-13.02](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.02) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution |
| Provides | probe-c-acquisition-proof |
| Start prerequisites | none |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.05](#task-nat-05), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:benchmarks/probes/acquisition/**` |
| Validation | Sustained-throughput run with recorded rate/memory/drop counts; induced overrun; induced disconnect; pause-while-recording test |
| Completion evidence | Sustained-throughput record with overrun/gap/pause results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no benchmarks/probes/acquisition scaffolding found. |
| Notes | No hard start-dependency on any other WP -- can begin immediately using a real TCP/UDP loopback or serial-over-USB pair; exotic hardware is not required for the first real-transport configuration. Parallel with NAT.01/02/04. |

<a id="task-nat-04"></a>

### NAT.04 — Probe D: native decode and audio/video synchronisation

**Outcome.** Native decode through a thin C ABI shim displays one frame in the desktop shell with audio/video synchronised against a shared timeline clock; safe handles, managed-side input validation, a clean sanitiser run and a sacrificial-process crash test all pass; hardware acceleration is discovered at runtime with a proven software fallback.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-04` and ledger record `ledger/tasks/nat-04.md` in the Plan repository; task branch `task/nat-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-13.03](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.03) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution |
| Provides | probe-d-decode-sync-proof |
| Start prerequisites | **artifact** [PRF.01](runtime-proofs.md#task-prf-01) — a shape for an AOT-published desktop shell capable of hosting a display surface. *Why:* the probe 'displays one frame in the desktop shell'; any of PRF.01-03 would equally satisfy this, PRF.01 is representative |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.05](#task-nat-05), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:benchmarks/probes/media/**` |
| Shared resources | [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Frame-display run; audio/video sync measurement; sanitiser run (ASan/UBSan); sacrificial-process crash test; forced-software-path run |
| Completion evidence | Frame display, synchronisation measurement, sanitiser and sacrificial-process results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no benchmarks/probes/media scaffolding found; DesktopPlatform's own native toolchain (CMake profiles, sanitiser support) is the real prerequisite and already exists per native-abi.yml. |
| Notes | GPU-accelerated path testing is necessarily per-local-machine (whatever GPU is available); the required CPU software-fallback path is universally testable. Parallel with NAT.01/02/03. |

<a id="task-nat-05"></a>

### NAT.05 — Probe evidence, licence positions, conclusions and hardware-lab inventory seed

**Outcome.** Each of the four probes has a written conclusion (proved / not proved / downstream constraint / open items); every native dependency the probes introduced has a recorded licence position; the tests/HardwareLab device inventory is created (device/firmware/driver versions) -- seeding [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) (completed later by NAT.28/[WP-13.16](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.16)).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-05` and ledger record `ledger/tasks/nat-05.md` in the Plan repository; task branch `task/nat-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.04](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.04) — full |
| Provides | probe-conclusions; hardware-lab-inventory-seed |
| Start prerequisites | **artifact** [NAT.01](#task-nat-01) — Probe A result. *Why:* the conclusion cannot be written before the probe runs<br>**artifact** [NAT.02](#task-nat-02) — Probe B result. *Why:* same<br>**artifact** [NAT.03](#task-nat-03) — Probe C result. *Why:* same<br>**artifact** [NAT.04](#task-nat-04) — Probe D result. *Why:* same |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:eng/verification/probe-evidence/**`<br>`DesktopPlatform:tests/HardwareLab/**` |
| Validation | Completeness check: every probe has a recorded environment, procedure, result and conclusion |
| Completion evidence | Four written probe conclusions; licence positions for probe-introduced dependencies; hardware inventory shell |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: depends entirely on NAT.01-04 existing first. |
| Notes | Small synthesis task; not itself a risk probe. |

<a id="task-nat-06"></a>

### NAT.06 — Common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers

**Outcome.** annex-06 common preambles, fixed numeric keys, pack8 records, ownership/cancellation/bounded-buffer helpers compile as C17/C++20 headers and C# layouts for all seven families; every field offset and all 17 normative sizes are asserted; wrong-size/version/null/closed-handle cases and zero-leaked-output-on-failure are proven. ArcForges.Native.Abstractions managed package (status/handle types only) is published. The five existing probe-library identities (incl. arc_metal_*) are retained unchanged.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-06` and ledger record `ledger/tasks/nat-06.md` in the Plan repository; task branch `task/nat-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-13.05](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.05) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | native-abi-common-v1.1; native-abstractions-package |
| Start prerequisites | none |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.07](#task-nat-07), [NAT.08](#task-nat-08), [NAT.09](#task-nat-09), [NAT.10](#task-nat-10), [NAT.11](#task-nat-11), [NAT.12](#task-nat-12), [NAT.13](#task-nat-13), [NAT.14](#task-nat-14), [NAT.15](#task-nat-15), [NAT.30](#task-nat-30), [NOTES.09](arcnotes.md#task-notes-09), [SLATE.15](arcslate.md#task-slate-15), [SLATE.38](arcslate.md#task-slate-38) |
| Write scope | `DesktopPlatform:native/shared/**`<br>`DesktopPlatform:native/*/include/arc/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Abstractions/**` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Compile C17/C++20 headers and C# layouts on the admitted RIDs; offset/size assertions; wrong-size/version/null/closed-handle negative tests |
| Completion evidence | Common ABI and deterministic failure surface: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: native/shared/include/arc/arc_native_abi.h and native/shared/src/arc_native_abi_internal.hpp already exist (probe-level ABI1.0: get_abi_version/get_build_info/get_last_error only, per design's repeated 'probe-only' warning); the ABI1.1 functional preamble/pack8 records from contracts/06-native-functional-abi.md SS2 are not yet present. src/Native/ArcForges.Native.Abstractions/NativeAbi.cs exists as an early scaffold. |
| Notes | Hard prerequisite for NAT.07-15 (artifact edges from each). |

<a id="task-nat-07"></a>

### NAT.07 — Media family: reader, probe, frame and seek (arc_media_reader_*)

**Outcome.** arc_media_reader_open/stream/seek/next/close and arc_media_buffer_* implemented over the selected FFmpeg demux/decode path and the WP11 restricted helper; stream metadata, delayed frames, EOF and seek epochs preserved; every export has a behavioral oracle and bounded isolated execution.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-07` and ledger record `ledger/tasks/nat-07.md` in the Plan repository; task branch `task/nat-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-13.06](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.06) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-media-reader-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_io_v1, arc_reader_options_v1, arc_frame_v1, arc_region_v1). *Why:* these declarations are the exact parameter types of every arc_media_reader_* export |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.20](#task-nat-20), [NAT.30](#task-nat-30), [SLATE.04](arcslate.md#task-slate-04), [SLATE.15](arcslate.md#task-slate-15) |
| Write scope | `DesktopPlatform:native/arcmedia-ffmpeg-abi/src/**`<br>`DesktopPlatform:native/arcmedia-ffmpeg-abi/include/**`<br>`DesktopPlatform:native/arcmedia-ffmpeg-abi/tests/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Known two-frame seek, malformed input, B-frame/drain, tiled copy, exact audio sample bounds, repeated cancel/close against the actual FFmpeg dependency build; sanitiser build for parser paths ([SB-03](../../../architecture/12-native-interop-and-media.md#rule-sb-03)/[SB-04](../../../architecture/12-native-interop-and-media.md#rule-sb-04)) |
| Completion evidence | Media reader/probe/frame/seek: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: native/arcmedia-ffmpeg-abi/{src,include/arc,tests,exports,fuzz,generated} directories exist with only the ABI1.0 probe exports (get_abi_version/get_build_info/get_last_error); src/Native/ArcForges.Native.Media/MediaAbi.cs is an early probe-level scaffold; native/CMakeLists.txt already requires FFmpeg/libusb/miniaudio for the 'runtime-shared' profile that builds this target. |
| Notes | Shares the arcmedia-ffmpeg-abi library/target with NAT.08 (writer/convert/resample) and NAT.09 (audio) -- see 'shared' entries. All three can be developed in parallel branches but should merge sequentially. |

<a id="task-nat-08"></a>

### NAT.08 — Media family: convert, resample and media writer

**Outcome.** arc_media_video_convert, arc_media_resampler_* and arc_media_writer_* implemented with the fixed portable profiles (FFV1/PCM/WAV, MP4 MPEG4-AAC); resampler delay/PTS preserved; writer commits only after complete output/sidecars/hash.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-08` and ledger record `ledger/tasks/nat-08.md` in the Plan repository; task branch `task/nat-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.07](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.07) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-media-writer-convert-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_video_convert_v1, arc_audio_convert_v1, arc_writer_options_v1). *Why:* exact parameter types of these exports |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.20](#task-nat-20), [NAT.30](#task-nat-30), [SLATE.15](arcslate.md#task-slate-15), [SLATE.19](arcslate.md#task-slate-19), [SLATE.20](arcslate.md#task-slate-20), [SLATE.21](arcslate.md#task-slate-21), [SLATE.27](arcslate.md#task-slate-27), [SLATE.28](arcslate.md#task-slate-28) |
| Write scope | `DesktopPlatform:native/arcmedia-ffmpeg-abi/src/**`<br>`DesktopPlatform:native/arcmedia-ffmpeg-abi/include/**`<br>`DesktopPlatform:native/arcmedia-ffmpeg-abi/tests/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Independent fresh decode of FFV1/PCM/WAV and MP4 MPEG4-AAC; resample length, finish-twice, cancel/abort, disk-full corruption rejection |
| Completion evidence | Convert, resample and media writer: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: same directory state as NAT.07; writer/convert exports not yet implemented. |
| Notes | Does not functionally require NAT.07 (arc_media_buffer_create can construct input buffers directly per the ABI doc), only the shared-file contention noted above. |

<a id="task-nat-09"></a>

### NAT.09 — Media family: audio devices (miniaudio)

**Outcome.** arc_media_audio_* implemented over miniaudio device/context/ring primitives with explicit negotiation, bounded rings, counters, disconnect/reopen; missing output device permits video-only playback with a stated reason without blocking offline export.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-09` and ledger record `ledger/tasks/nat-09.md` in the Plan repository; task branch `task/nat-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.08](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.08) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-media-audio-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_device_options_v1, arc_device_state_v1). *Why:* exact parameter types of these exports |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.20](#task-nat-20), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:native/arcmedia-ffmpeg-abi/src/**`<br>`DesktopPlatform:native/arcmedia-ffmpeg-abi/include/**`<br>`DesktopPlatform:native/arcmedia-ffmpeg-abi/tests/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Physical output/input, underflow, overflow, device loss, exclusive-use refusal, no-device video clock, offline render -- physical audio hardware is ordinary (most dev machines have one), not a scarce [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) lab resource |
| Completion evidence | Audio devices: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: same directory state as NAT.07; miniaudio already required by native/CMakeLists.txt's runtime-shared profile but no audio exports implemented yet. |
| Notes | Independent of NAT.07/08 functionally; shares the same target/export files. |

<a id="task-nat-10"></a>

### NAT.10 — Colour family: OCIO transforms

**Outcome.** arc_color_* implemented with immutable OCIO config/processor assets and alpha-correct CPU transforms; no ambient file/network config lookup; named refusal of invalid transforms.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-10` and ledger record `ledger/tasks/nat-10.md` in the Plan repository; task branch `task/nat-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.09](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.09) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-colour-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_colour_options_v1). *Why:* exact parameter types |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.21](#task-nat-21), [NAT.30](#task-nat-30), [SLATE.24](arcslate.md#task-slate-24) |
| Write scope | `DesktopPlatform:native/arcslate-color-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Colour/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Independent RGB/alpha vectors, alpha 0, unknown space, tampered bundle, preview/render agreement |
| Completion evidence | Colour transforms: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: native/arcslate-color-abi and src/Native/ArcForges.Native.Colour exist at ABI1.0 probe level only; OpenColorIO already required by the 'shim-static' CMake profile. |
| Notes | Independent native library from Media -- no shared-file contention with NAT.07-09. Parallel with NAT.11/12/13/14/15. |

<a id="task-nat-11"></a>

### NAT.11 — Image family: still-image codecs (PNG/TIFF/EXR)

**Outcome.** arc_image_* implemented with PNG/TIFF/EXR metadata and bounded tile reads/writes via OIIO/OpenEXR/Imath; hostile reads execute only in the WP11 helper.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-11` and ledger record `ledger/tasks/nat-11.md` in the Plan repository; task branch `task/nat-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.10](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.10) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-image-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_image_options_v1, arc_region_v1). *Why:* exact parameter types<br>**artifact** [PLT.45](platform.md#task-plt-45) — published ContentSandbox.Contracts/Broker/foundation Runtime.<rid>. *Why:* 'hostile reads execute only in WP11 helper' -- the still-image decode path for untrusted content must run inside the same restricted host NAT.14/Pdf uses, not a bespoke isolation mechanism |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.22](#task-nat-22), [NAT.30](#task-nat-30), [SLATE.21](arcslate.md#task-slate-21) |
| Write scope | `DesktopPlatform:native/arcslate-image-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Image/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Bit depth/metadata round trip, edge tiles, decompression bomb, failed codec, incomplete-output refusal |
| Completion evidence | Still-image codecs: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: native/arcslate-image-abi and src/Native/ArcForges.Native.Image exist at ABI1.0 probe level; OpenImageIO already required by the 'shim-static' CMake profile. |
| Notes | Consumed by both ArcSlate (stills) and ArcNotes (attachment images) per the platform matrix SS3.2 slot table. |

<a id="task-nat-12"></a>

### NAT.12 — Otio family: OTIO0.18.1 interchange

**Outcome.** arc_otio_read/write implemented under the official OTIO0.18.1 library with the selected schema allowlist and fidelity report; exact tick conversion preserved; unsupported schema/malicious path/parser-death cases reported as loss before commit, never silently.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-12` and ledger record `ledger/tasks/nat-12.md` in the Plan repository; task branch `task/nat-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-13.11](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.11) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-otio-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_io_v1). *Why:* canonical/input/output I/O uses this declaration |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.23](#task-nat-23), [NAT.30](#task-nat-30), [SLATE.38](arcslate.md#task-slate-38), [SLATE.39](arcslate.md#task-slate-39) |
| Write scope | `DesktopPlatform:native/arcslate-otio-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Otio/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Mixed/fractional rate round trip, unsupported schema, malicious path, parser death, reported loss before commit -- [PG-15](../../../assurance/open-gates-register.md#rule-pg-15) evidence class |
| Completion evidence | OTIO interchange: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: native/arcslate-otio-abi and src/Native/ArcForges.Native.Otio exist at ABI1.0 probe level; the custom vcpkg opentimelineio port (with a patch removing the pybind11/Python build requirement) is already committed under eng/native/vcpkg/ports/opentimelineio. |
| Notes | [PG-15](../../../assurance/open-gates-register.md#rule-pg-15) (OTIO bidirectional evidence, owned by the ArcSlate lane [WP-39.05](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05)) consumes this task's output as its real-fixture producer. |

<a id="task-nat-13"></a>

### NAT.13 — Instruments family: serial and USB devices (NEW library)

**Outcome.** A new arcinstruments-abi native library and ArcForges.Native.Instruments managed package implement arc_instruments_* over generic OS serial and explicit libusb interface/endpoint open/read/write/cancel/close; identity revalidated at open; no auto-detach of unrelated drivers, no vendor SDK.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-13` and ledger record `ledger/tasks/nat-13.md` in the Plan repository; task branch `task/nat-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.12](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.12) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-instruments-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_instrument_options_v1, arc_transfer_v1). *Why:* exact parameter types |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.24](#task-nat-24), [NAT.30](#task-nat-30), [SCOPE.04](arcscope.md#task-scope-04) |
| Write scope | `DesktopPlatform:native/arcinstruments-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Instruments/**`<br>`DesktopPlatform:native/CMakeLists.txt`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Enumeration, explicit interface claim, control/bulk/interrupt transfers, partial writes, cancellation callback, hot unplug, driver absence, permission denial on Tier 1 -- against the [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) hardware inventory for the physical-device cases |
| Completion evidence | Serial and USB instruments: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no arcinstruments-abi directory and no ArcForges.Native.Instruments managed project exist yet; this is the first fully-new native library of the seven. libusb is already declared as a required dependency in native/CMakeLists.txt's runtime-shared profile even though nothing consumes it yet. |
| Notes | Degradation-path code (enumeration, driver-absence reporting) does not require the [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) lab to exist; the physical hot-unplug/permission-denial matrix against a named USB device does.. |

<a id="task-nat-14"></a>

### NAT.14 — Pdf family: PDFium and production parser containment in the WP11 helper (NEW library)

**Outcome.** A new arcpdf-abi native library and ArcForges.Native.Pdf managed package implement arc_pdf_* over actual PDFium; PDFium and all approved parser wrappers are composed into the existing [WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09) ContentSandbox host using generated local gRPC controls (no second helper, no duplicate DTO owner); the next immutable ContentSandbox.Runtime.<rid> version is published; test-parser production registration is removed (hostile regression fixture retained). Contributes real evidence to [PG-12](../../../assurance/open-gates-register.md#rule-pg-12) and [PG-22](../../../assurance/open-gates-register.md#rule-pg-22).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-14` and ledger record `ledger/tasks/nat-14.md` in the Plan repository; task branch `task/nat-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) — all work except the parts mapped to PLT.54<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-pdf-functions; contentsandbox-production-parser-runtime |
| Start prerequisites | **artifact** [PLT.45](platform.md#task-plt-45) — published ArcForges.ContentSandbox.Contracts,.Broker and the foundation Runtime.<rid> package (built around a deliberately hostile first-party TEST parser). *Why:* design text is explicit: WP11 'solely owns' the host/protocol/launcher; WP13.13 composes the real parser into that SAME host and 'no future parser is an input to WP11 and no already-published artifact is modified' -- a fixture or reimplementation is not acceptable, this must be the real published foundation binary<br>**artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_pdf_page_v1). *Why:* exact parameter types |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.25](#task-nat-25), [NAT.30](#task-nat-30), [NOTES.09](arcnotes.md#task-notes-09), [NOTES.37](arcnotes.md#task-notes-37), [PLT.45](platform.md#task-plt-45), [PLT.54](platform.md#task-plt-54), [SLATE.04](arcslate.md#task-slate-04), [SLATE.16](arcslate.md#task-slate-16) |
| Permitted substitutes | [SUB-hostile-test-parser](../substitutes.md#sub-hostile-test-parser) |
| Write scope | `DesktopPlatform:native/arcpdf-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Pdf/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/**`<br>`DesktopPlatform:native/CMakeLists.txt`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Packaged PDF page/text/tile fixtures, malformed/native-crash/hang and parent-death cleanup on every admitted RID; rerun of actual image/media/OTIO parser containment (not just PDF) |
| Completion evidence | Actual PDF dependency and containment evidence contributing to [PG-12](../../../assurance/open-gates-register.md#rule-pg-12); [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) runtime evidence for the real-parser leg (11.09 supplies the mechanism leg) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: src/DesktopHelpers/ArcForges.ContentSandbox exists with only a minimal Program.cs (the WP11.09 foundation shell); no arcpdf-abi, no ArcForges.Native.Pdf, no production parser composition yet. PDFium is not present in any vcpkg port or CMake profile found in this pass. |
| Notes | Highest residual security-relevant risk of the seven native families (hostile content inside a real isolation boundary) -- flagged as an early risk proof even though it is scheduled after NAT.06, unlike WP13's four canonical probes. |

<a id="task-nat-15"></a>

### NAT.15 — Graphics family: portable CPU surface and optional OS backends (NEW library)

**Outcome.** A new arcgraphics-abi native library and ArcForges.Native.Graphics managed package implement ArcGraphicsNative CPU surface/upload/present/fence/device-loss behavior on all admitted RIDs; the existing arcgraphics-metal-abi probe ABI is preserved unchanged as a private optional backend, not claimed as functional acceleration by itself.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-15` and ledger record `ledger/tasks/nat-15.md` in the Plan repository; task branch `task/nat-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.14](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.14) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-graphics-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_surface_options_v1, arc_region_v1). *Why:* exact parameter types |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.26](#task-nat-26), [NAT.30](#task-nat-30), [SLATE.19](arcslate.md#task-slate-19), [SLATE.22](arcslate.md#task-slate-22), [SLATE.25](arcslate.md#task-slate-25) |
| Write scope | `DesktopPlatform:native/arcgraphics-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Graphics/**`<br>`DesktopPlatform:native/CMakeLists.txt`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | CPU display/readback, ownership and fence lifetime, device loss and forced software path; each advertised accelerator exercised with its actual driver where locally available |
| Completion evidence | Portable graphics and optional OS backends: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: native/arcgraphics-metal-abi exists (APPLE-only ABI1.0 probe, ARC_ABI ok) but is explicitly NOT this task's deliverable -- design text requires it stay unchanged as a private backend of the new arcgraphics-abi. No arcgraphics-abi directory exists yet. |
| Notes | Consumed by both ArcSlate (preview surface) and ArcScope (live-view surface). |

<a id="task-nat-20"></a>

### NAT.20 — Media package production: all 6 RIDs

**Outcome.** ArcForges.Native.Media.Runtime.<rid> published for win-x64, win-arm64, osx-arm64, osx-x64, linux-x64, linux-arm64 with matched tested bytes, headers/import libraries, native manifests and complete dependency closures; isolated clean-cache C17 and C# AOT consumers pass on each admitted RID.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-20` and ledger record `ledger/tasks/nat-20.md` in the Plan repository; task branch `task/nat-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Media + Runtime.<rid> only<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-media-packages-all-rid |
| Start prerequisites | **artifact** [NAT.07](#task-nat-07) — complete arc_media_reader_* export set. *Why:* 13.15's gate: 'missing functional export or dependency prevents completion' -- packaging cannot precede the full family body<br>**artifact** [NAT.08](#task-nat-08) — complete arc_media_writer_*/convert/resample export set. *Why:* same<br>**artifact** [NAT.09](#task-nat-09) — complete arc_media_audio_* export set. *Why:* same |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Media.Runtime.win-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media.Runtime.osx-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media.Runtime.osx-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media.Runtime.linux-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Media.Runtime.linux-arm64/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17 and C# AOT consumers per RID; missing/transitive/wrong-RID library, hash collision, absent export, revoked artifact, source-unavailable negatives |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Media slice) |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: win-x64 packaging already scaffolded (ArcForges.Native.Media.Runtime.win-x64 csproj + packages.json entry); the other 5 RIDs are entirely new package projects. |
| Notes | Win-x64 leg can start as soon as NAT.07-09 land; win-arm64/osx-arm64/osx-x64/linux-x64/linux-arm64 legs are independent of each other and could be sub-split further if the integration owner wants finer parallelism (Tier-1 RIDs win-x64/osx-arm64/linux-x64 vs Tier-2 win-arm64/osx-x64/linux-arm64). |

<a id="task-nat-21"></a>

### NAT.21 — Colour package production: all 6 RIDs

**Outcome.** ArcForges.Native.Colour.Runtime.<rid> published for all 6 RIDs with matched tested bytes/headers/manifests/dependency closures.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-21` and ledger record `ledger/tasks/nat-21.md` in the Plan repository; task branch `task/nat-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Colour + Runtime.<rid> only<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-colour-packages-all-rid |
| Start prerequisites | **artifact** [NAT.10](#task-nat-10) — complete arc_color_* export set. *Why:* 13.15 gate: complete family required before packaging |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Colour.Runtime.win-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Colour.Runtime.osx-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Colour.Runtime.osx-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Colour.Runtime.linux-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Colour.Runtime.linux-arm64/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; same negative matrix as NAT.20 |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Colour slice) |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: win-x64 already scaffolded. |
| Notes | Independent of NAT.20/22-26 (different package identity, disjoint writes except the shared allowlist/vcpkg pin). |

<a id="task-nat-22"></a>

### NAT.22 — Image package production: all 6 RIDs

**Outcome.** ArcForges.Native.Image.Runtime.<rid> published for all 6 RIDs with matched tested bytes/headers/manifests/dependency closures.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-22` and ledger record `ledger/tasks/nat-22.md` in the Plan repository; task branch `task/nat-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Image + Runtime.<rid> only<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-image-packages-all-rid |
| Start prerequisites | **artifact** [NAT.11](#task-nat-11) — complete arc_image_* export set. *Why:* 13.15 gate: complete family required before packaging |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Image.Runtime.win-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Image.Runtime.osx-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Image.Runtime.osx-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Image.Runtime.linux-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Image.Runtime.linux-arm64/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; same negative matrix as NAT.20 |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Image slice) |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: win-x64 already scaffolded. |
| Notes | Independent of the other packaging tasks. |

<a id="task-nat-23"></a>

### NAT.23 — Otio package production: all 6 RIDs

**Outcome.** ArcForges.Native.Otio.Runtime.<rid> published for all 6 RIDs with matched tested bytes/headers/manifests/dependency closures.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-23` and ledger record `ledger/tasks/nat-23.md` in the Plan repository; task branch `task/nat-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Otio + Runtime.<rid> only<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-otio-packages-all-rid |
| Start prerequisites | **artifact** [NAT.12](#task-nat-12) — complete arc_otio_* export set. *Why:* 13.15 gate: complete family required before packaging |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Otio.Runtime.win-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Otio.Runtime.osx-arm64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Otio.Runtime.osx-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Otio.Runtime.linux-x64/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Otio.Runtime.linux-arm64/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; same negative matrix as NAT.20 |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Otio slice) |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: win-x64 already scaffolded. |
| Notes | Independent of the other packaging tasks. |

<a id="task-nat-24"></a>

### NAT.24 — Instruments package production: all 6 RIDs

**Outcome.** ArcForges.Native.Instruments.Runtime.<rid> published for all 6 RIDs.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-24` and ledger record `ledger/tasks/nat-24.md` in the Plan repository; task branch `task/nat-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Instruments + Runtime.<rid> only<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-instruments-packages-all-rid |
| Start prerequisites | **artifact** [NAT.13](#task-nat-13) — complete arc_instruments_* export set. *Why:* 13.15 gate: complete family required before packaging |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30), [SCOPE.11](arcscope.md#task-scope-11) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Instruments.Runtime.*/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; same negative matrix as NAT.20 |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Instruments slice) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no packaging scaffolding at all yet (family itself is new). |
| Notes | First RID (win-x64) is the realistic starting point given libusb Windows support is best-understood; other RIDs follow. |

<a id="task-nat-25"></a>

### NAT.25 — Pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition

**Outcome.** ArcForges.Native.Pdf.Runtime.<rid> published for all 6 RIDs; the composed ContentSandbox.Runtime.<rid> (real parser closure) is rebuilt/signed once and published as the next immutable version per admitted RID.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-25` and ledger record `ledger/tasks/nat-25.md` in the Plan repository; task branch `task/nat-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Pdf + Runtime.<rid>, plus the ContentSandbox.Runtime.<rid> republication from 13.13<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-pdf-packages-all-rid; contentsandbox-runtime-production-all-rid |
| Start prerequisites | **artifact** [NAT.14](#task-nat-14) — complete arc_pdf_* export set and the composed ContentSandbox parser registration. *Why:* 13.15 gate: complete family required before packaging; also 'never alter already released WP11 package bytes' means this republishes a NEW version, not a patch<br>**artifact** [PLT.45](platform.md#task-plt-45) — the WP11-owned host/broker/launcher mechanics stay the versioning authority for ContentSandbox.Runtime identity. *Why:* 13.15 explicit: 'use the WP11 host/broker and the newly signed production helper version composed in 13.13' -- packaging does not fork a second identity |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30), [NOTES.37](arcnotes.md#task-notes-37) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Pdf.Runtime.*/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) hostile-parser containment re-run at package level (not just source level) |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Pdf slice); [PG-12](../../../assurance/open-gates-register.md#rule-pg-12) contribution |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no Pdf packaging scaffolding yet. |
| Notes | Depends on NAT.14 landing first (unlike the other packaging tasks, this one also republishes the shared ContentSandbox helper, so it is more tightly sequenced). |

<a id="task-nat-26"></a>

### NAT.26 — Graphics package production: all 6 RIDs

**Outcome.** ArcForges.Native.Graphics.Runtime.<rid> published for all 6 RIDs, CPU path mandatory everywhere, optional accelerators labelled per RID.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-26` and ledger record `ledger/tasks/nat-26.md` in the Plan repository; task branch `task/nat-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.15](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.15) — ArcForges.Native.Graphics + Runtime.<rid> only<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' — package-level obligation contribution |
| Provides | arc-graphics-packages-all-rid |
| Start prerequisites | **artifact** [NAT.15](#task-nat-15) — complete arc_graphics_* export set. *Why:* 13.15 gate: complete family required before packaging |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Graphics.Runtime.*/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; forced-software-path verified on every RID even where an accelerator is also present |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Graphics slice) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no packaging scaffolding yet (family itself is new). |
| Notes | Independent of the other packaging tasks. |

<a id="task-nat-28"></a>

### NAT.28 — Dependency adoption receipts and hardware-lab closure

**Outcome.** AD01-AD08 recorded for FFmpeg, miniaudio, OCIO, OIIO, OpenEXR, Imath, OTIO, libusb, PDFium and every shipped transitive dependency; the hardware-lab inventory (serial/audio/GPU plus an actual USB device with vendor/product identity, explicit interface/endpoint, firmware and driver versions) is completed; SBOM/licence/source and enabled-feature lists matched to actual packaged files.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-28` and ledger record `ledger/tasks/nat-28.md` in the Plan repository; task branch `task/nat-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.16](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.16) — full |
| Provides | pg03-full-closure; pg08-full-closure |
| Start prerequisites | **artifact** [NAT.20](#task-nat-20) — Media package closure (FFmpeg/miniaudio/libusb positions). *Why:* [AD-01](../../../architecture/08-security-architecture.md#rule-ad-01)..08 obligations are recorded against the actual shipped dependency graph, which only exists once packaging lands<br>**artifact** [NAT.21](#task-nat-21) — Colour package closure (OCIO position). *Why:* same<br>**artifact** [NAT.22](#task-nat-22) — Image package closure (OIIO/OpenEXR/Imath positions). *Why:* same<br>**artifact** [NAT.23](#task-nat-23) — Otio package closure (OTIO position). *Why:* same<br>**artifact** [NAT.24](#task-nat-24) — Instruments package closure (libusb position, physical USB device). *Why:* same, plus this is the one family requiring the actual labelled hardware-lab device<br>**artifact** [NAT.25](#task-nat-25) — Pdf package closure (PDFium position). *Why:* same<br>**artifact** [NAT.26](#task-nat-26) — Graphics package closure. *Why:* same |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:tests/HardwareLab/**`<br>`DesktopPlatform:eng/provenance/**`<br>`DesktopPlatform:eng/policy/dependency-reviews/**` |
| Validation | Match SBOM/license/source and enabled-feature lists to actual packaged files; bind every physical result and each simulated absence to its evidence class |
| Completion evidence | Dependency adoption and hardware receipts: behavioral, failure and package evidence; [PG-03](../../../assurance/open-gates-register.md#rule-pg-03) and [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) contributions covering the complete shipped graph and physical fixtures |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: eng/provenance/artifact-profiles and eng/provenance/records exist with early native-win-x64 build-identity profiles; no dependency-adoption receipts for the seven families found yet. |
| Notes | This is where [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) is genuinely CLOSED (not merely seeded); requires a real labelled USB device to exist. Everything else in this task (SBOM/licence matching, non-USB inventory) can proceed without exotic hardware. |

<a id="task-nat-29"></a>

### NAT.29 — Verify the owned WP06 artifact set and real cross-runtime integration

**Outcome.** Actual candidate NuGet restore/native loading and desktop AOT; C# AOT gRPC/gRPC-Web plus selected auth/storage/SQL adapters; Kotlin/Jetpack Compose generated-client calls; React client calls; a minimal deployed CF<->reachable C#<->R2 chain -- a bounded foundation probe, explicitly not the full [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) Cloud Harness

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-29` and ledger record `ledger/tasks/nat-29.md` in the Plan repository; task branch `task/nat-29` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-06.90](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.90) — full |
| Start prerequisites | **artifact** [PRF.01](runtime-proofs.md#task-prf-01) — real, delivered outcome of PRF.01 (ArcNotes desktop Native AOT package proof). *Why:* this integration exercises the real arcNotes desktop Native AOT package proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.02](runtime-proofs.md#task-prf-02) — real, delivered outcome of PRF.02 (ArcScope desktop Native AOT package proof). *Why:* this integration exercises the real arcScope desktop Native AOT package proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.03](runtime-proofs.md#task-prf-03) — real, delivered outcome of PRF.03 (ArcSlate desktop Native AOT package proof). *Why:* this integration exercises the real arcSlate desktop Native AOT package proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.04](runtime-proofs.md#task-prf-04) — real, delivered outcome of PRF.04 (Local RPC under AOT: bidirectional named-pipe/UDS probe processes). *Why:* this integration exercises the real local RPC under AOT: bidirectional named-pipe/UDS probe processes instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.05](runtime-proofs.md#task-prf-05) — real, delivered outcome of PRF.05 (Generated gRPC-Web under AOT against deployed Worker/Container ingress). *Why:* this integration exercises the real generated gRPC-Web under AOT against deployed Worker/Container ingress instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.06](runtime-proofs.md#task-prf-06) — real, delivered outcome of PRF.06 (Realtime (EventService.Watch/Poll) under AOT). *Why:* this integration exercises the real realtime (EventService.Watch/Poll) under AOT instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.07](runtime-proofs.md#task-prf-07) — real, delivered outcome of PRF.07 (Cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof). *Why:* this integration exercises the real cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.08](runtime-proofs.md#task-prf-08) — real, delivered outcome of PRF.08 (React production build and generated TS SDK proof). *Why:* this integration exercises the real react production build and generated TS SDK proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.09](runtime-proofs.md#task-prf-09) — real, delivered outcome of PRF.09 (Third-party control AOT admission gate and first candidate). *Why:* this integration exercises the real third-party control AOT admission gate and first candidate instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.10](runtime-proofs.md#task-prf-10) — real, delivered outcome of PRF.10 (Android Kotlin/Jetpack Compose gRPC-Web and CF proof). *Why:* this integration exercises the real android Kotlin/Jetpack Compose gRPC-Web and CF proof instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Actual candidate NuGet restore/native loading and desktop AOT; C# AOT gRPC/gRPC-Web plus selected auth/storage/SQL adapters; Kotlin/Jetpack Compose generated-client calls; React client calls; a minimal deployed CF<->reachable C#<->R2 chain -- a bounded foundation probe, explicitly not the full [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) Cloud Harness |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-nat-30"></a>

### NAT.30 — Verify the complete native producer set as one immutable candidate

**Outcome.** Decode/seek/drain, encode->independent decode, image tiles, colour, OTIO, PDF, instruments, graphics CPU/fallback, cancel/lifetime/hostile-helper vectors and missing-DLL/wrong-RID negative consumers, all against actual WP07 to WP12 mechanisms (persistence, local RPC, shell, ContentSandbox, telemetry) -- probe-only exports never pass; this is the gate WP14/WP33/WP36 consumers wait behind

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-30` and ledger record `ledger/tasks/nat-30.md` in the Plan repository; task branch `task/nat-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-13.90](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.90) — full |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — real, delivered outcome of NAT.06 (Common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers). *Why:* this integration exercises the real common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.07](#task-nat-07) — real, delivered outcome of NAT.07 (Media family: reader, probe, frame and seek (arc_media_reader_*)). *Why:* this integration exercises the real media family: reader, probe, frame and seek (arc_media_reader_*) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.08](#task-nat-08) — real, delivered outcome of NAT.08 (Media family: convert, resample and media writer). *Why:* this integration exercises the real media family: convert, resample and media writer instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.09](#task-nat-09) — real, delivered outcome of NAT.09 (Media family: audio devices (miniaudio)). *Why:* this integration exercises the real media family: audio devices (miniaudio) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.10](#task-nat-10) — real, delivered outcome of NAT.10 (Colour family: OCIO transforms). *Why:* this integration exercises the real colour family: OCIO transforms instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.11](#task-nat-11) — real, delivered outcome of NAT.11 (Image family: still-image codecs (PNG/TIFF/EXR)). *Why:* this integration exercises the real image family: still-image codecs (PNG/TIFF/EXR) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.12](#task-nat-12) — real, delivered outcome of NAT.12 (Otio family: OTIO0.18.1 interchange). *Why:* this integration exercises the real otio family: OTIO0.18.1 interchange instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.13](#task-nat-13) — real, delivered outcome of NAT.13 (Instruments family: serial and USB devices (NEW library)). *Why:* this integration exercises the real instruments family: serial and USB devices (NEW library) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.14](#task-nat-14) — real, delivered outcome of NAT.14 (Pdf family: PDFium and production parser containment in the WP11 helper (NEW library)). *Why:* this integration exercises the real pdf family: PDFium and production parser containment in the WP11 helper (NEW library) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.15](#task-nat-15) — real, delivered outcome of NAT.15 (Graphics family: portable CPU surface and optional OS backends (NEW library)). *Why:* this integration exercises the real graphics family: portable CPU surface and optional OS backends (NEW library) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.20](#task-nat-20) — real, delivered outcome of NAT.20 (Media package production: all 6 RIDs). *Why:* this integration exercises the real media package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.21](#task-nat-21) — real, delivered outcome of NAT.21 (Colour package production: all 6 RIDs). *Why:* this integration exercises the real colour package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.22](#task-nat-22) — real, delivered outcome of NAT.22 (Image package production: all 6 RIDs). *Why:* this integration exercises the real image package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.23](#task-nat-23) — real, delivered outcome of NAT.23 (Otio package production: all 6 RIDs). *Why:* this integration exercises the real otio package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.24](#task-nat-24) — real, delivered outcome of NAT.24 (Instruments package production: all 6 RIDs). *Why:* this integration exercises the real instruments package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.25](#task-nat-25) — real, delivered outcome of NAT.25 (Pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition). *Why:* this integration exercises the real pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.26](#task-nat-26) — real, delivered outcome of NAT.26 (Graphics package production: all 6 RIDs). *Why:* this integration exercises the real graphics package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.28](#task-nat-28) — real, delivered outcome of NAT.28 (Dependency adoption receipts and hardware-lab closure). *Why:* this integration exercises the real dependency adoption receipts and hardware-lab closure instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.01](#task-nat-01) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [NAT.02](#task-nat-02) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [NAT.03](#task-nat-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [NAT.04](#task-nat-04) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [NAT.05](#task-nat-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [PLT.54](platform.md#task-plt-54) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Decode/seek/drain, encode->independent decode, image tiles, colour, OTIO, PDF, instruments, graphics CPU/fallback, cancel/lifetime/hostile-helper vectors and missing-DLL/wrong-RID negative consumers, all against actual WP07 to WP12 mechanisms (persistence, local RPC, shell, ContentSandbox, telemetry) -- probe-only exports never pass; this is the gate WP14/WP33/WP36 consumers wait behind |
| Baseline (unreviewed unless accepted) | not-started |
