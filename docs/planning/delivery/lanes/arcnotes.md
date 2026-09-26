# ArcNotes — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Document core, search and portability, properties and saved views.

Tasks: 35 · Owning repositories: ArcNotes · Integration owner(s): ArcNotes integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [NOTES.01](#task-notes-01) | Notebook/folder hierarchy, document placement and structural commands | feature | M | [PLT.01](platform.md#task-plt-01) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [NOTES.02](#task-notes-02) | Block/inline content model, EditTransaction engine, kind conversions and clipboard | feature | XL | [PLT.01](platform.md#task-plt-01) (artifact), [CON.91](contracts.md#task-con-91) (contract), [CON.03](contracts.md#task-con-03) (contract) | not-started |
| [NOTES.03](#task-notes-03) | Editor interaction: caret, selection, IME composition, markdown-friendly input | feature | L | [PLT.27](platform.md#task-plt-27) (artifact), [APP.01](app-composition.md#task-app-01) (artifact), [PLT.26](platform.md#task-plt-26) (artifact) | not-started |
| [NOTES.04](#task-notes-04) | Virtualised block layout, measurement caching and scroll anchoring | feature | L | [PLT.26](platform.md#task-plt-26) (artifact), [PLT.27](platform.md#task-plt-27) (artifact) | not-started |
| [NOTES.05](#task-notes-05) | Rich content kinds: code highlighting, math rendering (notes.math.v1), table interaction | feature | L | [PLT.27](platform.md#task-plt-27) (artifact) | not-started |
| [NOTES.06](#task-notes-06) | Links, backlinks and outline over the canonical block store | feature | M | [NOTES.01](#task-notes-01) (artifact), [NOTES.02](#task-notes-02) (artifact) | not-started |
| [NOTES.07](#task-notes-07) | Document-level typed properties and tags (basic) | feature | M | [NOTES.01](#task-notes-01) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [NOTES.08](#task-notes-08) | Managed and external attachments (non-PDF): storage, availability, preview levels 1-2 | feature | M | [PLT.05](platform.md#task-plt-05) (artifact), [NOTES.02](#task-notes-02) (artifact) | not-started |
| [NOTES.09](#task-notes-09) | PDF in-product viewer, page anchors and native parser isolation | feature | L | [PLT.45](platform.md#task-plt-45) (artifact), [NAT.06](native.md#task-nat-06) (artifact) | not-started |
| [NOTES.10](#task-notes-10) | Undo, history, checkpoint and trash as four distinct mechanisms | feature | L | [NOTES.02](#task-notes-02) (artifact) | not-started |
| [NOTES.11](#task-notes-11) | Crash recovery and upgrade/downgrade migration | feature | M | [PLT.02](platform.md#task-plt-02) (artifact), [PLT.03](platform.md#task-plt-03) (artifact), [PLT.04](platform.md#task-plt-04) (artifact) | not-started |
| [NOTES.12](#task-notes-12) | ArcNotes capability surface registration | feature | M | [PLT.18](platform.md#task-plt-18) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [NOTES.13](#task-notes-13) | ArcNotes reference-matrix drift check (AFFiNE/SiYuan) | governance | S | none | not-started |
| [NOTES.14](#task-notes-14) | Owned-artifact and real-integration verification | acceptance | M | [NOTES.01](#task-notes-01) (artifact), [NOTES.02](#task-notes-02) (artifact), [NOTES.03](#task-notes-03) (artifact), [NOTES.04](#task-notes-04) (artifact), [NOTES.05](#task-notes-05) (artifact), [NOTES.06](#task-notes-06) (artifact), [NOTES.07](#task-notes-07) (artifact), [NOTES.08](#task-notes-08) (artifact), [NOTES.09](#task-notes-09) (artifact), [NOTES.10](#task-notes-10) (artifact), [NOTES.11](#task-notes-11) (artifact), [NOTES.12](#task-notes-12) (artifact), [NOTES.13](#task-notes-13) (artifact) | not-started |
| [NOTES.15](#task-notes-15) | Local full-text index over hydrated content | feature | L | [NOTES.02](#task-notes-02) (artifact), [PLT.07](platform.md#task-plt-07) (artifact) | not-started |
| [NOTES.16](#task-notes-16) | Query, ranking and permission over the local index | feature | M | [NOTES.15](#task-notes-15) (artifact), [NOTES.07](#task-notes-07) (artifact) | not-started |
| [NOTES.17](#task-notes-17) | Citation anchors | feature | M | [NOTES.15](#task-notes-15) (artifact) | not-started |
| [NOTES.18](#task-notes-18) | Saved views (list projection only) | feature | M | [NOTES.16](#task-notes-16) (artifact), [NOTES.07](#task-notes-07) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [NOTES.19](#task-notes-19) | Non-destructive Markdown/plain-text import (incl. Obsidian-style folders) | feature | L | [NOTES.01](#task-notes-01) (artifact), [NOTES.02](#task-notes-02) (artifact), [NOTES.06](#task-notes-06) (artifact) | not-started |
| [NOTES.20](#task-notes-20) | Cloud Notes export client and its named fixture endpoint | feature | L | [NOTES.01](#task-notes-01) (artifact), [CON.91](contracts.md#task-con-91) (contract), [CON.20](contracts.md#task-con-20) (contract) | not-started |
| [NOTES.21](#task-notes-21) | Repository-projection prohibition (structural assertion) | governance | S | [GOV.03](governance.md#task-gov-03) (artifact) | not-started |
| [NOTES.22](#task-notes-22) | Owned-artifact and real-integration verification | acceptance | M | [NOTES.15](#task-notes-15) (artifact), [NOTES.16](#task-notes-16) (artifact), [NOTES.17](#task-notes-17) (artifact), [NOTES.18](#task-notes-18) (artifact), [NOTES.19](#task-notes-19) (artifact), [NOTES.20](#task-notes-20) (artifact), [NOTES.21](#task-notes-21) (artifact) | not-started |
| [NOTES.23](#task-notes-23) | Typed property schemas: full bounded scalar set | feature | M | [NOTES.07](#task-notes-07) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [NOTES.24](#task-notes-24) | Query model: local evaluator and notes.scalar.v1 conformance fixtures | feature | L | [NOTES.23](#task-notes-23) (artifact), [NOTES.16](#task-notes-16) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [NOTES.26](#task-notes-26) | View kinds: list and table projections | feature | L | [NOTES.24](#task-notes-24) (artifact), [NOTES.18](#task-notes-18) (artifact) | not-started |
| [NOTES.27](#task-notes-27) | Editing through a view | feature | M | [NOTES.26](#task-notes-26) (artifact), [NOTES.02](#task-notes-02) (artifact) | not-started |
| [NOTES.28](#task-notes-28) | Lightness preservation for plain notes | governance | S | [NOTES.23](#task-notes-23) (artifact) | not-started |
| [NOTES.29](#task-notes-29) | Supported-schema migration for property/view data (local) | feature | M | [NOTES.11](#task-notes-11) (artifact), [NOTES.23](#task-notes-23) (artifact), [NOTES.26](#task-notes-26) (artifact) | not-started |
| [NOTES.30](#task-notes-30) | Cloud export fidelity for property/view metadata | feature | S | [NOTES.20](#task-notes-20) (artifact), [NOTES.23](#task-notes-23) (artifact), [NOTES.26](#task-notes-26) (artifact) | not-started |
| [NOTES.31](#task-notes-31) | Scale: large collections, many properties, large result sets | feature | M | [NOTES.26](#task-notes-26) (artifact), [NOTES.04](#task-notes-04) (artifact) | not-started |
| [NOTES.32](#task-notes-32) | Owned-artifact and real-integration verification | acceptance | M | [NOTES.23](#task-notes-23) (artifact), [NOTES.24](#task-notes-24) (artifact), [NOTES.26](#task-notes-26) (artifact), [NOTES.27](#task-notes-27) (artifact), [NOTES.28](#task-notes-28) (artifact), [NOTES.29](#task-notes-29) (artifact), [NOTES.31](#task-notes-31) (artifact) | not-started |
| [NOTES.33](#task-notes-33) | Real Cloud Notes export join replaces the / fixture endpoint | integration | M | [NOTES.20](#task-notes-20) (artifact), [NOTES.30](#task-notes-30) (artifact), [CLOUD.45](cloud.md#task-cloud-45) (artifact) | not-started |
| [NOTES.34](#task-notes-34) | Cross-evaluator conformance of notes.scalar.v1 between the native cache and the real Cloud query evaluator | integration | M | [NOTES.24](#task-notes-24) (artifact), [CLOUD.37](cloud.md#task-cloud-37) (artifact) | not-started |
| [NOTES.35](#task-notes-35) | ArcNotes participates in the three-device convergence harness | integration | M | [NOTES.01](#task-notes-01) (artifact), [NOTES.02](#task-notes-02) (artifact), [NOTES.10](#task-notes-10) (artifact), [CLOUD.44](cloud.md#task-cloud-44) (artifact), [CLOUD.37](cloud.md#task-cloud-37) (artifact), [CLOUD.38](cloud.md#task-cloud-38) (artifact), [CLOUD.39](cloud.md#task-cloud-39) (artifact), [CLOUD.40](cloud.md#task-cloud-40) (artifact), [CLOUD.41](cloud.md#task-cloud-41) (artifact), [CLOUD.42](cloud.md#task-cloud-42) (artifact) | not-started |
| [NOTES.37](#task-notes-37) | ArcNotes PDF attachment viewer against the real ContentSandbox | integration | M | [PLT.45](platform.md#task-plt-45) (artifact), [NAT.14](native.md#task-nat-14) (artifact), [NOTES.09](#task-notes-09) (artifact), [NAT.25](native.md#task-nat-25) (artifact) | not-started |

## Tasks

<a id="task-notes-01"></a>

### NOTES.01 — Notebook/folder hierarchy, document placement and structural commands

**Outcome.** ArcNotes.Domain has Notebook/Folder/Document aggregates with fractional-ordinal placement, cycle-denial, cross-notebook move and trash/restore, each structural edit a single-write-path transaction producing a typed structural outbox entry (contentProposal/namedStructuralCommand union per data-model 02).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-01` and ledger record `ledger/tasks/notes-01.md` in the Plan repository; task branch `task/notes-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-18.00](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.00) — notebook->folder hierarchy, stable folder IDs, document placement, notebook-owned structural commands, no-documents-in-documents; final-review paragraph: typed structural outbox entries, multi-root local tokens, move classification mapping/preview, offline create->move->edit crash test<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) Final-review paragraph (S5, before 18.90): independent verification of 02-desktop-data-model; typed structural outbox entries; multi-root local tokens; complete move classification mapping/preview; offline create->move->edit and crash-before/after-acknowledgement test; scalar-definition fixtures follow the fixed profile ([WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) repeats with real property/view UI) — package-level obligation contribution |
| Provides | notes.notebook-store; notes.structural-commands |
| Start prerequisites | **artifact** [PLT.01](platform.md#task-plt-01) — published ArcForges.Persistence.Sqlite commit-unit (state+command+journal+revision+outbox in one transaction). *Why:* every structural command must be the atomic commit unit defined in 06-data-persistence-and-formats.md S2.1; DesktopPlatform's Persistence.Sqlite project is currently an AssemblyPlaceholder only, so this is a real unmet artifact dependency, not a formality<br>**contract** [CON.91](contracts.md#task-con-91) — NotebookView, FolderView, NotesDocument wire records in ArcForges.Contracts.PublicApi. *Why:* already published and consumed by ArcNotes today (v1.0.0-ci.36.1); confirmed present in public/proto/arcforges/publicapi/v1/content.proto - this edge is satisfied, listed for completeness |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.37](cloud.md#task-cloud-37) — Cloud canonical Notes schema (notebook-owned folders/documents) accepts the identical structural operations (create/rename/move/reorder/trash/restore) Notes implements locally. *Why:* [WP-18.00](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.00) requires 'the matching Cloud canonical schema contract'; structural-operation parity is only provable once the real Cloud validator exists ([WP-25.00](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00)), not at Notes' start - a contract-bound fixture proves shape only, not acceptance |
| Unblocks | [NOTES.06](#task-notes-06), [NOTES.07](#task-notes-07), [NOTES.14](#task-notes-14), [NOTES.19](#task-notes-19), [NOTES.20](#task-notes-20), [NOTES.35](#task-notes-35) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Domain/Notebooks/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Domain/Folders/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Infrastructure/Migrations/0001_*`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Domain/Structural/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit tests (deep folders, cycle denial, reorder, cross-notebook move, delete/restore, immutable revision references); AOT compile; no live Cloud call in this task's own tests |
| Completion evidence | folder structure/document placement ownership+revision rule test results; structural-command atomicity results; offline create->move->edit crash-recovery result |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: ArcNotes/src currently contains only ArcForges.ArcNotes (Avalonia Hello World: ArcNotesApp.cs, MainWindow.cs, LiveSmoke.cs) and ArcForges.ArcNotes.Core (BuildIdentity.cs, CloudHelloClient.cs, HelloViewModel.cs) - no Domain/Infrastructure project exists yet |
| Notes | Does not need [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) (Hub/provider slice) or [WP-10](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10) (shell) - this is pure domain+persistence, hostable in a unit-test process before any UI exists. |

<a id="task-notes-02"></a>

### NOTES.02 — Block/inline content model, EditTransaction engine, kind conversions and clipboard

**Outcome.** A closed Block/InlineContent domain model and EditTransaction operation set (InsertBlock, RemoveBlock, MoveBlock, SetBlockKind, SplitBlock, MergeBlocks, ReplaceInlineRange, ApplyMark, SetBlockAttribute, SetProperty) exist with computed inverses, atomic apply, declared conversion mappings and no markup-string round-trip anywhere on an internal path.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-02` and ledger record `ledger/tasks/notes-02.md` in the Plan repository; task branch `task/notes-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / XL · early risk proof |
| Obligations | [WP-18.00](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.00) — typed inline content model, closed block-kind set, EditTransaction closed operation set with computed inverses and fractional ordinals, declared kind-conversion mappings, multi-block selection, drag/drop move-vs-reference-vs-copy, unknown-kind/mark forward compatibility; clipboard tests: exact code round-trip, table-shape preservation; repository-policy test that no internal path serialises content to Markdown/HTML/RTF<br>[WP-18.90](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.90) — block/document/editor scalar base and content-origin/attachment checks (domain-model portion)<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (bottom of file): stable run/atom/cell IDs, NotesTextPosition/NotesCommand, explicit IME conflict preservation, disabled stale undo with original recoverable inverse, no unspecified rebase — package-level obligation contribution<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) S8 additional completion requirement: content paths pass the stated content-origin vectors, including unknown input and failed publication — package-level obligation contribution |
| Provides | notes.block-model; notes.edit-transaction; notes.content-origin-binding |
| Start prerequisites | **artifact** [PLT.01](platform.md#task-plt-01) — same persistence commit-unit as NOTES.01. *Why:* block edits share the single write-path transaction<br>**contract** [CON.91](contracts.md#task-con-91) — Block, BlockBody, BlockProperties, RichText, TextSpan, InlineAtom, LinkSpec, MathContent, TableBlock/TableRow/TableCell wire records. *Why:* already published in ArcForges.Contracts.PublicApi (content.proto) - satisfied, confirmed by direct inspection<br>**contract** [CON.03](contracts.md#task-con-03) — a published wire schema for the EditTransaction/BlockEdit operation list that architecture/contracts/02-local-rpc-operations.md [NO-01](../../../architecture/contracts/02-local-rpc-operations.md#rule-no-01) calls 'the typed notes.commands.v1 edit list'. *Why:* grepped Contracts repo (public/, internal/, src/) for EditTransaction, InsertBlock, notes.commands, NotesCommand, ApplyBlockEdits - zero matches outside this design citation; internal/proto/arcforges/local/notes/v1/notes.proto contains only one placeholder message ('NotesOperationsServiceTrashDocumentValue', explicitly marked 'no product RPC service is registered'). This is a genuinely unmet contract closure, not yet started by the Contracts lane or anyone |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NOTES.35](#task-notes-35) — three-device convergence harness exercises Notes block edits end to end. *Why:* real multi-device convergence can only be proven once Cloud sync ([WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25)) is real; modelled as IM.notes-multi-device-convergence |
| Unblocks | [NOTES.06](#task-notes-06), [NOTES.08](#task-notes-08), [NOTES.10](#task-notes-10), [NOTES.14](#task-notes-14), [NOTES.15](#task-notes-15), [NOTES.19](#task-notes-19), [NOTES.27](#task-notes-27), [NOTES.35](#task-notes-35) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Domain/Blocks/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Domain/Editing/**`<br>`ArcNotes:fixtures/formats/arcnotes/v1/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Domain/Editing/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append), [RES-arcnotes-format-fixtures](../shared-resources.md#res-arcnotes-format-fixtures) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | offline unit tests: command round-trip per block kind, multi-block operation tests, block-identity stability test, transaction-atomicity test, conversion matrix, forward-compatibility test on unknown kinds/marks, clipboard round-trip tests, repository-policy test (no Markdown/HTML/RTF on internal path); AOT compile |
| Completion evidence | write-path/atomicity/conversion-mapping/block-identity-stability results; no-markup-string repository policy test result; per-kind command round-trip and clipboard fidelity results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no Domain project exists; this is the largest single unit of new ArcNotes domain code |
| Notes | Could be further split (block/inline core vs conversion+clipboard) if a single PR proves too large in practice; kept as one task here because the conversion matrix and clipboard both operate over the same closed operation set and block-identity guarantee. |

<a id="task-notes-03"></a>

### NOTES.03 — Editor interaction: caret, selection, IME composition, markdown-friendly input

**Outcome.** The ArcNotes.Desktop editor surface handles grapheme/bidi-correct caret and selection, commits exactly one transaction per IME composition positioned from the real caret rectangle, and supports the closed set of markdown input rules and the slash menu, all built on NOTES.02's EditTransaction model.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-03` and ledger record `ledger/tasks/notes-03.md` in the Plan repository; task branch `task/notes-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-18.01](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.01) — grapheme-correct caret/selection, Unicode word boundaries, bidirectional caret movement, discontiguous selection painting, IME composition as view state (one transaction, never interrupted by concurrent edit), markdown keyboard syntax, slash menu distinct from command palette<br>[WP-18.00](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.00) — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) closure: stable run/atom/cell IDs, NotesTextPosition/NotesCommand, explicit IME conflict preservation, disabled stale undo with original recoverable inverse<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (bottom of file): stable run/atom/cell IDs, NotesTextPosition/NotesCommand, explicit IME conflict preservation, disabled stale undo with original recoverable inverse, no unspecified rebase — package-level obligation contribution |
| Provides | notes.editor.caret-ime; notes.editor.markdown-input |
| Start prerequisites | **artifact** [PLT.27](platform.md#task-plt-27) — published ArcForges.Desktop.Experience / design-system shell package for Avalonia hosting. *Why:* editor surface needs the shared shell; DesktopPlatform's ArcForges.Desktop.Experience/RichContent/Text/Preview projects are currently AssemblyPlaceholder-only, so this is presently unmet as a real artifact (ArcNotes today only depends on raw Avalonia.Desktop directly, not any DesktopPlatform shell package)<br>**artifact** [APP.01](app-composition.md#task-app-01) — the independent-product hosting/composition pattern (how ArcNotes.Desktop is composed as its own process under the shared shell). *Why:* editor UI is hosted inside that composition; [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) is owned by the assistant lanes and its Assistant.Abstractions/Core output is the precedent ArcNotes' own hosting should follow<br>**artifact** [PLT.26](platform.md#task-plt-26) — published design-system tokens and theming. *Why:* the product shell composes the shared tokens |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14), [PLT.56](platform.md#task-plt-56) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes/Editor/**`<br>`ArcNotes:src/ArcForges.ArcNotes/Editor/Ime/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Editor/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit/UI-automation tests: text-correctness corpus (emoji with modifiers, Devanagari, Thai, combining marks), composition-input test per platform (one undo entry, one transaction) plus concurrent-edit-during-composition test, bidi caret/selection-painting test; no live device/GUI E2E in CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | grapheme/bidi correctness and composition-fidelity results per [VF-05](../../../architecture/18-editing-and-rich-content.md#rule-vf-05)/[VF-06](../../../architecture/18-editing-and-rich-content.md#rule-vf-06)/[VF-07](../../../architecture/18-editing-and-rich-content.md#rule-vf-07) of 18-editing-and-rich-content.md |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: current ArcForges.ArcNotes project only has a MainWindow.cs Hello World shell |

<a id="task-notes-04"></a>

### NOTES.04 — Virtualised block layout, measurement caching and scroll anchoring

**Outcome.** A block layout engine realises only the viewport window plus bounded overscan, caches measurement by (blockId, contentFingerprint, availableWidth, fontScale, locale), and anchors scroll position to (blockId, offset) so a remote edit above the viewport never moves the reader.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-04` and ledger record `ledger/tasks/notes-04.md` in the Plan repository; task branch `task/notes-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-18.01](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.01) — virtualised block layout with measurement caching, scroll anchoring to (blockId, offset), bounded nesting, 10000-block scale-corpus responsiveness |
| Provides | notes.editor.virtualised-layout |
| Start prerequisites | **artifact** [PLT.26](platform.md#task-plt-26) — same design-system/shell package as NOTES.03. *Why:* layout engine renders inside the shared shell's control hosting<br>**artifact** [PLT.27](platform.md#task-plt-27) — the published windows, panels and layout package NOTES.03 also hosts on. *Why:* block layout renders inside the shared shell package, not a private host |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14), [NOTES.31](#task-notes-31) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes/Editor/Layout/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Editor/Layout/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append) |
| Validation | offline scale-corpus benchmark fixture committed to the repo; regressions fail the gate per [PF-01](../../../architecture/04-desktop-application-architecture.md#rule-pf-01)/[PF-02](../../../architecture/04-desktop-application-architecture.md#rule-pf-02); no live GUI E2E in CI |
| Completion evidence | 10000-block open-interactive-without-full-measurement result; no-re-measurement-on-scroll-back result; scroll-anchor-above-viewport result |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Split out of [WP-18.01](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.01) from NOTES.03/05 because layout/virtualisation is a distinct performance-engineering skill area that can proceed in parallel once NOTES.02's block model exists, independent of caret/IME work. |

<a id="task-notes-05"></a>

### NOTES.05 — Rich content kinds: code highlighting, math rendering (notes.math.v1), table interaction

**Outcome.** Code blocks highlight from a bounded, statically registered grammar set with graceful plain-text degradation; math blocks render the notes.math.v1 supported grammar subset with an explicit unsupported-construct marker and never execute TeX; table blocks support the interaction set (insert/delete row/column, merge/split-free V1 spans).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-05` and ledger record `ledger/tasks/notes-05.md` in the Plan repository; task branch `task/notes-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-18.01](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.01) — code highlighting from a bounded statically-registered grammar set degrading to plain text; math rendering with explicit unsupported-construct marking; run every notes.math.v1 accepted/unsupported/malformed/depth/length vector |
| Provides | notes.editor.rich-content-kinds |
| Start prerequisites | **artifact** [PLT.27](platform.md#task-plt-27) — same shell package as NOTES.03/04. *Why:* rendering surfaces host inside the shared shell |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes/Editor/RichContent/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Editor/RichContent/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append) |
| Validation | offline unit tests running every notes.math.v1 accepted/unsupported/malformed/depth/length vector from 26-product-behavior-profiles.md; code-highlighting degrades off-UI-thread; no live GUI E2E |
| Completion evidence | unsupported-math-construct-renders-as-source-with-marker result; code-block plain-text-degradation result; table-shape clipboard round-trip cross-check with NOTES.02 |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-06"></a>

### NOTES.06 — Links, backlinks and outline over the canonical block store

**Outcome.** Document and block links target stable identities with optional alias; a derived link_index produces the backlinks panel and outline; renaming never breaks a link; a broken link has an explicit state.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-06` and ledger record `ledger/tasks/notes-06.md` in the Plan repository; task branch `task/notes-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-18.02](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.02) — full |
| Provides | notes.link-index; notes.backlinks; notes.outline |
| Start prerequisites | **artifact** [NOTES.01](#task-notes-01) — notebook/document identity. *Why:* links target DocumentId/BlockId<br>**artifact** [NOTES.02](#task-notes-02) — Block/BlockId model. *Why:* block links target stable BlockId |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14), [NOTES.19](#task-notes-19) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Domain/Links/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Domain/Links/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit tests: rename-preserves-link, index rebuild from scratch, broken-link state test, structural test asserting backlinks absent from stored content |
| Completion evidence | link/backlink/index-rebuild results per [WP-18.02](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.02) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-07"></a>

### NOTES.07 — Document-level typed properties and tags (basic)

**Outcome.** System/user property separation, missing/empty/false/zero distinction, decimal/date/offset validation, label rename vs refused dependent type change, tag cross-cutting classification whose deletion never deletes documents, and plain notes with zero property overhead.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-07` and ledger record `ledger/tasks/notes-07.md` in the Plan repository; task branch `task/notes-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-18.03](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.03) — full<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) S8 additional completion requirement: property types and persistence agree with the frozen query profile; no local culture defaults affect stored meaning — package-level obligation contribution |
| Provides | notes.property-store.basic; notes.tags |
| Start prerequisites | **artifact** [NOTES.01](#task-notes-01) — Document aggregate. *Why:* properties attach to documents<br>**contract** [CON.91](contracts.md#task-con-91) — PropertyDefinition, PropertyValue, ScalarValue, SelectOption wire records and their constraint sidecars (constraints.json rules propertyDefinition/scalarValue). *Why:* already published in ArcForges.Contracts.PublicApi and its validation sidecar - confirmed present; satisfied edge |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14), [NOTES.16](#task-notes-16), [NOTES.18](#task-notes-18), [NOTES.23](#task-notes-23) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Domain/Properties/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Domain/Tags/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Domain/Properties/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit tests: type validation per property kind, tag-deletion-survives-documents test, default-experience (no-properties) test |
| Completion evidence | property typing and tag-deletion results per [WP-18.03](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.03) completion gate |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This is the basic document-level property model only; the full typed query/view package (8 scalar kinds incl. relation/derived exclusion, notes.scalar.v1 query evaluator) is [WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28), tasks NOTES.23/24. |

<a id="task-notes-08"></a>

### NOTES.08 — Managed and external attachments (non-PDF): storage, availability, preview levels 1-2

**Outcome.** Managed attachments enter the managed resource store with content-hash identity; external references record location+availability; small drags default to managed, large/external prompt; image preview decodes off-thread bounded with EXIF applied; every preview degradation states its reason; no preview path performs a network fetch.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-08` and ledger record `ledger/tasks/notes-08.md` in the Plan repository; task branch `task/notes-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-18.04](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.04) — managed/external attachment classification, availability states, metadata-card and thin-preview levels for images/files, bounded off-thread image decode with EXIF orientation, no-embedding structural test, malformed-input degradation for images, egress test (no preview path fetches a remote resource)<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) S8 additional completion requirement: content paths pass the stated content-origin vectors, including unknown input and failed publication — package-level obligation contribution |
| Provides | notes.attachments.non-pdf |
| Start prerequisites | **artifact** [PLT.05](platform.md#task-plt-05) — managed_resource / resource_reference tables (content-addressed blob store) from the persistence foundation. *Why:* attachments enter the same managed resource store data-model 02 S1.6 defines<br>**artifact** [NOTES.02](#task-notes-02) — attachment block kind (image/attachment BlockBody variants). *Why:* attachments are referenced from blocks |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Infrastructure/Attachments/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Attachments/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit tests: managed round-trip with integrity, reference-unavailable behaviour, malformed-image corpus asserting placeholder+reason+no crash, egress test |
| Completion evidence | attachment integrity, no-embedding, malformed-input degradation and preview-egress results (image/file portion only; PDF portion is NOTES.09) |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Deliberately split from the PDF viewer (NOTES.09) so ordinary attachment handling does not wait on the native PDFium wrapper, which does not exist yet anywhere in DesktopPlatform - this is the aggregate-producer-gate pattern the delivery model avoids. |

<a id="task-notes-09"></a>

### NOTES.09 — PDF in-product viewer, page anchors and native parser isolation

**Outcome.** PDF attachments render through the in-product viewer with (attachmentContentHash, pageIndex, rectOrTextRange) page anchors, all parsing routed through ContentSandbox, and a real native-parser-crash test proving the parent process survives with a metadata-card fallback.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-09` and ledger record `ledger/tasks/notes-09.md` in the Plan repository; task branch `task/notes-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L · early risk proof |
| Obligations | [WP-18.04](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.04) — PDF viewer (pdfViewer attachment presentation), page-anchored annotation targets, citation anchors, routing hostile PDF parsing through [WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09) ContentSandbox, [PG-12](../../../assurance/open-gates-register.md#rule-pg-12) completion, PDF-specific malformed-input containment |
| Provides | notes.attachments.pdf-viewer |
| Start prerequisites | **artifact** [PLT.45](platform.md#task-plt-45) — the restricted fixture-parser ContentSandbox runtime (host, protocol, launch mechanics). *Why:* [WP-11](../../work-packages/11-security-foundation.md#rule-wp-11) owns ContentSandbox host/protocol/launch and publishes a real restricted fixture-parser runtime per producer-artifacts-and-integration.md; DesktopPlatform's ArcForges.ContentSandbox project currently only has a literal Hello World Program.cs, so even this fixture boundary is not yet built<br>**artifact** [NAT.06](native.md#task-nat-06) — the functional native ABI 1.1 (architecture/contracts/06-native-functional-abi.md) that DesktopPlatform's Native.* wrappers implement. *Why:* PDF wrapper must follow the same C ABI discipline as the existing probe-level Media/Colour/Image/Otio wrappers (MediaAbi.cs pattern: GetAbiVersion/GetBuildInfo/GetLastError over LibraryImport) |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NAT.14](native.md#task-nat-14) — a real, packaged ArcForges.Native.Pdf (PDFium) wrapper with build/licence inventory and hostile-input containment evidence, equivalent to the 13.13 production-parser-composition step described for ContentSandbox. *Why:* no ArcForges.Native.Pdf project exists anywhere in DesktopPlatform as of fe8476d (confirmed: only Media/Colour/Image/Otio Native projects and their win-x64 runtimes exist, each still probe-level - version/build-info/error only, no decode functions); [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22) explicitly require this real artifact and state 'a metadata fallback does not close that delivery gate' |
| Unblocks | [NOTES.14](#task-notes-14), [NOTES.37](#task-notes-37) |
| Permitted substitutes | [SUB-notes-pdf-fixture-parser](../substitutes.md#sub-notes-pdf-fixture-parser) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Infrastructure/Attachments/Pdf/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Attachments/Pdf/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append) |
| Validation | offline unit tests against the fixture parser now; real hostile-input containment test deferred to IM.notes-pdf-native-integration; no live GUI E2E in CI |
| Completion evidence | real native-parser-crash/hang-survival-with-metadata-card result; page-anchor survive-reopen result; [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22) evidence once the real [WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13) artifact lands |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: grepped DesktopPlatform for 'pdf' (case-insensitive) - zero results anywhere in src/ |
| Notes | Flagged as an early risk proof because [AT-05](../../../architecture/01-solution-and-project-layout.md#rule-at-05) (PDF first-class attachment) cannot be met by a metadata fallback per [PD-07](../../../architecture/18-editing-and-rich-content.md#rule-pd-07), and the native dependency chain ([WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09) -> [WP-13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13)) is currently the least-built part of the whole Notes surface - worth surfacing early rather than discovering it late. |

<a id="task-notes-10"></a>

### NOTES.10 — Undo, history, checkpoint and trash as four distinct mechanisms

**Outcome.** Session undo (composite grouping, selection-restoring, coalescing boundaries, agent-edit attribution, remote-change rebase-never-retarget), document history, explicit checkpoints and trash-with-restore exist as four independently behaving mechanisms, none substituting for another.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-10` and ledger record `ledger/tasks/notes-10.md` in the Plan repository; task branch `task/notes-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-18.05](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.05) — full<br>[WP-18.00](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.00) — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) closure: disabled stale undo with original recoverable inverse, no unspecified rebase (undo portion)<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (bottom of file): stable run/atom/cell IDs, NotesTextPosition/NotesCommand, explicit IME conflict preservation, disabled stale undo with original recoverable inverse, no unspecified rebase — package-level obligation contribution |
| Provides | notes.undo; notes.history; notes.checkpoint; notes.trash |
| Start prerequisites | **artifact** [NOTES.02](#task-notes-02) — EditTransaction computed inverses. *Why:* undo is built directly on the inverse each transaction already computes |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14), [NOTES.35](#task-notes-35) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Application/Undo/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Application/History/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Application/Undo/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit tests: distinction matrix, restore-from-trash, checkpoint restore, undo-is-not-crash-recovery test, undo-selection test, coalescing-boundary test, agent-edit undo/attribution test, rebase test |
| Completion evidence | four-mechanism distinction matrix, undo-selection and undo-rebase results per [WP-18.05](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.05) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-11"></a>

### NOTES.11 — Crash recovery and upgrade/downgrade migration

**Outcome.** Kill-during-edit/migration and corrupted-tail recovery reach the last committed boundary with explicit loss reporting; migration from every prior schema version preserves semantics against golden fixtures; downgrade is defined (reverse migration or clean refusal).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-11` and ledger record `ledger/tasks/notes-11.md` in the Plan repository; task branch `task/notes-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-18.06](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.06) — full |
| Provides | notes.recovery; notes.migration |
| Start prerequisites | **artifact** [PLT.02](platform.md#task-plt-02) — the journal/recovery pipeline and StorageSchemaVersion migration apparatus. *Why:* Notes-specific recovery/migration is built directly on the platform-owned journal replay and migration-ordering mechanics (06-data-persistence-and-formats.md S9)<br>**artifact** [PLT.03](platform.md#task-plt-03) — real snapshot and crash/corruption recovery. *Why:* crash recovery restores through the platform recovery pipeline<br>**artifact** [PLT.04](platform.md#task-plt-04) — the real migration runner and StorageSchemaVersion apparatus. *Why:* upgrade and downgrade migration run through the platform migration runner |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14), [NOTES.29](#task-notes-29) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Infrastructure/Migrations/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Recovery/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit tests: kill-during-edit, kill-during-migration, corrupted-tail recovery, migration-from-every-fixture with semantic comparison, downgrade-refusal test |
| Completion evidence | recovery matrix and migration semantic-comparison results per [WP-18.06](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.06) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-12"></a>

### NOTES.12 — ArcNotes capability surface registration

**Outcome.** ArcNotes registers query/read/create/edit/artifact-production capabilities each with risk level, side-effect class, reversibility and approval posture; owner-side validation refuses regardless of caller assertion.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-12` and ledger record `ledger/tasks/notes-12.md` in the Plan repository; task branch `task/notes-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-18.07](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.07) — full |
| Provides | notes.capability-surface |
| Start prerequisites | **artifact** [PLT.18](platform.md#task-plt-18) — the Platform capability/resource contribution model (capability/extension descriptor package). *Why:* capability registration follows the generic contribution model [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09) defines; DesktopPlatform has no such published package consumed by ArcNotes yet<br>**contract** [CON.91](contracts.md#task-con-91) — CapabilityArguments, CapabilityResult, ToolProposal, ToolResult wire records. *Why:* already published in content.proto - satisfied |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.05](harness.md#task-har-05), [NOTES.14](#task-notes-14) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.AssistantIntegration/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/AssistantIntegration/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit tests: capability descriptor validation, owner-side refusal tests, idempotency test per write capability |
| Completion evidence | capability descriptor and owner-side refusal results per [WP-18.07](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.07) completion gate |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Sequenced after NOTES.01/02/06/07/08 conceptually (it exposes their operations) but the registry scaffolding itself can start as soon as [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09) is available; individual descriptor entries land with their owning feature task. |

<a id="task-notes-13"></a>

### NOTES.13 — ArcNotes reference-matrix drift check (AFFiNE/SiYuan)

**Outcome.** A drift report compares the bound AFFiNE (81df4751a3) and SiYuan (eef105683) commits against their current upstream state, assesses any newly introduced material against accepted ArcNotes scope, and re-verifies the AFFiNE licence split (packages/backend, packages/common/native remain proprietary).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-13` and ledger record `ledger/tasks/notes-13.md` in the Plan repository; task branch `task/notes-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / S |
| Obligations | [WP-18.08](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.08) — full |
| Provides | notes.reference-drift-report |
| Start prerequisites | none |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.14](#task-notes-14) |
| Write scope | `ArcNotes:docs/reference-drift/arcnotes-affine-siyuan.md` |
| Validation | documentation/evidence task only; no product build required beyond reading the two reference trees' current state and licence files |
| Completion evidence | drift report listing changed rows, new material with assessment, and licence re-confirmation, per [WP-18.08](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.08) completion gate |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: the underlying matrix (docs/assurance/reference-coverage/arcnotes-affine-siyuan.md) is complete and closed - 41 rows, 0 unresolved, per its own S5 completeness check; this task is maintenance only, not a re-audit |
| Notes | No code dependency; can run at any time, fully in parallel with every other NOTES task. Explicitly NOT a baseline audit - [PG-01](../../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../../assurance/open-gates-register.md#rule-f-013) were already closed pre-package. |

<a id="task-notes-14"></a>

### NOTES.14 — Owned-artifact and real-integration verification

**Outcome.** Independent editor/store/recovery fixtures, helper isolation and content-origin/attachment checks are recorded against the real staged artifacts consumed at this point; the package is not signed off while any contract/owner/recovery rule still needs design during coding.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-14` and ledger record `ledger/tasks/notes-14.md` in the Plan repository; task branch `task/notes-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-18.90](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.90) — all work except the parts mapped to NOTES.02<br>[WP-18.00](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.00) — final-review paragraph: independent verification of 02-desktop-data-model; scalar-definition fixtures follow the fixed profile<br>[WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) Final-review paragraph (S5, before 18.90): independent verification of 02-desktop-data-model; typed structural outbox entries; multi-root local tokens; complete move classification mapping/preview; offline create->move->edit and crash-before/after-acknowledgement test; scalar-definition fixtures follow the fixed profile ([WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) repeats with real property/view UI) — package-level obligation contribution |
| Provides | notes.wp18-closure-receipt |
| Start prerequisites | **artifact** [NOTES.01](#task-notes-01) — own-lane completion. *Why:* gate covers the whole [WP-18](../../work-packages/18-arcnotes-document-core.md#rule-wp-18) surface<br>**artifact** [NOTES.02](#task-notes-02) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.03](#task-notes-03) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.04](#task-notes-04) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.05](#task-notes-05) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.06](#task-notes-06) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.07](#task-notes-07) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.08](#task-notes-08) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.09](#task-notes-09) — own-lane completion (fixture-parser scope only; real PDFium is separately tracked). *Why:* see above<br>**artifact** [NOTES.10](#task-notes-10) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.11](#task-notes-11) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.12](#task-notes-12) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.13](#task-notes-13) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.01](release.md#task-rel-01) |
| Write scope | `ArcNotes:docs/release-notes.md`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Integration/Wp18/**` |
| Validation | offline initial-state matrix rows applicable to this product (fresh shell, hydrated outage, unavailable content, signout, restart); no macOS/hosted-runtime CI |
| Completion evidence | owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations, real-vs-fixture status per [WP-18.90](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.90) |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-15"></a>

### NOTES.15 — Local full-text index over hydrated content

**Outcome.** An incremental FTS index over document/block content, properties, tags and attachment-extracted text follows the write path, never diverges after a crash, rebuilds fully from canonical data, and meets query latency budget on the scale corpus.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-15` and ledger record `ledger/tasks/notes-15.md` in the Plan repository; task branch `task/notes-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L · early risk proof |
| Obligations | [WP-19.00](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.00) — full |
| Provides | notes.fts-index |
| Start prerequisites | **artifact** [NOTES.02](#task-notes-02) — block content to index. *Why:* index source<br>**artifact** [PLT.07](platform.md#task-plt-07) — journal-driven derived-store update pattern (data-model 03 S1: [DS-01](../../../architecture/06-data-persistence-and-formats.md#rule-ds-01)..[DS-07](../../../architecture/data-model/03-derived-stores.md#rule-ds-07)). *Why:* index updates must be published only when the source-version token still matches, per the derived-store contract |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.16](#task-notes-16), [NOTES.17](#task-notes-17), [NOTES.22](#task-notes-22) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Search/Index/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Search/Index/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit tests: divergence test after crash mid-index-update, full-rebuild-equivalence test, latency measurement against the scale corpus |
| Completion evidence | index divergence, rebuild-equivalence and latency results per [WP-19.00](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.00) completion gate |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | implementation-sequence.md S3's 'What may be mocked' table explicitly lists 'Local full-text indexing and citation anchors' under 'Must be real early' (Cloud search may be mocked, this may not) - flagged as an early risk proof accordingly. |

<a id="task-notes-16"></a>

### NOTES.16 — Query, ranking and permission over the local index

**Outcome.** Query supports text/property/tag/structural filters with explainable basic ranking; permission is applied during evaluation so a refused document never influences results or counts, including bounded notes.scalar.v1 predicates on the local hydrated path.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-16` and ledger record `ledger/tasks/notes-16.md` in the Plan repository; task branch `task/notes-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-19.01](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.01) — full |
| Provides | notes.search.query |
| Start prerequisites | **artifact** [NOTES.15](#task-notes-15) — the FTS index to query. *Why:* direct dependency<br>**artifact** [NOTES.07](#task-notes-07) — property/tag store. *Why:* property and tag filters query this store |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.18](#task-notes-18), [NOTES.22](#task-notes-22), [NOTES.24](#task-notes-24) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Search/Query/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Search/Query/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit tests: filter coverage tests, permission test (refused content invisible in results and counts), ranking stability test |
| Completion evidence | filter/permission/ranking results per [WP-19.01](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.01) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-17"></a>

### NOTES.17 — Citation anchors

**Outcome.** search_anchor rows (block_id, offset range, content_fingerprint) survive insert/delete/reorder/reparent edits where the cited content still exists, and report invalidity explicitly rather than drifting.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-17` and ledger record `ledger/tasks/notes-17.md` in the Plan repository; task branch `task/notes-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M · early risk proof |
| Obligations | [WP-19.02](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.02) — full |
| Provides | notes.citation-anchor |
| Start prerequisites | **artifact** [NOTES.15](#task-notes-15) — search index/derived-store plumbing. *Why:* anchors live alongside search_document rows |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.22](#task-notes-22) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Search/Anchors/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Search/Anchors/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append) |
| Validation | offline unit tests: anchor survival across insert/delete/reorder/reparent, explicit-invalid test after content removal |
| Completion evidence | anchor survival and invalidity results per [WP-19.02](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.02) completion gate |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Also covered by the 'must be real early' scaffolding table entry for citation anchors (see NOTES.15). |

<a id="task-notes-18"></a>

### NOTES.18 — Saved views (list projection only)

**Outcome.** A saved_view row (notebook scope, query profile, semantic-definition bindings, view revision) produces a list projection; deleting a view never deletes content; results always reflect current data. Full typed query/table delivery is explicitly NOT emulated here - it is [WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) (NOTES.24/26).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-18` and ledger record `ledger/tasks/notes-18.md` in the Plan repository; task branch `task/notes-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-19.03](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.03) — full - eq/ne/isMissing/isPresent for all declared scalar kinds, all/any/not composition, DocumentId ordering under the profile bounds; later value operators and property sorting explicitly unavailable until [WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28)<br>[WP-19](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19) S8 additional completion requirement: the initial view stores the final profile/bindings; neither invents a temporary semantic profile nor claims full table/query delivery before [WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) — package-level obligation contribution |
| Provides | notes.saved-view.list |
| Start prerequisites | **artifact** [NOTES.16](#task-notes-16) — query evaluation. *Why:* a saved view is a saved query<br>**artifact** [NOTES.07](#task-notes-07) — property definitions. *Why:* filters reference declared properties<br>**contract** [CON.91](contracts.md#task-con-91) — SavedViewRecord, NotesQuery, NotesFilter, ScalarPredicate wire records. *Why:* already published in content.proto - satisfied |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.22](#task-notes-22), [NOTES.26](#task-notes-26) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Search/SavedViews/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/Search/SavedViews/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit tests: ownership test (deletion non-destructive), re-evaluation test (results reflect current content) |
| Completion evidence | saved-view ownership and freshness results per [WP-19.03](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.03) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-19"></a>

### NOTES.19 — Non-destructive Markdown/plain-text import (incl. Obsidian-style folders)

**Outcome.** Import from Markdown/plain-text sources (including an Obsidian-style vault layout) produces a reviewable import plan then a report of created/transformed/skipped items; the source is never modified; a partial failure leaves a coherent result and clear report.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-19` and ledger record `ledger/tasks/notes-19.md` in the Plan repository; task branch `task/notes-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-19.04](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.04) — full |
| Provides | notes.import.markdown |
| Start prerequisites | **artifact** [NOTES.01](#task-notes-01) — notebook/document placement. *Why:* import creates ordinary documents<br>**artifact** [NOTES.02](#task-notes-02) — EditTransaction write path (origin=import). *Why:* import applies through the same single write path<br>**artifact** [NOTES.06](#task-notes-06) — link resolution. *Why:* relative links in imported Markdown resolve through the link model |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.22](#task-notes-22) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.ImportExport/Import/**`<br>`ArcNotes:fixtures/formats/import/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Import/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append), [RES-arcnotes-format-fixtures](../shared-resources.md#res-arcnotes-format-fixtures) (append) |
| Validation | offline unit/integration tests: import from every declared source fixture, source-immutability assertion, induced-failure test asserting coherent partial result with report |
| Completion evidence | per-source import results, immutability assertion, partial-failure report per [WP-19.04](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.04) completion gate; this is ArcNotes' [PG-07](../../../assurance/open-gates-register.md#rule-pg-07) contribution (import fixture obligation, not export) |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | No native/ContentSandbox dependency - Markdown/plain-text parsing is managed-code text parsing, unlike PDF/image attachments. |

<a id="task-notes-20"></a>

### NOTES.20 — Cloud Notes export client and its named fixture endpoint

**Outcome.** The Notes Cloud-export client builds a snapshot request over acknowledged revisions and validates the returned Markdown/attachments/metadata/fidelity-report shape against a named, registered fixture endpoint; the client itself is real and complete, only the server side is a fixture.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-20` and ledger record `ledger/tasks/notes-20.md` in the Plan repository; task branch `task/notes-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-19.05](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05) — full - client-side export flow, fidelity manifest, offline-refuses-new-export-without-losing-drafts behaviour<br>[WP-19](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19) S6 Impacts: no Notes printing/PDF-export feature is added — package-level obligation contribution |
| Provides | notes.cloud-export-client |
| Start prerequisites | **artifact** [NOTES.01](#task-notes-01) — acknowledged-revision snapshot source. *Why:* export snapshots acknowledged document/notebook state<br>**contract** [CON.91](contracts.md#task-con-91) — ArtifactRef and ExportRequest-shaped wire records (INotesOperations.ExportAsync returns ArtifactRef per architecture/contracts/02-local-rpc-operations.md). *Why:* ArtifactRef already exists in the published contract set (seen referenced from ToolResult.artifacts); satisfied for the reference shape<br>**contract** [CON.20](contracts.md#task-con-20) — published notes.requestExport and export records. *Why:* the ArcNotes export client calls the generated operation |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.45](cloud.md#task-cloud-45) — the real Cloud Notes export producer (bounded leased export job, acknowledged-revision manifest, verified expiring download artifact). *Why:* [WP-19.05](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05)'s own text: 'Use the registered export fixture at this early stage; WP25.08 supplies the real Cloud export join' - modelled as IM.notes-cloud-export |
| Unblocks | [NOTES.22](#task-notes-22), [NOTES.30](#task-notes-30), [NOTES.33](#task-notes-33) |
| Permitted substitutes | [SUB-notes-cloud-export](../substitutes.md#sub-notes-cloud-export) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.ImportExport/Export/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Export/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit/integration tests against the named fixture: acknowledged-source snapshot identity, attachment hashes, metadata/link fidelity, complete loss entries; Cloud-unavailable-refuses-new-export test; no live Cloud call in this task's own CI |
| Completion evidence | Cloud export content, attachment-hash, link-manifest and fidelity results (against the fixture) per [WP-19.05](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05) completion gate; real producer evidence recorded separately at [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08)/IM.notes-cloud-export |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This task must register its fixture endpoint in a way IM.notes-cloud-export can structurally assert was removed (implementation-sequence.md [TS-01](../../implementation-sequence.md#rule-ts-01)/[TS-02](../../implementation-sequence.md#rule-ts-02): 'scaffolding is deleted, never adapted'; the deleting package is [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08), owned by the Cloud lane, so ArcNotes' obligation is to make the fixture registration a single removable seam). |

<a id="task-notes-21"></a>

### NOTES.21 — Repository-projection prohibition (structural assertion)

**Outcome.** A dependency-policy test fails the build on any Git or LFS client package reference from any ArcNotes project; a structural test asserts no type implements or is named as a projection writer; the exclusion is explained in the product UI rather than merely absent.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-21` and ledger record `ledger/tasks/notes-21.md` in the Plan repository; task branch `task/notes-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / S |
| Obligations | [WP-19.06](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.06) — full |
| Provides | notes.no-repository-projection |
| Start prerequisites | **artifact** [GOV.03](governance.md#task-gov-03) — the dependency-policy analyzer infrastructure. *Why:* ArcNotes already consumes eng/policy/dependency-policy.json and DependencyPolicy.cs today (confirmed present in eng/ArcForges.Repository) - this need is already satisfied |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.22](#task-notes-22) |
| Write scope | `ArcNotes:eng/policy/dependency-policy.json`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests/DependencyPolicyTests.cs` |
| Validation | offline static/dependency-policy test only |
| Completion evidence | dependency-policy, structural and presentation results proving no repository-projection or Git/LFS path exists, per [WP-19.06](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.06) completion gate |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DependencyPolicyTests.cs already exists as a Hello-World-era policy test in tests/ArcForges.ArcNotes.Tests - this task extends that existing mechanism rather than inventing a new one |
| Notes | Can run essentially any time in parallel; minimal real dependency since the governance tooling it extends already exists in the repo. |

<a id="task-notes-22"></a>

### NOTES.22 — Owned-artifact and real-integration verification

**Outcome.** Independent import/search/export and missing-resource outcomes are recorded; public value profiles and owner authorization remain compatible; no Git mirror, DOCX or newly invented export suite exists.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-22` and ledger record `ledger/tasks/notes-22.md` in the Plan repository; task branch `task/notes-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-19](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-19.90](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.90) — full |
| Provides | notes.wp19-closure-receipt |
| Start prerequisites | **artifact** [NOTES.15](#task-notes-15) — own-lane completion. *Why:* gate covers the whole [WP-19](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19) surface<br>**artifact** [NOTES.16](#task-notes-16) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.17](#task-notes-17) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.18](#task-notes-18) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.19](#task-notes-19) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.20](#task-notes-20) — own-lane completion (fixture scope). *Why:* see above<br>**artifact** [NOTES.21](#task-notes-21) — own-lane completion. *Why:* see above |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.01](release.md#task-rel-01) |
| Write scope | `ArcNotes:tests/ArcForges.ArcNotes.Tests/Integration/Wp19/**` |
| Validation | offline initial-state matrix rows applicable to this product; no macOS/hosted-runtime CI |
| Completion evidence | owned artifact and real-integration receipt per [WP-19.90](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.90) |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-23"></a>

### NOTES.23 — Typed property schemas: full bounded scalar set

**Outcome.** Property definitions cover text, number, date, dateTime, single-select, multi-select, checkbox, URL with exact notes.scalar.v1 encodings; relation and derived are structurally excluded (no join engine, no formula evaluator); a full lifecycle (create/rename/type-change-with-preview/delete) is enforced with no silent data loss.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-23` and ledger record `ledger/tasks/notes-23.md` in the Plan repository; task branch `task/notes-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-28.00](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.00) — full - all eight declared scalar kinds/config bounds/exact encodings; rename preserves semantic bindings; dependent type/option changes refused after preview; trashed definitions make views visibly invalid<br>[WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) Final-review paragraph (S5, before 28.90): independent verification of 04-protobuf-wire-registry; cross-notebook move with real scalar definitions/select options/tags - stale target semantics, incomplete mapping and conflicting destination mappings refuse atomically; explicit approved removals remain in history — package-level obligation contribution |
| Provides | notes.property-store.full |
| Start prerequisites | **artifact** [NOTES.07](#task-notes-07) — the basic document-level property model this extends. *Why:* same aggregate, extended schema depth<br>**contract** [CON.91](contracts.md#task-con-91) — PropertyDefinition.type/profile/numberScale/semanticRevision fields and the notesQuery/scalarPredicate/scalarValue constraint rules. *Why:* already published (content.proto + constraints.json) - satisfied |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.24](#task-notes-24), [NOTES.28](#task-notes-28), [NOTES.29](#task-notes-29), [NOTES.30](#task-notes-30), [NOTES.32](#task-notes-32) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Database/Properties/**`<br>`ArcNotes:fixtures/formats/arcnotes/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Properties/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-format-fixtures](../shared-resources.md#res-arcnotes-format-fixtures) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit/integration tests: type validation per kind, rename-preserves-values test, type-change-stated-behaviour test, deletion-stated-consequence test |
| Completion evidence | property lifecycle results with no silent loss per [WP-28.00](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.00) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-24"></a>

### NOTES.24 — Query model: local evaluator and notes.scalar.v1 conformance fixtures

**Outcome.** A local query evaluator over properties/tags/links/content/structure implements notes.scalar.v1 exactly (operators, missing/isMissing/isPresent semantics, AST bounds, stable sort with DocumentId tiebreak, dataset-token pagination) with permission applied during evaluation and stability under concurrent mutation, proven against a committed fixture-vector suite usable by both native and Cloud evaluators.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-24` and ledger record `ledger/tasks/notes-24.md` in the Plan repository; task branch `task/notes-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-28.01](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.01) — local evaluator + fixture-based conformance suite covering every v1 operator, boolean/missing behaviour, AST limit, ordinal/decimal/instant comparison, signed dataset-bound pagination<br>[WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) S8 additional completion requirement: every scalar/query/profile vector passes on both owners; all supported list/table operations implemented without new product design choices — package-level obligation contribution |
| Provides | notes.query-evaluator.local |
| Start prerequisites | **artifact** [NOTES.23](#task-notes-23) — full property schema. *Why:* query predicates reference typed properties<br>**artifact** [NOTES.16](#task-notes-16) — the existing local query/permission plumbing from [WP-19.01](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.01). *Why:* [WP-28.01](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.01) extends rather than replaces it<br>**contract** [CON.91](contracts.md#task-con-91) — the complete notes.scalar.v1 wire vocabulary (ScalarPredicate, ScalarValue, NotesQuery, NotesFilter, FilterGroup, NotesSort, PageRequest) and its constraints.json AST-bound rules. *Why:* already published and validated - satisfied; this is the strongest-specified contract surface Notes consumes |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NOTES.34](#task-notes-34) — cross-evaluator conformance against the real Cloud (D1-backed) evaluator. *Why:* producer-artifacts-and-integration.md row 28 states 'Numerical/format vectors independent; no mock Cloud acceptance' - the local conformance suite can be built and proven against fixtures alone, but final acceptance explicitly forbids a mock standing in for the real Cloud evaluator |
| Unblocks | [NOTES.26](#task-notes-26), [NOTES.32](#task-notes-32), [NOTES.34](#task-notes-34) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Database/Query/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Query/**` |
| Shared resources | [RES-notes-scalar-vectors](../shared-resources.md#res-notes-scalar-vectors) (append) |
| Validation | offline unit/integration tests: predicate coverage, permission test, stability-under-concurrent-mutation test; the fixture vectors from arcnotes.md S7.1 acceptance-vectors paragraph (D1 to D4 ordering, ne semantics, numeric/checkbox/offset equality) run without any live Cloud dependency |
| Completion evidence | query permission and stability results per [WP-28.01](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.01) completion gate (local portion); cross-evaluator match is IM.notes-cloud-query-conformance's evidence |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This is the clearest example in this area of the 'aggregate producer gate' pattern to avoid: [WP-28.01](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.01)'s text bundles the local evaluator and the Cloud cross-check into one substep, but only the cross-check genuinely needs a real Cloud artifact. Modelled as one local task (NOTES.24) plus a separate integration proposal (IM.notes-cloud-query-conformance) rather than making the whole substep wait. |

<a id="task-notes-26"></a>

### NOTES.26 — View kinds: list and table projections

**Outcome.** Table and list views project the same NOTES.24 query with identical ordering (missing last, ascending DocumentId tiebreak); switching kinds preserves the query; deleting a view destroys no content. Board/gallery/calendar/timeline are structurally absent, not merely unimplemented.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-26` and ledger record `ledger/tasks/notes-26.md` in the Plan repository; task branch `task/notes-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-28.02](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.02) — full - list/table projections with visible-properties/sorting/filtering configuration, D1 to D4/numeric/checkbox/offset/equal-key/mutation-restart vectors, kind-switch preserves query<br>[WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) S8 additional completion requirement: every scalar/query/profile vector passes on both owners; all supported list/table operations implemented without new product design choices — package-level obligation contribution |
| Provides | notes.view.list-table |
| Start prerequisites | **artifact** [NOTES.24](#task-notes-24) — the query evaluator. *Why:* a view is a projection over a query<br>**artifact** [NOTES.18](#task-notes-18) — the [WP-19.03](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.03) saved-view list projection this extends to table+full filter/sort depth. *Why:* same saved_view aggregate, extended |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.27](#task-notes-27), [NOTES.29](#task-notes-29), [NOTES.30](#task-notes-30), [NOTES.31](#task-notes-31), [NOTES.32](#task-notes-32) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Database/Views/**`<br>`ArcNotes:src/ArcForges.ArcNotes.Presentation/Views/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Views/**` |
| Shared resources | [RES-arcnotes-build-config](../shared-resources.md#res-arcnotes-build-config) (append), [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | offline unit/integration tests: per-kind rendering/interaction tests, kind-switch-preserves-query test, ownership test |
| Completion evidence | per-kind projection, switch and ownership results per [WP-28.02](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.02) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-27"></a>

### NOTES.27 — Editing through a view

**Outcome.** Property values are editable directly in a view, going through the same EditTransaction write path (SetProperty) as document editing, with full validation and permission - never a shortcut.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-27` and ledger record `ledger/tasks/notes-27.md` in the Plan repository; task branch `task/notes-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-28.03](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.03) — full |
| Provides | notes.view-editing |
| Start prerequisites | **artifact** [NOTES.26](#task-notes-26) — the view surface to edit through. *Why:* direct dependency<br>**artifact** [NOTES.02](#task-notes-02) — the single EditTransaction write path (SetProperty operation). *Why:* view edits must reuse this exact path, never bypass it |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.32](#task-notes-32) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Presentation/Views/Editing/**`<br>`ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Views/Editing/**` |
| Validation | offline unit tests: write-path assertion, validation test, permission test |
| Completion evidence | view-edit write-path, validation and permission results per [WP-28.03](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.03) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-28"></a>

### NOTES.28 — Lightness preservation for plain notes

**Outcome.** A plain note with no properties carries no property panel, no schema, no measurable performance cost; the property system is opt-in per document and per collection.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-28` and ledger record `ledger/tasks/notes-28.md` in the Plan repository; task branch `task/notes-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / S |
| Obligations | [WP-28.04](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.04) — full |
| Provides | notes.lightness-guarantee |
| Start prerequisites | **artifact** [NOTES.23](#task-notes-23) — the property schema whose absence is being proven cost-free. *Why:* direct dependency |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.32](#task-notes-32) |
| Write scope | `ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Lightness/**` |
| Validation | offline unit test: default-experience assertion (new note requires nothing) plus a performance comparison asserting no regression for property-free documents |
| Completion evidence | lightness default and performance comparison per [WP-28.04](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.04) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-29"></a>

### NOTES.29 — Supported-schema migration for property/view data (local)

**Outcome.** Every actually-shipped scalar-property/list/table schema version upgrades preserving stable IDs and additive unknown fields, with no canvas-era or invented historical fixture.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-29` and ledger record `ledger/tasks/notes-29.md` in the Plan repository; task branch `task/notes-29` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05) — supported-schema migration: actual shipped scalar-property/list/table schemas migrate preserving stable IDs and additive fields; reading additive unknown fields |
| Provides | notes.schema-migration |
| Start prerequisites | **artifact** [NOTES.11](#task-notes-11) — the migration framework this extends to property/view tables. *Why:* same mechanism, new tables<br>**artifact** [NOTES.23](#task-notes-23) — the schemas being migrated. *Why:* direct dependency<br>**artifact** [NOTES.26](#task-notes-26) — the view schemas being migrated. *Why:* direct dependency |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.32](#task-notes-32) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.Infrastructure/Migrations/**`<br>`ArcNotes:fixtures/formats/arcnotes/**` |
| Shared resources | [RES-arcnotes-format-fixtures](../shared-resources.md#res-arcnotes-format-fixtures) (append), [RES-arcnotes-migrations](../shared-resources.md#res-arcnotes-migrations) (append) |
| Validation | offline unit tests: upgrade every historical supported schema, read additive unknown fields |
| Completion evidence | supported-schema migration result (local portion) per [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05) completion gate |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Split from the export-fidelity half of [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05) (NOTES.30) because migration needs no Cloud artifact at all, while export fidelity explicitly needs the real [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) producer - keeping them together would make a purely-local schema-migration task wait on Cloud for no reason. |

<a id="task-notes-30"></a>

### NOTES.30 — Cloud export fidelity for property/view metadata

**Outcome.** The Cloud export manifest built by NOTES.20 additionally declares property/view metadata with an accurate fidelity report, verified against the real [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) export producer (not a mock).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-30` and ledger record `ledger/tasks/notes-30.md` in the Plan repository; task branch `task/notes-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05) — Cloud export includes declared property/view metadata and a fidelity report, verified through the real [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) producer<br>[WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (bottom of file): verify local hydrated/pending export + actual Cloud export; source-policy/one-use context permission; notebook/document/query/structural conflict behavior — package-level obligation contribution |
| Provides | notes.export.property-view-fidelity |
| Start prerequisites | **artifact** [NOTES.20](#task-notes-20) — the Cloud export client this extends. *Why:* same export pipeline, additional content class<br>**artifact** [NOTES.23](#task-notes-23) — property schema to describe in the manifest. *Why:* direct dependency<br>**artifact** [NOTES.26](#task-notes-26) — view schema to describe in the manifest. *Why:* direct dependency |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NOTES.33](#task-notes-33) — real Cloud export producer, same as NOTES.20. *Why:* [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05)'s own testing requirement: 'export through the real [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) producer and verify declared values/metadata/omissions' - explicitly not satisfiable by a mock |
| Unblocks | [NOTES.33](#task-notes-33) |
| Write scope | `ArcNotes:src/ArcForges.ArcNotes.ImportExport/Export/PropertyViewFidelity/**` |
| Shared resources | [RES-arcnotes-composition](../shared-resources.md#res-arcnotes-composition) (append) |
| Validation | integration test against the real [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) producer once available; no mock Cloud acceptance permitted per producer-artifacts-and-integration.md row 28 |
| Completion evidence | supported-schema migration and Cloud-export fidelity results (export portion) per [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-31"></a>

### NOTES.31 — Scale: large collections, many properties, large result sets

**Outcome.** Every view kind meets responsiveness and memory budgets on the scale corpus through virtualisation and indexing; a soak test on a large view holds memory within the product ceiling.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-31` and ledger record `ledger/tasks/notes-31.md` in the Plan repository; task branch `task/notes-31` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-28.06](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.06) — full |
| Provides | notes.view.scale |
| Start prerequisites | **artifact** [NOTES.26](#task-notes-26) — the view kinds being scale-tested. *Why:* direct dependency<br>**artifact** [NOTES.04](#task-notes-04) — the virtualised layout engine reused for large table/list bodies. *Why:* shared rendering-performance mechanism |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.32](#task-notes-32) |
| Write scope | `ArcNotes:tests/ArcForges.ArcNotes.Tests.Integration/Scale/**` |
| Validation | offline scale-corpus benchmark fixtures; memory-ceiling assertion; soak test |
| Completion evidence | scale corpus and soak results per view kind, per [WP-28.06](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.06) completion gate |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-32"></a>

### NOTES.32 — Owned-artifact and real-integration verification

**Outcome.** Independent local/Cloud query vectors, null/missing/invalid values, sorting/tie-breaks and snapshot pagination are recorded; the producer edge to [WP-40](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) is kept ([WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) provides for [WP-40](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40), never blocks on it).

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/notes-32` and ledger record `ledger/tasks/notes-32.md` in the Plan repository; task branch `task/notes-32` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-28.90](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.90) — all work except the parts mapped to NOTES.34<br>[WP-28.00](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.00) — final-review paragraph: independent verification of 04-protobuf-wire-registry; cross-notebook move with real scalar defs/select options/tags<br>[WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) Final-review paragraph (S5, before 28.90): independent verification of 04-protobuf-wire-registry; cross-notebook move with real scalar definitions/select options/tags - stale target semantics, incomplete mapping and conflicting destination mappings refuse atomically; explicit approved removals remain in history — package-level obligation contribution<br>[WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (bottom of file): verify local hydrated/pending export + actual Cloud export; source-policy/one-use context permission; notebook/document/query/structural conflict behavior — package-level obligation contribution |
| Provides | notes.wp28-closure-receipt |
| Start prerequisites | **artifact** [NOTES.23](#task-notes-23) — own-lane completion. *Why:* gate covers the whole [WP-28](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) surface<br>**artifact** [NOTES.24](#task-notes-24) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.26](#task-notes-26) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.27](#task-notes-27) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.28](#task-notes-28) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.29](#task-notes-29) — own-lane completion. *Why:* see above<br>**artifact** [NOTES.31](#task-notes-31) — own-lane completion. *Why:* see above |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NOTES.34](#task-notes-34) — the real local-vs-Cloud query conformance evidence [WP-28.90](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.90) explicitly requires. *Why:* 'Independent local/Cloud query vectors... no mock Cloud acceptance' cannot close without it<br>**integration** [NOTES.33](#task-notes-33) — NOTES.30's real producer evidence. *Why:* export-fidelity portion of the gate |
| Unblocks | [REL.01](release.md#task-rel-01) |
| Write scope | `ArcNotes:tests/ArcForges.ArcNotes.Tests/Integration/Wp28/**` |
| Validation | offline where possible; real Cloud cross-check evidence attached from IM.notes-cloud-query-conformance; no macOS/hosted-runtime CI |
| Completion evidence | owned artifact and real-integration receipt per [WP-28.90](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.90), including local/Cloud query vector parity and export fidelity |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-33"></a>

### NOTES.33 — Real Cloud Notes export join replaces the / fixture endpoint

**Outcome.** Real host/database/object-store Notes export across concurrent edits, notebook moves, deleted attachments, quota limits, expiry, restart, cancellation and paid-term end; structural removal of the runtime fixture registration NOTES.20 created

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes`; also touches Cloud |
| Claim, branch and ledger | `claims/notes-33` and ledger record `ledger/tasks/notes-33.md` in the Plan repository; task branch `task/notes-33` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-28.05](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.05) — Cloud export fidelity for property/view metadata<br>[WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) — Notes/Chat export producer (owned by the Cloud lane; Chat half is the assistant lanes [WP-15.06](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.06)) |
| Start prerequisites | **artifact** [NOTES.20](#task-notes-20) — real, delivered outcome of NOTES.20 (Cloud Notes export client and its named fixture endpoint). *Why:* this integration exercises the real cloud Notes export client and its named fixture endpoint instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NOTES.30](#task-notes-30) — real, delivered outcome of NOTES.30 (Cloud export fidelity for property/view metadata). *Why:* this integration exercises the real cloud export fidelity for property/view metadata instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.45](cloud.md#task-cloud-45) — real, delivered outcome of CLOUD.45 (Real Cloud Notes and Chat export producers). *Why:* this integration exercises the real real Cloud Notes and Chat export producers instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.47](cloud.md#task-cloud-47), [CLOUD.58](cloud.md#task-cloud-58), [NOTES.30](#task-notes-30), [NOTES.32](#task-notes-32) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Real host/database/object-store Notes export across concurrent edits, notebook moves, deleted attachments, quota limits, expiry, restart, cancellation and paid-term end; structural removal of the runtime fixture registration NOTES.20 created |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-34"></a>

### NOTES.34 — Cross-evaluator conformance of notes.scalar.v1 between the native cache and the real Cloud query evaluator

**Outcome.** Identical operator, ordering and pagination semantics between ArcNotes' local evaluator (NOTES.24) and Cloud's D1-backed evaluator, on the same authorized, fully hydrated revision set, per the arcnotes.md S7.1 acceptance vectors

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes`; also touches Cloud |
| Claim, branch and ledger | `claims/notes-34` and ledger record `ledger/tasks/notes-34.md` in the Plan repository; task branch `task/notes-34` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-28.01](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.01) — native-vs-Cloud conformance suite execution<br>[WP-28.90](../../work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.90) — independent local/Cloud query vectors, no mock Cloud acceptance |
| Start prerequisites | **artifact** [NOTES.24](#task-notes-24) — real, delivered outcome of NOTES.24 (Query model: local evaluator and notes.scalar.v1 conformance fixtures). *Why:* this integration exercises the real query model: local evaluator and notes.scalar.v1 conformance fixtures instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.37](cloud.md#task-cloud-37) — real, delivered outcome of CLOUD.37 (Cloud Notes authority and sync scopes). *Why:* this integration exercises the real cloud Notes authority and sync scopes instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.24](#task-notes-24), [NOTES.32](#task-notes-32) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Identical operator, ordering and pagination semantics between ArcNotes' local evaluator (NOTES.24) and Cloud's D1-backed evaluator, on the same authorized, fully hydrated revision set, per the arcnotes.md S7.1 acceptance vectors |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-notes-35"></a>

### NOTES.35 — ArcNotes participates in the three-device convergence harness

**Outcome.** ArcNotes documents/blocks/attachments/deletions converge to verifiably identical state across three devices under concurrent editing, an extended offline device, and a mid-sync crash

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes`; also touches Cloud |
| Claim, branch and ledger | `claims/notes-35` and ledger record `ledger/tasks/notes-35.md` in the Plan repository; task branch `task/notes-35` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-25.07](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.07) — Notes object-kind coverage of the convergence harness; the real ArcNotes-client side of the three-device convergence harness |
| Start prerequisites | **artifact** [NOTES.01](#task-notes-01) — real, delivered outcome of NOTES.01 (Notebook/folder hierarchy, document placement and structural commands). *Why:* this integration exercises the real notebook/folder hierarchy, document placement and structural commands instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NOTES.02](#task-notes-02) — real, delivered outcome of NOTES.02 (Block/inline content model, EditTransaction engine, kind conversions and clipboard). *Why:* this integration exercises the real block/inline content model, EditTransaction engine, kind conversions and clipboard instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NOTES.10](#task-notes-10) — real, delivered outcome of NOTES.10 (Undo, history, checkpoint and trash as four distinct mechanisms). *Why:* this integration exercises the real undo, history, checkpoint and trash as four distinct mechanisms instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.44](cloud.md#task-cloud-44) — real, delivered outcome of CLOUD.44 (Multi-device convergence harness). *Why:* this integration exercises the real multi-device convergence harness instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.37](cloud.md#task-cloud-37) — real, delivered outcome of CLOUD.37 (Cloud Notes authority and sync scopes). *Why:* this integration exercises the real cloud Notes authority and sync scopes instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.38](cloud.md#task-cloud-38) — real, delivered outcome of CLOUD.38 (Client outbox and conflict lineage (desktop data model)). *Why:* this integration exercises the real client outbox and conflict lineage (desktop data model) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.39](cloud.md#task-cloud-39) — real, delivered outcome of CLOUD.39 (Guarded publication and convergent bootstrap). *Why:* this integration exercises the real guarded publication and convergent bootstrap instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.40](cloud.md#task-cloud-40) — real, delivered outcome of CLOUD.40 (Conflict detection and five resolution policies). *Why:* this integration exercises the real conflict detection and five resolution policies instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.41](cloud.md#task-cloud-41) — real, delivered outcome of CLOUD.41 (Deletion and tombstones). *Why:* this integration exercises the real deletion and tombstones instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.42](cloud.md#task-cloud-42) — real, delivered outcome of CLOUD.42 (Blob lifecycle (real R2 staged/verified/committed)). *Why:* this integration exercises the real blob lifecycle (real R2 staged/verified/committed) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.47](cloud.md#task-cloud-47), [NOTES.02](#task-notes-02) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | ArcNotes documents/blocks/attachments/deletions converge to verifiably identical state across three devices under concurrent editing, an extended offline device, and a mid-sync crash |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as CLOUD.56. |

<a id="task-notes-37"></a>

### NOTES.37 — ArcNotes PDF attachment viewer against the real ContentSandbox

**Outcome.** the full [PG-12](../../../assurance/open-gates-register.md#rule-pg-12) gate: a malformed/hostile PDF opened through ArcNotes' attachment viewer cannot crash or compromise the parent product, and licence/provenance evidence for the PDF dependency closure is complete.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes`; also touches DesktopPlatform |
| Claim, branch and ledger | `claims/notes-37` and ledger record `ledger/tasks/notes-37.md` in the Plan repository; task branch `task/notes-37` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-18.04](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.04) — full - owned by the ArcNotes lane, listed here only because it is the gate-closing consumer of this area's PLT.45; real PDF viewer integration and malformed native input containment |
| Start prerequisites | **artifact** [PLT.45](platform.md#task-plt-45) — real, delivered outcome of PLT.45 (Content helper and OS-enforced isolation (ContentSandbox host)). *Why:* this integration exercises the real content helper and OS-enforced isolation (ContentSandbox host) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.14](native.md#task-nat-14) — real, delivered outcome of NAT.14 (Pdf family: PDFium and production parser containment in the WP11 helper (NEW library)). *Why:* this integration exercises the real pdf family: PDFium and production parser containment in the WP11 helper (NEW library) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NOTES.09](#task-notes-09) — real, delivered outcome of NOTES.09 (PDF in-product viewer, page anchors and native parser isolation). *Why:* this integration exercises the real pDF in-product viewer, page anchors and native parser isolation instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.25](native.md#task-nat-25) — real, delivered outcome of NAT.25 (Pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition). *Why:* this integration exercises the real pdf package production: all 6 RIDs + ContentSandbox Runtime.<rid> composition instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.04.arcnotes](adoption.md#task-adopt-04-arcnotes) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.44](cloud.md#task-cloud-44) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | the full [PG-12](../../../assurance/open-gates-register.md#rule-pg-12) gate: a malformed/hostile PDF opened through ArcNotes' attachment viewer cannot crash or compromise the parent product, and licence/provenance evidence for the PDF dependency closure is complete. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as NOTES.36. |
