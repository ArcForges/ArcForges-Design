<a id="rule-wp-20"></a>

# WP-20 — First Real Cross-Product Workflow

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: D — ArcNotes core
> Upstream: `17`, `19` · Downstream: `50`, `52`

> **Goal.** Close the first genuine ArcForges workflow end to end: ArcChat is asked to produce a report, ArcNotes creates the document and receives its content, the user approves, the result saves, undoes and recovers, and ArcChat receives an artifact reference. This is where ArcForges stops being a chat client with neighbours and becomes a platform.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcChat + ArcNotes; version manifest. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Fixture AI is permitted only for the named local product slice; WP52 replaces it with real CF execution before Mobile/Web/full release.

---

## 1. Scope and purpose

**In scope.** The native capability portion of [the canonical workflow](../../assurance/end-to-end-workflow-verification.md#first-arcchat-arcnotes-workflow); ArcNotes as a context provider to ArcChat; ArcNotes artifact handlers; federated search across ArcChat and ArcNotes; real semantic modification through capabilities; and the closure of the corresponding V1B items declared in [WP-17.07](17-arcchat-independent-core.md#rule-wp-17.07).

**Out of scope.** ArcScope and ArcSlate integration (`35`, `39`). Cloud placement of the workflow (`26`). Workflow blueprints as a contribution kind (`41`).

**Why this package exists.** [WP-17.07](17-arcchat-independent-core.md#rule-wp-17.07) deliberately declared ArcChat's ecosystem tier incomplete. This package closes the first three of those items with a real second product, proving the ecosystem model rather than asserting it.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [First ArcChat–ArcNotes workflow acceptance](../../assurance/end-to-end-workflow-verification.md#first-arcchat-arcnotes-workflow) | The canonical scenario and failure outcomes; this package proves native capabilities, and the Cloud Harness package proves agent execution |
| [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md) `§16` | Handoff versus orchestration and the artifact model |
| [`../../requirements/06-knowledge-search-and-retrieval.md`](../../requirements/06-knowledge-search-and-retrieval.md) | Federated search, evidence and citation |
| [WP-17](17-arcchat-independent-core.md#rule-wp-17), [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19) output | The ArcChat core and ArcNotes search and portability |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **ArcNotes owns every ArcNotes resource forever.** ArcChat never writes ArcNotes state directly; it invokes capabilities. |
| <a id="rule-br-02"></a>BR-02 | **Owner-side validation refuses regardless of caller assertion**, including for the agent. |
| BR-03 | **Approval is required before content is written**, with the operation described in the user's terms — not as a raw capability name. |
| BR-04 | **The artifact returned to ArcChat is a reference**, never a document body ([WP-14.05](14-hub-and-minimal-provider-slice.md#rule-wp-14.05)). |
| BR-05 | **Federated search is permission-aware per source**, and a refused source contributes nothing, including to counts. |
| BR-06 | **Context passed to a model is bounded and explicit**; a whole workspace is never handed over implicitly. |
| BR-07 | **A cross-product operation is a Task of the appropriate kind.** A user-initiated product operation is a **native Product Job** ([WP-16](16-unified-execution-engine.md#rule-wp-16)); an agent-driven one is a **Cloud Agent Task** ([WP-52](52-cloud-harness.md#rule-wp-52)). Both have a trace and a recovery story; **only the Agent Task has an AI budget** ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121)). Conflating them would put a product operation under AI metering. |
| BR-08 | **The workflow must degrade honestly**: with ArcNotes absent, the capability is unavailable with a reason, and ArcChat continues to function. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.LocalRpc/` | Context provider and artifact handler registration |
| `src/ArcChat/ArcChat.Agent/` | Presentation and ArtifactRef handoff for Cloud-owned multi-step plans; the Harness implements orchestration in [WP-52](52-cloud-harness.md#rule-wp-52) |
| `src/ArcChat/ArcChat.Application/` | Federated search aggregation and result attribution |
| `src/BuildingBlocks/ArcForges.Capabilities/` | Context provider aggregation and freezing across providers |
| `tests/EndToEndTests/` | The full workflow suite with degradation and recovery cases |

**Major types introduced.** `ContextContribution`, `FederatedSearchRequest`, `FederatedSearchResult`, `SourceAttribution`, `ArtifactHandlerRegistration`, `DocumentArtifactRef`, `SemanticEditCommand`.

---

## 5. Required implementation work

<a id="rule-wp-20.00"></a>

### WP-20.00 — ArcNotes as a context provider

**What must be fully done.** ArcNotes contributes typed context to ArcChat: the current document, a selection, a search result set, or an explicitly chosen set of documents. Context is bounded and its size is visible. The user always knows what is being shared before it is shared.

**Testing requirements.** Context contribution across each kind; a bounding test asserting oversized context is refused explicitly; a visibility test asserting the user sees what is shared.

**Completion gate.** Context contribution is typed, bounded, refused explicitly when oversized, and visible before sharing.

<a id="rule-wp-20.01"></a>

### WP-20.01 — Federated search

**What must be fully done.** One query fans out to ArcChat's and ArcNotes' local indexes, merges results with clear source attribution, and applies permission per source. A slow or absent source degrades the result set with a stated reason rather than failing the query.

**Testing requirements.** Merge and attribution tests; a per-source permission test including counts; an absent-source and slow-source degradation test.

**Completion gate.** Results carry source attribution, permission is applied per source, and an absent source degrades with a stated reason.

<a id="rule-wp-20.02"></a>

### WP-20.02 — Real semantic modification

**What must be fully done.** ArcChat requests a semantic change — create a document, append structured blocks, apply a specified edit — through ArcNotes capabilities. Each is idempotent under retry, produces one revision, and returns the resulting revision. ArcNotes validates every request against its own rules.

**Testing requirements.** Idempotency under retry and disconnection; owner-side rejection of a malformed or unauthorized request; a revision-return assertion.

**Completion gate.** Semantic modification is idempotent, owner-validated, and returns the resulting revision.

<a id="rule-wp-20.03"></a>

### WP-20.03 — The full workflow · **RELOCATED**

> **Relocated 2026-09-07 to [`52-cloud-harness.md`](52-cloud-harness.md) `§[WP-52.05](52-cloud-harness.md#rule-wp-52.05)`.** The full agent-driven workflow requires the **Cloud Harness**, which admits through Commerce (`42`) and dispatches through Cloud AI (`43`). Neither exists in Phase D, so this step could not have run where it stood. The identifier is retired here and not reused.

**What remains in this package** is everything the workflow *calls*: the context provider ([WP-20.00](#rule-wp-20.00)), federated search ([WP-20.01](#rule-wp-20.01)), real semantic modification ([WP-20.02](#rule-wp-20.02)) and artifact handlers ([WP-20.04](#rule-wp-20.04)). Those are capability surfaces and are genuinely buildable in Phase D — they are exercised here by direct invocation, and by the Harness later.

<a id="rule-wp-20.04"></a>

### WP-20.04 — Artifact handlers

**Required design implementation and verification.** A generated report copied into Notes creates a Notes-owned document with new owner identity and inherited origin kinds/selected lineage. Verify ArtifactRef integrity, manual edit propagation and absence of private source/workspace IDs in exported origin; the Cloud Harness remains the plan owner.

**What must be fully done.** ArcNotes registers an artifact handler for its document artifacts. ArcChat displays a thin preview and offers rich handoff to ArcNotes. The artifact reference resolves with permission re-checked at access, and reports honestly when the target has since changed or been deleted.

**Testing requirements.** Preview and handoff tests with the target running and not running; a stale-artifact test after deletion; a permission re-check test.

**Completion gate.** Artifacts preview, hand off and resolve correctly, and report staleness honestly.

<a id="rule-wp-20.05"></a>

### WP-20.05 — V1B closure record

**What must be fully done.** The V1B items closed by this package — federated search, ArcNotes context provider, real semantic modification, ArcNotes artifact handlers — are marked closed with their evidence. The remaining V1B items keep their named closing packages.

**Testing requirements.** A completeness check that closed items cite evidence and open items still name a package.

**Completion gate.** Closed V1B items cite evidence; remaining items still name their closing package.

---

<a id="rule-wp-20.90"></a>
### WP-20.90 — Verify the owned artifact and real integration

**What must be fully done.** Preserve the first real local typed capability workflow. Name exact released/candidate app and contract versions, retained fixture AI scope and the real AI replacement at WP-52.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Real two-product ownership/revision/error behavior; fixture tests do not imply model/Cloud/usage integration has passed.

**Completion gate.** Real two-product ownership/revision/error behavior; fixture tests do not imply model/Cloud/usage integration has passed. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Cross-product task state and artifact references become durable |
| Protocol | Context, federated search and artifact contracts become live |
| UI | Approval in a real workflow, thin preview, handoff and merged search |
| Security | Owner-side validation, bounded context and permission-aware federation proven together |
| Platform | The workflow is verified on every desktop platform |
| Migration | Artifact reference format enters the compatibility window |
| Compatibility | The first multi-product contract set that must version together |

---

## 7. Tests and verification evidence

**Required evidence addition.** [WP-20.04](#rule-wp-20.04) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Context contribution, bounding and visibility results | [WP-20.00](#rule-wp-20.00) |
| Federated search attribution, permission and degradation results | [WP-20.01](#rule-wp-20.01) |
| Semantic modification idempotency and owner-validation results | [WP-20.02](#rule-wp-20.02) |
| The full agent-driven scenario plus every failure variant | **[WP-52.05](52-cloud-harness.md#rule-wp-52.05)** *(relocated)* |
| Preview, handoff, staleness and permission re-check results | [WP-20.04](#rule-wp-20.04) |
| V1B closure record | [WP-20.05](#rule-wp-20.05) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-20.90](#rule-wp-20.90) and all inherited domain-specific gates must pass on the same candidate closure. Real two-product ownership/revision/error behavior; fixture tests do not imply model/Cloud/usage integration has passed.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Context contribution is typed, bounded, explicitly refused when oversized, and visible to the user before sharing.
2. Federated search attributes results per source, applies permission per source including counts, and degrades with a stated reason when a source is absent or slow.
3. Semantic modification is idempotent under retry and disconnection, owner-validated, and returns the resulting revision.
4. **Every capability the workflow needs is exercised by direct invocation** — document creation, block insertion, approval, write, undo, save, kill, recovery, artifact reference resolution — and every failure variant produces a correct, explained outcome.
5. Artifacts preview and hand off correctly whether or not the target is running, and report staleness honestly.
6. With ArcNotes absent, the capability is unavailable with a reason and ArcChat continues to function.
7. Closed V1B items cite evidence; remaining V1B items still name their closing package.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-17](17-arcchat-independent-core.md#rule-wp-17)
- [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19)

**Downstream — consumers of these released outputs.**

- [WP-50](50-full-platform-production-release.md#rule-wp-50)
- [WP-52](52-cloud-harness.md#rule-wp-52)


---
