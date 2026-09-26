<a id="rule-wp-12"></a>

# WP-12 — Observability Foundation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Instrument once, correctly: standard signals with a bounded dimension set, correlation that survives every hop, redaction enforced by construction, and desktop diagnostics that never leave the machine without consent.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Shared headless tooling; all emitters. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The telemetry infrastructure shared by desktop and cloud: signal emission, the required dimension set, correlation and causation propagation, redaction, sampling and cardinality control, health probes, and the desktop diagnostic tiers with their consent flow.

**Out of scope.** The audit subsystem (`11`) — deliberately separate. Alerting, runbooks, the status page and the operator surface (`45`). Cloud-specific instrumentation of modules that do not exist yet (`21`).

**Why this package exists.** Instrumentation added late is instrumentation added inconsistently. More importantly, redaction cannot be retrofitted: once a content type has a logging representation, it will be logged.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/13-observability-and-operations.md`](../../architecture/13-observability-and-operations.md) | Signal architecture, dimensions, correlation, redaction, health, diagnostics |
| [`../../requirements/07-security-privacy-and-trust.md`](../../requirements/07-security-privacy-and-trust.md) `§17` | Privacy obligations and consent |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) `§19` | The diagnostics contract and its tiers |
| [WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04) output | Correlation, causation and reason-code primitives |
| [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) output | Published hosts to instrument |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Business code never references a vendor logging type** ([OA-02](../../architecture/13-observability-and-operations.md#rule-oa-02)). |
| <a id="rule-br-02"></a>BR-02 | **Observability is never a user-content database** ([I-273](../../requirements/01-normative-glossary-and-invariants.md#rule-i-273)). |
| <a id="rule-br-03"></a>BR-03 | **Audit and observability are separate systems** ([I-272](../../requirements/01-normative-glossary-and-invariants.md#rule-i-272)) with separate storage, retention and access. |
| <a id="rule-br-04"></a>BR-04 | **Desktop telemetry is minimal and opt-in**; local diagnostics are always available without any upload. |
| <a id="rule-br-05"></a>BR-05 | **A crash or diagnostic report is shown to the user before it is sent**, and a full memory dump is never sent by default. |
| <a id="rule-br-06"></a>BR-06 | **An unbounded identifier is never a metric label** ([SG-02](../../architecture/13-observability-and-operations.md#rule-sg-02)). |
| <a id="rule-br-07"></a>BR-07 | **A secret-bearing or content type has no logging representation** ([RD-03](../../architecture/13-observability-and-operations.md#rule-rd-03), [RD-04](../../architecture/13-observability-and-operations.md#rule-rd-04)). |
| <a id="rule-br-08"></a>BR-08 | **A user-visible task identifier resolves to its trace** ([CR-04](../../architecture/13-observability-and-operations.md#rule-cr-04)). |
| <a id="rule-br-09"></a>BR-09 | **Correlation propagation is implemented once**, in shared infrastructure ([CR-06](../../architecture/13-observability-and-operations.md#rule-cr-06)). |
| <a id="rule-br-10"></a>BR-10 | **A diagnostic log is not an audit record** ([QI-23](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-23)), and **diagnostics are not telemetry consent** ([QI-24](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-24)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Observability/` | Reconciled and extended: emission, dimensions, correlation, redaction processor, sampling, health |
| `src/BuildingBlocks/ArcForges.Observability.Desktop/` | Created: local diagnostic store, tiers, report generation, consent flow |
| `eng/policy/telemetry-policy.json` | Created: dimension allowlist, metric label allowlist, sampling and retention configuration |
| `tests/ObservabilityTests/` | Created: redaction markers, correlation propagation, cardinality assertions, consent behaviour |

**Major types introduced.** `SignalContext`, `CorrelationId`, `CausationId`, `TelemetryScope`, `RedactionProcessor`, `MetricLabelSet`, `SamplingPolicy`, `HealthProbe`, `DiagnosticTier`, `DiagnosticReport`, `TelemetryConsent`.

---

## 5. Required implementation work

<a id="rule-wp-12.00"></a>

