<a id="rule-wp-52"></a>

# WP-52 — Sole Cloudflare Workflow Harness

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion *(sequenced after `43`; numbered `52` because `00`–`51` are allocated and a retired identifier is never reused)*
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Build the **single Cloud Harness** of [`../../architecture/17-agent-harness.md`](../../architecture/17-agent-harness.md): the turn loop, tool batching, context assembly, compaction, approval interleaving, streaming, cancellation and recovery — running in the ArcForges-AI CF Workflow, against real admission and real metering.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: AI sole loop; Cloud business ports; clients/tools. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**Why this package exists.** WP52 produces the sole real CF model/tool loop after production Cloud/admission/metering and product capabilities. WP17 supplies named UI/transport fixtures only. Current acceptance uses independent same-application workflows; no earlier local cross-product milestone supplies a prerequisite.

Rather than leave a package whose steps cannot run in their stated order, the Harness is one package at its real dependency position.

**In scope.** The turn loop and its durable iteration; response classification and continuation; loop bounds and progress detection; parallel tool batching against declared conflict sets; context assembly, staleness invalidation and tool-declaration filtering; history compaction; approval interleaving across restarts; the stream buffer and its read path; crash recovery by dispatch intent; provider failure classification; and the first agent-driven same-application workflow.

**Out of scope.** Provider routing, tariffs, normalisation and settlement (`43`). Admission, capacity and service terms (`42`). The device-side tool executor (`17`, `26`). Product capability surfaces (`18`, `33`, `36`, `39`).

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

Explicit inputs: WP17 assistant client, WP26 one-application bridge, WP39 Slate capabilities, WP40 permission-aware own-app retrieval, WP41 extensions and WP44 policy. All are exact artifacts with real owner evidence; WP20 is future-only.

