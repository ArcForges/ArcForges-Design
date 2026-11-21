# Verification and acceptance contract

## Design/Plan migration acceptance

The current migration changes only Design, Plan and their necessary validation tools. Its observable result is one current English specification and one AFV2 task graph with source-pinned assets, official MXC facts/limitations, explicit experiments, APIs/state/storage models, all removal/compatibility paths and independently reviewed task details. The frozen V1 graph/ledger and Design bytes remain unchanged. All new product tasks begin planned.

Run both repository validators and all tooling unittests, generate API/state/sequence documents, check links/references/archive hashes and two-way requirement/task coverage. The Design full profile still restores pinned protoc, compiles all protos and generated C# with AOT compatibility checks. SQLite target DDL is executed structurally; PostgreSQL target DDL receives static structural checks only, and real PostgreSQL upgrade/restore is future task F-CTR-01. Never call those static checks a successful migration.

Required native host checks use the unchanged repository eng/verify.py profiles at exact pushed SHAs. Design merges first; Plan is then verified against actual Design main on both hosts. An independent reviewer reads the complete paired result and fixes are resolved at the final head. Missing hosts/statuses prevent merge; an authored review alone is not a merge-gate pass.

## Product acceptance layers

[AD-0023](../decisions/AD-0023-current-dependency-baseline.md) records the owner-clarified toolchain baseline. AFV2-ENV-01 preserves completed upgrades and finishes necessary mainstream toolchains and local/CI parity (Plan AR-13) before product roots resume. Ordinary compilation, tests, security, provenance and required native checks remain; changed native components still require their relevant composed P1 qualification.

| Layer | What proves it | Owner |
|---|---|---|
| Current toolchain baseline | Actual selected necessary tools and local/CI fingerprints, compatible locked producer/consumer resolution and the normal required exact-head checks for all seven delivery repositories; preserve completed upgrades without extra individually-latest transitive or upstream-tag qualification | AFV2-ENV-01 |
| Official engine admission | Exact stable artifact/source/license/AOT receipt and required native Windows local MVP and Linux composed tests | AFV2-MXC-01..04 |
| Core state and receipts | Real stores, locks, failure points, identity/revision/dedup and state-transition tests | AFV2-DATA-01, AFV2-CORE-01, AFV2-CORE-02, AFV2-REC-01 |
| Terminal | Real TTY detection, full-screen redraw, Ctrl+C, resize, EOF, exclusive writer, detach and output GAP | AFV2-CORE-03, AFV2-CLI-02 |
| Resources | Host reserve, multi-Sandbox grants, native saturation/readback, stale/mismatch/error and pressure/preemptibility | AFV2-RES-01, AFV2-RES-02, AFV2-RES-03 |
| Data safety | Native opened-root/no-follow/identity, bounded transfers, partial commit, managed-use delete and recovery | AFV2-FILE-01, AFV2-FILE-02 |
| Remote security | Actual Go/PostgreSQL/Node with explicit enrollment/grants/templates, stale epoch, revoke and lost-response reconciliation | AFV2-CENTER-01, AFV2-CENTER-02, AFV2-CENTER-03, AFV2-CENTER-04 |
| Business boundary | Free/offline local; self-host independent; official hosted access gated; account/expiry never kills local work | AFV2-ID-01, AFV2-HOST-01, AFV2-HOST-02, AFV2-HOST-03 |
| UI | Seven pages with real APIs; responsive keyboard/focus/accessibility; offline/stale/error/unknown flow | AFV2-WEB-01..04 |
| Removal and compatibility | Zero obsolete runtime routes/projects, immutable public artifacts/history, protected independent consumers, real schema/restore tests | AFV2-MIG-01, AFV2-MIG-02 |
| Release | Coherent install/update/rollback artifacts plus all mandatory native and remote journeys in the declared matrix on the same candidate | AFV2-DIST-01, AFV2-DIST-02, AFV2-ACC-01, AFV2-ACC-02 |

### Official MXC wrapper acceptance

