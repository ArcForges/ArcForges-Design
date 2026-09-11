<a id="rule-wp-39"></a>

# WP-39 — ArcSlate Integration and Portability

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: I — ArcSlate
> Upstream: `25`, `38` · Downstream: `50`

> **Goal.** Connect ArcSlate to the platform once its timeline, command and undo semantics are stable — never before — and make projects genuinely portable: collect, consolidate, export, re-import and relink across machines.

---

## 1. Scope and purpose

**In scope.** The ArcSlate capability set exposed to ArcChat; bounded context provision; collect and consolidate; the portable project package; cross-device media resolution and relinking; interchange import and export; cloud sync scope with large media handled correctly; and the ArcSlate V1B closure items.

**Out of scope.** Cloud-side rendering. Collaborative editing.

**Why this package exists.** This package’s binding rule and [ArcSlate capability acceptance](#rule-wp-39.00) require: **ArcChat capabilities must only be exposed once timeline, command and undo semantics stabilise; do not lock APIs prematurely.** This package is where that condition is finally met.

---

## 2. Required inputs and dependencies

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [ArcSlate product requirements](../../requirements/products/arcslate.md#15-cross-product-integration) | The capability boundary; this package’s binding rules require stable timeline, command and undo semantics before exposing it |
| [`../../requirements/products/arcslate.md`](../../requirements/products/arcslate.md) `§13`–`§16` | Portability, cross-device behaviour, AI integration and the capability surface |
| [`../../requirements/13-data-formats-and-portability.md`](../../requirements/13-data-formats-and-portability.md) | The portability constitution and collect/consolidate obligations |
| [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25), [WP-38](38-arcslate-render-and-colour.md#rule-wp-38) output | The sync engine and a complete render and export path |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Capabilities are exposed only after timeline, command and undo semantics are stable**. |
| BR-02 | **ArcSlate's big media never goes through the ArcChat Hub.** |
| BR-03 | **Collect or consolidate gathers external media into a managed portable form on request, without destroying the originals.** |
| BR-04 | **The same asset may resolve to different locations on different devices** and remains one logical asset. |
| BR-05 | **Offline media is a normal state** and never blocks opening a project. |
| BR-06 | **AI receives bounded structured context** — sequence structure, markers, selected ranges, metadata — never raw media. |
| BR-07 | **A render is a native Product Job owned by ArcSlate** ([RN-03](../../requirements/products/arcslate.md#rule-rn-03), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)), visible in the shared task centre alongside Cloud Agent Tasks with correct ownership attribution. |
| BR-08 | **Caches, proxies and analysis outputs are never synced as authority**; they are derived and rebuildable. |
| BR-09 | **Interchange export states its fidelity** and never silently drops timeline structure. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcSlate/ArcSlate.LocalRpc/` | Capability registration: query, edit, render, export and artifact capabilities |
| `src/ArcSlate/ArcSlate.ImportExport/` | Collect and consolidate, portable package, interchange import and export |
| `src/ArcSlate/ArcSlate.CloudClient/` | Sync scope with project data synced and heavyweight media handled explicitly |
| `src/ArcSlate/ArcSlate.Application/` | Context provision, relink and media resolution services |
| `fixtures/formats/arcslate/` | Project and interchange fixtures for every claimed version |
| `tests/EndToEndTests/ArcSlate/` | Capability, portability, relink and sync suites |

**Major types introduced.** `SlateCapabilitySet`, `SequenceContextReference`, `CollectRequest`, `ConsolidateReport`, `PortableProjectPackage`, `MediaResolutionStrategy`, `RelinkPlan`, `InterchangeExport`, `SlateSyncScope`.

---

## 5. Required implementation work

<a id="rule-wp-39.00"></a>

### WP-39.00 — Capability surface

**What must be fully done.** Query capabilities over projects, sequences, timelines, media and markers; edit capabilities with explicit risk and approval; render and export capabilities as Tasks; and artifact production for rendered output. Each declares risk, side-effect class, reversibility and approval posture, with owner-side validation always.

**Testing requirements.** Descriptor validation; owner-side refusal; idempotency per write capability; a stability assertion that the capability contract was frozen only after the semantics stabilised.

**Completion gate.** Every capability declares its risk and approval posture with owner-side validation, and the contract was frozen only after timeline, command and undo semantics stabilised.

<a id="rule-wp-39.01"></a>

### WP-39.01 — Bounded context provision

**What must be fully done.** Context as sequence structure, markers, selected ranges, timecodes and metadata. Raw media never enters a context payload. Size is bounded and visible.

**Testing requirements.** A structural test asserting media data cannot enter a context payload; bounding and visibility tests.

**Completion gate.** **Raw media structurally cannot enter an AI context payload**, and oversized context is refused explicitly.

<a id="rule-wp-39.02"></a>

### WP-39.02 — Collect, consolidate and the portable package

**What must be fully done.** Collect or consolidate gathers external media into a managed portable form on request, reporting exactly what was gathered, what was skipped and why, without destroying originals. The portable package contains project data plus managed media and re-imports with equivalence.

**Testing requirements.** Collect with mixed available and offline media; an originals-untouched assertion; package round-trip equivalence; a large-project performance measurement.

**Completion gate.** Collect never destroys originals, reports skipped items honestly, and the portable package round-trips with equivalence.

<a id="rule-wp-39.03"></a>

### WP-39.03 — Cross-device resolution and relink

**What must be fully done.** Media resolution strategies per device with a relink workflow that handles moved, renamed and partially available media. A project opens with media offline, and relinking restores full function without altering edit decisions.

**Testing requirements.** Open-with-all-offline; relink after a path change; partial relink; a test asserting edit decisions survive every relink path.

**Completion gate.** A project opens with all media offline and relinks without altering any edit decision.

<a id="rule-wp-39.04"></a>

### WP-39.04 — Sync scope

**What must be fully done.** Project data, sequences, markers, presets and metadata sync. Heavyweight media follows an explicit policy rather than being swept up by enabling sync. Derived data — proxies, caches, analysis — never syncs as authority. Big media never traverses the Hub.

**Testing requirements.** An enable-sync test asserting no heavyweight media is transferred implicitly; a derived-data exclusion assertion; a Hub no-body assertion; multi-device project convergence.

**Completion gate.** Enabling sync never implicitly transfers heavyweight media, derived data never syncs as authority, and projects converge across devices.

<a id="rule-wp-39.05"></a>

### WP-39.05 — OTIO interchange

**Required design implementation and verification.** Preserve origin in native collect/import and OTIO metadata.arcforges.contentOrigin; hash the final output in its sidecar. Test unknown fields, export-local IDs/parent truncation and AI/non-AI mixed assets through the real OTIO round trip; no private source path enters the marker.

**What must be fully done.** Implement the official double value/rate ingress/egress under [OB-01](../../architecture/23-simulator-and-interchange.md#rule-ob-01)–[OB-05](../../architecture/23-simulator-and-interchange.md#rule-ob-05) of the simulator/interchange architecture, with exact binary-rational conversion, declared rate normalisation, checked range and one rounded projection.  Canonical `.otio` **import and export**, both directions, in V1 ([OT-01](../../requirements/products/arcslate.md#rule-ot-01)). A declared support profile naming the pinned library, supported schema versions and supported top-level types ([OT-02](../../requirements/products/arcslate.md#rule-ot-02)). The supported semantic subset of [OT-03](../../requirements/products/arcslate.md#rule-ot-03): ordered video and audio tracks and stacks, clips, gaps, source ranges, timeline placement, rate-aware times, external and missing media references, names, markers, bounded namespaced metadata, straight cuts and explicitly mapped standard dissolves. Import staged before commit with a fidelity report the user reviews or cancels; import creating ArcSlate-owned canonical objects with provenance, never a mutable OTIO working store. Export binding a **committed** sequence revision, writing a temporary destination and publishing atomically. Item-level retained/approximated/omitted dispositions for everything outside the subset. Media relink for Offline Media. Bounded parsing with **no adapters, no Python plug-ins and no executable content**, behind an owned narrow C ABI.

**Testing requirements.** Test finite/nonfinite, standard 30000/1001 versus decimal 29.97, large/fractional values, metadata-stripped external files and exact/lossy export reports.  Real fixtures and the pinned official library exercising both directions; mixed and fractional frame rates proving **no silent frame shift**; gaps and stack ordering; repeated uses of one source retaining placement; missing references becoming relinkable Offline Media; supported dissolves and markers; unsupported features each producing an item-level disposition; malicious relative and absolute paths denied; malformed and oversized input rejected before commit; export cancellation leaving the project and any existing destination untouched; semantic round-trip compared on **timeline meaning and media references, not bytes or internal identifiers**; and a round-trip through external tooling that drops private ArcSlate metadata, proving core supported edits survive.

**Completion gate.** No hidden floating-point position arithmetic or silent fidelity claim exists.  **Both directions work against real fixtures and the pinned official library**, nothing is silently flattened or dropped, no frame shift occurs, and no adapter or plug-in loads. Merely opening JSON is insufficient ([OT-12](../../requirements/products/arcslate.md#rule-ot-12)).

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Sync scope mapping, relink state and collect records |
| Protocol | ArcSlate capabilities and context contracts |
| UI | Collect, relink, sync policy and AI context surfaces |
| Security | Media path handling; no path leakage through references |
| Platform | Large media handling and storage pressure per platform |
| Migration | Portable package and interchange versioning |
| Compatibility | Interchange claims backed by fixtures |

---

## 7. Tests and verification evidence

**Required evidence addition.** [WP-39.05](#rule-wp-39.05) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Capability descriptor, refusal and freeze-timing records | [WP-39.00](#rule-wp-39.00) |
| Structural media-exclusion and bounding results | [WP-39.01](#rule-wp-39.01) |
| Collect report, originals-untouched and round-trip results | [WP-39.02](#rule-wp-39.02) |
| Offline-open, relink and edit-decision preservation results | [WP-39.03](#rule-wp-39.03) |
| Sync exclusion, derived-data and convergence results | [WP-39.04](#rule-wp-39.04) |
| Per-format interchange round-trips and fidelity statements | [WP-39.05](#rule-wp-39.05) |

---

## 8. Completion gate

**[PG-20](../../assurance/open-gates-register.md#rule-pg-20) evidence:** [WP-39.05](#rule-wp-39.05) — Official OTIO double-boundary and explicit inexact-source conform evidence, combined with timeline/audio proof. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-15](../../assurance/open-gates-register.md#rule-pg-15) evidence:** [WP-39.05](#rule-wp-39.05) — Pinned official OTIO library exercises both directions, fractional/mixed rates, malicious input, fidelity and cancellation fixtures. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-03](../../assurance/open-gates-register.md#rule-pg-03) evidence:** [WP-39.05](#rule-wp-39.05) — Recorded OTIO substitute analysis and approved licence/provenance of the chosen bridge before use. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Every ArcSlate capability declares risk and approval posture with owner-side validation, and the contract was frozen **only after** timeline, command and undo semantics stabilised.
2. **Raw media structurally cannot enter an AI context payload**; oversized context is refused explicitly.
3. Collect never destroys originals, reports skipped items honestly, and the portable package round-trips with equivalence.
4. A project opens with all media offline and relinks without altering any edit decision.
5. Enabling sync never implicitly transfers heavyweight media; derived data never syncs as authority; big media never traverses the Hub; projects converge across devices.
6. Every claimed interchange version has a fixture, states its fidelity before writing, and never fabricates missing data — satisfying [PG-07](../../assurance/open-gates-register.md#rule-pg-07) for ArcSlate.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [25 — Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md)
- [38 — ArcSlate Render, Export and Colour Management](38-arcslate-render-and-colour.md)

**Downstream — these consume this package’s completed output.**

- [50 — Full-Platform Production Release](50-full-platform-production-release.md)