### WP-12.00 — Emission and dimensions

**What must be fully done.** A single emission surface for metrics, traces and structured logs, with the required dimension set attached automatically from the ambient context. A dimension present in context is always attached; one absent is omitted rather than defaulted. Build identifier and instance identity are on every signal.

**Testing requirements.** A dimension-coverage test across representative operations; a test asserting an absent dimension is omitted rather than faked.

**Completion gate.** Every emitted signal carries the applicable dimension subset, with no fabricated values.

<a id="rule-wp-12.01"></a>

### WP-12.01 — Correlation and causation

**What must be fully done.** Correlation created at the originating edge or accepted from a validated client value, propagated across HTTP, queue, worker, realtime and provider calls. Causation records which operation caused which. A user-visible task or run identifier resolves to its trace.

**Testing requirements.** A synthetic end-to-end action producing one connected trace across all hop kinds; a resolution test from a task identifier to its trace; a validation test rejecting a malformed client-supplied correlation value.

**Completion gate.** One synthetic action produces one connected trace across every hop kind, and a task identifier resolves to it.

<a id="rule-wp-12.02"></a>

### WP-12.02 — Redaction by construction

**What must be fully done.** Secret-bearing and content types have no logging representation. A scrubbing processor removes known-sensitive header and field names as a second line of defence. URLs are recorded as route templates plus identifiers. Exception messages that can embed user input are mapped to reason codes before export.

**Testing requirements.** Marker values injected as headers, tokens, prompts, note content and file paths must never appear in exported signals; a structural test asserting content types cannot be logged.

