# AI and Agent Runtime Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (agent framework only on AOT-validated surfaces), **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (remote execution), **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** (economic model), **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** (MCP)
> Companions: [`../requirements/05-ai-and-agent-execution.md`](../requirements/05-ai-and-agent-execution.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`16-billing-and-commerce-architecture.md`](16-billing-and-commerce-architecture.md)

One Cloud Harness, one Task model, one metering path. Tool locality varies; the model loop never leaves Cloud (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**, [I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)).

---

## 1. Component map

**Every model call, the single Harness and all durable agent orchestration are Cloud** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**). The desktop contributes UI, authorised local tool execution and product-local jobs. There is no second agent runtime anywhere.

```
Desktop / React / Kotlin Android: intent, Task/approval UI, draft/ack state
    -> C# Native AOT: Task/Chat/Agent/Commerce/Entitlement authority
        -> transactional dispatch outbox -> CF RunWorkflow
            -> authorized context + typed tool proposals + Workers AI
            -> C# intent/outcome/settlement/finalization ports
Desktop tool executor pulls durable ToolRequests from C#,
re-authorizes through the owner, commits, and reports actual effect.
Native ProductJobs own capture/render/analysis; no model loop.
CF RunStream DO carries live presentation only; C# owns final facts.
```

| # | Rule |
|---|---|
| <a id="rule-cm-01"></a>CM-01 | **There is one Task model and one Harness, both Cloud-owned** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**). Tool *locality* varies; the model loop does not ([I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)). |
| <a id="rule-cm-02"></a>CM-02 | **No desktop, mobile or browser client runs a model loop, holds provider credentials or plans agent work.** A client proposes intent and executes authorised tools. |
| <a id="rule-cm-03"></a>CM-03 | **The credit ledger is always cloud-side and always ArcForges-owned** ([RT-04](../requirements/05-ai-and-agent-execution.md#rule-rt-04) in the AI requirements). A gateway's dashboard is never the business ledger. |
| <a id="rule-cm-04"></a>CM-04 | **A Cloud Agent Task and a native Product Job are different things** ([I-121](../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). A render, a capture, an index rebuild and an export are product jobs: they invoke no model, consume no AI capacity, and are owned and recovered by the product that runs them. |
| <a id="rule-cm-05"></a>CM-05 | **Product AI entry points call the Cloud AI surface directly** with minimal authorised context (`§4.5` of the product scope). They do not require ArcChat Desktop and do not constitute a second orchestrator. |
| <a id="rule-cm-06"></a>CM-06 | **Official inference requires an active paid service term** ([C-03](../requirements/00-product-scope-and-portfolio.md#rule-c-03), `§8.7` of the commerce requirements). No local mode, desktop setting, credit balance or self-host flag can authorise it. |

---

## 2. Agent runtime under AOT

[P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) places the only model/tool loop in CF Workflow. Both the C# business ports and desktop typed tool path are Native AOT; framework constraints below apply to the C# boundary, while CF execution follows [the integration contract](contracts/05-cloudflare-integration.md).

| # | Rule |
|---|---|
| <a id="rule-ao-01"></a>AO-01 | **Built-in agents, tools and capabilities are statically registered or source-generated.** |
| <a id="rule-ao-02"></a>AO-02 | **Arbitrary runtime assembly scanning, dynamic proxies and runtime code generation are prohibited** in the ArcChat main process. |
| <a id="rule-ao-03"></a>AO-03 | **Third-party executable extensions run out of process by default** ([EX-01](../requirements/08-extensions-and-developer-platform.md#rule-ex-01) in the extension requirements), so they may use any runtime while the host stays a Native AOT deliverable. |
| <a id="rule-ao-04"></a>AO-04 | **An agent framework feature is enabled only on surfaces validated by AOT analysis and a real publish** — never assumed from a debug build. |
| <a id="rule-ao-05"></a>AO-05 | **A capability is exposed to the model through an explicitly generated binding**, not through runtime reflection over method signatures. |
| <a id="rule-ao-06"></a>AO-06 | **Where a framework feature cannot be made AOT-safe, the surface is narrowed or the feature is replaced** — the desktop is not silently downgraded to JIT while still being described as AOT. |

---

## 3. Capability registry

```
Static contribution manifests (readable before start-up)
        +
Runtime instance registrations (availability, health, contract set)
        =
Capability Registry  →  filtered by intent, permission, entitlement, policy, budget
                     →  a small relevant tool set exposed to the model
```

| # | Rule |
|---|---|
| <a id="rule-cr-01"></a>CR-01 | **The full catalogue is never handed to the model** ([CE-01](../requirements/05-ai-and-agent-execution.md#rule-ce-01) in the AI requirements). Hundreds of tool schemas per turn degrade quality and explode cost. |
| <a id="rule-cr-02"></a>CR-02 | **Selection is a pipeline**: intent and capability discovery within the frozen owning or explicitly targeted application and authorized Cloud scope → a small relevant capability set → invoke. |
| <a id="rule-cr-03"></a>CR-03 | **Capability metadata drives behaviour**, not the model's inference: execution shape, effect semantics, retry semantics, cancellation semantics, preview support, checkpoint support, compensation support, risk and scope (`§4.2` of the contracts architecture). |
| <a id="rule-cr-04"></a>CR-04 | **Invocation ordering is fixed**: native capability → trusted connector, MCP or API → computer use as an advanced fallback (`§8.1` of the ArcChat requirements). |
| <a id="rule-cr-05"></a>CR-05 | **A capability's availability is dynamic** and reflects installation, running state, health, compatibility, permission, entitlement and policy ([AC-04](02-contracts-and-protocols.md#rule-ac-04) in the contracts architecture). |

---

## 4. Task engine

### 4.1 Structure

```
Intent
 └── Task            durable, owned, one authoritative owner
      └── Run        one execution attempt; freezes an Execution Snapshot at start
           ├── Plan Revision (retained, reasoned)
           │    └── Step (DAG)
           │         └── Attempt
           │              └── Capability Invocation / AI Request / ProductJobRef / Gate / Wait
           └── Checkpoints, budget reservation, trace
```

| # | Rule |
|---|---|
| <a id="rule-te-01"></a>TE-01 | **Task, run, plan, step and attempt are separate persisted entities** ([I-080](../requirements/01-normative-glossary-and-invariants.md#rule-i-080)–[I-085](../requirements/01-normative-glossary-and-invariants.md#rule-i-085)). |
| <a id="rule-te-02"></a>TE-02 | **A run freezes its execution snapshot at start** ([EX-05](../requirements/05-ai-and-agent-execution.md#rule-ex-05) in the AI requirements): intent version, profile version, skill versions, model and routing policy, permission policy, budget, execution target, workspace and realm, input bindings, automation version, **and the resolved policy and tariff decisions**. |
| <a id="rule-te-03"></a>TE-03 | **One active run per task** ([EX-04](../requirements/05-ai-and-agent-execution.md#rule-ex-04) there). |
| <a id="rule-te-04"></a>TE-04 | **Plan revisions are retained with categorised reasons** ([EX-06](../requirements/05-ai-and-agent-execution.md#rule-ex-06) there). |
| <a id="rule-te-05"></a>TE-05 | One model loop advances per Run. Bounded independent tool calls may run concurrently and join before the loop continues; dependency records support recovery without requiring a general DAG scheduler ([EX-08](../requirements/05-ai-and-agent-execution.md#rule-ex-08) of the AI requirements). |
| <a id="rule-te-06"></a>TE-06 | **State is `LifecycleState + Reason facet`**, so adding a wait reason never changes the state machine (`§2.1` there). |
| <a id="rule-te-07"></a>TE-07 | **Task authority never migrates** ([OW-02](../requirements/05-ai-and-agent-execution.md#rule-ow-02)). All agent Tasks are Cloud-owned. Device execution is an owner command or ProductJob referenced by the Cloud step, never a local agent child Task. |

### 4.2 Persistence

| # | Rule |
|---|---|
| <a id="rule-tp-01"></a>TP-01 | **Task, run, plan, step, attempt, approval, steering event, budget reservation and trace entry are all durable**, on the owner's side. |
| <a id="rule-tp-02"></a>TP-02 | **A process crash leaves an interrupted run that enters recovery evaluation** ([RV-01](../requirements/05-ai-and-agent-execution.md#rule-rv-01)–[RV-03](../requirements/05-ai-and-agent-execution.md#rule-rv-03) there), never a blanket retry. |
| <a id="rule-tp-03"></a>TP-03 | **A cloud worker crash does not lose a task** ([RV-05](../requirements/05-ai-and-agent-execution.md#rule-rv-05) there). |
| <a id="rule-tp-04"></a>TP-04 | **The task snapshot is the authoritative read surface**, carrying revision and sequence ([SN-01](../requirements/05-ai-and-agent-execution.md#rule-sn-01), [SN-02](../requirements/05-ai-and-agent-execution.md#rule-sn-02) there). |
| <a id="rule-tp-05"></a>TP-05 | **Realtime progress is notification only** ([SN-03](../requirements/05-ai-and-agent-execution.md#rule-sn-03) there). |

### 4.3 Idempotency

| Identity | Scope |
|---|---|
| `CommandId` | The logical write action — stable across attempts |
| `InvocationId` | This actual call |
| `AttemptId` | This execution try of a step |
| Provider attempt id | This upstream request try |

**A write retried after an ambiguous failure re-sends the same `CommandId`**, and the owner deduplicates ([ID-01](../requirements/05-ai-and-agent-execution.md#rule-id-01) there). **Effect certainty** — `NotApplied`, `Applied`, `Unknown` — governs whether retry is even permitted ([FL-07](../requirements/05-ai-and-agent-execution.md#rule-fl-07) there).

---

## 5. Context assembly

```
Explicit attachments  ·  pinned context  ·  project context  ·  temporary context
        ↓ scope resolution (explicit → project → profile → nothing)
        ↓ knowledge policy filter (searchable · AI retrieval · managed AI processing)
        ↓ permission filter (authorization-aware retrieval)
        ↓ retrieval (hybrid: lexical + semantic + metadata, with budget and per-source cap)
        ↓ revalidation against the authoritative owner
        ↓ evidence assembly (bound to source, revision, anchor, permission decision)
        ↓ Context Pack  → the model
```

| # | Rule |
|---|---|
| <a id="rule-ca-01"></a>CA-01 | **There is no ambient default scope** ([AS-02](../requirements/06-knowledge-search-and-retrieval.md#rule-as-02) in the knowledge requirements). |
| <a id="rule-ca-02"></a>CA-02 | **Scope expansion is visible and enters the retrieval trace** ([AS-05](../requirements/06-knowledge-search-and-retrieval.md#rule-as-05), [AS-06](../requirements/06-knowledge-search-and-retrieval.md#rule-as-06) there). |
| <a id="rule-ca-03"></a>CA-03 | **References are retrieved first; content is materialised last** ([CP-02](../requirements/06-knowledge-search-and-retrieval.md#rule-cp-02) there). |
| <a id="rule-ca-04"></a>CA-04 | **An automation's scope freezes into the run's evidence scope** ([AS-07](../requirements/06-knowledge-search-and-retrieval.md#rule-as-07) there). |
| <a id="rule-ca-05"></a>CA-05 | **Cache isolation is a security requirement**: user-derived prompt cache is workspace-scoped; only genuinely public content is reused across workspaces ([CO-03](../requirements/05-ai-and-agent-execution.md#rule-co-03) in the AI requirements). |
| <a id="rule-ca-06"></a>CA-06 | **Conversation compaction is context engineering, not memory** ([HM-03](../requirements/products/arcchat.md#rule-hm-03) in the ArcChat requirements). |
| <a id="rule-ca-07"></a>CA-07 | Indexed knowledge uses acknowledged owner revisions. Separately approved bounded transient input uses SourceConsentRef and the exact source/purpose/hash/expiry profile; it is not sync or index enrollment. Pending Notes edits cannot be passed off as an acknowledged revision. Missing/denied context is disclosed, and enabling AI alone never uploads local content. |

---

## 6. Provider routing

Providers are reached with **deployment-operator credentials only**. End-user BYOK does not exist in any form ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04) of the commerce requirements, [I-015](../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired).

```
Logical AI Request  (Cloud, authorised, service term verified)
   -> resolve model (explicit pin honoured; Auto routes within its cost class)
   -> resolve supplier price version applicable at dispatch
   -> resolve customer retail tariff snapshot and pin it to the Run/request
   -> admission: capacity + credits + concurrency + provider budget, reserved atomically
   -> resolve the pinned Workers AI binding/model in the sole CF RunWorkflow
   -> Provider Attempt 1 ... N
   -> usage normalisation -> supplier cost record + customer settlement + ledger entries
```

| # | Rule |
|---|---|
| <a id="rule-pr-01"></a>PR-01 | **Provider and model are separate axes** ([I-116](../requirements/01-normative-glossary-and-invariants.md#rule-i-116)). The source axis is gone: there is exactly one source, the operator-funded Cloud provider set. |
| <a id="rule-pr-02"></a>PR-02 | **An explicitly pinned model is never substituted** ([RT-08](../requirements/05-ai-and-agent-execution.md#rule-rt-08) in the AI requirements). The provider route may change; the model may not. |
| <a id="rule-pr-03"></a>PR-03 | **Auto routing is bounded by cost class, policy and task budget** ([RT-06](../requirements/05-ai-and-agent-execution.md#rule-rt-06), [BG-08](../requirements/05-ai-and-agent-execution.md#rule-bg-08) there). |
| <a id="rule-pr-04"></a>PR-04 | **Fallback stays within the tariff class or asks before escalating price** ([RT-07](../requirements/05-ai-and-agent-execution.md#rule-rt-07) there). |
| <a id="rule-pr-05"></a>PR-05 | **Supplier price and customer tariff are resolved separately and never derived from one another** ([MT-06](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-06)). The supplier version applies at dispatch; the customer snapshot pins to the Run. |
| <a id="rule-pr-06"></a>PR-06 | Workers AI is the only admitted model supplier. No AI Gateway failover/bypass or hidden provider/model substitution exists. An unavailable model fails with its durable reason; choosing a different admitted model is an explicit new request. |
| <a id="rule-pr-07"></a>PR-07 | **`Logical AI Request ≠ Provider Attempt ≠ Step Attempt`** ([LG-03](../requirements/05-ai-and-agent-execution.md#rule-lg-03) there, [MT-02](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02)). |
| <a id="rule-pr-08"></a>PR-08 | **Model availability is policy, not health** ([I-361](../requirements/01-normative-glossary-and-invariants.md#rule-i-361)), and a task snapshots its model policy decision ([PA-07](../requirements/11-policy-and-configuration.md#rule-pa-07) in the policy requirements). |
| <a id="rule-pr-09"></a>PR-09 | **An emergency model suspension may interrupt future invocations inside a running run** — the single documented exception to snapshot immutability ([PA-08](../requirements/11-policy-and-configuration.md#rule-pa-08) there). |
| <a id="rule-pr-10"></a>PR-10 | **A route with no configured price for a billable category cannot be dispatched** ([DC-05](../requirements/11-policy-and-configuration.md#rule-dc-05), [MT-15](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-15)). There is no assumed zero rate and no silent default. |

---

## 7. Metering and budget

```
Task start
 → estimate → reserve from the credit ledger (Available → Reserved)
 → execute; each logical request debits actual usage at the locked tariff
 → completion: settle actual, release the remainder
 → hard stop at exhaustion; no negative balance ever
```

| # | Rule |
|---|---|
| <a id="rule-mb-01"></a>MB-01 | **Reservation precedes execution** ([CR-20](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-20) there), which is what prevents concurrent tasks from collectively overdrawing. |
| <a id="rule-mb-02"></a>MB-02 | The single Cloud Run shares one authorised total across its bounded invocations and concurrent tool calls. No multi-agent run, delegation or agent-team budget exists. |
| <a id="rule-mb-03"></a>MB-03 | **Three records per request**: usage, upstream cost, credit debit ([LG-01](../requirements/05-ai-and-agent-execution.md#rule-lg-01) there). |
| <a id="rule-mb-04"></a>MB-04 | **Every request binds a tariff version** ([TR-03](../requirements/05-ai-and-agent-execution.md#rule-tr-03) there), so any historical charge is exactly recomputable. |
| <a id="rule-mb-05"></a>MB-05 | **A run locks its tariff snapshot at start** ([TR-04](../requirements/05-ai-and-agent-execution.md#rule-tr-04) there); mid-run upstream price changes are absorbed. |
| <a id="rule-mb-06"></a>MB-06 | **Fixed-precision sub-credit accounting**; per-request rounding up is prohibited ([CD-03](../requirements/05-ai-and-agent-execution.md#rule-cd-03) there). |
| <a id="rule-mb-07"></a>MB-07 | **Platform-caused retries are not charged to the user** ([CU-03](../requirements/05-ai-and-agent-execution.md#rule-cu-03) there). |
| <a id="rule-mb-08"></a>MB-08 | **Internal platform AI — routing classifiers, embedding, reranking, safety, health, cost prediction — never debits user credits** ([CU-01](../requirements/05-ai-and-agent-execution.md#rule-cu-01), [CU-02](../requirements/05-ai-and-agent-execution.md#rule-cu-02) there). |
| <a id="rule-mb-09"></a>MB-09 | **An agent cannot raise its own budget** ([BG-07](../requirements/05-ai-and-agent-execution.md#rule-bg-07) there). |
| <a id="rule-mb-10"></a>MB-10 | **Three ledgers stay separate**: provider cost, customer credit, payment/revenue ([I-011](../requirements/01-normative-glossary-and-invariants.md#rule-i-011)). |

---

## 8. Approval and steering integration

| # | Rule |
|---|---|
| <a id="rule-as-01"></a>AS-01 | **An approval gate is a Step**, not an out-of-band interruption. The run enters `Waiting` with reason `Approval` and `AutoResume = false` ([ST-01](../requirements/05-ai-and-agent-execution.md#rule-st-01) there). |
| <a id="rule-as-02"></a>AS-02 | **The approval binds the action snapshot including target revision and a parameter digest** ([AP-02](08-security-architecture.md#rule-ap-02) in the security architecture). |
| <a id="rule-as-03"></a>AS-03 | **A revision change invalidates the approval**; the action is rebased, the preview regenerated, approval re-requested ([AP-04](../requirements/05-ai-and-agent-execution.md#rule-ap-04) in the AI requirements). |
| <a id="rule-as-04"></a>AS-04 | **Steering produces an immutable event** that may trigger a plan revision; the original intent is never rewritten ([SG-02](../requirements/05-ai-and-agent-execution.md#rule-sg-02), [SG-03](../requirements/05-ai-and-agent-execution.md#rule-sg-03) there). |
| <a id="rule-as-05"></a>AS-05 | **Steering application timing is explicit** — applied, queued to a safe point, or not applicable ([SG-05](../requirements/05-ai-and-agent-execution.md#rule-sg-05) there). |
| <a id="rule-as-06"></a>AS-06 | **A denied approval does not automatically fail the task** ([AP-06](../requirements/05-ai-and-agent-execution.md#rule-ap-06) there). |

---

## 9. Tool locality and remote execution

Placement no longer describes where the model loop runs — it always runs in Cloud ([I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)). It describes **where an individual tool executes**.

| Tool locality | Executed by | Reached how |
|---|---|---|
| **Cloud tool** | The owning C# module | CF invokes the typed tool/admission port; C# executes its owner handler and commits an outcome |
| **Device tool** | The explicitly targeted application's own authorized in-process tool executor | Durable `ToolRequest` pulled by the device (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**) |

| # | Rule |
|---|---|
| <a id="rule-pl-01"></a>PL-01 | **Every Task is Cloud-owned.** There is no local, hybrid or auto *task placement*; the only variable is each tool's locality. |
| <a id="rule-pl-02"></a>PL-02 | **A tool declares its locality**, and a tool that requires the device is never silently substituted by a cloud approximation. |
| <a id="rule-pl-03"></a>PL-03 | **A device tool with no eligible online device enters `WaitingForDevice`** with a stated reason and a bounded wait ([RX-02](../requirements/03-cloud-services-and-sync.md#rule-rx-02) in the cloud requirements). Waiting consumes no model capacity ([AC-05](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-05)). |
| <a id="rule-pl-04"></a>PL-04 | **Remote execution is a durable `ToolRequest` pulled by the desktop, re-authorised locally, answered with an idempotent `ToolResult`** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**, `§10` of the cloud architecture). Cloud never connects to a device. |
| <a id="rule-pl-05"></a>PL-05 | **A device tool never uploads local-only data merely to make a cloud alternative possible** ([OW-08](../requirements/05-ai-and-agent-execution.md#rule-ow-08) in the AI requirements). If the data cannot leave, the tool runs on the device or the step fails with a reason. |
| <a id="rule-pl-06"></a>PL-06 | **A cloud failure never silently performs an external side effect on a desktop** ([OW-09](../requirements/05-ai-and-agent-execution.md#rule-ow-09) there), and the reverse is equally prohibited. |
| <a id="rule-pl-07"></a>PL-07 | **A native Product Job is not a tool locality.** A render, capture or export started by the user is owned and recovered by its product ([CM-04](#rule-cm-04)); the Harness may *observe* one through a status tool, never adopt it as a Step. |

---

<a id="10-child-tasks-and-long-running-capabilities"></a>

## 10. Product jobs and long-running capabilities

```
Parent Step invokes a long-running capability
  → the owner returns a ProductJobRef
  → the parent step enters Waiting(ProductJob)
  → the Run observes the product job by snapshot and events
  → completion: the parent receives result, ResourceRef, ArtifactRef, outcome
```

| # | Rule |
|---|---|
| <a id="rule-ct-01"></a>CT-01 | Long operations use ProductJob references; internal agent Steps remain inside one Run ([CT-03](../requirements/05-ai-and-agent-execution.md#rule-ct-03) of the AI requirements). |
| <a id="rule-ct-02"></a>CT-02 | Cancellation requests propagate only to jobs initiated by this Run and authorised for its control; shared/pre-existing jobs continue ([CT-04](../requirements/05-ai-and-agent-execution.md#rule-ct-04) of the AI requirements). |
| <a id="rule-ct-03"></a>CT-03 | The Run observes job references, status and output references; it never imports a product state store ([CT-05](../requirements/05-ai-and-agent-execution.md#rule-ct-05) of the AI requirements). |
| <a id="rule-ct-04"></a>CT-04 | Bounded independent tool calls are allowed; sub-agents, agent teams, handoff and external-agent delegation are excluded ([CT-06](../requirements/05-ai-and-agent-execution.md#rule-ct-06) of the AI requirements). |

---

## 11. Compensation and checkpoints

| # | Rule |
|---|---|
| <a id="rule-cc-01"></a>CC-01 | **Two checkpoint kinds**: an execution checkpoint owned by the runtime, and a domain checkpoint owned by the product (`§5.1` there). |
| <a id="rule-cc-02"></a>CC-02 | **ArcChat never creates a system-wide snapshot** ([CK-01](../requirements/05-ai-and-agent-execution.md#rule-ck-01) there). It requests a checkpoint and receives a reference. |
| <a id="rule-cc-03"></a>CC-03 | **A domain checkpoint precedes any high-risk batch modification** ([CK-02](../requirements/05-ai-and-agent-execution.md#rule-ck-02) there). |
| <a id="rule-cc-04"></a>CC-04 | **Compensation between Cloud and the targeted application is a saga executed in reverse through each owner** ([CP-02](../requirements/05-ai-and-agent-execution.md#rule-cp-02) there), never a simulated distributed transaction. |
| <a id="rule-cc-05"></a>CC-05 | **Compensation is traced and can fail** ([CP-03](../requirements/05-ai-and-agent-execution.md#rule-cp-03), [CP-04](../requirements/05-ai-and-agent-execution.md#rule-cp-04) there). |
| <a id="rule-cc-06"></a>CC-06 | **Failure does not automatically trigger compensation** ([CP-05](../requirements/05-ai-and-agent-execution.md#rule-cp-05) there). |

---

## 12. Trace and explainability

```
Operational Trace          product-level, user-visible: plans, actions, capability input
                           summaries, outputs, approvals, results, costs
Retrieval Trace            what was searched, in what scope, what was admitted or excluded and why
Audit                      security decisions and high-value effects
Diagnostic Log             operations only
```

| # | Rule |
|---|---|
| <a id="rule-tr-01"></a>TR-01 | **All four are separate systems** ([I-107](../requirements/01-normative-glossary-and-invariants.md#rule-i-107), [I-167](../requirements/01-normative-glossary-and-invariants.md#rule-i-167), [I-272](../requirements/01-normative-glossary-and-invariants.md#rule-i-272)–[I-276](../requirements/01-normative-glossary-and-invariants.md#rule-i-276)). |
| <a id="rule-tr-02"></a>TR-02 | **Chain-of-thought never enters any of them** ([PR-10](../requirements/05-ai-and-agent-execution.md#rule-pr-10) in the AI requirements). |
| <a id="rule-tr-03"></a>TR-03 | **An external agent's internal reasoning never enters the ArcChat model** ([EA-07](../requirements/08-extensions-and-developer-platform.md#rule-ea-07) in the extension requirements). |
| <a id="rule-tr-04"></a>TR-04 | **An AI context inspector renders what the model was actually given** ([RT-03](../requirements/06-knowledge-search-and-retrieval.md#rule-rt-03) in the knowledge requirements). |

---

## 13. Automation engine

```
Automation Definition (versioned)
  → Scheduler (time zone + DST policy) or Event Subscriber (durable events only)
      → Trigger Occurrence (stable identity; deduplicated)
          → Task (created from the Task Template, with the version bound)
              → Run
```

| # | Rule |
|---|---|
| <a id="rule-au-01"></a>AU-01 | **An automation is a rule that creates tasks; it never executes work itself** (`§10` of the AI requirements). |
| <a id="rule-au-02"></a>AU-02 | **A trigger occurrence has stable identity**, so a scheduler restart does not double-fire ([TG-03](../requirements/05-ai-and-agent-execution.md#rule-tg-03) there). |
| <a id="rule-au-03"></a>AU-03 | **Event triggers deduplicate by event id** ([TG-04](../requirements/05-ai-and-agent-execution.md#rule-tg-04) there) and subscribe only to durable events ([EV-07](02-contracts-and-protocols.md#rule-ev-07) in the contracts architecture). |
| <a id="rule-au-04"></a>AU-04 | **Loop protection is structural**: causation chains, causation depth limits, self-recursion suppression, cross-automation cycle detection where feasible ([LP-01](../requirements/05-ai-and-agent-execution.md#rule-lp-01)–[LP-03](../requirements/05-ai-and-agent-execution.md#rule-lp-03) there). |
| <a id="rule-au-05"></a>AU-05 | **Storm caps are enforced**: per-automation rate limit, per-workspace concurrency, global agent concurrency, AI budget cap ([LP-04](../requirements/05-ai-and-agent-execution.md#rule-lp-04) there). |
| <a id="rule-au-06"></a>AU-06 | **Catch-up is bounded** ([MR-02](../requirements/05-ai-and-agent-execution.md#rule-mr-02) there). |
| <a id="rule-au-07"></a>AU-07 | **Every triggered task re-authorises** ([AP-10](../requirements/05-ai-and-agent-execution.md#rule-ap-10) there). |
| <a id="rule-au-08"></a>AU-08 | AI automation scheduling exists only in Cloud. Ordinary native Product Jobs can run without Cloud or AI and do not create a desktop agent scheduler ([LA-01](../requirements/05-ai-and-agent-execution.md#rule-la-01) of the AI requirements). |

---

## 14. MCP integration

| # | Rule |
|---|---|
| <a id="rule-mc-01"></a>MC-01 | **MCP is an edge adapter behind the capability registry** ([`MC-01`](../requirements/08-extensions-and-developer-platform.md#rule-mc-01) in the extension requirements), never the internal protocol. |
| <a id="rule-mc-02"></a>MC-02 | **The protocol core is stateless** (**[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**): no initialize exchange, no session header, per-request capability negotiation. **ArcForges must not build session identity on MCP transport state.** |
| <a id="rule-mc-03"></a>MC-03 | **Server-to-client requests use the protocol's multi-round-trip mechanism**, which is transport, not an ArcForges execution concept. |
| <a id="rule-mc-04"></a>MC-04 | **MCP's own task and skill vocabulary never conflates with ArcForges'** (glossary §9). |
| <a id="rule-mc-05"></a>MC-05 | **The exact SDK version is pinned at first consumption, and the vocabulary mapping is recorded.** *Owner: Architecture Owner. Trigger: start of the MCP/extension work package.* |
| <a id="rule-mc-06"></a>MC-06 | **MCP content is untrusted data** (`§8` of the security architecture). |
| <a id="rule-mc-07"></a>MC-07 | **A down MCP server degrades that integration only** ([IN-05](../requirements/products/arcchat.md#rule-in-05) in the ArcChat requirements). |

---

## 15. Failure handling

| Failure class | Runtime behaviour |
|---|---|
| `Transient` | Bounded automatic retry with backoff |
| `Conflict` | Refresh, rebase, regenerate the action, re-approve if the approval was revision-bound |
| `PermissionDenied` / `ApprovalDenied` | Stop or ask; never retry to probe |
| `BudgetExceeded` | Pause and request an extension |
| `EntitlementBlocked` | Report the entitlement reason, distinct from a policy or security reason |
| `CapabilityUnsupported` | Explain the unavailable own-application capability; wait for its explicitly selected target or propose an authorized alternative. Never launch or discover another product. |
| `VersionIncompatible` | Wait or need attention, naming the required version |
| `ExternalEffectUnknown` | **Reconcile before any retry**; unresolved → Needs Attention |
| `Timeout` | Attempt failure handled by the retry policy |
| `PermanentDomainFailure` | Fail the step; the task policy decides keep / compensate / ask |

**Retry safety is declared by the capability owner, never guessed** ([FL-08](../requirements/05-ai-and-agent-execution.md#rule-fl-08) in the AI requirements).

---

## 16. Traceability

| Current document | Relationship |
|---|---|
| [AI, Agent Execution, Tasks and Automation Requirements](../requirements/05-ai-and-agent-execution.md) | Owns execution states, placement, approvals, automation and recovery |
| [Commerce, Entitlement and AI Credits Requirements](../requirements/04-commerce-entitlement-and-credits.md) | Owns admission, metering, tariffs and reconciliation |
| [Agent Harness](17-agent-harness.md) | Defines the concrete Cloud turn loop and tool dispatch |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Agent framework enabled only on AOT-validated surfaces; desktop stays a Native AOT deliverable |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Durable `ToolRequest` / `ToolResult` remote execution |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Reserve-then-settle, fixed precision, per-run tariff snapshot, hard stop, three ledgers |
| **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** | MCP stability, statelessness and vocabulary disambiguation |

## [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) execution placement and supplier binding

Selected Workers AI routes: @cf/openai/gpt-oss-120b for default text/tool work; @cf/openai/gpt-oss-20b as explicit lower-latency text profile; @cf/google/gemma-4-26b-a4b-it only for accepted authorized image-context understanding; @cf/baai/bge-m3 for multilingual 1024-dimensional embeddings; @cf/baai/bge-reranker-base for bounded reranking. No text-to-image/voice product feature added. Direct bindings, no mandatory AI Gateway/Agents SDK/Vercel SDK/external provider. Text input cap 24,000 tokens, output 4096, tools 32, total context<=256 KiB default; vision max 4 approved images <=1024px longest side/1 MiB each, no raw media/capture egress. Embedding chunk512tokens/overlap 64, batch 16,1024 finite float components; query/doc use same version, max 200rerank candidates. Model max limits may be higher; product limits stay these bounded values.

Model route/config pins exact CF model ID and adapter profile v1. CF does not promise immutable weights behind an ID: a supplier change triggers eval/versioned embedding rebuild. No silent fallback across modality/tool capabilities. Operator can activate another supported selected model only through versioned config/canary; unavailable route returns named availability reason, no external-provider reroute. Model output classification stays Harness§3; tools decoded/validated through generated capability schema before proposing approval. No embedded function executor can bypass C# authorization. Rerank/scientific measurement remains advisory versus deterministic scalar/unit meanings.

Supplier request ID is nullable until CF returns one; ArcForges attempt identity exists first. Usage counts come from per-call response if supplied; missing/partial measurements stay unknown. Normalize input/output/cached counts and exact decimal supplier price version; existing customer tariff, admission/hold/settlement/refund examples unchanged. No promise that CF aggregate billing can resolve one missing call; late supplier totals reconcile operator liability separately, never debit a customer after its existing terminal hold deadline. Production prices are operator input snapshots of published CF rates, synthetic testprices explicitly labeled.

Search keeps D1 FTS5 and Vectorize projections and query-time authorization; D1 FTS5 and Vectorize projections under the current D1 profile. Projection key(sourceId,sourceRev,embeddingModelId,embeddingProfileVersion,chunkHash), tombstone/source-denial before counts/citations. Model dimension/profile change builds separate index from authorized acknowledged sources, catches up journal, switches reader atomically and retains rollback window; no mixing vectors or changing canonical Notes scalar order. C# config activation creates immutable snapshot, Worker acknowledges supported schema/model/limits and version hash, then C# atomically moves active head; stale Worker cannot admit a new call. Emergency denial applies immediately even to a frozen Run; existing tariff snapshot remains for already admitted work.

The [sole Workflow and transactional ports](contracts/05-cloudflare-integration.md) supply the concrete placement, transitions, retry/approval/cancellation and restore rules. C# schedules deterministic occurrences and owns their Task record; CF advances the model/tool loop. ProductJob remains product-owned.

## Slate transcription within the sole Harness

The accepted [slate.transcribe.v1 profile](23-simulator-and-interchange.md#5-slate-metadata-render-and-subtitle-profiles) adds Workers AI whisper-large-v3-turbo to the selected catalogue for audio transcription only. Task.startTranscription creates a normal Cloud Task with immutable uploaded-audio input pins, explicit paid budget and a fixed chunk-processing plan. RunWorkflow executes it using existing claim/model-intent/model-outcome/settle/finalize ports and unknown-effect rules. It does not invoke Search InferenceWorkflow, create another agent loop or execute render code in CF. Final Task output is a TranscriptRecord artifact or explicit partial/no-result outcome; adopting subtitles remains a separately approved local NativeContentRev edit.

## Ordinary and temporary execution authority

The Task engine sections govern AgentTask. Ordinary ChatTurn uses the same sole CF Harness and owner-discriminated C# ports, with pure-read capabilities only and explicit promotion before any effectful tool. [Harness owner/context lifecycle](17-agent-harness.md#execution-owners-protected-context-and-temporary-cleanup) and [client journeys](contracts/07-client-journeys-and-ports.md) fix persistent/temporary storage, mode transitions, platform-funded compaction, transient consent and Brave search. Every financial attempt references its actual execution owner. Temporary mode does not imply an on-device model, zero cost or provider non-processing.
