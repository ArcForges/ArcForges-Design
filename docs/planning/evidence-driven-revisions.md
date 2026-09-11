# Evidence-Driven Revisions

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** (the plan is derived after the prerequisite evidence), [P2-004](../decisions/phase-2-specification-decisions.md#rule-p2-004)
> Companions: [`implementation-sequence.md`](implementation-sequence.md), [`work-packages/README.md`](work-packages/README.md), [`../assurance/reference-coverage/README.md`](../assurance/reference-coverage/README.md), [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md)

The prerequisite evidence **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** requires was produced, and then the plan was re-derived from it. This document records every change the evidence caused, in the form the repair requires: the evidence, the affected statement, the correction, the downstream consumers, and the verification that confirms it.

**A change appears here only if evidence caused it.** Documents the evidence did not touch were not reorganised.

**Historical evidence boundary.** Revision entries describe the evidence and counts at their recorded baseline. The completed input extraction in the invariant revisions is not an ongoing source-reading or reconciliation task. Current implementation consumes the [normative catalogue and its mappings](../assurance/invariant-coverage.md) and the [effective work-package sequence](work-packages/README.md); historical input accounting neither defines the current audit denominator nor overrides those definitions. Existing supersession notes continue to determine which recorded corrections are effective.

---

## 1. Revisions caused by the reference matrices

<a id="rule-r-01"></a>

### R-01 — No reuse is possible from any reference

| Field | Content |
|---|---|
| **Evidence** | [`../assurance/reference-coverage/README.md`](../assurance/reference-coverage/README.md) `§Aggregate licence position`. Of six accessible references: AionUi Apache-2.0; AFFiNE **split** MIT / proprietary Enterprise Edition; SiYuan AGPL-3.0; Serial-Studio **dual GPL-3.0-only / commercial with named excluded modules**; ArcVideo and ArcVideoFoundation GPL-3.0-only |
| **Affected statement** | The provenance document's framing implied that per-product licence audits might clear material for reuse, making `Copy`, `Rewrite` or `Improve` dispositions plausible outcomes |
| **Correction** | **No matrix row proposes reuse.** All 145 non-excluded rows are `Reference Only`. Every product is an original implementation informed by behavioural evidence. Recorded as the aggregate position in the matrix set README |
| **Downstream consumers** | [WP-15](work-packages/15-arcchat-conversation-core.md#rule-wp-15), [WP-18](work-packages/18-arcnotes-document-core.md#rule-wp-18), [WP-33](work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33), [WP-36](work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) — each package's first binding rule now states the matrix is a consumed input with no reuse authorised; [WP-00.03](work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03)'s provenance process remains, but has no pending subject |
| **Verification** | The completeness check in each matrix asserts *"any row proposing reuse carries a provenance obligation"* and records **Not applicable — no row proposes reuse** |

### R-02 — AFFiNE's server subtree is proprietary

| Field | Content |
|---|---|
| **Evidence** | [`arcnotes-affine-siyuan.md`](../assurance/reference-coverage/arcnotes-affine-siyuan.md) `§2.1`. The root `LICENSE` delegates `packages/backend/**` and `packages/common/native/**` to `packages/backend/server/LICENSE`, which opens *"The AFFiNE Enterprise Edition (EE) license"* |
| **Affected statement** | A repository-root reading would have concluded "MIT" for the whole repository |
| **Correction** | Those two subtrees are **permanently ineligible** for reuse and were deliberately **not read beyond their licence file**, to avoid contamination with no offsetting benefit. Rows [AN-18](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-18) and [AN-19](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-19) record it |
| **Downstream consumers** | [WP-18](work-packages/18-arcnotes-document-core.md#rule-wp-18), [WP-25](work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) — sync-shape evidence comes only from the MIT `packages/common/{nbstore,realtime,s3-compat}`, not from the server |
| **Verification** | [MT-02](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-mt-02) of that matrix requires the licence split to be re-verified on every drift check, because a subtree licence can change upstream |

### R-03 — ArcNotes slides have no reference evidence

| Field | Content |
|---|---|
| **Evidence** | [`arcnotes-affine-siyuan.md`](../assurance/reference-coverage/arcnotes-affine-siyuan.md) `F-AN-2`. Neither AFFiNE nor SiYuan implements a presentation mode |
| **Affected statement** | [WP-29](work-packages/29-arcnotes-slides.md#rule-wp-29) was written assuming reference oracles comparable to its sibling packages [WP-27](work-packages/27-arcnotes-edgeless-canvas.md#rule-wp-27) and [WP-28](work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) |
| **Correction** | Historical first-party slides-oracle requirement superseded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): slides are excluded and the package is retired, with no future hook. The reference observation is preserved. |
| **Downstream consumers** | Current Notes core/property packages implement the amended notebook scope. No live slides-oracle work or slides-parity claim is assigned to release. |
| **Verification** | The completeness check in that matrix records **[D-006](../decisions/phase-1-foundation-decisions.md#rule-d-006)** phase coverage explicitly, naming slides as an absence |

### R-04 — Serial-Studio creates an authorship boundary

| Field | Content |
|---|---|
| **Evidence** | [`arcscope-serial-studio.md`](../assurance/reference-coverage/arcscope-serial-studio.md) `§2`. `LICENSE.md` §4 excludes MQTT, XY plotting, 3D visualisation and the activation system from GPL and reserves them commercially, stating that source visibility *"does not confer any right to use, modify, compile, or distribute"* |
| **Affected statement** | The plan treated the whole reference as readable behavioural evidence |
| **Correction** | Three capability areas were **deliberately not read**. Rows [AS-03](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-03), [AS-14](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-14) and [AS-27](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-27) are accepted exclusions on licence grounds, with the non-reading recorded so a later reader does not mistake it for incomplete review |
| **Downstream consumers** | [WP-33](work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33), [WP-34](work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) — no ArcScope capability may derive from those modules' expression |
| **Verification** | [MT-02](../assurance/reference-coverage/arcscope-serial-studio.md#rule-mt-02) of that matrix requires the §4 Pro-module list to be re-read on every drift check, because a feature can move into or out of it |

### R-05 — ArcVideoFoundation is not a reusable core

| Field | Content |
|---|---|
| **Evidence** | [`arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md) [AL-30](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-30). The complete tree is **10 source files and 17 headers** — rational, timecode, timerange, bezier, colour, math, string, value, log, sample buffer, audio params, pixel format. Its README describes a *"fat core"*; the tree is a thin utility layer with no timeline, media, render-graph or project model |
| **Affected statement** | Any planning assumption that a substantial reusable core existed for ArcSlate |
| **Correction** | Recorded as an evidence-versus-claim finding. [WP-36](work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) and [WP-37](work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) plan original implementations, which the evidence now shows is necessary rather than merely chosen |
| **Downstream consumers** | [WP-36](work-packages/36-arcslate-project-and-timeline.md#rule-wp-36), [WP-37](work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) |
| **Verification** | [MT-02](../assurance/reference-coverage/arcslate-arcvideo.md#rule-mt-02) of that matrix re-checks [AL-30](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-30) on drift: if the Foundation grows into the core its README describes, the assumption changes |

### R-06 — ArcSlate's reference baseline narrowed to the two actual repositories

| Field | Content |
|---|---|
| **Evidence** | [`arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md) `§2`. No Olive repository existed at the authorized reference-map location. ArcVideo's `README.md` (lines 12, 20, 98) documents it as a fork of Olive, and it is the buildable codebase |
| **Affected statement** | **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**'s reference map listed Olive as a third ArcSlate reference; the plan assumed all three were available |
| **Correction** | **User decision [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005), 2026-09-05**: ArcSlate's direct references are **ArcVideo and ArcVideoFoundation**; no Olive repository is to be obtained or independently reviewed. Olive could not be built in the user's environment and ArcVideo carries the modifications that made it build. **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** is amended by dated record; the Olive-direct audit scope and the missing-repository blocker are removed; [OC-01](../assurance/open-gates-register.md#rule-oc-01) is closed |
| **What was deliberately not removed** | **Olive-origin provenance.** ArcVideo's GPL-3.0 obligations, upstream copyright and attribution to the Olive authors are retained wherever inherited material requires them (`§3.1` of that matrix; [LP-02](../assurance/reference-coverage/arcslate-arcvideo.md#rule-lp-02)). Matrix rows previously labelled *(Olive-derived)* now read *(upstream-derived)* — an attribution note about ArcVideo's own tree, not a claim about an Olive repository |
| **Downstream consumers** | [WP-36](work-packages/36-arcslate-project-and-timeline.md#rule-wp-36)–[WP-39](work-packages/39-arcslate-integration-and-portability.md#rule-wp-39); [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md) `§1.1`, `§2.2`, `§7`; [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md) `§1`; [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md) `§9` |
| **Verification** | The matrix completeness check now records **0 unresolved determinations**; the gates register records [OC-01](../assurance/open-gates-register.md#rule-oc-01) closed; no document claims Olive coverage or requires an Olive checkout |

### R-07 — Native NOTICE obligation extends to native assets

| Field | Content |
|---|---|
| **Evidence** | [`distribution-startarcforges.md`](../assurance/reference-coverage/distribution-startarcforges.md) [SD-06](../assurance/reference-coverage/distribution-startarcforges.md#rule-sd-06). The native reference product bundles OpenColorIO, OpenEXR, OpenImageIO, Imath, Iex and IlmThread DLLs with **no aggregated notice file**, while the Electron products all ship runtime notices |
| **Affected statement** | [WP-50.01](work-packages/50-full-platform-production-release.md#rule-wp-50.01)'s NOTICE verification was scoped implicitly to managed packages |
| **Correction** | **[WP-50.01](work-packages/50-full-platform-production-release.md#rule-wp-50.01) explicitly covers native assets.** ArcSlate and ArcScope will bundle the same dependency classes |
| **Downstream consumers** | [WP-50.01](work-packages/50-full-platform-production-release.md#rule-wp-50.01), and [PG-03](../assurance/open-gates-register.md#rule-pg-03)'s per-product native licence review |
| **Verification** | [SP-09](../architecture/14-build-packaging-and-release.md#rule-sp-09) of the build architecture already requires native assets to carry the same signing, SBOM and provenance rules; this makes the NOTICE half explicit at the gate |

<a id="rule-r-08"></a>

### R-08 — The crash handler is a signed release artifact

| Field | Content |
|---|---|
| **Evidence** | [`distribution-startarcforges.md`](../assurance/reference-coverage/distribution-startarcforges.md) [SD-07](../assurance/reference-coverage/distribution-startarcforges.md#rule-sd-07). The native reference ships `crashpad_handler.exe` and `arcvideo-crashhandler.exe` as separate processes |
| **Affected statement** | [WP-50.02](work-packages/50-full-platform-production-release.md#rule-wp-50.02)'s packaging matrix treated crash handling as an implementation detail |
| **Correction** | The crash handler is its own signed, versioned artifact in the packaging matrix |
| **Downstream consumers** | [WP-50.02](work-packages/50-full-platform-production-release.md#rule-wp-50.02), [WP-12.05](work-packages/12-observability-foundation.md#rule-wp-12.05) |
| **Verification** | The release matrix enumerates signed artifacts; the crash handler appears in it |

---

## 2. Revisions caused by the implementation-state reconciliation

<a id="rule-r-09"></a>

### R-09 — The repository is a skeleton, not a partial implementation

| Field | Content |
|---|---|
| **Evidence** | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) `§1.2`, `§3` [C-01](../assurance/implementation-state-reconciliation.md#rule-c-01), [C-02](../assurance/implementation-state-reconciliation.md#rule-c-02). **166 projects** (not 332 — the earlier count double-counted a nested worktree) and **8,638 C# lines total**, with **151 of 166** projects at or under 60 lines |
| **Affected statement** | The earlier inventory described per-area alignment as "Close", which read as substance |
| **Correction** | Alignment is **structural only**. The directory shape is a genuine asset; the behaviour does not exist. Every package's scope assumes a scaffold, not a partial implementation |
| **Downstream consumers** | Every package that touches `src/`; principally [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01), [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02), [WP-05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-21](work-packages/21-cloud-host-and-persistence.md#rule-wp-21) |
| **Verification** | The item-level table in `§4` of that document lists all 166 projects with measured content, so the claim is checkable rather than asserted |

### R-10 — Three licence-boundary defects, not pending work

| Field | Content |
|---|---|
| **Evidence** | There, `§5.1`. **All 273 `.cs` files declare `AGPL-3.0-only`**, including `src/Mobile/**` (15 files), `src/SDK/**` (4) and `src/Contracts/**` (36) — three subtrees Phase 1 requires to be Apache-2.0 (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) |
| **Affected statement** | [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01) framed the licence boundary as work not yet done |
| **Correction** | It is a **declared-wrong condition**. [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01)'s goal statement and `§1` now say so, and it is priority 1 |
| **Downstream consumers** | [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01), [WP-03](work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-30](work-packages/30-mobile-shared-architecture.md#rule-wp-30), [WP-32](work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) — **[F-023](../assurance/open-gates-register.md#rule-f-023)** cannot pass while mobile files declare AGPL |
| **Verification** | [WP-05.01](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01)'s licence-boundary tests, with a negative fixture; and the [F-023](../assurance/open-gates-register.md#rule-f-023) dependency-closure audit in [WP-32.02](work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.02) |

### R-11 — Four false conformance findings withdrawn

| Field | Content |
|---|---|
| **Evidence** | There, `§3` [C-03](../assurance/implementation-state-reconciliation.md#rule-c-03)–[C-06](../assurance/implementation-state-reconciliation.md#rule-c-06). `IsAotCompatible` **is** set, centrally in `eng/build/desktop-aot.props` and `contracts.props`; **165 `packages.lock.json`** exist; `RepositoryPolicyTests.cs` **exists** with 19 test methods; SPDX **is** declared in all 273 source files |
| **Affected statement** | [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) and [WP-05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) were scoped as if these were absent |
| **Correction** | **[WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) is narrower**: the Web posture file, the library `IsAotCompatible` sweep outside the two central imports, effective-property assertion, and version-axis plumbing. **[WP-05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) is narrower**: a working harness of 2,075 lines with a project-graph loader and a negative-fixture compiler already exists; the package reconciles 13 existing rules against the accepted 24 |
| **Downstream consumers** | [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02), [WP-05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), and every gate that depends on them |
| **Verification** | `§5.3` and `§5.4` of the reconciliation document record the effective configuration and the measured harness, both re-checkable |

### R-12 — Native shims are ABI skeletons, and two are fenced

| Field | Content |
|---|---|
| **Evidence** | There, `§5.2`. Each of the six shims contains **2–3 files, 28–120 lines**, exposing only the version / build-info / last-error triple. Total across all six plus shared: ~514 lines |
| **Affected statement** | The earlier framing — "a broader native surface than the architecture illustrates" — implied six implemented surfaces |
| **Correction** | They are six **named placeholders** sharing one ABI convention. Four are `Keep`; **two are `Fence`** pending substitute analyses: `arcslate-otio-abi` and `arcscope-mdf-abi`, where a managed substitute is plausible and the native architecture permits native code only where none exists |
| **Downstream consumers** | [WP-01.03](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.03) (fencing), [WP-35.04](work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04) and [WP-39.05](work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) (the substitute analyses), [WP-37.00](work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.00) (the shims that stay) |
| **Verification** | [WP-01.03](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.03)'s gate asserts the two fenced shims are unreferenceable and their analyses are scheduled against named sub-steps |

### R-13 — Preserve the single Cloud Host

| Field | Content |
|---|---|
| **Evidence** | There, `§5.5`. `src/Cloud` holds `Host`, `AppHost`, `BackgroundJobs`, `Infrastructure`, `Migrations`, `PublicApi`, `Realtime`, `ServiceDefaults` — **no `Worker`, no `TaskRunner`** |
| **Affected statement** | Not identified at all in the earlier inventory |
| **Correction** | The earlier split recommendation is withdrawn: the accepted topology is one Host containing bounded internal services and the Harness. Keep BackgroundJobs/AgentRuntime as libraries and AppHost for local development only. |
| **Downstream consumers** | [WP-21](work-packages/21-cloud-host-and-persistence.md#rule-wp-21) and every Cloud package consume the same single-Host composition. |
| **Verification** | [WP-21.01](work-packages/21-cloud-host-and-persistence.md#rule-wp-21.01) asserts identical replicas, all bounded hosted services in one deployable Host, no role flag/configuration leader, and lease/fencing coordination. |

<a id="rule-r-14"></a>

### R-14 — Priority order revised

| Field | Content |
|---|---|
| **Evidence** | There, `§6`, with a *changed by this evidence?* column |
| **Affected statement** | The earlier eight-item priority order |
| **Correction** | Licence correction **raised** to a defect; cloud role separation **added** at 3; native shim work **narrowed** from six shims to two questions; build governance and architecture-rule work **lowered** because most already conforms |
| **Downstream consumers** | The order in which [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01), [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02), [WP-05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) and [WP-21](work-packages/21-cloud-host-and-persistence.md#rule-wp-21) execute their sub-steps |
| **Verification** | Each affected package's sub-step ordering reflects it |

---

## 3. Revisions caused by the invariant accounting

<a id="rule-r-15"></a>

### R-15 — The catalogue is a counted set of rows, not "approximately 490"

> **Superseded figure.** This revision established **421** against the pre-P2-006 catalogue. [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) later added [I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)–[I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498), so **the current count is 429** ([PR-03](../assurance/invariant-coverage.md#rule-pr-03) of the coverage document). The finding below is retained as the record of *why* the count is counted rather than inferred from the highest identifier; **421 is not a current figure and is not a gate threshold**.

| Field | Content |
|---|---|
| **Evidence** | [`../assurance/invariant-coverage.md`](../assurance/invariant-coverage.md) `§1`, `§2`. 589 raw corpus lines → 484 unique statements → **421 catalogue rows**, with identifiers reaching [I-490](../requirements/01-normative-glossary-and-invariants.md#rule-i-490) because each section reserves headroom |
| **Affected statement** | Every document stating "roughly 490 invariants" read the highest identifier as a count |
| **Correction** | The count is 421. The 72 identifier gaps are **deliberate per-section reserved headroom**, evidenced by a table showing each section's last used identifier and its reserved range |
| **Downstream consumers** | [WP-00.01](work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01), [WP-05.05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05), [`../assurance/traceability-matrix.md`](../assurance/traceability-matrix.md) |
| **Verification** | The completeness check in `§5` of that document accounts for all 484 corpus statements |

### R-16 — Four invariants were missing and are now catalogued

| Field | Content |
|---|---|
| **Evidence** | There, `§3.3`. Present in the corpus, absent from the catalogue |
| **Affected statement** | The catalogue's completeness |
| **Correction** | Added in their sections' reserved ranges: [I-077](../requirements/01-normative-glossary-and-invariants.md#rule-i-077) ArtifactRef ≠ Permission Token; [I-224](../requirements/01-normative-glossary-and-invariants.md#rule-i-224) Project Reference ≠ Resource Copy; [I-405](../requirements/01-normative-glossary-and-invariants.md#rule-i-405) Push Notification ≠ Durable Attention State; [I-490](../requirements/01-normative-glossary-and-invariants.md#rule-i-490) ArcSlate Sequence ≠ Timeline Clip |
| **Downstream consumers** | [WP-00.01](work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01)'s export; the owning packages named in the coverage mapping |
| **Verification** | Re-running the accounting after the additions reduced unaccounted statements to five, each then individually confirmed as a phrasing variant of a catalogued row |

<a id="rule-r-17"></a>

### R-17 — [PG-06](../assurance/open-gates-register.md#rule-pg-06) split into a design gate and an implementation gate

| Field | Content |
|---|---|
| **Evidence** | [PG-06](../assurance/open-gates-register.md#rule-pg-06) required coverage; [WP-05.05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05) permitted an owned open finding to satisfy it. **Two different completion standards for one gate** |
| **Affected statement** | [PG-06](../assurance/open-gates-register.md#rule-pg-06), [WP-00.01](work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01), [WP-05.05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05), and the traceability matrix's invariant section |
| **Correction** | **[PG-06](../assurance/open-gates-register.md#rule-pg-06)** is now design-stage traceability — architecture home, mechanism, planned verification, owning gate — **closed** by the coverage document. **[PG-11](../assurance/open-gates-register.md#rule-pg-11)** is new: implementation-stage enforcement, requiring an implemented check with a passing result, discharged per invariant by its owning package. [WP-05.05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05) owns **accounting**, and its gate states explicitly that it closes neither |
| **Downstream consumers** | Every owning package named in the coverage mapping; [P-03](../assurance/release-gates.md#rule-p-03) for each product |
| **Verification** | [RS-03](../assurance/open-gates-register.md#rule-rs-03) of the open-gates register states that [PG-06](../assurance/open-gates-register.md#rule-pg-06) closing has no effect on [PG-11](../assurance/open-gates-register.md#rule-pg-11); [WP-05.05](work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05) carries a table of what its gate explicitly does not do |

---

## 4. What did not change, and why

| Area | Why the evidence did not change it |
|---|---|
| The 51-package count | No evidence item created or removed a package. Scope moved within packages; the dependency structure held |
| The dependency order | Every upstream relationship the evidence touched was already correct. [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01) before [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) before [WP-03](work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) is exactly what the licence-boundary defect requires |
| The requirements layer | The matrices produced **no new requirement**. Reference capability is not requirement ([RC-02](../assurance/reference-coverage/README.md#rule-rc-02) of the matrix set) |
| The architecture layer | Every reference finding either confirmed an existing rule or recorded a deliberate divergence. None contradicted a rule |
| Documents outside the evidence's reach | Not reorganised. A change without a dependency-based reason is churn |

---

## 5. Verification of this repair's own revisions

| Revision | Verification | Result |
|---|---|---|
| [R-01](#rule-r-01) – [R-08](#rule-r-08) | Each matrix's completeness check, run per matrix | 145 rows, 0 unresolved except [OC-01](../assurance/open-gates-register.md#rule-oc-01) |
| [R-09](#rule-r-09) – [R-14](#rule-r-14) | The reconciliation completeness check | 166 of 166 projects; 6 of 6 shims; 6 corrections recorded |
| [R-15](#rule-r-15) – [R-17](#rule-r-17) | The invariant accounting re-run after the additions | 484 of 484 statements accounted for; 421 of 421 mapped **at that revision** — superseded, see the banner on [R-15](#rule-r-15); the current figure is **429 of 429** |
| All | Link and identifier integrity across `docs/` | Reported in the closure summary |

| # | Rule |
|---|---|
| EV-01 | **A future evidence-driven change is added here** with the same five fields. |
| EV-02 | **A change with no evidence does not belong in this document** — and, absent a dependency-based reason, does not belong in the plan either. |


## React/TypeScript Web redesign — user decision

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) replaces Web Blazor and the C# static generator with React/TypeScript on Node/npm. The ReactApp2 template was inspected for esproj/Vite integration only. The C# → OpenAPI → TS SDK preserves contract authority and adds exact-value cross-language tests. [P2-003](../decisions/phase-2-specification-decisions.md#rule-p2-003) now selects same-origin opaque-cookie sessions in the existing Cloud host. [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) now precedes [WP-47](work-packages/47-static-public-site.md#rule-wp-47), and both index directions are amended; [WP-22.08](work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) supplies browser sessions before generated-client integration, [WP-47.07](work-packages/47-static-public-site.md#rule-wp-47.07) supplies the shared consumer design system, and [WP-50.06](work-packages/50-full-platform-production-release.md#rule-wp-50.06) aggregates real production-browser/rollback evidence. All earlier code observations remain baseline evidence, not proof of the new UI.
