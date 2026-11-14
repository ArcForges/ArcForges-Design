# V2 consolidated review and repair record

This file preserves the initial nonauthor review and the single coordinated repair batch. The initial findings below apply to the exact candidate identities in their table; they are not findings against an unexamined later commit. The paired PR descriptions record the final independent delta outcome at the actual published heads and the still-required host verification. No author check or candidate review is a protected-merge approval.

# Initial independent review — ArcForges V2 Design and Plan

Date: 2026-11-14 UTC. Reviewer: independent nonauthor subagent `/root/v2_independent_review` (ChatGPT). This is the one consolidated substantive review of the paired Design/Plan migration. It is not a native-host verification receipt or protected-merge approval.

## Reviewed identities

| Repository | Local immutable candidate | Published candidate with identical tree | Tree |
|---|---|---|---|
| ArcForges-Design | `e563762c926821aa713efe5a44833671736b9eaf` | `6c0115ba82a93830e601fc1cb352dbf67edfc82c` | `985b2ac550d99db4e5b8fd4f7ee9016befb9ce24` |
| Plan | `4e22eb17c79266e3e9cd003f3b4af9e27e0070e2` | `01fc7d954b13a00b09b077a12fcc0b94a1e38790` | `cd1649bbb00f064c106131df3c9aab02c0563cdc` |

Review used detached worktrees in the existing clones. No author document, product source, repository setting, GitHub status or credential was changed by the reviewer. Published identities were supplied by the coordinator after connector publication of the identical trees.

## Result

**Changes requested before substantive acceptance.** The product direction, source-supported MXC strategy, honest experiment gates, preserved resource assets, free local/self-host boundary, shared-consumer protections and immutable history are coherent. The findings below concern the ability to implement the stated contracts and task graph without inventing missing decisions or violating their own scope. They can be repaired in one bounded Design/Plan consistency batch; no product implementation is requested.

### R1 — P1: Correct the task path allowlists to the audited repositories

Location: Plan `delivery-graph.json`, especially `AFV2-API-01`, `AFV2-ID-01`, `AFV2-CENTER-02..04`, `AFV2-MIG-01/02`.

Several tasks authorize a different layout from the actual source they must change. `AFV2-API-01` lists `proto/**`, `packages/**`, `src/**`, `eng/**` and buf files, but Contracts stores specifications in `public/proto/**` and `internal/proto/**`, generated Go in `go/**`, and tests/vectors in `tests/**` and `fixtures/**`. Those necessary paths are outside its scope. `AFV2-ID-01` lists new `identitytests`/`httpapi` paths but omits the actual `center/internal/identityapi/**` adapter and `pages/**` surfaces. Center migration/routing tasks omit actual `fleetapi/**` registration/adapters and relevant `server/**` composition. Most decisively, `AFV2-MIG-01` allows nonexistent `src/ArcForges.Cloud.Runtime*` and `src/ArcForges.Cloud.Host*`, but excludes the actual old `src/ArcForges.Cloud/**` host, `src/ArcForges.Cloud.Storage.D1/**`, most old module projects, `center/internal/fleetapi/**` and `mobileauth/**` that its removal outcome requires.

Execution policy §4 permits ancillary solution/package/lock changes for declared modules; it does not authorize replacing these missing business/module paths. A future agent must either violate scope, create redundant adapters, or stop for repeated Plan amendments.

Repair: reconcile each affected allowlist against the pinned audit and actual source tree; identify existing retained/reworked/deleted modules and explicit new module paths. Include necessary generated clients, contract fixtures and adapter/composition tests. For legacy C# modules, list actual deletion paths or an explicit retained-consumer reason. Do not solve this by authorizing all repositories wholesale. Recheck task dependencies for the real feature slices.

### R2 — P1: Align normative task ownership and delivery order with the graph

Locations: Design `docs/architecture/09-go-center.md` §8 and opening status, `11-identity-commerce.md` §8, `10-blazor-dashboard.md` task table, and `docs/research/cloud-audit.md` §8/task boundary table; Plan `AFV2-HOST-03`.

The Center chapter assigns early migration qualification to `AFV2-MIG-01`, enrollment/channel to CENTER-01, mutations to CENTER-02 and streams to CENTER-03. The actual graph assigns those respectively to BASE-01/CENTER-01, CENTER-02, CENTER-03 and CENTER-04; MIG-01 is the final cutover and depends on completed Center/Web work. Following the chapter's ordered procedure would create a circular prerequisite. Identity/commerce similarly says HOST-01 delivers the self-host package and HOST-02 delivers operations, whereas the graph uses HOST-01 for entitlements and HOST-03 for packaging/operations. WEB-04 is omitted from the chapter ownership boundary despite owning the complete accessibility/UX qualification.

