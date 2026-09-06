# WP-43 — Managed AI, BYOK, Routing and Metering

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `16`, `42` · Downstream: `50`

> **Goal.** Replace the stubbed provider path with the real one: provider routing with locked tariffs, BYOK with server-side reference use, metering that reserves before and settles after, transparency obligations, and honest failure when a provider is unavailable.

---

## 1. Scope and purpose

**In scope.** Provider adapters and routing; model and provider availability as policy; tariff versioning and cost dimensions; the provider interaction record; metering integrated with credits; BYOK for cloud and desktop with their different secret paths; AI transparency obligations; and failure handling when providers degrade.

**Out of scope.** The execution engine itself (`16`). Retrieval (`40`). Commercial policy authoring (`42`).

**Why this package exists.** `WP-17.05` deliberately stubbed the managed path and `WP-16` built the budget interface without economics. This package closes both, and it is also where **V-01**'s transparency gate attaches.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/05-ai-and-agent-execution.md`](../../requirements/05-ai-and-agent-execution.md) `§13` | AI economics: tariff versioning, cost dimensions, routing, three ledgers, transparency |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§6`, `§7` | Provider routing and metering architecture |
| **V-01** | The AI transparency gate and its trigger |
| **D-020** | Versioned economic policy, immutable history, hard stop at zero |
| `WP-16`, `WP-42` output | The budget interface and real credits |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Every run locks a tariff snapshot at start**; a rate change never alters a settled charge (**D-020**). |
| BR-02 | **Credits are reserved before execution and settled after**, with a hard stop at zero (**D-020**). |
| BR-03 | **The three ledgers stay separate** (`I-011`): provider cost, customer credit, payment and revenue. |
| BR-04 | **A desktop-local BYOK secret never leaves the device**; a cloud BYOK secret is used server-side by reference and never downloaded. |
| BR-05 | **BYOK changes the economics, not the permission model.** A user with their own key still passes the same security pipeline. |
| BR-06 | **Provider and model availability is policy**, not a compiled list, and a withdrawn model degrades explicitly. |
| BR-07 | **Provider interaction records are a separate trace system** from execution, capability and audit traces. |
| BR-08 | **Hidden model reasoning never enters the product model.** |
| BR-09 | **Cost transparency is a product obligation**: a user can see what a run cost and why. |
| BR-10 | **A provider outage degrades AI capability with a reason and releases reservations**; it never silently consumes credit. |
| BR-11 | **AI-generated content carries the transparency marking the applicable regime requires** (**V-01**). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.AI/` | Provider adapters, routing, tariffs, metering, interaction records |
| `src/Cloud/ArcForges.Cloud.Modules.Entitlement/` | Credit settlement integration |
| `src/ArcChat/ArcChat.Infrastructure/` | Desktop provider adapters and the local BYOK path |
| `src/BuildingBlocks/ArcForges.Execution.Budget/` | Real reserve, settle and release against credits |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.AI/` | AI request, response and metering DTOs |
| `tests/CloudIntegrationTests/AI/` | Routing, tariff, metering, BYOK, outage and transparency suites |

**Major types introduced.** `AiProviderAdapter`, `ProviderCapabilityDescriptor`, `ModelDescriptor`, `RoutingPolicy`, `RoutingDecision`, `TariffVersion`, `TariffSnapshot`, `CostDimension`, `ProviderInteractionRecord`, `MeteringResult`, `ByokBinding`, `TransparencyMarking`.

---

## 5. Required implementation work

### WP-43.00 — Provider adapters and routing

**What must be fully done.** Adapters per provider with typed capability descriptors. Routing selects a provider and model from policy, considering availability, capability fit, entitlement and cost. The decision is recorded and explainable. Streaming is supported where the provider offers it, with interruption handled explicitly.

**Testing requirements.** Routing decision tests across policy configurations; an explainability assertion; streaming interruption tests; an adapter-substitution test.

**Completion gate.** Routing is policy-driven, explainable and recorded, and streaming interruption never stores a partial response as complete.

### WP-43.01 — Tariffs and cost dimensions

**What must be fully done.** Versioned tariffs with effective dates and the full cost-dimension set. Each run locks a tariff snapshot at start. A historical charge is explainable against the rates in force at the time. Media units are metered separately from text units.

**Testing requirements.** A rate-change test asserting settled charges are unaffected; an explainability test reconstructing a historical charge; per-dimension metering tests.

**Completion gate.** A rate change never alters a settled charge, and every historical charge is explainable from its locked snapshot.

### WP-43.02 — Metering and settlement

**What must be fully done.** Estimate, reserve, execute, settle actual, release unused — atomic against the credit lots. Settlement is idempotent per attempt. A crashed run's reservation is swept. Exhaustion is a hard stop with a clear remediation prompt.

**Testing requirements.** Reserve-settle-release accounting; idempotent settlement under retry; sweep after a crashed run; a hard-stop test; a concurrency test asserting no overdraft.

**Completion gate.** Metering never double-charges, never leaks a reservation, and never permits an overdraft.

### WP-43.03 — Operator provider credentials and the absence of BYOK

**What must be fully done.** **End-user BYOK is excluded in every form** (`BY-01`–`BY-04`, `I-015` retired). Provider credentials belong to the deployment operator and are injected by secret manager or Docker secret with least privilege (`DC-15`); they never appear in the policy file, the image, the logs, the public sample or any client projection (`DC-14`). Self-host operators provision their own server credentials the same way — that is infrastructure provisioning, not customer BYOK (`I-495`). Historical BYOK changes entitlement economics without changing the permission model.

