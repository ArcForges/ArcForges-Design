# 16 — Testing strategy

Decisions: [AD-0014](../decisions/AD-0014-delivery-method.md) (verification responsibilities, fakes only at unavailable boundaries), [AD-0016](../decisions/AD-0016-local-first-verification.md) (local-first verification, testing techniques). Requirements: R-TEST-001..003.

**Development-stage target:** complete functionality proven by automated closed-loop tests. Fakes are used only where a real external environment is unavailable. The OS secret stores are unavailable to routine tests by the user's decision of 2026-10-17: only the separate OS secret-store integration tier (§1) reaches them, and everything else uses the isolated secret-store backend (§2). Practical real tests run on the Windows workstation and in WSL2. Final real-world user acceptance comes later, through the Plan's acceptance register.

## 1. Test layers

| Layer | Scope | Real or fake | Runs |
|---|---|---|---|
| Unit | Pure logic: budget formulas, admission, classifier rules, retry tables, state machines, parsers, redaction, scoring, token and signature handling | Real code, no I/O fakes needed | Author; hosted CI |
| Property and model-based | The same unit logic as generated properties (CsCheck): invariants, boundary conditions and resource constraints (budget formulas, admission, retry tables, redaction), round trips and malformed input for the parsers ArcForges owns (frames, configuration, CLI arguments); state machines and stateful components checked against a simple reference model; concurrent components checked for linearizability | Real code; generated inputs, shrunk to a minimal failing case | Author; hosted CI (bounded iterations); deep tier for long runs (§4) |
| Contract | Proto compilation, field-number and reserved-range rules, wire compatibility against the previous published package, JSON mapping golden files, error catalogue | Real generated code | Hosted CI (Contracts repository gates, reused) |
| Store | Node store migrations (forward from every released schema), expand-only check, queries against real SQLite, crash-consistency (kill during write, then reopen) | Real SQLite | Author; hosted CI |
| Platform | Windows job objects, pipes, ACLs, console signals; Linux transient units, D-Bus, cgroup reads, freeze | **Real OS only.** Never faked. | Author on the workstation (Windows + WSL2); hosted CI where the runner supports it (§3). The OS secret stores are not in this layer; they have their own tier below. |
| OS secret-store integration | The OS secret-store adapters only: the Windows Credential Manager and Linux Secret Service backends of `ArcForges.Security.Secrets` and the node's binding to them. Write, read back, overwrite, delete and verify absence of uniquely named test entries; a missing entry; the backend unavailable where that can be produced without changing the machine | **Real OS store**, minimal and sequential (rules below) | Windows Credential Manager: disposable GitHub-hosted Windows runners for external PRs, manual dispatch and a weekly schedule; on the workstation only on explicit opt-in. Linux Secret Service: the isolated `ArcForgesTest` WSL distribution, on explicit opt-in. Never in a default suite, the pre-push hook or the deep tier |
| Node component | One subsystem with real neighbours: scheduler + platform, supervisor + recovery, storage cleanup on real directories, toolchain adapters with real tools | Real | Author; hosted CI for platform-independent parts |
| Closed loop (local) | Node + CLI + MCP adapter + hooks + Desktop view models, through the real local API, executing real commands | Real; AI clients replaced by scripted MCP and hook drivers (AI internals are unavailable) | Author; hosted CI (headless) |
| Closed loop (multi-node) | Two or three node processes on one machine with separate data roots and loopback addresses, acting as LAN peers: pairing, placement, transfer, cache serving | Real nodes and real TLS; "other machines" simulated by processes (a physical LAN is deferred) | Author on the workstation; hosted CI |
| Closed loop (host ↔ WSL guest) | Windows host node plus guest node in WSL2 through the real `wsl.exe` bridge | Real | Workstation only |
| Closed loop (cloud) | Node and clients ↔ the local cloud stack (§3.1): the C# Cloud host as a native process, and the Worker, `FleetHub` Durable Object and D1 in local workerd | Real cloud code; **fakes** for Paddle, Google Play Developer API, Pub/Sub OIDC, FCM, the e-mail provider and the system browser (scripted consent) | Author; hosted CI (where the repository's local workerd suite already runs) |
| UI | Avalonia headless tests for every Desktop page (states, commands, accessibility tree, keyboard order); bUnit for Blazor pages; MAUI view-model tests | Real view models over real clients against a running node or the cloud closed loop | Author; hosted CI (headless only) |
| Performance | [15](15-performance-targets.md) | Real | Workstation; CI for size and startup |
| Fault injection | Unexpected termination and crashes of the node, supervisor, helpers and executions at each lifecycle point; memory exhaustion and limits (`TestLoad` ramps against job commit limits and cgroup `memory.max`); IPC failures (pipe or socket peer gone mid-call, partial frames, refused connections); timeouts and interrupted operations (deadlines, cancellation during launch, write and cleanup); permission failures (ACLs, read-only directories); disk full; store corruption; network partition between peers; relay disconnects; clock skew; webhook replays; secret-store failures (backend unavailable, failed or lost write, missing or unreadable key, a stale read after delete) through the isolated secret-store backend (§2), never against a real OS store. Each test asserts recovery and cleanup: consistent records, no leftover jobs, units, processes or temporary files, and supervisor and node lifecycle states as specified. | Real processes and OS mechanisms with controlled faults; no fault framework | Author; hosted CI where possible; deep tier repeats (§4) |

