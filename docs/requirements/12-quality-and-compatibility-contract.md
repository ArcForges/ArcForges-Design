# Product Quality and Compatibility Contract
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **D-008** (runtime and AOT matrix), **V-03**/**V-04**/**V-05** (AOT evidence)
> Companions: [`09-shared-desktop-experience.md`](09-shared-desktop-experience.md), [`13-data-formats-and-portability.md`](13-data-formats-and-portability.md), [`../assurance/testing-and-verification-strategy.md`](../assurance/testing-and-verification-strategy.md), [`../assurance/release-gates.md`](../assurance/release-gates.md)

> **Quality Requirement ≠ Engineering Suggestion** (`I-402`).

Everything in this document is a **release gate**. A budget that is not enforced by a gate is not a budget; a compatibility claim that is not tested is not a claim.

The mechanism, in five parts: **Budget + Matrix + Fixture + Test + Release Gate.**

---

## 1. The Product Quality Contract

Each of the following carries its own versioned Product Quality Contract: **ArcChat Desktop**, **ArcNotes**, **ArcScope**, **ArcSlate**, **ArcChat Mobile**, **ArcChat Web**, plus the user-perceived quality of cloud interaction.

Every contract contains at minimum:

```
Performance Budget · Memory Budget · Startup Budget · Background Resource Budget
Responsiveness Budget · Scale & Soak Scenarios
Accessibility Contract · Localization Contract · Units/Time/Number Contract
AOT Contract · Supported Platform Matrix · Compatibility Matrix · Migration Matrix
Recovery Contract · Diagnostics Contract · Test Matrix
```

| # | Requirement |
|---|---|
| QC-01 | **The quality contract lives in the repository, under version control**, with a machine-readable representation that CI consumes directly. A wiki page is not a contract. |
| QC-02 | **A quality threshold must never be quietly relaxed in an ordinary change.** Changing a budget requires an explicit **Quality ADR** with evidence and review. |
| QC-03 | Every budget value in this document is an **initial project release budget**, not a marketing promise. If the first real vertical slice proves a budget unreasonable, it is changed through a Quality ADR — and thereafter must not drift without evidence. |

---

## 2. Two-tier thresholds

Every key metric carries **two** limits simultaneously:

| Tier | Meaning | Consequence |
|---|---|---|
| **Absolute budget** | A hard ceiling the product may never exceed, regardless of history | **Unconditional release block** |
| **Regression budget** | Even below the ceiling, it may not keep getting worse | **Blocking review** |

| # | Requirement |
|---|---|
| TH-01 | **A repeatable regression of ~10 % against the last stable baseline on a key P50/P95 metric enters a blocking review.** Memory uses the same ~10 % warning line. |
| TH-02 | **Benchmarks are noisy**, so a regression gate requires repeated sampling and statistical stability — never a single-machine fluctuation. |
| TH-03 | **Exceeding an absolute ceiling blocks unconditionally**, with no statistical argument available. |
| TH-04 | *Worked example:* ceiling 2.0 s, previous release 1.30 s, new build 1.72 s. Under the ceiling, but +32 % — this blocks for review. "It's still under two seconds" is not an acceptable justification. |

---

## 3. Reference hardware

A performance contract must never mean "it's fast on my machine".

**Desktop V1 Reference Hardware Class** — a class, not a specific CPU model:

- A supported 64-bit architecture
- 8 or more logical CPU cores
- 16 GB RAM
- NVMe-class SSD
- A supported GPU where the product requires one
- Release build, **no debugger attached**, **production AOT artifact**

A **Lower-bound Supported Hardware Class** is maintained in parallel, to answer whether the product is unusable on an ordinary machine.

| # | Requirement |
|---|---|
| RH-01 | **Benchmarks run against real publish artifacts**: the production Native AOT desktop package, the release Android AOT package, the production WebAssembly build. A Debug or JIT measurement is not a benchmark result (`I-380`, `I-381`). |

---

## 4. Responsiveness

| # | Requirement |
|---|---|
| RS-01 | Input to visible acknowledgement is fast enough that the user knows the operation was accepted, immediately. |
| RS-02 | **Animation must not be used to conceal real slowness** (`I-392`). A spinner over a slow operation is not responsiveness. |
| RS-03 | **A synchronous block of more than ~50 ms on the UI thread is a serious defect**, and a sustained one is release-blocking. |
| RS-04 | **Responsive animation ≠ responsive product** (`I-392`). A smooth frame rate during an unusable wait is not a pass. |
| RS-05 | Long work returns an owner-qualified handle and reports progress without blocking: TaskHandle for Cloud agent tasks, ProductJobHandle for ordinary product work. The UI does not imply identical schedulers. |

