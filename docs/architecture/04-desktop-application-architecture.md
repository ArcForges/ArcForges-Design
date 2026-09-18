# Desktop Application Architecture

[P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) current implementation authorities: [Concrete Platform/product projects and lifetime](27-platform-projects-and-application-assistants.md); [Complete embedded assistant UX](../experience/01-embedded-assistant.md).

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
├── Own-app typed ports + Cloud client ── adapters
├── Cloud client (HTTP + realtime)  ── adapters
├── Application Services            ── the single write path
├── Domain                          ── pure
├── Infrastructure                  ── AOT-safe persistence, files, native adapters
└── In-process notifications        ── domain → projector → UI
```

The Generic Host owns, in one place: dependency injection, configuration and secret references, logging and telemetry, the local RPC endpoint and connection lifecycle, the cloud client lifecycles, database migration checks and recovery, native runtime initialisation, and orderly shutdown.

| # | Rule |
|---|---|
| <a id="rule-ps-01"></a>PS-01 | **The Avalonia lifetime and the host lifetime are explicitly coordinated.** On shutdown the process **drains** first: stop accepting new remote write commands, wait for critical transactions to reach disk, then stop the local endpoint, then the realtime connection, then the native runtime. |
| <a id="rule-ps-02"></a>PS-02 | **Each product process is autonomous.** Its native libraries run inside it; nothing is delegated to a separate long-lived worker process. |
| <a id="rule-ps-03"></a>PS-03 | **One infrastructure component owns the local RPC connection lifecycle** (`§5` of the local IPC architecture). |

---

## 2. Native AOT constraints

| # | Rule |
|---|---|
| <a id="rule-ao-01"></a>AO-01 | **`PublishAot` on the executable; `IsAotCompatible` on every library it consumes** (**[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)**). |
| <a id="rule-ao-02"></a>AO-02 | **XAML uses compiled bindings.** Runtime loading of arbitrary XAML is prohibited as a core path. |
| <a id="rule-ao-03"></a>AO-03 | **Dependency injection uses explicit or generated registration.** "Scan the assembly and auto-register" is never an irreplaceable mechanism. |
| <a id="rule-ao-04"></a>AO-04 | **No reflection-based service location, no dynamic proxies, no runtime code generation on the main path.** |
| <a id="rule-ao-05"></a>AO-05 | **Assets are embedded resources with the framework's resource build action.** |
| <a id="rule-ao-06"></a>AO-06 | **Built-in COM interop support is disabled where the UI framework requires it** for the version in use. |
| <a id="rule-ao-07"></a>AO-07 | **Every third-party control is verified by a real AOT publish** before acceptance — the unbounded exposure identified by **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)**. *Owner: owning platform work-package owner. Trigger: before accepting any third-party control into an AOT deliverable.* |
| <a id="rule-ao-08"></a>AO-08 | **Dynamic control creation, where genuinely needed, is declared in trimmer configuration** and covered by a publish test. |
| <a id="rule-ao-09"></a>AO-09 | **Every desktop RID genuinely publishes an AOT package** and runs start-up, document-open, local RPC round-trip, cloud HTTP and realtime smoke tests. |
| <a id="rule-ao-10"></a>AO-10 | **Trimming and AOT diagnostics are build-breaking**; blanket suppression is prohibited. |
| <a id="rule-ao-11"></a>AO-11 | **`System.Linq.Expressions` always runs interpreted under AOT**, so it is never used on a hot path. |
| <a id="rule-ao-12"></a>AO-12 | **Generic instantiations are pre-generated**, so unbounded generic fan-out is avoided for artifact size. |

---

## 3. MVVM

| # | Rule |
|---|---|
| <a id="rule-mv-01"></a>MV-01 | **A view model is view state, never a domain object.** |
| <a id="rule-mv-02"></a>MV-02 | **A command binding calls a facade or application service** and nothing else. |
| <a id="rule-mv-03"></a>MV-03 | **View models hold no database connection, no session, no native pointer, no `SafeHandle`.** |
| <a id="rule-mv-04"></a>MV-04 | **Long-running work surfaces through a task projection**, never by blocking a command. |
| <a id="rule-mv-05"></a>MV-05 | **Domain notifications pass through a view-state projector** before being marshalled to the UI thread. |
| <a id="rule-mv-06"></a>MV-06 | **A remote modification produces the same projected update as a local one** ([LY-06](00-architecture-overview.md#rule-ly-06) in the overview). |
| <a id="rule-mv-07"></a>MV-07 | **View models are not shared with mobile** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| <a id="rule-mv-08"></a>MV-08 | **The shared design system and shell provide mechanism, never product domain** (`§15` of the shared desktop requirements). |

---

## 4. Threading

| # | Rule |
|---|---|
| <a id="rule-th-01"></a>TH-01 | **The UI thread performs layout, input and lightweight state application only.** |
| <a id="rule-th-02"></a>TH-02 | **CPU-bound work goes to a controlled scheduler.** Arbitrary background task creation that produces unbounded concurrency is prohibited. |
| <a id="rule-th-03"></a>TH-03 | **I/O is asynchronous end to end.** |
| <a id="rule-th-04"></a>TH-04 | **Native callbacks copy minimal metadata as early as possible** and hand off to a managed queue. |
| <a id="rule-th-05"></a>TH-05 | **Each document, timeline or capture session protects write ordering** with a serial mailbox or an async lock. |
| <a id="rule-th-06"></a>TH-06 | **Never wait on an RPC callback, the UI dispatcher, or a long native call while holding a domain lock.** |
| <a id="rule-th-07"></a>TH-07 | **Every channel has a capacity and an overflow policy.** |
| <a id="rule-th-08"></a>TH-08 | **A synchronous UI-thread block beyond the responsiveness threshold is a defect** ([RS-03](../requirements/12-quality-and-compatibility-contract.md#rule-rs-03) in the quality contract). |

---

## 5. Windows, sessions and instances

| # | Rule |
|---|---|
| <a id="rule-wi-01"></a>WI-01 | **One process may own several windows; state is partitioned by document session.** |
| <a id="rule-wi-02"></a>WI-02 | **One document has exactly one write authority at a time** ([WN-04](../requirements/09-shared-desktop-experience.md#rule-wn-04) in the shared desktop requirements). Several windows on one document share one session. |
| <a id="rule-wi-03"></a>WI-03 | **Opening the same document from two processes requires an explicit lock, a read-only mode, or a coordination protocol** — never two silent writable copies. |
| <a id="rule-wi-04"></a>WI-04 | **Start-up from a file association first attempts to route to a suitable existing instance** before creating a new one. |
| <a id="rule-wi-05"></a>WI-05 | **`InstanceId` is unique per launch; `AppId` is stable** ([PM-07](00-architecture-overview.md#rule-pm-07) in the overview). |
| <a id="rule-wi-06"></a>WI-06 | **Multi-window is the default capability; multi-process is an explicit extension** ([SI-21](../requirements/09-shared-desktop-experience.md#rule-si-21), [SI-22](../requirements/09-shared-desktop-experience.md#rule-si-22)). |
| <a id="rule-wi-07"></a>WI-07 | **Window and layout physical state is device-local** ([SI-24](../requirements/09-shared-desktop-experience.md#rule-si-24)). |

---

## 6. Persistence inside the process

| # | Rule |
|---|---|
| <a id="rule-pr-01"></a>PR-01 | **Local persistence uses an AOT-safe data access path** with explicit or generated mapping — not a reflection-driven ORM runtime as an irreplaceable dependency (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| <a id="rule-pr-02"></a>PR-02 | **Connection and transaction lifetimes follow the unit of work.** No global singleton connection. |
| <a id="rule-pr-03"></a>PR-03 | **Write transactions are short.** |
| <a id="rule-pr-04"></a>PR-04 | **Journaling mode is enabled only after platform and file-system validation.** |
| <a id="rule-pr-05"></a>PR-05 | **Schema migration has its own versioning and a rollback or forward-recovery strategy** (`§6` of the data requirements). |
| <a id="rule-pr-06"></a>PR-06 | **User documents and cache directories are separate.** |
| <a id="rule-pr-07"></a>PR-07 | **Writable database files are never shared between products** ([P-09](../requirements/00-product-scope-and-portfolio.md#rule-p-09)). |
| <a id="rule-pr-08"></a>PR-08 | **Serializers and mappers are statically generated or explicitly registered.** Runtime entity scanning is prohibited. |

Full local data structure is specified in [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md).

---

## 7. Journal, snapshot and recovery

| # | Rule |
|---|---|
| <a id="rule-jr-01"></a>JR-01 | **The journal records the minimum needed to recover a confirmed command**: sequence, `CommandId`, previous and new revision, command type and version, payload or a durable reference, checksum, actor, correlation, causation and commit time. |
| <a id="rule-jr-02"></a>JR-02 | **Durability is guaranteed before success is reported** to any caller — local UI, local RPC or HTTP. |
| <a id="rule-jr-03"></a>JR-03 | **Notifications are emitted only after commit.** A lost notification never loses state; recovery is by revision and sequence. |
| <a id="rule-jr-04"></a>JR-04 | **Snapshots are created by command count, elapsed time and size**, carry a schema version and a checksum, are written to a temporary file with an explicit flush policy and atomic replacement, and retain at least one verified previous generation. |
| <a id="rule-jr-05"></a>JR-05 | **Caches are rebuildable and never enter a critical snapshot.** |
| <a id="rule-jr-06"></a>JR-06 | **Recovery replays the journal from the most recent valid snapshot.** |

### 7.1 Recovery after a native crash

Because native libraries share the process, an access violation terminates the application — the failure boundary explicitly accepted when a separate worker process was rejected. The next start-up must:

1. Detect the abnormal-exit marker
2. Validate the last transaction and the journal
3. Recover to the last committed revision
4. **Quarantine the media, plug-in or operation that may have triggered the crash**
5. Present a recovery report and offer an optional diagnostic bundle
6. Reopen this app's Cloud session/presence and recreate parent-owned helper channels
7. Re-establish the realtime session and query missing state over HTTP
8. **Never report unfinished work as successful**

**Crash-loop protection** enters a read-first Safe Start mode after repeated start-up failure, which never modifies canonical content and never deletes user data ([CR-06](../requirements/12-quality-and-compatibility-contract.md#rule-cr-06) in the quality contract).

---

## 8. Long-running work

| # | Rule |
|---|---|
| <a id="rule-lt-01"></a>LT-01 | **Import, indexing, rendering, transcoding, model download, capture and cloud sync never run as a long-occupying RPC or HTTP request.** They return a `TaskHandle`. |
| <a id="rule-lt-02"></a>LT-02 | **The task owner is the product that actually performs the work** ([OW-01](../requirements/05-ai-and-agent-execution.md#rule-ow-01) in the AI requirements). |
| <a id="rule-lt-03"></a>LT-03 | **Task state is persisted** and, after a restart, is recovered, failed, or explicitly marked interrupted. |
| <a id="rule-lt-04"></a>LT-04 | **Progress is a monotonic best estimate** ([PR-01](../requirements/05-ai-and-agent-execution.md#rule-pr-01) there). |
| <a id="rule-lt-05"></a>LT-05 | **Local progress surfaces through local RPC events and queries; public progress goes over realtime**, with an HTTP query always available for compensation and final state. |
| <a id="rule-lt-06"></a>LT-06 | **Cancellation is a request** ([CN-01](../requirements/05-ai-and-agent-execution.md#rule-cn-01) there). |
| <a id="rule-lt-07"></a>LT-07 | **Task output uses a `ResourceRef`.** |
| <a id="rule-lt-08"></a>LT-08 | **The assistant presents its own application's task projections.** It never takes over authoritative execution state or aggregates another product's task store. |
| <a id="rule-lt-09"></a>LT-09 | In-process background services and channel consumers are part of the host — never a reintroduced separate worker process. |

---

## 9. Cloud client inside the desktop

| # | Rule |
|---|---|
| <a id="rule-cc-01"></a>CC-01 | **Each product owns its own cloud client** for its own data (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). ArcChat is not a proxy. |
| <a id="rule-cc-02"></a>CC-02 | Consume released generated gRPC-Web clients with explicit registration and AOT-compatible serializers. Source-generated typed HTTP adapters are limited to the declared exceptions; [F-026](../assurance/open-gates-register.md#rule-f-026) proves the actual closure. |
| <a id="rule-cc-03"></a>CC-03 | **One factory manages the HTTP client**, with the access token injected by a delegating handler and **token refresh serialised**. |
| <a id="rule-cc-04"></a>CC-04 | **Timeout, cancellation and retry are explicit policies.** A write retry requires `CommandId` idempotency. |
| <a id="rule-cc-05"></a>CC-05 | **Realtime reconnection uses exponential backoff with jitter**, then backfills gaps by sequence and revision over HTTP. |
| <a id="rule-cc-06"></a>CC-06 | **Authorization headers and query tokens never appear in logs.** |
| <a id="rule-cc-07"></a>CC-07 | **A local sync outbox is durable** ([SY-32](../requirements/03-cloud-services-and-sync.md#rule-sy-32) in the cloud requirements) and survives a crash immediately after save. |

---

## 10. Shared shell composition

The design system and desktop shell supply: semantic tokens, typography, iconography, density, motion, window and panel infrastructure, the command system, the settings framework, the attention and activity surfaces, error presentation, deep-link handling, drag-and-drop semantics, clipboard handling, the account surface, and lifecycle coordination.

| # | Rule |
|---|---|
| <a id="rule-sh-01"></a>SH-01 | **The shell holds no product domain state** ([SI-28](../requirements/09-shared-desktop-experience.md#rule-si-28)). |
| <a id="rule-sh-02"></a>SH-02 | **A product composes the shell; the shell never dictates the product's workspace layout** ([SI-01](../requirements/09-shared-desktop-experience.md#rule-si-01)). |
| <a id="rule-sh-03"></a>SH-03 | **Every command, menu item, toolbar button, shortcut and palette entry resolves to one command identity** ([CM-02](../requirements/09-shared-desktop-experience.md#rule-cm-02)). |
| <a id="rule-sh-04"></a>SH-04 | **Undo state belongs to the product** ([CM-06](../requirements/09-shared-desktop-experience.md#rule-cm-06)); the shell provides the command plumbing only. |

---

## 11. Start-up sequence

```
Process start
 → host construction, configuration, logging
 → open the local store; run the compatibility check (migrate only what is opened)
 → detect abnormal exit; run recovery if required
 → show the first window
 → reach a usable workspace                    ← the measured Time To Usable
 → [background] connect this app to Cloud; register its own presence; start required private helpers
 → [background] restore the cloud session; refresh entitlement and policy
 → [background] resume sync; resume interrupted tasks; rebuild derived data