HOST-03 also says it packages the complete Go/PostgreSQL/Blazor self-host product before any WEB task is delivered. Clarify whether this is only deployment infrastructure with final Dashboard assembly in DIST-01, or move the complete bundle acceptance after WEB-04 with real dependencies; an existing probe bundle must not count as the new Dashboard.

Repair: make all current task tables and numbered sequences agree with the actual graph. Separate baseline inventory, guarded schema transition, typed routing, final cutover and final distribution. Regenerate trace/sequence after any graph changes. Historical source descriptions may stay historical; current AFV2 owner assignments must be correct.

### R3 — P1: Define a concrete local deduplication lifetime that survives receipt compaction

Locations: Design `docs/data/node-store.md` command_receipt row, `node-store.sql` command_receipt, `docs/contracts/README.md` §§2–3, `07-lifecycle-recovery.md` §9; Plan `AFV2-DATA-01`.

Known Node receipts have a normal 24-hour retention/expiry, while the lifecycle chapter leaves a choice between a bounded tombstone or rejecting expired command IDs. The wire command ID is an opaque random 128-bit ID with no authenticated issuance/expiry window. After deleting a known receipt and eventually its bounded tombstone, an old identical Start can be indistinguishable from a new command and execute again. The Cloud model explicitly retains non-executable identities until enrollment revocation invalidates replay; the local model has no equivalent concrete rule. Merely saying UNKNOWN never expires does not cover a successful Start whose client later replays after compaction.

Repair: choose an implementable local rule, for example compact only response bodies while retaining owner/command/method/digest/effect identity for the lifetime of the admitted owner epoch, reject new mutations rather than evict executable identities when the budget is exhausted, and define a safe explicit epoch retirement before keys can be purged. Alternatively define a protected freshness protocol that can reject retired IDs. State exact `expires_utc` meaning and typed replay-expired response; do not change immutable foundation fields in place. Add post-retention and post-restart replay cases to DATA-01 acceptance.

### R4 — P1: Separate transient terminal input acknowledgments from durable business commands

Locations: Design `docs/contracts/proto/arcforges/sandbox/v2/platform.proto` RunService Acquire/Write/Resize/Detach annotations, `docs/contracts/README.md` §2, `06-local-node-cli.md` §7 and `node-store.md` receipt rules.

Every terminal write is currently annotated with the same durable `(owner, command_id, canonical request hash)`/GetOperation model as Start/Delete, and the generic API rules say to persist it before native effects. The terminal chapter instead specifies only a bounded lease-generation acknowledgment window, no retained input transcript and no exactly-once promise beyond that window. These are incompatible recovery/retention contracts. Persisting a hash per tiny input frame can also retain reconstructible low-entropy input and introduces a database write path for ordinary keystrokes.

Repair: explicitly classify terminal lease/input/resize/detach operations. Prefer supervisor-memory sequence/dedup acknowledgments bound to the live lease, with stale/expired acknowledgment semantics and an explicit uncertain-input error after loss; do not persist raw input or input-derived hashes in durable receipts/audit. Specify what GetOperation can and cannot reconcile for these methods and update their annotations. Durable Run Start/Stop and file/config mutations keep their normal receipt guarantees. Add tests for lease-window expiry, Node/supervisor loss and absence of input-derived durable records.

### R5 — P2: Close the user-action-to-CLI/API gaps

Locations: Design `06-local-node-cli.md` command table, `03-sandbox-run-model.md`, `07-lifecycle-recovery.md` Sandbox operation table, `10-blazor-dashboard.md` page table, both V2 protos; Plan CLI/Core/Center tasks.

The complete local command table has only `resources show/watch`, and no grant set/list/revoke or operation-inspect command, even though the only way to enable remote management is a local grant action and the Web explicitly promises the exact local command. The Dashboard refers to `arcforges center connect`, absent from the canonical table. Required local resource configuration and doctor are also not mapped. Sandbox rename is explicitly accepted by CORE-01, but Configure only carries SandboxConfig and no display-name mutation. Device rename is promised in the Dashboard but management.v2 provides only List/Inspect/Revoke; the old Fleet rename route is slated for removal without an explicit retained or replacement mapping. Run detail promises executable/command/snapshot display but the Run wire model contains only a digest/profile ID, not a safe display or bound config/profile revision.

The lifecycle chapter also promises explicit local ERROR repair and deletion/recovery resume/cancel while the public surface never defines which existing method and request safely authorizes those operations. Reading GetOperation is reconciliation observation, not authority to restart an effect.