---

## 5. Startup

Three distinct moments, never collapsed into "startup time":

```
Process Start → First Window Visible → First Usable Workspace
```

The product metric is **Time To Usable** (`I-389`).

**Desktop V1 startup budget** — reference hardware, release Native AOT, normal local state, cold process to usable workspace, P95:

| Product | Budget |
|---|---|
| ArcChat | ≤ 2.0 s |
| ArcNotes | ≤ 2.0 s |
| ArcScope | ≤ 2.5 s |
| ArcSlate | ≤ 3.0 s |

| # | Requirement |
|---|---|
| SU-01 | ArcScope and ArcSlate may continue device scanning, media indexing and derived-cache loading in the background — **but must never block first workspace availability on them**. |
| SU-02 | Native startup opens the shell and authorized cached work without waiting on Cloud. First-run or missing-content views state sign-in/network requirements honestly; Cloud refresh is asynchronous and does not promise account-free local AI or a standalone notebook. |
| SU-03 | **Startup must not require ArcChat to be online.** ArcNotes, ArcScope and ArcSlate open their core workspace first; the Hub connection is background recovery. |

---

## 6. Memory

**Quiescent base memory ceiling** — release AOT, main workspace open, no large project loaded, 60 s quiescent, derived startup work finished:

| Product | Ceiling |
|---|---|
| ArcChat + local Hub | ≤ 250 MiB |
| ArcNotes | ≤ 250 MiB |
| ArcScope | ≤ 320 MiB |
| ArcSlate | ≤ 450 MiB |

| # | Requirement |
|---|---|
| MM-01 | **Managed heap ≠ total memory** (`I-390`). The budget counts managed heap, native heap, pinned buffers, media buffers, RPC buffers, image buffers and index working memory. GPU memory is measured separately and is never ignored merely because it is not on the managed heap. |
| MM-02 | **"Cache doesn't count as memory" is not a valid exemption.** |
| MM-03 | **Memory pressure must be surrenderable.** Every cache — thumbnails, render cache, frame cache, waveforms, proxy working data, decoded data, analysis cache, visualisation buffers — has a budget and an eviction policy. |
| MM-04 | Under OS memory pressure, **derived and rebuildable memory is released first**. An application must never be killed by the OS while protecting a cache. |

---

## 7. Leaks and soak

| # | Requirement |
|---|---|
| SK-01 | Every product has a **long-running soak test** as a release gate. |
| SK-02 | **No monotonic growth is permitted** in handles, native resources, threads, subscriptions, timers or event registrations. |
| SK-03 | Product soaks cover Cloud agent cycles with native task projections; native note editing with pending sync/index work; at least 8 hours of hardware capture/visualization; the 24-hour Cloud simulator soak in SIM-20; and native timeline/playback/export with cache churn. |
| SK-04 | **Small benchmark ≠ scale reliability** (`I-388`). Soak and scale results, not micro-benchmarks, decide the gate. |

---

## 8. Background resource contract

> ArcForges is not a permanent CPU-burning tool.

| Condition | Budget |
|---|---|
| Idle, application in background, no active work | ≤ ~0.5 % of one logical core, averaged |
| Fully quiescent (nothing pending at all) | Target ≤ ~0.2 % of one logical core, averaged |

| # | Requirement |
|---|---|
| BG-01 | **Busy polling is prohibited.** Waiting is event-driven, with bounded backoff. |
| BG-02 | Background traffic is bounded. Prefer notifications/outbox dispatch; when realtime is unavailable, authorized HTTP polling with backoff, jitter, idle limits and reconnect backfill is supported. Busy polling and unbounded retries are prohibited. |
| BG-03 | **Background work must not starve foreground work.** Task resource competition has explicit priority: a timeline drag must not stutter, a capture must not lose data, and typing must not lag because of background indexing, sync or rendering. |

---

## 9. Scale corpus

| # | Requirement |
|---|---|
| SC-01 | Each product declares a **Scale Corpus** — the size each release must support and remain stable at. Anything at or below that scale must behave correctly. |
| SC-02 | **Performance budgets are expressed in terms of user work**, not only function-level micro-benchmarks: open a large document, scrub a long timeline, run an 8-hour capture, search a large corpus. |
| SC-03 | **Search quality and search performance are separate contracts** (`QA-01`, `QA-04` in the knowledge requirements). A fast search that returns the wrong result is a failure of a different contract. |

---

## 10. Accessibility contract

