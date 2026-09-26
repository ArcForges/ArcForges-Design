<a id="rule-wp-06"></a>

# WP-06 — AOT, Android, CF and Real Artifact Publish Proof

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Prove the runtime matrix on real published artifacts, not on intentions. Every desktop product publishes Native AOT and launches; Cloud publishes Native AOT and runs its full pipeline; the React application builds into production browser assets. Until this holds, every downstream design choice is a hypothesis.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform, Contracts, Cloud, AI, Web, Mobile. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** A minimal but *real* deliverable per target that publishes with the production posture and runs: a desktop host with the real contract set and local RPC attach, a cloud host with its real pipeline order, a production React application with a generated TypeScript SDK call, and the toolchain evidence for each.

**Out of scope.** Product features. UI beyond what is required to prove a window opens and a command runs. Full mobile business features; this package includes the minimal selected Kotlin/Jetpack Compose transport/native-module proof before WP30.

**Why this package exists.** [QI-02](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-02) states plainly that a JIT test pass is not AOT compatibility. **[V-05](../../assurance/phase-1-official-verification.md#rule-v-05)** left several dependency-level questions open precisely because they can only be answered by a real publish. This is where they are answered.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


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

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Desktop products are Native AOT deliverables** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| <a id="rule-br-02"></a>BR-02 | **Cloud is ASP.NET Core Native AOT with explicit session/SQL/HTTP adapters and zero publish diagnostics** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). |
| <a id="rule-br-03"></a>BR-03 | Web produces React/TypeScript browser assets with the pinned Node/npm build; no .NET WASM/AOT flags apply. |
| <a id="rule-br-04"></a>BR-04 | **Zero trim and AOT diagnostics on the AOT path.** A suppressed diagnostic is not a pass ([PJ-08](../../architecture/01-solution-and-project-layout.md#rule-pj-08)). |
| <a id="rule-br-05"></a>BR-05 | **A debug build passing is never evidence for a release target** ([PM-01](../../architecture/14-build-packaging-and-release.md#rule-pm-01) in the build architecture). |
| <a id="rule-br-06"></a>BR-06 | **The proof is continuous**, re-run on every main-branch build ([PM-02](../../architecture/14-build-packaging-and-release.md#rule-pm-02) there), not a one-off milestone. |
| <a id="rule-br-07"></a>BR-07 | **Every third-party control entering an AOT deliverable requires its own publish proof** (**[V-05a](../../assurance/phase-1-official-verification.md#rule-v-05a)**). |
| <a id="rule-br-08"></a>BR-08 | Generated gRPC-Web clients and explicit HTTP-exception adapters must pass their real AOT dependency/registration gate; browser/Android use their selected generated TS closure. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `DesktopPlatform/samples/AssistantHost/` | Minimal AOT shell/typed-port probe; full assistant implementation follows WP15/17, with no dependency on those future packages |
| `src/ArcNotes/ArcNotes.Desktop/`, `src/ArcScope/ArcScope.Desktop/`, `src/ArcSlate/ArcSlate.Desktop/` | Equivalent minimal AOT-publishable hosts |
| `src/Cloud/ArcForges.Cloud.Host/` | Minimal host running the real pipeline order with a health endpoint and one contract endpoint |
| `src/Web/ArcForges.Web.App/` | Minimal React browser application making one typed client call |
| `tests/LocalRpcAotTests/` | Extended: attach, invoke and detach against a published AOT binary |
| `tests/ReleaseArtifactTests/` | Extended: published-artifact launch and posture inspection |
| `eng/verification/` | The publish proof scripts and their evidence output |
| CI | AOT publish added to the main-branch pipeline for all three professional desktop products |

---

## 5. Required implementation work

<a id="rule-wp-06.00"></a>

### WP-06.00 — Desktop Native AOT package proof

**What must be fully done.** Publish one minimal real host for each of ArcNotes/ArcScope/ArcSlate consuming Platform packages, with embedded assistant composition and private child channels. No fourth assistant executable.

**Testing requirements.** Run published binaries on required RIDs; load real native libraries and execute the existing ABI smoke vectors; verify no reflection or sibling-source fallback.

**Completion gate.** Actual immutable package consumers pass the required AOT/RID gates.

<a id="rule-wp-06.01"></a>

### WP-06.01 — Local RPC under AOT


**What must be fully done.** Publish two AOT desktop probe processes using the selected Kestrel HTTP/2 named-pipe/UDS listeners and client ConnectCallback. Authenticate same-user peers, complete LocalBootstrap, register both endpoint directions, invoke generated services, cancel, disconnect and reattach.

**Testing requirements.** Actual Windows/Linux/macOS process-to-process runs with malformed input, unauthorized peer and bounded resource tests.

**Completion gate.** [VG-04](../../assurance/open-gates-register.md#rule-vg-04) is supported by working generated gRPC over the exact local OS transports, not an in-memory or TCP substitute.

<a id="rule-wp-06.02"></a>

### WP-06.02 — Generated gRPC-Web under AOT


**What must be fully done.** Consume exact generated binary gRPC-Web client from published AOT desktop against actual Worker/Container ingress; prove headers, trailers, cancellation, scoped errors and exact primitives.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

**Completion gate.** [F-026](../../assurance/open-gates-register.md#rule-f-026) passes on the actual generated-client AOT closure.

<a id="rule-wp-06.03"></a>

### WP-06.03 — Realtime under AOT


**What must be fully done.** Prove EventService.Watch and output server streams plus Poll/readOutput recovery from annex 10 on actual Worker/Container/DO; drop/expire/revoke and recover through authoritative reads.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

**Completion gate.** Generated unary hints and durable reads work under AOT; no SignalR dependency or claimed hint durability.

<a id="rule-wp-06.04"></a>

### WP-06.04 — Cloudflare Native AOT and D1 proof


**What must be fully done.** Publish/deploy the actual C# Container, private Worker D1 named-plan binding, DO/Queue/R2 foundation; prove rollback on guard failure, exact 64 bit/decimal, session/CSRF/revoke and bounded checkpoint/restart. No full product Harness claim.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

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
### WP-06.07 — Android gRPC-Web and CF proof

**What must be fully done.** Build/install Kotlin Android release consuming actual Maven Connect Kotlin gRPC-Web clients; exercise unary/server-stream/trailers/cancel/Keystore and real Worker/Container/D1/DO/R2 foundation. Pin the compatible actual toolchain after proof.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

**Completion gate.** Selected runtime and transport are proven; this minimal probe requires no future full Harness, product native package or WP30 app.

<a id="rule-wp-06.90"></a>
### WP-06.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Prove actual candidate NuGet restore/native loading and desktop AOT; C# AOT gRPC/gRPC-Web plus selected auth/storage/SQL adapters; Kotlin/Jetpack Compose generated-client calls; React client calls; a minimal deployed CF ↔ reachable C# ↔ R2 chain. This is a bounded foundation probe, not the full [WP-52](52-cloud-harness.md#rule-wp-52) Harness.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

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

Acceptance includes every amended §5 producer/consumer and [WP-06.90](#rule-wp-06.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

[Local gRPC closure](../../architecture/contracts/09-local-grpc-and-sandbox.md): Run actual Windows Named Pipe/Linux and macOS UDS AOT peers with bootstrap/renew/reconnect, reverse generated invocation and zero TCP listeners. A memory stream is insufficient; full restricted launch remains WP11-owned.

| Evidence | Produced by |
|---|---|
| Per-RID AOT publish logs with zero-diagnostic assertions | [WP-06.00](#rule-wp-06.00) |
| Cross-process AOT RPC integration results | [WP-06.01](#rule-wp-06.01) |
| Dependency-graph and negative build-test results for the typed client | [WP-06.02](#rule-wp-06.02) |
| AOT realtime reconnection results | [WP-06.03](#rule-wp-06.03) |
| Cloud image build, pipeline order and integration results | [WP-06.04](#rule-wp-06.04) |
| production Web build, load and bundle baseline | [WP-06.05](#rule-wp-06.05) |
| Third-party control probe log | [WP-06.06](#rule-wp-06.06) |
| Pre-artifact Apache closure and Android/device/native/CF proof | [WP-06.07](#rule-wp-06.07) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-06.90](#rule-wp-06.90) |

---

## 8. Completion gate

**Runtime/closure producers.** [VG-06](../../assurance/open-gates-register.md#rule-vg-06) through [WP-06.04](#rule-wp-06.04); [VG-07](../../assurance/open-gates-register.md#rule-vg-07) through [WP-06.07](#rule-wp-06.07); [F-023](../../assurance/open-gates-register.md#rule-f-023) through [WP-06.07](#rule-wp-06.07). The named candidate must supply actual passing evidence; documentation does not close these gates.

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-06.90](#rule-wp-06.90) and all inherited domain-specific gates must pass on the same candidate closure. Published binaries/artifacts run in clean consumer environments; no JIT exemption, SignalR or production Node sidecar. Record real CF and native/device evidence separately from fixtures. Selected adapters work without losing exact values.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-06.05](#rule-wp-06.05) — Production Web foundation artifacts, generated SDK/exact values and IDE/portable CLI proof; this is the foundation contribution only. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. All three desktop hosts publish Native AOT with zero trim, AOT and single-file diagnostics, and launch on every supported platform without a machine-installed runtime.
2. Bidirectional local RPC works between two published AOT binaries with generated proxies — satisfying [VG-04](../../assurance/open-gates-register.md#rule-vg-04).
3. A published AOT binary makes a generated gRPC call with the selected explicit AOT-compatible adapters — satisfying [F-026](../../assurance/open-gates-register.md#rule-f-026).
4. Realtime connects, receives, disconnects and reconnects with sequence backfill from a published AOT binary.
5. The cloud host publishes and runs Native AOT with explicit adapters and zero trim/AOT diagnostics.
6. Production React assets load and call the real C# probe through the generated TS SDK with exact-value vectors, Windows/CLI workflow evidence and recorded budgets.
7. The third-party control admission process exists and has been exercised once.
8. The selected Kotlin/Jetpack Compose release probe passes first-artifact closure and actual device/service/native-adapter tests.
9. All of the above run on every main-branch build, not once.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [NAT.29](../delivery/lanes/native.md#task-nat-29) | [WP-06.90](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.90) (full) | none |
| [PRF.01](../delivery/lanes/runtime-proofs.md#task-prf-01) | [WP-06.00](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) (ArcNotes host only)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [FND.01](../delivery/lanes/foundation.md#task-fnd-01) (artifact) |
| [PRF.02](../delivery/lanes/runtime-proofs.md#task-prf-02) | [WP-06.00](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) (ArcScope host only)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [FND.01](../delivery/lanes/foundation.md#task-fnd-01) (artifact) |
| [PRF.03](../delivery/lanes/runtime-proofs.md#task-prf-03) | [WP-06.00](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) (ArcSlate host only)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [FND.01](../delivery/lanes/foundation.md#task-fnd-01) (artifact) |
| [PRF.04](../delivery/lanes/runtime-proofs.md#task-prf-04) | [WP-06.01](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.01) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.05](../delivery/lanes/contracts.md#task-con-05) (contract) |
| [PRF.05](../delivery/lanes/runtime-proofs.md#task-prf-05) | [WP-06.02](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.02) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.92](../delivery/lanes/contracts.md#task-con-92) (contract) |
| [PRF.06](../delivery/lanes/runtime-proofs.md#task-prf-06) | [WP-06.03](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.03) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | none |
| [PRF.07](../delivery/lanes/runtime-proofs.md#task-prf-07) | [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.92](../delivery/lanes/contracts.md#task-con-92) (contract) |
| [PRF.08](../delivery/lanes/runtime-proofs.md#task-prf-08) | [WP-06.05](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.92](../delivery/lanes/contracts.md#task-con-92) (contract) |
| [PRF.09](../delivery/lanes/runtime-proofs.md#task-prf-09) | [WP-06.06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.06) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [PLT.34](../delivery/lanes/platform.md#task-plt-34) (design) |
| [PRF.10](../delivery/lanes/runtime-proofs.md#task-prf-10) | [WP-06.07](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.07) (full)<br>[WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once (package-level obligation contribution) | [CON.90](../delivery/lanes/contracts.md#task-con-90) (contract) |

**Consumers outside this package:** [AND.01](../delivery/lanes/android.md#task-and-01), [APP.03](../delivery/lanes/app-composition.md#task-app-03), [AST.11](../delivery/lanes/assistant.md#task-ast-11), [CLOUD.25](../delivery/lanes/cloud.md#task-cloud-25), [CLOUD.26](../delivery/lanes/cloud.md#task-cloud-26), [NAT.01](../delivery/lanes/native.md#task-nat-01), [NAT.04](../delivery/lanes/native.md#task-nat-04), [PLT.09](../delivery/lanes/platform.md#task-plt-09), [PLT.26](../delivery/lanes/platform.md#task-plt-26), [PLT.34](../delivery/lanes/platform.md#task-plt-34), [UPD.08](../delivery/lanes/updater.md#task-upd-08), [WEB.30](../delivery/lanes/web.md#task-web-30).

<!-- delivery-graph:end -->