Repair: add an exact action→command→method map for these current functions, implement missing necessary wire fields/method semantics, and assign them to the existing task scopes/acceptance. For optional actions such as rename, either define the bounded mutation or remove the promise from current acceptance/UI. Recovery may reuse an explicitly defined local Configure/Delete same-intent path rather than add a broad repair endpoint; the exact guards and identity must be specified. No generic host-operation endpoint is needed.

### R6 — P2: Make lifecycle and telemetry models match their normative behavior

Locations: Design `docs/state-machines/machines.json`, `05-filesystem-data.md` §7, `02-mxc-integration.md` §6, `06/07` payload-start vocabulary, and `platform.proto` ResourceSnapshot/WatchUsage.

Related concrete mismatches:

- File deletion permits cancellation before quarantine back to READY, but SM-SANDBOX has no DELETING→READY transition. Any retained cancellation path must have exact no-effect/identity guards, or that unsupported promise should be removed.
- SM-TRANSFER marks export complete and immediately releases staging. The filesystem contract says the immutable export remains until CloseTransfer/expiry; releasing on the final ReadExport breaks a retry after losing the last response. Distinguish completed data transfer from snapshot release, preserving authorized replay until explicit close/expiry.
- SM-RUN has no RECOVERY_REQUIRED→FAILED path when recovery proves no payload ever started and cleanup is complete; it can only recover to RUNNING or DRAINING→EXITED, contradicting the promised definite-launch-failure classification.
- SM-LIMIT is marked non-persisted while limit_application persists its state; ensure state/persistence mapping is truthful.
- ResourceService.WatchUsage still emits OutputGap with byte offsets and Run-style epoch while its request has no resume cursor and ResourceSnapshot has no sample epoch. Define a typed sample epoch/sequence gap or explicitly specify fresh-snapshot-only stream semantics; do not reuse byte offsets as sample sequences.
- Architecture 02 still names `stop_reason` and several chapters use `payload_started=no`; the canonical wire/data fields use `termination_reason` and `NOT_STARTED`. Use one explicit mapping rather than incompatible literals. Architecture 03's absolute prohibition on joining argv also contradicts the required tested backend-specific Windows/POSIX serialization in architecture 02; prohibit raw interpolation, not the necessary safe adapter serialization.

Repair these as one contract/state consistency batch and regenerate catalogue/state README. Add small meaningful validation tests only where they protect schema/state consistency, not tests mirroring prose wording.

### R7 — P2: Name the allowed external test fixtures in the tasks that require them

Locations: Plan `delivery-graph.json` `fakes_allowed`, especially AFV2-ID-01/HOST-02 and relevant UI tasks; `execution-policy.md` §3; `acceptance-register.md` AR-10/H-04.

All 39 tasks currently say `none; native behavior is never mocked for acceptance`. The policy permits only task-listed external doubles, while the hosting acceptance expressly separates code delivery using provider fixtures from unavailable provider/domain/legal activation. No such provider/mail/browser-state fixtures are listed, so future execution either blocks development on external credentials/business inputs or violates its own fixture policy. The prohibition on mocking native isolation is correct and should stay.

Repair: enumerate only the needed external transport or rendering fixtures per applicable task, including their limits. Keep real cryptographic verification, identity/entitlement business code, PostgreSQL persistence, file/Job/cgroup/PTY behavior and final native journeys mandatory. Explicitly state which separate provider sandbox/live qualification remains unproven until activation.

## Independent checks and strengths

- Compared every frozen archive file with `git show <original-main>:<path>`: **137 Design + 36 Plan entries, zero mismatches**. Historical task states/evidence were preserved, not relabeled as V2 completion.
- Independently checked **39 pinned MXC repository-file SHA-256 values** against their exact Git objects, with no mismatch. Spot-read the stable executor/Node PTY adapter and native fallback/Job code. The no-fork official executor decision and conditional native composition are evidence-backed; no runtime pass is inferred.
- Changed-tool review diagnostics: **41 Plan tests, 38 Design checker tests, 16 V2 integrity tests passed**. Reciprocal Design/Plan validators passed with 39 tasks/47 requirements/35 RPC methods/6 state machines. These tests do not detect the semantic cross-document findings above.
- Source-versus-runtime evidence is clearly separated. Windows BaseContainer/native deny plus no DACL fallback, Linux delegated resource scope, real PTY, before-execution membership, independent descendant drain and foreground-root lifetime are all explicitly qualified by future gates.
- Free offline local execution, free self-hosted management, official-only entitlement, immutable published contracts/applied migrations, independent apps, explicit unknown effects and final old-runtime deletion are all represented.
- No product implementation, deployed database, hook, verification profile, ruleset or security-setting change is part of this candidate.