> **All major user workflows reach WCAG 2.2 AA semantic level and correctly connect to the target platform's accessibility APIs.**

| # | Requirement |
|---|---|
| AX-01 | **No core workflow may require a mouse** (`I-394`). Every action has a keyboard-accessible semantic path through the command system. |
| AX-02 | **Focus contract**: focus is always visible; focus order is logical; a dialog traps and restores focus; **Focus ≠ Selection** (`I-404`); after an operation, focus returns to a sensible origin. |
| AX-03 | **Screen reader contract**: every control exposes role, name, value and state; live regions announce state changes; complex professional surfaces expose a meaningful structure rather than a flat control soup. |
| AX-04 | **Every icon-only control has an accessible name**, and an icon is never the sole carrier of information (`DS-07`). |
| AX-05 | **Colour is never the only source of information** (`I-393`). Every state distinguished by colour is also distinguished by shape, text or icon. |
| AX-06 | **High-contrast and reduced-motion system settings are honoured.** |
| AX-07 | **Text scaling to 200 %** keeps every core workflow usable, with no clipped or unreachable controls. |
| AX-08 | **Accessible colour ≠ accessible product** (`I-393`). Contrast conformance alone does not satisfy the contract. |
| AX-09 | **The accessibility test matrix is real**: automated semantic checks on every change; assistive-technology verification on the release train against each Tier-1 platform's own accessibility stack. |
| AX-10 | **An accessibility failure in a core workflow is a release blocker.** |

---

## 11. Localization contract

| # | Requirement |
|---|---|
| LO-01 | **Every user-visible string is localisable from day one**, including in shared components. |
| LO-02 | **Persistent identifiers are never localised.** Enum values, ids, capability identifiers, format keys, file-format tokens and protocol constants are stable invariants; only their display is localised. |
| LO-03 | **String concatenation to build sentences is prohibited.** Localisation resources support parameters and plural semantics. |
| LO-04 | **Pseudo-localisation is a CI test**, catching hard-coded strings, truncation and concatenation before translation exists. |
| LO-05 | **RTL is a foundation concern, not a future rewrite.** The foundation must not make RTL impossible, even where an RTL locale does not ship in V1. |
| LO-06 | **User data never changes because the interface language changed** (`I-395`). The same document, the same measurement, the same project produce identical stored bytes in every locale. |
| LO-07 | **Localized UI ≠ locale-safe data** (`I-395`). Storage is canonical and invariant; presentation is localised. |
| LO-08 | Dates, numbers and currency display in the user's locale and store in an invariant representation. |
| LO-09 | **Parsing semantics do not change with locale** for stored or interchange content. A file written under one locale parses identically under another. |

### 11.1 Time

| # | Requirement |
|---|---|
| TZ-01 | An instant is stored as a UTC-equivalent stable representation. |
| TZ-02 | Where the **original zone carries meaning** — a scheduled automation, a capture timestamp, a user-authored deadline — the original zone semantics are stored alongside, not discarded. |
| TZ-03 | Scheduling carries a time zone and an explicit DST resolution policy (`TG-01`, `TG-02`). |

### 11.2 Units

> **Quantity = Value + Dimension + Unit semantics** (`I-396`).

| # | Requirement |
|---|---|
| UN-01 | **Canonical unit and display unit are separate.** Changing a display unit never changes the recorded measurement fact. |
| UN-02 | **ArcScope retains the source unit** as acquisition provenance. A converted display value never overwrites what the instrument reported. |
| UN-03 | **Engineering prefixes are handled by a unified formatter.** Products must not write their own prefix string formatting. |
| UN-04 | **Unit conversion is dimension-safe.** Converting across incompatible dimensions is a compile-time or validation error, never a silent numeric operation. |
| UN-05 | **ArcSlate time is not forced into the general unit system.** It uses a rational time and time-base model, because frame-accurate editing requires exact rational arithmetic rather than floating-point seconds (`I-478`). |

---

## 12. AOT contract

> **AOT compatibility is not a compilation option; it is part of the compatibility contract.**

