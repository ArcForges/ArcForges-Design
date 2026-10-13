# 16 — Testing strategy

Decisions: [AD-0014](../decisions/AD-0014-delivery-method.md) (verification responsibilities, fakes only at unavailable boundaries). Requirements: R-TEST-001..003.

**Development-stage target:** complete functionality proven by automated closed-loop tests. Fakes are used only where a real external environment is unavailable. Practical real tests run on the Windows workstation and in WSL2. Final real-world user acceptance comes later, through the Plan's acceptance register.

## 1. Test layers

| Layer | Scope | Real or fake | Runs |
|---|---|---|---|
| Unit | Pure logic: budget formulas, admission, classifier rules, retry tables, state machines, parsers, redaction, scoring, token and signature handling | Real code, no I/O fakes needed | Author; hosted CI |
| Contract | Proto compilation, field-number and reserved-range rules, wire compatibility against the previous published package, JSON mapping golden files, error catalogue | Real generated code | Hosted CI (Contracts repository gates, reused) |
| Store | Node store migrations (forward from every released schema), expand-only check, queries against real SQLite, crash-consistency (kill during write, then reopen) | Real SQLite | Author; hosted CI |
| Platform | Windows job objects, pipes, ACLs, console signals; Linux transient units, D-Bus, cgroup reads, freeze | **Real OS only.** Never faked. | Author on the workstation (Windows + WSL2); hosted CI where the runner supports it (§3) |
| Node component | One subsystem with real neighbours: scheduler + platform, supervisor + recovery, storage cleanup on real directories, toolchain adapters with real tools | Real | Author; hosted CI for platform-independent parts |
| Closed loop (local) | Node + CLI + MCP adapter + hooks + Desktop view models, through the real local API, executing real commands | Real; AI clients replaced by scripted MCP and hook drivers (AI internals are unavailable) | Author; hosted CI (headless) |
| Closed loop (multi-node) | Two or three node processes on one machine with separate data roots and loopback addresses, acting as LAN peers: pairing, placement, transfer, cache serving | Real nodes and real TLS; "other machines" simulated by processes (a physical LAN is deferred) | Author on the workstation; hosted CI |
| Closed loop (host ↔ WSL guest) | Windows host node plus guest node in WSL2 through the real `wsl.exe` bridge | Real | Workstation only |
| Closed loop (cloud) | Node and clients ↔ the local cloud stack (§3.1): the C# Cloud host as a native process, and the Worker, `FleetHub` Durable Object and D1 in local workerd | Real cloud code; **fakes** for Paddle, Google Play Developer API, Pub/Sub OIDC, FCM, the e-mail provider and the system browser (scripted consent) | Author; hosted CI (where the repository's local workerd suite already runs) |
| UI | Avalonia headless tests for every Desktop page (states, commands, accessibility tree, keyboard order); bUnit for Blazor pages; MAUI view-model tests | Real view models over real clients against a running node or the cloud closed loop | Author; hosted CI (headless only) |
| Performance | [15](15-performance-targets.md) | Real | Workstation; CI for size and startup |
| Fault injection | Kill node at each lifecycle point; kill supervisor; disk full; store corruption; network partition between peers; relay disconnects; clock skew; webhook replays | Real processes with controlled faults | Author; hosted CI where possible |

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

**Synthetic workloads are not fakes.** `TestLoad` (`tools/ArcForges.TestLoad`) generates deterministic CPU, memory, output and fork patterns as the *input* to the behaviour under test (scheduling, enforcement, capture, diagnosis). It replaces no external system, so every task may use it, and evidence names the workload that ran.

A fake is never used for the behaviour under test (R-TEST-001). Results from a fake-backed test are labelled `closed-loop` in evidence and never reported as real-world validation. The real billing flow on a Play-enabled emulator or device stays in the acceptance register (AR-06).

## 3. Environments and responsibilities