**Testing requirements.** A contract policy test asserting **no operation, schema field, setting or UI accepts a customer provider key, model endpoint or credential**; a structural test asserting no desktop, mobile or browser assembly references a provider adapter; a projection test asserting no supplier rate, route weight or credential reaches a client (`DC-14`); a secret-handling test asserting credentials are absent from the image, the sample configuration and the logs.

**Completion gate.** **No end-user BYOK path exists anywhere in the product**, and provider credentials are present only in the Cloud host's injected secrets.

### WP-43.04 — Provider interaction records and transparency

**What must be fully done.** A provider interaction record per call, separate from the execution, capability and audit traces, carrying no content beyond what policy permits. Cost transparency surfaces show what a run cost and why. AI-generated content carries the required transparency marking per artifact type.

**Testing requirements.** Trace-separation test; a content-redaction test on interaction records; a cost-explainability test; a marking-coverage test per artifact type.

**Completion gate.** Interaction records are separate and redacted, run cost is explainable to the user, and every artifact type has a defined marking. **This satisfies `VG-01` once the regime determination is recorded.**

### WP-43.05 — Availability and failure

**What must be fully done.** Provider and model availability driven by policy, with a withdrawn model degrading explicitly rather than disappearing. A provider outage fails runs with a typed reason, releases reservations, and offers a fallback where policy permits. All-routes-unavailable is a page-worthy condition.

**Testing requirements.** Model-withdrawal degradation; provider-outage reservation release; fallback routing; an alert assertion for all-routes-unavailable.

**Completion gate.** A provider outage never silently consumes credit, and a withdrawn model degrades with a stated reason.

### WP-43.07 — Real-provider metering evidence

**What must be fully done.** The complete path exercised against a **real provider**, not a fixture: normalisation of that provider's actual usage report into non-overlapping categories with its declared inclusion relationships; cumulative stream snapshots replacing rather than summing; supplier cost at the dispatch-time price version; customer cost at the Run's pinned tariff snapshot; idempotent settlement keyed on `(provider_attempt_id, usage_revision, category)`; and the `§8.6` worked fixture asserted exactly — USD 0.00244 supplier cost, 4,880,000 micro-credits customer cost, 1.12 credits released to the original funding sources.

**Testing requirements.** Two providers whose cache and reasoning fields overlap differently, both settling correctly; a duplicate usage event proving no double debit; an undeclared usage field entering reconciliation rather than a debit; a cancellation settling verified consumption and releasing the remainder; a lost final usage producing `UsagePending` and, at the deadline, releasing the customer hold while **retaining the supplier liability**; a platform-caused retry charged once to the customer and fully visible in supplier cost; a token-category and tier price change applying to future dispatch only; historical replay after replacing every current rate, reproducing the original charge exactly.

**Completion gate.** **One real provider usage response and one real payment-provider event are reconciled through the same code as the fixtures** (`MT-01`, `§10.6` of the configuration requirements). Deterministic fixtures supplement this evidence; they do not replace it.

### WP-43.06 — Provider test-environment coverage

**What must be fully done.** Every provider integration exercised against the provider's test environment, with its contract shape frozen as recorded fixtures so CI does not depend on provider availability.

**Testing requirements.** A per-provider test-environment run; a fixture-driven CI run with the provider unreachable.

**Completion gate.** Every provider is exercised against its test environment and has recorded fixtures — **satisfying `PG-10` for AI providers**.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Tariffs, interaction records and metering results |
| Protocol | AI request, response and metering contracts |
| UI | Model selection, cost transparency and availability surfaces |
| Security | BYOK secret custody; egress control on model interaction; instruction provenance on model output |
| Platform | Local model support where available, surfaced honestly |
| Migration | Tariff and interaction record schema versioning |
| Compatibility | AI contracts enter the supported window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Routing decision, explainability and streaming results | `WP-43.00` |
| Rate-change immutability and historical explainability results | `WP-43.01` |
| Metering accounting, idempotency, sweep and overdraft results | `WP-43.02` |
| BYOK boundary assertions and permission-parity results | `WP-43.03` |
| Trace separation, redaction, cost explainability and marking coverage | `WP-43.04` |
| Degradation, reservation release and alert results | `WP-43.05` |
| Per-provider test-environment runs and fixture-driven CI results | `WP-43.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Routing is policy-driven, explainable and recorded; streaming interruption never stores a partial response as complete.
2. A rate change never alters a settled charge; every historical charge is explainable from its locked tariff snapshot.
3. Metering never double-charges, never leaks a reservation, and never permits an overdraft under concurrency.
4. **No BYOK secret ever crosses a boundary it must not cross**, and BYOK never relaxes the permission model.
5. Provider interaction records are a separate, redacted trace system; run cost is explainable to the user; every artifact type has a defined transparency marking — satisfying `VG-01` once the regime determination is recorded.
6. A provider outage never silently consumes credit; a withdrawn model degrades with a stated reason; all-routes-unavailable alerts.
7. Every provider is exercised against its test environment with recorded fixtures — satisfying `PG-10` for AI providers.

---

## 9. Dependencies

**Upstream.** `16` (the budget interface), `42` (real credits and ledgers).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `50` — Production release | Managed AI as a complete, metered capability |
