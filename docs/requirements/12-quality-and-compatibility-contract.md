# Product Quality and Compatibility Contract
> Effective scope: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) and [P2-013](../decisions/phase-2-specification-decisions.md#rule-p2-013) amend the technology and application ownership below. **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime and AOT matrix), **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**/**[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**/**[V-05](../assurance/phase-1-official-verification.md#rule-v-05)** (AOT evidence)
> Companions: [`09-shared-desktop-experience.md`](09-shared-desktop-experience.md), [`13-data-formats-and-portability.md`](13-data-formats-and-portability.md), [`../assurance/testing-and-verification-strategy.md`](../assurance/testing-and-verification-strategy.md), [`../assurance/release-gates.md`](../assurance/release-gates.md)

> **Quality Requirement ≠ Engineering Suggestion** ([I-402](01-normative-glossary-and-invariants.md#rule-i-402)).

Everything in this document is a **release gate**. A budget that is not enforced by a gate is not a budget; a compatibility claim that is not tested is not a claim.

The mechanism, in five parts: **Budget + Matrix + Fixture + Test + Release Gate.**

---

## 1. The Product Quality Contract

Each professional desktop carries a versioned Product Quality Contract including its embedded assistant. Android companion, Web companion and user-perceived Cloud interaction have their own contracts.

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
| <a id="rule-qc-01"></a>QC-01 | **The quality contract lives in the repository, under version control**, with a machine-readable representation that CI consumes directly. A wiki page is not a contract. |
| <a id="rule-qc-02"></a>QC-02 | **A quality threshold must never be quietly relaxed in an ordinary change.** Changing a budget requires an explicit **Quality ADR** with evidence and review. |
| <a id="rule-qc-03"></a>QC-03 | Every budget value in this document is an **initial project release budget**, not a marketing promise. If the first real vertical slice proves a budget unreasonable, it is changed through a Quality ADR — and thereafter must not drift without evidence. |

---

## 2. Two-tier thresholds

Every key metric carries **two** limits simultaneously:

| Tier | Meaning | Consequence |
|---|---|---|
| **Absolute budget** | A hard ceiling the product may never exceed, regardless of history | **Unconditional release block** |
| **Regression budget** | Even below the ceiling, it may not keep getting worse | **Blocking review** |

| # | Requirement |
|---|---|
| <a id="rule-th-01"></a>TH-01 | **A repeatable regression of ~10 % against the last stable baseline on a key P50/P95 metric enters a blocking review.** Memory uses the same ~10 % warning line. |
| <a id="rule-th-02"></a>TH-02 | **Benchmarks are noisy**, so a regression gate requires repeated sampling and statistical stability — never a single-machine fluctuation. |
| <a id="rule-th-03"></a>TH-03 | **Exceeding an absolute ceiling blocks unconditionally**, with no statistical argument available. |
| <a id="rule-th-04"></a>TH-04 | *Worked example:* ceiling 2.0 s, previous release 1.30 s, new build 1.72 s. Under the ceiling, but +32 % — this blocks for review. "It's still under two seconds" is not an acceptable justification. |

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
| <a id="rule-rh-01"></a>RH-01 | **Benchmarks run against real release artifacts:** the production Native AOT desktop package, release Android Kotlin/ART package and production Node-built Web assets. A Debug/dev-server result, or a JIT desktop substitute for its required AOT artifact, is not evidence. Cloud and browser measurements use their own supported production runtimes ([I-380](01-normative-glossary-and-invariants.md#rule-i-380), [I-381](01-normative-glossary-and-invariants.md#rule-i-381)). |

---

## 4. Responsiveness

| # | Requirement |
|---|---|
| <a id="rule-rs-01"></a>RS-01 | Input to visible acknowledgement is fast enough that the user knows the operation was accepted, immediately. |
| <a id="rule-rs-02"></a>RS-02 | **Animation must not be used to conceal real slowness** ([I-392](01-normative-glossary-and-invariants.md#rule-i-392)). A spinner over a slow operation is not responsiveness. |
| <a id="rule-rs-03"></a>RS-03 | **A synchronous block of more than ~50 ms on the UI thread is a serious defect**, and a sustained one is release-blocking. |
| <a id="rule-rs-04"></a>RS-04 | **Responsive animation ≠ responsive product** ([I-392](01-normative-glossary-and-invariants.md#rule-i-392)). A smooth frame rate during an unusable wait is not a pass. |
| <a id="rule-rs-05"></a>RS-05 | Long work returns an owner-qualified handle and reports progress without blocking: TaskHandle for Cloud agent tasks, ProductJobHandle for ordinary product work. The UI does not imply identical schedulers. |

---

## 5. Startup

Three distinct moments, never collapsed into "startup time":

```
Process Start → First Window Visible → First Usable Workspace
```

The product metric is **Time To Usable** ([I-389](01-normative-glossary-and-invariants.md#rule-i-389)).

**Desktop V1 startup budget** — reference hardware, release Native AOT, normal local state, cold process to usable workspace, P95:

| Product | Budget |
|---|---|
| Embedded assistant first open (inside each host budget) | Proposed P95 ≤ 300 ms incremental UI activation; no Cloud dependency |
| ArcNotes | ≤ 2.0 s |
| ArcScope | ≤ 2.5 s |
| ArcSlate | ≤ 3.0 s |

| # | Requirement |
|---|---|
| <a id="rule-su-01"></a>SU-01 | ArcScope and ArcSlate may continue device scanning, media indexing and derived-cache loading in the background — **but must never block first workspace availability on them**. |
| <a id="rule-su-02"></a>SU-02 | Native startup opens the shell and authorized cached work without waiting on Cloud. First-run or missing-content views state sign-in/network requirements honestly; Cloud refresh is asynchronous and does not promise account-free local AI or a standalone notebook. |
| <a id="rule-su-03"></a>SU-03 | Core workspace startup never waits for Cloud or assistant activation. ArcNotes, ArcScope and ArcSlate open usable local state first and reconnect their own session in the background. |

---

**Cloud-dependent first action.** Local startup never waits for Cloud. The [launch profile](../architecture/data-model/04-d1-execution-profile.md#launch-capacity-profile-v1) separately measures warm command P95<=2 seconds and idle-to-first-response P95<=10 seconds. Show connecting after one second; preserve pending work and expose retryable failure at the ten-second first-request deadline. This budget is an acceptance target, not a Cloudflare latency guarantee or an AOT startup measurement.

## 6. Memory

**Quiescent base memory ceiling** — release AOT, main workspace open, no large project loaded, 60 s quiescent, derived startup work finished:

| Product | Ceiling |
|---|---|
| Embedded assistant idle overhead (included in host ceiling) | Proposed ≤ 60 MiB incremental main-process memory with an empty conversation |
| ArcNotes | ≤ 250 MiB |
| ArcScope | ≤ 320 MiB |
| ArcSlate | ≤ 450 MiB |

| # | Requirement |
|---|---|
| <a id="rule-mm-01"></a>MM-01 | **Managed heap ≠ total memory** ([I-390](01-normative-glossary-and-invariants.md#rule-i-390)). The budget counts managed heap, native heap, pinned buffers, media buffers, RPC buffers, image buffers and index working memory. GPU memory is measured separately and is never ignored merely because it is not on the managed heap. |
| <a id="rule-mm-02"></a>MM-02 | **"Cache doesn't count as memory" is not a valid exemption.** |
| <a id="rule-mm-03"></a>MM-03 | **Memory pressure must be surrenderable.** Every cache — thumbnails, render cache, frame cache, waveforms, proxy working data, decoded data, analysis cache, visualisation buffers — has a budget and an eviction policy. |
| <a id="rule-mm-04"></a>MM-04 | Under OS memory pressure, **derived and rebuildable memory is released first**. An application must never be killed by the OS while protecting a cache. |

---

### 6.1 Isolation and playback acceptance

Main-process quiescent ceilings include the assistant. Parser/decoder child memory is reported separately while active and included in the total active-work budget; it is not hidden as free memory. GPU consumption is reported separately. Native containment bounds from contracts 06 remain enforced.

Proposed [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020) acceptance profile, requiring owner approval and WP13/37 measurements: on the declared reference hardware, 1080p30 8-bit 4:2:0 material for each supported decode profile, ten minutes at 1× with ContentSandbox isolation enabled; at most 1 dropped frame per 1,000, audio/video offset within ±40 ms, P95 seek-to-first-frame ≤ 500 ms. Report cold/warm seeks, decoding backend, child/main/GPU peaks and sample counts. Missing the target blocks the gate and requires a bounded correction; it never authorizes moving hostile decode into the main process.

## 7. Leaks and soak

| # | Requirement |
|---|---|
| <a id="rule-sk-01"></a>SK-01 | Every product has a **long-running soak test** as a release gate. |
| <a id="rule-sk-02"></a>SK-02 | **No monotonic growth is permitted** in handles, native resources, threads, subscriptions, timers or event registrations. |
| <a id="rule-sk-03"></a>SK-03 | Product soaks cover Cloud agent cycles with native task projections; native note editing with pending sync/index work; at least 8 hours of hardware capture/visualization; the 24-hour Cloud simulator soak in [SIM-20](products/arcscope.md#rule-sim-20); and native timeline/playback/export with cache churn. |
| <a id="rule-sk-04"></a>SK-04 | **Small benchmark ≠ scale reliability** ([I-388](01-normative-glossary-and-invariants.md#rule-i-388)). Soak and scale results, not micro-benchmarks, decide the gate. |

---

## 8. Background resource contract

> ArcForges is not a permanent CPU-burning tool.

| Condition | Budget |
|---|---|
| Idle, application in background, no active work | ≤ ~0.5 % of one logical core, averaged |
| Fully quiescent (nothing pending at all) | Target ≤ ~0.2 % of one logical core, averaged |

| # | Requirement |
|---|---|
| <a id="rule-bg-01"></a>BG-01 | **Busy polling is prohibited.** Waiting is event-driven, with bounded backoff. |
| <a id="rule-bg-02"></a>BG-02 | Background traffic is bounded. Prefer notifications/outbox dispatch; when realtime is unavailable, authorized HTTP polling with backoff, jitter, idle limits and reconnect backfill is supported. Busy polling and unbounded retries are prohibited. |
| <a id="rule-bg-03"></a>BG-03 | **Background work must not starve foreground work.** Task resource competition has explicit priority: a timeline drag must not stutter, a capture must not lose data, and typing must not lag because of background indexing, sync or rendering. |

---

## 9. Scale corpus

| # | Requirement |
|---|---|
| <a id="rule-sc-01"></a>SC-01 | Each product declares a **Scale Corpus** — the size each release must support and remain stable at. Anything at or below that scale must behave correctly. |
| <a id="rule-sc-02"></a>SC-02 | **Performance budgets are expressed in terms of user work**, not only function-level micro-benchmarks: open a large document, scrub a long timeline, run an 8-hour capture, search a large corpus. |
| <a id="rule-sc-03"></a>SC-03 | **Search quality and search performance are separate contracts** ([QA-01](06-knowledge-search-and-retrieval.md#rule-qa-01), [QA-04](06-knowledge-search-and-retrieval.md#rule-qa-04) in the knowledge requirements). A fast search that returns the wrong result is a failure of a different contract. |

---

## 10. Accessibility contract

> **All major user workflows reach WCAG 2.2 AA semantic level and correctly connect to the target platform's accessibility APIs.**

| # | Requirement |
|---|---|
| <a id="rule-ax-01"></a>AX-01 | **No core workflow may require a mouse** ([I-394](01-normative-glossary-and-invariants.md#rule-i-394)). Every action has a keyboard-accessible semantic path through the command system. |
| <a id="rule-ax-02"></a>AX-02 | **Focus contract**: focus is always visible; focus order is logical; a dialog traps and restores focus; **Focus ≠ Selection** ([I-404](01-normative-glossary-and-invariants.md#rule-i-404)); after an operation, focus returns to a sensible origin. |
| <a id="rule-ax-03"></a>AX-03 | **Screen reader contract**: every control exposes role, name, value and state; live regions announce state changes; complex professional surfaces expose a meaningful structure rather than a flat control soup. |
| <a id="rule-ax-04"></a>AX-04 | **Every icon-only control has an accessible name**, and an icon is never the sole carrier of information ([DS-07](09-shared-desktop-experience.md#rule-ds-07)). |
| <a id="rule-ax-05"></a>AX-05 | **Colour is never the only source of information** ([I-393](01-normative-glossary-and-invariants.md#rule-i-393)). Every state distinguished by colour is also distinguished by shape, text or icon. |
| <a id="rule-ax-06"></a>AX-06 | **High-contrast and reduced-motion system settings are honoured.** |
| <a id="rule-ax-07"></a>AX-07 | **Text scaling to 200 %** keeps every core workflow usable, with no clipped or unreachable controls. |
| <a id="rule-ax-08"></a>AX-08 | **Accessible colour ≠ accessible product** ([I-393](01-normative-glossary-and-invariants.md#rule-i-393)). Contrast conformance alone does not satisfy the contract. |
| <a id="rule-ax-09"></a>AX-09 | **The accessibility test matrix is real**: automated semantic checks on every change; assistive-technology verification on the release train against each Tier-1 platform's own accessibility stack. |
| <a id="rule-ax-10"></a>AX-10 | **An accessibility failure in a core workflow is a release blocker.** |

---

## 11. Localization contract

| # | Requirement |
|---|---|
| <a id="rule-lo-01"></a>LO-01 | **Every user-visible string is localisable from day one**, including in shared components. |
| <a id="rule-lo-02"></a>LO-02 | **Persistent identifiers are never localised.** Enum values, ids, capability identifiers, format keys, file-format tokens and protocol constants are stable invariants; only their display is localised. |
| <a id="rule-lo-03"></a>LO-03 | **String concatenation to build sentences is prohibited.** Localisation resources support parameters and plural semantics. |
| <a id="rule-lo-04"></a>LO-04 | **Pseudo-localisation is a CI test**, catching hard-coded strings, truncation and concatenation before translation exists. |
| <a id="rule-lo-05"></a>LO-05 | **RTL is a foundation concern, not a future rewrite.** The foundation must not make RTL impossible, even where an RTL locale does not ship in V1. |
| <a id="rule-lo-06"></a>LO-06 | **User data never changes because the interface language changed** ([I-395](01-normative-glossary-and-invariants.md#rule-i-395)). The same document, the same measurement, the same project produce identical stored bytes in every locale. |
| <a id="rule-lo-07"></a>LO-07 | **Localized UI ≠ locale-safe data** ([I-395](01-normative-glossary-and-invariants.md#rule-i-395)). Storage is canonical and invariant; presentation is localised. |
| <a id="rule-lo-08"></a>LO-08 | Dates, numbers and currency display in the user's locale and store in an invariant representation. |
| <a id="rule-lo-09"></a>LO-09 | **Parsing semantics do not change with locale** for stored or interchange content. A file written under one locale parses identically under another. |

### 11.1 Time

| # | Requirement |
|---|---|
| <a id="rule-tz-01"></a>TZ-01 | An instant is stored as a UTC-equivalent stable representation. |
| <a id="rule-tz-02"></a>TZ-02 | Where the **original zone carries meaning** — a scheduled automation, a capture timestamp, a user-authored deadline — the original zone semantics are stored alongside, not discarded. |
| <a id="rule-tz-03"></a>TZ-03 | Scheduling carries a time zone and an explicit DST resolution policy ([TG-01](05-ai-and-agent-execution.md#rule-tg-01), [TG-02](05-ai-and-agent-execution.md#rule-tg-02)). |

### 11.2 Units

> **Quantity = Value + Dimension + Unit semantics** ([I-396](01-normative-glossary-and-invariants.md#rule-i-396)).

| # | Requirement |
|---|---|
| <a id="rule-un-01"></a>UN-01 | **Canonical unit and display unit are separate.** Changing a display unit never changes the recorded measurement fact. |
| <a id="rule-un-02"></a>UN-02 | **ArcScope retains the source unit** as acquisition provenance. A converted display value never overwrites what the instrument reported. |
| <a id="rule-un-03"></a>UN-03 | **Engineering prefixes are handled by a unified formatter.** Products must not write their own prefix string formatting. |
| <a id="rule-un-04"></a>UN-04 | **Unit conversion is dimension-safe.** Converting across incompatible dimensions is a compile-time or validation error, never a silent numeric operation. |
| <a id="rule-un-05"></a>UN-05 | **ArcSlate time is not forced into the general unit system.** It uses a rational time and time-base model, because frame-accurate editing requires exact rational arithmetic rather than floating-point seconds ([I-478](01-normative-glossary-and-invariants.md#rule-i-478)). |

---

## 12. AOT contract

> **AOT compatibility is not a compilation option; it is part of the compatibility contract.**

| # | Requirement |
|---|---|
| <a id="rule-ao-01"></a>AO-01 | **Every official release runs the real publish matrix**, producing genuine artifacts. A failure to publish is a failed release, not a warning. |
| <a id="rule-ao-02"></a>AO-02 | **`IL2026` / `IL3050` and equivalent trimming/AOT warnings are release-blocking by default** on any project consumed by an AOT deliverable. |
| <a id="rule-ao-03"></a>AO-03 | **Suppression is permitted but audited**: each suppression is narrow, justified, attributed, and carries a revalidation trigger. A blanket global suppression is prohibited. |
| <a id="rule-ao-04"></a>AO-04 | **AOT tests use the final published artifact**, not a Debug or JIT build ([I-381](01-normative-glossary-and-invariants.md#rule-i-381)). |
| <a id="rule-ao-05"></a>AO-05 | Native AOT gates apply to every desktop and C# Cloud deliverable and their complete managed dependency closures under P2-009. Kotlin/Jetpack Compose and browser assets have their own measured release gates. |
| <a id="rule-ao-06"></a>AO-06 | **A third-party extension does not change this contract.** The host stays a Native AOT deliverable; an extension runs out of process with its own runtime and does not affect the host's AOT metrics ([EX-04](08-extensions-and-developer-platform.md#rule-ex-04) in the extension requirements). |
| <a id="rule-ao-07"></a>AO-07 | Android uses the pinned Kotlin/Jetpack Compose release profile. No .NET mobile runtime/AOT flag is applied; iOS is outside the current scope. |
| <a id="rule-ao-08"></a>AO-08 | **Web is React/TypeScript production browser assets built with the pinned Node.js/npm toolchain** ([P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008)); .NET WebAssembly/AOT flags do not apply. Type safety, generated-contract drift, browser/visual/accessibility behavior and asset budgets are release gates. |
| <a id="rule-ao-09"></a>AO-09 | Publish real generated gRPC/Protobuf clients and servers, explicit serializers/auth/SQL adapters, Avalonia and every admitted native/control dependency with zero trimming/AOT diagnostics; WP06 proves actual candidate artifacts. |

---

## 13. Native ABI contract

The native boundary is a compatibility contract in its own right: exported ABI version, struct layout and size/version fields, calling convention, string encoding and ownership, handle semantics, error model, callback protocol, and the minimum driver or system capability required.

**Native and managed ship as one version set** ([I-208](01-normative-glossary-and-invariants.md#rule-i-208) analogue). An ABI change is a versioned, tested, migration-aware event.

---

## 14. Version axes

**"Version" alone is never sufficient.** Nine independent axes exist and none may be collapsed into another ([I-383](01-normative-glossary-and-invariants.md#rule-i-383)):

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
| <a id="rule-cm-01"></a>CM-01 | **Every release produces a Compatibility Manifest as a release artifact**, answering: which product versions can this interoperate with locally; which contract sets it speaks; which native formats it can read and write; which cloud API versions it can reach; which extension protocol versions it supports; which native ABI it requires. |
| <a id="rule-cm-02"></a>CM-02 | **The three professional desktop products version independently** ([P-12](00-product-scope-and-portfolio.md#rule-p-12)), and **mixed-version combinations must actually be tested**. Nominal independent release plus de facto lockstep upgrade is a failed contract. |
| <a id="rule-cm-03"></a>CM-03 | Client↔Cloud and parent↔helper contracts support the current stable and immediately previous supported stable line. Compatibility is tested on protocol versions and published artifacts, not on pairs of different professional products. |
| <a id="rule-cm-04"></a>CM-04 | A contract major upgrade requires an explicit **coexistence migration window** in which V1 and V2 both operate. |
| <a id="rule-cm-05"></a>CM-05 | **"Previous version" is a floor, not a ceiling.** Some contracts may be supported longer; a security-driven sunset may be scheduled earlier through the policy control plane. |
| <a id="rule-cm-06"></a>CM-06 | **Cloud compatibility follows a declared Supported Client Set.** Removing support is planned and communicated through compatibility policy, never discovered by users. |
| <a id="rule-cm-07"></a>CM-07 | **A client newer than Cloud must also be tested.** Rolling upgrade means both orderings occur. |
| <a id="rule-cm-08"></a>CM-08 | **Extension protocol compatibility: current major plus previous major**, except where a security reason forces earlier revocation. |
| <a id="rule-cm-09"></a>CM-09 | **Native format compatibility outlives application interoperability.** Every historical format still in the Supported Native Format set has a golden fixture and a migration test. Formats beyond that set have a maintained conversion or archival migration path. |
| <a id="rule-cm-10"></a>CM-10 | **Read compatibility ≠ write compatibility** ([I-385](01-normative-glossary-and-invariants.md#rule-i-385)). Being able to open an older or newer file does not imply being able to save it without loss. Each is declared and tested separately. |
| <a id="rule-cm-11"></a>CM-11 | There is no "ArcForges 4.0" that implies a synchronized version across products. |

---

## 16. Migration testing

| # | Requirement |
|---|---|
| <a id="rule-mg-01"></a>MG-01 | **Migration is a first-class test type** with its own **Migration Test Corpus**, not a subset of integration tests. |
| <a id="rule-mg-02"></a>MG-02 | **Every historical format version has a permanent golden fixture** — fixed, immutable test data committed to the repository. |
| <a id="rule-mg-03"></a>MG-03 | **Golden fixtures come from multiple sources**: synthesised, captured from real usage with consent and redaction, and edge cases. **Unredacted real user data never enters the test repository.** |
| <a id="rule-mg-04"></a>MG-04 | **Migration tests verify semantics, not merely "it opens"** ([I-386](01-normative-glossary-and-invariants.md#rule-i-386)). Content, structure, references, revisions, properties, timing and units must all survive. |
| <a id="rule-mg-05"></a>MG-05 | **Round-trip migration is tested** where the format supports it. |
| <a id="rule-mg-06"></a>MG-06 | **Migration failure injection is a required test**: interruption at each stage must leave **no half-upgraded writable store**. |
| <a id="rule-mg-07"></a>MG-07 | **The pre-migration recovery point is tested, not merely implemented** ([SV-04](03-cloud-services-and-sync.md#rule-sv-04)). Restoring from it must genuinely restore. |
| <a id="rule-mg-08"></a>MG-08 | **Downgrade behaviour is tested.** An older application encountering newer data enters a safe read-only or explicitly-blocked state; it must never silently discard fields it does not understand ([SV-02](03-cloud-services-and-sync.md#rule-sv-02)). |
| <a id="rule-mg-09"></a>MG-09 | **Application binary rollback ≠ data rollback** ([I-208](01-normative-glossary-and-invariants.md#rule-i-208)). Both are tested, and their separation is explicit in the product. |

---

## 17. Contract testing

Contract tests cover **every** communication boundary: local RPC, public HTTP API, realtime, the native ABI, the extension protocol, and persisted formats.

| # | Requirement |
|---|---|
| <a id="rule-ct-01"></a>CT-01 | **"Both sides reference the same assembly" is not a contract test.** A real contract test exercises a previously published client against the current implementation, and vice versa. |
| <a id="rule-ct-02"></a>CT-02 | **Serialized golden vectors** are committed: exact bytes for representative messages and documents, so an accidental wire or format change fails loudly. |
| <a id="rule-ct-03"></a>CT-03 | **The error contract is tested.** Stable semantic error codes are part of the contract; **the code never changes with localisation** ([LO-02](#rule-lo-02)). |
| <a id="rule-ct-04"></a>CT-04 | **`CommandId` idempotency is a contract test**: the same logical write delivered several times produces exactly one effect. |
| <a id="rule-ct-05"></a>CT-05 | **Realtime disconnection recovery is a contract test**: after a gap, sequence backfill must recover the missed range exactly — a client at sequence 100 that reconnects at 130 must not silently skip 101–129. |
| <a id="rule-ct-06"></a>CT-06 | Contract tests run against **real transports** — real named pipes and domain sockets, a real HTTP server, a real realtime connection — not in-memory doubles alone. |

---

## 18. Crash and recovery contract

**Actively killing the process is a formal testing method.** Every stable release must do it.

| # | Requirement |
|---|---|
| <a id="rule-cr-01"></a>CR-01 | **The core crash contract: anything reported as saved locally must exist after a crash.** Violating it is a **P0 release blocker**. |
| <a id="rule-cr-02"></a>CR-02 | **Derived data may be lost** and must be rebuildable. Losing a cache must never corrupt a project. |
| <a id="rule-cr-03"></a>CR-03 | Fault-injection points include at least: kill immediately after save; kill mid-write; kill mid-migration; kill mid-sync; kill during capture; kill during render; disk full; database busy; corrupted snapshot; corrupted derived cache; native library fault. |
| <a id="rule-cr-04"></a>CR-04 | **ArcScope capture recovery is separately tested**: an interrupted capture must recover to the last durably committed data with an accurate, honest boundary — never silently truncated and presented as complete. |
| <a id="rule-cr-05"></a>CR-05 | **ArcSlate recovery is separately tested**: a project must not be damaged by a proxy or render failure; the timeline and project data survive independently of derived media. |
| <a id="rule-cr-06"></a>CR-06 | **Crash-loop protection** is required: repeated startup failures enter **Safe Start / Recovery Mode**, which is read-first, does not modify canonical content, and **never automatically deletes user data**. |
| <a id="rule-cr-07"></a>CR-07 | **Cache recovery ≠ canonical data recovery** ([I-222](01-normative-glossary-and-invariants.md#rule-i-222)). Rebuilding a cache is not evidence that canonical recovery works. |
| <a id="rule-cr-08"></a>CR-08 | **Crash-free ≠ recoverable** ([I-387](01-normative-glossary-and-invariants.md#rule-i-387)). A release with no crashes but no proven recovery path has not met this contract. |

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
| <a id="rule-dg-01"></a>DG-01 | **A diagnostic bundle is never uploaded automatically** ([I-424](01-normative-glossary-and-invariants.md#rule-i-424)). It is exported on explicit user action, its contents are shown, and it is redacted by default. |
| <a id="rule-dg-02"></a>DG-02 | **A diagnostic bundle does not include by default**: document content, note content, chat content, media, raw captures, secrets, or tokens. Including any of these requires an explicit, itemised user choice. |
| <a id="rule-dg-03"></a>DG-03 | **Local paths are redacted or normalised by default**, because a path can identify a person. |
| <a id="rule-dg-04"></a>DG-04 | **Verbose diagnostics are time-bounded** and revert automatically. |
| <a id="rule-dg-05"></a>DG-05 | **Logs have a rotation budget** — size, age and count — and never grow without limit. |
| <a id="rule-dg-06"></a>DG-06 | **Correlation runs through the entire system**: one correlation identity traverses local RPC, HTTP, realtime, tasks and audit, so an incident can be reconstructed. |
| <a id="rule-dg-07"></a>DG-07 | **Crash symbols are tied to build identity**, retained, and resolvable for the supported version window. |
| <a id="rule-dg-08"></a>DG-08 | **Diagnostics must never become a telemetry bypass** ([I-399](01-normative-glossary-and-invariants.md#rule-i-399)). "It's a diagnostic" does not license collecting what telemetry consent forbids. |
| <a id="rule-dg-09"></a>DG-09 | **Diagnostic Log ≠ Audit** ([I-276](01-normative-glossary-and-invariants.md#rule-i-276)). |

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
| <a id="rule-pm-01"></a>PM-01 | **Desktop Tier-1 platforms genuinely enter build, AOT publish, install, UI, recovery, compatibility, performance and release matrices.** A platform that only compiles is not supported. |
| <a id="rule-pm-02"></a>PM-02 | **The supported OS range is a versioned matrix** published as release metadata, not folklore. |
| <a id="rule-pm-03"></a>PM-03 | **Android companion is verified on real devices**, not only emulators — the Kotlin/Jetpack Compose release artifact, cold start, weak network, background resume, and store-package verification. |
| <a id="rule-pm-04"></a>PM-04 | **All four Web outputs are verified against [browser-support.v1](#202-browser-supportv1)**, including production assets, first load, caching, authentication/step-up, streaming/fallback and reconnect. The matrix is a release artifact with exact tested versions, not an undefined package-local target. |
| <a id="rule-pm-05"></a>PM-05 | **A hardware lab is mandatory for ArcScope and ArcSlate.** Real serial, network and device interfaces; real media, codecs and GPUs. A CI virtual machine cannot detect the failures these products actually have. |
| <a id="rule-pm-06"></a>PM-06 | **Native hardware paths require fallback tests**: missing GPU, unsupported codec, absent device, driver failure — each must degrade explicitly rather than crash. |
| <a id="rule-pm-07"></a>PM-07 | **Cross-platform file-system behaviour is tested**: case sensitivity, path length, reserved names, Unicode normalisation, permissions, locking, and network or removable volumes. |
| <a id="rule-pm-08"></a>PM-08 | **DPI and multi-monitor are tested**: fractional scaling, mixed-DPI monitors, monitor hot-plug, and window restoration across configuration changes. |
| <a id="rule-pm-09"></a>PM-09 | **The input matrix is tested**: keyboard layouts, IME composition, touch, pen, trackpad gestures, and high-precision pointing. |
| <a id="rule-pm-10"></a>PM-10 | **Shortcut tests follow platform semantics** and verify no conflict with critical OS shortcuts ([SH-04](09-shared-desktop-experience.md#rule-sh-04)). |
| <a id="rule-pm-11"></a>PM-11 | **One OS passing ≠ cross-platform support** ([I-398](01-normative-glossary-and-invariants.md#rule-i-398)). |


### 20.1 [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) delivery and exclusion checks

| # | Requirement |
|---|---|
| <a id="rule-scv-01"></a>SCV-01 | Published Native AOT desktops contain no WebView/DOM/JavaScript UI or local AI. Cloud is independently Native AOT; the sole remote AI loop is the CF Workflow. Test each actual artifact. |
| <a id="rule-scv-02"></a>SCV-02 | Native cached Notes work survives offline edits, restart, service expiry and disk/cache pressure, then reconciles through revisions/conflicts. Pending edits/uploads cannot be evicted. Property-view tests cover only the accepted scalar/list/table scope and loss-safe type changes. |
| <a id="rule-scv-03"></a>SCV-03 | Real metering verifies cached/uncached/reasoning categories, cumulative streaming, interrupted calls, unknown usage, cancellation, platform retries, concurrent clients, holds, corrections, price changes, period transitions and duplicate payment events under MT/AC/DC requirements. Deterministic provider fixtures complement a controlled real-provider integration; neither alone proves the full billing loop. |
| <a id="rule-scv-04"></a>SCV-04 | The same public Cloud code runs with a documented mounted sample configuration and operator secrets. Validate missing/invalid policy, atomic activation, rollback, replica convergence, no balance reset, historic-rate retention and no disclosure of private values. A stub policy interface does not pass. |
| <a id="rule-scv-05"></a>SCV-05 | Cloud simulation passes [SIM-20](products/arcscope.md#rule-sim-20) through the actual database, storage, host and native source adapter. This does not substitute for hardware acquisition tests. |
| <a id="rule-scv-06"></a>SCV-06 | ArcSlate .otio passes [OT-12](products/arcslate.md#rule-ot-12), including both directions and semantic fidelity, separately from native-project recovery and rendered-media verification. |
| <a id="rule-scv-07"></a>SCV-07 | No obsolete acceptance or schema obligation reintroduces BYOK, multi-agent/ACP delegation, team/member/invite models, whiteboard/slides, flashcards, DOCX import, formula/relation/rollup engines, custom encrypted stores/exports or E2EE. Ordinary TLS, server storage/backup protection, token storage and native data recovery remain verified. |

---

### 20.2 Browser support.v1

Web owns the versioned `browser-support.v1.json` artifact; Quality verifies it and the release approver signs its hash with the compatibility manifest. Publish beside the OS matrix at `downloads.arcforges.com/compatibility/<releaseId>/browser-support.v1.json`, and link it from the public support page and each interactive unsupported-browser notice. It binds site, account, chat and operations, including their narrow layouts; it adds no iOS application target.

| Browser / admitted OS | Technical build floor | Fully supported release set |
|---|---|---|
| Chrome and Edge on supported Windows/macOS/Linux | 134 | Current and immediately previous stable major, at their latest vendor security patch at release freeze, and never below 134 |
| Firefox on supported Windows/macOS/Linux | 136 | Current and immediately previous stable major, latest security patch, never below 136; ESR only when its actual major belongs to this same set |
| Safari on supported macOS | 18.4 | Current and immediately previous supported stable major family, latest OS/security update, never below 18.4 |
| Chrome on supported Android | 134 | Current and previous stable major at latest patch, never below 134; test on the maintained Android OS/device matrix |

The previous-major rule is the product support decision; resolving vendor release numbers is a deterministic release task, not permission to choose an arbitrary market floor. The artifact records schemaVersion=browser-support.v1, releaseId, frozenAt, owner, qualityApprovalRef, buildTargets, and entries{browser,engine,osRange,minVersion,maxTestedVersion,testedVersions,tier,streaming,stepUp,previewIsolation,evidenceHashes}, plus outputArtifactHashes for all four outputs. No literal current/latest value is permitted in a published version field. Reject a release with a required entry missing or with its production asset hash different from the tested one. Exact browser patches are maintained in Web's release/test inputs, not guessed permanently in this Design.

Tier behavior is explicit: **supported** means every required flow passes; **degraded-with-notice** is allowed for a supported browser when the network buffers streaming or the device lacks an enrolled usable authenticator, with only the declared fallback/refusal below; **blocked** covers below-floor/unsupported engines, embedded/in-app WebViews, or absent essential secure-cookie/WebCrypto/fetch/BigInt/ES-module primitives. Blocked interactive output displays a static update/open-in-supported-browser action before authentication or mutation, preserves existing local drafts and never destroys private data. Public static content/downloads/docs remain readable without JavaScript; no security assurance is inferred for untested browsers. Browser identity detection is advisory, never an authorization check.

| Capability | Supported behavior and explicit fallback/refusal |
|---|---|
| Response-body streaming | Use generated binary gRPC-Web Watch/WatchOutput. After the existing 45-second silence timeout, or a proved buffered/unavailable stream, select EventService.Poll and ExecutionService.ReadOutput using the same cursor, owner and final-hash rules; show “Live updates delayed”. One event poll per 10 seconds and each active output read per 5 seconds, full jitter +/-20%, no overlapping requests; honor retryAfter/backoff, pause hidden idle views, and immediately reconcile on foreground/user refresh. This is a transport fallback only; it never restarts a command or marks partial output complete. Test the all-poll workload as well as streaming. |
| WebAuthn step-up | Require the same server challenge/origin/RP/UV policy on every engine. A capability probe or successful password/email login is not step-up proof. If the selected account has no usable enrolled passkey/authenticator, keep the sensitive action unexecuted and offer the accepted account recovery or another supported device/browser ceremony; do not lower its assurance, auto-approve or transfer a sibling application's token. Preserve the pending action for explicit revalidation afterwards. |
| Untrusted-content preview | Require the selected iframe sandbox/CSP isolation, with no same-origin-plus-script escape. If isolation cannot be enforced, refuse inline preview and offer only an authorized download/open action under the original resource policy. Never render unsafe HTML as a compatibility fallback. |

The technical floors are deliberate compilation targets. Vite and CSS tooling must receive explicit matching targets rather than their moving defaults; generated Contracts adapters use the same minimums. Polyfills may supply presentation conveniences but never fabricate WebAuthn, credential isolation, streaming authority or iframe security. Primary capability references checked 2026-09-18: [Fetch response streams](https://developer.mozilla.org/en-US/docs/Web/API/Response/body), [WebAuthn authenticator availability](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/isUserVerifyingPlatformAuthenticatorAvailable_static), and [Vite production targets](https://vite.dev/guide/build.html). Actual release browser/OS combinations still require real evidence.

## 21. Severity and waivers

| Severity | Definition | Handling |
|---|---|---|
| **P0** | User data loss or corruption; a security boundary failure; a core workflow entirely unusable; a failed recovery contract | **Release stop. No waiver possible.** |
| **P1** | A major workflow broken, a hard budget ceiling exceeded, an accessibility blocker in a core workflow, a compatibility contract violated | Release blocker; waiver only under §21.1 |
| **P2** | Significant degradation with a workaround | Scheduled; may be waived with expiry |
| **P3** | Minor defect | Tracked |

| # | Requirement |
|---|---|
| <a id="rule-sv-01"></a>SV-01 | **An accessibility failure in a core workflow is a release blocker** ([AX-10](#rule-ax-10)). |
| <a id="rule-sv-02"></a>SV-02 | **Exceeding a performance hard ceiling is a release blocker** ([TH-03](#rule-th-03)). |

### 21.1 Quality waivers

| # | Requirement |
|---|---|
| <a id="rule-wv-01"></a>WV-01 | A **Quality Waiver** is explicit, attributed, justified, scoped to a specific metric and release, and recorded in the repository. |
| <a id="rule-wv-02"></a>WV-02 | **A waiver expires automatically.** When it does, CI turns red again. |
| <a id="rule-wv-03"></a>WV-03 | **A waiver can never be applied to a P0.** |
| <a id="rule-wv-04"></a>WV-04 | **Quality Waiver ≠ permanently lower standard** ([I-401](01-normative-glossary-and-invariants.md#rule-i-401)). The budget is unchanged; only its enforcement is temporarily deferred for a stated reason. |

---

## 22. Dependency upgrade gate

A dependency upgrade — especially of the communication, serialization, UI or native stack — runs: full build, the AOT publish matrix, contract compatibility tests against previously published clients, performance benchmarks with regression comparison, licence and vulnerability scanning, SBOM regeneration, and the migration corpus where persistence is affected.

**Framework major upgrades additionally re-verify the runtime posture** — notably the Android runtime posture at any framework major version change (**[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**).

---

## 23. Architecture tests as a quality gate

Architecture tests are part of the quality contract, not a nice-to-have. They fail the build when: the domain references UI, infrastructure or transport libraries; a local RPC adapter references a ViewModel; a contracts project references a platform type; products reference each other's Domain or Application assemblies; a native pointer crosses the adapter boundary; a cloud module reaches into another module's persistence; a catch-all string/object RPC appears; a forbidden alias or obsolete product name appears; a GPL-family or AGPL-only reference enters the Apache-2.0 mobile boundary (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7); or a required AOT contract attribute is missing.

---

## 24. Quality dashboard and release report

| # | Requirement |
|---|---|
| <a id="rule-qd-01"></a>QD-01 | **The quality dashboard shows only actionable indicators** — budgets against current values, regression trends, gate status, waiver expiries, matrix health. Hundreds of unread charts are not a quality system. |
| <a id="rule-qd-02"></a>QD-02 | **Every release candidate produces a Quality Report**: budget results against ceilings and regressions, matrix results, migration corpus results, accessibility results, compatibility manifest, open waivers with expiry dates, and known issues. |

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
| <a id="rule-qi-01"></a>QI-01 | Fast in Debug ≠ fast in Production |
| <a id="rule-qi-02"></a>QI-02 | JIT test pass ≠ AOT compatibility |
| <a id="rule-qi-03"></a>QI-03 | Build success ≠ runtime compatibility |
| <a id="rule-qi-04"></a>QI-04 | App version ≠ contract version |
| <a id="rule-qi-05"></a>QI-05 | Contract compatibility ≠ product policy availability |
| <a id="rule-qi-06"></a>QI-06 | Read compatibility ≠ write compatibility |
| <a id="rule-qi-07"></a>QI-07 | Migration success ≠ data semantic preservation |
| <a id="rule-qi-08"></a>QI-08 | Crash-free ≠ recoverable |
| <a id="rule-qi-09"></a>QI-09 | Undo ≠ crash recovery |
| <a id="rule-qi-10"></a>QI-10 | Cache recovery ≠ canonical data recovery |
| <a id="rule-qi-11"></a>QI-11 | Small benchmark ≠ scale reliability |
| <a id="rule-qi-12"></a>QI-12 | Startup time ≠ time to usable |
| <a id="rule-qi-13"></a>QI-13 | Managed heap ≠ total memory |
| <a id="rule-qi-14"></a>QI-14 | Process running ≠ healthy |
| <a id="rule-qi-15"></a>QI-15 | Responsive animation ≠ responsive product |
| <a id="rule-qi-16"></a>QI-16 | Accessible colour ≠ accessible product |
| <a id="rule-qi-17"></a>QI-17 | Keyboard shortcut ≠ keyboard accessibility |
| <a id="rule-qi-18"></a>QI-18 | Localized UI ≠ locale-safe data |
| <a id="rule-qi-19"></a>QI-19 | Display unit ≠ canonical quantity |
| <a id="rule-qi-20"></a>QI-20 | File path ≠ resource identity |
| <a id="rule-qi-21"></a>QI-21 | Automated test ≠ real-hardware validation |
| <a id="rule-qi-22"></a>QI-22 | One OS passing ≠ cross-platform support |
| <a id="rule-qi-23"></a>QI-23 | Diagnostic log ≠ audit |
| <a id="rule-qi-24"></a>QI-24 | Diagnostics ≠ telemetry consent |
| <a id="rule-qi-25"></a>QI-25 | Performance target ≠ marketing claim |
| <a id="rule-qi-26"></a>QI-26 | Quality waiver ≠ permanently lower standard |
| <a id="rule-qi-27"></a>QI-27 | SLO ≠ external SLA |

---

## 27. Must-pass release scenarios

**Startup** — launching the application requires no account ([`ID-01`](02-identity-account-and-workspace.md#rule-id-01)). With an **already enrolled and hydrated** notebook and Cloud entirely offline: ArcNotes starts, the hydrated workspace is editable within budget, pending edits are durably saved and visibly unsynchronised, cloud state refreshes in the background when Cloud returns, and **a cached session is never forced into an interactive re-authentication prompt merely because Cloud is unreachable**. Enrolment itself requires Cloud and sign-in ([PR-02](products/arcnotes.md#rule-pr-02) and [CL-02](products/arcnotes.md#rule-cl-02) of [the ArcNotes requirements](products/arcnotes.md)), so an unenrolled first run is a different scenario and is not this one.

**Independent assistant ownership** — two professional apps launch with separate stores/connections; each saves with Cloud offline. Closing/restarting one cannot alter the other's history or pending work.

**Responsiveness** — under scale-corpus load, input to acknowledgement stays within budget; no UI-thread block exceeds the threshold.

**ArcScope** — an 8-hour continuous capture and visualisation with no monotonic resource growth and no data loss.

**ArcSlate** — a long editing, playback and export cycle with cache churn; memory returns to budget; the project is never damaged by derived-media failure.

**Leak** — soak shows no monotonic growth in handles, threads, subscriptions or native resources.

**Accessibility** — every core workflow completes with keyboard only and with a screen reader; text at 200 % leaves no control unreachable.

**Localization** — pseudo-localised build shows no hard-coded strings and no truncation; the same document produces identical bytes under different locales.

**Units** — a converted display never alters the recorded measurement; a cross-dimension conversion fails; ArcScope retains the source unit.

**AOT** — the full publish matrix produces real artifacts with zero unreviewed trimming/AOT warnings, and the round-trip smoke tests pass on each platform.

**Mixed contract versions** — current/previous client↔Cloud and parent↔helper combinations negotiate or refuse explicitly. No product-to-product interoperability gate exists.

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

| Current document | Relationship |
|---|---|
| [Testing and Verification Strategy](../assurance/testing-and-verification-strategy.md) | Assigns verification families and evidence responsibilities |
| [Release Gates](../assurance/release-gates.md) | Applies quality and compatibility acceptance at release boundaries |
| [Deployment and Release Execution](../architecture/22-deployment-and-release-execution.md) | Implements migration, mixed-version and rollback constraints |
| **[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)**, **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | React/TypeScript Web posture under [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008); Cloud is Native AOT; desktop AOT gates; Android Kotlin/Jetpack Compose |
| **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**, **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)** | AOT support surfaces, Android runtime posture, and the per-dependency AOT gates enforced here |