| Environment | Runs | Notes |
|---|---|---|
| Workstation, Windows 11 | All Windows platform and closed-loop tests; WSL bridge tests; performance | The author runs the affected suites for every task |
| Workstation, WSL2 Debian 13 | All Linux platform tests (systemd user manager, transient units, freeze, OOM); guest-node tests | Installs inside the distribution are done by the user. Tests needing new packages list them as prerequisites. |
| Hosted CI, Windows runner | Build, unit, contract, store, Windows job-object tests that need no interactive session, closed loop (headless), AOT publish, packaging | No GUI, device, browser, live-service or inference jobs |
| Hosted CI, Linux runner | Build, unit, contract, store, AOT publish, packaging. Transient-unit tests only if the runner offers a user manager; otherwise they are skipped with an explicit `requires-user-manager` reason. | The workstation's WSL2 run remains the authoritative Linux evidence |
| Emulator (local) | Android UI and billing flows with `FakeBillingClient` against the fake Play backend | Local opt-in. A Play-enabled emulator with a licence-test account (H-17) and a physical device are deferred to AR-06 and AR-08. |
| Deferred (acceptance register) | Physical LAN machines, real store purchases, real FCM delivery, production signing reputation, second OS accounts, human screen-reader sessions, macOS (out of scope) | Never reported as proven |

### 3.1 Local cloud stack

The cloud closed loop runs natively on the workstation and needs neither Docker nor WSL:
1. **Worker side.** `workerd` under Miniflare (the Cloud repository's local scripts) runs the Worker ingress, the relay routes, the `FleetHub` Durable Object, and local D1, R2 and Queue. Miniflare's local S3 endpoint, configured with test `s3Credentials`, serves the SigV4 presigned uploads of the support flow (F-C03 checks it first).
2. **C# host.** `ArcForges.Cloud` runs as a native process on a loopback port: the JIT build for most suites, the Native AOT binary for the AOT suites.
3. **Container shim.** In the local profile, the Worker's Container binding is replaced by a shim that forwards to the native host's loopback port. The host reaches D1, R2 and the Queue through the same signed internal routes as in production, with test keys. AF-CLD-01 builds the shim as part of the repository's local verification scripts.
4. **Clients.** Nodes, CLI, Desktop view models, the Blazor app (bUnit and HTTP) and the Android view models point at the local ingress.

Docker is optional (H-18). It enables only the Cloud repository's existing `test:container` diagnostics, which are never a gate. Live Cloudflare deployments are not part of any test.

Verification roles follow [AD-0014](../decisions/AD-0014-delivery-method.md) §4: the author runs targeted and affected suites, the reviewer adds only distinct evidence, hosted CI is the merge gate, and nobody repeats an identical full run on an unchanged head.

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
- **Isolation.** Each test node gets a temporary data root, a unique pipe or socket name, a unique node ID (so Windows job names cannot collide) and its own transient slice name on Linux (`arcforges-test-<id>.slice`). A fixture cleans up leftover jobs, units and processes and fails the test if any remain.

## 5. Release-candidate acceptance

The release candidate (AF-ACC-01) runs every journey J-01 to J-10 end to end with:
- **real core implementations**: node, CLI, MCP adapter, hooks, Desktop view models, cloud host, Worker and Durable Object code, Blazor and Android view models;
- **the approved external fakes** of §2 where the external system is unavailable: `FakePaddle`, `FakePlayDeveloperApi`, `FakePubSubPush`, `FakeFcm`, `FakeMailSender`, `FakeBillingClient`, `ScriptedBrowser`, `ScriptedMcpClient`, `HookPayloadFixtures`, and `PeerProcess` for other machines. A fake never replaces the behaviour under test;
- **honest labels**: results are labelled closed-loop, and every remaining real-world validation stays in the acceptance register (AR-01 to AR-16).

## 6. Acceptance evidence per task

Each delivery task's PR records:
1. the exact commands run, with their results (author);
2. the environments covered (Windows real, WSL2 real, hosted CI);
3. which acceptance criteria each test proves, by requirement ID;
4. benchmarks when a measured path changed;
5. any acceptance-register entries created or advanced, with the human prerequisite stated.

The reviewer's record lists only the distinct checks performed and the diff review result ([AD-0014](../decisions/AD-0014-delivery-method.md) §4).