## External gates, separate from findings

The designated native Windows/Linux MCP hosts are unavailable to this session. Neither required `arcforges/windows` nor `arcforges/linux` success is established. Protoc/generated-C# compilation is also not performed in this environment. PostgreSQL DDL checks are structural only; real V2 runtime experiments belong to the future Plan and remain NOT_RUN. After content repairs, the independent delta can close substantive findings, but the PRs still need the unchanged host profiles and final exact-head review procedure. Design must merge first; Plan must then be verified against actual new Design main. No approval, merge or native pass is implied by this record.


## Coordinator repair record

The original author team repaired the seven groups in one coordinated batch; no production implementation was begun. The final independent reviewer is the same nonauthor who wrote the initial review, and must verify the concrete delta before substantive acceptance is reported in the paired PRs.

| Finding | Applied repair | Evidence location |
|---|---|---|
| R1 | Audit all 39 task allowlists; correct 32 repository arrays; use real Contracts roots, Cloud adapters/composition and all 22 legacy C# projects; classify new paths and preserve independent consumers | [Applied scope audit](../reuse/plan-scope-audit.md), current Plan graph module paths/notes |
| R2 | Align current task owners and order; Center migration precedes routing and late cutover; HOST-03 delivers infrastructure; final Go/PostgreSQL/Blazor assembly is DIST-01 after completed Web; real Center CLI comes with CENTER-02 | Architecture 09–11, graph and generated Plan sequence |
| R3 | Persistent owner epoch and protected keyed command digest; retain admitted identities for epoch lifetime; 24 hours compacts known bodies only; stale epoch/old backup refusal; explicit offline retirement and reserved safety capacity; propagate epoch through Center | [API conventions](../contracts/README.md), Node/Cloud stores, lifecycle, DATA-01 primitives and CORE-02/REC-01/CLI-01 integration acceptance |
| R4 | Four terminal methods use bounded supervisor-memory acknowledgments; consumed-sequence high-water, explicit uncertainty and no retransmission; no durable input/control hashes or GetOperation; distinguish echoed output with a no-output fixture | API annotations/conventions, CLI/lifecycle/store, CORE-03/CLI-02 |
| R5 | Complete local action map; six typed local-only CenterControl methods reuse existing identity internals; Configure name/guarded ERROR repair, original-intent Delete resume, safe Run snapshot display, transfer inspection; remove optional Device rename | [Contract catalogue](../contracts/api-catalogue.md), architecture 03/05/06/07/09/10 and task acceptance |
| R6 | No cancellation after accepted Delete; retain COMPLETE export snapshots until close/expiry; recovery-to-FAILED requires NOT_STARTED proof; Limit state is persisted and checked against SQL; fresh sample streams replace byte-gap misuse; canonical field vocabulary | [State machines](../state-machines/README.md), proto/data specifications, state-storage regression tests |
| R7 | Explicit external mail/authenticator/provider/deployment/rendering fixtures only where needed, preserving real crypto/authorization/business/PostgreSQL/native acceptance and separate live-provider activation evidence | Task fakes_allowed fields, execution policy and AR-10/H-04 |

### Evidence and remaining gates

The author semantic checker and reciprocal Plan validator cover **47 requirements, 39 planned tasks, 42 RPC methods and 6 state machines**. Node target SQL contains **17 tables**, including explicit owner-epoch identity; the Cloud specification contains **12 PostgreSQL tables**. Known-body compaction, immutable replay identities and persisted state/SQL agreement have focused specification tests. Exact final commands, test totals and independent delta findings are recorded in the PRs rather than represented as native receipts here.

The 173 frozen archive files remain byte-identical to their original Git objects. No applied migration, published package, verification hook/profile, required status, protection or independent product source is changed. Both designated native MCP host legs remain required. Protoc/generated-C# compilation is not established in this environment; PostgreSQL checks here are structural only. All MXC composed runtime qualification remains NOT_RUN in its assigned P1 tasks. Design must merge first, then Plan must be verified against the actual new Design main; missing checks block merge.

### Bounded follow-up after the repair delta

The independent delta closed R1–R7 and found one P2 acceptance-allocation regression: DATA-01 preceded the Core/security/client behaviors it was asked to prove. The coordinator split real SQLite/store fixture acceptance from CORE-02 settled native Start replay, REC-01 live-owner recovery/safety-capacity/restore integration and CLI-01 saved-command/Handshake behavior. Only DATA-01 explicitly permits a synthetic admission effect counter; later runtime acceptance remains real. The same nonauthor reviewer checks this bounded correction and the final identities in the paired PRs. The extra EOF blank line in CenterControl was also removed. This record does not claim designated-host checks or merge approval.