| # | Requirement |
|---|---|
| AO-01 | **Every official release runs the real publish matrix**, producing genuine artifacts. A failure to publish is a failed release, not a warning. |
| AO-02 | **`IL2026` / `IL3050` and equivalent trimming/AOT warnings are release-blocking by default** on any project consumed by an AOT deliverable. |
| AO-03 | **Suppression is permitted but audited**: each suppression is narrow, justified, attributed, and carries a revalidation trigger. A blanket global suppression is prohibited. |
| AO-04 | **AOT tests use the final published artifact**, not a Debug or JIT build (`I-381`). |
| AO-05 | **Per D-008, AOT gates apply only to projects actually consumed by an AOT deliverable.** Cloud is a JIT modular monolith and carries no strict AOT requirement. Shared public contracts and client libraries consumed by desktop or mobile remain trim-safe and source-generation friendly. |
| AO-06 | **A third-party extension does not change this contract.** The host stays a Native AOT deliverable; an extension runs out of process with its own runtime and does not affect the host's AOT metrics (`EX-04` in the extension requirements). |
| AO-07 | **Android production is .NET 10 Mono AOT** (**D-008**, **V-04**). `UseMonoRuntime` is explicit in the project file rather than relying on a default that changes in a later framework version. Documentation must never conflate Mono AOT with CoreCLR Native AOT. |
| AO-08 | **Web uses Blazor WebAssembly with `RunAOTCompilation=false`** (**D-007**) unless a measured benchmark and an explicit decision justify otherwise. |
| AO-09 | Dependency-specific AOT gates carried from Phase 1 verification are enforced: source-generated StreamJsonRpc proxies with the required contract attributes; Refit generated-only entry points with the reflection package absent and its diagnostic build-breaking; a real publish proof for Avalonia plus every third-party control actually used. |

---

## 13. Native ABI contract

The native boundary is a compatibility contract in its own right: exported ABI version, struct layout and size/version fields, calling convention, string encoding and ownership, handle semantics, error model, callback protocol, and the minimum driver or system capability required.

**Native and managed ship as one version set** (`I-208` analogue). An ABI change is a versioned, tested, migration-aware event.

---

## 14. Version axes

**"Version" alone is never sufficient.** Nine independent axes exist and none may be collapsed into another (`I-383`):

| Axis | Meaning |
|---|---|
| `AppVersion` | The product version the user installed |
| `ContractVersion` / `ContractSet` | LocalRpc, PublicApi and Realtime contracts |
| `CapabilityVersion` | Business capability version |
| `NativeFormatVersion` | Portable project/document format |
| `StorageSchemaVersion` | Internal working store |
| `NativeAbiVersion` | The C/native boundary |
| `PolicySchemaVersion` | Policy bundle schema |
| `ExtensionProtocolVersion` | Extension host protocol |
| `PackageVersion` | Third-party package version |

---

## 15. Compatibility matrix

| # | Requirement |
|---|---|
| CM-01 | **Every release produces a Compatibility Manifest as a release artifact**, answering: which product versions can this interoperate with locally; which contract sets it speaks; which native formats it can read and write; which cloud API versions it can reach; which extension protocol versions it supports; which native ABI it requires. |
| CM-02 | **The four desktop products version independently** (`P-12`), and **mixed-version combinations must actually be tested**. Nominal independent release plus de facto lockstep upgrade is a failed contract. |
| CM-03 | **Minimum first-party local interoperability window: current stable plus the immediately previous supported stable line**, in **both** directions — new ArcChat with previous ArcNotes, and previous ArcChat with new ArcNotes. |
| CM-04 | A contract major upgrade requires an explicit **coexistence migration window** in which V1 and V2 both operate. |
| CM-05 | **"Previous version" is a floor, not a ceiling.** Some contracts may be supported longer; a security-driven sunset may be scheduled earlier through the policy control plane. |
| CM-06 | **Cloud compatibility follows a declared Supported Client Set.** Removing support is planned and communicated through compatibility policy, never discovered by users. |
| CM-07 | **A client newer than Cloud must also be tested.** Rolling upgrade means both orderings occur. |
| CM-08 | **Extension protocol compatibility: current major plus previous major**, except where a security reason forces earlier revocation. |
| CM-09 | **Native format compatibility outlives application interoperability.** Every historical format still in the Supported Native Format set has a golden fixture and a migration test. Formats beyond that set have a maintained conversion or archival migration path. |
| CM-10 | **Read compatibility ≠ write compatibility** (`I-385`). Being able to open an older or newer file does not imply being able to save it without loss. Each is declared and tested separately. |
| CM-11 | There is no "ArcForges 4.0" that implies a synchronized version across products (`SI-01` analogue). |

---

## 16. Migration testing

