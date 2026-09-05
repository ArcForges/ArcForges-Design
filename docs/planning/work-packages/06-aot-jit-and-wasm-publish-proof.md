# WP-06 — AOT, JIT and WebAssembly Publish Proof

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `03`, `04`, `05` · Downstream: `07`, `08`, `10`, `12`, `13`

> **Goal.** Prove the runtime matrix on real published artifacts, not on intentions. Every desktop product publishes Native AOT and launches; Cloud publishes JIT and runs its full pipeline; the web application publishes to WebAssembly. Until this holds, every downstream design choice is a hypothesis.

---

## 1. Scope and purpose

**In scope.** A minimal but *real* deliverable per target that publishes with the production posture and runs: a desktop host with the real contract set and local RPC attach, a cloud host with its real pipeline order, a WebAssembly application with a real typed client call, and the toolchain evidence for each.

**Out of scope.** Product features. UI beyond what is required to prove a window opens and a command runs. The mobile targets — Android's proof is `30`/`32`, because it depends on the mobile boundary that does not exist yet.

**Why this package exists.** `QI-02` states plainly that a JIT test pass is not AOT compatibility. **V-05** left several dependency-level questions open precisely because they can only be answered by a real publish. This is where they are answered.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| **D-008** | The runtime matrix being proven |
| **V-03**, **V-05a**–**V-05e** | The specific evidence obligations and their gates |
| [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md) `§3` | The publish matrix and its verification obligations |
| [`../../architecture/04-desktop-application-architecture.md`](../../architecture/04-desktop-application-architecture.md) `§2` | Desktop AOT constraints `AO-01`–`AO-12` |
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§1`, `§3` | The JIT decision and the host pipeline order |
| `WP-03`, `WP-04`, `WP-05` output | Real contracts, real primitives, and policy tests that keep the proof true |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Desktop products are Native AOT deliverables** (**D-008**). |
| BR-02 | **Cloud is ASP.NET Core JIT. Strict AOT is explicitly not required and must not be attempted for consistency** (**D-008**, **V-03**). |
| BR-03 | **The web application publishes with AOT compilation disabled** unless a measured benchmark and an explicit decision prove otherwise (**D-007**). |
| BR-04 | **Zero trim and AOT diagnostics on the AOT path.** A suppressed diagnostic is not a pass (`PJ-08`). |
| BR-05 | **A debug build passing is never evidence for a release target** (`PM-01` in the build architecture). |
| BR-06 | **The proof is continuous**, re-run on every main-branch build (`PM-02` there), not a one-off milestone. |
| BR-07 | **Every third-party control entering an AOT deliverable requires its own publish proof** (**V-05a**). |
| BR-08 | **The reflection package of the typed HTTP client is absent and its generator diagnostic is build-breaking** (**F-026**). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Desktop/` | Minimal AOT-publishable host: window, one command, local RPC attach, cloud client construction |
| `src/ArcNotes/ArcNotes.Desktop/`, `src/ArcScope/ArcScope.Desktop/`, `src/ArcSlate/ArcSlate.Desktop/` | Equivalent minimal AOT-publishable hosts |
| `src/Cloud/ArcForges.Cloud.Host/` | Minimal host running the real pipeline order with a health endpoint and one contract endpoint |
| `src/Web/ArcForges.Web.App/` | Minimal WebAssembly application making one typed client call |
| `tests/LocalRpcAotTests/` | Extended: attach, invoke and detach against a published AOT binary |
| `tests/ReleaseArtifactTests/` | Extended: published-artifact launch and posture inspection |
| `eng/verification/` | The publish proof scripts and their evidence output |
| CI | AOT publish added to the main-branch pipeline for all four desktop products |

---

## 5. Required implementation work

### WP-06.00 — Desktop AOT publish

**What must be fully done.** Each desktop host publishes Native AOT for every supported runtime identifier with zero trim, AOT and single-file diagnostics. The published binary launches, opens a window, executes one command through the real application service path, and shuts down cleanly. No machine-installed runtime is required.

**Testing requirements.** A publish log per RID with a zero-diagnostic assertion; a launch smoke test executed against the published artifact on each platform; a clean-machine test confirming no runtime prerequisite.

**Completion gate.** All four hosts publish AOT with zero diagnostics and launch on every supported platform.

### WP-06.01 — Local RPC under AOT

**What must be fully done.** Two published AOT binaries attach over the real transport using generated proxies and the binary formatter, invoke a contract method in both directions, propagate cancellation, and detach cleanly. No reflection-based marshalling is involved.

**Testing requirements.** An AOT-published integration test covering attach, bidirectional invoke, cancellation, disconnect and reattach; the policy test from `WP-05.03` asserting the generated-shape attribute.

