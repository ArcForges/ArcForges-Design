<a id="rule-wp-35"></a>

# WP-35 — ArcScope Integration and Metadata Sync

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: H — ArcScope
> Upstream: `25`, `34` · Downstream: `50`

> **Goal.** Connect ArcScope to the platform on its own terms: metadata, analysis, annotations and reports sync by default; **raw capture stays local unless explicitly uploaded**; and ArcChat receives bounded structured context, never a raw capture.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcScope + Cloud; AI context consumer. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The ArcScope capability set for ArcChat; context provision as bounded structured results; cloud sync scope with raw capture excluded by default; explicit per-session raw upload; import and export including the native full-fidelity bundle; and the ArcScope V1B closure items.

**Out of scope.** Device control. Cloud-side analysis execution.

**Why this package exists.** [I-474](../../requirements/01-normative-glossary-and-invariants.md#rule-i-474) states plainly that cloud sync is not raw capture upload. This package is where that invariant becomes structural rather than a policy note, and where the sync engine's scope model ([WP-25.00](25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00)) is proven against a real exclusion requirement.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [scope.measurement.v1](../../requirements/products/arcscope.md#measurement-profile)

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) `§14`, `§15`, `§16` | AI integration, capability surface and cloud posture |
| [ArcScope product requirements](../../requirements/products/arcscope.md) | Raw captures stay local by default; metadata, analysis, annotations and reports participate in the declared Cloud scope |
| [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25) output | The sync engine and its scope model |
| [WP-34](34-arcscope-analysis-and-reporting.md#rule-wp-34) output | Analysis results and reports as the payload |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **`Cloud Sync ≠ Raw Capture Upload`** ([I-474](../../requirements/01-normative-glossary-and-invariants.md#rule-i-474)). |
| BR-02 | **Default sync scope**: project, session metadata, annotations, findings, analysis results, reports and configurations. **Raw capture is local by default.** |
| BR-03 | **Enabling project cloud sync does not upload raw capture.** Raw upload is an explicit per-session act. |
| BR-04 | **A local-only capture must not be uploaded because an AI button was pressed** ([I-182](../../requirements/01-normative-glossary-and-invariants.md#rule-i-182)). |
| BR-05 | **AI does not process an entire raw capture.** It receives necessary structured results — measurements, analysis outputs, decoded event summaries, selected ranges. |
| BR-06 | **"Ask ArcChat" passes a bounded context reference**, never the raw capture. |
| BR-07 | **A third-party extension can never write raw capture arbitrarily.** Raw capture is written by ArcScope alone. |
| BR-08 | **Native export is the complete data migration format**, and import enters the unified session model with a recorded origin. |
| BR-09 | **The raw-capture cloud policy is explicit and visible** per project and per session. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcScope/ArcScope.LocalRpc/` | Capability registration: query, analysis, authoring and operational capabilities |
| `src/ArcScope/ArcScope.CloudClient/` | Sync scope mapping with raw capture excluded by default; explicit raw upload path |
| `src/ArcScope/ArcScope.ImportExport/` | Native bundle, tabular export with precision warnings, import with origin recording |
| `src/ArcScope/ArcScope.Application/` | Context provision as bounded structured results |
| `fixtures/formats/arcscope/` | Capture and bundle fixtures for every claimed version |
| `tests/SyncConflictTests/ArcScope/` | Scope exclusion, explicit upload and convergence suites |

**Major types introduced.** `ScopeCapabilitySet`, `SessionContextReference`, `StructuredResultBundle`, `RawUploadRequest`, `RawCapturePolicy`, `NativeBundle`, `ImportOrigin`.

---

## 5. Required implementation work

<a id="rule-wp-35.00"></a>

### WP-35.00 — Capability surface

**What must be fully done.** Query capabilities (projects, sessions, captures, channels, signals, events; measurements, analysis results, annotations, findings, configuration snapshots), analysis capabilities (run a measurement or analysis, apply a recipe, compare sessions), authoring capabilities (annotation, finding, report) and operational capabilities (start and stop capture) — each with its risk level, permission requirement and approval posture.

**Testing requirements.** Descriptor validation per capability; owner-side refusal tests; an operational-capability risk assertion.

**Completion gate.** Every capability declares risk and approval posture, and start and stop capture are treated as operations with real side effects rather than read-only conveniences.

<a id="rule-wp-35.01"></a>

### WP-35.01 — Bounded context provision

**Required design implementation and verification.** Project measurement values with profile, immutable source/configuration binding, counts, coverage and status into bounded context/report references. Test that unknown-profile and insufficient results are never silently rendered as a numeric zero.

**What must be fully done.** ArcScope contributes structured results — measurements, analysis outputs, decoded event summaries and selected ranges — as bounded context. A raw capture is never a context payload. Context size is visible and oversized context is refused explicitly.

**Testing requirements.** A structural test asserting raw capture cannot enter a context payload; a bounding test; a visibility test.

**Completion gate.** **Raw capture structurally cannot enter an AI context payload**, and oversized context is refused explicitly.

<a id="rule-wp-35.02"></a>

### WP-35.02 — Cloud sync scope

**What must be fully done.** The ArcScope sync scope excludes raw capture by default and includes metadata, analysis, annotations, findings, reports and configurations. Enabling project sync never uploads raw capture. The policy is visible per project and per session.

**Testing requirements.** An enable-sync test asserting no raw bytes are transferred; a policy-visibility test; a convergence test across devices for the included scope.

**Completion gate.** Enabling project sync transfers no raw capture bytes, and the included scope converges across devices.

<a id="rule-wp-35.03"></a>

### WP-35.03 — Explicit raw upload

**What must be fully done.** Raw upload as an explicit per-session act with a clear statement of size, destination and consequence, using the chunked upload path with resumption and verification. It is never triggered by an AI action or by enabling sync.

**Testing requirements.** An explicit-upload flow test; a negative test asserting no automatic trigger path exists; resumption and verification tests on a large capture.

**Completion gate.** Raw upload is explicit only, resumable and verified, with **no automatic trigger path anywhere**.

<a id="rule-wp-35.04"></a>

### WP-35.04 — Import, export and fixtures

**Required design implementation and verification.** Native bundles preserve origin, measurement profile/configuration and simulator provenance separately. CSV/JSON/report export publishes required sidecars atomically; structured context carries selected origins and measurement quality, never raw capture.

**What must be fully done.** Native full-fidelity bundle export and import with equivalence; tabular export with explicit precision warnings; import entering the unified session model with a recorded origin, never disguised as a live device. A fixture exists for every claimed import version.

**Testing requirements.** Bundle round-trip equivalence; precision-warning assertions; origin-recording test; fixture coverage for every claimed version.

**Completion gate.** The native bundle round-trips with equivalence, imports record their origin, and every claimed import version has a fixture. **This satisfies [PG-07](../../assurance/open-gates-register.md#rule-pg-07) for ArcScope.**

<a id="rule-wp-35.05"></a>

### WP-35.05 — Extension boundary

**What must be fully done.** A structural guarantee that a third-party extension cannot write raw capture. Extension access to ArcScope is through capabilities with owner-side validation only.

**Testing requirements.** A structural test asserting no extension-reachable raw write path exists; an owner-side refusal test from an extension caller.

**Completion gate.** No extension-reachable path can write raw capture.

---

<a id="rule-wp-35.90"></a>
### WP-35.90 — Verify the owned artifact and real integration

**What must be fully done.** Bind bounded context, managed metadata, explicit raw-data uploads and resource references to gRPC/R2/CF. Preserve input selection and source authorization.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Metadata sync and explicit-upload behavior remain distinct; context/report data retain measurement identity and ownership across real service calls.

**Completion gate.** Metadata sync and explicit-upload behavior remain distinct; context/report data retain measurement identity and ownership across real service calls. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Sync scope mapping and raw upload state |
| Protocol | ArcScope capabilities and context contracts |
| UI | Sync policy, raw upload and AI context surfaces |
| Security | Raw capture as the most sensitive local data, structurally protected |
| Platform | Large upload behaviour per platform and network |
| Migration | Bundle format versioning |
| Compatibility | ArcScope import claims backed by fixtures |

---

## 7. Tests and verification evidence

**Required evidence addition.** Structured context and bundle round-trip retain measurement meaning without raw capture leakage.

**Required evidence addition.** [WP-35.04](#rule-wp-35.04) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Capability descriptor and refusal results | [WP-35.00](#rule-wp-35.00) |
| Structural raw-capture exclusion and bounding results | [WP-35.01](#rule-wp-35.01) |
| No-raw-bytes sync assertion and convergence results | [WP-35.02](#rule-wp-35.02) |
| Explicit upload, no-auto-trigger and resumption results | [WP-35.03](#rule-wp-35.03) |
| Bundle round-trip, precision warnings, origin and fixture coverage | [WP-35.04](#rule-wp-35.04) |
| Extension no-write structural results | [WP-35.05](#rule-wp-35.05) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-35.90](#rule-wp-35.90) and all inherited domain-specific gates must pass on the same candidate closure. Metadata sync and explicit-upload behavior remain distinct; context/report data retain measurement identity and ownership across real service calls.

**[PG-03](../../assurance/open-gates-register.md#rule-pg-03) evidence:** [WP-35.04](#rule-wp-35.04) — Recorded substitute analysis and native import dependency licence disposition before use. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** Reported/imported measurement meaning and numerical profile survive the declared portability path.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Every ArcScope capability declares risk and approval posture; start and stop capture are treated as real side effects.
2. **Raw capture structurally cannot enter an AI context payload**; oversized context is refused explicitly.
3. Enabling project cloud sync transfers no raw capture bytes; the included scope converges across devices.
4. Raw upload is explicit only, resumable and verified, with no automatic trigger path anywhere.
5. The native bundle round-trips with equivalence; imports record origin and never impersonate a live device; every claimed import version has a fixture — satisfying [PG-07](../../assurance/open-gates-register.md#rule-pg-07) for ArcScope.
6. No extension-reachable path can write raw capture.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [25 sync engine and blob lifecycle](25-sync-engine-and-blob-lifecycle.md#rule-wp-25)
- [34 arcscope analysis and reporting](34-arcscope-analysis-and-reporting.md#rule-wp-34)

**Downstream — consumers of these released outputs.**

- [50 full platform production release](50-full-platform-production-release.md#rule-wp-50)

---
