<a id="rule-wp-43"></a>

# WP-43 — Cloud AI Routing, Metering and Settlement

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `25`, `42`, `44` · Downstream: `40`, `50`, `52`

> **Goal.** Replace the stubbed provider path with the real one: provider routing under **operator-funded credentials**, dispatch-time supplier prices and Run-pinned customer tariffs, real usage normalisation, metering that reserves before and settles after, transparency obligations, and honest failure when a provider is unavailable.

---

## 1. Scope and purpose

**In scope.** Cloud provider adapters and routing under operator-funded credentials; model and provider availability as policy; supplier price versions and Run-pinned customer tariffs; real usage normalisation into non-overlapping categories; settlement and the three ledgers; the provider interaction record; metering integrated with credits; **operator-funded provider credential custody and the structural absence of any end-user key path** ([WP-43.03](#rule-wp-43.03); [AI-02](../../requirements/products/arcchat.md#rule-ai-02) of the AI requirements; [ON-03](../../requirements/products/arcchat.md#rule-on-03) of the ArcChat requirements); AI transparency obligations; and failure handling when providers degrade.

**Out of scope.** The execution engine itself (`16`). Retrieval (`40`). Commercial policy authoring (`42`).

**Why this package exists.** [WP-17.05](17-arcchat-independent-core.md#rule-wp-17.05) deliberately stubbed the managed path and [WP-16](16-unified-execution-engine.md#rule-wp-16) built the budget interface without economics. This package closes both, and it is also where **[V-01](../../assurance/phase-1-official-verification.md#rule-v-01)**'s transparency gate attaches.

---

## 2. Required inputs and dependencies

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
| BR-04 | **Provider credentials exist only as Cloud deployment secrets** ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)), injected by secret manager or Docker secret with least privilege. They never appear in the policy file, the image, the logs, the public sample or any client projection ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)). |
| <a id="rule-br-05"></a>BR-05 | **There is no end-user BYOK** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired). Provider credentials are deployment secrets ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)); a self-host operator provisioning server credentials is infrastructure provisioning, not customer BYOK ([I-495](../../requirements/01-normative-glossary-and-invariants.md#rule-i-495)). |
| BR-06 | **Provider and model availability is policy**, not a compiled list, and a withdrawn model degrades explicitly. |
| BR-07 | **Provider interaction records are a separate trace system** from execution, capability and audit traces. |
| BR-08 | **Hidden model reasoning never enters the product model.** |
| BR-09 | **Cost transparency is a product obligation**: a user can see what a run cost and why. |
| BR-10 | **A provider outage degrades AI capability with a reason and releases reservations**; it never silently consumes credit. |
| BR-11 | **AI-generated content carries the transparency marking the applicable regime requires** (**[V-01](../../assurance/phase-1-official-verification.md#rule-v-01)**). |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.AI/` | Provider adapters, routing, tariffs, metering, interaction records |
| `src/Cloud/ArcForges.Cloud.Modules.Entitlement/` | Credit settlement integration |
| `src/Cloud/ArcForges.Cloud.Modules.AI/` | Provider adapters, routing, normalisation, settlement. **No desktop project participates** |
| `src/BuildingBlocks/ArcForges.Execution.Budget/` | Real reserve, settle and release against credits |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.AI/` | AI request, response and metering DTOs |
| `tests/CloudIntegrationTests/AI/` | Routing, supplier price, customer tariff, normalisation, settlement, uncertain-usage, outage and transparency suites |

**Major types introduced.** `AiProviderAdapter`, `ProviderCapabilityDescriptor`, `ModelDescriptor`, `RoutingPolicy`, `RoutingDecision`, `TariffVersion`, `TariffSnapshot`, `CostDimension`, `ProviderInteractionRecord`, `MeteringResult`, `SupplierPriceVersion`, `AttemptUsage`, `CustomerSettlement`, `TransparencyMarking`. **`ByokBinding` is retired** — no customer credential type exists ([BR-05](#rule-br-05)).

---

## 5. Required implementation work

<a id="rule-wp-43.00"></a>

### WP-43.00 — Provider adapters and routing

**What must be fully done.** Adapters per provider with typed capability descriptors. Routing selects a provider and model from policy, considering availability, capability fit, entitlement and cost. The decision is recorded and explainable. Streaming is supported where the provider offers it, with interruption handled explicitly.

**Testing requirements.** Routing decision tests across policy configurations; an explainability assertion; streaming interruption tests; an adapter-substitution test.

**Completion gate.** Routing is policy-driven, explainable and recorded, and streaming interruption never stores a partial response as complete.

<a id="rule-wp-43.01"></a>

### WP-43.01 — Tariffs and cost dimensions

**What must be fully done.** Versioned tariffs with effective dates and the full cost-dimension set. Each run locks a tariff snapshot at start. A historical charge is explainable against the rates in force at the time. Media units are metered separately from text units.

**Testing requirements.** A rate-change test asserting settled charges are unaffected; an explainability test reconstructing a historical charge; per-dimension metering tests.

**Completion gate.** A rate change never alters a settled charge, and every historical charge is explainable from its locked snapshot.

<a id="rule-wp-43.02"></a>

### WP-43.02 — Metering and settlement

**What must be fully done.** Persist provider intent with nullable provider reference/outcome before network I/O; reserve supplier exposure per attempt and Run customer total atomically. Platform jobs use operator authority without a customer term/hold. Settle one durable invocation, not an unfinished whole Turn.  Estimate, reserve, execute, settle actual, release unused — atomic against the credit lots. Settlement is idempotent per attempt. A crashed run's reservation is swept. Exhaustion is a hard stop with a clear remediation prompt.

**Testing requirements.** Crash before provider response ID, then reconcile; race workspaces and platform retries at a supplier cap; release a customer hold while preserving unknown supplier/Run exposure; settle tool-only output before the next call.  Reserve-settle-release accounting; idempotent settlement under retry; sweep after a crashed run; a hard-stop test; a concurrency test asserting no overdraft.

**Completion gate.** Every dispatch has committed bounded exposure and every customer debit has durable delivered evidence; unknown liability survives deadline/restart/rollover.  Metering never double-charges, never leaks a reservation, and never permits an overdraft.

<a id="rule-wp-43.03"></a>

### WP-43.03 — Operator provider credentials and the absence of BYOK

**What must be fully done.** **End-user BYOK is excluded in every form** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired). Provider credentials belong to the deployment operator and are injected by secret manager or Docker secret with least privilege ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)); they never appear in the policy file, the image, the logs, the public sample or any client projection ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)). Self-host operators provision their own server credentials the same way — that is infrastructure provisioning, not customer BYOK ([I-495](../../requirements/01-normative-glossary-and-invariants.md#rule-i-495)).

**Testing requirements.** A contract policy test asserting **no operation, schema field, setting or UI accepts a customer provider key, model endpoint or credential**; a structural test asserting no desktop, mobile or browser assembly references a provider adapter; a projection test asserting no supplier rate, route weight or credential reaches a client ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)); a secret-handling test asserting credentials are absent from the image, the sample configuration and the logs.

**Completion gate.** **No end-user BYOK path exists anywhere in the product**, and provider credentials are present only in the Cloud host's injected secrets.

<a id="rule-wp-43.04"></a>

### WP-43.04 — Provider interaction records and transparency

**Required design implementation and verification.** Implement the already frozen content-origin profile at the provider generation boundary. Test real provider text through durable output and downstream carrier fixtures, deterministic/non-AI and legacy controls, malformed/hash-mismatched mark and marking retry. Supplier usage remains recorded; platform non-delivery releases/compensates customer funding under existing metering rules. Record the separate [VG-01](../../assurance/open-gates-register.md#rule-vg-01) regime/adequacy approval before its market trigger.

**What must be fully done.** A provider interaction record per call, separate from the execution, capability and audit traces, carrying no content beyond what policy permits. Cost transparency surfaces show what a run cost and why. AI-generated content carries the required transparency marking per artifact type.

**Testing requirements.** Trace-separation test; a content-redaction test on interaction records; a cost-explainability test; a marking-coverage test per artifact type.

**Completion gate.** Interaction records are separate and redacted, run cost is explainable to the user, and every artifact type has a defined marking. **This satisfies [VG-01](../../assurance/open-gates-register.md#rule-vg-01) once the regime determination is recorded.**

<a id="rule-wp-43.05"></a>

### WP-43.05 — Availability and failure

**What must be fully done.** Provider and model availability driven by policy, with a withdrawn model degrading explicitly rather than disappearing. A provider outage fails runs with a typed reason, releases reservations, and offers a fallback where policy permits. All-routes-unavailable is a page-worthy condition.

**Testing requirements.** Model-withdrawal degradation; provider-outage reservation release; fallback routing; an alert assertion for all-routes-unavailable.

**Completion gate.** A provider outage never silently consumes credit, and a withdrawn model degrades with a stated reason.

<a id="rule-wp-43.07"></a>

### WP-43.07 — Real-provider metering evidence

**What must be fully done.** The complete path exercised against a **real provider**, not a fixture: normalisation of that provider's actual usage report into non-overlapping categories with its declared inclusion relationships; cumulative stream snapshots replacing rather than summing; supplier cost at the dispatch-time price version; customer cost at the Run's pinned tariff snapshot; idempotent settlement keyed on `(provider_attempt_id, usage_revision, category)`; and the `§8.6` worked fixture asserted exactly — USD 0.00244 supplier cost, 4,880,000 micro-credits customer cost, 1.12 credits released to the original funding sources.

**Testing requirements.** Two providers whose cache and reasoning fields overlap differently, both settling correctly; a duplicate usage event proving no double debit; an undeclared usage field entering reconciliation rather than a debit; a cancellation settling verified consumption and releasing the remainder; a lost final usage producing `UsagePending` and, at the deadline, releasing the customer hold while **retaining the supplier liability**; a platform-caused retry charged once to the customer and fully visible in supplier cost; a token-category and tier price change applying to future dispatch only; historical replay after replacing every current rate, reproducing the original charge exactly.

**Completion gate.** **One real provider usage response and one real payment-provider event are reconciled through the same code as the fixtures** ([MT-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-01), `§10.6` of the configuration requirements). Deterministic fixtures supplement this evidence; they do not replace it.

<a id="rule-wp-43.06"></a>

### WP-43.06 — Provider test-environment coverage

**What must be fully done.** Every provider integration exercised against the provider's test environment, with its contract shape frozen as recorded fixtures so CI does not depend on provider availability.

**Testing requirements.** A per-provider test-environment run; a fixture-driven CI run with the provider unreachable.

**Completion gate.** Every provider is exercised against its test environment and has recorded fixtures — **satisfying [PG-10](../../assurance/open-gates-register.md#rule-pg-10) for AI providers**.

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

- [25 — Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md)
- [42 — Commerce, Entitlement and Credits](42-commerce-entitlement-and-credits.md)
- [44 — Dynamic Policy and Configuration Control Plane](44-dynamic-policy-and-configuration.md)

**Downstream — these consume this package’s completed output.**

- [40 — Knowledge, Search and Retrieval](40-knowledge-search-and-retrieval.md)
- [50 — Full-Platform Production Release](50-full-platform-production-release.md)
- [52 — The Cloud Harness](52-cloud-harness.md)