| # | Requirement |
|---|---|
| MG-01 | **Migration is a first-class test type** with its own **Migration Test Corpus**, not a subset of integration tests. |
| MG-02 | **Every historical format version has a permanent golden fixture** — fixed, immutable test data committed to the repository. |
| MG-03 | **Golden fixtures come from multiple sources**: synthesised, captured from real usage with consent and redaction, and edge cases. **Unredacted real user data never enters the test repository.** |
| MG-04 | **Migration tests verify semantics, not merely "it opens"** (`I-386`). Content, structure, references, revisions, properties, timing and units must all survive. |
| MG-05 | **Round-trip migration is tested** where the format supports it. |
| MG-06 | **Migration failure injection is a required test**: interruption at each stage must leave **no half-upgraded writable store**. |
| MG-07 | **The pre-migration recovery point is tested, not merely implemented** (`SV-04`). Restoring from it must genuinely restore. |
| MG-08 | **Downgrade behaviour is tested.** An older application encountering newer data enters a safe read-only or explicitly-blocked state; it must never silently discard fields it does not understand (`SV-02`). |
| MG-09 | **Application binary rollback ≠ data rollback** (`I-208`). Both are tested, and their separation is explicit in the product. |

---

## 17. Contract testing

Contract tests cover **every** communication boundary: local RPC, public HTTP API, realtime, the native ABI, the extension protocol, and persisted formats.

| # | Requirement |
|---|---|
| CT-01 | **"Both sides reference the same assembly" is not a contract test.** A real contract test exercises a previously published client against the current implementation, and vice versa. |
| CT-02 | **Serialized golden vectors** are committed: exact bytes for representative messages and documents, so an accidental wire or format change fails loudly. |
| CT-03 | **The error contract is tested.** Stable semantic error codes are part of the contract; **the code never changes with localisation** (`LO-02`). |
| CT-04 | **`CommandId` idempotency is a contract test**: the same logical write delivered several times produces exactly one effect. |
| CT-05 | **Realtime disconnection recovery is a contract test**: after a gap, sequence backfill must recover the missed range exactly — a client at sequence 100 that reconnects at 130 must not silently skip 101–129. |
| CT-06 | Contract tests run against **real transports** — real named pipes and domain sockets, a real HTTP server, a real realtime connection — not in-memory doubles alone. |

---

## 18. Crash and recovery contract

**Actively killing the process is a formal testing method.** Every stable release must do it.

| # | Requirement |
|---|---|
| CR-01 | **The core crash contract: anything reported as saved locally must exist after a crash.** Violating it is a **P0 release blocker**. |
| CR-02 | **Derived data may be lost** and must be rebuildable. Losing a cache must never corrupt a project. |
| CR-03 | Fault-injection points include at least: kill immediately after save; kill mid-write; kill mid-migration; kill mid-sync; kill during capture; kill during render; disk full; database busy; corrupted snapshot; corrupted derived cache; native library fault. |
| CR-04 | **ArcScope capture recovery is separately tested**: an interrupted capture must recover to the last durably committed data with an accurate, honest boundary — never silently truncated and presented as complete. |
| CR-05 | **ArcSlate recovery is separately tested**: a project must not be damaged by a proxy or render failure; the timeline and project data survive independently of derived media. |
| CR-06 | **Crash-loop protection** is required: repeated startup failures enter **Safe Start / Recovery Mode**, which is read-first, does not modify canonical content, and **never automatically deletes user data**. |
| CR-07 | **Cache recovery ≠ canonical data recovery** (`I-222`). Rebuilding a cache is not evidence that canonical recovery works. |
| CR-08 | **Crash-free ≠ recoverable** (`I-387`). A release with no crashes but no proven recovery path has not met this contract. |

---

## 19. Diagnostics contract

Three tiers, with different content and different rules:

| Tier | Audience | Content |
|---|---|---|
| **User diagnostics** | The user, in-product | Plain-language state, what happened, what to do — **no stack traces** |
| **Support diagnostic bundle** | Support, on explicit user action | Structured, redacted, contents disclosed before sending |
| **Internal telemetry** | Operations | Consented, minimal, no user content |

| # | Requirement |
|---|---|
| DG-01 | **A diagnostic bundle is never uploaded automatically** (`I-424`). It is exported on explicit user action, its contents are shown, and it is redacted by default. |
| DG-02 | **A diagnostic bundle does not include by default**: document content, note content, chat content, media, raw captures, secrets, or tokens. Including any of these requires an explicit, itemised user choice. |
| DG-03 | **Local paths are redacted or normalised by default**, because a path can identify a person. |
| DG-04 | **Verbose diagnostics are time-bounded** and revert automatically. |
| DG-05 | **Logs have a rotation budget** — size, age and count — and never grow without limit. |
| DG-06 | **Correlation runs through the entire system**: one correlation identity traverses local RPC, HTTP, realtime, tasks and audit, so an incident can be reconstructed. |
| DG-07 | **Crash symbols are tied to build identity**, retained, and resolvable for the supported version window. |
| DG-08 | **Diagnostics must never become a telemetry bypass** (`I-399`). "It's a diagnostic" does not license collecting what telemetry consent forbids. |
| DG-09 | **Diagnostic Log ≠ Audit** (`I-276`). |

