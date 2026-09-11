<a id="rule-wp-06"></a>

# WP-06 — AOT, RN, CF and Real Artifact Publish Proof

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `03`, `04`, `05` · Downstream: `07`, `08`, `10`, `12`, `13`, `17`, `30`

> **Goal.** Prove the runtime matrix on real published artifacts, not on intentions. Every desktop product publishes Native AOT and launches; Cloud publishes Native AOT and runs its full pipeline; the React application builds into production browser assets. Until this holds, every downstream design choice is a hypothesis.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform, Contracts, Cloud, AI, Web, Mobile. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** A minimal but *real* deliverable per target that publishes with the production posture and runs: a desktop host with the real contract set and local RPC attach, a cloud host with its real pipeline order, a production React application with a generated TypeScript SDK call, and the toolchain evidence for each.

**Out of scope.** Product features. UI beyond what is required to prove a window opens and a command runs. Full mobile business features; this package includes the minimal selected RN/Hermes transport/native-module proof before WP30.

**Why this package exists.** [QI-02](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-02) states plainly that a JIT test pass is not AOT compatibility. **[V-05](../../assurance/phase-1-official-verification.md#rule-v-05)** left several dependency-level questions open precisely because they can only be answered by a real publish. This is where they are answered.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** | The runtime matrix being proven |
| **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-05a](../../assurance/phase-1-official-verification.md#rule-v-05a)**–**[V-05e](../../assurance/phase-1-official-verification.md#rule-v-05e)** | The specific evidence obligations and their gates |
| [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md) `§3` | The publish matrix and its verification obligations |
| [`../../architecture/04-desktop-application-architecture.md`](../../architecture/04-desktop-application-architecture.md) `§2` | Desktop AOT constraints [AO-01](../../architecture/04-desktop-application-architecture.md#rule-ao-01)–[AO-12](../../architecture/04-desktop-application-architecture.md#rule-ao-12) |
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§1`, `§3` | The selected Cloud AOT closure and host pipeline order |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04), [WP-05](05-architecture-and-repository-policy-tests.md#rule-wp-05) output | Real contracts, real primitives, and policy tests that keep the proof true |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Desktop products are Native AOT deliverables** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| BR-02 | **Cloud is ASP.NET Core Native AOT with explicit session/SQL/HTTP adapters and zero publish diagnostics** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). |
| BR-03 | Web produces React/TypeScript browser assets with the pinned Node/npm build; no .NET WASM/AOT flags apply. |
| BR-04 | **Zero trim and AOT diagnostics on the AOT path.** A suppressed diagnostic is not a pass ([PJ-08](../../architecture/01-solution-and-project-layout.md#rule-pj-08)). |
| BR-05 | **A debug build passing is never evidence for a release target** ([PM-01](../../architecture/14-build-packaging-and-release.md#rule-pm-01) in the build architecture). |
| BR-06 | **The proof is continuous**, re-run on every main-branch build ([PM-02](../../architecture/14-build-packaging-and-release.md#rule-pm-02) there), not a one-off milestone. |
| BR-07 | **Every third-party control entering an AOT deliverable requires its own publish proof** (**[V-05a](../../assurance/phase-1-official-verification.md#rule-v-05a)**). |
| BR-08 | Generated native gRPC clients and explicit HTTP-exception adapters must pass their real AOT dependency/registration gate; browser/RN use their selected generated TS closure. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Desktop/` | Minimal AOT-publishable host: window, one command, local RPC attach, cloud client construction |
| `src/ArcNotes/ArcNotes.Desktop/`, `src/ArcScope/ArcScope.Desktop/`, `src/ArcSlate/ArcSlate.Desktop/` | Equivalent minimal AOT-publishable hosts |
| `src/Cloud/ArcForges.Cloud.Host/` | Minimal host running the real pipeline order with a health endpoint and one contract endpoint |
| `src/Web/ArcForges.Web.App/` | Minimal React browser application making one typed client call |
| `tests/LocalRpcAotTests/` | Extended: attach, invoke and detach against a published AOT binary |
| `tests/ReleaseArtifactTests/` | Extended: published-artifact launch and posture inspection |
| `eng/verification/` | The publish proof scripts and their evidence output |
| CI | AOT publish added to the main-branch pipeline for all four desktop products |

---

## 5. Required implementation work

<a id="rule-wp-06.00"></a>

### WP-06.00 — Desktop AOT publish

**What must be fully done.** Each desktop host publishes Native AOT for every supported runtime identifier with zero trim, AOT and single-file diagnostics. The published binary launches, opens a window, executes one command through the real application service path, and shuts down cleanly. No machine-installed runtime is required.

**Testing requirements.** A publish log per RID with a zero-diagnostic assertion; a launch smoke test executed against the published artifact on each platform; a clean-machine test confirming no runtime prerequisite.

**Completion gate.** All four hosts publish AOT with zero diagnostics and launch on every supported platform.

<a id="rule-wp-06.01"></a>

### WP-06.01 — Local RPC under AOT


**What must be fully done.** Publish two AOT desktop probe processes using the selected Kestrel HTTP/2 named-pipe/UDS listeners and client ConnectCallback. Authenticate same-user peers, complete LocalBootstrap, register both endpoint directions, invoke generated services, cancel, disconnect and reattach.

**Testing requirements.** Actual Windows/Linux/macOS process-to-process runs with malformed input, unauthorized peer and bounded resource tests.

**Completion gate.** [VG-04](../../assurance/open-gates-register.md#rule-vg-04) is supported by working generated gRPC over the exact local OS transports, not an in-memory or TCP substitute.

<a id="rule-wp-06.02"></a>

### WP-06.02 — Generated gRPC client under AOT


**What must be fully done.** From a published AOT desktop binary consume the actual released generated native gRPC client and source-generated HTTP-exception adapters against the AOT Cloud probe. Verify explicit registration, opaque native session handler, deadlines/status/details and exact primitive values.

**Testing requirements.** Real TLS call, negative dynamic/reflection dependency check, invalid protocol response, expiry/refresh and supported contract vectors.

**Completion gate.** [F-026](../../assurance/open-gates-register.md#rule-f-026) passes on the actual generated-client AOT closure.

<a id="rule-wp-06.03"></a>

### WP-06.03 — Realtime under AOT


**What must be fully done.** From the AOT probe use EventService.Poll with scoped cursor initialization, bounded event pages and snapshot/backfill. Drop connections, expire the cursor and revoke scope; verify current authoritative reads recover hints.

**Testing requirements.** Actual host reconnect/reset/duplicate/out-of-order and revoked-session runs.

**Completion gate.** Generated unary hints and durable reads work under AOT; no SignalR dependency or claimed hint durability.

<a id="rule-wp-06.04"></a>

### WP-06.04 — Cloud Native AOT publish


**What must be fully done.** Publish the single Native AOT Cloud OCI image with the selected Linux base, Npgsql/SQL and explicit session/WebAuthn/OIDC/HTTP adapters. Run real PostgreSQL migrations, transaction/outbox/lease and auth/CSRF/revoke probes. Deploy the exact CF Worker/Workflow/DO bindings and R2 test buckets, use reachable authenticated C# callback ports and exercise one bounded model intent/outcome and one staged/verified object. Measure the admitted verifier envelope.

**Testing requirements.** Zero AOT/trim diagnostics; pipeline order, cookie/native auth and WebAuthn proof vectors under published code; real DB/CF/R2/lease-loss and provider version acknowledgement.

**Completion gate.** [VG-06](../../assurance/open-gates-register.md#rule-vg-06) foundation proof covers the entire selected dependency closure and deployed provider boundary; no full product Harness claim is made.

<a id="rule-wp-06.05"></a>

### WP-06.05 — React production build and generated SDK proof


**What must be fully done.** Build minimal Account/Chat production React profiles from Web root locks and exact released generated gRPC-Web SDK. Call the actual AOT probe through same-origin routing/cookie/CSRF and exercise exact values, typed failures, cancellation and CF authenticated presentation. Measure existing asset/interaction budgets; prove own esproj and portable npm entry points.

**Testing requirements.** Production browser round trips with real AOT host and deployed CF, no frontend dev server or handwritten DTO; malformed frame/status, session expiry and asset/CSP checks.

**Completion gate.** The foundation contributes real [PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence; production identity/business/checkout remain their scheduled packages.

<a id="rule-wp-06.06"></a>

### WP-06.06 — Third-party control gate

**What must be fully done.** The process for admitting a third-party control into an AOT deliverable is established: a candidate control is added to a probe host, published AOT, and required to produce zero diagnostics before adoption. The process is recorded and the first candidate is evaluated through it.

**Testing requirements.** The probe publish log for the first candidate.

**Completion gate.** The process exists and has been exercised once. **This schedules [VG-03](../../assurance/open-gates-register.md#rule-vg-03) for `10`.**

---

<a id="rule-wp-06.07"></a>
### WP-06.07 — RN native and transport foundation proof

**What must be fully done.** Before producing the first Mobile artifact, enumerate and clear the exact Apache npm/Gradle/native public closure under [F-023](../../assurance/open-gates-register.md#rule-f-023). Build the pinned RN/Hermes arm64 release probe and run native navigation, OP-SQLite atomic write/reopen, secure storage, passkey result binding and the generated unary gRPC-Web adapter on a physical Android device. Call the actual AOT host, handle trailers/status/cancellation and bigint; authenticate the CF first-frame nonce and recover after process death. Record iOS as deferred.

**Testing requirements.** Dependency/source/NOTICE closure and prohibited-import negatives precede build; real artifact/device/protocol/native-adapter results follow it. CF and Cloud identities match the candidate manifest; no mock closes this proof.

**Completion gate.** First-artifact [F-023](../../assurance/open-gates-register.md#rule-f-023), selected RN/Hermes/native compatibility and actual AOT/CF transport proofs exist before WP30 starts. Product feature and final store gates remain WP31/WP32.

<a id="rule-wp-06.90"></a>
### WP-06.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Prove actual candidate NuGet restore/native loading and desktop AOT; C# AOT gRPC/gRPC-Web plus selected auth/storage/SQL adapters; RN/Hermes generated-client calls; React client calls; a minimal deployed CF ↔ reachable C# ↔ R2 chain. This is a bounded foundation probe, not the full [WP-52](52-cloud-harness.md#rule-wp-52) Harness.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Published binaries/artifacts run in clean consumer environments; no JIT exemption, SignalR or production Node sidecar. Record real CF and native/device evidence separately from fixtures. Selected adapters work without losing exact values.

**Completion gate.** Published binaries/artifacts run in clean consumer environments; no JIT exemption, SignalR or production Node sidecar. Record real CF and native/device evidence separately from fixtures. Selected adapters work without losing exact values. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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
| Per-RID AOT publish logs with zero-diagnostic assertions | [WP-06.00](#rule-wp-06.00) |
| Cross-process AOT RPC integration results | [WP-06.01](#rule-wp-06.01) |
| Dependency-graph and negative build-test results for the typed client | [WP-06.02](#rule-wp-06.02) |
| AOT realtime reconnection results | [WP-06.03](#rule-wp-06.03) |
| Cloud image build, pipeline order and integration results | [WP-06.04](#rule-wp-06.04) |
| production Web build, load and bundle baseline | [WP-06.05](#rule-wp-06.05) |
| Third-party control probe log | [WP-06.06](#rule-wp-06.06) |
| Pre-artifact Apache closure and RN/device/native/CF proof | [WP-06.07](#rule-wp-06.07) |

---

## 8. Completion gate

**Runtime/closure producers.** [VG-06](../../assurance/open-gates-register.md#rule-vg-06) through [WP-06.04](#rule-wp-06.04); [VG-07](../../assurance/open-gates-register.md#rule-vg-07) through [WP-06.07](#rule-wp-06.07); [F-023](../../assurance/open-gates-register.md#rule-f-023) through [WP-06.07](#rule-wp-06.07). The named candidate must supply actual passing evidence; documentation does not close these gates.

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-06.90](#rule-wp-06.90) and all inherited domain-specific gates must pass on the same candidate closure. Published binaries/artifacts run in clean consumer environments; no JIT exemption, SignalR or production Node sidecar. Record real CF and native/device evidence separately from fixtures. Selected adapters work without losing exact values.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-06.05](#rule-wp-06.05) — Production Web foundation artifacts, generated SDK/exact values and IDE/portable CLI proof; this is the foundation contribution only. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. All four desktop hosts publish Native AOT with zero trim, AOT and single-file diagnostics, and launch on every supported platform without a machine-installed runtime.
2. Bidirectional local RPC works between two published AOT binaries with generated proxies — satisfying [VG-04](../../assurance/open-gates-register.md#rule-vg-04).
3. A published AOT binary makes a generated gRPC call with the selected explicit AOT-compatible adapters — satisfying [F-026](../../assurance/open-gates-register.md#rule-f-026).
4. Realtime connects, receives, disconnects and reconnects with sequence backfill from a published AOT binary.
5. The cloud host publishes and runs Native AOT with explicit adapters and zero trim/AOT diagnostics.
6. Production React assets load and call the real C# probe through the generated TS SDK with exact-value vectors, Windows/CLI workflow evidence and recorded budgets.
7. The third-party control admission process exists and has been exercised once.
8. The selected RN/Hermes release probe passes first-artifact closure and actual device/service/native-adapter tests.
9. All of the above run on every main-branch build, not once.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [03 contract foundation and licence split](03-contract-foundation-and-licence-split.md#rule-wp-03)
- [04 identity error and versioning primitives](04-identity-error-and-versioning-primitives.md#rule-wp-04)
- [05 architecture and repository policy tests](05-architecture-and-repository-policy-tests.md#rule-wp-05)

**Downstream — consumers of these released outputs.**

- [07 local persistence foundation](07-local-persistence-foundation.md#rule-wp-07)
- [08 local ipc and registration](08-local-ipc-and-registration.md#rule-wp-08)
- [10 design system and desktop shell](10-design-system-and-desktop-shell.md#rule-wp-10)
- [12 observability foundation](12-observability-foundation.md#rule-wp-12)
- [13 high risk technical probes](13-high-risk-technical-probes.md#rule-wp-13)
- [17 arcchat independent core](17-arcchat-independent-core.md#rule-wp-17)
- [30 mobile shared architecture](30-mobile-shared-architecture.md#rule-wp-30)

---
