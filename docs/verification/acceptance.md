# Verification and acceptance contract

## Design/Plan migration acceptance

The current migration changes only Design, Plan and their necessary validation tools. Its observable result is one current English specification and one AFV2 task graph with source-pinned assets, official MXC facts/limitations, explicit experiments, APIs/state/storage models, all removal/compatibility paths and independently reviewed task details. The frozen V1 graph/ledger and Design bytes remain unchanged. All new product tasks begin planned.

Run both repository validators and all tooling unittests, generate API/state/sequence documents, check links/references/archive hashes and two-way requirement/task coverage. The Design full profile still restores pinned protoc, compiles all protos and generated C# with AOT compatibility checks. SQLite target DDL is executed structurally; PostgreSQL target DDL receives static structural checks only, and real PostgreSQL upgrade/restore is future task F-CTR-01. Never call those static checks a successful migration.

Required native host checks use the unchanged repository eng/verify.py profiles at exact pushed SHAs. Design merges first; Plan is then verified against actual Design main on both hosts. An independent reviewer reads the complete paired result and fixes are resolved at the final head. Missing hosts/statuses prevent merge; an authored review alone is not a merge-gate pass.

## Product acceptance layers

[AD-0023](../decisions/AD-0023-current-dependency-baseline.md) adds a documents-first dependency baseline. AFV2-ENV-01 owns the seven-repository latest-stable upgrade and local/CI parity evidence (Plan AR-13) before the product roots resume. Its implementation begins after this paired policy amendment merges. The dated original source audit and MXC research remain evidence of their recorded versions; changed components require new admission evidence and the composed P1 native gates.

| Layer | What proves it | Owner |
|---|---|---|
| Current dependency baseline | Complete official-source version/artifact inventory, compatible shared producers/consumers, local/CI fingerprints and exact-head required native profiles for all seven delivery repositories | AFV2-ENV-01 |
| Official engine admission | Exact stable artifact/source/license/AOT receipt and full composed Windows/Linux tests | AFV2-MXC-01..04 |
| Core state and receipts | Real stores, locks, failure points, identity/revision/dedup and state-transition tests | AFV2-DATA-01, AFV2-CORE-01, AFV2-CORE-02, AFV2-REC-01 |
| Terminal | Real TTY detection, full-screen redraw, Ctrl+C, resize, EOF, exclusive writer, detach and output GAP | AFV2-CORE-03, AFV2-CLI-02 |
| Resources | Host reserve, multi-Sandbox grants, native saturation/readback, stale/mismatch/error and pressure/preemptibility | AFV2-RES-01, AFV2-RES-02, AFV2-RES-03 |
| Data safety | Native opened-root/no-follow/identity, bounded transfers, partial commit, managed-use delete and recovery | AFV2-FILE-01, AFV2-FILE-02 |
| Remote security | Actual Go/PostgreSQL/Node with explicit enrollment/grants/templates, stale epoch, revoke and lost-response reconciliation | AFV2-CENTER-01, AFV2-CENTER-02, AFV2-CENTER-03, AFV2-CENTER-04 |
| Business boundary | Free/offline local; self-host independent; official hosted access gated; account/expiry never kills local work | AFV2-ID-01, AFV2-HOST-01, AFV2-HOST-02, AFV2-HOST-03 |
| UI | Seven pages with real APIs; responsive keyboard/focus/accessibility; offline/stale/error/unknown flow | AFV2-WEB-01..04 |
| Removal and compatibility | Zero obsolete runtime routes/projects, immutable public artifacts/history, protected independent consumers, real schema/restore tests | AFV2-MIG-01, AFV2-MIG-02 |
| Release | Coherent install/update/rollback artifacts plus all mandatory native and remote journeys on same candidate | AFV2-DIST-01, AFV2-DIST-02, AFV2-ACC-01, AFV2-ACC-02 |

## Performance evidence

Measure source/artifact/OS/profile, CPU/RAM and helper configuration; cold and warm launch latency with p50/p95 and sample count; Node/supervisor idle CPU and resident/commit memory; workload resource overhead; terminal throughput/backpressure and dropped/gap count; time to bounded stop/empty; sample cadence cost. Compare the same workload against an unsandboxed reference only in an isolated benchmark fixture, never as a product fallback. There is no invented zero-overhead promise or arbitrary universal pass threshold. Detect regressions against the accepted P1 baseline and justify any required cap.

## Allowed doubles and unresolved work

Pure algorithm tests use explicit deterministic inputs. External email/payment/hosting transport may use the task's listed controlled fixtures during development, while cryptography, authorization, business state, file operations, persistence, audit and recovery remain real. These fixtures never prove live external configuration. Required kernel/terminal/resource/data safety is never mocked or deferred as successful acceptance.

No macOS/device/GUI/browser/live-service/inference CI is added. Necessary interactive Web/native tests are explicit local opt-in in approved venues. No 24-hour or analogous wall-clock development wait is reinstated; retention/expiry semantics use clocks/fixtures plus the distinct real environment check where necessary.

Final activation depends on owner-controlled pricing/provider/legal/domain settings and explicit approval. Their absence need not block code design or permissible dark development, but official public service cannot be claimed deployed/accepted without them. All remaining items live in Plan's acceptance register with specific Blocks and owner columns.
