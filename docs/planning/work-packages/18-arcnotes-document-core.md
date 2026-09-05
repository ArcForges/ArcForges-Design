# WP-18 — ArcNotes Document Core

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: D — ArcNotes core
> Upstream: `07`, `10`, `14` · Downstream: `19`

> **Goal.** Make ArcNotes a complete local product: block editing, links and backlinks, properties and tags, attachments, undo, history, checkpoints and trash — with crash recovery and upgrade migration proven, and large-document performance measured.

---

## 1. Scope and purpose

**In scope.** The block document model and editor; internal links, block links and backlinks; typed properties and tags at document level; managed and referenced attachments; undo, history, checkpoint and trash as four distinct mechanisms; crash recovery; upgrade migration; and large-document performance.

**Out of scope.** Edgeless canvas (`27`), database views (`28`) and slides (`29`) — the phased completion of **D-006**. Search, import and export (`19`). Sync (`25`).

**Why this package exists.** `I2 §III.5` starts ArcNotes from the local closed loop. `SQ-05` then uses ArcNotes to prove sync, which requires a real document model with revisions, attachments, deletions and history first.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md) | The full product model, domain concepts and V1 scope |
| [`../../requirements/13-data-formats-and-portability.md`](../../requirements/13-data-formats-and-portability.md) | Storage strategy, save semantics and the four-mechanism separation |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The ArcNotes Reference Coverage Matrix over its two references |
| `WP-13.01` output | The editor, store, undo and recovery probe conclusions |
| `WP-07`, `WP-10`, `WP-14` output | Persistence, shell and the provider skeleton |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcNotes Reference Coverage Matrix and licence audit over both references are complete before this package begins** (`DC-02`). |
| BR-02 | **ArcNotes scope is phased full inclusion of edgeless, database views and slides** (**D-006**). This package builds the V1 compatibility baseline every later phase must preserve. |
| BR-03 | **Undo, history, checkpoint and journal are four distinct mechanisms** (`QI-09`) and never substitute for one another. |
| BR-04 | **A document rename never breaks a link** — links target a stable identity, not a name. |
| BR-05 | **Backlinks are derived** from a link index and are never written into document content. |
| BR-06 | **A broken link has an explicit state**, never a silent failure or a deleted reference. |
| BR-07 | **Deleting a tag never deletes a document**; it removes classification. |
| BR-08 | **An attachment is never base64-embedded in document content.** |
| BR-09 | **The editing authority of an embedded reference stays with the original object** — there is no second writable block. |
| BR-10 | **Table blocks are document tables, not a relational database engine** in V1. |
| BR-11 | **ArcNotes works fully with no account and no cloud.** |

---

## 4. Projects, directories, files and major types affected

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

### WP-18.00 — Block document model

**What must be fully done.** A document is an ordered tree of typed blocks with stable block identities. Every editing operation is a command through the single write path, producing one revision. Multi-block selection is first-class. Block drag and drop distinguishes move from reference and from copy.

**Testing requirements.** Command round-trips per block kind; multi-block operation tests; a stability test asserting block identity survives reorder and reparent.

**Completion gate.** Every editing operation is a single-write-path command, and block identity is stable across structural change.

### WP-18.01 — Editor interaction

**What must be fully done.** Rich block editing with markdown-friendly keyboard syntax and a slash menu, distinct from the command palette. Editing is responsive under the large-document corpus. Composition (input-method) editing works correctly on every platform.

**Testing requirements.** Interaction tests per block kind; a composition-input test per platform; responsiveness measurement against the scale corpus.

**Completion gate.** Editing meets the responsiveness budget on the scale corpus, and composition input works on every platform.

### WP-18.02 — Links, backlinks and outline

**What must be fully done.** Document links and block links target stable identities with an optional display alias. Renaming never breaks a link. Backlinks derive from the link index and are presented in a panel, never written into content. A broken link shows an explicit state. A document outline derives from structure.

**Testing requirements.** Rename-preserves-link; index rebuild from scratch; broken-link state test; a structural test asserting backlinks are absent from stored content.

**Completion gate.** Rename never breaks a link, the index rebuilds, and backlinks are provably derived.

### WP-18.03 — Properties and tags

**What must be fully done.** Typed properties with system and user properties separated. Tags as cross-cutting classification that carry no hierarchical position and whose deletion removes classification only. Light notes stay light: properties are optional and never imposed.

