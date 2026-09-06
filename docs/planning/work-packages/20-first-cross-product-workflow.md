# WP-20 — First Real Cross-Product Workflow

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: D — ArcNotes core
> Upstream: `17`, `19` · Downstream: `50`

> **Goal.** Close the first genuine ArcForges workflow end to end: ArcChat is asked to produce a report, ArcNotes creates the document and receives its content, the user approves, the result saves, undoes and recovers, and ArcChat receives an artifact reference. This is where ArcForges stops being a chat client with neighbours and becomes a platform.

---

## 1. Scope and purpose

**In scope.** The end-to-end workflow of `I2 §III.5`; ArcNotes as a context provider to ArcChat; ArcNotes artifact handlers; federated search across ArcChat and ArcNotes; real semantic modification through capabilities; and the closure of the corresponding V1B items declared in `WP-17.07`.

**Out of scope.** ArcScope and ArcSlate integration (`35`, `39`). Cloud placement of the workflow (`26`). Workflow blueprints as a contribution kind (`41`).

**Why this package exists.** `WP-17.07` deliberately declared ArcChat's ecosystem tier incomplete. This package closes the first three of those items with a real second product, proving the ecosystem model rather than asserting it.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| `I2 §III.5` | The exact scenario this package must demonstrate |
| [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md) `§16` | Handoff versus orchestration and the artifact model |
| [`../../requirements/06-knowledge-search-and-retrieval.md`](../../requirements/06-knowledge-search-and-retrieval.md) | Federated search, evidence and citation |
| `WP-17`, `WP-19` output | The ArcChat core and ArcNotes search and portability |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **ArcNotes owns every ArcNotes resource forever.** ArcChat never writes ArcNotes state directly; it invokes capabilities (`I4 §Stage 24 §14`). |
| BR-02 | **Owner-side validation refuses regardless of caller assertion**, including for the agent. |
| BR-03 | **Approval is required before content is written**, with the operation described in the user's terms — not as a raw capability name. |
| BR-04 | **The artifact returned to ArcChat is a reference**, never a document body (`WP-14.05`). |
| BR-05 | **Federated search is permission-aware per source**, and a refused source contributes nothing, including to counts. |
| BR-06 | **Context passed to a model is bounded and explicit**; a whole workspace is never handed over implicitly. |
| BR-07 | **A cross-product operation is a Task of the appropriate kind.** A user-initiated product operation is a **native Product Job** (`WP-16`); an agent-driven one is a **Cloud Agent Task** (`WP-52`). Both have a trace and a recovery story; **only the Agent Task has an AI budget** (`CM-04`, `I-121`). Conflating them would put a product operation under AI metering. |
| BR-08 | **The workflow must degrade honestly**: with ArcNotes absent, the capability is unavailable with a reason, and ArcChat continues to function. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.LocalRpc/` | Context provider and artifact handler registration |
| `src/ArcChat/ArcChat.Agent/` | Multi-step plans that span providers; artifact reference handling |
| `src/ArcChat/ArcChat.Application/` | Federated search aggregation and result attribution |
| `src/BuildingBlocks/ArcForges.Capabilities/` | Context provider aggregation and freezing across providers |
| `tests/EndToEndTests/` | The full workflow suite with degradation and recovery cases |

**Major types introduced.** `ContextContribution`, `FederatedSearchRequest`, `FederatedSearchResult`, `SourceAttribution`, `ArtifactHandlerRegistration`, `DocumentArtifactRef`, `SemanticEditCommand`.

---

## 5. Required implementation work

### WP-20.00 — ArcNotes as a context provider

**What must be fully done.** ArcNotes contributes typed context to ArcChat: the current document, a selection, a search result set, or an explicitly chosen set of documents. Context is bounded and its size is visible. The user always knows what is being shared before it is shared.

**Testing requirements.** Context contribution across each kind; a bounding test asserting oversized context is refused explicitly; a visibility test asserting the user sees what is shared.

**Completion gate.** Context contribution is typed, bounded, refused explicitly when oversized, and visible before sharing.

### WP-20.01 — Federated search

**What must be fully done.** One query fans out to ArcChat's and ArcNotes' local indexes, merges results with clear source attribution, and applies permission per source. A slow or absent source degrades the result set with a stated reason rather than failing the query.

**Testing requirements.** Merge and attribution tests; a per-source permission test including counts; an absent-source and slow-source degradation test.

**Completion gate.** Results carry source attribution, permission is applied per source, and an absent source degrades with a stated reason.

### WP-20.02 — Real semantic modification

**What must be fully done.** ArcChat requests a semantic change — create a document, append structured blocks, apply a specified edit — through ArcNotes capabilities. Each is idempotent under retry, produces one revision, and returns the resulting revision. ArcNotes validates every request against its own rules.

**Testing requirements.** Idempotency under retry and disconnection; owner-side rejection of a malformed or unauthorized request; a revision-return assertion.

**Completion gate.** Semantic modification is idempotent, owner-validated, and returns the resulting revision.

### WP-20.03 — The full workflow · **RELOCATED**

> **Relocated 2026-09-07 to [`52-cloud-harness.md`](52-cloud-harness.md) `§WP-52.05`.** The full agent-driven workflow requires the **Cloud Harness**, which admits through Commerce (`42`) and dispatches through Cloud AI (`43`). Neither exists in Phase D, so this step could not have run where it stood. The identifier is retired here and not reused.

**What remains in this package** is everything the workflow *calls*: the context provider (`WP-20.00`), federated search (`WP-20.01`), real semantic modification (`WP-20.02`) and artifact handlers (`WP-20.04`). Those are capability surfaces and are genuinely buildable in Phase D — they are exercised here by direct invocation, and by the Harness later.

### WP-20.04 — Artifact handlers

**What must be fully done.** ArcNotes registers an artifact handler for its document artifacts. ArcChat displays a thin preview and offers rich handoff to ArcNotes. The artifact reference resolves with permission re-checked at access, and reports honestly when the target has since changed or been deleted.

**Testing requirements.** Preview and handoff tests with the target running and not running; a stale-artifact test after deletion; a permission re-check test.

**Completion gate.** Artifacts preview, hand off and resolve correctly, and report staleness honestly.

### WP-20.05 — V1B closure record

**What must be fully done.** The V1B items closed by this package — federated search, ArcNotes context provider, real semantic modification, ArcNotes artifact handlers — are marked closed with their evidence. The remaining V1B items keep their named closing packages.

**Testing requirements.** A completeness check that closed items cite evidence and open items still name a package.

**Completion gate.** Closed V1B items cite evidence; remaining items still name their closing package.

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

| Evidence | Produced by |
|---|---|
| Context contribution, bounding and visibility results | `WP-20.00` |
| Federated search attribution, permission and degradation results | `WP-20.01` |
| Semantic modification idempotency and owner-validation results | `WP-20.02` |
| The full agent-driven scenario plus every failure variant | **`WP-52.05`** *(relocated)* |
| Preview, handoff, staleness and permission re-check results | `WP-20.04` |
| V1B closure record | `WP-20.05` |

---

## 8. Completion gate

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

**Upstream.** `17` (ArcChat V1A), `19` (ArcNotes search and portability).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `35`, `39` | The integration pattern ArcScope and ArcSlate follow |
| `40` — Knowledge | Federated search extended to retrieval and evidence |
| `50` — Production release | The proven cross-product workflow as a must-pass scenario |
