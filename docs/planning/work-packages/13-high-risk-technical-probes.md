<a id="rule-wp-13"></a>

# WP-13 — Complete Native Producers and Technical Probes

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Retire the four early technical risks and deliver the complete functional native producer set before product implementation consumes it. Probe evidence and production package evidence are distinct required outputs.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform and affected products. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Four isolated technical probes followed by the seven functional native libraries, eight managed native packages, seven runtime package families across the six declared desktop RIDs, and integration with the WP11 restricted helper. The functional ABI, algorithms, formats and limits are fixed by [native annex 06](../../architecture/contracts/06-native-functional-abi.md); no missing function is deferred to product coding.

**Out of scope.** Product UI, editing commands, Cloud business handlers and the AI model loop. Probe scaffolds are cleaned up or kept as isolated regression fixtures. Production ABI/wrapper/runtime code from 13.05–13.16 is retained and published; [ND-05](../implementation-sequence.md#rule-nd-05) does not discard those deliverables.

**Why this package exists.** Every downstream native consumer needs working, versioned packages with their actual dependencies. Neither a probe-only DLL nor an appended verification instruction can substitute for implementing that producer here.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [Quality and compatibility requirements](../../requirements/12-quality-and-compatibility-contract.md) | The acceptance constraints for the four probes defined in this package; native, editor and acquisition designs below supply their mechanisms |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§2` | The AOT resolution the agent probe must validate |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) | The native boundary and safety obligations the media probe must respect |
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) `§4`, `§18` | Acquisition, overrun and rolling-buffer semantics |
| [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-07](07-local-persistence-foundation.md#rule-wp-07), [WP-08](08-local-ipc-and-registration.md#rule-wp-08) output | Proven AOT publish, the local store, and the real transport |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **A probe runs against a real published AOT binary**, not a debug host ([QI-01](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-01), [QI-02](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-02)). |
| <a id="rule-br-02"></a>BR-02 | **Probe evidence is reproducible**: a recorded environment, a recorded procedure and a recorded result. |
| <a id="rule-br-03"></a>BR-03 | **Probe scaffolds and production deliverables are separate.** Production 13.05–13.16 is maintained; probe code reaches production only after the same functional, safety and package gates. |
| <a id="rule-br-04"></a>BR-04 | **A probe that fails produces a decision, not a workaround.** A failed probe raises the conflict rather than being papered over (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**). |
| <a id="rule-br-05"></a>BR-05 | **Native probes obey the native safety obligations from the start** — validated input, sanitiser builds, sacrificial-process tests (`§6` of the native architecture). |
| <a id="rule-br-06"></a>BR-06 | **The acquisition probe uses a real transport**, not an in-memory generator, for at least one configuration. |
| <a id="rule-br-07"></a>BR-07 | **Every native dependency the probes introduce receives a licence position** before use ([PG-03](../../assurance/open-gates-register.md#rule-pg-03)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `benchmarks/probes/agent-aot/` | Probe A workspace and evidence |
| `benchmarks/probes/editor-store/` | Probe B workspace and evidence |
| `benchmarks/probes/acquisition/` | Probe C workspace and evidence |
| `benchmarks/probes/media/` | Probe D workspace and evidence |
| `native/arcmedia-ffmpeg-abi/`, `arcslate-color-abi/`, `arcslate-image-abi/`, `arcslate-otio-abi/` | Extend the existing owned shims without renaming their published symbols |
| `native/arcinstruments-abi/`, `arcpdf-abi/`, `arcgraphics-abi/` | New functional libraries with the fixed annex 06 declarations |
| `src/Native/ArcForges.Native.Abstractions/` and `ArcForges.Native.Media/Colour/Image/Otio/Instruments/Pdf/Graphics` | Eight managed status/handle/wrapper packages; slash-separated names here expand to separate projects |
| `src/Native/ArcForges.Native.<Capability>.Runtime.<rid>/` | Seven families × six RID package definitions, each carrying its admitted native dependency closure |
| `src/DesktopHelpers/` | Consume WP11 helper/Broker/Contracts; add only the approved native parser composition, not a second helper owner |
| `eng/packaging/`, `tests/NativeConsumers/` | Exact package allowlist, headers/import libraries, SBOMs and independent C17/C# AOT package-only consumers |
| `eng/verification/probe-evidence/` | The recorded environments, procedures and results |
| `tests/HardwareLab/` | Created: the device inventory the later hardware families depend on |

**Major types introduced:** the fixed annex 06 status, safe handle, reader/writer, image, colour, OTIO, instrument, PDF and graphics wrappers. No native pointer becomes a managed domain identifier or a wire field.

---

## 5. Required implementation work

<a id="rule-wp-13.00"></a>

### WP-13.00 — Probe A: device tool execution under Native AOT

**What must be fully done.** The **device side** of the Harness runs inside a published Native AOT desktop binary: it pulls a stub `ToolRequest`, re-authorises it locally, resolves a `CapabilityKey` through the **generated allowlist**, decodes structured arguments into a **typed** product request (`§3.1` of the local RPC contract), invokes it, and returns an idempotent result. **The model loop is not probed here — it is the CF Workflow** ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02), **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). What is at risk under AOT is the generated decode and static registration path, not the loop. No reflection, no dynamic assembly, no runtime code generation is involved. Static registration and out-of-process extensibility are both exercised.

**Testing requirements.** An AOT publish log with zero diagnostics; an end-to-end `ToolRequest` → decode → typed invocation → result run inside the published binary; a negative test confirming a reflection-based registration or decode path fails to compile or is absent; a containment test confirming the structured value type appears only in the boundary dispatch assembly ([DP-02](../../architecture/contracts/02-local-rpc-operations.md#rule-dp-02)).

**Completion gate.** A device tool request is decoded and executed through generated, typed, statically registered code inside a published AOT binary, with no reflection path present.

<a id="rule-wp-13.01"></a>

### WP-13.01 — Probe B: block editor, store, undo and recovery

**What must be fully done.** A minimal block editor over the local store: create, edit and reorder blocks; undo and redo across a composite operation; and recovery from a hard process kill mid-edit, returning to the last committed boundary with uncommitted work reported rather than silently lost. Undo, revision, checkpoint and journal are exercised as four distinct mechanisms.

**Testing requirements.** A kill-during-edit recovery run; an undo-across-composite-operation test; a test asserting undo history is not crash recovery ([QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)).

**Completion gate.** Recovery returns to a committed boundary with explicit loss reporting, and undo and recovery are demonstrably different mechanisms.

<a id="rule-wp-13.02"></a>

### WP-13.02 — Probe C: high-throughput acquisition

**What must be fully done.** Sustained acquisition from a real transport at a rate above the intended product target, through a ring buffer, with plot downsampling that keeps the display responsive. Overrun is surfaced with a count and a timestamp, never hidden. Pausing the view does not stop recording. A disconnect leaves an explicit gap.

**Testing requirements.** A sustained-throughput run with recorded rate, memory and drop counts; an induced overrun; an induced disconnect; a pause-view-while-recording test.

**Completion gate.** Sustained throughput above target with bounded memory, and every overrun, gap and disconnect explicitly reported.

<a id="rule-wp-13.03"></a>

### WP-13.03 — Probe D: native decode and synchronisation

**What must be fully done.** Native decode through a thin C ABI shim, displaying one frame in the desktop shell, with audio and video synchronised against a shared timeline clock. Handle lifetime uses safe handles; input is validated in managed code; the probe runs under a sanitiser build and in a sacrificial process for its integration tests. Hardware acceleration is discovered at runtime with a software fallback proven.

**Testing requirements.** A frame-display run; an audio/video synchronisation measurement; a sanitiser run; a sacrificial-process crash test; a forced-software-path run.

**Completion gate.** A frame displays with synchronised audio, the sanitiser run is clean, and the software fallback works when acceleration is disabled.

<a id="rule-wp-13.04"></a>

### WP-13.04 — Evidence, licence positions and conclusions

**What must be fully done.** Each probe produces a written conclusion: what was proven, what was not, what constraint it imposes on the owning product package, and what remains open. Every native dependency introduced receives a licence position. The hardware-lab device inventory is created with device, firmware and driver versions.

**Testing requirements.** A completeness check that each probe has a recorded environment, procedure, result and conclusion.

**Completion gate.** Four conclusions exist, every native dependency has a licence position, and the hardware inventory exists. This seeds [PG-08](../../assurance/open-gates-register.md#rule-pg-08);13.16 completes its production inventory and the full [PG-03](../../assurance/open-gates-register.md#rule-pg-03) dependency obligations.

---

<a id="rule-wp-13.05"></a>

### WP-13.05 — Common ABI and deterministic failure surface

**What must be fully done.** Implement annex 06 common preambles, fixed numeric keys, pack 8 records, ownership, cancellation and bounded-buffer helpers underlying the ABI1.1 declarations. This step compiles all declarations; the family bodies are implemented in 13.06–13.14 and their complete runtime export set is accepted in 13.15/13.90. Retain the five existing probe-library identities, including arc_metal_*; compatibility is not evidence of functional graphics.

**Testing requirements.** Compile C17/C++20 headers and C# layouts; assert every field offset and all 17 sizes, wrong-size/version/null/closed-handle cases and zero leaked output on failure.

**Completion gate.** The common helpers, complete header/layout declarations and common failure rules are independently verified; later family implementation is not required to pass this first substep.

<a id="rule-wp-13.06"></a>

### WP-13.06 — Media reader, probe, frame and seek

**What must be fully done.** Implement arc_media_reader_* and frame access through the selected FFmpeg demux/decode path, restricted helper and exact time model. Preserve stream metadata, delayed frames, EOF and seek epochs.

**Testing requirements.** Known two-frame seek, malformed input, B-frame/drain, tiled copy, exact audio sample bounds and repeated cancel/close with the actual dependency build.

**Completion gate.** Every reader/probe/frame/seek export has a behavioral oracle and bounded isolated execution.

<a id="rule-wp-13.07"></a>

### WP-13.07 — Convert, resample and media writer

**What must be fully done.** Implement conversion/resampling and writer open/write/finish/abort with the fixed portable profiles. Preserve resampler delay and PTS; commit only after complete output/sidecars/hash.

**Testing requirements.** Independent fresh decode of FFV1/PCM/WAV and MP4 MPEG4-AAC; resample length, finish twice, cancel/abort and disk-full corruption rejection.

**Completion gate.** All portable writer profiles and exact conversion semantics pass actual package consumers.

<a id="rule-wp-13.08"></a>

### WP-13.08 — Audio devices

**What must be fully done.** Implement miniaudio-backed capture/playback and explicit negotiation, bounded rings, counters and disconnect/reopen. Missing output devices permit video-only playback with a stated reason and do not block offline export.

**Testing requirements.** Physical output/input, underflow, overflow, device loss, exclusive-use refusal, no-device video clock and offline render.

**Completion gate.** Audio effects and degraded behavior are measured; no silently selected replacement device.

<a id="rule-wp-13.09"></a>

### WP-13.09 — Colour transforms

**What must be fully done.** Implement immutable OCIO config/processor assets and alpha-correct CPU transforms; no ambient file/network config lookup.

**Testing requirements.** Independent RGB/alpha vectors, alpha 0, unknown space, tampered bundle and preview/render agreement.

**Completion gate.** Colour functions and pinned asset provenance pass with named refusal of invalid transforms.

<a id="rule-wp-13.10"></a>

### WP-13.10 — Still-image codecs

**What must be fully done.** Implement PNG/TIFF/EXR metadata, bounded tile reads and writes with OIIO/OpenEXR/Imath; hostile reads execute only in WP11 helper.

**Testing requirements.** Bit depth/metadata round trip, edge tiles, decompression bomb, failed codec and incomplete-output refusal.

**Completion gate.** All image exports and named codec degradation pass without silent image loss.

<a id="rule-wp-13.11"></a>

### WP-13.11 — OTIO interchange

**What must be fully done.** Implement official OTIO0.18.1 read/write under the selected schema allowlist and fidelity report; preserve exact tick conversion and inert unknown fields.

**Testing requirements.** Mixed/fractional rate round trip, unsupported schema, malicious path, parser death and reported loss before commit.

**Completion gate.** Both directions preserve the declared timeline semantics or refuse explicitly.

<a id="rule-wp-13.12"></a>

### WP-13.12 — Serial and USB instruments

**What must be fully done.** Implement generic OS serial and explicit USB interface/endpoint open/read/write/cancel/close; identity is revalidated at open. Do not auto-detach unrelated drivers or enable vendor SDKs.

**Testing requirements.** Enumeration, explicit interface claim, control/bulk/interrupt transfers, partial writes, cancellation callback, hot unplug, driver absence and permission denial on Tier 1.

**Completion gate.** Native instrument functions and permission/loss semantics pass against the hardware inventory.

<a id="rule-wp-13.13"></a>

### WP-13.13 — PDF and production parser containment

**What must be fully done.** Compose actual PDFium and all approved parser wrappers into the WP11 helper using generated local gRPC controls. WP11 remains the helper host/protocol/launcher authority. This step implements the production parser composition in that same DesktopPlatform helper and publishes the next immutable ContentSandbox.Runtime.<rid> version with its exact native closure. Broker/Contracts and launcher mechanics are consumed from 11; no second helper design or duplicate DTO owner is created. Remove test-parser production registration, retain hostile regression fixtures.

**Testing requirements.** Packaged PDF page/text/tile fixtures, malformed/native-crash/hang and parent-death cleanup on every admitted RID; rerun actual image/media/OTIO parser containment.

**Completion gate.** Actual PDF dependency and containment evidence contributes to PG12; WP18.04 separately closes the real viewer path. No mock parser closes native producer acceptance.

<a id="rule-wp-13.14"></a>

### WP-13.14 — Portable graphics and optional OS backends

**What must be fully done.** Implement ArcGraphicsNative CPU surface/upload/present/fence/device-loss behavior on all admitted RIDs. Preserve ArcGraphicsMetalNative probe ABI unchanged; optional Metal code is a private backend of the new functional library, not functionality obtained through the three probe methods. Other admitted OS acceleration remains optional.

**Testing requirements.** CPU display/readback, ownership and fence lifetime, device loss and forced software path; exercise each advertised accelerator with its actual driver.

**Completion gate.** Required CPU functionality passes on every admitted RID; absent optional acceleration has a visible reason.

<a id="rule-wp-13.15"></a>

### WP-13.15 — Immutable native package production

**What must be fully done.** Publish ArcForges.Native.Abstractions plus Media/Colour/Image/Otio/Instruments/Pdf/Graphics and their Runtime.<rid> families: win-x64,win-arm64,osx-arm64,osx-x64,linux-x64,linux-arm64. Expand the allowlist explicitly; record any Tier 2 waiver and omit unusable capability claims. These eight managed and 42 runtime definitions are additional to other Platform mechanisms. Build native dependencies before pack; pack once; use the WP11 host/broker and the newly signed production helper version composed in 13.13. Never alter already released WP11 package bytes.

**Testing requirements.** Isolated clean-cache C17 and C# AOT consumers on each admitted RID; missing/transitive/wrong-RID library, hash collision, absent export, revoked artifact and source-unavailable negatives.

**Completion gate.** Same tested bytes, headers/import libraries, native manifests and complete dependency closures are promoted together; placeholders never satisfy a family.

<a id="rule-wp-13.16"></a>

### WP-13.16 — Dependency adoption and hardware receipts

**What must be fully done.** Record AD01–AD08 for FFmpeg, miniaudio, OCIO, OIIO, OpenEXR, Imath, OTIO, libusb and PDFium plus every shipped transitive dependency. Inventory serial/audio/GPU and an actual USB device with vendor/product identity, explicit interface/endpoint, firmware and driver versions.

**Testing requirements.** Match SBOM/license/source and enabled-feature lists to actual packaged files. Bind every physical result and each simulated absence to its evidence class.

**Completion gate.** PG03 and PG08 contributions cover the complete shipped graph and physical fixtures; remaining product/per-RID evidence stays explicitly assigned.

<a id="rule-wp-13.90"></a>
### WP-13.90 — Verify the owned artifact and real integration

**What must be fully done.** Verify the production outputs of 13.05–13.16 as one immutable candidate using actual 07–12 mechanisms. This step accepts completed implementations; it does not first design or implement the native families.

**Testing requirements.** Decode/seek/drain, encode→independent decode, image tiles, colour, OTIO, PDF, instruments, graphics CPU/fallback, cancel/lifetime/hostile-helper vectors and missing-DLL/wrong-RID negative consumers.

**Completion gate.** Probe-only exports never pass; complete portable functional producers and required per-RID closure verified before product WPs.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Probe B validates the store's recovery behaviour under real editing load |
| Protocol | Probe A validates capability invocation under AOT |
| UI | Probes B and D validate that the shell can host an editor and a video surface |
| Security | Probe D exercises the native safety obligations before any product depends on them |
| Platform | Probes C and D establish the hardware-lab requirement |
| Migration | None |
| Compatibility | Probe conclusions constrain the design of `33` and `36` |

---

## 7. Tests and verification evidence

[Local gRPC closure](../../architecture/contracts/09-local-grpc-and-sandbox.md): Invoke each real packaged media/image/PDF/OTIO helper method through generated gRPC over the restricted OS stream; verify slot races, generation/ack/cancel cleanup and throughput. No private XPC control or fake parser receipt.

| Evidence | Produced by |
|---|---|
| AOT publish log and an in-binary **device tool request** decoded and executed through generated, statically registered code — **no model loop is probed here**, it is the CF Workflow | [WP-13.00](#rule-wp-13.00) |
| Kill-during-edit recovery and undo distinction results | [WP-13.01](#rule-wp-13.01) |
| Sustained-throughput record with overrun, gap and pause results | [WP-13.02](#rule-wp-13.02) |
| Frame display, synchronisation measurement, sanitiser and sacrificial-process results | [WP-13.03](#rule-wp-13.03) |
| Four written probe conclusions | [WP-13.04](#rule-wp-13.04) |
| Common ABI and deterministic failure surface: behavioral, failure and package evidence | [WP-13.05](#rule-wp-13.05) |
| Media reader, probe, frame and seek: behavioral, failure and package evidence | [WP-13.06](#rule-wp-13.06) |
| Convert, resample and media writer: behavioral, failure and package evidence | [WP-13.07](#rule-wp-13.07) |
| Audio devices: behavioral, failure and package evidence | [WP-13.08](#rule-wp-13.08) |
| Colour transforms: behavioral, failure and package evidence | [WP-13.09](#rule-wp-13.09) |
| Still-image codecs: behavioral, failure and package evidence | [WP-13.10](#rule-wp-13.10) |
| OTIO interchange: behavioral, failure and package evidence | [WP-13.11](#rule-wp-13.11) |
| Serial and USB instruments: behavioral, failure and package evidence | [WP-13.12](#rule-wp-13.12) |
| PDF and production parser containment: behavioral, failure and package evidence | [WP-13.13](#rule-wp-13.13) |
| Portable graphics and optional OS backends: behavioral, failure and package evidence | [WP-13.14](#rule-wp-13.14) |
| Immutable native package production: behavioral, failure and package evidence | [WP-13.15](#rule-wp-13.15) |
| Dependency adoption and hardware receipts: behavioral, failure and package evidence | [WP-13.16](#rule-wp-13.16) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-13.90](#rule-wp-13.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-13.90](#rule-wp-13.90) and all inherited domain-specific gates must pass on the same candidate closure. Probe results are tied to package/RID/native graph identities and existing independent behavioral oracles; no full new reference audit or reference execution is added.

**[PG-03](../../assurance/open-gates-register.md#rule-pg-03) evidence:** [WP-13](#rule-wp-13) — Licence/provenance approval for each native dependency admitted by the probes. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. A device tool request is decoded and executed through generated, typed, statically registered code inside a published Native AOT binary, with no reflection path present. **The model loop is not probed here** — it is the CF Workflow ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02), **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**).
2. A kill during editing recovers to a committed boundary with explicit loss reporting, and undo is demonstrably not crash recovery.
3. Sustained acquisition above the product target runs with bounded memory, and every overrun, gap and disconnect is explicitly reported.
4. A decoded frame displays with synchronised audio; the sanitiser run is clean; the software fallback works with acceleration disabled.
5. Each probe has a written conclusion stating what it proved, what it did not, and what constraint it imposes downstream.
6. Every shipped dependency has a recorded licence position and the 13.16 hardware inventory exists, contributing to [PG-08](../../assurance/open-gates-register.md#rule-pg-08).

7. All 58 functional exports, eight managed native packages and every admitted runtime family are verified through clean package-only consumers; actual helper containment and all 13.05–13.16 gates pass. No probe-only export set passes production closure.

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [NAT.01](../delivery/lanes/native.md#task-nat-01) | [WP-13.00](13-high-risk-technical-probes.md#rule-wp-13.00) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution) | [PLT.18](../delivery/lanes/platform.md#task-plt-18) (artifact), [PLT.09](../delivery/lanes/platform.md#task-plt-09) (artifact), [PRF.04](../delivery/lanes/runtime-proofs.md#task-prf-04) (artifact) |
| [NAT.02](../delivery/lanes/native.md#task-nat-02) | [WP-13.01](13-high-risk-technical-probes.md#rule-wp-13.01) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution) | [PLT.01](../delivery/lanes/platform.md#task-plt-01) (artifact) |
| [NAT.03](../delivery/lanes/native.md#task-nat-03) | [WP-13.02](13-high-risk-technical-probes.md#rule-wp-13.02) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution) | none |
| [NAT.04](../delivery/lanes/native.md#task-nat-04) | [WP-13.03](13-high-risk-technical-probes.md#rule-wp-13.03) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution) | [PRF.01](../delivery/lanes/runtime-proofs.md#task-prf-01) (artifact) |
| [NAT.05](../delivery/lanes/native.md#task-nat-05) | [WP-13.04](13-high-risk-technical-probes.md#rule-wp-13.04) (full) | none |
| [NAT.06](../delivery/lanes/native.md#task-nat-06) | [WP-13.05](13-high-risk-technical-probes.md#rule-wp-13.05) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.07](../delivery/lanes/native.md#task-nat-07) | [WP-13.06](13-high-risk-technical-probes.md#rule-wp-13.06) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.08](../delivery/lanes/native.md#task-nat-08) | [WP-13.07](13-high-risk-technical-probes.md#rule-wp-13.07) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.09](../delivery/lanes/native.md#task-nat-09) | [WP-13.08](13-high-risk-technical-probes.md#rule-wp-13.08) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.10](../delivery/lanes/native.md#task-nat-10) | [WP-13.09](13-high-risk-technical-probes.md#rule-wp-13.09) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.11](../delivery/lanes/native.md#task-nat-11) | [WP-13.10](13-high-risk-technical-probes.md#rule-wp-13.10) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |
| [NAT.12](../delivery/lanes/native.md#task-nat-12) | [WP-13.11](13-high-risk-technical-probes.md#rule-wp-13.11) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.13](../delivery/lanes/native.md#task-nat-13) | [WP-13.12](13-high-risk-technical-probes.md#rule-wp-13.12) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.14](../delivery/lanes/native.md#task-nat-14) | [WP-13.13](13-high-risk-technical-probes.md#rule-wp-13.13) (all work except the parts mapped to PLT.54)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |
| [NAT.15](../delivery/lanes/native.md#task-nat-15) | [WP-13.14](13-high-risk-technical-probes.md#rule-wp-13.14) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | none |
| [NAT.20](../delivery/lanes/native.md#task-nat-20) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Media + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.21](../delivery/lanes/native.md#task-nat-21) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Colour + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.22](../delivery/lanes/native.md#task-nat-22) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Image + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.23](../delivery/lanes/native.md#task-nat-23) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Otio + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.24](../delivery/lanes/native.md#task-nat-24) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Instruments + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.25](../delivery/lanes/native.md#task-nat-25) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Pdf + Runtime.<rid>, plus the ContentSandbox.Runtime.<rid> republication from 13.13)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |
| [NAT.26](../delivery/lanes/native.md#task-nat-26) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Graphics + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.28](../delivery/lanes/native.md#task-nat-28) | [WP-13.16](13-high-risk-technical-probes.md#rule-wp-13.16) (full) | none |
| [NAT.30](../delivery/lanes/native.md#task-nat-30) | [WP-13.90](13-high-risk-technical-probes.md#rule-wp-13.90) (full) | none |
| [PLT.54](../delivery/lanes/platform.md#task-plt-54) | [WP-13.13](13-high-risk-technical-probes.md#rule-wp-13.13) (production parser composition and its own containment evidence) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |

**Consumers outside this package:** [APP.03](../delivery/lanes/app-composition.md#task-app-03), [NOTES.09](../delivery/lanes/arcnotes.md#task-notes-09), [NOTES.37](../delivery/lanes/arcnotes.md#task-notes-37), [PLT.45](../delivery/lanes/platform.md#task-plt-45), [PLT.46](../delivery/lanes/platform.md#task-plt-46), [SCOPE.04](../delivery/lanes/arcscope.md#task-scope-04), [SCOPE.11](../delivery/lanes/arcscope.md#task-scope-11), [SLATE.04](../delivery/lanes/arcslate.md#task-slate-04), [SLATE.15](../delivery/lanes/arcslate.md#task-slate-15), [SLATE.16](../delivery/lanes/arcslate.md#task-slate-16), [SLATE.19](../delivery/lanes/arcslate.md#task-slate-19), [SLATE.20](../delivery/lanes/arcslate.md#task-slate-20), [SLATE.21](../delivery/lanes/arcslate.md#task-slate-21), [SLATE.22](../delivery/lanes/arcslate.md#task-slate-22), [SLATE.24](../delivery/lanes/arcslate.md#task-slate-24), [SLATE.25](../delivery/lanes/arcslate.md#task-slate-25), [SLATE.27](../delivery/lanes/arcslate.md#task-slate-27), [SLATE.28](../delivery/lanes/arcslate.md#task-slate-28), [SLATE.38](../delivery/lanes/arcslate.md#task-slate-38), [SLATE.39](../delivery/lanes/arcslate.md#task-slate-39).

<!-- delivery-graph:end -->

