<a id="rule-wp-44"></a>

# WP-44 — Dynamic Policy and Configuration Control Plane

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Build the control plane that lets behaviour change without a release — feature flags, deterministic rollout, kill switches, schema-constrained remote configuration and compatibility policy — while keeping compiled hard limits authoritative and remaining safe under Native AOT.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud authority; AI/clients consumers. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The four boundaries separating policy from entitlement, settings, health and the data plane; feature and flag lifecycle; deterministic rollout; the four kill-switch modes; schema-constrained remote configuration; scoped resolution; workspace policy; compatibility policy; provider and model availability; experiments; publication, staleness, last-known-good and application timing; and explainability.

**Out of scope.** Entitlement itself (`42`). Operator tooling (`45`).

**Why this package exists.** Without a control plane, every behavioural change needs a release, and a bad version cannot be halted. With an unconstrained one, remote configuration becomes remote code — which Native AOT forbids and security should forbid anyway.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../requirements/11-policy-and-configuration.md`](../../requirements/11-policy-and-configuration.md) | The complete policy model, boundaries, kill switches and explainability |
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§12` | Configuration and secret handling |
| [WP-23](23-public-api-and-generated-clients.md#rule-wp-23), [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) output | The API surface and entitlement, which policy must not duplicate |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Policy is not entitlement, not user settings, not health, and not the data plane.** The four boundaries are enforced structurally. |
| <a id="rule-br-02"></a>BR-02 | **Remote configuration is data, not code.** No expression language, no downloadable logic, no dynamic assembly — a hard requirement under Native AOT. |
| <a id="rule-br-03"></a>BR-03 | **A compiled hard limit always wins over remote configuration.** Remote policy may tighten, never loosen, a safety limit. |
| <a id="rule-br-04"></a>BR-04 | **Configuration is schema-constrained and validated before application.** An invalid bundle is rejected wholesale, never partially applied. |
| <a id="rule-br-05"></a>BR-05 | **Rollout is deterministic per installation**, so a user does not flip between variants on each evaluation. |
| <a id="rule-br-06"></a>BR-06 | **Kill switches have four modes** with defined blast radius, and every activation is audited with a reason. |
| <a id="rule-br-07"></a>BR-07 | **A bad version must be immediately haltable** — the update feed can stop offering it and compatibility policy can block a specific range without blocking neighbours. |
| <a id="rule-br-08"></a>BR-08 | **A minimum-version requirement is never imposed before every channel has had a genuine chance to update.** |
| <a id="rule-br-09"></a>BR-09 | **Policy resolution is explainable**: the product can state which scope and which bundle produced an effective value. |
| <a id="rule-br-10"></a>BR-10 | **A stale bundle falls back to last-known-good, then to compiled defaults**, and the state is visible. |

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

**What must be fully done.** Consume policy.body.v1 and configuration.v1 from annex 08; implement full exact-key/type/scope/limit/cross-reference validation and dry-run proposal/dual-approval/activation CAS.

**Testing requirements.** Unknown key/field/version, invalid commercial route, secret-in-body, conflicting rule priority, stale parent, mixed-replica version and rollback tests.

**Completion gate.** No JSON payload with implementer-defined keys can activate.

<a id="rule-wp-44.02"></a>

### WP-44.02 — Compiled hard limits

**What must be fully done.** Safety-critical limits are compiled and authoritative. Remote policy may tighten them; an attempt to loosen one is rejected and recorded.

**Testing requirements.** A loosening-rejection test per hard limit; a tightening-acceptance test; an audit assertion on rejection.

**Completion gate.** **No remote configuration can loosen a compiled hard limit**, and every attempt is rejected and recorded.

<a id="rule-wp-44.03"></a>

### WP-44.03 — Features, flags and deterministic rollout

**What must be fully done.** Implement deterministic target predicate/percent hashing, exclusion groups, sticky experiment allocation and explicit-setting/entitlement priority from annex 08; preserve past variant evidence.

**Testing requirements.** Independent byte/hash/bucket vectors, boundary 0/9999, holdout, overlapping exclusion group, account/device change and cached signed bundle expiry.

**Completion gate.** Same stable subject/version selects the same result across languages and cannot grant commercial/security authority.

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

<a id="rule-wp-44.90"></a>
### WP-44.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement versioned compatibility/model/cost/security policy with explicit C#/CF activation and stale-policy behavior. Keep signed/auditable targeting and rollback horizons.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** A CF run and each effect use the required policy version; stale/disallowed models or revoked permission fail deterministically, without client-side policy becoming authority.

**Completion gate.** A CF run and each effect use the required policy version; stale/disallowed models or revoked permission fail deterministically, without client-side policy becoming authority. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Operator contract closure.** Consume [registry04 §9](../../architecture/contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary) and [model01 operator state](../../architecture/data-model/01-cloud-data-model.md#operator-proposal-approval-and-financial-owner-closure). Generate/implement every operation exactly once with its eight authorization fields, operator scope and [OC-03](../../requirements/10-distribution-update-and-support.md#rule-oc-03) role binding. Public customer/PAT/agent access refuses. Verify distinct approver, stale hash/revision/configuration, role revocation, expiry, concurrent consumption and lost receipt; no direct SQL or public-SDK operator import. WP03 produces schema/negative vectors, WP23 real identity/dispatch conformance, WP42 the financial owners, WP44 configuration/policy owners, and WP45 the real console join. Earlier packages retain their named fixture boundary until the existing downstream join.

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
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-44.90](#rule-wp-44.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-44.90](#rule-wp-44.90) and all inherited domain-specific gates must pass on the same candidate closure. A CF run and each effect use the required policy version; stale/disallowed models or revoked permission fail deterministically, without client-side policy becoming authority.

**[PG-16](../../assurance/open-gates-register.md#rule-pg-16) evidence:** [WP-44.01](#rule-wp-44.01) — Atomic version activation/rejection and two-policy/no-retroactivity/concurrent-replica results, combined with durable capacity evidence from package 42. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

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

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [POL.01](../delivery/lanes/policy.md#task-pol-01) | [WP-44.00](44-dynamic-policy-and-configuration.md#rule-wp-44.00) (full) | none |
| [POL.02](../delivery/lanes/policy.md#task-pol-02) | [WP-44.01](44-dynamic-policy-and-configuration.md#rule-wp-44.01) (full)<br>[WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) Operator contract closure — configuration/policy owners (operator contract closure; configuration/policy owner: dry-run proposal/dual-approval/activation CAS as the typed proposal protocol) | [CON.12](../delivery/lanes/contracts.md#task-con-12) (contract) |
| [POL.03](../delivery/lanes/policy.md#task-pol-03) | [WP-44.02](44-dynamic-policy-and-configuration.md#rule-wp-44.02) (full) | none |
| [POL.04](../delivery/lanes/policy.md#task-pol-04) | [WP-44.03](44-dynamic-policy-and-configuration.md#rule-wp-44.03) (server-side flag/rollout definition, publication and byte/hash/bucket algorithm; on-device execution split to POL.09) | [COM.05](../delivery/lanes/commerce.md#task-com-05) (artifact) |
| [POL.05](../delivery/lanes/policy.md#task-pol-05) | [WP-44.04](44-dynamic-policy-and-configuration.md#rule-wp-44.04) (full)<br>[WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) operator contract closure; the 'kill' typed operator RPC (operator contract closure; the 'kill' typed operator RPC)<br>[WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) Operator contract closure — configuration/policy owners (package-level obligation contribution) | [CON.14](../delivery/lanes/contracts.md#task-con-14) (contract) |
| [POL.06](../delivery/lanes/policy.md#task-pol-06) | [WP-44.05](44-dynamic-policy-and-configuration.md#rule-wp-44.05) (server-side resolution across application/workspace/device/installation scopes with fixed order, and the explainability endpoint/data; client-side consumption split to POL.09) | none |
| [POL.07](../delivery/lanes/policy.md#task-pol-07) | [WP-44.06](44-dynamic-policy-and-configuration.md#rule-wp-44.06) (full) | none |
| [POL.08](../delivery/lanes/policy.md#task-pol-08) | [WP-44.07](44-dynamic-policy-and-configuration.md#rule-wp-44.07) (bundle publication with versioning and audit; server-side staleness signalling; the application-timing contract clients must honour. Client caching/fallback/mid-operation behaviour split to POL.09) | none |
| [POL.09](../delivery/lanes/policy.md#task-pol-09) | [WP-44.05](44-dynamic-policy-and-configuration.md#rule-wp-44.05) (client-side consumption of scoped resolution/explainability)<br>[WP-44.07](44-dynamic-policy-and-configuration.md#rule-wp-44.07) (client caching, staleness threshold, fallback to last-known-good then compiled defaults, staleness visible, mid-operation application timing)<br>[WP-44.03](44-dynamic-policy-and-configuration.md#rule-wp-44.03) (client execution of the deterministic rollout hash so the same subject/version selects the same result on-device) | [CON.12](../delivery/lanes/contracts.md#task-con-12) (contract), [CON.22](../delivery/lanes/contracts.md#task-con-22) (contract) |
| [POL.10](../delivery/lanes/policy.md#task-pol-10) | [WP-44.90](44-dynamic-policy-and-configuration.md#rule-wp-44.90) (full) | none |
| [POL.11](../delivery/lanes/policy.md#task-pol-11) | [WP-44.07](44-dynamic-policy-and-configuration.md#rule-wp-44.07) (real fallback chain against a deployed publication endpoint) | none |

**Consumers outside this package:** [AIR.00](../delivery/lanes/ai-routing.md#task-air-00), [AIR.01](../delivery/lanes/ai-routing.md#task-air-01), [CLOUD.64](../delivery/lanes/cloud.md#task-cloud-64), [OPS.05](../delivery/lanes/operations.md#task-ops-05), [OPS.13](../delivery/lanes/operations.md#task-ops-13), [REL.06](../delivery/lanes/release.md#task-rel-06), [REL.08](../delivery/lanes/release.md#task-rel-08), [SIM.07](../delivery/lanes/simulator.md#task-sim-07), [SRCH.06](../delivery/lanes/search.md#task-srch-06), [SRCH.90](../delivery/lanes/search.md#task-srch-90), [UPD.05](../delivery/lanes/updater.md#task-upd-05), [UPD.08](../delivery/lanes/updater.md#task-upd-08), [WEB.14](../delivery/lanes/web.md#task-web-14), [WEB.29](../delivery/lanes/web.md#task-web-29).

<!-- delivery-graph:end -->