```

| # | Rule |
|---|---|
| <a id="rule-su-01"></a>SU-01 | **Nothing in the background column may block reaching a usable workspace** ([`SU-01`](../requirements/12-quality-and-compatibility-contract.md#rule-su-01)–[SU-03](../requirements/12-quality-and-compatibility-contract.md#rule-su-03) in the quality contract). |
| <a id="rule-su-02"></a>SU-02 | **Start-up never waits for account, cloud, policy or a model catalogue.** |
| <a id="rule-su-03"></a>SU-03 | **Start-up never requires ArcChat to be online.** |
| <a id="rule-su-04"></a>SU-04 | Installation and shell launch require no account ([ID-01](../requirements/02-identity-account-and-workspace.md#rule-id-01) of the identity requirements). Cloud Notes enrolment, AI and continuity require sign-in; previously authorised hydrated content and pending edits retain their stated offline protections. ArcScope/ArcSlate native operations require neither Cloud enrolment nor a paid AI term. |

---

## 12. Shutdown sequence

```
Shutdown requested
 → stop accepting new remote write commands (Draining)
 → cancel or checkpoint cancellable work; let non-cancellable work reach a safe point
 → flush critical transactions to disk
 → disconnect this app's presence; stop owned helper endpoints
 → close the realtime connection; drain the sync outbox opportunistically
 → shut down the native runtime
 → exit