---

## 20. Cross-platform test matrix

Three tiers of matrix, running at different cadences:

| Matrix | Cadence | Contents |
|---|---|---|
| **PR matrix** | Every change | Build, unit, application, architecture and contract tests; a fast subset of integration tests; an AOT publish smoke test |
| **Nightly matrix** | Daily | Full integration, multi-process end-to-end, migration corpus, soak subset, accessibility automation, performance benchmarks, full publish matrix |
| **Release matrix** | Release train | Everything above, plus assistive-technology verification, hardware-lab tests, install/upgrade/rollback, mixed-version interoperability, disaster-recovery rehearsal, and the full compatibility matrix |

| # | Requirement |
|---|---|
| PM-01 | **Desktop Tier-1 platforms genuinely enter build, AOT publish, install, UI, recovery, compatibility, performance and release matrices.** A platform that only compiles is not supported. |
| PM-02 | **The supported OS range is a versioned matrix** published as release metadata, not folklore. |
| PM-03 | **ArcChat Mobile is verified on real devices**, not only emulators — the release AOT artifact, cold start, weak network, background resume, and store-package verification. |
| PM-04 | **ArcChat Web is verified against a maintained browser matrix**, including the WebAssembly publish, first load, caching and realtime reconnection. |
| PM-05 | **A hardware lab is mandatory for ArcScope and ArcSlate.** Real serial, network and device interfaces; real media, codecs and GPUs. A CI virtual machine cannot detect the failures these products actually have. |
| PM-06 | **Native hardware paths require fallback tests**: missing GPU, unsupported codec, absent device, driver failure — each must degrade explicitly rather than crash. |
| PM-07 | **Cross-platform file-system behaviour is tested**: case sensitivity, path length, reserved names, Unicode normalisation, permissions, locking, and network or removable volumes. |
| PM-08 | **DPI and multi-monitor are tested**: fractional scaling, mixed-DPI monitors, monitor hot-plug, and window restoration across configuration changes. |
| PM-09 | **The input matrix is tested**: keyboard layouts, IME composition, touch, pen, trackpad gestures, and high-precision pointing. |
| PM-10 | **Shortcut tests follow platform semantics** and verify no conflict with critical OS shortcuts (`SH-04`). |
| PM-11 | **One OS passing ≠ cross-platform support** (`I-398`). |


### 20.1 P2-006 delivery and exclusion checks

| # | Requirement |
|---|---|
| SCV-01 | Published Native AOT desktops contain no WebView/DOM/JavaScript UI, local provider inference or agent scheduler. Core workflows exercise real native controls. Cloud JIT behavior is verified separately; desktop AOT does not impose Cloud AOT. |
| SCV-02 | Native cached Notes work survives offline edits, restart, service expiry and disk/cache pressure, then reconciles through revisions/conflicts. Pending edits/uploads cannot be evicted. Property-view tests cover only the accepted scalar/list/table scope and loss-safe type changes. |
| SCV-03 | Real metering verifies cached/uncached/reasoning categories, cumulative streaming, interrupted calls, unknown usage, cancellation, platform retries, concurrent clients, holds, corrections, price changes, period transitions and duplicate payment events under MT/AC/DC requirements. Deterministic provider fixtures complement a controlled real-provider integration; neither alone proves the full billing loop. |
| SCV-04 | The same public Cloud code runs with a documented mounted sample configuration and operator secrets. Validate missing/invalid policy, atomic activation, rollback, replica convergence, no balance reset, historic-rate retention and no disclosure of private values. A stub policy interface does not pass. |
| SCV-05 | Cloud simulation passes [SIM-20](products/arcscope.md) through the actual database, storage, host and native source adapter. This does not substitute for hardware acquisition tests. |
| SCV-06 | ArcSlate .otio passes [OT-12](products/arcslate.md), including both directions and semantic fidelity, separately from native-project recovery and rendered-media verification. |
| SCV-07 | No obsolete acceptance or schema obligation reintroduces BYOK, multi-agent/ACP delegation, team/member/invite models, whiteboard/slides, flashcards, DOCX import, formula/relation/rollup engines, custom encrypted stores/exports or E2EE. Ordinary TLS, server storage/backup protection, token storage and native data recovery remain verified. |

---

## 21. Severity and waivers

