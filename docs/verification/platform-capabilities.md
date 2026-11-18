# Platform capabilities and evidence authority

**Initial status at design delivery (2026-11-14):** V2 implementation had not started and all future items were NOT_RUN. Historical V1 acceptance stays separate. **Historical update (2026-11-16):** real MXC-AOT-01 candidate execution failed the then-selected Linux request-environment argv privacy check. **Current policy update (2026-11-17):** the [owner-approved local process boundary](../decisions/AD-0022-cli-sandbox-platform-pivot.md#local-process-visibility--2026-11-17-amendment) supersedes that argv-only blocker; F-AOT-01 passed fresh win-x64/linux-x64 cohort revalidation at candidate `9a9378bc` under that boundary. At that checkpoint, admission still required the complete native profiles. See the original FAILED report for the historical observation. Source observations and partial native results remain distinguished below.

**Linux native update (2026-11-17 UTC):** the H-22 full-profile experiment at
Node `50e602a83ece2c4de75d8dbd32777c7833a6eaf7` passed all **72 recorded cases
in six groups**, including the combined terminal/filesystem/network/resource
and recovery scenarios, with confirmed owned-scope cleanup. The
[dated checkpoint](mxc-experiments.md#linux-full-profile-native-checkpoint--2026-11-17-utc)
binds the original receipt and artifact hashes, host, limits and measurement
definitions. AFV2-MXC-04 consumes this F-MXC-02 evidence for the
[qualified Linux profile](#qualified-official-profiles). The permitted
namespace-denial injection was not feasible and remains explicitly NOT_RUN.
DNS evidence covers denial only.

**Windows wrapper scope update (2026-11-18):** [AD-0022](../decisions/AD-0022-cli-sandbox-platform-pivot.md#official-mxc-wrapper-boundary--2026-11-18-amendment) limits the required Windows experiment to the local MVP matrix. Keep the external selected TCP/UDP and dependent combinations unverified on the designated host. The [Plan evidence record](https://github.com/ArcForges/Plan/blob/f4767f08176526ec309de45ca10b0b361fd82e1a/docs/afv2-mxc-02-progress.md) preserves the 59 workstation passes along with the attempted and unrun cases. This evidence gap does not establish upstream lack of support.

**Windows native update (2026-11-18 UTC):** the [local wrapper checkpoint](mxc-experiments.md#windows-local-wrapper-native-checkpoint--2026-11-18-utc) at Node `fac982f628799c8905ea911bd949355072a4d2a7` passed 60/60 required cases on DEKU with owned cleanup confirmed. WIN-06 observed the default-deny effect against a calibrated host-loopback peer while the same Run exercised files, ConPTY, resources, recovery and cleanup. External selected TCP/UDP and its dependent Run combinations remain UNVERIFIED.

## Qualified official profiles

AFV2-MXC-04 registers the exact [Windows and Linux composed native receipts](mxc-experiments.md#afv2-mxc-04-profile-admission). Node records them in `eng/mxc/profiles/windows-process-executor-v1.qualification.json` and `eng/mxc/profiles/linux-bubblewrap-sdk-v1.qualification.json`. Qualification binds the profile revision, official SDK/native version 1.0.1, schema 1.0.0, artifact identities, native backend, OS and architecture to the required composed evidence. Admission also requires the applicable native prerequisites at the time of the request.

| Profile | Official support | Native evidence and scope |
|---|---|---|
| `windows-process-executor-v1` / `win-wrapper-local-v1` | Official `wxc-exec.exe` with ProcessContainer native BaseContainer/PSEC, denied paths and exact directional network policy. ConPTY and the outer Job are owned by ArcForges. BaseContainer rejects the LPAC-specific `processContainer.leastPrivilege=true` option at this pin. | Windows NT 10.0.26300.0, win-x64, final **60/60** on DEKU. Composed local default-deny includes the calibrated host-loopback peer. External selected TCP/UDP egress and its dependent combinations remain **UNVERIFIED**. Explicit pipes remain **UNVERIFIED** at full composition scope. Ingress observations cover the recorded local fixture cases. |
| `linux-bubblewrap-sdk-v1` | Official typed SDK with explicit Bubblewrap, PTY or explicit pipes, and native network helpers for selected egress. Stable Bubblewrap lacks host/public ingress and IPv6 connectivity. | Debian 13, kernel `6.12.63+deb13-amd64`, linux-x64, **72/72** on H-22. Composed default-deny and selected literal IPv4 TCP. Native selected UDP passed in a separate case. DNS observation covers denial. Explicit pipes passed a separate SDK comparison and remain **UNVERIFIED** at full composition scope. The qualifying host uses the recorded helpers, delegated systemd 257.9-1~deb13u1 user manager and cgroup v2 controls. |

Windows external selected TCP/UDP egress retains its exact request for the supported mode. Native preflight still applies and returns the actual result. A mandatory local composition or prerequisite failure blocks admission, and a request for locally verified behavior requires relevant evidence.

## Source facts

| ID | Fact and evidence | Scope |
|---|---|---|
| V-MXC-01 | [Stable source/release/payload pins](../research/mxc-sources.json): SDK 1.0.1, schema1.0.0, commit fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2 | Source/package only |
| V-MXC-02 | [Official .NET gaps and executor contract](../research/mxc-research.md): no stable ProcessContainer ConPTY handle setter; unchanged official executor adjunct is documented | Official contract, with the scoped local composition observed under F-MXC-01 |
| V-MXC-03 | [Windows Job ownership](../research/mxc-research.md): MXC internal Job is private and kill-on-close; pre-exec outer resource scope needs qualification | Native outer Job assignment, readback and cleanup observed under F-MXC-01 |
| V-MXC-04 | [Linux Bubblewrap](../research/mxc-research.md): policy/dependency/PTY and ingress/IPv6 restrictions are explicit | H-22 native combination PASS at `50e602a8`, scoped by F-MXC-02 and the qualified profile above |
| V-MXC-05 | [Filesystem semantics](../research/mxc-research.md): grants use supported same absolute paths; no universal redirection | Linux positive/negative effects observed at50e602a8 under F-MXC-02; other profiles retain their own runtime obligations |
| V-MXC-06 | [Lifecycle/exit source](../research/mxc-research.md): wait/dispose/kill/drain differ; terminal text is untrusted; executor exit is not payload-empty proof | Source fact; independent outer-scope verification required |
| V-MXC-07 | [AOT/distribution](../research/mxc-research.md): package TFM/native/helpers/license are inventoried | Real win-x64/linux-x64 Native AOT, coherent official stage, five native observations and four invalid-stage cases per host passed at9a9378bc; original FAILED report retained; no full profile claim |
| V-BASE-01 | [Repository baseline](../research/baseline.md) and [runtime audit](../research/runtime-audit.md) pin actual implementations and historical delivered state | Read-only source/ledger audit |
| V-BASE-02 | [Cloud/consumer audit](../research/cloud-audit.md) pins Go capability, Web scaffolds, published consumers and schema10/11 gap | Read-only source/ledger audit |

## Design assumptions requiring qualification

| ID | Assumption | Owner and resolution |
|---|---|---|
| A-MXC-01 | Windows official executor, ConPTY, outer Job, local native BaseContainer policy and recovery meet the required local composition together | AFV2-MXC-02 recorded the scoped DEKU native PASS. AFV2-MXC-04 qualifies the local composition with unverified optional capabilities. |
| A-MXC-02 | Linux official typed SDK+PTY+Bubblewrap+delegated cgroup meets every mandatory requirement together | AFV2-MXC-03 produced the scoped H-22 native PASS at `50e602a8`. AFV2-MXC-04 qualifies that composed profile. |

## Future evidence register

| ID | Required evidence | Owner task | Status / exact protocol |
|---|---|---|
| F-AOT-01 | SDK/AOT/distribution closure | AFV2-MXC-01 | PASS for the isolated official1.0.1 win-x64/linux-x64 cohort at9a9378bc under the [owner decision](mxc-experiments.md#owner-decision-and-resumption--2026-11-17-utc): warning-free AOT, native execution/cleanup, verified distribution closure and four negative staging cases per host. See dated revalidation evidence in mxc-experiments.md and mxc-sources.json. Original8252c8f FAILED report/argv observation remain unchanged. Repository delivery checks remain separate; no full profile admission. |
| F-MXC-01 | Windows local MVP profile | AFV2-MXC-02 | NATIVE PASS — MXC-WIN-01..06 local matrix 60/60 at final `da7f5bfcfe497a35cece41f0e97b5863481bcc56` on DEKU with owned cleanup. External selected TCP/UDP and dependent combinations remain UNVERIFIED. [Final original receipt identity and scope](mxc-experiments.md#afv2-mxc-04-profile-admission). |
| F-MXC-02 | Linux complete profile | AFV2-MXC-03 | NATIVE PASS — MXC-LNX-01..05 together at50e602a83ece2c4de75d8dbd32777c7833a6eaf7 on H-22, six groups72/72 with cleanup confirmed. [Original receipt/identity/limits](mxc-experiments.md#linux-full-profile-native-checkpoint--2026-11-17-utc). Namespace-denial injection remains NOT_RUN under the protocol's where-feasible clause; DNS is deny-only and selected IPv4 is literal address/protocol/port. The [qualified Linux profile](#qualified-official-profiles) uses this receipt. |
| F-RES-01 | Dynamic resource limits and aggregate safety | AFV2-RES-02 | NOT_RUN — Real CPU/memory saturation, child groups, reductions/increases, native readback/failure |
| F-REC-01 | Crash/reboot/unknown ownership recovery | AFV2-REC-01 | NOT_RUN — Node and supervisor death, PID reuse, duplicate handles, reboot identity and replay refusal |
| F-FILE-01 | Safe deletion and native filesystem recovery | AFV2-FILE-02 | NOT_RUN — Owned-root negative races, managed use, partial delete, quarantine, foreign path exclusion |
| F-CTR-01 | Real PostgreSQL upgrade/admission/restore | AFV2-CENTER-01 | NOT_RUN — Fresh/schema10/schema11 guarded chain with preserved floors and uncertain receipts |
| F-REMOTE-01 | Typed remote effect and grants | AFV2-CENTER-03 | NOT_RUN — Real Node+Go+PG lost reply, stale epoch, revoke, bounded template and denied arbitrary route |
| F-HOST-01 | Official/self-host entitlement separation | AFV2-HOST-01 | NOT_RUN — Self-host with official offline; official expiry while local Run survives |
| F-WEB-01 | Responsive accessibility and reconnect | AFV2-WEB-04 | NOT_RUN — Explicit local browser/assistive checks across seven pages; no browser CI |
| F-DIST-01 | Final package install and AOT identity | AFV2-DIST-01 | NOT_RUN — Both native signed/verified cohorts and actual helper/license closure |
| F-ACC-01 | Full native local product | AFV2-ACC-01 | NOT_RUN — Same final candidate on both native profiles, all journeys required by the declared matrix. Record optional capabilities without end-to-end evidence. |
| F-REMOTE-02 | Full remote/self-host/account acceptance | AFV2-ACC-02 | NOT_RUN — Real self-host plus approved official/provider tests; activation prerequisites separately recorded |

A locally demonstrated item requires exact commit/artifact hashes, OS and backend identity, native commands/results, applicable refusal cases, author and independent review. The [experiment protocol](mxc-experiments.md) supplies mandatory engine cases. Mandatory safety and interactive failures block the affected profile and dependent delivery. An unverified optional mode is reported at the scope of that mode.

Design/Plan static checks and generated-code compilation are different evidence from these runtime experiments. The designated Windows/Linux host statuses for documentation PRs remain required even when product experiments are intentionally future work. No manual status reporting or security-rule change is allowed.