**Testing requirements.** Type validation per property kind; a tag-deletion test asserting documents survive; a default-experience test asserting a plain note requires no properties.

**Completion gate.** Property typing is enforced, tag deletion never deletes documents, and plain notes remain unencumbered.

### WP-18.04 — Attachments

**What must be fully done.** Managed attachments enter the managed resource store; external references record a location with an availability state. Small dragged files default to managed; large or clearly external material defaults to reference. Extracted text from a document attachment is derived data.

**Testing requirements.** Managed round-trip with integrity; reference-unavailable behaviour; a structural test asserting no embedded encoding in content; a derived-data rebuild test.

**Completion gate.** No attachment body is embedded in content, integrity is verified, and extracted text is rebuildable derived data.

### WP-18.05 — Undo, history, checkpoint and trash

**What must be fully done.** Four distinct mechanisms: session undo with composite operation grouping; document history across revisions; explicit user checkpoints; and trash with restore and permanent deletion. None substitutes for another, and each has its own retention and scope.

**Testing requirements.** A distinction matrix asserting each mechanism's independent behaviour; restore-from-trash; checkpoint restore; a test asserting undo history is not crash recovery.

**Completion gate.** All four mechanisms behave independently, and none can be used to recover what another is responsible for.

### WP-18.06 — Recovery and migration

**What must be fully done.** Crash recovery to the last committed boundary with explicit loss reporting. Upgrade migration from every prior schema version with semantic preservation verified against golden fixtures. Downgrade behaviour defined: supported with a reverse migration, or refused cleanly.

**Testing requirements.** Kill-during-edit, kill-during-migration and corrupted-tail recovery; migration from every fixture with semantic comparison; a downgrade refusal test.

**Completion gate.** Recovery is clean and honest in every case, migration preserves semantics, and downgrade never leaves partial state.

### WP-18.07 — Capability surface

**What must be fully done.** ArcNotes registers its real capability set: query, read, create, edit, and artifact production — each with risk level, side-effect class, reversibility and approval posture. Owner-side validation is enforced regardless of caller.

**Testing requirements.** Capability descriptor validation; owner-side refusal tests; an idempotency test per write capability.

**Completion gate.** Every capability declares its risk and approval posture, and owner-side validation refuses regardless of what the caller asserts.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The ArcNotes schema and its V1 migration baseline |
| Protocol | ArcNotes' real capability contracts |
| UI | The complete ArcNotes editing experience on the shared shell |
| Security | Attachment handling, link resolution and owner-side validation |
| Platform | Composition input, drag and drop, and file handling per platform |
| Migration | The V1 format fixture every later phase must still read |
| Compatibility | The V1 data compatibility baseline for `27`, `28` and `29` |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Write-path and block-identity stability results | `WP-18.00` |
| Interaction, composition and responsiveness results | `WP-18.01` |
| Link, backlink and index-rebuild results | `WP-18.02` |
| Property typing and tag-deletion results | `WP-18.03` |
| Attachment integrity and no-embedding results | `WP-18.04` |
| Four-mechanism distinction matrix | `WP-18.05` |
| Recovery matrix and migration semantic comparison | `WP-18.06` |
| Capability descriptor and owner-side refusal results | `WP-18.07` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The ArcNotes Reference Coverage Matrix and licence audit over both references are complete.
2. Every editing operation is a single-write-path command; block identity survives structural change.
3. Editing meets the responsiveness budget on the scale corpus, including composition input on every platform.
4. Rename never breaks a link; the link index rebuilds from scratch; backlinks are provably derived.
5. Property typing is enforced; tag deletion never deletes documents; plain notes stay light.
6. No attachment body is embedded in content; integrity is verified; extracted text is rebuildable.
7. Undo, history, checkpoint and trash behave independently, and none recovers what another owns.
8. Crash recovery is clean and honest; migration preserves semantics against every fixture; downgrade never leaves partial state.
9. Every ArcNotes capability declares risk and approval posture, and owner-side validation refuses regardless of caller assertion.
10. **ArcNotes is fully usable with no account, no cloud and no ArcChat.**

---

## 9. Dependencies

**Upstream.** `07` (persistence), `10` (shell), `14` (the provider skeleton).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `19` — Search and portability | The document model to index and export |
| `20` — First workflow | Real capabilities for the cross-product workflow |
| `25` — Sync | The document revision, attachment and deletion semantics sync proves against |
| `27`–`29` | The V1 compatibility baseline every later phase preserves |