The [2026-11-18 AD-0022 amendment](../decisions/AD-0022-cli-sandbox-platform-pivot.md#official-mxc-wrapper-boundary--2026-11-18-amendment) defines the Windows MVP matrix. Require actual composed terminal, filesystem/control isolation, resource enforcement and lifetime/recovery on native Windows with the official executor. Exercise local policy effects and official refusal paths using the [protocol](mxc-experiments.md#3-windows-experiments). Separately retain the Windows external selected TCP/UDP attempts and unrun dependent cases as unverified. Neither admission of other capabilities nor completion of AFV2-ACC-01 depends on those optional results. The existing Linux native matrix and its scoped evidence still apply.

Published claims and acceptance receipts distinguish official contract support, local native verification and modes without end-to-end evidence. Supported policy requests retain their semantics through the official backend, and the receipt reflects actual errors or outcome certainty. An unverified mode cannot satisfy a request for verified behavior. Required native safety failures still block the affected profile. Repository-required verification, independent review and separate outward-facing activation approval still apply.

### Local process visibility

Apply the [2026-11-17 AD-0022 amendment](../decisions/AD-0022-cli-sandbox-platform-pivot.md#local-process-visibility--2026-11-17-amendment) to MXC admission: visibility of explicitly requested environment values in official/helper argv to the trusted owning host user or administrator is not a standalone blocker. Preserve and classify that native observation; do not hide it or rewrite its old result. Implicit host credential inheritance, unauthorized payload/cross-Sandbox access and raw secret disclosure into ordinary logs, public Plan/GitHub records or exported evidence still fail their applicable requirements.

F-AOT-01 passed fresh isolated win-x64/linux-x64 cohort revalidation at9a9378bc under this boundary; see the dated evidence in [mxc-experiments.md](mxc-experiments.md) and [mxc-sources.json](../research/mxc-sources.json). The old Linux argv-only FAILED decision is superseded, while its report, `argv_sentinel_observed=true`, hashes and cleanup facts remain unchanged. This policy decision does not establish package/license closure, complete terminal/resource/isolation composition or a delivered task; continue the existing required checks and native experiments without adding an argv-absence gate for trusted local inspection.

## Performance evidence

Measure source/artifact/OS/profile, CPU/RAM and helper configuration; cold and warm launch latency with p50/p95 and sample count; Node/supervisor idle CPU and resident/commit memory; workload resource overhead; terminal throughput/backpressure and dropped/gap count; time to bounded stop/empty; sample cadence cost. Compare the same workload against an unsandboxed reference only in an isolated benchmark fixture, never as a product fallback. There is no invented zero-overhead promise or arbitrary universal pass threshold. Detect regressions against the accepted P1 baseline and justify any required cap.

## Allowed doubles and unresolved work

Pure algorithm tests use explicit deterministic inputs. External email/payment/hosting transport may use the task's listed controlled fixtures during development, while cryptography, authorization, business state, file operations, persistence, audit and recovery remain real. These fixtures never prove live external configuration. Required kernel/terminal/resource/data safety is never mocked or deferred as successful acceptance.

WEB-04 development may use deterministic component and transport fixtures. Local browser renders may document presentation and interaction at the measured viewport when the browser intercepts all fixture requests and aborts unmatched requests. The fixture starts no listening server, opens no port and connects to no real Center, PostgreSQL, Node or remote endpoint. Classify these checks as development evidence. Keep real browser accessibility and assistive observations open in F-WEB-01 and Plan AR-09 until exercised. The remaining connected reconnect checks use the real Dashboard, Center/PostgreSQL and designated native Node profiles. ACC-02 retains the full integrated effects. Unverified mandatory cases continue to block final acceptance claims. Required exact-head repository checks and independent review continue during development.

No macOS/device/GUI/browser/live-service/inference CI is added. Necessary interactive Web/native tests are explicit local opt-in in approved venues. No 24-hour or analogous wall-clock development wait is reinstated; retention/expiry semantics use clocks/fixtures plus the distinct real environment check where necessary.

Final activation depends on owner-controlled pricing/provider/legal/domain settings and explicit approval. Their absence need not block code design or permissible dark development, but official public service cannot be claimed deployed/accepted without them. All remaining items live in Plan's acceptance register with specific Blocks and owner columns.
