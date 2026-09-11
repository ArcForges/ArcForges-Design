<a id="rule-wp-43"></a>

# WP-43 — Workers AI Routing and Metering

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `25`, `42`, `44` · Downstream: `40`, `50`, `52`

> **Goal.** Replace the stubbed provider path with the real one: provider routing under **operator-funded credentials**, dispatch-time supplier prices and Run-pinned customer tariffs, real usage normalisation, metering that reserves before and settles after, transparency obligations, and honest failure when a provider is unavailable.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: AI Workers AI adapter + Cloud metering. Inputs: the assigned exact Contracts packages/descriptors and actual provider artifacts; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Cloud provider adapters and routing under operator-funded credentials; model and provider availability as policy; supplier price versions and Run-pinned customer tariffs; real usage normalisation into non-overlapping categories; settlement and the three ledgers; the provider interaction record; metering integrated with credits; **operator-funded provider credential custody and the structural absence of any end-user key path** ([WP-43.03](#rule-wp-43.03); [AI-02](../../requirements/products/arcchat.md#rule-ai-02) of the AI requirements; [ON-03](../../requirements/products/arcchat.md#rule-on-03) of the ArcChat requirements); AI transparency obligations; and failure handling when providers degrade.

**Out of scope.** The execution engine itself (`16`). Retrieval (`40`). Commercial policy authoring (`42`).

**Why this package exists.** [WP-17.05](17-arcchat-independent-core.md#rule-wp-17.05) deliberately stubbed the managed path and [WP-16](16-unified-execution-engine.md#rule-wp-16) built the budget interface without economics. This package closes both, and it is also where **[V-01](../../assurance/phase-1-official-verification.md#rule-v-01)**'s transparency gate attaches.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

[WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25) provides authoritative Chat/Notes stores and durable output/resource commits; [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) provides money/capacity admission; [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) provides active route/policy snapshots. Single-invocation integration is tested here through those real ports without implementing a second Harness; [WP-52](52-cloud-harness.md#rule-wp-52) composes the loop.

| Input | Why it matters |
|---|---|
| [`../../requirements/05-ai-and-agent-execution.md`](../../requirements/05-ai-and-agent-execution.md) `§13` | AI economics: tariff versioning, cost dimensions, routing, three ledgers, transparency |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§6`, `§7` | Provider routing and metering architecture |
| **[V-01](../../assurance/phase-1-official-verification.md#rule-v-01)** | The AI transparency gate and its trigger |
| **[D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Versioned economic policy, immutable history, hard stop at zero |
| [WP-16](16-unified-execution-engine.md#rule-wp-16), [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) output | The budget interface and real credits |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Every run locks a tariff snapshot at start**; a rate change never alters a settled charge (**[D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020)**). |
| BR-02 | **Credits are reserved before execution and settled after**, with a hard stop at zero (**[D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020)**). |
| BR-03 | **The three ledgers stay separate** ([I-011](../../requirements/01-normative-glossary-and-invariants.md#rule-i-011)): provider cost, customer credit, payment and revenue. |
| BR-04 | Workers AI calls use the AI binding in the CF deployment. C#/CF service authentication and other designated provider secrets remain in their owning deployment secret stores; never in images, policy values, public samples or clients. |
| <a id="rule-br-05"></a>BR-05 | **There is no end-user BYOK** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired). Provider credentials are deployment secrets ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)); a self-host operator provisioning server credentials is infrastructure provisioning, not customer BYOK ([I-495](../../requirements/01-normative-glossary-and-invariants.md#rule-i-495)). |
| BR-06 | Policy may activate only models/capabilities in the selected Workers AI catalogue/profile. Withdrawal produces an explicit unavailable state; an unvalidated model is not admitted by changing a string. |
| BR-07 | **Provider interaction records are a separate trace system** from execution, capability and audit traces. |
| BR-08 | **Hidden model reasoning never enters the product model.** |
| BR-09 | **Cost transparency is a product obligation**: a user can see what a run cost and why. |
| BR-10 | Provider failure before dispatch releases unused reservations; possible dispatch/outcome loss retains the existing unknown-usage hold/reconciliation deadline. No outage is silently treated as free, charged twice or safely replayable. |
| BR-11 | **AI-generated content carries the transparency marking the applicable regime requires** (**[V-01](../../assurance/phase-1-official-verification.md#rule-v-01)**). |

---

## 4. Projects, directories, files and major types affected

| Owner / location | Deliverable |
|---|---|
| AI: src/providers/workers-ai/, src/inference/ | Selected Workers AI catalogue adapter, model/text/embedding/rerank request/response normalization and service ports |
| Cloud: src/Cloud/ArcForges.Cloud.Modules.Agent/ | Catalogue/policy validation, routing decision, intent/outcome/usage/supplier records |
| Cloud: Modules.Task, Modules.Commerce, Modules.Entitlement | Their owned run, tariff, reservation, credit/settlement and audit transaction participants |
| Contracts: public Agent/usage and internal AI HTTP profiles | Generated types and independent fixtures from the fixed registry |
| Cloud/AI integration tests | Real provider capability, usage, unknown outcome, tariff, funding and recovery evidence |

The provider implementation is confined to ArcForges-AI; C# owns canonical commerce/authority and typed integration ports. No desktop/mobile model SDK or second loop is introduced.

---

## 5. Required implementation work

<a id="rule-wp-43.00"></a>

### WP-43.00 — Provider adapters and routing


**What must be fully done.** Implement only the selected Workers AI catalogue/capability profiles using env.AI.run: default/fast text, accepted image context, bge-m3 embedding and reranker. Validate model availability and frozen config, canonical request limits and supported tool/stream shapes before dispatch. C# records admission/routing and supplier version; CF executes the already admitted intent.

**Testing requirements.** Actual selected models/capability shapes, withdrawn/unknown/unsupported requests, request-size/output bounds and version mismatch.

**Completion gate.** The validated CF catalogue supplies every accepted AI call kind; no external provider, BYOK, Gateway or Node sidecar is required.

<a id="rule-wp-43.01"></a>

### WP-43.01 — Tariffs and cost dimensions

**What must be fully done.** Versioned tariffs with effective dates and the full cost-dimension set. Each run locks a tariff snapshot at start. A historical charge is explainable against the rates in force at the time. Media units are metered separately from text units.

**Testing requirements.** A rate-change test asserting settled charges are unaffected; an explainability test reconstructing a historical charge; per-dimension metering tests.

**Completion gate.** A rate change never alters a settled charge, and every historical charge is explainable from its locked snapshot.

<a id="rule-wp-43.02"></a>

### WP-43.02 — Metering and settlement


**What must be fully done.** Implement C# reservation/intent before CF I/O, outcome receipt before settlement and immutable attempt usage revisions under the existing transaction families. Cover interactive runs and bounded inference jobs; operator maintenance remains separately funded. Use stable attempt identity, supplier exposure, Run customer total and exact credit lots. Unknown usage follows its existing deadline/liability ladder, never an automatic model resend.

**Testing requirements.** Actual CF normal/interrupted/lost outcome with concurrent duplicates and replayed receipts; cancelled/unknown hold sweep, tariff change and operator-job isolation.

**Completion gate.** Each possible invocation is accounted once; holds and unknown liability reconcile without duplicate effect or unapproved spend.

<a id="rule-wp-43.03"></a>

### WP-43.03 — Operator provider credentials and the absence of BYOK


**What must be fully done.** Provision the Workers AI binding and restricted service credentials as deployment inputs, with dual-key HMAC rotation/clock/nonces from the CF contract. C# does not receive an end-user provider key. Self-host installation provisions its own CF resources and same typed integration/config contract.

**Testing requirements.** Deployment secret/source/log/client projection checks and key-rotation/replay/forged callback tests.

**Completion gate.** Only authorized service deployments can invoke admitted jobs or acknowledge outcomes; customer BYOK remains structurally absent.

<a id="rule-wp-43.04"></a>

### WP-43.04 — Provider interaction records and transparency

**Required design implementation and verification.** Implement the already frozen content-origin profile at the provider generation boundary. Test real provider text through durable output and downstream carrier fixtures, deterministic/non-AI and legacy controls, malformed/hash-mismatched mark and marking retry. Supplier usage remains recorded; platform non-delivery releases/compensates customer funding under existing metering rules. Record the separate [VG-01](../../assurance/open-gates-register.md#rule-vg-01) regime/adequacy approval before its market trigger.

**What must be fully done.** A provider interaction record per call, separate from the execution, capability and audit traces, carrying no content beyond what policy permits. Cost transparency surfaces show what a run cost and why. AI-generated content carries the required transparency marking per artifact type.

**Testing requirements.** Trace-separation test; a content-redaction test on interaction records; a cost-explainability test; a marking-coverage test per artifact type.

**Completion gate.** Interaction records are separate and redacted, run cost is explainable to the user, and every artifact type has a defined marking. **This satisfies [VG-01](../../assurance/open-gates-register.md#rule-vg-01) once the regime determination is recorded.**

<a id="rule-wp-43.05"></a>

### WP-43.05 — Availability and failure


**What must be fully done.** Implement catalogue health, explicit model withdrawal, pre-dispatch failure and possible-dispatch unknown classification. Use only the selected fallback policy within the catalogue and a new authorized intent when permitted; never retry an uncertain model effect automatically. Keep keyword/local work available when all AI routes fail.

**Testing requirements.** Rate limit, timeout before/after effect, partial usage, unavailable catalogue and all-models-unavailable alert/recovery.

**Completion gate.** Visible AI degradation retains correct reservation and effect certainty without affecting unrelated product capabilities.

<a id="rule-wp-43.07"></a>

### WP-43.07 — Real-provider metering evidence


**What must be fully done.** Record actual Workers AI responses for each selected capability and normalize them into independent sanitized fixtures. Run deterministic fixtures on ordinary CI and the credentialed real-CF candidate gate with exact Worker/model/config identities; fixtures never replace supplier/usage proof.

**Testing requirements.** Model response drift, missing category, cumulative stream and embedding/rerank result validation, plus controlled real-provider run.

**Completion gate.** The selected provider closure has both repeatable protocol tests and actual integration evidence.

<a id="rule-wp-43.06"></a>

### WP-43.06 — Provider test-environment coverage

**What must be fully done.** Every provider integration exercised against the provider's test environment, with its contract shape frozen as recorded fixtures so CI does not depend on provider availability.

**Testing requirements.** A per-provider test-environment run; a fixture-driven CI run with the provider unreachable.

**Completion gate.** Every provider is exercised against its test environment and has recorded fixtures — **satisfying [PG-10](../../assurance/open-gates-register.md#rule-pg-10) for AI providers**.

---

<a id="rule-wp-43.90"></a>
### WP-43.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement the frozen Workers AI model subset/direct binding, capability matrix, normalization, limits and known/unknown usage contract. Gateway is not a required dependency.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Real selected model/tool/embedding cases and provider refusal/lost-result/usage reconciliation, tied to C# admitted call and config identity. No general external-provider integration implied.

**Completion gate.** Real selected model/tool/embedding cases and provider refusal/lost-result/usage reconciliation, tied to C# admitted call and config identity. No general external-provider integration implied. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Tariffs, interaction records and metering results |
| Protocol | AI request, response and metering contracts |
| UI | Model selection, cost transparency and availability surfaces |
| Security | Operator credential custody by secret injection ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)); egress control on model interaction; instruction provenance on model output |
| Platform | **No local model support** ([C-02](../../requirements/00-product-scope-and-portfolio.md#rule-c-02)). Provider availability and route health are surfaced honestly |
| Migration | Tariff and interaction record schema versioning |
| Compatibility | AI contracts enter the supported window |

---

## 7. Tests and verification evidence

**Required evidence addition.** [WP-43.04](#rule-wp-43.04) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Routing decision, explainability and streaming results | [WP-43.00](#rule-wp-43.00) |
| Rate-change immutability and historical explainability results | [WP-43.01](#rule-wp-43.01) |
| Metering accounting, idempotency, sweep and overdraft results | [WP-43.02](#rule-wp-43.02) |
| No-BYOK structural assertions and credential-custody results | [WP-43.03](#rule-wp-43.03) |
| Real-provider normalisation, settlement and worked-fixture results | [WP-43.07](#rule-wp-43.07) |
| Trace separation, redaction, cost explainability and marking coverage | [WP-43.04](#rule-wp-43.04) |
| Degradation, reservation release and alert results | [WP-43.05](#rule-wp-43.05) |
| Per-provider test-environment runs and fixture-driven CI results | [WP-43.06](#rule-wp-43.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-43.90](#rule-wp-43.90) and all inherited domain-specific gates must pass on the same candidate closure. Real selected model/tool/embedding cases and provider refusal/lost-result/usage reconciliation, tied to C# admitted call and config identity. No general external-provider integration implied.

**[PG-13](../../assurance/open-gates-register.md#rule-pg-13) evidence:** [WP-43.07](#rule-wp-43.07) — Real provider usage and exact synthetic supplier/customer settlement fixture through production code; combine with payment/term evidence from package 42. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Routing is policy-driven, explainable and recorded; streaming interruption never stores a partial response as complete.
2. A rate change never alters a settled charge; every historical charge is explainable from its locked tariff snapshot.
3. Metering never double-charges, never leaks a reservation, and never permits an overdraft under concurrency.
4. **No end-user BYOK path exists anywhere in the product** — no operation, schema field, setting or UI accepts a customer provider key — and provider credentials are present only in the Cloud host's injected secrets.
5. Provider interaction records are a separate, redacted trace system; run cost is explainable to the user; every artifact type has a defined transparency marking — satisfying [VG-01](../../assurance/open-gates-register.md#rule-vg-01) once the regime determination is recorded.
6. A provider outage never silently consumes credit; a withdrawn model degrades with a stated reason; all-routes-unavailable alerts.
7. Every provider is exercised against its test environment with recorded fixtures — satisfying [PG-10](../../assurance/open-gates-register.md#rule-pg-10) for AI providers.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [25 sync engine and blob lifecycle](25-sync-engine-and-blob-lifecycle.md#rule-wp-25)
- [42 commerce entitlement and credits](42-commerce-entitlement-and-credits.md#rule-wp-42)
- [44 dynamic policy and configuration](44-dynamic-policy-and-configuration.md#rule-wp-44)

**Downstream — consumers of these released outputs.**

- [40 knowledge search and retrieval](40-knowledge-search-and-retrieval.md#rule-wp-40)
- [50 full platform production release](50-full-platform-production-release.md#rule-wp-50)
- [52 cloud harness](52-cloud-harness.md#rule-wp-52)

---


### Inference-job implementation binding

In the existing adapter/admission substeps, implement AI src/workflows/InferenceWorkflow.ts and src/inference/ for fixed-stage embedding/rerank jobs, and Cloud Search/Commerce typed ports for the [canonical job and receipt record](../../architecture/data-model/01-cloud-data-model.md#search-inference-job-execution-record). Add its binding to the same Worker artifact. Apply the exact inference-job/lease/input/outcome/state HTTP schemas, conditional60-second lease renewed20 seconds,120-second job deadline, deterministic Workflow ID, zero model-step retries and observed deployment-version gate. This is an additional bounded job handler inside the same deployment, with no agent planning/tool loop.

Prove duplicate start, lost receipt, stale fence/generation, active-term expiry, source revocation, complete output with unconfirmed supplier cost, and partial/unknown output. The existing Commerce platformJob chain records supplier exposure once; assert zero customer reservation, customer settlement and credit debit for every embedding/rerank scenario. WP40 consumes these real adapters/receipts before testing index readiness/fallback; WP52 remains the first full model/tool Harness.
