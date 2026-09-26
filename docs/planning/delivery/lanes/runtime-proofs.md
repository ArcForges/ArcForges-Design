# Runtime proofs — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Early real-runtime proofs per platform: Native AOT desktop, local gRPC, gRPC-Web, Cloudflare Container and D1, React, third-party controls and Android.

Tasks: 10 · Owning repositories: ArcNotes, ArcScope, ArcSlate, Cloud, DesktopPlatform, Mobile, Web · Integration owner(s): ArcNotes integration owner, ArcScope integration owner, ArcSlate integration owner, Cloud integration owner, DesktopPlatform integration owner, Mobile integration owner, Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [PRF.01](#task-prf-01) | ArcNotes desktop Native AOT package proof | proof | M | [CON.91](contracts.md#task-con-91) (contract), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PRF.02](#task-prf-02) | ArcScope desktop Native AOT package proof | proof | M | [CON.91](contracts.md#task-con-91) (contract), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PRF.03](#task-prf-03) | ArcSlate desktop Native AOT package proof | proof | M | [CON.91](contracts.md#task-con-91) (contract), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PRF.04](#task-prf-04) | Local RPC under AOT: bidirectional named-pipe/UDS probe processes | proof | L | [CON.05](contracts.md#task-con-05) (contract) | not-started |
| [PRF.05](#task-prf-05) | Generated gRPC-Web under AOT against deployed Worker/Container ingress | proof | M | [CON.92](contracts.md#task-con-92) (contract), [PRF.07](#task-prf-07) (artifact) | not-started |
| [PRF.06](#task-prf-06) | Realtime (EventService.Watch/Poll) under AOT | proof | M | [PRF.07](#task-prf-07) (artifact) | not-started |
| [PRF.07](#task-prf-07) | Cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof | proof | XL | [CON.92](contracts.md#task-con-92) (contract) | not-started |
| [PRF.08](#task-prf-08) | React production build and generated TS SDK proof | proof | L | [CON.92](contracts.md#task-con-92) (contract), [PRF.07](#task-prf-07) (artifact) | not-started |
| [PRF.09](#task-prf-09) | Third-party control AOT admission gate and first candidate | proof | S | [PLT.34](platform.md#task-plt-34) (design) | not-started |
| [PRF.10](#task-prf-10) | Android Kotlin/Jetpack Compose gRPC-Web and CF proof | proof | L | [CON.90](contracts.md#task-con-90) (contract), [PRF.07](#task-prf-07) (artifact) | not-started |

## Tasks

<a id="task-prf-01"></a>

### PRF.01 — ArcNotes desktop Native AOT package proof

**Outcome.** ArcForges.ArcNotes publishes self-contained Native AOT per Tier-1/Tier-2 RID, launches without a machine runtime, loads real native libraries and passes existing ABI smoke vectors with no reflection/sibling-source fallback; wired into continuous main-branch CI ([BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06)).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/prf-01` and ledger record `ledger/tasks/prf-01.md` in the Plan repository; task branch `task/prf-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / M · early risk proof |
| Obligations | [WP-06.00](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) — ArcNotes host only<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | arcnotes-desktop-aot-host |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — ArcForges.Contracts.Foundation/LocalRpc.Notes published package. *Why:* the host's typed local port and error surface compile against these generated records; WP03.01 is already accepted<br>**artifact** [FND.01](foundation.md#task-fnd-01) — Foundation/Application.Abstractions identity/error primitives. *Why:* the host and its Core reference these primitive types; only the primitives, not all of WP04's substeps |
| Entry condition | [ADOPT.04.runtime-proofs](adoption.md#task-adopt-04-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.04](native.md#task-nat-04), [NAT.29](native.md#task-nat-29), [PLT.26](platform.md#task-plt-26), [PLT.34](platform.md#task-plt-34), [UPD.08](updater.md#task-upd-08) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes/**`<br>`ArcNotes:ArcNotes.slnx` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-product-solutions](../shared-resources.md#res-product-solutions) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Windows/Linux local Native AOT publish with zero trim/AOT/single-file diagnostics ([BR-04](../../../architecture/14-build-packaging-and-release.md#rule-br-04)); real per-RID launch and ABI smoke vectors; no macOS CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), local-opt-in macOS only |
| Completion evidence | Per-RID AOT publish log with zero-diagnostic assertion; smoke-vector pass log; continuous main-branch CI run reference |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/ArcForges.ArcNotes/ArcForges.ArcNotes.csproj + src/ArcForges.ArcNotes.Core already exist; docs/assurance/wp02-02-aot-sweep-evidence.md records a one-off research Windows x64 AOT publish+execute of this host reaching deployed Cloud rev 8942437a5e42c01ae7595b64a220efd60f33b4f0, but explicitly not the WP06 continuous/full-contract-set proof. Exact contents of ArcForges.ArcNotes.csproj not read line-by-line (budget); recommend the integration owner or a follow-up pass confirm embedded-assistant composition state before scheduling. |
| Notes | Runs in parallel with PRF.02/PRF.03 (different repos, no shared write scope). |

<a id="task-prf-02"></a>

### PRF.02 — ArcScope desktop Native AOT package proof

**Outcome.** ArcForges.ArcScope publishes self-contained Native AOT per Tier-1/Tier-2 RID, launches without a machine runtime, loads real native libraries and passes existing ABI smoke vectors; wired into continuous main-branch CI.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/prf-02` and ledger record `ledger/tasks/prf-02.md` in the Plan repository; task branch `task/prf-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / M · early risk proof |
| Obligations | [WP-06.00](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) — ArcScope host only<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | arcscope-desktop-aot-host |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — ArcForges.Contracts.Foundation/LocalRpc.Scope published package. *Why:* host typed local port compiles against these generated records<br>**artifact** [FND.01](foundation.md#task-fnd-01) — Foundation/Application.Abstractions identity/error primitives. *Why:* same as PRF.01 |
| Entry condition | [ADOPT.05.runtime-proofs](adoption.md#task-adopt-05-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.29](native.md#task-nat-29) |
| Write scope | `ArcScope:src/ArcForges.ArcScope/**`<br>`ArcScope:ArcScope.slnx` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-product-solutions](../shared-resources.md#res-product-solutions) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Windows/Linux local Native AOT publish with zero trim/AOT/single-file diagnostics; real per-RID launch and ABI smoke vectors; no macOS CI |
| Completion evidence | Per-RID AOT publish log with zero-diagnostic assertion; smoke-vector pass log; continuous main-branch CI run reference |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/ArcForges.ArcScope/ArcForges.ArcScope.csproj + Core already exist; same wp02-02 one-off research caveat as PRF.01 applies. |
| Notes | Runs in parallel with PRF.01/PRF.03. |

<a id="task-prf-03"></a>

### PRF.03 — ArcSlate desktop Native AOT package proof

**Outcome.** ArcForges.ArcSlate publishes self-contained Native AOT per Tier-1/Tier-2 RID, launches without a machine runtime, loads real native libraries and passes existing ABI smoke vectors; wired into continuous main-branch CI.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/prf-03` and ledger record `ledger/tasks/prf-03.md` in the Plan repository; task branch `task/prf-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / M · early risk proof |
| Obligations | [WP-06.00](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) — ArcSlate host only<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | arcslate-desktop-aot-host |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — ArcForges.Contracts.Foundation/LocalRpc.Slate published package. *Why:* host typed local port compiles against these generated records<br>**artifact** [FND.01](foundation.md#task-fnd-01) — Foundation/Application.Abstractions identity/error primitives. *Why:* same as PRF.01 |
| Entry condition | [ADOPT.06.runtime-proofs](adoption.md#task-adopt-06-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.29](native.md#task-nat-29) |
| Write scope | `ArcSlate:src/ArcForges.ArcSlate/**`<br>`ArcSlate:ArcSlate.slnx` |
| Shared resources | [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-product-solutions](../shared-resources.md#res-product-solutions) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Windows/Linux local Native AOT publish with zero trim/AOT/single-file diagnostics; real per-RID launch and ABI smoke vectors; no macOS CI |
| Completion evidence | Per-RID AOT publish log with zero-diagnostic assertion; smoke-vector pass log; continuous main-branch CI run reference |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/ArcForges.ArcSlate/ArcForges.ArcSlate.csproj + Core already exist; same wp02-02 one-off research caveat as PRF.01 applies. |
| Notes | Runs in parallel with PRF.01/PRF.02. |

<a id="task-prf-04"></a>

### PRF.04 — Local RPC under AOT: bidirectional named-pipe/UDS probe processes

**Outcome.** Two published AOT desktop probe processes complete LocalBootstrap over Kestrel HTTP/2 named-pipe (Windows) / UDS (Linux/macOS), authenticate same-user peers, register both endpoint directions, invoke generated services, cancel, disconnect and reattach; malformed-input/unauthorized-peer/bounded-resource negative tests pass.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/prf-04` and ledger record `ledger/tasks/prf-04.md` in the Plan repository; task branch `task/prf-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / L · early risk proof |
| Obligations | [WP-06.01](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.01) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | local-rpc-aot-proof |
| Start prerequisites | **contract** [CON.05](contracts.md#task-con-05) — local RPC generated server/client codegen (LocalBootstrap, ConnectCallback surface). *Why:* the probe processes invoke generated services over the local transport; this exact codegen is [VG-04](../../../assurance/open-gates-register.md#rule-vg-04)'s own scheduled-in producer |
| Entry condition | [ADOPT.02.runtime-proofs](adoption.md#task-adopt-02-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.03](app-composition.md#task-app-03), [NAT.01](native.md#task-nat-01), [NAT.29](native.md#task-nat-29), [PLT.09](platform.md#task-plt-09) |
| Write scope | `DesktopPlatform:tests/LocalRpcAotTests/**`<br>`DesktopPlatform:eng/verification/**` |
| Shared resources | [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Actual Windows/Linux/macOS(local opt-in) process-to-process runs; no in-memory or TCP substitute (explicit design prohibition); malformed input, unauthorized peer, bounded resource tests |
| Completion evidence | Cross-process AOT RPC integration results satisfying [VG-04](../../../assurance/open-gates-register.md#rule-vg-04) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: tests/LocalRpcAotTests not found under a shallow listing; |
| Notes | Directly closes [VG-04](../../../assurance/open-gates-register.md#rule-vg-04). Independent of PRF.01-03 (uses its own dedicated probe processes, not the product hosts). |

<a id="task-prf-05"></a>

### PRF.05 — Generated gRPC-Web under AOT against deployed Worker/Container ingress

**Outcome.** A published AOT desktop probe calls the real generated binary gRPC-Web client against actual deployed Worker/Container ingress, proving headers, trailers, cancellation, scoped errors and exact primitives; [F-026](../../../assurance/open-gates-register.md#rule-f-026) closes on this artifact.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/prf-05` and ledger record `ledger/tasks/prf-05.md` in the Plan repository; task branch `task/prf-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / M · early risk proof |
| Obligations | [WP-06.02](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.02) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | desktop-grpc-web-aot-proof |
| Start prerequisites | **contract** [CON.92](contracts.md#task-con-92) — ArcForges.Sdk.Client / generated gRPC-Web client, AOT-clean per accepted WP03.02 evidence. *Why:* [F-026](../../../assurance/open-gates-register.md#rule-f-026) requires the published-artifact call, and WP03.02 already produced the AOT-clean generated client that this substep must exercise for real, not merely compile<br>**artifact** [PRF.07](#task-prf-07) — a deployed Worker/Container ingress endpoint (from [WP-06.04](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04)). *Why:* 06.02 explicitly calls 'actual Worker/Container ingress' — no fixture substitute closes [F-026](../../../assurance/open-gates-register.md#rule-f-026) |
| Entry condition | [ADOPT.02.runtime-proofs](adoption.md#task-adopt-02-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.11](assistant.md#task-ast-11), [NAT.29](native.md#task-nat-29) |
| Write scope | `DesktopPlatform:tests/ReleaseArtifactTests/**`<br>`DesktopPlatform:eng/verification/**` |
| Validation | Production browser-equivalent round trip against real AOT host + deployed CF; scope/permission, wrong/stale target, loss/retry, expiry cases; local opt-in only, not hosted CI |
| Completion evidence | Dependency-graph and negative build-test results for the typed client; [F-026](../../../assurance/open-gates-register.md#rule-f-026) closure evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: tests/ReleaseArtifactTests listed in WP06 SS4 as 'Extended' (implies it exists from WP02/03); not independently confirmed by directory listing in this pass. |
| Notes | Start-depends on PRF.07 (same area) for the deployed ingress target. |

<a id="task-prf-06"></a>

### PRF.06 — Realtime (EventService.Watch/Poll) under AOT

**Outcome.** A published AOT desktop probe proves EventService.Watch and output server streams plus Poll/readOutput recovery from annex 10 against actual Worker/Container/DO, including drop/expire/revoke and recovery through authoritative reads; no SignalR dependency, no claimed hint durability beyond what is proven.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/prf-06` and ledger record `ledger/tasks/prf-06.md` in the Plan repository; task branch `task/prf-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / M |
| Obligations | [WP-06.03](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.03) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | desktop-realtime-aot-proof |
| Start prerequisites | **artifact** [PRF.07](#task-prf-07) — deployed Worker/Container/DO providing EventService.Watch. *Why:* 06.03 requires the actual deployed provider boundary; no fixture closes real integration per WP06 SS5 text |
| Entry condition | [ADOPT.02.runtime-proofs](adoption.md#task-adopt-02-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.29](native.md#task-nat-29) |
| Write scope | `DesktopPlatform:tests/ReleaseArtifactTests/**`<br>`DesktopPlatform:eng/verification/**` |
| Validation | Real deployed DO/Worker realtime round trip; scope/permission, stale target, loss/retry, expiry cases; local opt-in only |
| Completion evidence | AOT realtime reconnection results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no realtime-specific probe found in this pass; treat as new work pending confirmation. |
| Notes | Runs after PRF.07 stands up DO/Worker; independent of PRF.04/05 otherwise. |

<a id="task-prf-07"></a>

### PRF.07 — Cloudflare Native AOT host + D1 + DO/Queue/R2 foundation proof

**Outcome.** ArcForges.Cloud.Host publishes/deploys as a Linux x64 Native AOT container with the real private Worker D1 binding, DO/Queue/R2 foundation, rollback on guard failure, exact 64-bit/decimal handling, session/CSRF/revoke and bounded checkpoint/restart; zero trim/AOT diagnostics; [VG-06](../../../assurance/open-gates-register.md#rule-vg-06) is supported (not yet closed platform-wide, since [VG-06](../../../assurance/open-gates-register.md#rule-vg-06) is also maintained by [WP-21.00](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.00)/[WP-50.04](../../work-packages/50-full-platform-production-release.md#rule-wp-50.04)).

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/prf-07` and ledger record `ledger/tasks/prf-07.md` in the Plan repository; task branch `task/prf-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / XL · early risk proof |
| Obligations | [WP-06.04](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | cloud-aot-foundation |
| Start prerequisites | **contract** [CON.92](contracts.md#task-con-92) — ArcForges.Contracts.CloudInternal, native auth exception/catalog/index/revocation/realm schemas and independent signed vectors (fixture keys per WP02/06). *Why:* WP06 itself is a permitted producer of the signing-key fixture, not solely a consumer |
| Entry condition | [ADOPT.07.runtime-proofs](adoption.md#task-adopt-07-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.25](cloud.md#task-cloud-25), [NAT.29](native.md#task-nat-29), [PRF.05](#task-prf-05), [PRF.06](#task-prf-06), [PRF.08](#task-prf-08), [PRF.10](#task-prf-10) |
| Permitted substitutes | [SUB-signed-format-fixture-keys](../substitutes.md#sub-signed-format-fixture-keys) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Host/**`<br>`Cloud:eng/verification/**` |
| Shared resources | [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Native AOT compilation required; real-adapter runtime verification is scoped local opt-in per [V-03](../../../assurance/phase-1-official-verification.md#rule-v-03)/[P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); no EF/dynamic ORM/ASP.NET Session/CookieAuthenticationHandler; chiseled Ubuntu image, non-root, read-only root |
| Completion evidence | Cloud image build, pipeline order and integration results; [VG-06](../../../assurance/open-gates-register.md#rule-vg-06) supporting evidence |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/Cloud/ArcForges.Cloud.Host present per WP02.02 receipt (published Linux x64 Native AOT, real health+greeting endpoint reachable); full D1/DO/Queue/R2/passkey/CSRF closure not yet built. [VG-06](../../../assurance/open-gates-register.md#rule-vg-06) register state is 'TRIGGERED — execution evidence pending', consistent with this being open work. |
| Notes | This is the foundation every other Cloud-touching PRF task (05, 06, 08, 10) depends on. |

<a id="task-prf-08"></a>

### PRF.08 — React production build and generated TS SDK proof

**Outcome.** Minimal Account/Chat production React profiles build from Web root locks using the exact released generated gRPC-Web SDK, call the real AOT Cloud probe through same-origin routing/cookie/CSRF, exercise exact values/typed failures/cancellation and CF authenticated presentation; asset/interaction budgets measured; esproj and portable npm entry points proven. Contributes the foundation slice of [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) only.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/prf-08` and ledger record `ledger/tasks/prf-08.md` in the Plan repository; task branch `task/prf-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / L |
| Obligations | [WP-06.05](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | web-production-aot-proof |
| Start prerequisites | **contract** [CON.92](contracts.md#task-con-92) — @arcforges/api-client generated TS gRPC-Web client, AOT-irrelevant but descriptor/compat-checked. *Why:* the production build calls the actual generated SDK, not a handwritten DTO<br>**artifact** [PRF.07](#task-prf-07) — a deployed Cloud AOT probe reachable same-origin through CF. *Why:* 06.05 explicitly requires calling 'the actual AOT probe' with CF authenticated presentation; no dev-server or handwritten DTO substitute is acceptable |
| Entry condition | [ADOPT.09.runtime-proofs](adoption.md#task-adopt-09-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.29](native.md#task-nat-29), [WEB.30](web.md#task-web-30) |
| Permitted substitutes | [SUB-web-msw-fixtures](../substitutes.md#sub-web-msw-fixtures) |
| Write scope | `Web:src/Web/ArcForges.Web.App/**`<br>`Web:apps/**` |
| Validation | Production Node/npm build, no dev server; browser/CSP/visual/bundle-budget checks; malformed frame/status and session-expiry cases; Windows win.slnx/esproj + portable npm entry points |
| Completion evidence | Production Web build, load and bundle baseline; [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) foundation contribution |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: wp02-03-runtime-boundary-evidence.md confirms win.slnx/esproj Build/Deploy wiring and a working local IDE + portable npm dev flow already exist and were verified end-to-end against deployed Cloud's Hello boundary at web-0.1.0-ci.24.1; production Account/Chat profile itself is not yet built. |
| Notes | Lower novel-technology risk than the native/AOT proofs (React/Node toolchain is well understood); still a required [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) contribution. |

<a id="task-prf-09"></a>

### PRF.09 — Third-party control AOT admission gate and first candidate

**Outcome.** The process for admitting a third-party UI control into an AOT deliverable is documented and exercised once against a real candidate control published AOT with zero diagnostics; schedules [VG-03](../../../assurance/open-gates-register.md#rule-vg-03) for WP10.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/prf-09` and ledger record `ledger/tasks/prf-09.md` in the Plan repository; task branch `task/prf-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / S |
| Obligations | [WP-06.06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.06) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | third-party-control-admission-process |
| Start prerequisites | **design** [PLT.34](platform.md#task-plt-34) — a candidate third-party control the desktop shell actually intends to use. *Why:* the process needs one real candidate to exercise; if WP10 has not yet named a candidate control this substep can only stand up the process and defer the first exercise |
| Entry condition | [ADOPT.02.runtime-proofs](adoption.md#task-adopt-02-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.29](native.md#task-nat-29) |
| Write scope | `DesktopPlatform:eng/verification/probe-evidence/**` |
| Validation | Single probe-host AOT publish with zero diagnostics for the first candidate |
| Completion evidence | Probe publish log for the first candidate |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no candidate-control probe found in this pass. |
| Notes | Low coupling; can run independent of PRF.01-08. Formally schedules [VG-03](../../../assurance/open-gates-register.md#rule-vg-03) to WP10, not itself. |

<a id="task-prf-10"></a>

### PRF.10 — Android Kotlin/Jetpack Compose gRPC-Web and CF proof

**Outcome.** A Kotlin Android release build consumes the actual Maven Connect Kotlin gRPC-Web client, exercises unary/server-stream/trailers/cancel/Keystore against real Worker/Container/D1/DO/R2 foundation; the compatible actual toolchain is pinned after proof. Closes [VG-07](../../../assurance/open-gates-register.md#rule-vg-07) and the first-artifact leg of [F-023](../../../assurance/open-gates-register.md#rule-f-023) (already CLOSED for the inspected android-0.1.0-ci.14.1 replacement per the gates register, but reopens on dependency/resource change).

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/prf-10` and ledger record `ledger/tasks/prf-10.md` in the Plan repository; task branch `task/prf-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | proof / L · early risk proof |
| Obligations | [WP-06.07](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.07) — full<br>[WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) SS8 completion gate item 9 / [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06): every proof runs continuously on main-branch builds, not once — package-level obligation contribution |
| Provides | android-grpc-web-cf-proof |
| Start prerequisites | **contract** [CON.90](contracts.md#task-con-90) — io.github.arcforges:contracts-connect-client Maven artifact (public schema only, Connect Kotlin generated client). *Why:* the release build calls this exact generated client, selecting binary gRPC-Web explicitly<br>**artifact** [PRF.07](#task-prf-07) — deployed Worker/Container/D1/DO/R2 foundation. *Why:* 06.07 requires the real deployed provider boundary, matching the pattern of 06.02/06.03 |
| Entry condition | [ADOPT.10.runtime-proofs](adoption.md#task-adopt-10-runtime-proofs) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.01](android.md#task-and-01), [CLOUD.26](cloud.md#task-cloud-26), [NAT.29](native.md#task-nat-29) |
| Write scope | `Mobile:app/**`<br>`Mobile:gradle/**` |
| Shared resources | [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive) |
| Validation | Actual device/service/native-adapter tests; scope/permission, wrong/stale target, loss/retry, expiry cases; CI builds the release artifact, device checks are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Pre-artifact Apache closure and Android/device/native/CF proof |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: open-gates-register.md records [F-023](../../../assurance/open-gates-register.md#rule-f-023) CLOSED 2026-09-19 for candidate android-0.1.0-ci.14.1 (Mobile PR4/PR5), with real main CI and public upgrade verification passed -- meaning substantial Android release-build and dependency-closure work already landed. [VG-07](../../../assurance/open-gates-register.md#rule-vg-07) itself remains OPEN (full native-module + real transport inspection against that candidate not yet recorded as closed). |
| Notes | Different runtime family (Kotlin/JVM) from the rest of WP06 -- genuine independent risk axis. |
