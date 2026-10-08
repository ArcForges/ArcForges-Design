<a id="rule-wp-13"></a>

# WP-13 — Complete Native Producers and Technical Probes

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Retire the two early technical risks and deliver the complete functional native producer set before product implementation consumes it. Probe evidence and production package evidence are distinct required outputs.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform and affected products. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Two isolated technical probes followed by the three functional native libraries, four managed native packages, three runtime package families across the six declared desktop RIDs, and integration with the WP11 restricted helper. The functional ABI, algorithms, formats and limits are fixed by [native annex 06](../../architecture/contracts/06-native-functional-abi.md); no missing function is deferred to product coding.

**Out of scope.** Product UI, editing commands, Cloud business handlers and the AI model loop. Probe scaffolds are cleaned up or kept as isolated regression fixtures. Production ABI/wrapper/runtime code from 13.05–13.16 is retained and published; [ND-05](../implementation-sequence.md#rule-nd-05) does not discard those deliverables.

**Why this package exists.** Every downstream native consumer needs working, versioned packages with their actual dependencies. Neither a probe-only DLL nor an appended verification instruction can substitute for implementing that producer here.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [Quality and compatibility requirements](../../requirements/12-quality-and-compatibility-contract.md) | The acceptance constraints for the two probes defined in this package; native and acquisition designs below supply their mechanisms |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§2` | The AOT resolution the agent probe must validate |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) | The native boundary and safety obligations the native probes and functional libraries must respect |
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
| `benchmarks/probes/acquisition/` | Probe C workspace and evidence |
| `native/arcimage-abi/` (the still-image shim, moved here by [GOV.17](../delivery/lanes/governance.md#task-gov-17) as `ArcImageNative`; the media/colour/OTIO shims are retired) | Extend the existing owned shim without renaming its published `arc_image_*` symbols |
| `native/arcinstruments-abi/` | New functional library with the fixed annex 06 declarations; the arcpdf-abi library is retired and not created ([P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)) |
| `src/Native/ArcForges.Native.Abstractions/` and `ArcForges.Native.Image/Instruments` | Three managed status/handle/wrapper packages (no Pdf wrapper, per [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)); slash-separated names here expand to separate projects |
| `src/Native/ArcForges.Native.<Capability>.Runtime.<rid>/` | Three families × six RID package definitions, each carrying its admitted native dependency closure |
| `src/DesktopHelpers/` | Consume WP11 helper/Broker/Contracts; add only the approved native parser composition, not a second helper owner |
| `eng/packaging/`, `tests/NativeConsumers/` | Exact package allowlist, headers/import libraries, SBOMs and independent C17/C# AOT package-only consumers |
| `eng/verification/probe-evidence/` | The recorded environments, procedures and results |
| `tests/HardwareLab/` | Created: the device inventory the later hardware families depend on |

**Major types introduced:** the fixed annex 06 status, safe handle, image and instrument wrappers; there is no PDF reader, writer or wrapper ([P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)). No native pointer becomes a managed domain identifier or a wire field.

---

## 5. Required implementation work

<a id="rule-wp-13.00"></a>

### WP-13.00 — Probe A: device tool execution under Native AOT

**What must be fully done.** The **device side** of the Harness runs inside a published Native AOT desktop binary: it pulls a stub `ToolRequest`, re-authorises it locally, resolves a `CapabilityKey` through the **generated allowlist**, decodes structured arguments into a **typed** product request (`§3.1` of the local RPC contract), invokes it, and returns an idempotent result. **The model loop is not probed here — it runs in the C# Cloud Harness, not a Cloudflare Workflow** ([P2-021](../../decisions/phase-2-specification-decisions.md#rule-p2-021); this supersedes the Workflow placement of [LS-02](../../architecture/17-agent-harness.md#rule-ls-02)). What is at risk under AOT is the generated decode and static registration path, not the loop. No reflection, no dynamic assembly, no runtime code generation is involved. Static registration and out-of-process extensibility are both exercised.

**Testing requirements.** An AOT publish log with zero diagnostics; an end-to-end `ToolRequest` → decode → typed invocation → result run inside the published binary; a negative test confirming a reflection-based registration or decode path fails to compile or is absent; a containment test confirming the structured value type appears only in the boundary dispatch assembly ([DP-02](../../architecture/contracts/02-local-rpc-operations.md#rule-dp-02)).

**Completion gate.** A device tool request is decoded and executed through generated, typed, statically registered code inside a published AOT binary, with no reflection path present.

<a id="rule-wp-13.02"></a>

### WP-13.02 — Probe C: high-throughput acquisition

**What must be fully done.** Sustained acquisition from a real transport at a rate above the intended product target, through a ring buffer, with plot downsampling that keeps the display responsive. Overrun is surfaced with a count and a timestamp, never hidden. Pausing the view does not stop recording. A disconnect leaves an explicit gap.

**Testing requirements.** A sustained-throughput run with recorded rate, memory and drop counts; an induced overrun; an induced disconnect; a pause-view-while-recording test.

**Completion gate.** Sustained throughput above target with bounded memory, and every overrun, gap and disconnect explicitly reported.

<a id="rule-wp-13.04"></a>

### WP-13.04 — Evidence, licence positions and conclusions

**What must be fully done.** Each probe produces a written conclusion: what was proven, what was not, what constraint it imposes on the owning product package, and what remains open. Every native dependency introduced receives a licence position. The hardware-lab device inventory is created with device, firmware and driver versions.

**Testing requirements.** A completeness check that each probe has a recorded environment, procedure, result and conclusion.

**Completion gate.** Two conclusions exist, every native dependency has a licence position, and the hardware inventory exists. This seeds [PG-08](../../assurance/open-gates-register.md#rule-pg-08);13.16 completes its production inventory and the full [PG-03](../../assurance/open-gates-register.md#rule-pg-03) dependency obligations.

---

<a id="rule-wp-13.05"></a>

### WP-13.05 — Common ABI and deterministic failure surface

**What must be fully done.** Implement annex 06 common preambles, fixed numeric keys, pack 8 records, ownership, cancellation and bounded-buffer helpers underlying the ABI1.1 declarations. This step compiles all declarations; the family bodies are implemented in 13.10, 13.12 and 13.13 and their complete runtime export set is accepted in 13.15/13.90. Retain the existing `arc_image_*` probe-library identity; compatibility with it is not evidence of functional behavior.

**Testing requirements.** Compile C17/C++20 headers and C# layouts; assert every field offset and all 17 sizes, wrong-size/version/null/closed-handle cases and zero leaked output on failure.

**Completion gate.** The common helpers, complete header/layout declarations and common failure rules are independently verified; later family implementation is not required to pass this first substep.

<a id="rule-wp-13.10"></a>

### WP-13.10 — Still-image codecs

**What must be fully done.** Implement PNG/TIFF/EXR metadata and bounded tile reads with OIIO/OpenEXR/Imath as the `ArcImageNative` logical library in `native/arcimage-abi` (moved there by [GOV.17](../delivery/lanes/governance.md#task-gov-17), publishing unchanged `arc_image_*` symbols); hostile reads execute only in WP11 helper.

**Testing requirements.** Bit depth/metadata round trip, edge tiles, decompression bomb, failed codec and incomplete-output refusal.

**Completion gate.** All image exports and named codec degradation pass without silent image loss.

<a id="rule-wp-13.12"></a>

### WP-13.12 — Serial and USB instruments

**What must be fully done.** Implement generic OS serial and explicit USB interface/endpoint open/read/write/cancel/close; identity is revalidated at open. Do not auto-detach unrelated drivers or enable vendor SDKs.

**Testing requirements.** Enumeration, explicit interface claim, control/bulk/interrupt transfers, partial writes, cancellation callback, hot unplug, driver absence and permission denial on Tier 1.

**Completion gate.** Native instrument functions and permission/loss semantics pass against the hardware inventory.

<a id="rule-wp-13.13"></a>

### WP-13.13 — Production still-image parser containment (PDF retired, P2-022)

**What must be fully done.** Compose the approved still-image parser wrappers (the NAT.11 family) into the WP11 helper using generated local gRPC controls; PDFium and PDF parsing are retired ([P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)), and image composition is owned by NAT.31. WP11 remains the helper host/protocol/launcher authority. This step implements the production still-image parser composition in that same DesktopPlatform helper and publishes the next immutable ContentSandbox.Runtime.<rid> version with its exact native closure. Broker/Contracts and launcher mechanics are consumed from 11; no second helper design or duplicate DTO owner is created. Remove test-parser production registration, retain hostile regression fixtures.

**Testing requirements.** Packaged image decode/tile fixtures, malformed/native-crash/hang and parent-death cleanup on every admitted RID; rerun actual image parser containment.

**Completion gate.** Actual image-parser dependency and containment evidence contributes to PG-22 (PG-12 is retired under [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)). No mock parser closes native producer acceptance.

<a id="rule-wp-13.15"></a>

### WP-13.15 — Immutable native package production

**What must be fully done.** Publish ArcForges.Native.Abstractions plus Image and Instruments and their Runtime.<rid> families: win-x64, win-arm64, linux-x64 and linux-arm64 (no osx RIDs, per [P2-023](../../decisions/phase-2-specification-decisions.md#rule-p2-023)). Expand the allowlist explicitly; record any Tier 2 waiver and omit unusable capability claims. These three managed and eight runtime definitions are additional to other Platform mechanisms. Build native dependencies before pack; pack once; use the WP11 host/broker and the newly signed production helper version composed in 13.13. Never alter already released WP11 package bytes.

**Testing requirements.** Isolated clean-cache C17 and C# AOT consumers on each admitted RID; missing/transitive/wrong-RID library, hash collision, absent export, revoked artifact and source-unavailable negatives.

**Completion gate.** Same tested bytes, headers/import libraries, native manifests and complete dependency closures are promoted together; placeholders never satisfy a family.

<a id="rule-wp-13.16"></a>

### WP-13.16 — Dependency adoption and hardware receipts

**What must be fully done.** Record AD01–AD08 for OIIO, OpenEXR, Imath and libusb plus every shipped transitive dependency; PDFium is not admitted (retired under [P2-022](../../decisions/phase-2-specification-decisions.md#rule-p2-022)). Inventory serial hardware and an actual USB device with vendor/product identity, explicit interface/endpoint, firmware and driver versions.

**Testing requirements.** Match SBOM/license/source and enabled-feature lists to actual packaged files. Bind every physical result and each simulated absence to its evidence class.

**Completion gate.** PG03 and PG08 contributions cover the complete shipped graph and physical fixtures; remaining product/per-RID evidence stays explicitly assigned.

<a id="rule-wp-13.90"></a>
### WP-13.90 — Verify the owned artifact and real integration

**What must be fully done.** Verify the production outputs of 13.05–13.16 as one immutable candidate using actual 07–12 mechanisms. This step accepts completed implementations; it does not first design or implement the native families.

**Testing requirements.** Image tiles, instruments, cancel/lifetime/hostile-helper vectors and missing-DLL/wrong-RID negative consumers.

**Completion gate.** Probe-only exports never pass; complete portable functional producers and required per-RID closure verified before product WPs.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | Probe A validates capability invocation under AOT |
| UI | Probe C validates that the shell can host a responsive live acquisition plot |
| Security | The retained native libraries (image and instruments; PDF retired per P2-022) exercise the native safety obligations before any product depends on them |
| Platform | Probe C establishes the hardware-lab requirement |
| Migration | None |
| Compatibility | Probe conclusions constrain the design of `33` |

---

## 7. Tests and verification evidence

[Local gRPC closure](../../architecture/contracts/09-local-grpc-and-sandbox.md): Invoke each real packaged image helper method through generated gRPC over the restricted OS stream; verify slot races, generation/ack/cancel cleanup and throughput. No private control channel or fake parser receipt.

| Evidence | Produced by |
|---|---|
| AOT publish log and an in-binary **device tool request** decoded and executed through generated, statically registered code — **no model loop is probed here**, it is the C# Cloud Harness ([P2-021](../../decisions/phase-2-specification-decisions.md#rule-p2-021)) | [WP-13.00](#rule-wp-13.00) |
| Sustained-throughput record with overrun, gap and pause results | [WP-13.02](#rule-wp-13.02) |
| Two written probe conclusions | [WP-13.04](#rule-wp-13.04) |
| Common ABI and deterministic failure surface: behavioral, failure and package evidence | [WP-13.05](#rule-wp-13.05) |
| Still-image codecs: behavioral, failure and package evidence | [WP-13.10](#rule-wp-13.10) |
| Serial and USB instruments: behavioral, failure and package evidence | [WP-13.12](#rule-wp-13.12) |
| Production still-image parser containment (PDF retired, P2-022): behavioral, failure and package evidence | [WP-13.13](#rule-wp-13.13) |
| Immutable native package production: behavioral, failure and package evidence | [WP-13.15](#rule-wp-13.15) |
| Dependency adoption and hardware receipts: behavioral, failure and package evidence | [WP-13.16](#rule-wp-13.16) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-13.90](#rule-wp-13.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-13.90](#rule-wp-13.90) and all inherited domain-specific gates must pass on the same candidate closure. Probe results are tied to package/RID/native graph identities and existing independent behavioral oracles; no full new reference audit or reference execution is added.

**[PG-03](../../assurance/open-gates-register.md#rule-pg-03) evidence:** [WP-13](#rule-wp-13) — Licence/provenance approval for each native dependency admitted by the probes. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. A device tool request is decoded and executed through generated, typed, statically registered code inside a published Native AOT binary, with no reflection path present. **The model loop is not probed here** — it runs in the C# Cloud Harness ([P2-021](../../decisions/phase-2-specification-decisions.md#rule-p2-021)).
2. Sustained acquisition above the product target runs with bounded memory, and every overrun, gap and disconnect is explicitly reported.
3. Each probe has a written conclusion stating what it proved, what it did not, and what constraint it imposes downstream.
4. Every shipped dependency has a recorded licence position and the 13.16 hardware inventory exists, contributing to [PG-08](../../assurance/open-gates-register.md#rule-pg-08).

5. All 14 functional exports, four managed native packages and every admitted runtime family are verified through clean package-only consumers; actual helper containment and all 13.05–13.16 gates pass. No probe-only export set passes production closure.

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [NAT.01](../delivery/lanes/native.md#task-nat-01) | [WP-13.00](13-high-risk-technical-probes.md#rule-wp-13.00) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution) | [PLT.18](../delivery/lanes/platform.md#task-plt-18) (artifact), [PLT.09](../delivery/lanes/platform.md#task-plt-09) (artifact), [PRF.04](../delivery/lanes/runtime-proofs.md#task-prf-04) (artifact) |
| [NAT.03](../delivery/lanes/native.md#task-nat-03) | [WP-13.02](13-high-risk-technical-probes.md#rule-wp-13.02) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution) | none |
| [NAT.05](../delivery/lanes/native.md#task-nat-05) | [WP-13.04](13-high-risk-technical-probes.md#rule-wp-13.04) (full) | none |
| [NAT.06](../delivery/lanes/native.md#task-nat-06) | [WP-13.05](13-high-risk-technical-probes.md#rule-wp-13.05) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | [GOV.17](../delivery/lanes/governance.md#task-gov-17) (artifact) |
| [NAT.11](../delivery/lanes/native.md#task-nat-11) | [WP-13.10](13-high-risk-technical-probes.md#rule-wp-13.10) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact), [GOV.17](../delivery/lanes/governance.md#task-gov-17) (artifact) |
| [NAT.13](../delivery/lanes/native.md#task-nat-13) | [WP-13.12](13-high-risk-technical-probes.md#rule-wp-13.12) (full)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution) | [GOV.17](../delivery/lanes/governance.md#task-gov-17) (artifact) |
| [NAT.14](../delivery/lanes/native.md#task-nat-14) | [WP-13.13](13-high-risk-technical-probes.md#rule-wp-13.13) (composition, interfaces, limits and fake-backend containment tests; excludes the real PDFium build/binding and real-parser containment acceptance (NAT.15) and the parts mapped to PLT.54)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution (interface-level part: probe scaffolds retired or kept as regression fixtures for the PDF family seam; the real-library part is NAT.15))<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution (interface-level part: major-types note and no native pointer crossing the ABI for the PDF family; the real-library part is NAT.15)) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact), [GOV.17](../delivery/lanes/governance.md#task-gov-17) (artifact) |
| [NAT.15](../delivery/lanes/native.md#task-nat-15) | [WP-13.13](13-high-risk-technical-probes.md#rule-wp-13.13) (the real PDFium (chromium/8044) build and binding, the packaged PDF page/text/tile fixtures, malformed/native-crash/hang and parent-death cleanup against the real library on every admitted RID, rerun of the actual image-parser containment, and the next immutable ContentSandbox.Runtime.<rid> composition input; the composition, interfaces, limits and fake-backend tests are NAT.14)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS1/[ND-05](../implementation-sequence.md#rule-nd-05): probe scaffolds (13.00-13.03) are cleanup-or-regression-fixture; production 13.05-13.16 code is retained and maintained -- different lifecycle rules for the two groups even though both may live under similar directories (package-level obligation contribution (real-library part: probe scaffolds retired against the real PDFium build; the interface-level part is NAT.14))<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) SS4 major-types note: no native pointer becomes a managed domain identifier or a wire field (package-level obligation contribution (real-library part: major-types note verified against the real PDFium binding; the interface-level part is NAT.14)) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |
| [NAT.22](../delivery/lanes/native.md#task-nat-22) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Image + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.24](../delivery/lanes/native.md#task-nat-24) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Instruments + Runtime.<rid> only)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | none |
| [NAT.25](../delivery/lanes/native.md#task-nat-25) | [WP-13.15](13-high-risk-technical-probes.md#rule-wp-13.15) (ArcForges.Native.Pdf + Runtime.<rid>, plus the ContentSandbox.Runtime.<rid> republication from 13.13)<br>[WP-13](13-high-risk-technical-probes.md#rule-wp-13) producer-artifacts-and-integration.md WP13 row: 'Probe-only 1.0, missing functional export or dependency prevents completion' (package-level obligation contribution) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |
| [NAT.28](../delivery/lanes/native.md#task-nat-28) | [WP-13.16](13-high-risk-technical-probes.md#rule-wp-13.16) (full) | none |
| [NAT.30](../delivery/lanes/native.md#task-nat-30) | [WP-13.90](13-high-risk-technical-probes.md#rule-wp-13.90) (full) | [GOV.17](../delivery/lanes/governance.md#task-gov-17) (artifact) |
| [PLT.54](../delivery/lanes/platform.md#task-plt-54) | [WP-13.13](13-high-risk-technical-probes.md#rule-wp-13.13) (production parser composition and its own containment evidence) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact) |

**Consumers outside this package:** [APP.03](../delivery/lanes/app-composition.md#task-app-03), [PLT.45](../delivery/lanes/platform.md#task-plt-45), [PLT.46](../delivery/lanes/platform.md#task-plt-46), [SCOPE.04](../delivery/lanes/arcscope.md#task-scope-04), [SCOPE.11](../delivery/lanes/arcscope.md#task-scope-11).

<!-- delivery-graph:end -->