**Completion gate.** Bidirectional RPC works between two published AOT binaries. **This satisfies `VG-04`.**

### WP-06.02 — Typed HTTP client under AOT

**What must be fully done.** The typed HTTP client is exercised from a published AOT desktop binary against the cloud host, using the generated-only registration path. The reflection package is absent from the dependency graph and its generator diagnostic is build-breaking. The client version is pinned deliberately.

**Testing requirements.** A dependency-graph assertion; a negative build test proving the diagnostic breaks the build; an AOT-published call against the real host.

**Completion gate.** A published AOT binary makes a successful typed call with no reflection path present. **This satisfies `F-026`.**

### WP-06.03 — Realtime under AOT

**What must be fully done.** A published AOT desktop binary connects to the cloud realtime endpoint using the text protocol with source-generated payload metadata, receives a message, survives a disconnect, and reconnects with sequence backfill over HTTP.

**Testing requirements.** An AOT-published reconnection test with an induced disconnect and a sequence gap.

**Completion gate.** Realtime works from a published AOT binary including reconnection. **This closes the stale corpus claim that realtime is unsupported under AOT, consistent with V-03.**

### WP-06.04 — Cloud JIT publish

**What must be fully done.** The cloud host publishes as a container image running the real pipeline order, serves a health endpoint and one contract endpoint, and connects to a real database and a real object store in the integration environment. **No AOT publish is attempted.**

**Testing requirements.** An image build and run test; a pipeline-order assertion test; an integration test against real dependencies.

**Completion gate.** The cloud host runs its real pipeline and serves a contract endpoint, with the JIT posture explicit and no AOT properties present.

### WP-06.05 — WebAssembly publish

**What must be fully done.** The web application publishes to WebAssembly with AOT compilation disabled, loads in a browser, and makes one typed client call using source-generated serialization. Initial bundle size is measured and recorded as the first budget baseline.

**Testing requirements.** A publish and load test; a typed call test; a recorded bundle size measurement.

**Completion gate.** The application publishes, loads and calls successfully, and a bundle baseline exists.

### WP-06.06 — Third-party control gate

**What must be fully done.** The process for admitting a third-party control into an AOT deliverable is established: a candidate control is added to a probe host, published AOT, and required to produce zero diagnostics before adoption. The process is recorded and the first candidate is evaluated through it.

**Testing requirements.** The probe publish log for the first candidate.

**Completion gate.** The process exists and has been exercised once. **This schedules `VG-03` for `10`.**

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Confirms the cloud data path works against real infrastructure |
| Protocol | Confirms local RPC, typed HTTP and realtime all work under their production runtime posture |
| UI | Confirms the desktop shell can be AOT-published at all — the single largest platform risk |
| Security | None directly |
| Platform | This package *is* the platform risk retirement for the runtime matrix |
| Migration | None |
| Compatibility | Establishes the published-artifact verification pattern every release gate reuses |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Per-RID AOT publish logs with zero-diagnostic assertions | `WP-06.00` |
| Cross-process AOT RPC integration results | `WP-06.01` |
| Dependency-graph and negative build-test results for the typed client | `WP-06.02` |
| AOT realtime reconnection results | `WP-06.03` |
| Cloud image build, pipeline order and integration results | `WP-06.04` |
| WebAssembly publish, load and bundle baseline | `WP-06.05` |
| Third-party control probe log | `WP-06.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. All four desktop hosts publish Native AOT with zero trim, AOT and single-file diagnostics, and launch on every supported platform without a machine-installed runtime.
2. Bidirectional local RPC works between two published AOT binaries with generated proxies — satisfying `VG-04`.
3. A published AOT binary makes a typed HTTP call with the reflection package absent and its diagnostic build-breaking — satisfying `F-026`.
4. Realtime connects, receives, disconnects and reconnects with sequence backfill from a published AOT binary.
5. The cloud host publishes and runs JIT with its real pipeline order and no AOT properties.
6. The web application publishes to WebAssembly, loads, makes a typed call, and has a recorded bundle baseline.
7. The third-party control admission process exists and has been exercised once.
8. All of the above run on every main-branch build, not once.

---

## 9. Dependencies

**Upstream.** `03` (real contracts), `04` (primitives that must survive trimming), `05` (policy tests that keep the proof true).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `07` — Persistence | A proven AOT host to run the store inside |
| `08` — Local IPC | The proven transport and formatter posture |
| `10` — Design system | The AOT control admission process |
| `12` — Observability | A proven host to instrument |
| `13` — Probes | A platform whose runtime risk is already retired |
| Every later package | The knowledge that the runtime matrix is real |
