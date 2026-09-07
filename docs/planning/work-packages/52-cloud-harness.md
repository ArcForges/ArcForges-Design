<a id="rule-wp-52"></a>

# WP-52 — The Cloud Harness

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion *(sequenced after `43`; numbered `52` because `00`–`51` are allocated and a retired identifier is never reused)*
> Upstream: `15`, `17`, `20`, `21`, `23`, `26`, `40`, `41`, `42`, `43`, `44` · Downstream: `31`, `49`, `50`

> **Goal.** Build the **single Cloud Harness** of [`../../architecture/17-agent-harness.md`](../../architecture/17-agent-harness.md): the turn loop, tool batching, context assembly, compaction, approval interleaving, streaming, cancellation and recovery — running in `ArcForges.Cloud.Host`, against real admission and real metering.

---

## 1. Scope and purpose

**Why this package exists, and why it is here.** [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) moved the model loop to Cloud ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)). Its work was previously distributed across [WP-13.00](13-high-risk-technical-probes.md#rule-wp-13.00) (a Native AOT desktop agent probe), [WP-16](16-unified-execution-engine.md#rule-wp-16) (a unified Task engine that also covered agent runs), [WP-17.08](17-arcchat-independent-core.md#rule-wp-17.08)/[WP-17.09](17-arcchat-independent-core.md#rule-wp-17.09) (the turn loop and compaction, in a **Phase C** desktop package) and [WP-20.03](20-first-cross-product-workflow.md#rule-wp-20.03) (the first agent-driven workflow, in **Phase D**). **Every one of those placements is now unexecutable.** A *minimal real* Cloud host exists from [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) — real pipeline, real database, one contract endpoint — but the Harness needs the **production** host and its lease-fenced hosted services (`21`), the public surface (`23`), admission and capacity (`42`), and provider routing and settlement (`43`). None of those exists before Phase J, and a turn loop cannot admit, dispatch or settle without them.

Rather than leave a package whose steps cannot run in their stated order, the Harness is one package at its real dependency position.

**In scope.** The turn loop and its durable iteration; response classification and continuation; loop bounds and progress detection; parallel tool batching against declared conflict sets; context assembly, staleness invalidation and tool-declaration filtering; history compaction; approval interleaving across restarts; the stream buffer and its read path; crash recovery by dispatch intent; provider failure classification; and the first agent-driven cross-product workflow.

**Out of scope.** Provider routing, tariffs, normalisation and settlement (`43`). Admission, capacity and service terms (`42`). The device-side tool executor (`17`, `26`). Product capability surfaces (`18`, `20`, `33`, `36`).

---

## 2. Required inputs and dependencies

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
| BR-02 | **The Cloud host is JIT, not AOT** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). No AOT constraint applies to Harness code, and no gate here asks for an AOT publish. |
| BR-03 | **A Cloud Agent Task is not a native Product Job** ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). This package owns the former; [WP-16](16-unified-execution-engine.md#rule-wp-16) owns the latter. |
| BR-04 | **Admission commits before dispatch** (`§6.1.2` of the data-model overview). Nothing crosses the dispatch barrier inside a transaction. |
| BR-05 | **Recovery is decided by dispatch intent, never by outcome absence** (`§6.3` of the harness). Retry safety is a declared capability property ([FL-08](../../requirements/05-ai-and-agent-execution.md#rule-fl-08)). |
| BR-06 | **No agent teams, sub-agents or external-agent delegation** ([EA-01](../../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08), `§9` of the harness). |
| BR-07 | **The stream buffer is transient presentation state**, never a message and never synchronised ([SB-01](../../architecture/17-agent-harness.md#rule-sb-01)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.AgentRuntime/` | The turn loop, batching, context assembly, compaction, recovery |
| `src/Cloud/ArcForges.Cloud.Modules.Task/` | Task/run/step/iteration, automation occurrence and approval persistence; owns the `task` schema and exposes its module API |
| `src/Cloud/ArcForges.Cloud.Modules.Agent/` | Reuses provider/model/routing policy APIs from the routing package; it does not write Task tables |
| `src/Cloud/ArcForges.Cloud.Modules.Chat/` | The stream buffer and the committed message write path ([CW-02](../../architecture/data-model/00-data-model-overview.md#rule-cw-02)) |
| `src/Cloud/ArcForges.Cloud.PublicApi/` | `task.readStream` and the turn operations |
| `src/Cloud/ArcForges.Cloud.BackgroundJobs/` | The harness runner as a lease-fenced hosted service |
| `tests/Cloud.Tests.Integration/` | Loop, recovery, streaming, compaction and workflow suites |

**Major types introduced.** `TurnLoop`, `TurnIteration`, `ToolCallBatch`, `ConflictSet`, `ContextPack`, `CompactionRecord`, `StreamBuffer`, `DispatchIntent`, `EffectCertainty`, `ResolutionLadder`.

---

## 5. Required implementation work

<a id="rule-wp-52.00"></a>

### WP-52.00 — The turn loop, batching and bounds

**What must be fully done.** The durable turn loop of `§2`: every iteration persisted before the next begins; response classification and continuation decisions (`§3.2`); every loop bound ending the turn with a stated reason (`§3.3`); no-progress detection (`§3.4`); and parallel tool batching against declared conflict sets with an undeclared capability treated as exclusive (`§2.1`).

**Testing requirements.** A crash-injection suite resuming from each loop point with no duplicate effect and no duplicate charge; a bounds suite proving no unbounded loop is reachable; a repetition test proving no-progress termination; a conflict suite proving two writes to one target never run in parallel while two independent reads do; a partial-failure test proving a failing call returns its siblings' real results.

**Completion gate.** No unbounded loop is reachable, every bound ends the turn with a stated reason, and parallel batching never violates a declared conflict.

<a id="rule-wp-52.01"></a>

### WP-52.01 — Context assembly and compaction

**What must be fully done.** Assembly in the order of `§4.2` — references first, content last — with permission applied per source; revision stamping and staleness invalidation before a write (`§4.3`); tool-declaration filtering so an uninvocable capability is never declared (`§4.4`); budget and disclosed truncation (`§4.5`); and history compaction as a derived `CompactionRecord` (`§4.6`).

**Testing requirements.** A permission test asserting a refused source contributes nothing including to counts; a staleness test asserting a changed revision is reported to the model rather than silently substituted; **a test asserting only acknowledged Cloud revisions enter the pack** and a pending client edit never does ([PK-04](../../architecture/17-agent-harness.md#rule-pk-04), [I-498](../../requirements/01-normative-glossary-and-invariants.md#rule-i-498)); a long-conversation suite proving the stored branch is byte-identical before and after compaction; a decision-retention test proving a refused proposal is not re-proposed.

**Completion gate.** Context is bounded, permission-filtered and revision-stamped; compaction reduces what is sent without altering what is stored and never loses an approval, a refusal or a user correction.

<a id="rule-wp-52.02"></a>

### WP-52.02 — Approval, cancellation and crash recovery

**What must be fully done.** Durable approval suspension surviving a restart of either side, with context revalidated on resume (`§5`); cancellation at every point leaving a determinate state (`§6.2`); and recovery decided by **dispatch intent** with the resolution ladder of `§6.4` — declared idempotency, owner status operation, provider record, deadline, user decision.

**Testing requirements.** An approval-suspended turn surviving restart of both sides; cancellation at each loop point; **a crash after dispatch but before any outcome, asserting the state is `unknown` and is not retried automatically**; a capability declaring neither idempotency nor a status operation, asserting it **cannot be registered** ([UR-02](../../architecture/17-agent-harness.md#rule-ur-02)); a device-tool crash resolved by the device command log.

**Completion gate.** No crash path resolves an uncertain external effect to *did not happen*, and no non-idempotent capability is retried without a resolution step.

<a id="rule-wp-52.03"></a>

### WP-52.03 — Shared streaming with durable Task fallback

**What must be fully done.** Implement the logged shared PostgreSQL presentation tables and full readStream contract in [Harness §7](../../architecture/17-agent-harness.md#7-streaming). Distinguish stream completed/truncated/superseded/evicted from Task state. Persist each invocation output before settlement, and final/interrupted message or no-answer with terminal Task atomically. Document WAL/backup retention and restore purge; no process-socket takeover assumption.

**Testing requirements.** Different replica read, no chunk yet, full buffer while Task running, completed tool-only invocation, expired state marker, lost provider process, cancellation, Unicode offset boundary, stale fence and restored database. With realtime disabled all clients reach authoritative output/status; no nonexistent final-message fetch or blind redispatch.

**Completion gate.** Every stream loss/state has a bounded authoritative fallback, each billed delivered invocation has durable evidence, and Task completion has its final-message/no-answer receipt. Presentation retention and physical backups make consistent claims.

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

**What must be fully done.** Implement the Cloud automation definition/version, trigger schedule/event cursor, unique occurrence receipt, grant/budget snapshot and Task linkage. The same single Harness executes occurrences. Use one bounded lease/fence per schedule partition, transactional occurrence deduplication and catch-up/coalescing policy; re-evaluate service, consent and limits before dispatch. Disable/revoke stops future occurrences and explicitly handles in-flight work. Remove [WP-17.04](17-arcchat-independent-core.md#rule-wp-17.04) fixture transitions.

**Testing requirements.** Two replicas fire the same occurrence; crash after occurrence creation/before Task start; missed schedule and clock rollback; cascade and concurrency saturation; disable during run; expired grant/service and exhausted Run budget. Test with the real host/provider and desktop client, and no fixture scheduler.

**Completion gate.** Every authorised occurrence has at most one durable Task, no event storm creates unbounded work and no desktop executes AI scheduling. Failed/blocked occurrences have visible history and remediation.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Task, run, plan, step, attempt, approval; the `CompactionRecord` derived store |
| Protocol | `task.readStream`; `task.outputAppended` payload; the turn operations |
| UI | Streaming display, approval prompts, admission reasons — all client-side rendering of Cloud state |
| Security | Every tool invocation passes the pipeline; MCP content stays untrusted data |
| Platform | Cloud JIT only; **no AOT constraint applies to this package** |
| Migration | `CompactionRecord` is derived and rebuildable; losing it costs compute, never content |
| Compatibility | The turn and stream contracts are consumed by Desktop, Web and Mobile alike |

---

## 7. Tests and verification evidence

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

- [15 — ArcChat Conversation and Project Core](15-arcchat-conversation-core.md)
- [17 — ArcChat Independent Core V1A](17-arcchat-independent-core.md)
- [20 — First Real Cross-Product Workflow](20-first-cross-product-workflow.md)
- [21 — Cloud Host, Modules, Persistence and Migrations](21-cloud-host-and-persistence.md)
- [23 — Public API Surface and Generated Clients](23-public-api-and-generated-clients.md)
- [26 — Device Presence, Remote Action and the Tool Bridge](26-remote-action-and-tool-bridge.md)
- [40 — Knowledge, Search and Retrieval](40-knowledge-search-and-retrieval.md)
- [41 — Extension Platform and Integrations](41-extension-platform-and-integrations.md)
- [42 — Commerce, Entitlement and Credits](42-commerce-entitlement-and-credits.md)
- [43 — Cloud AI Routing, Metering and Settlement](43-managed-ai-routing-and-metering.md)
- [44 — Dynamic Policy and Configuration Control Plane](44-dynamic-policy-and-configuration.md)

**Downstream — these consume this package’s completed output.**

- [31 — ArcChat Mobile Android Remote Closed Loop](31-arcchat-mobile-android.md)
- [49 — ArcChat Web Companion](49-arcchat-web-companion.md)
- [50 — Full-Platform Production Release](50-full-platform-production-release.md)
