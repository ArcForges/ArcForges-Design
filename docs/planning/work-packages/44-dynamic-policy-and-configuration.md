<a id="rule-wp-44"></a>

# WP-44 — Dynamic Policy and Configuration Control Plane

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `23`, `42` · Downstream: `40`, `43`, `45`, `48`, `51`, `52`

> **Goal.** Build the control plane that lets behaviour change without a release — feature flags, deterministic rollout, kill switches, schema-constrained remote configuration and compatibility policy — while keeping compiled hard limits authoritative and remaining safe under Native AOT.

---

## 1. Scope and purpose

**In scope.** The four boundaries separating policy from entitlement, settings, health and the data plane; feature and flag lifecycle; deterministic rollout; the four kill-switch modes; schema-constrained remote configuration; scoped resolution; workspace policy; compatibility policy; provider and model availability; experiments; publication, staleness, last-known-good and application timing; and explainability.

**Out of scope.** Entitlement itself (`42`). Operator tooling (`45`).

**Why this package exists.** Without a control plane, every behavioural change needs a release, and a bad version cannot be halted. With an unconstrained one, remote configuration becomes remote code — which Native AOT forbids and security should forbid anyway.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/11-policy-and-configuration.md`](../../requirements/11-policy-and-configuration.md) | The complete policy model, boundaries, kill switches and explainability |
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§12` | Configuration and secret handling |
| [WP-23](23-public-api-and-generated-clients.md#rule-wp-23), [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) output | The API surface and entitlement, which policy must not duplicate |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Policy is not entitlement, not user settings, not health, and not the data plane.** The four boundaries are enforced structurally. |
| BR-02 | **Remote configuration is data, not code.** No expression language, no downloadable logic, no dynamic assembly — a hard requirement under Native AOT. |
| BR-03 | **A compiled hard limit always wins over remote configuration.** Remote policy may tighten, never loosen, a safety limit. |
| BR-04 | **Configuration is schema-constrained and validated before application.** An invalid bundle is rejected wholesale, never partially applied. |
| BR-05 | **Rollout is deterministic per installation**, so a user does not flip between variants on each evaluation. |
| BR-06 | **Kill switches have four modes** with defined blast radius, and every activation is audited with a reason. |
| BR-07 | **A bad version must be immediately haltable** — the update feed can stop offering it and compatibility policy can block a specific range without blocking neighbours. |
| BR-08 | **A minimum-version requirement is never imposed before every channel has had a genuine chance to update.** |
| BR-09 | **Policy resolution is explainable**: the product can state which scope and which bundle produced an effective value. |
| BR-10 | **A stale bundle falls back to last-known-good, then to compiled defaults**, and the state is visible. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Policy/` | Policy authoring, bundle publication, rollout, kill switches, audit |
| `src/Cloud/ArcForges.Cloud.Modules.Configuration/` | Schema registry, validation, distribution |
| `src/BuildingBlocks/ArcForges.Policy/` | Client-side resolution, caching, staleness, last-known-good, explainability |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.Policy/` | Policy bundle and schema DTOs |
| `tests/PolicyTests/` | Boundary, validation, rollout determinism, kill-switch and staleness suites |

**Major types introduced.** `PolicyBundle`, `PolicySchema`, `PolicyVersion`, `FeatureDefinition`, `FlagDefinition`, `FlagState`, `RolloutRule`, `RolloutBucket`, `KillSwitch`, `KillSwitchMode`, `ConfigurationValue`, `ResolutionScope`, `EffectiveValue`, `ResolutionExplanation`, `StalenessState`, `LastKnownGood`, `CompatibilityRule`, `ExperimentDefinition`.

---

## 5. Required implementation work

<a id="rule-wp-44.00"></a>

### WP-44.00 — The four boundaries

**What must be fully done.** Policy, entitlement, user settings, health and data plane kept structurally distinct. A policy value can never grant entitlement; a user setting can never override a policy limit downward; health is never expressed as policy; and no user content flows through the policy channel.

**Testing requirements.** Four boundary tests with negative fixtures; an architecture test asserting no policy type reaches an entitlement decision.

**Completion gate.** Each boundary is enforced structurally with a failing negative fixture.

<a id="rule-wp-44.01"></a>

### WP-44.01 — Schema-constrained configuration

**What must be fully done.** Use the enumerated Config/Entitlement/Commerce/Agent/Policy transaction for activation head, price snapshots and offer-policy boundaries. Workspace plan changes advance under old history first.  Every configuration key has a typed schema with bounds. A bundle is validated wholesale before application and rejected atomically on any violation. No expression language or downloadable logic exists.

**Testing requirements.** Inject failure between every participant write, activate while holds exist, and retry the same revision on two replicas.  Schema validation coverage; an atomic-rejection test; a structural test asserting no dynamic evaluation path exists; an AOT publish with the policy client present.

**Completion gate.** No mixed configuration or partial policy period can become visible.  An invalid bundle is rejected atomically, no dynamic evaluation exists, and the policy client publishes AOT cleanly.

<a id="rule-wp-44.02"></a>

### WP-44.02 — Compiled hard limits

**What must be fully done.** Safety-critical limits are compiled and authoritative. Remote policy may tighten them; an attempt to loosen one is rejected and recorded.

**Testing requirements.** A loosening-rejection test per hard limit; a tightening-acceptance test; an audit assertion on rejection.

**Completion gate.** **No remote configuration can loosen a compiled hard limit**, and every attempt is rejected and recorded.

<a id="rule-wp-44.03"></a>

### WP-44.03 — Features, flags and deterministic rollout

**What must be fully done.** Feature and flag definitions with lifecycle states from introduced through to removed. Rollout deterministic per installation so evaluation is stable, with percentage, cohort and targeted rules. A flag's effective state is explainable.

**Testing requirements.** Determinism across repeated evaluations and restarts; distribution accuracy at target percentages; lifecycle transition tests.

**Completion gate.** Rollout is stable per installation across restarts and distributes accurately.

<a id="rule-wp-44.04"></a>

### WP-44.04 — Kill switches

**What must be fully done.** Four modes with defined blast radius, each requiring a reason, each audited, each with a defined client-side effect and user-visible explanation. Activation propagates promptly and is reversible.

**Testing requirements.** Per-mode activation and propagation tests; a user-visibility test; an audit-completeness test; a reversal test.

**Completion gate.** Every kill-switch mode propagates promptly with a user-visible reason and a complete audit record.

<a id="rule-wp-44.05"></a>

### WP-44.05 — Scoped resolution and explainability

**What must be fully done.** Resolution across application, workspace, device and installation scopes with a fixed order. The product can state which scope and bundle produced any effective value.

**Testing requirements.** Resolution order matrix; an explainability test per scope; a workspace-policy override test.

**Completion gate.** Resolution order is correct and every effective value is explainable to its source scope and bundle.

<a id="rule-wp-44.06"></a>

### WP-44.06 — Compatibility policy

**What must be fully done.** Compatibility rules expressing supported client windows, blocked version ranges and minimum cloud versions. A bad version can be blocked without blocking neighbouring versions. A minimum-version requirement honours the grace period before enforcement.

**Testing requirements.** Range-blocking precision tests; a grace-period enforcement test; an update-feed integration test.

**Completion gate.** **A specific bad version can be blocked without affecting neighbouring versions**, and a minimum-version requirement is not enforced before the grace period elapses.

<a id="rule-wp-44.07"></a>

### WP-44.07 — Publication, staleness and last-known-good

**What must be fully done.** Bundle publication with versioning and audit; client caching with a staleness threshold; fallback to last-known-good and then compiled defaults; the staleness state visible; application timing defined so a change never takes effect mid-operation in a way that produces inconsistent behaviour.

**Testing requirements.** Staleness fallback chain tests; a mid-operation application test; an offline-extended test; a publication audit test.

**Completion gate.** The fallback chain works to compiled defaults, staleness is visible, and a policy change never produces inconsistent behaviour mid-operation.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Policy bundles, rollout state and audit records |
| Protocol | Policy bundle distribution contracts |
| UI | Feature availability, kill-switch explanations and staleness indicators |
| Security | Kill switches are a security control; hard limits cannot be loosened remotely |
| Platform | Policy client works identically on every surface including AOT and React browser |
| Migration | Policy schema versioning |
| Compatibility | Compatibility policy is itself distributed as policy |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Four boundary negative fixtures | [WP-44.00](#rule-wp-44.00) |
| Schema validation, atomic rejection and AOT results | [WP-44.01](#rule-wp-44.01) |
| Hard-limit loosening rejection and audit results | [WP-44.02](#rule-wp-44.02) |
| Rollout determinism and distribution results | [WP-44.03](#rule-wp-44.03) |
| Per-mode kill-switch propagation, visibility and audit results | [WP-44.04](#rule-wp-44.04) |
| Resolution order and explainability results | [WP-44.05](#rule-wp-44.05) |
| Range-blocking precision and grace-period results | [WP-44.06](#rule-wp-44.06) |
| Fallback chain, staleness and mid-operation results | [WP-44.07](#rule-wp-44.07) |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Each of the four boundaries is enforced structurally with a failing negative fixture.
2. An invalid bundle is rejected atomically; no dynamic evaluation path exists; the policy client publishes AOT cleanly.
3. **No remote configuration can loosen a compiled hard limit**, and every attempt is rejected and recorded.
4. Rollout is deterministic per installation across restarts and distributes accurately at target percentages.
5. Every kill-switch mode propagates promptly with a user-visible reason and a complete audit record.
6. Resolution order is correct and every effective value is explainable to its source scope and bundle.
7. **A specific bad version can be blocked without affecting neighbouring versions**; a minimum-version requirement is not enforced before its grace period elapses.
8. The staleness fallback chain reaches compiled defaults, is visible, and a policy change never produces inconsistent behaviour mid-operation.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [23 — Public API Surface and Generated Clients](23-public-api-and-generated-clients.md)
- [42 — Commerce, Entitlement and Credits](42-commerce-entitlement-and-credits.md)

**Downstream — these consume this package’s completed output.**

- [40 — Knowledge, Search and Retrieval](40-knowledge-search-and-retrieval.md)
- [43 — Cloud AI Routing, Metering and Settlement](43-managed-ai-routing-and-metering.md)
- [45 — Operations, Support and Trust & Safety](45-operations-support-and-trust-safety.md)
- [48 — Account Portal](48-account-portal.md)
- [51 — ArcScope Deterministic Cloud Simulator](51-arcscope-cloud-simulator.md)
- [52 — The Cloud Harness](52-cloud-harness.md)
