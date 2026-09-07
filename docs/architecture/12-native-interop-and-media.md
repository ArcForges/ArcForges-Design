# Native Interoperability and Media Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Native AOT desktop), **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** (deferred-decision ownership), the technology constitution and closed exception list (`§8` of [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md))
> Companions: [`04-desktop-application-architecture.md`](04-desktop-application-architecture.md), [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md), [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md), [`../requirements/products/arcscope.md`](../requirements/products/arcscope.md)

Native code exists in ArcForges for one reason: some low-level capability has no reasonable managed substitute. It never exists because native code is faster in general, because the team is more familiar with it, or because an implementation already exists elsewhere. This document defines the boundary that keeps that concession small, auditable and reversible, and the media and acquisition pipelines that sit on top of it.

---

## 1. The controlling position

| # | Rule |
|---|---|
| NI-01 | No C++ business worker is permitted. Native libraries execute in the product or its explicitly approved C# Native AOT content helper according to [isolation architecture](24-content-and-extension-isolation.md). The helper holds no product logic or persistent authority. |
| NI-02 | **Only low-level libraries with no reasonable substitute are native**: codecs, GPU access, device SDKs, system APIs and high-performance primitives. |
| <a id="rule-ni-03"></a>NI-03 | **A native library must never own ArcForges domain**. A native decoder is permitted; a native project manager, task scheduler, state owner or business-rule engine is not — *even where native performance would be higher*. |
| NI-04 | **Product area, business rules, Task, state ownership, scheduling, persistence, policy and UI are C#**. |
| NI-05 | **Where a dependency offers only a C++ API, a very thin `extern "C"` ABI shim is provided under `native/`**. That shim is a *library adaptation*, holds no product business state, and is not a route back to a worker. |
| <a id="rule-ni-06"></a>NI-06 | **A native resource belongs to exactly one product process**. An ArcSlate GPU texture and an ArcScope device handle must never enter an ArcChat domain object, a Cloud DTO, or a `ResourceRef` as a raw pointer. |
| NI-07 | **Only stable resource identity, metadata and controlled access cross a process boundary**. |
| NI-08 | **The native surface is deliberately small.** Growth in the native ABI is a reviewed architectural change, not an implementation detail. |
| NI-09 | **Untrusted third-party native plug-ins never load into a stable main process**. |
| <a id="rule-ni-10"></a>NI-10 | [P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007) exercises [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016) for the C# content-isolation helper and OS-enforced extension profiles. Other isolated hosts still require their own decision. The approved helper does not become a model loop, service, scheduler or C++ domain host. |

### 1.1 What this costs, stated plainly

A native memory error kills the process that loaded the library. Hostile parsing therefore runs in the C# content helper, where failure can be contained. In-process GPU/device calls retain a stated native crash/recovery risk. ABI validation and fuzzing reduce defects but do not create memory isolation.

---

## 2. Where native code is permitted

