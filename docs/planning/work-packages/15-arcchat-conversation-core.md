<a id="rule-wp-15"></a>

# WP-15 — ArcChat Conversation and Project Core

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `14` · Downstream: `17`, `52`

> **Goal.** Build ArcChat's own domain — conversation, message, branch, attachment, project, profile and skill — as durable local state with search, history and recovery, independent of any other product.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcChat. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The conversation domain model and its persistence; message composition, streaming assembly and branching; attachments; projects and profiles; skills as declarative guidance; local search over conversation content; and conversation history, export and recovery.

**Out of scope.** Task execution (`16`). Ecosystem capabilities that depend on other products (`20`). Cloud sync (`25`). Managed AI economics (`43`) — providers are adapter-shaped and may be stubbed here.

**Why this package exists.** [the product scope](../../requirements/00-product-scope-and-portfolio.md#3-product-independence-requirements) requires ArcChat to be completed **without dependencies on other products** first. An ArcChat that only works when ArcNotes is running is not an independent product.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md) | The full ArcChat product model, V1 scope and acceptance scenarios |
| [`../../assurance/reference-coverage/arcchat-aionui.md`](../../assurance/reference-coverage/arcchat-aionui.md) | **The completed ArcChat Reference Coverage Matrix** — 30 rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, oracle and owner |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix method and the ten-field provenance record that governs any future reuse |
| [`../../architecture/04-desktop-application-architecture.md`](../../architecture/04-desktop-application-architecture.md) | Host structure, MVVM, threading and persistence |
| [WP-07](07-local-persistence-foundation.md#rule-wp-07) output | The local store, journal and recovery |
| [WP-14](14-hub-and-minimal-provider-slice.md#rule-wp-14) output | The Hub and a working provider |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcChat Reference Coverage Matrix is a completed, versioned planning input** — [`../../assurance/reference-coverage/arcchat-aionui.md`](../../assurance/reference-coverage/arcchat-aionui.md), 30 item-level rows, bound to AionUi at `29c9271a5`. It was produced before this plan was derived (**[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)**). **This package consumes it and checks it for drift; it does not create it.** |
| BR-02 | **ArcChat is fully usable with every other product absent.** |
| BR-03 | **`Conversation ≠ Project` and `Project ≠ Workspace`.** Three distinct containers with distinct ownership. |
| BR-04 | **A skill is declarative guidance and never code**, and **a skill confers no capability**. |
| BR-05 | **A branch is a first-class structure**, not a hidden copy; branching never mutates the original. |
| BR-06 | **Streaming assembly is a presentation concern.** The durable message is written once, complete; a partial stream is never the stored fact. |
| BR-07 | **An attachment is either managed or referenced**, and the distinction is explicit and visible. |
| BR-08 | **Search over cached conversation content is a first-class capability**, available during a Cloud outage. Chat is Cloud-authoritative ([CW-02](../../architecture/data-model/00-data-model-overview.md#rule-cw-02)), so this searches the working cache and unsent drafts; workspace-wide search is `search.query` on the public surface, and neither is presented as the other. |
| BR-09 | **A provider adapter is an interface**; the real provider integration lands in `43`. |
| BR-10 | **Hidden reasoning from a model never enters the product model**. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Domain/` | Conversation, message, branch, attachment, project, profile, skill |
| `src/ArcChat/ArcChat.Application/` | Application services for every operation, shared by UI and RPC |
| `src/ArcChat/ArcChat.Infrastructure/` | Store schema, search index, attachment storage, provider adapter interfaces |
| `src/ArcChat/ArcChat.Presentation/` | View models for conversation, project, profile and skill surfaces |
| `src/ArcChat/ArcChat.Desktop/` | The real ArcChat shell surfaces |
| `fixtures/formats/arcchat/` | The first ArcChat export fixtures |
| `tests/ArcChat.Tests.*` | Domain, application, store, search and recovery suites |

**Major types introduced.** `Conversation`, `Message`, `MessagePart`, `Branch`, `Attachment`, `AttachmentKind`, `Project`, `AgentProfile`, `Skill`, `SkillVersion`, `ConversationSearchIndex`, `ConversationExport`.

---

## 5. Required implementation work

<a id="rule-wp-15.00"></a>

### WP-15.00 — Conversation and message model

**Required design implementation and verification.** Persist origin per message part with the immutable payload; branching/copy retains kind union and new payload versions receive new records. Test model text and unknown imported text, provisional stream headers and final hash binding. The export client verifies the manifest/sidecar from the acknowledged snapshot.

**What must be fully done.** Conversations own ordered messages composed of typed parts. Messages are immutable once committed; an edit produces a new revision with the prior one retained. Streaming produces a durable message exactly once at completion, with interruption handled explicitly rather than storing a truncated fragment as fact.

**Testing requirements.** Immutability and revision tests; a stream-interruption test asserting no partial message is stored as complete; large-conversation performance against the scale corpus.

**Completion gate.** A committed message is immutable, an interrupted stream never produces a message claiming to be complete, and large conversations meet the responsiveness budget.

<a id="rule-wp-15.01"></a>

### WP-15.01 — Branching

**What must be fully done.** Branching from any message produces an independent continuation sharing prior history by reference, never by copy. Branch navigation, comparison and deletion are supported. Deleting a branch never affects its parent.

**Testing requirements.** Branch independence, shared-history integrity and deletion-isolation tests.

**Completion gate.** Branching never mutates the original and never duplicates shared history.

<a id="rule-wp-15.02"></a>

### WP-15.02 — Attachments

**What must be fully done.** Managed attachments enter the managed resource store with integrity verification; referenced attachments record an external location with an availability state. Neither is embedded in message content. Availability changes are surfaced rather than producing an error at read time.

**Testing requirements.** Managed round-trip with integrity verification; reference-unavailable behaviour; a test asserting no attachment body is embedded in message storage.

**Completion gate.** Attachments are stored by reference, integrity is verified, and unavailability is a visible state rather than a failure.

<a id="rule-wp-15.03"></a>

### WP-15.03 — Projects and profiles

**What must be fully done.** A project groups conversations and context with its own settings; an agent profile bundles model choice, mode and behavioural configuration. Both are first-class objects with their own lifecycle. A profile is not a skill and a project is not a workspace.

**Testing requirements.** Lifecycle tests; a distinction test asserting the three container concepts are not interchangeable.

**Completion gate.** Projects and profiles have independent lifecycles and are structurally distinct from workspaces and skills.

<a id="rule-wp-15.04"></a>

### WP-15.04 — Skills

**What must be fully done.** Skills are versioned declarative guidance that reference capabilities without conferring them. A skill update never modifies a historical result. Skills are manageable as first-class objects rather than buried in settings.

**Testing requirements.** A test asserting a skill grants no capability; a versioning test asserting historical results are unchanged by an update.

**Completion gate.** A skill confers no capability, and updating a skill leaves historical results untouched.

<a id="rule-wp-15.05"></a>

### WP-15.05 — Local search

**What must be fully done.** Full-text search over **hydrated** conversation content, attachments' extracted text and project metadata, **available while Cloud is unreachable**. Conversation content is Cloud-authoritative with a durable native cache, so this searches what the device holds — it is outage tolerance, not an account-free product, and uncached history is not silently treated as absent. The index is a derived store: deleting it rebuilds. Search respects the same permission model as direct access.

**Testing requirements.** Index rebuild-from-scratch test; relevance tests against a fixture corpus; a permission test asserting search reveals nothing direct access would refuse.

**Completion gate.** Search over cached content works during a Cloud outage, the index rebuilds fully from the cache, and search never leaks what access would refuse.

<a id="rule-wp-15.06"></a>

### WP-15.06 — History, export client and recovery

**What must be fully done.** Implement the client history/download/fidelity presentation using acknowledged Chat data and pending drafts. Before the production Cloud exists, exercise transport against explicitly registered test-only export fixtures on the [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) host. Build no local archive or provider logic. The real Cloud export producer and its end-to-end acceptance are WP-25.08.

**Testing requirements.** Read a fixture manifest, verify attachment hashes and omissions, display unsent-draft exclusion and retry interruption; assert no secrets. Kill during local pending-write recovery. Record the fixture and its removal owner.

**Completion gate.** The production client and recovery path work against the declared test protocol. This gate proves client behaviour only; Cloud export completeness is not claimed until [WP-25.08](25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) removes the fixture and exercises the real producer.

<a id="rule-wp-15.07"></a>

### WP-15.07 — Reference drift check

> **Not a baseline audit.** The ArcChat matrix is complete and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. This sub-step is **maintenance**, and it is the producer of the drift check the package gate requires.

**What must be fully done.** The reference is compared against its bound commit — AionUi at `29c9271a5`. Three outputs are produced:

1. **Changed material**: any file behind a matrix row that changed since the bound commit, with the row re-assessed.
2. **Newly introduced material**: capabilities added upstream since the bound commit, each assessed against the accepted ArcChat scope. **A new upstream capability does not become an ArcForges requirement by appearing** — it is mapped to an existing requirement or recorded as an accepted exclusion.
3. **Licence re-verification**: the reference's licence files are re-read. A subtree licence can change upstream, and the disposition of every row depends on it.

**Testing requirements.** A drift report listing changed rows, new material with its assessment, and the licence comparison. A completeness check that every changed or new item has a disposition.

**Completion gate.** The drift report exists, every changed and newly introduced item carries a disposition, and the licence position is re-confirmed or amended with a reason. **If the licence position changed, the affected rows' dispositions are corrected before any dependent work continues** (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**).

---

<a id="rule-wp-15.90"></a>
### WP-15.90 — Verify the owned artifact and real integration

**What must be fully done.** Keep conversation/branch/profile/skill/local-search and export-client behavior. Rebind durable Cloud reads/writes, attachments and stream projections to the new SDK/AI endpoints while preserving content origin and committed-message immutability.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Existing conversation/recovery/provenance cases pass against generated contracts; local projection is not a second authoritative AI history.

**Completion gate.** Existing conversation/recovery/provenance cases pass against generated contracts; local projection is not a second authoritative AI history. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The ArcChat store schema and its first migration baseline |
| Protocol | ArcChat's own capabilities become registrable in `17` |
| UI | The real ArcChat surfaces |
| Security | Attachment handling and search permission boundaries |
| Platform | Attachment and export file handling per platform |
| Migration | ArcChat schema version 1 and its fixture |
| Compatibility | The first ArcChat export format version |

---

## 7. Tests and verification evidence

**Required evidence addition.** [WP-15.00](#rule-wp-15.00) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Immutability, streaming and scale results | [WP-15.00](#rule-wp-15.00) |
| Branch independence results | [WP-15.01](#rule-wp-15.01) |
| Attachment integrity and availability results | [WP-15.02](#rule-wp-15.02) |
| Container distinction results | [WP-15.03](#rule-wp-15.03) |
| Skill capability-free and versioning results | [WP-15.04](#rule-wp-15.04) |
| Index rebuild, relevance and permission results | [WP-15.05](#rule-wp-15.05) |
| Export completeness, manifest agreement, secret-scan and recovery results | [WP-15.06](#rule-wp-15.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-15.90](#rule-wp-15.90) and all inherited domain-specific gates must pass on the same candidate closure. Existing conversation/recovery/provenance cases pass against generated contracts; local projection is not a second authoritative AI history.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. **Drift check only**: the reference is compared against its bound commit, and any newly introduced material is assessed against the accepted ArcChat scope. The matrix and its licence audit were completed as design-stage evidence and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. Findings carried in: **F-AC-1** records that the reference implements remote control by running a web server on the user’s machine — the shape **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** forbids. [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26) and [WP-31](31-arcchat-mobile-android.md#rule-wp-31) already assert the prohibition structurally.
2. Committed messages are immutable; an interrupted stream never stores a fragment as complete; large conversations meet the responsiveness budget.
3. Branching shares history by reference and never mutates the original.
4. Attachments are stored by reference with integrity verification, and unavailability is a visible state.
5. Projects, profiles and skills are structurally distinct, with skills conferring no capability and updates not altering history.
6. Search over cached content works during a Cloud outage, rebuilds from scratch, and leaks nothing direct access would refuse.
7. The export client validates its declared fixture manifest here; WP25.08 proves the real Cloud conversation export. The client excludes unsynchronised edits and says so, carries no secrets ([EX-03](../../requirements/products/arcchat.md#rule-ex-03) there), and recovery reports uncommitted loss explicitly. **No local conversation archive format is built** ([EX-01](../../requirements/products/arcchat.md#rule-ex-01) of the ArcChat requirements).
8. **ArcChat is fully usable with every other product absent.**

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-14](14-hub-and-minimal-provider-slice.md#rule-wp-14)

**Downstream — consumers of these released outputs.**

- [WP-17](17-arcchat-independent-core.md#rule-wp-17)
- [WP-52](52-cloud-harness.md#rule-wp-52)


---