| Severity | Definition | Handling |
|---|---|---|
| **P0** | User data loss or corruption; a security boundary failure; a core workflow entirely unusable; a failed recovery contract | **Release stop. No waiver possible.** |
| **P1** | A major workflow broken, a hard budget ceiling exceeded, an accessibility blocker in a core workflow, a compatibility contract violated | Release blocker; waiver only under §21.1 |
| **P2** | Significant degradation with a workaround | Scheduled; may be waived with expiry |
| **P3** | Minor defect | Tracked |

| # | Requirement |
|---|---|
| SV-01 | **An accessibility failure in a core workflow is a release blocker** (`AX-10`). |
| SV-02 | **Exceeding a performance hard ceiling is a release blocker** (`TH-03`). |

### 21.1 Quality waivers

| # | Requirement |
|---|---|
| WV-01 | A **Quality Waiver** is explicit, attributed, justified, scoped to a specific metric and release, and recorded in the repository. |
| WV-02 | **A waiver expires automatically.** When it does, CI turns red again. |
| WV-03 | **A waiver can never be applied to a P0.** |
| WV-04 | **Quality Waiver ≠ permanently lower standard** (`I-401`). The budget is unchanged; only its enforcement is temporarily deferred for a stated reason. |

---

## 22. Dependency upgrade gate

A dependency upgrade — especially of the communication, serialization, UI or native stack — runs: full build, the AOT publish matrix, contract compatibility tests against previously published clients, performance benchmarks with regression comparison, licence and vulnerability scanning, SBOM regeneration, and the migration corpus where persistence is affected.

**Framework major upgrades additionally re-verify the runtime posture** — notably the Android runtime posture at any framework major version change (**V-04**).

---

## 23. Architecture tests as a quality gate

Architecture tests are part of the quality contract, not a nice-to-have. They fail the build when: the domain references UI, infrastructure or transport libraries; a local RPC adapter references a ViewModel; a contracts project references a platform type; products reference each other's Domain or Application assemblies; a native pointer crosses the adapter boundary; a cloud module reaches into another module's persistence; a catch-all string/object RPC appears; a forbidden alias or obsolete product name appears; a GPL-family or AGPL-only reference enters the Apache-2.0 mobile boundary (**D-004** obligation 7); or a required AOT contract attribute is missing.

---

## 24. Quality dashboard and release report

| # | Requirement |
|---|---|
| QD-01 | **The quality dashboard shows only actionable indicators** — budgets against current values, regression trends, gate status, waiver expiries, matrix health. Hundreds of unread charts are not a quality system. |
| QD-02 | **Every release candidate produces a Quality Report**: budget results against ceilings and regressions, matrix results, migration corpus results, accessibility results, compatibility manifest, open waivers with expiry dates, and known issues. |

---

## 25. The test pyramid

The traditional three layers are insufficient here. The required families, each catching a different failure class:

1. Domain unit tests — pure, fast, no I/O
2. Application tests with port test doubles
3. Persistence tests against real databases
4. Serialization and type-shape compatibility tests
5. Local RPC integration tests over real named pipes and domain sockets
6. Public API contract tests: a generated client against a real server
7. Realtime integration tests: connect, disconnect, reconnect, sequence-gap recovery
8. Native ABI tests per RID, including every error path
9. UI component and automation tests
10. Accessibility tests, automated and assistive-technology-verified
11. Multi-process end-to-end tests
12. Migration and golden-fixture tests
13. Crash, fault-injection and recovery tests
14. Soak and scale tests
15. Performance benchmarks with regression gates
16. Publish, install, update, downgrade-protection and rollback tests
17. Architecture and repository-policy tests
18. Hardware-lab tests for ArcScope and ArcSlate

---

## 26. Quality invariants

| # | Invariant |
|---|---|
| QI-01 | Fast in Debug ≠ fast in Production |
| QI-02 | JIT test pass ≠ AOT compatibility |
| QI-03 | Build success ≠ runtime compatibility |
| QI-04 | App version ≠ contract version |
| QI-05 | Contract compatibility ≠ product policy availability |
| QI-06 | Read compatibility ≠ write compatibility |
| QI-07 | Migration success ≠ data semantic preservation |
| QI-08 | Crash-free ≠ recoverable |
| QI-09 | Undo ≠ crash recovery |
| QI-10 | Cache recovery ≠ canonical data recovery |
| QI-11 | Small benchmark ≠ scale reliability |
| QI-12 | Startup time ≠ time to usable |
| QI-13 | Managed heap ≠ total memory |
| QI-14 | Process running ≠ healthy |
| QI-15 | Responsive animation ≠ responsive product |
| QI-16 | Accessible colour ≠ accessible product |
| QI-17 | Keyboard shortcut ≠ keyboard accessibility |
| QI-18 | Localized UI ≠ locale-safe data |
| QI-19 | Display unit ≠ canonical quantity |
| QI-20 | File path ≠ resource identity |
| QI-21 | Automated test ≠ real-hardware validation |
| QI-22 | One OS passing ≠ cross-platform support |
| QI-23 | Diagnostic log ≠ audit |
| QI-24 | Diagnostics ≠ telemetry consent |
| QI-25 | Performance target ≠ marketing claim |
| QI-26 | Quality waiver ≠ permanently lower standard |
| QI-27 | SLO ≠ external SLA |

