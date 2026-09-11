<a id="rule-wp-52"></a>

# WP-52 — Sole Cloudflare Workflow Harness

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion *(sequenced after `43`; numbered `52` because `00`–`51` are allocated and a retired identifier is never reused)*
> Upstream: `15`, `17`, `20`, `21`, `23`, `26`, `40`, `41`, `42`, `43`, `44` · Downstream: `31`, `49`, `50`

> **Goal.** Build the **single Cloud Harness** of [`../../architecture/17-agent-harness.md`](../../architecture/17-agent-harness.md): the turn loop, tool batching, context assembly, compaction, approval interleaving, streaming, cancellation and recovery — running in the ArcForges-AI CF Workflow, against real admission and real metering.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: AI sole loop; Cloud business ports; clients/tools. Inputs: the assigned exact Contracts packages/descriptors and actual provider artifacts; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**Why this package exists, and why it is here.** [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) moved the model loop to Cloud ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)). Its work was previously distributed across [WP-13.00](13-high-risk-technical-probes.md#rule-wp-13.00) (a Native AOT desktop agent probe), [WP-16](16-unified-execution-engine.md#rule-wp-16) (a unified Task engine that also covered agent runs), [WP-17.08](17-arcchat-independent-core.md#rule-wp-17.08)/[WP-17.09](17-arcchat-independent-core.md#rule-wp-17.09) (the turn loop and compaction, in a **Phase C** desktop package) and [WP-20.03](20-first-cross-product-workflow.md#rule-wp-20.03) (the first agent-driven workflow, in **Phase D**). **Every one of those placements is now unexecutable.** A *minimal real* Cloud host exists from [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) — real pipeline, real database, one contract endpoint — but the Harness needs the **production** host and its lease-fenced hosted services (`21`), the public surface (`23`), admission and capacity (`42`), and provider routing and settlement (`43`). None of those exists before Phase J, and a turn loop cannot admit, dispatch or settle without them.

Rather than leave a package whose steps cannot run in their stated order, the Harness is one package at its real dependency position.

**In scope.** The turn loop and its durable iteration; response classification and continuation; loop bounds and progress detection; parallel tool batching against declared conflict sets; context assembly, staleness invalidation and tool-declaration filtering; history compaction; approval interleaving across restarts; the stream buffer and its read path; crash recovery by dispatch intent; provider failure classification; and the first agent-driven cross-product workflow.

**Out of scope.** Provider routing, tariffs, normalisation and settlement (`43`). Admission, capacity and service terms (`42`). The device-side tool executor (`17`, `26`). Product capability surfaces (`18`, `20`, `33`, `36`).

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

Explicit consumers: [WP-20](20-first-cross-product-workflow.md#rule-wp-20) supplies the cross-product workflow surface, [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26) the durable device bridge, [WP-40](40-knowledge-search-and-retrieval.md#rule-wp-40) permission-aware retrieval/context, [WP-41](41-extension-platform-and-integrations.md#rule-wp-41) MCP/extension adapters, and [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) active policy. None can be assumed merely because its contract type existed in WP-03.

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
| BR-01 | **One Harness, Cloud-only** ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)). No desktop, mobile or browser assembly contains a turn loop, a planner or a provider adapter. |
| BR-02 | **The Cloud business host is Native AOT; Harness TypeScript runs on CF** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). CF Worker deployment tests apply to the loop; all C# integration ports retain the AOT artifact gate. |
| BR-03 | **A Cloud Agent Task is not a native Product Job** ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). This package owns the former; [WP-16](16-unified-execution-engine.md#rule-wp-16) owns the latter. |
| BR-04 | **Admission commits before dispatch** (`§6.1.2` of the data-model overview). Nothing crosses the dispatch barrier inside a transaction. |
| BR-05 | **Recovery is decided by dispatch intent, never by outcome absence** (`§6.3` of the harness). Retry safety is a declared capability property ([FL-08](../../requirements/05-ai-and-agent-execution.md#rule-fl-08)). |
| BR-06 | **No agent teams, sub-agents or external-agent delegation** ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08), `§9` of the harness). |
| BR-07 | **The stream buffer is transient presentation state**, never a message and never synchronised ([SB-01](../../architecture/17-agent-harness.md#rule-sb-01)). |

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

**Testing requirements.** Large context paging, permission loss, stale source, prior compaction version and unsupported capability; no raw prompts in Workflow checkpoints.

**Completion gate.** All effect decisions refer to authorized immutable context and the loop never writes stale source implicitly.

<a id="rule-wp-52.02"></a>

### WP-52.02 — Approval, cancellation and crash recovery


**What must be fully done.** Implement approval waiting with at most the selected wait/reconcile steps and seven-day bound, reauthorization on resume, explicit cancel/pause/steer controls and C# reconciliation. Use intent→owner/provider evidence→deadline→user-decision ladder; request lifetime and UI session closure do not cancel a durable Task.

**Testing requirements.** Restart Workflow/Cloud during wait/model/tool, missed wake event, expired/stale proposal, cancel race, generation rotation and late evidence.

**Completion gate.** Wait/cancel/recovery retains one canonical outcome or explicit unknownEffect; no presumed safe replay or missing hold resolution.

<a id="rule-wp-52.03"></a>

### WP-52.03 — Shared streaming with durable Task fallback


**What must be fully done.** Implement RunStream DO with the selected 4 MiB tail, 64 KiB frames, flush/TTL/marker limits and authenticated first-frame connection binding. Reauthorize every delivered frame/range through C#; stream IDs/UTF-8 byte offsets distinguish interruption, truncation, supersession and eviction. Persist invocation output before settlement and terminal Task plus final/interrupted/no-answer Chat atomically through C# ports.

**Testing requirements.** CF connection loss/DO eviction, slow consumer, permission/session revoke, duplicated offsets, output-before-settlement and final-commit crash points; replay from canonical Chat.

**Completion gate.** Stream projection never acts as message authority or determines Task state; durable final content survives loss of all CF presentation state.

<a id="rule-wp-52.04"></a>

### WP-52.04 — Provider failure and effect certainty

**What must be fully done.** The classification of `§8`, keyed on whether dispatch occurred rather than on whether bytes returned; the `unknown` path into `§6.4`; release of customer holds at the reconciliation deadline with the supplier liability retained ([UU-03](../../architecture/20-cross-system-lifecycles.md#rule-uu-03)).

**Testing requirements.** A timeout before the first token asserting **`unknown`, not a retry**; a lost response reconciled against the provider's own record; a platform-caused retry charged once to the customer and fully visible in supplier cost; a deadline expiry releasing the customer hold while retaining the supplier liability.

**Completion gate.** No failure path silently resolves `unknown` to `didNotHappen`, and no dispatched request is retried automatically.

<a id="rule-wp-52.05"></a>

### WP-52.05 — The first agent-driven cross-product workflow

**What must be fully done.** **Delete the [WP-17.01](17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint** and prove the same client and device paths against the real Harness — the fixture is removed, never adapted into production code. *(This step is also where [WP-20.03](20-first-cross-product-workflow.md#rule-wp-20.03) was relocated from, having been in Phase D where no Harness existed.)* The [canonical workflow and failure outcomes](../../assurance/end-to-end-workflow-verification.md#first-arcchat-arcnotes-workflow) apply: ArcChat is asked to produce a report; the owning product checks authorization and obtains required approval before each affected mutation; ArcNotes creates and populates the document through typed device tools; the result saves, undoes and recovers, and an artifact reference resolves.

**Testing requirements.** The full workflow end to end — request, admission, dispatch, owner authorization and required approval before mutation, document creation and block insertion, save, undo, kill, recovery and artifact resolution — with **every failure variant** exercised: device offline, approval expired, capacity exhausted mid-turn, term expiring mid-turn, and a crash after dispatch. Include the concurrent-edit/revocation and native-commit-before-Cloud-acknowledgement cases in the canonical scenario.

**Completion gate.** The full workflow passes end to end against the real Cloud host, real admission and a real provider. Every failure variant in the [canonical acceptance scenario](../../assurance/end-to-end-workflow-verification.md#first-arcchat-arcnotes-workflow) reaches its specified waiting, refusal or terminal outcome; waiting is never reported as completion, and recovery produces no duplicate effect or charge.

---

<a id="rule-wp-52.06"></a>

### WP-52.06 — Durable Cloud automation and authorised scheduling


**What must be fully done.** Implement automation definition/version, trigger schedule/event cursor, occurrence dedup and grant/budget snapshot in C# Task-owned tables. Bounded leased jobs dispatch the same RunWorkflow identity through the existing outbox; disabled/revoked automation stops future occurrences and uses defined controls for active work. Remove only the labelled WP17 automation fixture.

**Testing requirements.** Duplicate schedule/event, catch-up/coalescing, service/grant expiry, disable during wait and actual CF occurrence/usage with one linked Task.

**Completion gate.** Automation uses the single Harness and canonical occurrence ledger with the accepted commercial and recovery rules.

<a id="rule-wp-52.90"></a>
### WP-52.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement the specified Worker/Workflow/DO roles. Implement context, model/tool loop, approval, retries, cancel, streams and schedule execution against real C# transactions/ports and selected Workers AI. Remove the named [WP-17](17-arcchat-independent-core.md#rule-wp-17)/[WP-20](20-first-cross-product-workflow.md#rule-wp-20) fixtures and own the first complete AI cross-product workflow.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

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

**Required evidence addition.** [WP-52.03](#rule-wp-52.03) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Loop-bound, crash-resume, no-progress and conflict-batching results | [WP-52.00](#rule-wp-52.00) |
| Context permission, staleness and compaction results | [WP-52.01](#rule-wp-52.01) |
| Approval-across-restart, cancellation and uncertain-effect results | [WP-52.02](#rule-wp-52.02) |
| Cross-replica read, miss-is-not-eviction, takeover, realtime-disabled equivalence and buffer-lifecycle results | [WP-52.03](#rule-wp-52.03) |
| Effect-certainty classification and deadline-release results | [WP-52.04](#rule-wp-52.04) |
| Full cross-product workflow with every failure variant | [WP-52.05](#rule-wp-52.05) |
| Real automation scheduling, missed-run policy, occurrence deduplication, cancellation and fixture removal | [WP-52.06](#rule-wp-52.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-52.90](#rule-wp-52.90) and all inherited domain-specific gates must pass on the same candidate closure. Real C#/CF/R2/device integration, duplicate/lost ack/approval/restart/stream-tail/terminal-commit cases, usage and provenance. One loop and one canonical business outcome; no unexplained provider retry.

**[PG-18](../../assurance/open-gates-register.md#rule-pg-18) evidence:** [WP-52.04](#rule-wp-52.04) — Dispatch/crash unknown-effect resolution and unregistrable unsafe capabilities, together with cancellation/approval recovery in this package. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Multi-step turns execute in the single Cloud host against a real provider, and **no desktop, mobile or browser assembly contains a turn loop, a planner or a provider adapter**.
2. No unbounded loop is reachable; every bound ends the turn with a stated reason.
3. Parallel batching never violates a declared conflict, and a failure returns its siblings' real results.
4. Only acknowledged Cloud revisions enter the context pack; a pending client edit never reaches the model.
5. Compaction reduces what is sent without altering what is stored, and never loses an approval, a refusal or a user correction.
6. An approval-suspended turn survives restart of either side and resumes with revalidated context.
7. **No crash or failure path resolves an uncertain external effect to *did not happen***, and no non-idempotent capability is retried without a resolution step.
8. A capability that can produce an external effect and declares neither idempotency nor a status operation **cannot be registered**.
9. Every surface reaches identical streamed output **with realtime fully disabled**; **a read served by a replica that never wrote the stream returns correct data**; a miss is never reported as an eviction; and no buffer byte is persisted as a message.
10. The full cross-product workflow passes end to end with every failure variant reaching a stated terminal state, and **the [WP-17.01](17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint no longer exists in the codebase** — asserted structurally.

11. [WP-52.06](#rule-wp-52.06) passes against the real host, persistent occurrence records and real admission; no desktop automation scheduler or fixture runtime endpoint remains.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [15 arcchat conversation core](15-arcchat-conversation-core.md#rule-wp-15)
- [17 arcchat independent core](17-arcchat-independent-core.md#rule-wp-17)
- [20 first cross product workflow](20-first-cross-product-workflow.md#rule-wp-20)
- [21 cloud host and persistence](21-cloud-host-and-persistence.md#rule-wp-21)
- [23 public api and generated clients](23-public-api-and-generated-clients.md#rule-wp-23)
- [26 remote action and tool bridge](26-remote-action-and-tool-bridge.md#rule-wp-26)
- [40 knowledge search and retrieval](40-knowledge-search-and-retrieval.md#rule-wp-40)
- [41 extension platform and integrations](41-extension-platform-and-integrations.md#rule-wp-41)
- [42 commerce entitlement and credits](42-commerce-entitlement-and-credits.md#rule-wp-42)
- [43 managed ai routing and metering](43-managed-ai-routing-and-metering.md#rule-wp-43)
- [44 dynamic policy and configuration](44-dynamic-policy-and-configuration.md#rule-wp-44)

**Downstream — consumers of these released outputs.**

- [31 arcchat mobile android](31-arcchat-mobile-android.md#rule-wp-31)
- [49 arcchat web companion](49-arcchat-web-companion.md#rule-wp-49)
- [50 full platform production release](50-full-platform-production-release.md#rule-wp-50)

---
