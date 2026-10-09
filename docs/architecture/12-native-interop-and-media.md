# Native Interoperability Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Native AOT desktop), **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** (deferred-decision ownership), the technology constitution and closed exception list (`§8` of [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md))
> Companions: [`04-desktop-application-architecture.md`](04-desktop-application-architecture.md), [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md), [`../requirements/products/arcscope.md`](../requirements/products/arcscope.md)

Native code exists in ArcForges for one reason: some low-level capability has no reasonable managed substitute. It never exists because native code is faster in general, because the team is more familiar with it, or because an implementation already exists elsewhere. This document defines the boundary that keeps that concession small, auditable and reversible, and the still-image and acquisition pipelines that sit on top of it. PDF preview and PDF parsing are retired ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)).

---

## 1. The controlling position

| # | Rule |
|---|---|
| <a id="rule-ni-01"></a>NI-01 | No C++ business worker is permitted. Native libraries execute in the product or its explicitly approved C# Native AOT content helper according to [isolation architecture](24-content-and-extension-isolation.md). The helper holds no product logic or persistent authority. |
| <a id="rule-ni-02"></a>NI-02 | **Only low-level libraries with no reasonable substitute are native**: codecs, GPU access, device SDKs, system APIs and high-performance primitives. |
| <a id="rule-ni-03"></a>NI-03 | **A native library must never own ArcForges domain**. A native decoder is permitted; a native project manager, task scheduler, state owner or business-rule engine is not — *even where native performance would be higher*. |
| <a id="rule-ni-04"></a>NI-04 | **Product area, business rules, Task, state ownership, scheduling, persistence, policy and UI are C#**. |
| <a id="rule-ni-05"></a>NI-05 | **Where a dependency offers only a C++ API, a very thin `extern "C"` ABI shim is provided under `native/`**. That shim is a *library adaptation*, holds no product business state, and is not a route back to a worker. |
| <a id="rule-ni-06"></a>NI-06 | **A native resource belongs to exactly one product process**. An ArcScope device handle and a ContentSandbox image tile must never enter an ArcChat domain object, a Cloud DTO, or a `ResourceRef` as a raw pointer. |
| <a id="rule-ni-07"></a>NI-07 | **Only stable resource identity, metadata and controlled access cross a process boundary**. |
| <a id="rule-ni-08"></a>NI-08 | **The native surface is deliberately small.** Growth in the native ABI is a reviewed architectural change, not an implementation detail. |
| <a id="rule-ni-09"></a>NI-09 | **Untrusted third-party native plug-ins never load into a stable main process**. |
| <a id="rule-ni-10"></a>NI-10 | [P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007) exercises [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016) for the C# content-isolation helper and OS-enforced extension profiles. Other isolated hosts still require their own decision. The approved helper does not become a model loop, service, scheduler or C++ domain host. |

### 1.1 What this costs, stated plainly

A native memory error kills the process that loaded the library. Hostile parsing therefore runs in the C# content helper, where failure can be contained. In-process GPU/device calls retain a stated native crash/recovery risk. ABI validation and fuzzing reduce defects but do not create memory isolation.

---

## 2. Where native code is permitted