---

## 27. Must-pass release scenarios

**Startup** — launching the application requires no account ([`ID-01`](02-identity-account-and-workspace.md)). With an **already enrolled and hydrated** notebook and Cloud entirely offline: ArcNotes starts, the hydrated workspace is editable within budget, pending edits are durably saved and visibly unsynchronised, cloud state refreshes in the background when Cloud returns, and **a cached session is never forced into an interactive re-authentication prompt merely because Cloud is unreachable**. Enrolment itself requires Cloud and sign-in (`PR-02` and `CL-02` of [the ArcNotes requirements](products/arcnotes.md)), so an unenrolled first run is a different scenario and is not this one.

**ArcChat Hub** — ArcChat absent; the professional product starts, works and saves; ArcChat starts later and registration recovers.

**Responsiveness** — under scale-corpus load, input to acknowledgement stays within budget; no UI-thread block exceeds the threshold.

**ArcScope** — an 8-hour continuous capture and visualisation with no monotonic resource growth and no data loss.

**ArcSlate** — a long editing, playback and export cycle with cache churn; memory returns to budget; the project is never damaged by derived-media failure.

**Leak** — soak shows no monotonic growth in handles, threads, subscriptions or native resources.

**Accessibility** — every core workflow completes with keyboard only and with a screen reader; text at 200 % leaves no control unreachable.

**Localization** — pseudo-localised build shows no hard-coded strings and no truncation; the same document produces identical bytes under different locales.

**Units** — a converted display never alters the recorded measurement; a cross-dimension conversion fails; ArcScope retains the source unit.

**AOT** — the full publish matrix produces real artifacts with zero unreviewed trimming/AOT warnings, and the round-trip smoke tests pass on each platform.

**Mixed application versions** — new with previous, and previous with new, in both directions, across the local interoperability window.

**Cloud rolling upgrade** — a client newer than the server, and a client older than the server, both behave per the compatibility policy.

**Migration** — every golden fixture migrates with semantics preserved; round-trip is lossless where declared.

**Migration crash** — interruption at each stage leaves no half-upgraded writable store, and the recovery point genuinely restores.

**Crash after save** — the process is killed immediately after a reported save; the change is present on restart. **Failure is a release stop.**

**Derived corruption** — a corrupted cache is detected, discarded and rebuilt; the project is never reported corrupt because of it.

**Diagnostics** — the bundle contains no secrets and no user content by default; its contents are disclosed; verbose mode expires.

**Cross-platform** — every Tier-1 platform passes build, AOT publish, install, UI, recovery, compatibility and performance.

**Upgrade** — install, upgrade from the previous stable version, downgrade protection, and rollback all succeed with data intact.

---

## 28. Quality process

```
Define budget → Encode in the machine-readable contract → Measure on reference hardware
  → Compare against ceiling and regression baseline
  → Gate in CI → Report in the release quality report
  → Change only through a Quality ADR
```

**A failed hard contract stops the release.** There is no path in which a P0 quality contract failure ships.

---

## 29. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 27` | The entire quality and compatibility contract: two-tier thresholds, reference hardware, startup, memory, soak, background budgets, accessibility, localization, units, AOT, version axes, compatibility matrix, migration testing, contract testing, crash and recovery, diagnostics, platform matrices, severity and waivers, the test pyramid, and the quality invariants |
| `I3 §22`–`§27` | Performance and backpressure principles, release-mode matrix, build governance, test strategy, CI gates, installation and update |
| `I4 §Stage 5`, `§Stage 9`, `§Stage 22` | Update, recovery and migration behaviour that the contract gates |
| **D-007**, **D-008** | Web WebAssembly posture; Cloud is JIT; desktop AOT gates; Android Mono AOT |
| **V-03**, **V-04**, **V-05** | AOT support surfaces, Android runtime posture, and the per-dependency AOT gates enforced here |
