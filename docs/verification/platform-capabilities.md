# Platform capabilities and evidence authority

**Status at design delivery:** V2 product implementation has not started. Source observations below are verified source facts, not runtime passes. All future V2 acceptance items are NOT_RUN. Historical V1 acceptance is preserved separately in the source audits and frozen snapshots.

## Source facts

| ID | Fact and evidence | Scope |
|---|---|---|
| V-MXC-01 | [Stable source/release/payload pins](../research/mxc-sources.json): SDK 1.0.1, schema1.0.0, commit fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2 | Source/package only |
| V-MXC-02 | [Official .NET gaps and executor contract](../research/mxc-research.md): no stable ProcessContainer ConPTY handle setter; unchanged official executor adjunct is documented | Source-supported architecture, not composed pass |
| V-MXC-03 | [Windows Job ownership](../research/mxc-research.md): MXC internal Job is private and kill-on-close; pre-exec outer resource scope needs qualification | Native combination NOT_RUN |
| V-MXC-04 | [Linux Bubblewrap](../research/mxc-research.md): policy/dependency/PTY and ingress/IPv6 restrictions are explicit | Native combination NOT_RUN |
| V-MXC-05 | [Filesystem semantics](../research/mxc-research.md): grants use supported same absolute paths; no universal redirection | Source fact; negative runtime probes still required |
| V-MXC-06 | [Lifecycle/exit source](../research/mxc-research.md): wait/dispose/kill/drain differ; terminal text is untrusted; executor exit is not payload-empty proof | Source fact; independent outer-scope verification required |
| V-MXC-07 | [AOT/distribution](../research/mxc-research.md): package TFM/native/helpers/license are inventoried | Full Native AOT artifact qualification NOT_RUN |
| V-BASE-01 | [Repository baseline](../research/baseline.md) and [runtime audit](../research/runtime-audit.md) pin actual implementations and historical delivered state | Read-only source/ledger audit |
| V-BASE-02 | [Cloud/consumer audit](../research/cloud-audit.md) pins Go capability, Web scaffolds, published consumers and schema10/11 gap | Read-only source/ledger audit |

## Design assumptions requiring qualification

| ID | Assumption | Owner and resolution |
|---|---|---|
| A-MXC-01 | Windows official executor+ConPTY+outer Job+native BaseContainer policy meets every mandatory requirement together | AFV2-MXC-02 produces evidence; AFV2-MXC-04 admits or blocks the profile |
| A-MXC-02 | Linux official typed SDK+PTY+Bubblewrap+delegated cgroup meets every mandatory requirement together | AFV2-MXC-03 produces evidence; AFV2-MXC-04 admits or blocks the profile |

## Future evidence register

| ID | Required evidence | Owner task | Status / exact protocol |
|---|---|---|
| F-AOT-01 | SDK/AOT/distribution closure | AFV2-MXC-01 | NOT_RUN — MXC-AOT-01; exact package/native/version/license/CPU architecture |
| F-MXC-01 | Windows complete profile | AFV2-MXC-02 | NOT_RUN — MXC-WIN-01..06 together; ConPTY, policy, nested Job and lifetime |
| F-MXC-02 | Linux complete profile | AFV2-MXC-03 | NOT_RUN — MXC-LNX-01..05 together; Bubblewrap, PTY, cgroup, networking and lifetime |
| F-RES-01 | Dynamic resource limits and aggregate safety | AFV2-RES-02 | NOT_RUN — Real CPU/memory saturation, child groups, reductions/increases, native readback/failure |
| F-REC-01 | Crash/reboot/unknown ownership recovery | AFV2-REC-01 | NOT_RUN — Node and supervisor death, PID reuse, duplicate handles, reboot identity and replay refusal |
| F-FILE-01 | Safe deletion and native filesystem recovery | AFV2-FILE-02 | NOT_RUN — Owned-root negative races, managed use, partial delete, quarantine, foreign path exclusion |
| F-CTR-01 | Real PostgreSQL upgrade/admission/restore | AFV2-CENTER-01 | NOT_RUN — Fresh/schema10/schema11 guarded chain with preserved floors and uncertain receipts |
| F-REMOTE-01 | Typed remote effect and grants | AFV2-CENTER-03 | NOT_RUN — Real Node+Go+PG lost reply, stale epoch, revoke, bounded template and denied arbitrary route |
| F-HOST-01 | Official/self-host entitlement separation | AFV2-HOST-01 | NOT_RUN — Self-host with official offline; official expiry while local Run survives |
| F-WEB-01 | Responsive accessibility and reconnect | AFV2-WEB-04 | NOT_RUN — Explicit local browser/assistive checks across seven pages; no browser CI |
| F-DIST-01 | Final package install and AOT identity | AFV2-DIST-01 | NOT_RUN — Both native signed/verified cohorts and actual helper/license closure |
| F-ACC-01 | Full native local product | AFV2-ACC-01 | NOT_RUN — Same final candidate on both native profiles, all mandatory positive/negative journeys |
| F-REMOTE-02 | Full remote/self-host/account acceptance | AFV2-ACC-02 | NOT_RUN — Real self-host plus approved official/provider tests; activation prerequisites separately recorded |

A future item can become proven only with exact commit/artifact hashes, OS and backend identity, native commands/results, negative cases, author and independent review. The [experiment protocol](mxc-experiments.md) supplies mandatory engine cases. Core mandatory safety/interactive failures block dependent delivery and final acceptance; they are not external business deferrals.

Design/Plan static checks and generated-code compilation are different evidence from these runtime experiments. The designated Windows/Linux host statuses for documentation PRs remain required even when product experiments are intentionally future work. No manual status reporting or security-rule change is allowed.
