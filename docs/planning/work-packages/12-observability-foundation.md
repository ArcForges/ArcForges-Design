# WP-12 — Observability Foundation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `04`, `06` · Downstream: `21`, `45`

> **Goal.** Instrument once, correctly: standard signals with a bounded dimension set, correlation that survives every hop, redaction enforced by construction, and desktop diagnostics that never leave the machine without consent.

---

## 1. Scope and purpose

**In scope.** The telemetry infrastructure shared by desktop and cloud: signal emission, the required dimension set, correlation and causation propagation, redaction, sampling and cardinality control, health probes, and the desktop diagnostic tiers with their consent flow.

**Out of scope.** The audit subsystem (`11`) — deliberately separate. Alerting, runbooks, the status page and the operator surface (`45`). Cloud-specific instrumentation of modules that do not exist yet (`21`).

**Why this package exists.** Instrumentation added late is instrumentation added inconsistently. More importantly, redaction cannot be retrofitted: once a content type has a logging representation, it will be logged.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/13-observability-and-operations.md`](../../architecture/13-observability-and-operations.md) | Signal architecture, dimensions, correlation, redaction, health, diagnostics |
| [`../../requirements/07-security-privacy-and-trust.md`](../../requirements/07-security-privacy-and-trust.md) `§17` | Privacy obligations and consent |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) `§19` | The diagnostics contract and its tiers |
| `WP-04` output | Correlation, causation and reason-code primitives |
| `WP-06` output | Published hosts to instrument |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Business code never references a vendor logging type** (`OA-02`). |
| BR-02 | **Observability is never a user-content database** (`I-273`). |
| BR-03 | **Audit and observability are separate systems** (`I-272`) with separate storage, retention and access. |
| BR-04 | **Desktop telemetry is minimal and opt-in**; local diagnostics are always available without any upload. |
| BR-05 | **A crash or diagnostic report is shown to the user before it is sent**, and a full memory dump is never sent by default. |
| BR-06 | **An unbounded identifier is never a metric label** (`SG-02`). |
| BR-07 | **A secret-bearing or content type has no logging representation** (`RD-03`, `RD-04`). |
| BR-08 | **A user-visible task identifier resolves to its trace** (`CR-04`). |
| BR-09 | **Correlation propagation is implemented once**, in shared infrastructure (`CR-06`). |
| BR-10 | **A diagnostic log is not an audit record** (`QI-23`), and **diagnostics are not telemetry consent** (`QI-24`). |

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

### WP-12.00 — Emission and dimensions

**What must be fully done.** A single emission surface for metrics, traces and structured logs, with the required dimension set attached automatically from the ambient context. A dimension present in context is always attached; one absent is omitted rather than defaulted. Build identifier and instance identity are on every signal.

**Testing requirements.** A dimension-coverage test across representative operations; a test asserting an absent dimension is omitted rather than faked.

**Completion gate.** Every emitted signal carries the applicable dimension subset, with no fabricated values.

### WP-12.01 — Correlation and causation

**What must be fully done.** Correlation created at the originating edge or accepted from a validated client value, propagated across HTTP, queue, worker, realtime and provider calls. Causation records which operation caused which. A user-visible task or run identifier resolves to its trace.

**Testing requirements.** A synthetic end-to-end action producing one connected trace across all hop kinds; a resolution test from a task identifier to its trace; a validation test rejecting a malformed client-supplied correlation value.

**Completion gate.** One synthetic action produces one connected trace across every hop kind, and a task identifier resolves to it.

### WP-12.02 — Redaction by construction

**What must be fully done.** Secret-bearing and content types have no logging representation. A scrubbing processor removes known-sensitive header and field names as a second line of defence. URLs are recorded as route templates plus identifiers. Exception messages that can embed user input are mapped to reason codes before export.

**Testing requirements.** Marker values injected as headers, tokens, prompts, note content and file paths must never appear in exported signals; a structural test asserting content types cannot be logged.

**Completion gate.** The marker test finds nothing in any exported signal, and content types are structurally unloggable. **This satisfies `PG-05`.**

### WP-12.03 — Cardinality and sampling

**What must be fully done.** Metric label sets are constrained to an allowlist, and an unbounded identifier used as a label fails the build. Sampling is head-based with tail retention for errors and slow requests, configurable per signal and per route without a code change.

**Testing requirements.** A cardinality policy test with a negative fixture; a sampling test asserting error paths are retained regardless of rate.

**Completion gate.** Unbounded labels fail the build, and error paths are retained regardless of sampling rate.

### WP-12.04 — Health probes

**What must be fully done.** Liveness, readiness and capability health as three distinct probe kinds. Readiness fails closed on a missing required dependency. Capability health uses the five health dimensions shared with the contract model.

**Testing requirements.** A dependency-outage test asserting readiness fails closed; a capability-health test reflecting a simulated degradation.

**Completion gate.** Readiness fails closed per required dependency, and capability health reflects simulated degradation.

### WP-12.05 — Desktop diagnostics and consent

**What must be fully done.** Local diagnostics always available without upload. Three tiers: minimal always-on local, user-approved report, and a time-bounded verbose session that self-disables and is visible while active. A report is generated, shown in full, and sent only after approval. No memory dump by default. Consent is revocable, and revocation stops collection immediately and locally.

**Testing requirements.** A consent-absent test asserting no client signal leaves the device; a crash test asserting no automatic upload; a verbose-session expiry test; a revocation test.

**Completion gate.** With consent absent, nothing leaves the device; a crash report requires approval; a verbose session expires on its own.

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
| Dimension coverage report | `WP-12.00` |
| A single connected trace across every hop kind | `WP-12.01` |
| Marker-injection redaction report, zero findings | `WP-12.02` |
| Cardinality negative fixture and sampling retention results | `WP-12.03` |
| Health probe fail-closed and degradation results | `WP-12.04` |
| Consent-absent, crash-approval, verbose-expiry and revocation results | `WP-12.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Every emitted signal carries its applicable dimension subset with no fabricated values.
2. One synthetic end-to-end action produces one connected trace across HTTP, queue, worker, realtime and provider hops, and a task identifier resolves to it.
3. Injected marker values never appear in exported signals, and content and secret types are structurally unloggable — satisfying `PG-05`.
4. An unbounded metric label fails the build; error paths are retained regardless of sampling rate.
5. Readiness fails closed on each required dependency, and capability health reflects simulated degradation.
6. With telemetry consent absent, no client signal leaves the device; a crash report is never sent without approval; a verbose diagnostic session self-disables.

---

## 9. Dependencies

**Upstream.** `04` (correlation, causation, reason codes), `06` (published hosts to instrument).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `21` — Cloud host | Instrumentation of the real pipeline and modules |
| `45` — Operations | Alerting, runbooks and the operator surface built on these signals |
| Every product package | The instrumentation surface its features emit through |