| Input | Why it matters |
|---|---|
| [`../../architecture/17-agent-harness.md`](../../architecture/17-agent-harness.md) | The complete Harness design |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) | The runtime it executes inside |
| [WP-21](21-cloud-host-and-persistence.md#rule-wp-21) output | The single host and its lease-fenced hosted services |
| [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) output | The public API surface the clients use |
| [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) output | Service term, capacity, admission (`§7.3` of the commerce architecture) |
| [WP-43](43-managed-ai-routing-and-metering.md#rule-wp-43) output | Provider adapters, supplier prices, customer tariffs, settlement |
| [WP-17](17-arcchat-independent-core.md#rule-wp-17) output | The device-side tool executor and the desktop surfaces |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **One Harness, Cloud-only** ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)). No desktop, mobile or browser assembly contains a turn loop, a planner or a provider adapter. |
| <a id="rule-br-02"></a>BR-02 | **The Cloud business host is Native AOT; Harness TypeScript runs on CF** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). CF Worker deployment tests apply to the loop; all C# integration ports retain the AOT artifact gate. |
| <a id="rule-br-03"></a>BR-03 | **A Cloud Agent Task is not a native Product Job** ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). This package owns the former; [WP-16](16-unified-execution-engine.md#rule-wp-16) owns the latter. |
| <a id="rule-br-04"></a>BR-04 | **Admission commits before dispatch** (`§6.1.2` of the data-model overview). Nothing crosses the dispatch barrier inside a transaction. |
| <a id="rule-br-05"></a>BR-05 | **Recovery is decided by dispatch intent, never by outcome absence** (`§6.3` of the harness). Retry safety is a declared capability property ([FL-08](../../requirements/05-ai-and-agent-execution.md#rule-fl-08)). |
| <a id="rule-br-06"></a>BR-06 | **No agent teams, sub-agents or external-agent delegation** ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08), `§9` of the harness). |
| <a id="rule-br-07"></a>BR-07 | **The stream buffer is transient presentation state**, never a message and never synchronised ([SB-01](../../architecture/17-agent-harness.md#rule-sb-01)). |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `ArcForges-AI/src/workflows/RunWorkflow.ts` | The turn loop, batching, context assembly, compaction, recovery |
| `src/Cloud/ArcForges.Cloud.Modules.Task/` | Task/run/step/iteration, automation occurrence and approval persistence; owns the `task` schema and exposes its module API |
| `src/Cloud/ArcForges.Cloud.Modules.Agent/` | Reuses provider/model/routing policy APIs from the routing package; it does not write Task tables |
| `src/Cloud/ArcForges.Cloud.Modules.Chat/` | The canonical committed message write path ([CW-02](../../architecture/data-model/00-data-model-overview.md#rule-cw-02)) |
| `src/Cloud/ArcForges.Cloud.PublicApi/` | Canonical Task/Chat operations and authenticated internal business ports |
| `ArcForges-AI/src/streams/RunStream.ts` | Disposable bounded presentation tail, authenticated live/catch-up and terminal markers |
| `src/Cloud/ArcForges.Cloud.BackgroundJobs/` | C# dispatch/control/reconciliation jobs; CF alone owns the loop |
| `tests/Cloud.Tests.Integration/` | Loop, recovery, streaming, compaction and workflow suites |

**Major types introduced.** `TurnLoop`, `TurnIteration`, `ToolCallBatch`, `ConflictSet`, `ContextPack`, `CompactionRecord`, `StreamBuffer`, `DispatchIntent`, `EffectCertainty`, `ResolutionLadder`.

---

## 5. Required implementation work

<a id="rule-wp-52.00"></a>

### WP-52.00 — The turn loop, batching and bounds


**What must be fully done.** Implement the sole RunWorkflow with deterministic Workflow identity, C# claim/epoch/generation and actual deployed Worker version. Persist iteration/context references and model/tool dispatch intent before effects; record immutable outcome receipts before continuation. Apply selected model/tool/parallel/progress/time/step budgets and declared conflict sets, including 60-second execution lease renewed every 20 seconds during long awaits.

**Testing requirements.** Real Workflow with forced duplicate start, replay, 120-second model await, lease loss/stale outcome, no-progress and every bound; no automatic effect retry after intent.

**Completion gate.** Exactly one fenced loop advances a Task under its frozen config with bounded checkpoints and a visible reason for every stop/wait.

<a id="rule-wp-52.01"></a>

### WP-52.01 — Context assembly and compaction


**What must be fully done.** Assemble context through authorized C# ports in the fixed order, page under one snapshot hash and retain immutable source pins/content origins. Filter invocable capabilities before model declaration, disclose budget truncation and store derived compaction refs. Before mutation, revalidate the source/revision and active grant.

**Testing requirements.** Large context paging, permission loss, stale source, prior compaction version and unsupported capability; no raw prompts in Workflow checkpoints. Run model 05 context vectors (under budget, compaction, protected overflow, changed branch) through typed TranscriptWindow/CompactionRecord inputs, plus wrong role/tool-pair, hash and origin-installation negatives. Assert [HC-09](../../architecture/17-agent-harness.md#rule-hc-09) refusal and no customer debit for compaction; exercise both inline and transient-object input.

**Completion gate.** All effect decisions refer to authorized immutable context and the loop never writes stale source implicitly. All four context vectors and typed role/pairing/large-input cases pass against the real Harness.

<a id="rule-wp-52.02"></a>

### WP-52.02 — Approval, cancellation and crash recovery


**What must be fully done.** Implement approval waiting with at most the selected wait/reconcile steps and seven-day bound, reauthorization on resume, explicit cancel/pause/steer controls and C# reconciliation. Use intent→owner/provider evidence→deadline→user-decision ladder; request lifetime and UI session closure do not cancel a durable Task.

**Testing requirements.** Restart Workflow/Cloud during wait/model/tool, missed wake event, expired/stale proposal, cancel race, generation rotation and late evidence.

**Completion gate.** Wait/cancel/recovery retains one canonical outcome or explicit unknownEffect; no presumed safe replay or missing hold resolution.

<a id="rule-wp-52.03"></a>

### WP-52.03 — Generated streaming and durable output


**What must be fully done.** Implement execution.readOutput/watchOutput, transient-turn admission/ack/purge and DO projections from annex 10/model 05; Cloud histories commit canonically, local histories recover verified transient output without Cloud Chat bodies.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration. Run model 05 context vectors (under budget, compaction, protected overflow, changed branch) through typed TranscriptWindow/CompactionRecord inputs, plus wrong role/tool-pair, hash and origin-installation negatives. Assert [HC-09](../../architecture/17-agent-harness.md#rule-hc-09) refusal and no customer debit for compaction; exercise both inline and transient-object input.

**Completion gate.** Stream projection never acts as message authority or determines Task state; Cloud-history final content survives projection loss. Local/temporary output survives reconnect within its declared retention while key/body exist; missing/expired content produces the explicit unavailable state without losing its durable outcome/usage receipt or rerunning the request. All four context vectors and typed role/pairing/large-input cases pass against the real Harness.

<a id="rule-wp-52.04"></a>

### WP-52.04 — Provider failure and effect certainty

**What must be fully done.** The classification of `§8`, keyed on whether dispatch occurred rather than on whether bytes returned; the `unknown` path into `§6.4`; release of customer holds at the reconciliation deadline with the supplier liability retained ([UU-03](../../architecture/20-cross-system-lifecycles.md#rule-uu-03)).

**Testing requirements.** A timeout before the first token asserting **`unknown`, not a retry**; a lost response reconciled against the provider's own record; a platform-caused retry charged once to the customer and fully visible in supplier cost; a deadline expiry releasing the customer hold while retaining the supplier liability.

**Completion gate.** No failure path silently resolves `unknown` to `didNotHappen`, and no dispatched request is retried automatically.

<a id="rule-wp-52.05"></a>

### WP-52.05 — Complete own-application execution proof

**What must be fully done.** Run two end-to-end oracles: ArcNotes embedded assistant processes its own selected document and local/cloud history; Android/Web explicitly target an authorized ArcNotes installation for an approved Notes command. Include typed transcript/compaction, promotion/export, binary streams and offline recovery.

**Testing requirements.** Protected-context overflow, stale summary/branch, large transient object, forged tool history, interrupted output/final hash, lost ack, app restart, revoke/epoch change and refused cross-product target.

**Completion gate.** Published Platform/Contracts/Cloud/AI/Mobile/Web producers complete the declared paths; no WP20/cross-product workflow is used as acceptance.

---

<a id="rule-wp-52.06"></a>

### WP-52.06 — Durable Cloud automation and authorised scheduling


**What must be fully done.** Implement automation definition/version, trigger schedule/event cursor, occurrence dedup and grant/budget snapshot in C# Task-owned tables. Bounded leased jobs dispatch the same RunWorkflow identity through the existing outbox; disabled/revoked automation stops future occurrences and uses defined controls for active work. Remove only the labelled WP17 automation fixture.

**Testing requirements.** Duplicate schedule/event, catch-up/coalescing, service/grant expiry, disable during wait and actual CF occurrence/usage with one linked Task.

**Completion gate.** Automation uses the single Harness and canonical occurrence ledger with the accepted commercial and recovery rules.

**Required implementation and closure from the final review.** Implement and independently verify [05-cloudflare-integration](../../architecture/contracts/05-cloudflare-integration.md). Close paid Slate transcription from actual WP39 selected-audio upload through CF Whisper, normal C# metering/final artifact and explicit local subtitle adoption. Exercise partial/unknown outcome, cancellation, budget bound, origin and no raw video upload. Verify paged exact CF purge inventory, stale controls/late evidence, seven-day wait budget guards and post-backup unsafe-effect quarantine. Provide real active/waiting/unknown states for WP50 recovery; permit declared waiting/unknown terminality rather than forcing success/failure. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-52.90"></a>
### WP-52.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement the specified Worker/Workflow/DO roles. Implement context, model/tool loop, approval, retries, cancel, streams and schedule execution against real C# transactions/ports and selected Workers AI. Remove the named [WP-17](17-arcchat-independent-core.md#rule-wp-17)/[WP-17](17-arcchat-independent-core.md#rule-wp-17) fixtures and own the first complete AI same-application workflow.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Real C#/CF/R2/device integration, duplicate/lost ack/approval/restart/stream-tail/terminal-commit cases, usage and provenance. One loop and one canonical business outcome; no unexplained provider retry.

**Completion gate.** Real C#/CF/R2/device integration, duplicate/lost ack/approval/restart/stream-tail/terminal-commit cases, usage and provenance. One loop and one canonical business outcome; no unexplained provider retry. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Task, run, plan, step, attempt, approval; the `CompactionRecord` derived store |
| Protocol | `task.readStream`; `task.outputAppended` payload; the turn operations |
| UI | Streaming display, approval prompts, admission reasons — all client-side rendering of Cloud state |
| Security | Every tool invocation passes the pipeline; MCP content stays untrusted data |
| Platform | C# ports require Native AOT proof; TypeScript Workflow requires actual CF deployment proof |
| Migration | `CompactionRecord` is derived and rebuildable; losing it costs compute, never content |
| Compatibility | The turn and stream contracts are consumed by Desktop, Web and Mobile alike |

---

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-52.90](#rule-wp-52.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

**Required evidence addition.** [WP-52.03](#rule-wp-52.03) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Loop-bound, crash-resume, no-progress and conflict-batching results | [WP-52.00](#rule-wp-52.00) |
| Context permission, staleness and compaction results | [WP-52.01](#rule-wp-52.01) |
| Approval-across-restart, cancellation and uncertain-effect results | [WP-52.02](#rule-wp-52.02) |
| Cross-replica read, miss-is-not-eviction, takeover, realtime-disabled equivalence and buffer-lifecycle results | [WP-52.03](#rule-wp-52.03) |
| Effect-certainty classification and deadline-release results | [WP-52.04](#rule-wp-52.04) |
| Full same-application workflow with every failure variant | [WP-52.05](#rule-wp-52.05) |
| Real automation scheduling, missed-run policy, occurrence deduplication, cancellation and fixture removal | [WP-52.06](#rule-wp-52.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-52.90](#rule-wp-52.90) |



---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-52.90](#rule-wp-52.90) and all inherited domain-specific gates must pass on the same candidate closure. Real C#/CF/R2/device integration, duplicate/lost ack/approval/restart/stream-tail/terminal-commit cases, usage and provenance. One loop and one canonical business outcome; no unexplained provider retry.

**[PG-18](../../assurance/open-gates-register.md#rule-pg-18) evidence:** [WP-52.04](#rule-wp-52.04) — Dispatch/crash unknown-effect resolution and unregistrable unsafe capabilities, together with cancellation/approval recovery in this package. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Multi-step turns execute in the sole CF RunWorkflow against the selected Workers AI binding, with C# owning canonical admission/state/settlement, and **no desktop, mobile or browser assembly contains a turn loop, a planner or a provider adapter**.
2. No unbounded loop is reachable; every bound ends the turn with a stated reason.
3. Parallel batching never violates a declared conflict, and a failure returns its siblings' real results.
4. Only acknowledged Cloud revisions enter the context pack; a pending client edit never reaches the model.
5. Compaction reduces what is sent without altering what is stored, and never loses an approval, a refusal or a user correction.
6. An approval-suspended turn survives restart of either side and resumes with revalidated context.
7. **No crash or failure path resolves an uncertain external effect to *did not happen***, and no non-idempotent capability is retried without a resolution step.
8. A capability that can produce an external effect and declares neither idempotency nor a status operation **cannot be registered**.
9. Every surface converges to the same authoritative final answer/artifact with realtime disabled. Disposable CF tails may be truncated/expired with explicit state; any C# replica reads canonical Task pointers/final outcome, and no buffer byte becomes a message without owner commit.
10. The full same-application workflow passes end to end with every failure variant reaching its specified terminal, waiting, paused or unknown-effect state and an executable recovery path, and **the [WP-17.01](17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint no longer exists in the codebase** — asserted structurally.

11. [WP-52.06](#rule-wp-52.06) passes against the real host, persistent occurrence records and real admission; no desktop automation scheduler or fixture runtime endpoint remains.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [AST.19](../delivery/lanes/assistant.md#task-ast-19) | [WP-52.05](52-cloud-harness.md#rule-wp-52.05) (all work except the parts mapped to DEV.13, HAR.05) | [AST.11](../delivery/lanes/assistant.md#task-ast-11) (artifact) |
| [AST.20](../delivery/lanes/assistant.md#task-ast-20) | [WP-52.06](52-cloud-harness.md#rule-wp-52.06) (all work except the parts mapped to HAR.06, HAR.91) | [AST.14](../delivery/lanes/assistant.md#task-ast-14) (artifact) |
| [DEV.13](../delivery/lanes/device-bridge.md#task-dev-13) | [WP-52.05](52-cloud-harness.md#rule-wp-52.05) (all work except the parts mapped to AST.19, HAR.05) | [DEV.02](../delivery/lanes/device-bridge.md#task-dev-02) (artifact), [DEV.03](../delivery/lanes/device-bridge.md#task-dev-03) (artifact), [DEV.04](../delivery/lanes/device-bridge.md#task-dev-04) (artifact), [DEV.05](../delivery/lanes/device-bridge.md#task-dev-05) (artifact), [DEV.06](../delivery/lanes/device-bridge.md#task-dev-06) (artifact), [DEV.12](../delivery/lanes/device-bridge.md#task-dev-12) (artifact) |
| [HAR.00](../delivery/lanes/harness.md#task-har-00) | [WP-52.00](52-cloud-harness.md#rule-wp-52.00) (full) | [CLOUD.01](../delivery/lanes/cloud.md#task-cloud-01) (artifact), [CON.15](../delivery/lanes/contracts.md#task-con-15) (contract), [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract), [CLOUD.05](../delivery/lanes/cloud.md#task-cloud-05) (artifact) |
| [HAR.01](../delivery/lanes/harness.md#task-har-01) | [WP-52.01](52-cloud-harness.md#rule-wp-52.01) (full) | [CON.11](../delivery/lanes/contracts.md#task-con-11) (contract) |
| [HAR.02](../delivery/lanes/harness.md#task-har-02) | [WP-52.02](52-cloud-harness.md#rule-wp-52.02) (full) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract) |
| [HAR.03](../delivery/lanes/harness.md#task-har-03) | [WP-52.03](52-cloud-harness.md#rule-wp-52.03) (full)<br>[WP-52](52-cloud-harness.md#rule-wp-52) Sec.8 gate item 9: every surface converges to the same authoritative final answer/artifact with realtime disabled (package-level obligation contribution) | [AIR.05](../delivery/lanes/ai-routing.md#task-air-05) (artifact) |
| [HAR.04](../delivery/lanes/harness.md#task-har-04) | [WP-52.04](52-cloud-harness.md#rule-wp-52.04) (full) | [AIR.06](../delivery/lanes/ai-routing.md#task-air-06) (contract) |
| [HAR.05](../delivery/lanes/harness.md#task-har-05) | [WP-52.05](52-cloud-harness.md#rule-wp-52.05) (all work except the parts mapped to AST.19, DEV.13)<br>[WP-52.90](52-cloud-harness.md#rule-wp-52.90) (structural assertion that the [WP-17.01](17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint no longer exists (Sec.8 gate item 10)) | [AST.11](../delivery/lanes/assistant.md#task-ast-11) (artifact), [DEV.08](../delivery/lanes/device-bridge.md#task-dev-08) (artifact), [AND.24](../delivery/lanes/android.md#task-and-24) (artifact), [WEB.27](../delivery/lanes/web.md#task-web-27) (artifact), [AIR.00](../delivery/lanes/ai-routing.md#task-air-00) (artifact), [NOTES.12](../delivery/lanes/arcnotes.md#task-notes-12) (artifact), [APP.03](../delivery/lanes/app-composition.md#task-app-03) (artifact) |
| [HAR.06](../delivery/lanes/harness.md#task-har-06) | [WP-52.06](52-cloud-harness.md#rule-wp-52.06) (automation definition/version, trigger schedule/event cursor, occurrence dedup, grant/budget snapshot, bounded leased dispatch through the existing outbox, disable/revoke control, and removal of the labelled [WP-17](17-arcchat-independent-core.md#rule-wp-17) automation fixture -- excluding the Slate transcription closure scenario)<br>[WP-52](52-cloud-harness.md#rule-wp-52) Final-review closure paragraph: paid Slate transcription end-to-end, CF purge inventory paging, seven-day wait guards, post-backup unsafe-effect quarantine, real active/waiting/unknown states for [WP-50](50-full-platform-production-release.md#rule-wp-50) recovery (package-level obligation contribution) | [COM.05](../delivery/lanes/commerce.md#task-com-05) (artifact) |
| [HAR.90](../delivery/lanes/harness.md#task-har-90) | [WP-52.90](52-cloud-harness.md#rule-wp-52.90) (remaining aggregation/receipt beyond HAR.05's structural assertion)<br>[WP-52](52-cloud-harness.md#rule-wp-52) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure: ordinary persistent/temporary ChatTurn and AgentTask through the same RunWorkflow, pure-read vs promoted-effectful mode (package-level obligation contribution) | none |
| [HAR.91](../delivery/lanes/harness.md#task-har-91) | [WP-52.06](52-cloud-harness.md#rule-wp-52.06) (the Slate transcription closure paragraph from the final-review addendum)<br>[WP-52](52-cloud-harness.md#rule-wp-52) Final-review closure paragraph: paid Slate transcription end-to-end, CF purge inventory paging, seven-day wait guards, post-backup unsafe-effect quarantine, real active/waiting/unknown states for [WP-50](50-full-platform-production-release.md#rule-wp-50) recovery (package-level obligation contribution) | [AIR.09](../delivery/lanes/ai-routing.md#task-air-09) (artifact), [SLATE.30](../delivery/lanes/arcslate.md#task-slate-30) (artifact), [AIR.08](../delivery/lanes/ai-routing.md#task-air-08) (artifact) |

**Consumers outside this package:** [AND.24](../delivery/lanes/android.md#task-and-24), [CLOUD.67](../delivery/lanes/cloud.md#task-cloud-67), [OPS.03](../delivery/lanes/operations.md#task-ops-03), [REL.06](../delivery/lanes/release.md#task-rel-06), [SLATE.30](../delivery/lanes/arcslate.md#task-slate-30), [SLATE.32](../delivery/lanes/arcslate.md#task-slate-32), [WEB.27](../delivery/lanes/web.md#task-web-27).

<!-- delivery-graph:end -->

## [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure

Execute ordinary persistent/temporary ChatTurn and AgentTask through the same real RunWorkflow, pure-read vs promoted effectful mode, transient source expiry/cleanup and platform-funded protected compaction. Every prior client/bridge fixture is replaced by actual C#/CF/model/R2 owner integration. The referenced normative profile and producer stage matrix are binding inputs. Record independent positive/negative vectors and actual owner integration at this WP's assigned stage; a mock cannot close a real-provider/device requirement.