"Hosted CI" in the table means the CI-equivalent verification: the local pre-push verification for the owner's PRs and hosted CI for external PRs and manual dispatch (§3). Coverage-guided fuzzing and mutation testing are not adopted now; the reasons and the conditions for revisiting them are in [AD-0016](../decisions/AD-0016-local-first-verification.md) §5.

**OS secret-store integration tier** (the user's decision of 2026-10-17, quoted in [AD-0016](../decisions/AD-0016-local-first-verification.md) §5, amendment). Credential Manager stays the node data key store; these rules govern only how tests reach real OS secret stores.
- **Separate from the default suite.** The tests carry `[Trait("env","os-secret-store")]`. No default suite (`unit`, `ci`, `exclusive`, the real-OS and closed-loop suites), no pre-push profile, no repeat-mode run and no deep-tier run selects them. Every other test that needs a secret store uses the isolated secret-store backend (§2), including routine and pre-push runs on the workstation.
- **Opt-in locally.** On the workstation the tier runs only when the user opts in explicitly for that run (a test-script switch). Without the opt-in the tests do not run, and the selection reports them as not run with that reason. The Windows tier's normal home is the hosted runner, whose job sets the opt-in. Linux Secret Service tests run in `ArcForgesTest`, never in the development distribution `Debian` or the user's session keyring.
- **Minimal and sequential.** One test at a time, in one process, with no parallel collection and no other process using the store. Each test performs only the operations its contract needs. A fixture enforces hard limits per run: at most 4 test entries existing at once, at most 32 secret-store calls, a 10 s timeout per call and 5 minutes for the tier. Reaching a limit fails the run; it never continues past it.
- **Unique names.** Every test entry is named `ArcForges.Test.<run id>.<n>`, with a fresh random run ID. Production never uses this prefix (node data keys are `ArcForges.Secrets.v1.<hash>`). The fixture records each name before it creates the entry.
- **Safe cleanup with verified absence.** A test deletes only the entries it recorded, by exact name, then reads each one back to verify that it is absent. A remaining entry fails the test and is reported by name. Cleanup never enumerates or deletes by pattern and never touches an entry it did not create: production `ArcForges.Secrets.v1.*` keys and unrelated credentials are never touched. A failed absence check is not retried in a loop; it is evidence (L-26).
- **Never stress or load.** No stress, load, soak or concurrency test runs against a real OS secret store, hosted runners included. Key lifecycle, sealing, failure injection and concurrency are tested against the isolated secret-store backend, and no test depends on a real store's behaviour under concurrent modification (L-26).

## 2. Fakes catalogue (the only permitted substitutes)

| Fake | Replaces | Fidelity source | Lives in |
|---|---|---|---|
| `FakePaddle` | Paddle API and webhook sender | Recorded signed webhook fixtures and API schemas from the historical adapter design | Cloud tests |
| `FakePlayDeveloperApi` | `purchases.subscriptionsv2`, `acknowledge`, voided purchases | Google API discovery schema; recorded responses | Cloud tests |
| `FakePubSubPush` | RTDN delivery with OIDC tokens | Token format per Google documentation; a test signing key | Cloud tests |
| `FakeFcm` | FCM HTTP v1 send | Request and response schema | Cloud tests |
| `FakeMailSender` | The transactional e-mail provider (Postmark, with Amazon SES as fallback) | The provider adapter's request and outcome schema. Tests read sign-in codes from captured messages. | Cloud tests |
| `FakeBillingClient` | The Play Billing Library `BillingClient` on the emulator (no Play Store or licence-test account) | Billing Library 8+ API surface: connection, product details, launch flow results, purchase updates, acknowledgement state. Scripted outcomes for success, pending, cancelled, already-owned and errors. | Mobile tests (AF-AND-03) |
| `ScriptedBrowser` | System browser for PKCE and device-code approval | Drives the real web profile endpoints with HTTP calls | ArcForges tests |
| `ScriptedMcpClient` | Claude Code / Codex as MCP clients | MCP schema for both revisions; transcripts of real client handshakes recorded on the workstation | ArcForges tests |
| `HookPayloadFixtures` | Client hook invocations | Fixtures captured from real clients on the workstation (F-A01 task) | ArcForges tests |
| `PeerProcess` | Another LAN machine | A real node process with its own data root and address | ArcForges tests |
| `IsolatedSecretStore` | The OS secret store (Windows Credential Manager, Linux Secret Service), for everything above the secret-store adapter: node data key lifecycle (create, load, a new version when the key is missing or the backend changed), sealing and unsealing of task secrets, node and link credential handling, failure injection and concurrency | The `ISecretBackingStore` contract of `ArcForges.Security.Secrets` (write, read, delete, reported isolation), with the selection's reported backend and protection. In memory, one instance per test. Optional scripted faults: backend unavailable, write or read failure or timeout, a write that reports success but is not readable later (lost write), a read that still returns a deleted value (L-26), a locked keyring. | ArcForges tests (`tests/Shared`) |

**Synthetic workloads are not fakes.** `TestLoad` (`tools/ArcForges.TestLoad`) generates deterministic CPU, memory, output and fork patterns as the *input* to the behaviour under test (scheduling, enforcement, capture, diagnosis). It replaces no external system, so every task may use it, and evidence names the workload that ran.

`IsolatedSecretStore` is never used for the adapters' own OS integration tests (§1), which exercise the real store. The owner-only file fallback under a test's temporary data root is not an OS store and stays real where a test needs it. Because routine tests cannot use the real OS secret store (the user's decision of 2026-10-17), this substitute stays within R-TEST-001 and [AD-0014](../decisions/AD-0014-delivery-method.md) §6 (as amended by [AD-0016](../decisions/AD-0016-local-first-verification.md)).

A fake is never used for the behaviour under test (R-TEST-001). Results from a fake-backed test are labelled `closed-loop` in evidence and never reported as real-world validation. The real billing flow on a Play-enabled emulator or device stays in the acceptance register (AR-06).

## 3. Environments and responsibilities

| Environment | Runs | Notes |
|---|---|---|
| Workstation, Windows 11 | All Windows platform and closed-loop tests; WSL bridge tests; performance | The author runs the affected suites for every task. Secret stores are the isolated backend (§2); real Credential Manager tests run only on the user's explicit opt-in (§1). |
| Workstation, WSL2 Debian 13 | All Linux platform tests (systemd user manager, transient units, freeze, OOM); guest-node tests | Installs inside the distribution are done by the user. Tests needing new packages list them as prerequisites. Never the Secret Service tier. |
| Workstation, WSL2 `ArcForgesTest` (Debian 13) | The Linux Secret Service tests of the OS secret-store tier (§1), on explicit opt-in | The user's separate, clean installation and restart test environment. The tier leaves no entries behind. A Secret Service provider there is installed by the user; without one the tests are skipped with an explicit reason, never reported as passed. |
| Workstation, pre-push verification (owner PRs) | The repository's CI-equivalent profile at the pushed commit, Windows and WSL2 Debian lanes concurrently, exclusive steps afterwards: build, analyzers, format, tests, closed loop on Native AOT, AOT publish x64, size and startup gates, packaging, secret scan | The owner's merge gate ([AD-0016](../decisions/AD-0016-local-first-verification.md)). Fails closed; a pass is reused only for an identical source state (the tree, plus the exact commits when a step reads history), step set, scripts and tool versions. Secret stores are the isolated backend; the OS secret-store tier never runs here. |
| Hosted CI, Windows runner (external PRs, manual dispatch) | Build, unit, contract, store, Windows job-object tests that need no interactive session, closed loop (headless), AOT publish, packaging. In its own job, also for a weekly schedule: the Credential Manager tests of the OS secret-store tier (§1), alone and sequential | No GUI, device, browser, live-service or inference jobs. Each job gets a fresh, disposable runner. |
| Hosted CI, Linux runner (external PRs, manual dispatch) | Build, unit, contract, store, AOT publish, packaging. Transient-unit tests only if the runner offers a user manager; otherwise they are skipped with an explicit `requires-user-manager` reason. | The workstation's WSL2 run remains the authoritative Linux evidence |
| Emulator (local) | Android UI and billing flows with `FakeBillingClient` against the fake Play backend | Local opt-in. A Play-enabled emulator with a licence-test account (H-17) and a physical device are deferred to AR-06 and AR-08. |
| Deferred (acceptance register) | Physical LAN machines, real store purchases, real FCM delivery, production signing reputation, second OS accounts, human screen-reader sessions, macOS (out of scope) | Never reported as proven |

### 3.1 Local cloud stack

The cloud closed loop runs natively on the workstation and needs neither Docker nor WSL:
1. **Worker side.** `workerd` under Miniflare (the Cloud repository's local scripts) runs the Worker ingress, the relay routes, the `FleetHub` Durable Object, and local D1, R2 and Queue. Miniflare's local S3 endpoint, configured with test `s3Credentials`, serves the SigV4 presigned uploads of the support flow (F-C03 checks it first).
2. **C# host.** `ArcForges.Cloud` runs as a native process on a loopback port: the JIT build for most suites, the Native AOT binary for the AOT suites.
3. **Container shim.** In the local profile, the Worker's Container binding is replaced by a shim that forwards to the native host's loopback port. The host reaches D1, R2 and the Queue through the same signed internal routes as in production, with test keys. AF-CLD-01 builds the shim as part of the repository's local verification scripts.
4. **Clients.** Nodes, CLI, Desktop view models, the Blazor app (bUnit and HTTP) and the Android view models point at the local ingress.

Docker is optional (H-18). It enables only the Cloud repository's existing `test:container` diagnostics, which are never a gate. Live Cloudflare deployments are not part of any test.

Verification roles follow [AD-0014](../decisions/AD-0014-delivery-method.md) §4: the author runs targeted and affected suites, the reviewer adds only distinct evidence, and nobody repeats an identical full run on an unchanged head. The merge gate is the local pre-push verification for the owner's PRs and hosted CI for external PRs ([AD-0016](../decisions/AD-0016-local-first-verification.md)).

## 4. Test organisation in the ArcForges repository

```
tests/
  ArcForges.Node.Core.Tests/            unit + component
  ArcForges.Node.Store.Tests/           store, migrations, crash consistency
  ArcForges.Node.Platform.Windows.Tests/ [Trait("env","windows-real")]
  ArcForges.Node.Platform.Linux.Tests/   [Trait("env","linux-real")]
  ArcForges.Node.Toolchains.Tests/       [Trait("tool","dotnet|cargo|cmake|npm")] real tools when present
  ArcForges.ClosedLoop.Tests/            local, multi-node, cloud (Trait "loop")
  ArcForges.Wsl.Tests/                   [Trait("env","wsl-bridge")] workstation only
  ArcForges.Desktop.Tests/               Avalonia headless
  ArcForges.Mcp.Tests/                   ScriptedMcpClient, both protocol revisions
  ArcForges.Bench/                       performance (not run by default)
```

- **Selection.** Traits select suites. `eng/test.ps1` / `eng/test.sh` map task kinds to suites, so authors run exactly the affected set. Tool-dependent tests are skipped with an explicit reason when the tool is missing, and the reason appears in the evidence.
- **Deterministic time.** Node subsystems take an `IClock`. Tests use a controllable clock except in real-OS timing tests.
- **Determinism.** Tests assert the guaranteed product contract, never an optional OS notification or a timing assumption the platform does not guarantee (V-W03). Fixed sleeps are condition waits; generous timeouts apply only on the failure path. A flaky test is fixed at its cause, never hidden by retries or weakened assertions.
- **Parallelism and exclusive phase.** `eng/test.ps1` / `eng/test.sh` run test projects concurrently, bounded by a default chosen from recorded measurements (wall time, CPU, failures over repeated runs). Serial collections remain only where tests share machine-wide state. Timing-, CPU-share- and memory-sensitive tests carry `[Trait("isolation","exclusive")]` and run in a separate phase after the parallel one, alone.
- **Repeat mode.** The same scripts run selected suites N times, stop at the first failure and report per-iteration timing. Repeat mode never selects the OS secret-store tier.
- **Secret stores.** Tests that need a secret store get an `IsolatedSecretStore` (§2). Only tests with `[Trait("env","os-secret-store")]` reach a real OS store, under the rules of §1.
- **Tiers.**
  - *Routine (inner loop):* the affected suites, built once, then rerun without rebuilding.
  - *Pre-push (the hook):* the full CI-equivalent profile on Windows and WSL2 Debian (§3).
  - *Deep (manual, release preparation, after a flaky failure):* repeat-mode stress runs, `ArcForges.Bench` performance, the `wsl-bridge` suite, long property runs (CsCheck iteration and time settings), and ARM64 through a manual `workflow_dispatch` when wanted. Never against a real OS secret store.
  - *OS secret-store integration (separate):* §1; hosted for external PRs, manual dispatch and weekly; locally only on opt-in.
- **Isolation.** Each test node gets a temporary data root, a unique pipe or socket name, a unique node ID (so Windows job names cannot collide) and its own transient slice name on Linux (`arcforges-test-<id>.slice`). A fixture cleans up leftover jobs, units and processes and fails the test if any remain.

## 5. Release-candidate acceptance

The release candidate (AF-ACC-01) runs every journey J-01 to J-11 end to end with:
- **real core implementations**: node, CLI, MCP adapter, hooks, Desktop view models, cloud host, Worker and Durable Object code, Blazor and Android view models;
- **the approved external fakes** of §2 where the external system is unavailable: `FakePaddle`, `FakePlayDeveloperApi`, `FakePubSubPush`, `FakeFcm`, `FakeMailSender`, `FakeBillingClient`, `ScriptedBrowser`, `ScriptedMcpClient`, `HookPayloadFixtures`, `PeerProcess` for other machines, and `IsolatedSecretStore` for the OS secret store (the real stores are covered by the OS secret-store tier of §1). A fake never replaces the behaviour under test;
- **honest labels**: results are labelled closed-loop, and every remaining real-world validation stays in the acceptance register (AR-01 to AR-16).

## 6. Acceptance evidence per task

Each delivery task's PR records:
1. the exact commands run, with their results (author);
2. the environments covered (Windows real, WSL2 real; for the owner's PRs the local verification record, the hook's `arcforges-verify: PASS` line; for external PRs hosted CI);
3. which acceptance criteria each test proves, by requirement ID;
4. benchmarks when a measured path changed;
5. any acceptance-register entries created or advanced, with the human prerequisite stated.

The reviewer's record lists only the distinct checks performed and the diff review result ([AD-0014](../decisions/AD-0014-delivery-method.md) §4).
