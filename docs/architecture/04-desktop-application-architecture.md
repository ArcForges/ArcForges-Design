# Desktop Application Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (desktop is a Native AOT deliverable), **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)** (Avalonia AOT evidence)
> Companions: [`00-architecture-overview.md`](00-architecture-overview.md), [`03-local-ipc-and-process-model.md`](03-local-ipc-and-process-model.md), [`../requirements/09-shared-desktop-experience.md`](../requirements/09-shared-desktop-experience.md)

One structure, used identically by ArcChat, ArcNotes, ArcScope and ArcSlate.

---

## 1. Process structure

```
.NET Generic Host  (Native AOT)
├── Avalonia UI                     ── view state only
├── Local RPC endpoint + Hub client ── adapters
├── Cloud client (HTTP + realtime)  ── adapters
├── Application Services            ── the single write path
├── Domain                          ── pure
├── Infrastructure                  ── AOT-safe persistence, files, native adapters
└── In-process notifications        ── domain → projector → UI
```

The Generic Host owns, in one place: dependency injection, configuration and secret references, logging and telemetry, the local RPC endpoint and connection lifecycle, the cloud client lifecycles, database migration checks and recovery, native runtime initialisation, and orderly shutdown.

| # | Rule |
|---|---|
| PS-01 | **The Avalonia lifetime and the host lifetime are explicitly coordinated.** On shutdown the process **drains** first: stop accepting new remote write commands, wait for critical transactions to reach disk, then stop the local endpoint, then the realtime connection, then the native runtime. |
| PS-02 | **Each product process is autonomous.** Its native libraries run inside it; nothing is delegated to a separate long-lived worker process (`I3 §1.2`). |
| PS-03 | **One infrastructure component owns the local RPC connection lifecycle** (`§5` of the local IPC architecture). |

---

## 2. Native AOT constraints

| # | Rule |
|---|---|
| <a id="rule-ao-01"></a>AO-01 | **`PublishAot` on the executable; `IsAotCompatible` on every library it consumes** (**[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)**). |
| AO-02 | **XAML uses compiled bindings.** Runtime loading of arbitrary XAML is prohibited as a core path. |
| AO-03 | **Dependency injection uses explicit or generated registration.** "Scan the assembly and auto-register" is never an irreplaceable mechanism. |
| AO-04 | **No reflection-based service location, no dynamic proxies, no runtime code generation on the main path.** |
| AO-05 | **Assets are embedded resources with the framework's resource build action.** |
| AO-06 | **Built-in COM interop support is disabled where the UI framework requires it** for the version in use. |
| AO-07 | **Every third-party control is verified by a real AOT publish** before acceptance — the unbounded exposure identified by **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)**. *Owner: owning platform work-package owner. Trigger: before accepting any third-party control into an AOT deliverable.* |
| AO-08 | **Dynamic control creation, where genuinely needed, is declared in trimmer configuration** and covered by a publish test. |
| AO-09 | **Every desktop RID genuinely publishes an AOT package** and runs start-up, document-open, local RPC round-trip, cloud HTTP and realtime smoke tests. |
| AO-10 | **Trimming and AOT diagnostics are build-breaking**; blanket suppression is prohibited. |
| AO-11 | **`System.Linq.Expressions` always runs interpreted under AOT**, so it is never used on a hot path. |
| <a id="rule-ao-12"></a>AO-12 | **Generic instantiations are pre-generated**, so unbounded generic fan-out is avoided for artifact size. |

---

## 3. MVVM