| Product | Permitted native surface | Explicitly not permitted |
|---|---|---|
| ArcSlate | Demux, decode, encode, colour conversion, scaling, resampling, GPU device and surface access, high-performance pixel and audio primitives | Project model, timeline model, edit decisions, render orchestration, export policy, cache policy |
| ArcScope | Device and transport SDKs, high-rate acquisition primitives, hardware timestamps, high-performance signal primitives | Session model, capture lifecycle, trigger semantics, analysis definitions, evidence storage |
| ArcNotes | Platform system APIs where required — shell integration, secure storage; **document rendering and text extraction for attachment viewing** (`§2.1`) | Anything in the note, block, link or search model; any editing, layout or content path |
| ArcChat | Platform system APIs where required — global hotkey, notification, secure storage | Anything in the conversation, task or capability model |
| Cloud | **None.** Cloud is managed code on a managed hosting platform (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | All native dependencies |
| Mobile and Web | Platform framework only; no first-party native ABI | A first-party C ABI shim |

| # | Rule |
|---|---|
| <a id="rule-np-01"></a>NP-01 | **A native dependency is introduced per product, with a named owner and a stated substitute analysis** — which managed option was evaluated, and why it was insufficient. |
| <a id="rule-np-02"></a>NP-02 | **A native library used by two products is still loaded per process**, with no shared global state between them. |
| NP-03 | **No global shared memory pool exists across products**. |

### 2.1 ArcNotes document rendering — the one amendment, and why

[AT-05](../requirements/products/arcnotes.md#rule-at-05) of the ArcNotes requirements makes PDF **a first-class attachment with in-product viewing, page-anchored annotation targets and citation anchors**. That is an in-product viewer, not a thumbnail, and no managed-only path in the current stack delivers it. The permitted surface is therefore extended — narrowly.

| # | Rule |
|---|---|
| <a id="rule-dr-01"></a>DR-01 | **The extension covers exactly two operations**: rasterising a page to a bitmap at a requested scale, and extracting text with per-glyph or per-range geometry. Nothing else. |
| <a id="rule-dr-02"></a>DR-02 | **No content, editing, layout, link or search path may call it.** The note, block, link and search models stay fully managed (`§2`), and a repository policy test asserts that only the viewer infrastructure project references the wrapper. |
| <a id="rule-dr-03"></a>DR-03 | **[NP-01](#rule-np-01) is not waived by this amendment.** The named owner, the substitute analysis, the licence position and the provenance record are prerequisites to adoption, not follow-ups (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**). |
| DR-04 | PDF parsing/rasterisation/text geometry run inside the C# ContentSandbox under the [mandatory OS profile](24-content-and-extension-isolation.md). The viewer brokers input and validates bounded results. C ABI discipline, signed loading and lifetime checks remain required; child crash/hang produces a metadata card without taking down the parent. |
| DR-05 | **Until adopted, [AT-05](../requirements/products/arcnotes.md#rule-at-05) is not met.** The gap is carried as [PG-12](../assurance/open-gates-register.md#rule-pg-12) in the [open-gates register](../assurance/open-gates-register.md), never absorbed by relabelling the viewer a preview. |
| DR-06 | **The same surface serves any later document-rendering need** — it is not re-opened per format. A format needing more than [DR-01](#rule-dr-01)'s two operations is a new decision. |

---

## 3. Managed-to-native calling discipline

### 3.1 Binding

| # | Rule |
|---|---|
| PI-01 | **`[LibraryImport]` source-generated P/Invoke is the default**, required for Native AOT correctness and for compile-time marshalling diagnostics. |
| PI-02 | **`[DllImport]` is used only where generated marshalling cannot cover the case**, and only with the specific usage verified and recorded. |
| <a id="rule-pi-03"></a>PI-03 | **All P/Invoke declarations for one native library live in one `internal static partial class`** in the infrastructure project that owns it. They are never scattered across feature code. |
| <a id="rule-pi-04"></a>PI-04 | **No feature code calls a P/Invoke declaration directly.** A managed wrapper type owns every call, so validation, handle lifetime and error translation exist in exactly one place. |
| PI-05 | **Strings marshal as UTF-8** with `StringMarshalling.Utf8`, and allocation and free responsibility is stated at every function that returns a string. |
| PI-06 | **Blittable structs only across the boundary.** No managed object graph, no reference type, no `bool` of unspecified width, no `char`. |
| PI-07 | **Callbacks use function pointers with an explicitly stated lifetime**; delegate and function-pointer lifetimes are pinned for as long as native code can call them. |

### 3.2 The C ABI contract

Every first-party native library, and every `extern "C"` shim over a third-party C++ library, obeys the following. These are the terms the managed side is entitled to rely on.

| # | Rule |
|---|---|
| <a id="rule-ab-01"></a>AB-01 | **The C calling convention is explicit and stable across compilers**. |
| <a id="rule-ab-02"></a>AB-02 | **Every exported function carries a fixed prefix and an ABI version** — for example `af_media_*`. |
| AB-03 | **Every struct carries a size and version field, and fields are only appended at the end.** Reordering, resizing or repurposing an existing field is a breaking ABI change. |
| AB-04 | **Fixed-width integer types only.** |
| AB-05 | **C++ `bool`, STL types, exceptions, RTTI and vtables never cross the boundary**. |
| AB-06 | **Handles are opaque pointers**; the managed side always represents them as a `SafeHandle`. |
| AB-07 | **Resource ownership is stated explicitly in every function's contract and asserted by a test**: who allocates, who frees, and when. |
| <a id="rule-ab-08"></a>AB-08 | **A native exception never crosses the C ABI.** A status or error object is returned instead. |
| AB-09 | **Callbacks have a defined registration, deregistration, threading, reentrancy and shutdown protocol**. A callback that can fire after deregistration is a defect. |
| AB-10 | **Functions are as coarse-grained as practical.** A P/Invoke per pixel or per audio sample is prohibited; work is submitted in buffers, plans or batches. |
| AB-11 | **Every length is checked for overflow and against its upper bound in managed code before the call**. |
| <a id="rule-ab-12"></a>AB-12 | **The ABI version is negotiated at load, not assumed.** A mismatch is a startup failure with an actionable message, never a crash later. |

### 3.3 Loading

| # | Rule |
|---|---|
| <a id="rule-ld-01"></a>LD-01 | **`NativeLibrary.SetDllImportResolver` maps logical library names to RID-specific assets published and signed with the application**. |
| <a id="rule-ld-02"></a>LD-02 | **Prohibited**: loading from the current working directory; loading an unsigned library from a user-writable search path; modifying the global search path to resolve dependencies; allowing a same-named system library to be picked up by accident. |
| <a id="rule-ld-03"></a>LD-03 | **Startup verification confirms** ABI version, build identifier and hash, required entry points, CPU and GPU feature availability, and minimum driver or system capability. |
| <a id="rule-ld-04"></a>LD-04 | **A failed verification degrades a feature explicitly**, with a named reason surfaced to the user and recorded in diagnostics. It never silently disables a capability, and never proceeds with a partially verified library. |
| <a id="rule-ld-05"></a>LD-05 | **Native assets are part of the signed package**, covered by the same signing and provenance requirements as managed assemblies. |
| LD-06 | **Native asset versions, hashes and source provenance are recorded in the release record** ([`14-build-packaging-and-release.md`](14-build-packaging-and-release.md)). |
| <a id="rule-ld-07"></a>LD-07 | **Native library licences are recorded and reviewed against the licence boundary of the consuming product** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, the **[F-013](../assurance/open-gates-register.md#rule-f-013)** gate). A native dependency incompatible with a product's licence is not shipped in that product. |

### 3.4 Handles and lifetime

| # | Rule |
|---|---|
| HL-01 | **Every native handle kind has a dedicated `SafeHandle` subclass**. A raw pointer is never held in a field. |
| HL-02 | **A reference-counted guard wraps every call that passes a handle**, so a handle cannot be freed while native code is using it. |
| HL-03 | **Asynchronous wrappers implement `IAsyncDisposable`**. |
| HL-04 | **Finalizers are a last-resort safety net**, never the normal release path. |
| HL-05 | **The native runtime shuts down only after UI and RPC have stopped accepting new work**, so no call is in flight while teardown runs. |
| HL-06 | **Handle leaks are detectable.** Debug and test builds assert that every created handle is disposed at scope exit, and handle counts are asserted in soak tests. |

---

## 4. Buffers and the large-data path

| # | Rule |
|---|---|
| BF-01 | **CPU buffers use `Span<T>`, `Memory<T>`, a memory pool and controlled pinned memory**. |
| BF-02 | **Pinning is scoped and short.** A long-lived pinned region is a documented exception with a stated reason. |
| BF-03 | **Pooled buffers are returned on every path including failure**, and pool exhaustion is a measured, surfaced condition rather than an unbounded allocation. |
| BF-04 | **A per-frame image is never serialised over StreamJsonRpc, the HTTP client or the realtime channel**. |
| <a id="rule-bf-05"></a>BF-05 | **The Hub never relays video frames or large file bodies**. |
| <a id="rule-bf-06"></a>BF-06 | **GPU resources are shared inside the process through a platform-specific rendering bridge; the UI receives only presentable surface or bitmap abstractions**. |
| BF-07 | **Cross-process large data uses `ResourceRef` plus a controlled stream, file-handle strategy or temporary resource channel**, never an inline payload. |
| <a id="rule-bf-08"></a>BF-08 | **`ResourceRef` never carries a raw pointer, GPU handle or device handle** ([NI-06](#rule-ni-06)). It carries identity and metadata only ([RR-01](02-contracts-and-protocols.md#rule-rr-01)–[RR-14](02-contracts-and-protocols.md#rule-rr-14) in the contract architecture). |
| BF-09 | **Backpressure is explicit.** A producer that outruns its consumer blocks, drops with a recorded reason, or fails; it never grows without bound. |

---

## 5. Threading across the boundary

| # | Rule |
|---|---|
| TH-01 | **Native work never runs on the UI thread.** Decode, encode, acquisition, analysis and GPU submission run on dedicated or pooled non-UI threads (`§4` of the desktop architecture). |
| TH-02 | **A native callback thread is not a managed synchronisation context.** Callback bodies do the minimum work and hand off to a managed queue. |
| TH-03 | **No managed lock is held across a native call that can block, and no native lock is held across a managed callback.** |
| TH-04 | **Cancellation is cooperative and defined per operation.** A native operation that cannot be cancelled is bounded in duration and documented as such. |
| TH-05 | **Thread affinity requirements of a device or GPU context are honoured explicitly**, with a dedicated owning thread where the underlying API demands one. |
| TH-06 | **Re-entrancy is prohibited by construction**: a callback never calls back into the same native object under the same lock. |

---

## 6. Failure and safety boundaries

These mitigations supplement the mandatory hostile-content process boundary. They do not substitute for OS isolation or make an access violation catchable in the parent.

| # | Obligation |
|---|---|
| SB-01 | **The native ABI is kept extremely small.** Every addition is reviewed. |
| SB-02 | **Input is validated in managed code before it reaches native code** — sizes, ranges, formats, counts, alignment. |
| SB-03 | **Native libraries are built with sanitiser configurations** — address and undefined behaviour — for test builds. |
| <a id="rule-sb-04"></a>SB-04 | **Media and image parsers are fuzzed**, with a corpus retained and extended by every parser defect found. |
| SB-05 | **Native integration tests run in a sacrificial process**, so a crash fails a test rather than the test host. |
| <a id="rule-sb-06"></a>SB-06 | **Crash dumps, symbols and build identifiers are retained in production**, and are sufficient to resolve a native frame. |
| SB-07 | **Business recovery relies on the journal** (`§3` of the persistence architecture). A native crash loses at most work since the last committed boundary, never committed work. |
| SB-08 | **A repeated native crash on the same input is a quarantine condition.** The offending asset, device or code path is marked, the user is told, and the application starts in a degraded but usable state (safe start, `§5` of the desktop architecture). |
| SB-09 | **Untrusted content is treated as hostile input at the native boundary.** A media file, capture stream or imported asset from outside the user's trust domain is parsed with the same suspicion as network input (`§7` of the security architecture). |
| SB-10 | **A native defect that cannot be mitigated within these obligations is grounds for removing the dependency**, not for relaxing the obligations. |

---

## 7. The ArcSlate media pipeline

### 7.1 Structure

```
MediaAsset — identity, metadata, availability            C# domain, authority
      ↓ resolve representation
original | managed copy | proxy                          C# decision
      ↓
Demux → Decode → colour convert · scale · resample       native, behind the ABI
      ↓ frames and audio buffers in pooled memory
Processing graph evaluation                              C# orchestration,
                                                         native primitives per node
      ↓
Preview → presentable surface → UI     |     Render → Encode → Mux → output
```

| # | Rule |
|---|---|
| <a id="rule-mp-01"></a>MP-01 | **The domain model is C# and owns every decision** ([NI-03](#rule-ni-03)). The native foundation answers "decode this range of this stream at this quality"; it never decides what to decode, when, or why. |
| MP-02 | **A native media foundation must never leak into the domain** ([RT-02](../requirements/products/arcslate.md#rule-rt-02) in the ArcSlate requirements). No native type, handle, enumeration or error code appears in a domain, contract or persisted type. |
| <a id="rule-mp-03"></a>MP-03 | **Preview and final render share processing semantics** ([PP-03](../requirements/products/arcslate.md#rule-pp-03), [RT-06](../requirements/products/arcslate.md#rule-rt-06) there). Effect and colour semantics are identical; only quality, speed and precision differ. This is enforced by one shared evaluation description, never by two independently written pipelines. |
| <a id="rule-mp-04"></a>MP-04 | **Preview may drop displayed frames; it must keep the audio and timeline clock correct** ([VW-04](../requirements/products/arcslate.md#rule-vw-04) there). |
| MP-05 | **A dropped preview frame is a playback-quality event, never data loss** ([I-480](../requirements/01-normative-glossary-and-invariants.md#rule-i-480)), reported through playback quality state rather than as an error. |
| <a id="rule-mp-06"></a>MP-06 | **Switching proxy on or off never changes render output** ([I-484](../requirements/01-normative-glossary-and-invariants.md#rule-i-484), [PX-02](../requirements/products/arcslate.md#rule-px-02) there). Final render uses the original unless proxy render is explicitly permitted. |
| MP-07 | **Proxies, render caches, thumbnails and waveforms are derived** ([PX-05](../requirements/products/arcslate.md#rule-px-05)–[PX-08](../requirements/products/arcslate.md#rule-px-08) there): fully reconstructable, never project authority, and safe to delete. |
| <a id="rule-mp-08"></a>MP-08 | **Decode capability is discovered at runtime and reported as capability**, never assumed from a build flag. Missing hardware acceleration degrades to software with a visible reason. |
| MP-09 | **A render task binds a project and sequence revision snapshot** ([RN-04](../requirements/products/arcslate.md#rule-rn-04) there). The native pipeline is handed an immutable plan; it never reads live editor state. |
| MP-10 | **Export writes to a temporary target and commits atomically**, so a cancelled or failed render never leaves a file that looks complete. |
| MP-11 | **Timebase conversion is exact.** Rational frame rates and audio sample rates are converted through explicit exact arithmetic at the managed boundary ([TM-02](../requirements/products/arcslate.md#rule-tm-02), [TM-03](../requirements/products/arcslate.md#rule-tm-03) there); native code receives already-resolved frame and sample indices. |
| <a id="rule-mp-12"></a>MP-12 | **Offline media is a normal state** ([MD-05](../requirements/products/arcslate.md#rule-md-05) there). The pipeline reports unavailability; it does not fail the project. |

### 7.2 GPU

| # | Rule |
|---|---|
| GP-01 | **GPU state stays inside the owning process**. |
| GP-02 | **The device, its context and its resources have a single owning component**, with an explicit creation, loss and recreation protocol. |
| GP-03 | **Device loss is recoverable**: resources are recreated, in-flight work fails with a typed reason, and the session continues. |
| <a id="rule-gp-04"></a>GP-04 | **GPU acceleration is optional at every stage.** A software path exists for every operation required for correctness, so a driver problem degrades performance rather than removing a feature. |
| GP-05 | **The UI receives presentable surfaces or bitmaps only**, never a GPU handle. |

---

## 8. The ArcScope acquisition pipeline

### 8.1 Structure

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
| AQ-01 | **The acquisition loop, capture lifecycle and trigger semantics are C#** ([NI-03](#rule-ni-03)). Native code supplies transport, device access, timestamps and high-rate primitives only. |
| AQ-02 | **Live observation and capture are separate paths** ([SE-04](../requirements/products/arcscope.md#rule-se-04) in the ArcScope requirements). Pausing the view never stops recording ([SE-05](../requirements/products/arcscope.md#rule-se-05)). |
| AQ-03 | **Raw capture is written to the chunked verifiable store** ([SE-14](../requirements/products/arcscope.md#rule-se-14) there), never buffered through a component that can lose it silently. |
| AQ-04 | **An acquisition overrun is surfaced, never hidden.** Dropped samples are counted, timestamped and recorded as a gap in the capture. |
| AQ-05 | **Hardware timestamps are preserved where available**, with the timing source recorded in the effective configuration snapshot ([SD-05](../requirements/products/arcscope.md#rule-sd-05) there). Where no hardware timestamp exists, the host timing source and its uncertainty are recorded. |
| AQ-06 | **A device handle never leaves the owning process** ([NI-06](#rule-ni-06)). Exclusive access is coordinated with lease and busy semantics ([SD-08](../requirements/products/arcscope.md#rule-sd-08) there). |
| AQ-07 | **Replay is a source adapter and is always labelled as replay** ([SD-10](../requirements/products/arcscope.md#rule-sd-10) there). A replay adapter must not present device-only fields as if measured. |
| <a id="rule-aq-08"></a>AQ-08 | **A device disconnect leaves the session open with an explicit gap** (`§4` there); it never truncates or invalidates the capture. |
| <a id="rule-aq-09"></a>AQ-09 | **A crash mid-capture recovers to the last committed boundary with an honest end marker.** Trailing partial data is either verifiable or discarded with the loss recorded. |
| AQ-10 | **Decoders are data interpreters, never device control** ([DE-06](../requirements/products/arcscope.md#rule-de-06) there). A decoder must not be able to write to the device. |
| AQ-11 | **Device control is a separate, higher-permission capability class** ([DC-02](../requirements/products/arcscope.md#rule-dc-02) there): R3 or above, explicit approval, and typically local presence. It is never reachable through the acquisition path. |

---

## 9. Testing the native boundary

| # | Test obligation |
|---|---|
| <a id="rule-nt-01"></a>NT-01 | **ABI conformance tests** assert prefix, version negotiation, struct size and version handling, and rejection of a mismatched library. |
| NT-02 | **Ownership tests** assert the documented allocate and free contract for every function that transfers memory. |
| NT-03 | **Handle lifetime tests** assert no leak and no use-after-free under normal, cancelled and failure paths. |
| NT-04 | **Sanitiser builds** run the native test suite under address and undefined-behaviour sanitisers in CI. |
| <a id="rule-nt-05"></a>NT-05 | **Fuzzing** runs against every parser reachable from untrusted content, with a retained corpus. |
| NT-06 | **Sacrificial-process integration tests** cover crash and hang behaviour, asserting that the managed side reports a typed failure. |
| NT-07 | **Degradation tests** assert that a missing hardware accelerator, a missing entry point, an ABI mismatch and a device loss each produce a named, visible, recoverable state. |
| NT-08 | **Soak tests** assert stable memory, stable handle counts and no pool exhaustion over the duration defined in the quality contract (`§8` there). |
| NT-09 | **Golden-output tests** assert that decode and render of a fixed input is stable across releases within a declared tolerance, so a codec update cannot silently change output. |
| NT-10 | **Proxy-equivalence tests** assert [MP-06](#rule-mp-06): render output is identical whether or not proxies are enabled. |
| NT-11 | **AOT tests** assert that every P/Invoke path is source-generated and that no reflection-based marshalling is required. |
| NT-12 | **Licence and provenance tests** assert that every shipped native asset is signed, recorded and licence-reviewed ([LD-05](#rule-ld-05)–[LD-07](#rule-ld-07)). |

---

## 10. Non-goals

The native layer is **not**: a worker process; a place for business logic that is easier to write in C++; a shared cross-product runtime; a plug-in host for third-party native code; a transport for domain data; a holder of ArcForges identity, task or state; or a reason to weaken the Native AOT posture of the desktop products.

---

## 11. Traceability

| Current document | Relationship |
|---|---|
| [ArcSlate — Product Requirements](../requirements/products/arcslate.md) | Owns media, render, timebase, proxy and recovery semantics |
| [ArcScope — Product Requirements](../requirements/products/arcscope.md) | Owns acquisition, evidence, device-control and replay semantics |
| [Local RPC Operations](contracts/02-local-rpc-operations.md) | Defines ResourceRef-based controlled access across the local boundary |
| `§8`, `§8.1` of the scope requirements | The prohibition on C++ workers and the closed technical exception list |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Native AOT constraints on marshalling and binding |
| **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** | Ownership of the deferred decision required before any isolated host is introduced |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[F-013](../assurance/open-gates-register.md#rule-f-013)** | Native dependency licence review against each product's licence boundary |
