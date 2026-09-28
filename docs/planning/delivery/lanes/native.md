# Native producers and probes — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Technical probes and the functional native families with their managed wrappers and RID runtime packages.

Tasks: 13 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [NAT.01](#task-nat-01) | Probe A: device tool execution under Native AOT | producer | M | [PLT.18](platform.md#task-plt-18) (artifact), [PLT.09](platform.md#task-plt-09) (artifact), [PRF.04](runtime-proofs.md#task-prf-04) (artifact) | not-started |
| [NAT.03](#task-nat-03) | Probe C: high-throughput acquisition over a real transport | producer | M | none | not-started |
| [NAT.05](#task-nat-05) | Probe evidence, licence positions, conclusions and hardware-lab inventory seed | producer | S | [NAT.01](#task-nat-01) (artifact), [NAT.03](#task-nat-03) (artifact) | not-started |
| [NAT.06](#task-nat-06) | Common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers | producer | L | [GOV.17](governance.md#task-gov-17) (artifact) | not-started |
| [NAT.11](#task-nat-11) | Image family: still-image codecs (PNG/TIFF/EXR) | producer | M | [NAT.06](#task-nat-06) (artifact), [PLT.45](platform.md#task-plt-45) (artifact), [GOV.17](governance.md#task-gov-17) (artifact) | not-started |
| [NAT.13](#task-nat-13) | Instruments family: serial and USB devices (NEW library) | producer | M | [NAT.06](#task-nat-06) (artifact), [GOV.17](governance.md#task-gov-17) (artifact) | not-started |
| [NAT.14](#task-nat-14) | Pdf family: PDFium and production parser containment in the WP11 helper (NEW library) | producer | L | [PLT.45](platform.md#task-plt-45) (artifact), [NAT.06](#task-nat-06) (artifact), [GOV.17](governance.md#task-gov-17) (artifact) | not-started |
| [NAT.22](#task-nat-22) | Image package production: all 6 RIDs | producer | S | [NAT.11](#task-nat-11) (artifact) | not-started |
| [NAT.24](#task-nat-24) | Instruments package production: all 6 RIDs | producer | S | [NAT.13](#task-nat-13) (artifact) | not-started |
| [NAT.25](#task-nat-25) | Pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition | producer | M | [NAT.14](#task-nat-14) (artifact), [PLT.45](platform.md#task-plt-45) (artifact) | not-started |
| [NAT.28](#task-nat-28) | Dependency adoption receipts and hardware-lab closure | producer | M | [NAT.22](#task-nat-22) (artifact), [NAT.24](#task-nat-24) (artifact), [NAT.25](#task-nat-25) (artifact) | not-started |
| [NAT.29](#task-nat-29) | Verify the owned WP06 artifact set and real cross-runtime integration | integration | M | [PRF.02](runtime-proofs.md#task-prf-02) (artifact), [PRF.04](runtime-proofs.md#task-prf-04) (artifact), [PRF.05](runtime-proofs.md#task-prf-05) (artifact), [PRF.06](runtime-proofs.md#task-prf-06) (artifact), [PRF.07](runtime-proofs.md#task-prf-07) (artifact), [PRF.08](runtime-proofs.md#task-prf-08) (artifact), [PRF.09](runtime-proofs.md#task-prf-09) (artifact), [PRF.10](runtime-proofs.md#task-prf-10) (artifact) | not-started |
| [NAT.30](#task-nat-30) | Verify the complete native producer set as one immutable candidate | integration | M | [NAT.06](#task-nat-06) (artifact), [NAT.11](#task-nat-11) (artifact), [NAT.13](#task-nat-13) (artifact), [NAT.14](#task-nat-14) (artifact), [NAT.22](#task-nat-22) (artifact), [NAT.24](#task-nat-24) (artifact), [NAT.25](#task-nat-25) (artifact), [NAT.28](#task-nat-28) (artifact), [NAT.01](#task-nat-01) (artifact), [NAT.03](#task-nat-03) (artifact), [NAT.05](#task-nat-05) (artifact), [PLT.54](platform.md#task-plt-54) (artifact), [GOV.17](governance.md#task-gov-17) (artifact) | not-started |

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
| Notes | One of WP13's two canonical early risk proofs (package goal: 'retire the early technical risks'). Parallel with NAT.03 (disjoint write scopes). |

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
| Write scope | `DesktopPlatform:benchmarks/probes/acquisition/**`<br>`DesktopPlatform:eng/runtime_ownership.py (classify only the exact task-owned benchmarks/probes/acquisition/AcquisitionProbe.csproj path as test-or-build-tool)`<br>`DesktopPlatform:eng/test_runtime_ownership.py (positive exact-path assertion and rejection fixtures for lookalike or any other benchmarks path)` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Run a single-channel probe at 1,000,000 scalar samples/second over real localhost TCP sustained for at least 10 seconds using a fixed-capacity ring buffer; record achieved rate, buffer capacity/memory and drop/overrun counts. Also induce and record overrun, disconnect/gap and pause-while-recording behavior. |
| Completion evidence | Sustained-throughput record with overrun/gap/pause results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no benchmarks/probes/acquisition scaffolding found. |
| Notes | No hard start-dependency on any other WP -- can begin immediately using a real TCP/UDP loopback or serial-over-USB pair; exotic hardware is not required for the first real-transport configuration. For this bounded probe, use one channel at 1,000,000 scalar samples/second over real localhost TCP for at least 10 seconds with a fixed-capacity ring buffer and record actual rate, memory/capacity and dropped/overrun samples. This probe-only measurement is not a shipping SLA, marketing claim or downstream performance target; existing overrun counting/timestamping, explicit disconnect gap, pause-with-recording and responsive plot-downsampling obligations remain unchanged. Parallel with NAT.01. The scoped runtime-ownership support admits only the full exact path benchmarks/probes/acquisition/AcquisitionProbe.csproj as test-or-build-tool, with a positive exact-path assertion and rejection of lookalike and other benchmarks paths. It does not authorize a general benchmarks prefix, another path exception, runtime/schema/security algorithm expansion, or any source outside eng/runtime_ownership.py and eng/test_runtime_ownership.py. |

<a id="task-nat-05"></a>

### NAT.05 — Probe evidence, licence positions, conclusions and hardware-lab inventory seed

**Outcome.** Each of the two retained probes (A and C) has a written conclusion (proved / not proved / downstream constraint / open items); every native dependency the probes introduced has a recorded licence position; the tests/HardwareLab device inventory is created (device/firmware/driver versions) -- seeding [PG-08](../../../assurance/open-gates-register.md#rule-pg-08) (completed later by NAT.28/[WP-13.16](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.16)).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-05` and ledger record `ledger/tasks/nat-05.md` in the Plan repository; task branch `task/nat-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-13.04](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.04) — full |
| Provides | probe-conclusions; hardware-lab-inventory-seed |
| Start prerequisites | **artifact** [NAT.01](#task-nat-01) — Probe A result. *Why:* the conclusion cannot be written before the probe runs<br>**artifact** [NAT.03](#task-nat-03) — Probe C result. *Why:* same |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:eng/verification/probe-evidence/**`<br>`DesktopPlatform:tests/HardwareLab/**` |
| Validation | Completeness check: every probe has a recorded environment, procedure, result and conclusion |
| Completion evidence | Two written probe conclusions; licence positions for probe-introduced dependencies; hardware inventory shell |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: depends on the retained NAT.01 and NAT.03 probe results. |
| Notes | Small synthesis task; not itself a risk probe. |

<a id="task-nat-06"></a>

### NAT.06 — Common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers

**Outcome.** annex-06 common preambles, fixed numeric keys, pack8 records, ownership/cancellation/bounded-buffer helpers compile as C17/C++20 headers and C# layouts for the retained still-image, instrument and PDF families; every field offset and all 17 normative sizes are asserted; wrong-size/version/null/closed-handle cases and zero-leaked-output-on-failure are proven. ArcForges.Native.Abstractions managed package (status/handle types only) is published. The existing arc_image_* probe-library identity is retained unchanged; retired families are removed by GOV.17 before this task starts.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-06` and ledger record `ledger/tasks/nat-06.md` in the Plan repository; task branch `task/nat-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-13.05](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.05) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | native-abi-common-v1.1; native-abstractions-package |
| Start prerequisites | **artifact** [GOV.17](governance.md#task-gov-17) — retired native families removed and the still-image shim moved. *Why:* the common ABI headers and package inventory are edited only after the retired families leave |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.11](#task-nat-11), [NAT.13](#task-nat-13), [NAT.14](#task-nat-14), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:native/shared/**`<br>`DesktopPlatform:native/CMakeLists.txt (register only the exact NAT.06 C17/C++20 common-ABI test targets below)`<br>`DesktopPlatform:native/shared/tests/arc_native_abi_c17_layout.c (retained shim-static test source only; CTest target arc_native_abi_c17_layout_tests)`<br>`DesktopPlatform:native/shared/tests/arc_native_abi_cpp20_tests.cpp (retained shim-static test source only; target arc_native_abi_cpp20_tests)`<br>`DesktopPlatform:native/*/include/arc/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Abstractions/**`<br>`DesktopPlatform:tests/NativeAbiTests/ArcForges.Tests.NativeAbiTests.csproj (add only a ProjectReference to the existing Native.Abstractions project; no PackageReference)`<br>`DesktopPlatform:tests/NativeAbiTests/CommonAbiLayoutTests.cs (existing Windows x64 test project only)`<br>`DesktopPlatform:.github/workflows/native-abi.yml (on Windows x64 run only the two exact CTest targets and `dotnet test tests/NativeAbiTests/ArcForges.Tests.NativeAbiTests.csproj --filter Category=NativeAbiLayout --no-restore`; this filter runs only common-layout tests and excludes the existing image runtime smoke)`<br>`DesktopPlatform:eng/provenance/files.json (append only the three exact new test-source rows above)` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | On the admitted RIDs compile the common headers and run only CTest targets arc_native_abi_c17_layout_tests (C17) and arc_native_abi_cpp20_tests (C++20), both retained shim-static; on Windows x64 run only `dotnet test tests/NativeAbiTests/ArcForges.Tests.NativeAbiTests.csproj --filter Category=NativeAbiLayout --no-restore`, excluding the existing image runtime smoke. Assert all field offsets and 17 normative sizes, wrong-size/version/null/closed-handle failures, and zero outputs on failure. |
| Completion evidence | Common ABI and deterministic failure surface: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: native/shared/include/arc/arc_native_abi.h and native/shared/src/arc_native_abi_internal.hpp already exist (probe-level ABI1.0: get_abi_version/get_build_info/get_last_error only, per design's repeated 'probe-only' warning); the ABI1.1 functional preamble/pack8 records from contracts/06-native-functional-abi.md SS2 are not yet present. src/Native/ArcForges.Native.Abstractions/NativeAbi.cs exists as an early scaffold. |
| Notes | Hard prerequisite for NAT.11, NAT.13 and NAT.14 (artifact edges from each). NAT.06 alone registers native/shared/tests/arc_native_abi_c17_layout.c as CTest target arc_native_abi_c17_layout_tests and native/shared/tests/arc_native_abi_cpp20_tests.cpp as target arc_native_abi_cpp20_tests in native/CMakeLists.txt; both tests and targets are retained shim-static only. The existing tests/NativeAbiTests/ArcForges.Tests.NativeAbiTests.csproj gains only a ProjectReference to the existing Native.Abstractions project; CommonAbiLayoutTests.cs uses that project. On Windows x64 native-abi.yml runs only `dotnet test tests/NativeAbiTests/ArcForges.Tests.NativeAbiTests.csproj --filter Category=NativeAbiLayout --no-restore`, so the existing image runtime smoke is excluded. Do not create a project, add a PackageReference or change package identity, or authorize other workflow behavior. Append only these three new test-source rows to eng/provenance/files.json. Preserve the 17 normative size/offset checks and wrong-size, version, null, closed-handle, and zero-output-on-failure cases. No native family implementation, library identity, package identity or dependency expansion is authorized; runtime/policy input binding changes are limited to exact [ADP-07](../adoption.md#rule-adp-07) current rows necessary for these files. |

<a id="task-nat-11"></a>

### NAT.11 — Image family: still-image codecs (PNG/TIFF/EXR)

**Outcome.** arc_image_* implemented with PNG/TIFF/EXR metadata and bounded tile reads via OIIO/OpenEXR/Imath; hostile reads execute only in the WP11 helper.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-11` and ledger record `ledger/tasks/nat-11.md` in the Plan repository; task branch `task/nat-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.10](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.10) — full<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories — package-level obligation contribution<br>[WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field — package-level obligation contribution |
| Provides | arc-image-functions |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_image_options_v1, arc_region_v1). *Why:* exact parameter types<br>**artifact** [PLT.45](platform.md#task-plt-45) — published ContentSandbox.Contracts/Broker/foundation Runtime.<rid>. *Why:* 'hostile reads execute only in WP11 helper' -- the still-image decode path for untrusted content must run inside the same restricted host NAT.14/Pdf uses, not a bespoke isolation mechanism<br>**artifact** [GOV.17](governance.md#task-gov-17) — the still-image shim at native/arcimage-abi under the ArcImageNative logical library. *Why:* the image family is implemented in the moved directory under its neutral identity |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.22](#task-nat-22), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:native/arcimage-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Image/**` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Bit depth/metadata round trip, edge tiles, decompression bomb, failed codec, incomplete-output refusal |
| Completion evidence | Still-image codecs: behavioral, failure and package evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: the still-image shim and src/Native/ArcForges.Native.Image exist at ABI1.0 probe level (GOV.17 moves the shim to native/arcimage-abi); OpenImageIO already required by the 'shim-static' CMake profile. |
| Notes | Consumed by the assistant image previews through the ContentSandbox per the platform matrix SS3.2 slot table. |

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
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_instrument_options_v1, arc_transfer_v1). *Why:* exact parameter types<br>**artifact** [GOV.17](governance.md#task-gov-17) — retired native families removed and the still-image shim moved. *Why:* the instruments family registers in the cleaned package inventory |
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
| Start prerequisites | **artifact** [PLT.45](platform.md#task-plt-45) — published ArcForges.ContentSandbox.Contracts,.Broker and the foundation Runtime.<rid> package (built around a deliberately hostile first-party TEST parser). *Why:* design text is explicit: WP11 'solely owns' the host/protocol/launcher; WP13.13 composes the real parser into that SAME host and 'no future parser is an input to WP11 and no already-published artifact is modified' -- a fixture or reimplementation is not acceptable, this must be the real published foundation binary<br>**artifact** [NAT.06](#task-nat-06) — compiled common ABI headers/layouts (arc_pdf_page_v1). *Why:* exact parameter types<br>**artifact** [GOV.17](governance.md#task-gov-17) — retired native families removed and the still-image shim moved. *Why:* the PDF family registers in the cleaned package inventory and helper composition |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.25](#task-nat-25), [NAT.30](#task-nat-30), [PLT.45](platform.md#task-plt-45), [PLT.54](platform.md#task-plt-54) |
| Permitted substitutes | [SUB-hostile-test-parser](../substitutes.md#sub-hostile-test-parser) |
| Write scope | `DesktopPlatform:native/arcpdf-abi/**`<br>`DesktopPlatform:src/Native/ArcForges.Native.Pdf/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/**`<br>`DesktopPlatform:native/CMakeLists.txt`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Packaged PDF page/text/tile fixtures, malformed/native-crash/hang and parent-death cleanup on every admitted RID; rerun of actual image parser containment (not just PDF) |
| Completion evidence | Actual PDF dependency and containment evidence contributing to [PG-12](../../../assurance/open-gates-register.md#rule-pg-12); [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) runtime evidence for the real-parser leg (11.09 supplies the mechanism leg) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: src/DesktopHelpers/ArcForges.ContentSandbox exists with only a minimal Program.cs (the WP11.09 foundation shell); no arcpdf-abi, no ArcForges.Native.Pdf, no production parser composition yet. PDFium is not present in any vcpkg port or CMake profile found in this pass. |
| Notes | Highest residual security-relevant risk of the seven native families (hostile content inside a real isolation boundary) -- flagged as an early risk proof even though it is scheduled after NAT.06, unlike WP13's four canonical probes. |

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
| Validation | Clean-cache C17/C# AOT consumers per RID; missing/transitive/wrong-RID library, hash collision, absent export, revoked artifact, source-unavailable negatives |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Image slice) |
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
| Validation | Clean-cache C17/C# AOT consumers per RID; missing/transitive/wrong-RID library, hash collision, absent export, revoked artifact, source-unavailable negatives |
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
| Unblocks | [NAT.28](#task-nat-28), [NAT.30](#task-nat-30) |
| Write scope | `DesktopPlatform:src/Native/ArcForges.Native.Pdf.Runtime.*/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/**`<br>`DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Clean-cache C17/C# AOT consumers per RID; [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) hostile-parser containment re-run at package level (not just source level) |
| Completion evidence | Immutable native package production: behavioral, failure and package evidence (Pdf slice); [PG-12](../../../assurance/open-gates-register.md#rule-pg-12) contribution |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no Pdf packaging scaffolding yet. |
| Notes | Depends on NAT.14 landing first (unlike the other packaging tasks, this one also republishes the shared ContentSandbox helper, so it is more tightly sequenced). |

<a id="task-nat-28"></a>

### NAT.28 — Dependency adoption receipts and hardware-lab closure

**Outcome.** AD01-AD08 recorded for OIIO, OpenEXR, Imath, libusb, PDFium and every shipped transitive dependency; the hardware-lab inventory (serial plus an actual USB device with vendor/product identity, explicit interface/endpoint, firmware and driver versions) is completed; SBOM/licence/source and enabled-feature lists matched to actual packaged files.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-28` and ledger record `ledger/tasks/nat-28.md` in the Plan repository; task branch `task/nat-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-13.16](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.16) — full |
| Provides | pg03-full-closure; pg08-full-closure |
| Start prerequisites | **artifact** [NAT.22](#task-nat-22) — Image package closure (OIIO/OpenEXR/Imath positions). *Why:* same<br>**artifact** [NAT.24](#task-nat-24) — Instruments package closure (libusb position, physical USB device). *Why:* same, plus this is the one family requiring the actual labelled hardware-lab device<br>**artifact** [NAT.25](#task-nat-25) — Pdf package closure (PDFium position). *Why:* same |
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
| Start prerequisites | **artifact** [PRF.02](runtime-proofs.md#task-prf-02) — real, delivered outcome of PRF.02 (ArcScope desktop Native AOT package proof). *Why:* this integration exercises the real arcScope desktop Native AOT package proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.04](runtime-proofs.md#task-prf-04) — real, delivered outcome of PRF.04 (Local RPC under AOT: bidirectional named-pipe/UDS probe processes). *Why:* this integration exercises the real local RPC under AOT: bidirectional named-pipe/UDS probe processes instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.05](runtime-proofs.md#task-prf-05) — real, delivered outcome of PRF.05 (Generated gRPC-Web under AOT against deployed Worker/Container ingress). *Why:* this integration exercises the real generated gRPC-Web under AOT against deployed Worker/Container ingress instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.06](runtime-proofs.md#task-prf-06) — real, delivered outcome of PRF.06 (Realtime (EventService.Watch/Poll) under AOT). *Why:* this integration exercises the real realtime (EventService.Watch/Poll) under AOT instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.07](runtime-proofs.md#task-prf-07) — real, delivered outcome of PRF.07 (Cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof). *Why:* this integration exercises the real cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.08](runtime-proofs.md#task-prf-08) — real, delivered outcome of PRF.08 (React production build and generated TS SDK proof). *Why:* this integration exercises the real react production build and generated TS SDK proof instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.09](runtime-proofs.md#task-prf-09) — real, delivered outcome of PRF.09 (Third-party control AOT admission gate and first candidate). *Why:* this integration exercises the real third-party control AOT admission gate and first candidate instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.10](runtime-proofs.md#task-prf-10) — real, delivered outcome of PRF.10 (Android Kotlin/Jetpack Compose gRPC-Web and CF proof). *Why:* this integration exercises the real android Kotlin/Jetpack Compose gRPC-Web and CF proof instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Actual candidate NuGet restore/native loading and desktop AOT; C# AOT gRPC/gRPC-Web plus selected auth/storage/SQL adapters; Kotlin/Jetpack Compose generated-client calls; React client calls; a minimal deployed CF<->reachable C#<->R2 chain -- a bounded foundation probe, explicitly not the full [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) Cloud Harness |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-nat-30"></a>

### NAT.30 — Verify the complete native producer set as one immutable candidate

**Outcome.** Image tiles, PDF, instruments, cancel/lifetime/hostile-helper vectors and missing-DLL/wrong-RID negative consumers, all against actual WP07 to WP12 mechanisms (persistence, local RPC, shell, ContentSandbox, telemetry) -- probe-only exports never pass; this is the gate WP14/WP33 consumers wait behind

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/nat-30` and ledger record `ledger/tasks/nat-30.md` in the Plan repository; task branch `task/nat-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-13.90](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.90) — full |
| Start prerequisites | **artifact** [NAT.06](#task-nat-06) — real, delivered outcome of NAT.06 (Common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers). *Why:* this integration exercises the real common native ABI: preambles, pack8 records, ownership, cancellation, bounded buffers instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.11](#task-nat-11) — real, delivered outcome of NAT.11 (Image family: still-image codecs (PNG/TIFF/EXR)). *Why:* this integration exercises the real image family: still-image codecs (PNG/TIFF/EXR) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.13](#task-nat-13) — real, delivered outcome of NAT.13 (Instruments family: serial and USB devices (NEW library)). *Why:* this integration exercises the real instruments family: serial and USB devices (NEW library) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.14](#task-nat-14) — real, delivered outcome of NAT.14 (Pdf family: PDFium and production parser containment in the WP11 helper (NEW library)). *Why:* this integration exercises the real pdf family: PDFium and production parser containment in the WP11 helper (NEW library) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.22](#task-nat-22) — real, delivered outcome of NAT.22 (Image package production: all 6 RIDs). *Why:* this integration exercises the real image package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.24](#task-nat-24) — real, delivered outcome of NAT.24 (Instruments package production: all 6 RIDs). *Why:* this integration exercises the real instruments package production: all 6 RIDs instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.25](#task-nat-25) — real, delivered outcome of NAT.25 (Pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition). *Why:* this integration exercises the real pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.28](#task-nat-28) — real, delivered outcome of NAT.28 (Dependency adoption receipts and hardware-lab closure). *Why:* this integration exercises the real dependency adoption receipts and hardware-lab closure instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.01](#task-nat-01) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [NAT.03](#task-nat-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [NAT.05](#task-nat-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [PLT.54](platform.md#task-plt-54) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [GOV.17](governance.md#task-gov-17) — the producer set without the retired native families. *Why:* the complete native candidate contains exactly the retained families |
| Entry condition | [ADOPT.02.native](adoption.md#task-adopt-02-native) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Image tiles, PDF, instruments, cancel/lifetime/hostile-helper vectors and missing-DLL/wrong-RID negative consumers, all against actual WP07 to WP12 mechanisms (persistence, local RPC, shell, ContentSandbox, telemetry) -- probe-only exports never pass; this is the gate WP14/WP33 consumers wait behind |
| Baseline (unreviewed unless accepted) | not-started |