**Completion gate.** The marker test finds nothing in any exported signal, and content types are structurally unloggable. **This satisfies [PG-05](../../assurance/open-gates-register.md#rule-pg-05).**

<a id="rule-wp-12.03"></a>

### WP-12.03 — Cardinality and sampling

**What must be fully done.** Enforce metric labels and bounded trace policy from observability 13: head sample plus a bounded diagnostic buffer, error/slow promotion only for spans still retained, explicit overflow/loss counters. Unsampled mandatory error facts remain redacted logs/metrics under consent.

**Testing requirements.** Cardinality negative fixture, sampled/unsampled error, slow-span buffer expiry, overflow and disabled-consent tests.

**Completion gate.** No false all-errors trace retention guarantee; bounded cost and observable loss.

<a id="rule-wp-12.04"></a>

### WP-12.04 — Health probes

**What must be fully done.** Liveness, readiness and capability health as three distinct probe kinds. Readiness fails closed on a missing required dependency. Capability health uses the five health dimensions shared with the contract model.

**Testing requirements.** A dependency-outage test asserting readiness fails closed; a capability-health test reflecting a simulated degradation.

**Completion gate.** Readiness fails closed per required dependency, and capability health reflects simulated degradation.

<a id="rule-wp-12.05"></a>

### WP-12.05 — Desktop diagnostics and consent

**What must be fully done.** Local diagnostics always available without upload. Three tiers: minimal always-on local, user-approved report, and a time-bounded verbose session that self-disables and is visible while active. A report is generated, shown in full, and sent only after approval. No memory dump by default. Consent is revocable, and revocation stops collection immediately and locally.

**Testing requirements.** A consent-absent test asserting no client signal leaves the device; a crash test asserting no automatic upload; a verbose-session expiry test; a revocation test.

**Completion gate.** With consent absent, nothing leaves the device; a crash report requires approval; a verbose session expires on its own.

---

<a id="rule-wp-12.90"></a>
### WP-12.90 — Verify the owned artifact and real integration

**What must be fully done.** Carry correlation/causation, run/attempt, model-call and artifact identities through C# ↔ CF ↔ device. Apply existing redaction, bounded cardinality and desktop consent; define selected AOT/Worker exporters.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** A trace can join one request across owners without logging prompts, credentials or unbounded payloads; health distinguishes backend, CF/model and R2 failures.

**Completion gate.** A trace can join one request across owners without logging prompts, credentials or unbounded payloads; health distinguishes backend, CF/model and R2 failures. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Local diagnostic store on desktop; telemetry storage is external |
| Protocol | Correlation headers and message metadata |
| UI | Diagnostic view, consent surface, verbose-session indicator |
| Security | Redaction is a security control; diagnostics are separate from audit |
| Platform | Per-platform crash capture and local diagnostic locations |
| Migration | None |
| Compatibility | Correlation propagation is part of the wire contract |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Dimension coverage report | [WP-12.00](#rule-wp-12.00) |
| A single connected trace across every hop kind | [WP-12.01](#rule-wp-12.01) |
| Marker-injection redaction report, zero findings | [WP-12.02](#rule-wp-12.02) |
| Cardinality negative fixture and sampling retention results | [WP-12.03](#rule-wp-12.03) |
| Health probe fail-closed and degradation results | [WP-12.04](#rule-wp-12.04) |
| Consent-absent, crash-approval, verbose-expiry and revocation results | [WP-12.05](#rule-wp-12.05) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-12.90](#rule-wp-12.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-12.90](#rule-wp-12.90) and all inherited domain-specific gates must pass on the same candidate closure. A trace can join one request across owners without logging prompts, credentials or unbounded payloads; health distinguishes backend, CF/model and R2 failures.

**All of the following, with recorded evidence:**

1. Every emitted signal carries its applicable dimension subset with no fabricated values.
2. One synthetic end-to-end action produces one connected trace across HTTP, queue, worker, realtime and provider hops, and a task identifier resolves to it.
3. Injected marker values never appear in exported signals, and content and secret types are structurally unloggable — satisfying [PG-05](../../assurance/open-gates-register.md#rule-pg-05).
4. An unbounded metric label fails the build; error paths are retained regardless of sampling rate.
5. Readiness fails closed on each required dependency, and capability health reflects simulated degradation.
6. With telemetry consent absent, no client signal leaves the device; a crash report is never sent without approval; a verbose diagnostic session self-disables.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [PLT.47](../delivery/lanes/platform.md#task-plt-47) | [WP-12.00](12-observability-foundation.md#rule-wp-12.00) (full) | [FND.01](../delivery/lanes/foundation.md#task-fnd-01) (artifact) |
| [PLT.48](../delivery/lanes/platform.md#task-plt-48) | [WP-12.01](12-observability-foundation.md#rule-wp-12.01) (full) | none |
| [PLT.49](../delivery/lanes/platform.md#task-plt-49) | [WP-12.02](12-observability-foundation.md#rule-wp-12.02) (full)<br>[WP-12](12-observability-foundation.md#rule-wp-12) eng/policy/telemetry-policy.json creation: dimension allowlist, metric label allowlist, sampling and retention configuration (package-level obligation contribution) | [PLT.40](../delivery/lanes/platform.md#task-plt-40) (artifact), [FND.05](../delivery/lanes/foundation.md#task-fnd-05) (artifact) |
| [PLT.50](../delivery/lanes/platform.md#task-plt-50) | [WP-12.03](12-observability-foundation.md#rule-wp-12.03) (full)<br>[WP-12](12-observability-foundation.md#rule-wp-12) eng/policy/telemetry-policy.json creation: dimension allowlist, metric label allowlist, sampling and retention configuration (package-level obligation contribution) | none |
| [PLT.51](../delivery/lanes/platform.md#task-plt-51) | [WP-12.04](12-observability-foundation.md#rule-wp-12.04) (full) | [PLT.23](../delivery/lanes/platform.md#task-plt-23) (artifact) |
| [PLT.52](../delivery/lanes/platform.md#task-plt-52) | [WP-12.05](12-observability-foundation.md#rule-wp-12.05) (full) | [PLT.31](../delivery/lanes/platform.md#task-plt-31) (artifact) |
| [PLT.53](../delivery/lanes/platform.md#task-plt-53) | [WP-12.90](12-observability-foundation.md#rule-wp-12.90) (full) | none |

**Consumers outside this package:** [UPD.06](../delivery/lanes/updater.md#task-upd-06).

<!-- delivery-graph:end -->