```

**Closing a window is not quitting, and quitting is not stopping background work** ([LF-01](../requirements/09-shared-desktop-experience.md#rule-lf-01)). Where genuine work continues — a capture, a render — the product says so and offers a choice ([LF-04](../requirements/09-shared-desktop-experience.md#rule-lf-04)).

---

## 13. Product-specific host extensions

| Product | Additional host concerns |
|---|---|
| **Embedded assistant** | Own-app chat/task/project/automation/approval/context UI, local or Cloud history, independent Cloud connection and device bridge; all packaged by DesktopPlatform |
| **ArcNotes** | Block editor infrastructure, link index, search index host, attachment store |
| **ArcScope** | Acquisition pipeline, ring buffers, decoder host, chunked capture store, real-time visualisation pipeline, device adapters |
| **ArcSlate** | Media runtime, decode and playback pipeline, audio clock, processing graph engine, proxy and cache managers, render queue |

Each is elaborated in its product requirements and in [`12-native-interop-and-media.md`](12-native-interop-and-media.md).

---

## 14. Performance architecture

| # | Rule |
|---|---|
| <a id="rule-pf-01"></a>PF-01 | **Small DTOs are allocated normally; over-pooling is avoided.** |
| <a id="rule-pf-02"></a>PF-02 | **Large buffers use pooled memory and are returned rigorously.** |
| <a id="rule-pf-03"></a>PF-03 | **Native buffers are pinned only where necessary, for a bounded duration.** |
| <a id="rule-pf-04"></a>PF-04 | **A large byte array never enters the state tree and is never repeatedly serialized.** |
| <a id="rule-pf-05"></a>PF-05 | **Image, frame and analysis caches have a budget, an eviction policy and pressure feedback** ([MM-03](../requirements/12-quality-and-compatibility-contract.md#rule-mm-03) in the quality contract). |
| <a id="rule-pf-06"></a>PF-06 | **Native memory enters the budget and the telemetry**; the managed heap alone is insufficient ([MM-01](../requirements/12-quality-and-compatibility-contract.md#rule-mm-01) there). |
| <a id="rule-pf-07"></a>PF-07 | **`GC.Collect()` is never called repeatedly from business code.** |
| <a id="rule-pf-08"></a>PF-08 | **Native AOT does not mean no garbage collector**; GC configuration follows measurement on the real runtime. |

---

## 15. Traceability

| Current document | Relationship |
|---|---|
| [Shared Desktop Experience Requirements](../requirements/09-shared-desktop-experience.md) | Owns the shared native user experience |
| [Working Data, Project Formats and Cloud Portability Requirements](../requirements/13-data-formats-and-portability.md) | Owns persistence, undo, recovery and format obligations |
| [Product Quality and Compatibility Contract](../requirements/12-quality-and-compatibility-contract.md) | Owns startup, responsiveness, memory and recovery acceptance |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Desktop as a Native AOT deliverable with trim/AOT-safe dependencies |
| **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)** | Avalonia AOT requirements and the third-party control publish gate |
| **[F-026](../assurance/open-gates-register.md#rule-f-026)** | The typed HTTP client entry point and reflection-package prohibition |