| Product | Permitted native surface | Explicitly not permitted |
|---|---|---|
| ArcScope | Device and transport SDKs, high-rate acquisition primitives, hardware timestamps, high-performance signal primitives | Session model, capture lifecycle, trigger semantics, analysis definitions, evidence storage |
| ArcChat | Platform system APIs where required — global hotkey, notification, secure storage; **still-image decoding for thin attachment preview is out of V1** ([P2-026](../decisions/phase-2-specification-decisions.md#rule-p2-026): V1 shows image attachments as metadata cards, `§2.1`; PDF rendering and text extraction retired by [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)) | Anything in the conversation, task or capability model; any editing, layout or authoring path |
| Cloud | **None.** Cloud is managed code on a managed hosting platform (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | All native dependencies |
| Mobile and Web | Platform framework only; no first-party native ABI | A first-party C ABI shim |

| # | Rule |
|---|---|
| <a id="rule-np-01"></a>NP-01 | **A native dependency is introduced per product, with a named owner and a stated substitute analysis** — which managed option was evaluated, and why it was insufficient. |
| <a id="rule-np-02"></a>NP-02 | **A native library used by two products is still loaded per process**, with no shared global state between them. |
| <a id="rule-np-03"></a>NP-03 | **No global shared memory pool exists across products**. |

### 2.1 ArcChat image attachments — metadata cards in V1 (PDF retired; P2-026)

**P2-026 (V1 scope correction, 2026-10-09).** The embedded assistant does not decode still images in V1, so the permitted native surface is not extended to still-image decoding for V1. Image attachments are fully supported as attachments: they are attached, stored, synced, exported, sent to an admitted model, and saved or opened externally by an explicit user action. In the app each image attachment is shown as a metadata card (type, name and size), with the type determined by magic-byte sniffing only (PNG, JPEG, GIF and WebP) in managed code and with no decode of untrusted image bytes. The in-app decoded thumbnail is out of V1 scope and is recorded as out of scope, not completed. Any later decode route (managed or native) needs its own reviewed decision, and the rules below that describe a still-image decode path (DR-01 and DR-04) apply only to such a route. NAT.31 is out of scope. The former PDF rasterisation and PDF text-extraction surface is retired ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)); no product has a native PDF preview or a PDF parsing path. ArcScope report export (`arcscope.report.pdf.v1`) is retained by [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022): report PDF production is not part of this retirement, its writer is admitted separately under SCOPE.18, and PDFium is not a writer. Companions present an exported report only through the platform viewer or as a download.

| # | Rule |
|---|---|
| <a id="rule-dr-01"></a>DR-01 | **Not in V1 ([P2-026](../decisions/phase-2-specification-decisions.md#rule-p2-026)). If a later reviewed decision admits a decode route, the extension covers exactly one operation**: decoding a still image to a bitmap tile at a requested scale. The former page-rasterisation and bounded-text operations were PDF operations and are retired ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)). Nothing else. |
| <a id="rule-dr-02"></a>DR-02 | **No content, editing or authoring path may call it.** Only the assistant's thin-preview surface may reference the wrapper (`§2`), and a repository policy test asserts it. |
| <a id="rule-dr-03"></a>DR-03 | **[NP-01](#rule-np-01) is not waived by this amendment.** The named owner, the substitute analysis, the licence position and the provenance record are prerequisites to adoption, not follow-ups (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**). |
| <a id="rule-dr-04"></a>DR-04 | (P2-026: applies only if a later reviewed decision admits a decode route; V1 performs none.) Still-image parsing and decoding run inside the C# ContentSandbox under the [mandatory OS profile](24-content-and-extension-isolation.md). The viewer brokers input and validates bounded results. C ABI discipline, signed loading and lifetime checks remain required; child crash/hang produces a metadata card without taking down the parent. No PDF parser runs in any helper. |
| <a id="rule-dr-05"></a>DR-05 | **The assistant's PDF preview is retired, not pending** ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)). PDF attachments are generic attachments: stored, transferred and downloaded as opaque files, with no parsing, presented as a metadata card whose only action is Save As (PDF attachments: Save As only); the app performs no in-app PDF parsing or rendering ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 2). [PG-12](../assurance/open-gates-register.md#rule-pg-12) is retired and is never completed; no PDF preview or PDF parsing path is a pending capability. |
| <a id="rule-dr-06"></a>DR-06 | **Retired by [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022).** The identifier is not reused. The original text, which let further document-rendering operations use this surface, is superseded. |

---

## 3. Managed-to-native calling discipline

### 3.1 Binding

| # | Rule |
|---|---|
| <a id="rule-pi-01"></a>PI-01 | **`[LibraryImport]` source-generated P/Invoke is the default**, required for Native AOT correctness and for compile-time marshalling diagnostics. |
| <a id="rule-pi-02"></a>PI-02 | **`[DllImport]` is used only where generated marshalling cannot cover the case**, and only with the specific usage verified and recorded. |
| <a id="rule-pi-03"></a>PI-03 | **All P/Invoke declarations for one native library live in one `internal static partial class`** in the infrastructure project that owns it. They are never scattered across feature code. |
| <a id="rule-pi-04"></a>PI-04 | **No feature code calls a P/Invoke declaration directly.** A managed wrapper type owns every call, so validation, handle lifetime and error translation exist in exactly one place. |
| <a id="rule-pi-05"></a>PI-05 | **Strings marshal as UTF-8** with `StringMarshalling.Utf8`, and allocation and free responsibility is stated at every function that returns a string. |
| <a id="rule-pi-06"></a>PI-06 | **Blittable structs only across the boundary.** No managed object graph, no reference type, no `bool` of unspecified width, no `char`. |
| <a id="rule-pi-07"></a>PI-07 | **Callbacks use function pointers with an explicitly stated lifetime**; delegate and function-pointer lifetimes are pinned for as long as native code can call them. |

### 3.2 The C ABI contract

Every first-party native library, and every `extern "C"` shim over a third-party C++ library, obeys the following. These are the terms the managed side is entitled to rely on.

| # | Rule |
|---|---|
| <a id="rule-ab-01"></a>AB-01 | **The C calling convention is explicit and stable across compilers**. |
| <a id="rule-ab-02"></a>AB-02 | **Every exported function carries a fixed prefix and an ABI version** — for example `arc_image_*`. |
| <a id="rule-ab-03"></a>AB-03 | **Existing frozen POD views/buffers/rationals keep their ABI1.0 layout.** New extensible records carry size/version and append-only compatible tails. Existing field order/size/meaning never changes. [Functional ABI](contracts/06-native-functional-abi.md) supplies exact declarations and wrapper/package mapping. |
| <a id="rule-ab-04"></a>AB-04 | **Fixed-width integer types only.** |
| <a id="rule-ab-05"></a>AB-05 | **C++ `bool`, STL types, exceptions, RTTI and vtables never cross the boundary**. |
| <a id="rule-ab-06"></a>AB-06 | **Handles are opaque pointers**; the managed side always represents them as a `SafeHandle`. |
| <a id="rule-ab-07"></a>AB-07 | **Resource ownership is stated explicitly in every function's contract and asserted by a test**: who allocates, who frees, and when. |
| <a id="rule-ab-08"></a>AB-08 | **A native exception never crosses the C ABI.** A status or error object is returned instead. |
| <a id="rule-ab-09"></a>AB-09 | **Callbacks have a defined registration, deregistration, threading, reentrancy and shutdown protocol**. A callback that can fire after deregistration is a defect. |
| <a id="rule-ab-10"></a>AB-10 | **Functions are as coarse-grained as practical.** A P/Invoke per pixel or per signal sample is prohibited; work is submitted in buffers, plans or batches. |
| <a id="rule-ab-11"></a>AB-11 | **Every length is checked for overflow and against its upper bound in managed code before the call**. |
| <a id="rule-ab-12"></a>AB-12 | **The ABI version is negotiated at load, not assumed.** A mismatch is a startup failure with an actionable message, never a crash later. |

### 3.3 Loading

| # | Rule |
|---|---|
| <a id="rule-ld-01"></a>LD-01 | **`NativeLibrary.SetDllImportResolver` maps logical library names to RID-specific assets published and signed with the application**. |
| <a id="rule-ld-02"></a>LD-02 | **Prohibited**: loading from the current working directory; loading an unsigned library from a user-writable search path; modifying the global search path to resolve dependencies; allowing a same-named system library to be picked up by accident. |
| <a id="rule-ld-03"></a>LD-03 | **Startup verification confirms** ABI version, build identifier and hash, required entry points, CPU and GPU feature availability, and minimum driver or system capability. |
| <a id="rule-ld-04"></a>LD-04 | **A failed verification degrades a feature explicitly**, with a named reason surfaced to the user and recorded in diagnostics. It never silently disables a capability, and never proceeds with a partially verified library. |
| <a id="rule-ld-05"></a>LD-05 | **Native assets are part of the signed package**, covered by the same signing and provenance requirements as managed assemblies. |
| <a id="rule-ld-06"></a>LD-06 | **Native asset versions, hashes and source provenance are recorded in the release record** ([`14-build-packaging-and-release.md`](14-build-packaging-and-release.md)). |
| <a id="rule-ld-07"></a>LD-07 | **Native library licences are recorded and reviewed against the licence boundary of the consuming product** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, the **[F-013](../assurance/open-gates-register.md#rule-f-013)** gate). A native dependency incompatible with a product's licence is not shipped in that product. |

### 3.4 Handles and lifetime

| # | Rule |
|---|---|
| <a id="rule-hl-01"></a>HL-01 | **Every native handle kind has a dedicated `SafeHandle` subclass**. A raw pointer is never held in a field. |
| <a id="rule-hl-02"></a>HL-02 | **A reference-counted guard wraps every call that passes a handle**, so a handle cannot be freed while native code is using it. |
| <a id="rule-hl-03"></a>HL-03 | **Asynchronous wrappers implement `IAsyncDisposable`**. |
| <a id="rule-hl-04"></a>HL-04 | **Finalizers are a last-resort safety net**, never the normal release path. |
| <a id="rule-hl-05"></a>HL-05 | **The native runtime shuts down only after UI and RPC have stopped accepting new work**, so no call is in flight while teardown runs. |
| <a id="rule-hl-06"></a>HL-06 | **Handle leaks are detectable.** Debug and test builds assert that every created handle is disposed at scope exit, and handle counts are asserted in soak tests. |

---

## 4. Buffers and the large-data path

| # | Rule |
|---|---|
| <a id="rule-bf-01"></a>BF-01 | **CPU buffers use `Span<T>`, `Memory<T>`, a memory pool and controlled pinned memory**. |
| <a id="rule-bf-02"></a>BF-02 | **Pinning is scoped and short.** A long-lived pinned region is a documented exception with a stated reason. |
| <a id="rule-bf-03"></a>BF-03 | **Pooled buffers are returned on every path including failure**, and pool exhaustion is a measured, surfaced condition rather than an unbounded allocation. |
| <a id="rule-bf-04"></a>BF-04 | **A per-frame image is never serialised over gRPC, the HTTP client or the realtime channel**. |
| <a id="rule-bf-05"></a>BF-05 | **The application runtime never relays raw capture frames or large file bodies**. |
| <a id="rule-bf-06"></a>BF-06 | **GPU resources are shared inside the process through a platform-specific rendering bridge; the UI receives only presentable surface or bitmap abstractions**. |
| <a id="rule-bf-07"></a>BF-07 | **Cross-process large data uses `ResourceRef` plus a controlled stream, file-handle strategy or temporary resource channel**, never an inline payload. |
| <a id="rule-bf-08"></a>BF-08 | **`ResourceRef` never carries a raw pointer, GPU handle or device handle** ([NI-06](#rule-ni-06)). It carries identity and metadata only ([RR-01](02-contracts-and-protocols.md#rule-rr-01)–[RR-14](02-contracts-and-protocols.md#rule-rr-14) in the contract architecture). |
| <a id="rule-bf-09"></a>BF-09 | **Backpressure is explicit.** A producer that outruns its consumer blocks, drops with a recorded reason, or fails; it never grows without bound. |

---

## 5. Threading across the boundary

| # | Rule |
|---|---|
| <a id="rule-th-01"></a>TH-01 | **Native work never runs on the UI thread.** Decode, encode, acquisition, analysis and GPU submission run on dedicated or pooled non-UI threads (`§4` of the desktop architecture). |
| <a id="rule-th-02"></a>TH-02 | **A native callback thread is not a managed synchronisation context.** Callback bodies do the minimum work and hand off to a managed queue. |
| <a id="rule-th-03"></a>TH-03 | **No managed lock is held across a native call that can block, and no native lock is held across a managed callback.** |
| <a id="rule-th-04"></a>TH-04 | **Cancellation is cooperative and defined per operation.** A native operation that cannot be cancelled is bounded in duration and documented as such. |
| <a id="rule-th-05"></a>TH-05 | **Thread affinity requirements of a device or GPU context are honoured explicitly**, with a dedicated owning thread where the underlying API demands one. |
| <a id="rule-th-06"></a>TH-06 | **Re-entrancy is prohibited by construction**: a callback never calls back into the same native object under the same lock. |

---

## 6. Failure and safety boundaries

These mitigations supplement the mandatory hostile-content process boundary. They do not substitute for OS isolation or make an access violation catchable in the parent.

| # | Obligation |
|---|---|
| <a id="rule-sb-01"></a>SB-01 | **The native ABI is kept extremely small.** Every addition is reviewed. |
| <a id="rule-sb-02"></a>SB-02 | **Input is validated in managed code before it reaches native code** — sizes, ranges, formats, counts, alignment. |
| <a id="rule-sb-03"></a>SB-03 | **Native libraries are built with sanitiser configurations** — address and undefined behaviour — for test builds. |
| <a id="rule-sb-04"></a>SB-04 | **Image parsers are fuzzed**, with a corpus retained and extended by every parser defect found. PDF parsers are retired ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)). |
| <a id="rule-sb-05"></a>SB-05 | **Native integration tests run in a sacrificial process**, so a crash fails a test rather than the test host. |
| <a id="rule-sb-06"></a>SB-06 | **Crash dumps, symbols and build identifiers are retained in production**, and are sufficient to resolve a native frame. |
| <a id="rule-sb-07"></a>SB-07 | **Business recovery relies on the journal** (`§3` of the persistence architecture). A native crash loses at most work since the last committed boundary, never committed work. |
| <a id="rule-sb-08"></a>SB-08 | **A repeated native crash on the same input is a quarantine condition.** The offending asset, device or code path is marked, the user is told, and the application starts in a degraded but usable state (safe start, `§5` of the desktop architecture). |
| <a id="rule-sb-09"></a>SB-09 | **Untrusted content is treated as hostile input at the native boundary.** An untrusted file, capture stream or imported asset from outside the user's trust domain is parsed with the same suspicion as network input (`§7` of the security architecture). |
| <a id="rule-sb-10"></a>SB-10 | **A native defect that cannot be mitigated within these obligations is grounds for removing the dependency**, not for relaxing the obligations. |

---

## 7. The ArcScope acquisition pipeline

### 7.1 Structure

```
SourceAdapter — serial · TCP · UDP · file replay · later device SDK      C#
      ↓ native transport and device primitives where required
Acquisition loop — bounded, timestamped, backpressure-aware              C#
      ↓
Rolling buffer (live view)            Durable capture writer (evidence)
      ↓                                          ↓
Decode · measure · analyse               Chunked verifiable store
      ↓
Visualisation
```

| # | Rule |
|---|---|
| <a id="rule-aq-01"></a>AQ-01 | **The acquisition loop, capture lifecycle and trigger semantics are C#** ([NI-03](#rule-ni-03)). Native code supplies transport, device access, timestamps and high-rate primitives only. |
| <a id="rule-aq-02"></a>AQ-02 | **Live observation and capture are separate paths** ([SE-04](../requirements/products/arcscope.md#rule-se-04) in the ArcScope requirements). Pausing the view never stops recording ([SE-05](../requirements/products/arcscope.md#rule-se-05)). |
| <a id="rule-aq-03"></a>AQ-03 | **Raw capture is written to the chunked verifiable store** ([SE-14](../requirements/products/arcscope.md#rule-se-14) there), never buffered through a component that can lose it silently. |
| <a id="rule-aq-04"></a>AQ-04 | **An acquisition overrun is surfaced, never hidden.** Dropped samples are counted, timestamped and recorded as a gap in the capture. |
| <a id="rule-aq-05"></a>AQ-05 | **Hardware timestamps are preserved where available**, with the timing source recorded in the effective configuration snapshot ([SD-05](../requirements/products/arcscope.md#rule-sd-05) there). Where no hardware timestamp exists, the host timing source and its uncertainty are recorded. |
| <a id="rule-aq-06"></a>AQ-06 | **A device handle never leaves the owning process** ([NI-06](#rule-ni-06)). Exclusive access is coordinated with lease and busy semantics ([SD-08](../requirements/products/arcscope.md#rule-sd-08) there). |
| <a id="rule-aq-07"></a>AQ-07 | **Replay is a source adapter and is always labelled as replay** ([SD-10](../requirements/products/arcscope.md#rule-sd-10) there). A replay adapter must not present device-only fields as if measured. |
| <a id="rule-aq-08"></a>AQ-08 | **A device disconnect leaves the session open with an explicit gap** (`§4` there); it never truncates or invalidates the capture. |
| <a id="rule-aq-09"></a>AQ-09 | **A crash mid-capture recovers to the last committed boundary with an honest end marker.** Trailing partial data is either verifiable or discarded with the loss recorded. |
| <a id="rule-aq-10"></a>AQ-10 | **Decoders are data interpreters, never device control** ([DE-06](../requirements/products/arcscope.md#rule-de-06) there). A decoder must not be able to write to the device. |
| <a id="rule-aq-11"></a>AQ-11 | **Device control is a separate, higher-permission capability class** ([DC-02](../requirements/products/arcscope.md#rule-dc-02) there): R3 or above, explicit approval, and typically local presence. It is never reachable through the acquisition path. |

---

**Measurement owner.** ArcScope managed Analysis/Application code implements [scope.measurement.v1](../requirements/products/arcscope.md#measurement-profile), including population statistics, sample weighting, gaps, thresholds, interpolation, units and status/tolerance. Native primitives may accelerate computation only if the same reference vectors pass. Replay, interactive readout, offline ProductJobs and reports consume the same immutable request/result projection. Neither display decimation nor a native library's default statistics defines product semantics.

## 8. Testing the native boundary

| # | Test obligation |
|---|---|
| <a id="rule-nt-01"></a>NT-01 | **ABI conformance tests** assert prefix, version negotiation, struct size and version handling, and rejection of a mismatched library. |
| <a id="rule-nt-02"></a>NT-02 | **Ownership tests** assert the documented allocate and free contract for every function that transfers memory. |
| <a id="rule-nt-03"></a>NT-03 | **Handle lifetime tests** assert no leak and no use-after-free under normal, cancelled and failure paths. |
| <a id="rule-nt-04"></a>NT-04 | **Sanitiser builds** run the native test suite under address and undefined-behaviour sanitisers in CI. |
| <a id="rule-nt-05"></a>NT-05 | **Fuzzing** runs against every parser reachable from untrusted content, with a retained corpus. |
| <a id="rule-nt-06"></a>NT-06 | **Sacrificial-process integration tests** cover crash and hang behaviour, asserting that the managed side reports a typed failure. |
| <a id="rule-nt-07"></a>NT-07 | **Degradation tests** assert that a missing entry point, an ABI mismatch and a device loss each produce a named, visible, recoverable state. |
| <a id="rule-nt-08"></a>NT-08 | **Soak tests** assert stable memory, stable handle counts and no pool exhaustion over the duration defined in the quality contract (`§8` there). |
| <a id="rule-nt-09"></a>NT-09 | **Golden-output tests** assert that decode and render of a fixed input is stable across releases within a declared tolerance, so a codec update cannot silently change output. |
| <a id="rule-nt-11"></a>NT-11 | **AOT tests** assert that every P/Invoke path is source-generated and that no reflection-based marshalling is required. |
| <a id="rule-nt-12"></a>NT-12 | **Licence and provenance tests** assert that every shipped native asset is signed, recorded and licence-reviewed ([LD-05](#rule-ld-05)–[LD-07](#rule-ld-07)). |

---

## 9. Non-goals

The native layer is **not**: a worker process; a place for business logic that is easier to write in C++; a shared cross-product runtime; a plug-in host for third-party native code; a transport for domain data; a holder of ArcForges identity, task or state; or a reason to weaken the Native AOT posture of the desktop product.

---

## 10. Traceability

| Current document | Relationship |
|---|---|
| [ArcScope — Product Requirements](../requirements/products/arcscope.md) | Owns acquisition, evidence, device-control and replay semantics |
| [Local RPC Operations](contracts/02-local-rpc-operations.md) | Defines ResourceRef-based controlled access across the local boundary |
| `§8`, `§8.1` of the scope requirements | The prohibition on C++ workers and the closed technical exception list |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Native AOT constraints on marshalling and binding |
| **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** | Ownership of the deferred decision required before any isolated host is introduced |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[F-013](../assurance/open-gates-register.md#rule-f-013)** | Native dependency licence review against each product's licence boundary |

## [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) capability package adoption

The [package registry](01-solution-and-project-layout.md#12-package-and-native-distribution-registry) fixes wrapper/RID package identities, exact source inputs, producer/consumer tests and the MDF disposition. MDF stays excluded from V1 distributions. All existing ABI/lifetime/buffer/error/time/sandbox rules remain requirements on those packages, not alternatives that a consumer must design. Ordinary product builds are C# package consumers and do not invoke vcpkg.

## Functional producer closure

[The initial functional ABI](contracts/06-native-functional-abi.md) is the initial producer surface (its still-image `arc_image_*` family is post-V1 and out of scope under [P2-026](../decisions/phase-2-specification-decisions.md#rule-p2-026) S1 and S8), including native library calls, states, ownership, wrappers, packages and sandbox bulk buffers. Published probe DLLs are not implementation of these functions. WP13 produces verified capability packages before product consumers; product domain decisions stay in C#. Under [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) the production still-image composition was NAT.31 and the PDF engine retirement record is NAT.32; both are out of scope under [P2-026](../decisions/phase-2-specification-decisions.md#rule-p2-026) (S8 and item 13(g)).