| # | Rule |
|---|---|
| MV-01 | **A view model is view state, never a domain object.** |
| MV-02 | **A command binding calls a facade or application service** and nothing else. |
| MV-03 | **View models hold no database connection, no session, no native pointer, no `SafeHandle`.** |
| MV-04 | **Long-running work surfaces through a task projection**, never by blocking a command. |
| MV-05 | **Domain notifications pass through a view-state projector** before being marshalled to the UI thread. |
| MV-06 | **A remote modification produces the same projected update as a local one** ([LY-06](00-architecture-overview.md#rule-ly-06) in the overview). |
| MV-07 | **View models are not shared with mobile** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| MV-08 | **The shared design system and shell provide mechanism, never product domain** (`§15` of the shared desktop requirements). |

---

## 4. Threading

| # | Rule |
|---|---|
| TH-01 | **The UI thread performs layout, input and lightweight state application only.** |
| TH-02 | **CPU-bound work goes to a controlled scheduler.** Arbitrary background task creation that produces unbounded concurrency is prohibited. |
| TH-03 | **I/O is asynchronous end to end.** |
| TH-04 | **Native callbacks copy minimal metadata as early as possible** and hand off to a managed queue. |
| TH-05 | **Each document, timeline or capture session protects write ordering** with a serial mailbox or an async lock. |
| TH-06 | **Never wait on an RPC callback, the UI dispatcher, or a long native call while holding a domain lock.** |
| TH-07 | **Every channel has a capacity and an overflow policy.** |
| TH-08 | **A synchronous UI-thread block beyond the responsiveness threshold is a defect** ([RS-03](../requirements/12-quality-and-compatibility-contract.md#rule-rs-03) in the quality contract). |

---

## 5. Windows, sessions and instances

| # | Rule |
|---|---|
| WI-01 | **One process may own several windows; state is partitioned by document session.** |
| WI-02 | **One document has exactly one write authority at a time** ([WN-04](../requirements/09-shared-desktop-experience.md#rule-wn-04) in the shared desktop requirements). Several windows on one document share one session. |
| WI-03 | **Opening the same document from two processes requires an explicit lock, a read-only mode, or a coordination protocol** — never two silent writable copies. |
| WI-04 | **Start-up from a file association first attempts to route to a suitable existing instance** before creating a new one. |
| WI-05 | **`InstanceId` is unique per launch; `AppId` is stable** ([PM-07](00-architecture-overview.md#rule-pm-07) in the overview). |
| WI-06 | **Multi-window is the default capability; multi-process is an explicit extension** ([SI-21](../requirements/09-shared-desktop-experience.md#rule-si-21), [SI-22](../requirements/09-shared-desktop-experience.md#rule-si-22)). |
| WI-07 | **Window and layout physical state is device-local** ([SI-24](../requirements/09-shared-desktop-experience.md#rule-si-24)). |

---

## 6. Persistence inside the process

| # | Rule |
|---|---|
| PR-01 | **Local persistence uses an AOT-safe data access path** with explicit or generated mapping — not a reflection-driven ORM runtime as an irreplaceable dependency (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, `I3 §12.1`). |
| PR-02 | **Connection and transaction lifetimes follow the unit of work.** No global singleton connection. |
| PR-03 | **Write transactions are short.** |
| PR-04 | **Journaling mode is enabled only after platform and file-system validation.** |
| PR-05 | **Schema migration has its own versioning and a rollback or forward-recovery strategy** (`§6` of the data requirements). |
| PR-06 | **User documents and cache directories are separate.** |
| PR-07 | **Writable database files are never shared between products** ([P-09](../requirements/00-product-scope-and-portfolio.md#rule-p-09)). |
| PR-08 | **Serializers and mappers are statically generated or explicitly registered.** Runtime entity scanning is prohibited. |

Full local data structure is specified in [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md).

---

## 7. Journal, snapshot and recovery

| # | Rule |
|---|---|
| JR-01 | **The journal records the minimum needed to recover a confirmed command**: sequence, `CommandId`, previous and new revision, command type and version, payload or a durable reference, checksum, actor, correlation, causation and commit time. |
| JR-02 | **Durability is guaranteed before success is reported** to any caller — local UI, local RPC or HTTP. |
| JR-03 | **Notifications are emitted only after commit.** A lost notification never loses state; recovery is by revision and sequence. |
| JR-04 | **Snapshots are created by command count, elapsed time and size**, carry a schema version and a checksum, are written to a temporary file with an explicit flush policy and atomic replacement, and retain at least one verified previous generation. |
| JR-05 | **Caches are rebuildable and never enter a critical snapshot.** |
| JR-06 | **Recovery replays the journal from the most recent valid snapshot.** |

### 7.1 Recovery after a native crash

Because native libraries share the process, an access violation terminates the application — the failure boundary explicitly accepted when a separate worker process was rejected. The next start-up must:

1. Detect the abnormal-exit marker
2. Validate the last transaction and the journal
3. Recover to the last committed revision
4. **Quarantine the media, plug-in or operation that may have triggered the crash**
5. Present a recovery report and offer an optional diagnostic bundle
6. Re-register with the Hub and rebuild proxies
7. Re-establish the realtime session and query missing state over HTTP
8. **Never report unfinished work as successful**

**Crash-loop protection** enters a read-first Safe Start mode after repeated start-up failure, which never modifies canonical content and never deletes user data ([CR-06](../requirements/12-quality-and-compatibility-contract.md#rule-cr-06) in the quality contract).

---

## 8. Long-running work

| # | Rule |
|---|---|
| LT-01 | **Import, indexing, rendering, transcoding, model download, capture and cloud sync never run as a long-occupying RPC or HTTP request.** They return a `TaskHandle`. |
| LT-02 | **The task owner is the product that actually performs the work** ([OW-01](../requirements/05-ai-and-agent-execution.md#rule-ow-01) in the AI requirements). |
| LT-03 | **Task state is persisted** and, after a restart, is recovered, failed, or explicitly marked interrupted. |
| LT-04 | **Progress is a monotonic best estimate** ([PR-01](../requirements/05-ai-and-agent-execution.md#rule-pr-01) there). |
| LT-05 | **Local progress surfaces through local RPC events and queries; public progress goes over realtime**, with an HTTP query always available for compensation and final state. |
| LT-06 | **Cancellation is a request** ([CN-01](../requirements/05-ai-and-agent-execution.md#rule-cn-01) there). |
| LT-07 | **Task output uses a `ResourceRef`.** |
| LT-08 | **The Hub aggregates task summaries only** and never takes over execution state. |
| LT-09 | In-process background services and channel consumers are part of the host — never a reintroduced separate worker process. |

---

## 9. Cloud client inside the desktop

| # | Rule |
|---|---|
| CC-01 | **Each product owns its own cloud client** for its own data (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). ArcChat is not a proxy. |
| CC-02 | **The typed HTTP client uses the generated-only registration and entry point.** The reflection package is absent; its diagnostic is build-breaking (**[F-026](../assurance/open-gates-register.md#rule-f-026)**). |
| CC-03 | **One factory manages the HTTP client**, with the access token injected by a delegating handler and **token refresh serialised**. |
| CC-04 | **Timeout, cancellation and retry are explicit policies.** A write retry requires `CommandId` idempotency. |
| CC-05 | **Realtime reconnection uses exponential backoff with jitter**, then backfills gaps by sequence and revision over HTTP. |
| CC-06 | **Authorization headers and query tokens never appear in logs.** |
| CC-07 | **A local sync outbox is durable** ([SY-32](../requirements/03-cloud-services-and-sync.md#rule-sy-32) in the cloud requirements) and survives a crash immediately after save. |

---

## 10. Shared shell composition

The design system and desktop shell supply: semantic tokens, typography, iconography, density, motion, window and panel infrastructure, the command system, the settings framework, the attention and activity surfaces, error presentation, deep-link handling, drag-and-drop semantics, clipboard handling, the account surface, and lifecycle coordination.

| # | Rule |
|---|---|
| SH-01 | **The shell holds no product domain state** ([SI-28](../requirements/09-shared-desktop-experience.md#rule-si-28)). |
| SH-02 | **A product composes the shell; the shell never dictates the product's workspace layout** ([SI-01](../requirements/09-shared-desktop-experience.md#rule-si-01)). |
| SH-03 | **Every command, menu item, toolbar button, shortcut and palette entry resolves to one command identity** ([CM-02](../requirements/09-shared-desktop-experience.md#rule-cm-02)). |
| SH-04 | **Undo state belongs to the product** ([CM-06](../requirements/09-shared-desktop-experience.md#rule-cm-06)); the shell provides the command plumbing only. |

---

## 11. Start-up sequence

```
Process start
 → host construction, configuration, logging
 → open the local store; run the compatibility check (migrate only what is opened)
 → detect abnormal exit; run recovery if required
 → show the first window
 → reach a usable workspace                    ← the measured Time To Usable
 → [background] create the local endpoint; connect to the Hub; register
 → [background] restore the cloud session; refresh entitlement and policy
 → [background] resume sync; resume interrupted tasks; rebuild derived data
```

| # | Rule |
|---|---|
| SU-01 | **Nothing in the background column may block reaching a usable workspace** (`SU-01`–[SU-03](../requirements/12-quality-and-compatibility-contract.md#rule-su-03) in the quality contract). |
| SU-02 | **Start-up never waits for account, cloud, policy or a model catalogue.** |
| SU-03 | **Start-up never requires ArcChat to be online.** |
| SU-04 | Installation and shell launch require no account ([ID-01](../requirements/02-identity-account-and-workspace.md#rule-id-01) of the identity requirements). Cloud Notes enrolment, AI and continuity require sign-in; previously authorised hydrated content and pending edits retain their stated offline protections. ArcScope/ArcSlate native operations require neither Cloud enrolment nor a paid AI term. |

---

## 12. Shutdown sequence

```
Shutdown requested
 → stop accepting new remote write commands (Draining)
 → cancel or checkpoint cancellable work; let non-cancellable work reach a safe point
 → flush critical transactions to disk
 → unregister from the Hub; stop the local endpoint
 → close the realtime connection; drain the sync outbox opportunistically
 → shut down the native runtime
 → exit
```

**Closing a window is not quitting, and quitting is not stopping background work** ([LF-01](../requirements/09-shared-desktop-experience.md#rule-lf-01)). Where genuine work continues — a capture, a render — the product says so and offers a choice ([LF-04](../requirements/09-shared-desktop-experience.md#rule-lf-04)).

---

## 13. Product-specific host extensions

| Product | Additional host concerns |
|---|---|
| **ArcChat** | Hub hosting, agent runtime, capability registry, provider routing, tray/background mode, remote bridge connection |
| **ArcNotes** | Block editor infrastructure, link index, search index host, attachment store |
| **ArcScope** | Acquisition pipeline, ring buffers, decoder host, chunked capture store, real-time visualisation pipeline, device adapters |
| **ArcSlate** | Media runtime, decode and playback pipeline, audio clock, processing graph engine, proxy and cache managers, render queue |

Each is elaborated in its product requirements and in [`12-native-interop-and-media.md`](12-native-interop-and-media.md).

---

## 14. Performance architecture

| # | Rule |
|---|---|
| PF-01 | **Small DTOs are allocated normally; over-pooling is avoided.** |
| PF-02 | **Large buffers use pooled memory and are returned rigorously.** |
| PF-03 | **Native buffers are pinned only where necessary, for a bounded duration.** |
| PF-04 | **A large byte array never enters the state tree and is never repeatedly serialized.** |
| PF-05 | **Image, frame and analysis caches have a budget, an eviction policy and pressure feedback** ([MM-03](../requirements/12-quality-and-compatibility-contract.md#rule-mm-03) in the quality contract). |
| PF-06 | **Native memory enters the budget and the telemetry**; the managed heap alone is insufficient ([MM-01](../requirements/12-quality-and-compatibility-contract.md#rule-mm-01) there). |
| PF-07 | **`GC.Collect()` is never called repeatedly from business code.** |
| PF-08 | **Native AOT does not mean no garbage collector**; GC configuration follows measurement on the real runtime. |

---

## 15. Traceability

| Source | Consumed as |
|---|---|
| `I3 §9` | Desktop process structure, AOT constraints, MVVM, threading, multi-window and multi-instance |
| `I3 §10`, `§11`, `§12` | Document identity, write commands, conflicts, undo ownership, journal, snapshot and crash recovery |
| `I3 §13`, `§22` | Long task model; performance, memory and backpressure |
| `I4 §Stage 14` | Shared shell composition and lifecycle behaviour |
| `I4 §Stage 27` | Start-up, memory, responsiveness and recovery gates |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Desktop as a Native AOT deliverable with trim/AOT-safe dependencies |
| **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)** | Avalonia AOT requirements and the third-party control publish gate |
| **[F-026](../assurance/open-gates-register.md#rule-f-026)** | The typed HTTP client entry point and reflection-package prohibition |
