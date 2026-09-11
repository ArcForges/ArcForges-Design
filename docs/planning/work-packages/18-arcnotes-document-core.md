<a id="rule-wp-18"></a>

# WP-18 — ArcNotes Document Core

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: D — ArcNotes core
> Upstream: `07`, `10`, `14` · Downstream: `19`

> **Goal.** Make ArcNotes a complete local product: block editing, links and backlinks, properties and tags, attachments, undo, history, checkpoints and trash — with crash recovery and upgrade migration proven, and large-document performance measured.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcNotes; Platform packages. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The block document model and editor; internal links, block links and backlinks; typed properties and tags at document level; managed and referenced attachments; undo, history, checkpoint and trash as four distinct mechanisms; crash recovery; upgrade migration; and large-document performance.

**Out of scope.** Bounded properties and saved views (`28`). **Edgeless canvas and slides are excluded from delivery by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — `27` and `29` are retired, not deferred. Search, import and export (`19`). Sync (`25`).

**Why this package exists.** The [native editing design](../../architecture/18-editing-and-rich-content.md) starts with a real editor, working store, undo and crash recovery. [SQ-05](../implementation-sequence.md#rule-sq-05) then uses ArcNotes to prove sync, which requires a real document model with revisions, attachments, deletions and history first.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile)

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md) | The full product model, domain concepts and V1 scope |
| [`../../requirements/13-data-formats-and-portability.md`](../../requirements/13-data-formats-and-portability.md) | Storage strategy, save semantics and the four-mechanism separation |
| [`../../assurance/reference-coverage/arcnotes-affine-siyuan.md`](../../assurance/reference-coverage/arcnotes-affine-siyuan.md) | **The completed ArcNotes Reference Coverage Matrix** — 41 rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, oracle and owner |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix method and the ten-field provenance record that governs any future reuse |
| [WP-13.01](13-high-risk-technical-probes.md#rule-wp-13.01) output | The editor, store, undo and recovery probe conclusions |
| [WP-07](07-local-persistence-foundation.md#rule-wp-07), [WP-10](10-design-system-and-desktop-shell.md#rule-wp-10), [WP-14](14-hub-and-minimal-provider-slice.md#rule-wp-14) output | Persistence, shell and the provider skeleton |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcNotes Reference Coverage Matrix is a completed, versioned planning input** — [`../../assurance/reference-coverage/arcnotes-affine-siyuan.md`](../../assurance/reference-coverage/arcnotes-affine-siyuan.md), 41 item-level rows, bound to AFFiNE at `81df4751a3` and SiYuan at `eef105683`. It was produced before this plan was derived (**[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)**). **This package consumes it and checks it for drift; it does not create it.** |
| BR-02 | **ArcNotes scope is the notebook core plus bounded properties and saved views** (**[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** as amended by **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**). This package builds the V1 baseline every later phase must preserve. |
| BR-03 | **Undo, history, checkpoint and journal are four distinct mechanisms** ([QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)) and never substitute for one another. |
| <a id="rule-br-04"></a>BR-04 | **A document rename never breaks a link** — links target a stable identity, not a name. |
| BR-05 | **Backlinks are derived** from a link index and are never written into document content. |
| BR-06 | **A broken link has an explicit state**, never a silent failure or a deleted reference. |
| <a id="rule-br-07"></a>BR-07 | **Deleting a tag never deletes a document**; it removes classification. |
| BR-08 | **An attachment is never base64-embedded in document content.** |
| BR-09 | **The editing authority of an embedded reference stays with the original object** — there is no second writable block. |
| BR-10 | **Table blocks are document tables, not a relational database engine** in V1. |
| <a id="rule-br-11"></a>BR-11 | **An enrolled, hydrated notebook remains editable and searchable during a Cloud outage**, and pending edits are durably recoverable (`§3.1` of the product scope). **This is outage tolerance, not an account-free product**: initial notebook creation and enrolment require Cloud, and uncached content is unavailable until it is fetched ([C-05](../../requirements/00-product-scope-and-portfolio.md#rule-c-05)). |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.Domain/` | Document, block, link, property, tag, attachment, checkpoint, trash |
| `src/ArcNotes/ArcNotes.Application/` | Application services shared by UI and RPC |
| `src/ArcNotes/ArcNotes.Editor/` | The block editor: composition, selection, drag and drop, keyboard syntax, slash menu |
| `src/ArcNotes/ArcNotes.Infrastructure/` | Store schema, link index, attachment storage, migration set |
| `src/ArcNotes/ArcNotes.Presentation/`, `.Desktop/` | The real ArcNotes surfaces |
| `fixtures/formats/arcnotes/v1/` | The V1 format fixture that every later phase must still read |
| `tests/ArcNotes.Tests.*` | Domain, editor, store, recovery and performance suites |

**Major types introduced.** `Document`, `Block`, `BlockKind`, `BlockSelection`, `DocumentLink`, `BlockLink`, `Backlink`, `LinkIndex`, `PropertyDefinition`, `PropertyValue`, `Tag`, `ManagedAttachment`, `ExternalAttachmentReference`, `DocumentCheckpoint`, `TrashEntry`, `UndoScope`.

---

## 5. Required implementation work

<a id="rule-wp-18.00"></a>

### WP-18.00 — Block document model

**Required design implementation and verification.** Preserve block/attachment origin in edits, copy, split/merge, undo, history, conflict alternatives and restore. A retained AI block remains marked after manual edits; removing the whole block removes only its contribution to the current document union. Commit content and metadata atomically, and test unknown profile preservation/refusal.

**What must be fully done.** Implement notebook→folder hierarchy→document placement, stable folder IDs, notebook-owned structural commands and the matching Cloud canonical schema contract; documents do not contain documents.  A document is an ordered tree of typed blocks with stable block identities. The typed inline content model and the closed block-kind set of [`../../architecture/18-editing-and-rich-content.md`](../../architecture/18-editing-and-rich-content.md) `§2`, with **no markup string on any internal path**. The closed `EditTransaction` operation set (`§3.1` there): atomic application, computed inverses, fractional ordinal insertion, and declared kind-conversion mappings including their stated losses. Multi-block selection is first-class. Block drag and drop distinguishes move from reference and from copy. An unknown block kind and an unknown mark survive a read-modify-write cycle unchanged.

**Testing requirements.** Exercise deep folders, cycle denial, reorder, cross-notebook move, delete/restore and immutable revision references.  Command round-trips per block kind; multi-block operation tests; a stability test asserting block identity survives reorder, reparent, split of a sibling, conversion and merge; a transaction-atomicity test asserting a failure at any operation leaves the document unchanged; a conversion matrix asserting every declared mapping and every stated loss; a forward-compatibility test on unknown kinds and marks; clipboard tests asserting exact code round-trip and table-shape preservation; a repository policy test asserting no internal path serialises content to Markdown, HTML or RTF.

**Completion gate.** Folder structure and document placement have an explicit owner and revision rule.  Every editing operation is a single-write-path transaction, block identity is stable across structural change, no internal path round-trips content through a markup string, and every conversion applies its declared mapping.

<a id="rule-wp-18.01"></a>

### WP-18.01 — Editor interaction

**What must be fully done.** Rich block editing with markdown-friendly keyboard syntax and a slash menu, distinct from the command palette. **Grapheme-correct caret movement, deletion and selection**; Unicode word boundaries; bidirectional caret movement and discontiguous selection painting (`§4.2` of the editing architecture). **IME composition as view state**, committing exactly one transaction, positioned from the caret's real rectangle, and never interrupted by a concurrent remote or agent edit (`§4.3` there). Virtualised block layout with measurement caching, scroll anchoring to `(blockId, offset)`, and bounded nesting (`§5.2` there). Code highlighting from a bounded, statically registered grammar set, degrading to plain text; math rendering with an explicitly marked unsupported-construct path.

**Testing requirements.** Interaction tests per block kind; a text-correctness corpus covering emoji with modifiers, Devanagari, Thai and combining marks; a composition-input test per platform asserting one undo entry and one transaction, plus a concurrent-edit-during-composition test; a bidi caret and selection-painting test; a ten-thousand-block scale test asserting interactive open and no re-measurement of measured blocks; a scroll-anchor test asserting an edit above the viewport does not move the reader; an unsupported-math-construct test asserting source with an explicit marker.

**Completion gate.** Editing meets the responsiveness budget on the scale corpus, text handling is grapheme- and bidi-correct, composition input works on every platform without loss, and no unsupported construct renders silently wrong.

<a id="rule-wp-18.02"></a>

### WP-18.02 — Links, backlinks and outline

**What must be fully done.** Document links and block links target stable identities with an optional display alias. Renaming never breaks a link. Backlinks derive from the link index and are presented in a panel, never written into content. A broken link shows an explicit state. A document outline derives from structure.

**Testing requirements.** Rename-preserves-link; index rebuild from scratch; broken-link state test; a structural test asserting backlinks are absent from stored content.

**Completion gate.** Rename never breaks a link, the index rebuilds, and backlinks are provably derived.

<a id="rule-wp-18.03"></a>

### WP-18.03 — Properties and tags

**Required design implementation and verification.** Implement exact scalar storage/validation and stable option IDs before exposing properties. Test missing/empty/false/zero, decimal/date/offset validation, label rename and refused dependent type changes. Persist semantic revision separately from label-only definition revisions.

**What must be fully done.** Typed properties with system and user properties separated. Tags as cross-cutting classification that carry no hierarchical position and whose deletion removes classification only. Light notes stay light: properties are optional and never imposed.

**Testing requirements.** Type validation per property kind; a tag-deletion test asserting documents survive; a default-experience test asserting a plain note requires no properties.

**Completion gate.** Property typing is enforced, tag deletion never deletes documents, and plain notes remain unencumbered.

<a id="rule-wp-18.04"></a>

### WP-18.04 — Attachments

**What must be fully done.** Route hostile PDF/image parsing through [WP-11.09](11-security-foundation.md#rule-wp-11.09) ContentSandbox; complete the PDF dependency/provenance adoption gate [PG-12](../../assurance/open-gates-register.md#rule-pg-12) here.  Managed attachments enter the managed resource store; external references record a location with an availability state. Small dragged files default to managed; large or clearly external material defaults to reference. Extracted text from a document attachment is derived data.

The three preview levels of `§8.1` of the editing architecture — metadata card, thin preview, in-product viewer — with **explicit degradation to the level below and a stated reason**, never a blank surface. Bounded, off-thread image decode with EXIF orientation applied. **No preview path fetches a remote resource referenced by the content, and none evaluates embedded program content.** The PDF viewer is subject to [PG-12](../../assurance/open-gates-register.md#rule-pg-12): until its dependency is adopted under [DR-03](../../architecture/12-native-interop-and-media.md#rule-dr-03), [AT-05](../../requirements/products/arcnotes.md#rule-at-05) is not met and the surface presents a metadata card.

**Testing requirements.** Cause a real native parser crash/hang and prove the parent survives with a metadata card and intact document.  Managed round-trip with integrity; reference-unavailable behaviour; a structural test asserting no embedded encoding in content; a derived-data rebuild test; a malformed-input corpus for images, PDFs and embeds asserting degradation to a placeholder with a reason and no process instability; an egress test asserting no preview path performs a network fetch; a level-degradation test asserting every unavailable level states its reason.

**Completion gate.** In-process status-code handling is not crash-containment evidence.  No attachment body is embedded in content, integrity is verified, extracted text is rebuildable derived data, every preview degradation states a reason, and no preview path fetches a remote resource or evaluates content.

<a id="rule-wp-18.05"></a>

### WP-18.05 — Undo, history, checkpoint and trash

**What must be fully done.** Four distinct mechanisms: session undo with composite operation grouping; document history across revisions; explicit user checkpoints; and trash with restore and permanent deletion. None substitutes for another, and each has its own retention and scope.

Session undo follows `§3.2` of the editing architecture: **selection is restored with content**, typing coalesces and breaks on the declared boundaries, an agent transaction is undoable and labelled with its origin, and a remote change rebases pending entries rather than retargeting them.

**Testing requirements.** A distinction matrix asserting each mechanism's independent behaviour; restore-from-trash; checkpoint restore; a test asserting undo history is not crash recovery; an undo-selection test; a coalescing-boundary test; an agent-edit undo and attribution test; a rebase test asserting a remote change never causes an undo entry to target the wrong block.

**Completion gate.** All four mechanisms behave independently, none can be used to recover what another is responsible for, undo restores selection with content, and no undo entry is ever applied to the wrong block after a concurrent change.

<a id="rule-wp-18.06"></a>

### WP-18.06 — Recovery and migration

**What must be fully done.** Crash recovery to the last committed boundary with explicit loss reporting. Upgrade migration from every prior schema version with semantic preservation verified against golden fixtures. Downgrade behaviour defined: supported with a reverse migration, or refused cleanly.

**Testing requirements.** Kill-during-edit, kill-during-migration and corrupted-tail recovery; migration from every fixture with semantic comparison; a downgrade refusal test.

**Completion gate.** Recovery is clean and honest in every case, migration preserves semantics, and downgrade never leaves partial state.

<a id="rule-wp-18.07"></a>

### WP-18.07 — Capability surface

**What must be fully done.** ArcNotes registers its real capability set: query, read, create, edit, and artifact production — each with risk level, side-effect class, reversibility and approval posture. Owner-side validation is enforced regardless of caller.

**Testing requirements.** Capability descriptor validation; owner-side refusal tests; an idempotency test per write capability.

**Completion gate.** Every capability declares its risk and approval posture, and owner-side validation refuses regardless of what the caller asserts.

<a id="rule-wp-18.08"></a>

### WP-18.08 — Reference drift check

> **Not a baseline audit.** The ArcNotes matrix is complete and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. This sub-step is **maintenance**, and it is the producer of the drift check the package gate requires.

**What must be fully done.** The reference is compared against its bound commit — AFFiNE at `81df4751a3` and SiYuan at `eef105683`. Three outputs are produced:

1. **Changed material**: any file behind a matrix row that changed since the bound commit, with the row re-assessed.
2. **Newly introduced material**: capabilities added upstream since the bound commit, each assessed against the accepted ArcNotes scope. **A new upstream capability does not become an ArcForges requirement by appearing** — it is mapped to an existing requirement or recorded as an accepted exclusion.
3. **Licence re-verification**: the reference's licence files are re-read. A subtree licence can change upstream, and the disposition of every row depends on it.

**Testing requirements.** A drift report listing changed rows, new material with its assessment, and the licence comparison. A completeness check that every changed or new item has a disposition.

**Completion gate.** The drift report exists, every changed and newly introduced item carries a disposition, and the licence position is re-confirmed or amended with a reason. **If the licence position changed, the affected rows' dispositions are corrected before any dependent work continues** (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**).

---

<a id="rule-wp-18.90"></a>
### WP-18.90 — Verify the owned artifact and real integration

**What must be fully done.** Keep block/document/editor, scalar base, attachment/PDF isolation, undo/history/pending-work behavior. Rebind shared resources and storage contracts; preserve accepted no-account launch and hydrated notebook outage behavior.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Independent editor/store/recovery fixtures, helper isolation and content-origin/attachment checks; no new edgeless or slide scope.

**Completion gate.** Independent editor/store/recovery fixtures, helper isolation and content-origin/attachment checks; no new edgeless or slide scope. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The ArcNotes schema and its V1 migration baseline |
| Protocol | ArcNotes' real capability contracts |
| UI | The complete ArcNotes editing experience on the shared shell, including virtualised block layout and the three preview levels |
| Security | Attachment handling, link resolution and owner-side validation |
| Platform | Composition input, text shaping and bidi, drag and drop, and file handling per platform; the document-rendering dependency of [PG-12](../../assurance/open-gates-register.md#rule-pg-12) where adopted |
| Migration | The V1 format fixture every later phase must still read |
| Compatibility | The supported notebook-core schema baseline consumed by `28`; canvas/slides packages are retired |

---

## 7. Tests and verification evidence

**Required evidence addition.** Property write vectors from the profile, including loss-preview/refusal and compatible rename.

**Required evidence addition.** [WP-18.00](#rule-wp-18.00) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Write-path, transaction-atomicity, conversion-mapping and block-identity stability results | [WP-18.00](#rule-wp-18.00) |
| No-markup-string repository policy test result | [WP-18.00](#rule-wp-18.00) |
| Text-correctness corpus (grapheme, bidi, composition) and scale-corpus responsiveness results | [WP-18.01](#rule-wp-18.01) |
| Link, backlink and index-rebuild results | [WP-18.02](#rule-wp-18.02) |
| Property typing and tag-deletion results | [WP-18.03](#rule-wp-18.03) |
| Attachment integrity, no-embedding, malformed-input degradation and preview-egress results | [WP-18.04](#rule-wp-18.04) |
| Four-mechanism distinction matrix, undo-selection and undo-rebase results | [WP-18.05](#rule-wp-18.05) |
| Recovery matrix and migration semantic comparison | [WP-18.06](#rule-wp-18.06) |
| Capability descriptor and owner-side refusal results | [WP-18.07](#rule-wp-18.07) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-18.90](#rule-wp-18.90) and all inherited domain-specific gates must pass on the same candidate closure. Independent editor/store/recovery fixtures, helper isolation and content-origin/attachment checks; no new edgeless or slide scope.

**[PG-22](../../assurance/open-gates-register.md#rule-pg-22) evidence:** [WP-18.04](#rule-wp-18.04) — Real packaged PDF/image parser isolation integration; combine with the platform broker proof. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-12](../../assurance/open-gates-register.md#rule-pg-12) evidence:** [WP-18.04](#rule-wp-18.04) — Real PDF viewer integration and malformed native input containment, consuming the packaged sandbox proof. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**Additional completion requirement.** Property types and persistence agree with the frozen query profile; no local culture defaults affect stored meaning.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. **Drift check only**: the reference is compared against its bound commit, and any newly introduced material is assessed against the accepted ArcNotes scope. The matrix and its licence audit were completed as design-stage evidence and closed [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) before this package began. Findings carried in: **F-AN-1** records that AFFiNE’s `packages/backend/**` and `packages/common/native/**` are **proprietary**, not MIT — permanently ineligible for reuse and deliberately unread. **F-AN-2** is historical: its slides-oracle obligation is superseded by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006), which excludes slides with no future hook.
2. Every editing operation is a single-write-path command; block identity survives structural change.
3. Editing meets the responsiveness budget on the scale corpus; text handling is grapheme- and bidi-correct; composition input works on every platform without loss and is never interrupted by a concurrent edit.
3a. **No internal path round-trips content through a markup string**, and every kind conversion applies its declared mapping with its stated loss shown first.
4. Rename never breaks a link; the link index rebuilds from scratch; backlinks are provably derived.
5. Property typing is enforced; tag deletion never deletes documents; plain notes stay light.
6. No attachment body is embedded in content; integrity is verified; extracted text is rebuildable. **Every preview level that is unavailable degrades to the level below with a stated reason**, no preview path fetches a remote resource or evaluates embedded content, and a malformed image, PDF or embed degrades to a placeholder without affecting process stability.
7. Undo, history, checkpoint and trash behave independently, and none recovers what another owns. Undo restores selection with content, an agent edit is undoable and attributed, and a concurrent change never causes an undo entry to target the wrong block.
8. Crash recovery is clean and honest; migration preserves semantics against every fixture; downgrade never leaves partial state.
9. Every ArcNotes capability declares risk and approval posture, and owner-side validation refuses regardless of caller assertion.
10. **An enrolled, hydrated notebook is editable and searchable through a Cloud outage, with pending edits durably recoverable**, and ArcNotes never requires ArcChat. Enrolment and uncached content require Cloud ([BR-11](#rule-br-11)).

---

## 9. Dependencies

**Upstream — all must be complete.**

- [07 local persistence foundation](07-local-persistence-foundation.md#rule-wp-07)
- [10 design system and desktop shell](10-design-system-and-desktop-shell.md#rule-wp-10)
- [14 hub and minimal provider slice](14-hub-and-minimal-provider-slice.md#rule-wp-14)

**Downstream — consumers of these released outputs.**

- [19 arcnotes search and portability](19-arcnotes-search-and-portability.md#rule-wp-19)

---
