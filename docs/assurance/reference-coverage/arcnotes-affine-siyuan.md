# Reference Coverage Matrix — ArcNotes / AFFiNE + SiYuan

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete**
> Governing authority: **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** (ArcNotes phased full scope)
> Consuming product: **ArcNotes** — [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md)

---

## 1. Source identity

| Field | AFFiNE | SiYuan |
|---|---|---|
| Repository | `github.com/toeverything/AFFiNE` | `github.com/siyuan-note/siyuan` |
| Local path | `C:\MyFile\ArcForges\AFFiNE` | `C:\MyFile\ArcForges\siyuan` |
| Commit | `81df4751a3` | `eef105683` |
| Commit date | 2026-07-19 | 2026-07-21 |
| Reviewed on | 2026-09-05 | 2026-09-05 |
| Reviewer | Architecture Owner (design stage) | Architecture Owner (design stage) |

---

## 2. Licence and provenance position

### 2.1 AFFiNE — a split licence, and the split matters

The repository root `LICENSE` is **not** a single grant. Read in full, it states:

| Subtree | Governing licence | Evidence |
|---|---|---|
| `packages/backend/**` and `packages/common/native/**` | The licence in `packages/backend/server/LICENSE` | root `LICENSE`, bullet 1 |
| Third-party components | Their own original licences | root `LICENSE`, bullet 2 |
| **Everything else** — including `blocksuite/**` and `packages/frontend/**` | **MIT**, per `LICENSE-MIT` | root `LICENSE`, bullet 3 |

`packages/backend/server/LICENSE` opens: *"The AFFiNE Enterprise Edition (EE) license"* — a **proprietary** grant, not an open-source licence.

| # | Finding |
|---|---|
| <a id="rule-lp-01"></a>LP-01 | **`packages/backend/**` and `packages/common/native/**` are proprietary.** Under **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** this is incompatible material: it must not be copied, translated or ported, and it may be used only as controlled behavioural reference. |
| LP-02 | **`blocksuite/**` and `packages/frontend/**` are MIT** — permissive, compatible with both ArcForges boundaries after a per-file record. No separate `LICENSE` file exists inside `blocksuite/`, so the root split governs it. |
| LP-03 | **This is precisely the case [D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013) warns about.** A repository-root reading would have concluded "MIT" and cleared a proprietary server subtree for reuse. The subtree licence governs. |

### 2.2 SiYuan

| Scope | Evidence | Finding |
|---|---|---|
| Repository root | `LICENSE` — GNU Affero General Public License Version 3 | **AGPL-3.0** |
| Subtree exceptions | No differing licence file found under `kernel/` or `app/` | None found in the reviewed scope |

| # | Finding |
|---|---|
| LP-04 | **AGPL-3.0 material may be reused only inside the ArcForges AGPL boundary**, and only after exact compatibility and provenance review (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). |
| LP-05 | **It is prohibited in the Apache-2.0 mobile and public-client boundary** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**). Any ArcNotes concept traced to SiYuan must never surface in a mobile or public-SDK contract. |

**No row in this matrix proposes reuse from either reference.** ArcNotes is an original C#/Avalonia implementation; the references supply behavioural, model and migration evidence.

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| AFFiNE editor block model | `blocksuite/affine/blocks/*` (20 block types) |
| AFFiNE editor framework | `blocksuite/framework/{global,std,store}`, `blocksuite/affine/{foundation,model,shared,inlines,rich-text,gfx,components,widgets,fragments,data-view,ext-loader}` |
| AFFiNE application modules | `packages/frontend/core/src/modules/*` (~75 modules) |
| AFFiNE common layer | `packages/common/{auth,env,error,graphql,infra,nbstore,reader,realtime,s3-compat,theme}` |
| AFFiNE server (licence position only) | `packages/backend/server/LICENSE` |
| SiYuan kernel domain | `kernel/model/*` (~100 files) |
| SiYuan kernel subsystems | `kernel/{av,search,sql,sync,plugin,mcp,agent,bazaar,job,task,treenode,filesys,api,server}` |
| Packaged release behaviour | `StartArcForges/{AFFiNE,siyuan}` |

**Not read, and why:** `node_modules` and lockfiles — no design evidence. `packages/backend/server/src/**` — **deliberately not read beyond its licence file**, because it is proprietary and reading its expression creates contamination risk with no offsetting benefit; the licence determination alone settles its disposition. `screenshots/`, `docs-site/` — presentation material.

---

## 4. Item-level matrix

| # | Capability / behaviour | Reference | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|---|
| <a id="rule-an-01"></a>AN-01 | Block document model, ordered tree, block identity | AFFiNE | `blocksuite/framework/store`, `blocksuite/affine/model` | `products/arcnotes.md` §block model; [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) | Reference Only | Confirms stable block identity across structural change is the core requirement | MIT; no reuse proposed | First-party test: block identity survives reorder and reparent | Product Owner | Evidence established |
| AN-02 | Block type set — paragraph, list, code, divider, image, attachment, bookmark, callout, latex, table | AFFiNE | `blocksuite/affine/blocks/{paragraph,list,code,divider,image,attachment,bookmark,callout,latex,table}` | `products/arcnotes.md` §block kinds; [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) | Reference Only | Establishes the expected V1 block vocabulary for a product in this category | MIT; no reuse proposed | Per-block-kind round-trip tests | Product Owner | Evidence established |
| <a id="rule-an-03"></a>AN-03 | Edgeless surface, frame, edgeless text, surface reference | AFFiNE | `blocksuite/affine/blocks/{surface,surface-ref,frame,edgeless-text}`, `blocksuite/affine/gfx` | **Accepted exclusion** — Edgeless, whiteboard, shapes, connectors and frames are excluded by **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** | Drop | Removed from required delivery by the [D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006) amendment of 2026-09-06. [WP-27](../../planning/work-packages/27-arcnotes-edgeless-canvas.md#rule-wp-27) is retired; no dormant hook remains | MIT; no reuse proposed | First-party test: content moves between surfaces with identity preserved | Product Owner | Accepted exclusion |
| <a id="rule-an-04"></a>AN-04 | Database blocks and data view | AFFiNE | `blocksuite/affine/blocks/{database,data-view}`, `blocksuite/affine/data-view` | `products/arcnotes.md` §properties and views (bounded by **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**); [WP-28](../../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) | Reference Only | Evidence that a view is a query rather than a container. **ArcForges delivers bounded scalar properties with saved list and table views only** — no formula, relation or rollup engine, and no board, gallery, calendar or timeline layout | MIT; no reuse proposed | First-party test: view kind switch preserves the query | Product Owner | Evidence established |
| AN-05 | Table block distinct from database block | AFFiNE | `blocksuite/affine/blocks/table` vs `.../database` | `products/arcnotes.md` §table is a document table; [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00), [WP-28](../../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) | Reference Only | **Direct support for the accepted non-goal**: the reference itself keeps a document table separate from a database view | MIT; no reuse proposed | First-party test: the two concepts are structurally distinct | Product Owner | Evidence established |
| AN-06 | Embedded document references | AFFiNE | `blocksuite/affine/blocks/{embed,embed-doc}` | `products/arcnotes.md` §embedded reference; [WP-18.02](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.02) | Reference Only | Supports the rule that editing authority stays with the original object | MIT; no reuse proposed | First-party test: no second writable block | Product Owner | Evidence established |
| <a id="rule-an-07"></a>AN-07 | Rich text and inline model | AFFiNE | `blocksuite/affine/{rich-text,inlines}` | `products/arcnotes.md` §editing; [WP-18.01](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) | Reference Only | Evidence on inline-level model separation from block model | MIT; no reuse proposed | First-party editing tests including composition input | Product Owner | Evidence established |
| <a id="rule-an-08"></a>AN-08 | Extension loader | AFFiNE | `blocksuite/affine/ext-loader` | `08-extensions-and-developer-platform.md`; [WP-41](../../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41) | Reference Only | **Divergence recorded**: an in-process extension loader is exactly what **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** and the extension architecture forbid for third-party code | MIT; no reuse proposed | First-party test: no third-party assembly in the main process | Architecture Owner | Evidence established |
| AN-09 | Docs search and workspace indexer | AFFiNE | `modules/docs-search`, `modules/workspace-indexer-embedding` | `06-knowledge-search-and-retrieval.md`; [WP-19.00](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.00), [WP-40.01](../../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.01) | Reference Only | Evidence that lexical and embedding indexes are separate derived projections | MIT; no reuse proposed | First-party test: index rebuild equivalence | Product Owner | Evidence established |
| AN-10 | Import / import-template / import-clipper | AFFiNE | `modules/{import,import-template,import-clipper}` | `13-data-formats-and-portability.md` §import; [WP-19.04](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.04) | Reference Only | **Migration evidence**: names the import sources a product in this category is expected to accept | MIT; no reuse proposed | Format fixture per claimed import version ([PG-07](../open-gates-register.md#rule-pg-07)) | Product Owner | Evidence established |
| AN-11 | Backup module | AFFiNE | `modules/backup` | `13-data-formats-and-portability.md` §backup; [WP-46](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) | Reference Only | Evidence on client-side backup expectations | MIT; no reuse proposed | First-party restore proof | Operations Owner | Evidence established |
| <a id="rule-an-12"></a>AN-12 | Journal | AFFiNE | `modules/journal` | **Accepted exclusion** — daily-note journal is not in the accepted ArcNotes V1 scope | Drop | **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** fixes ArcNotes' phased scope as edgeless, database views and slides; a journal surface is additional product scope | MIT; no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-an-13"></a>AN-13 | Comment | AFFiNE | `modules/comment` | **Accepted exclusion** — collaboration commenting is beyond first launch | Drop | Real-time multi-user collaboration is explicitly later; comments presuppose it | MIT; no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-an-14"></a>AN-14 | Share doc / share menu / share setting / paywall / quota | AFFiNE | `modules/{share-doc,share-menu,share-setting,paywall,quota}` | Public sharing: **accepted exclusion** (no public share links in V1). Quota: `04-commerce-entitlement-and-credits.md` §7 | Drop (sharing); Reference Only (quota) | The web architecture states there are no public share links in V1; quota evidence is separately useful | MIT; no reuse | Quota accounting comparison ([WP-42.06](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.06)) | Product Owner | Accepted exclusion (sharing); Evidence established (quota) |
| <a id="rule-an-15"></a>AN-15 | PDF and media modules | AFFiNE | `modules/{pdf,media}` | `products/arcnotes.md` §attachments; [WP-18.04](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) | Reference Only | Evidence that extracted text is derived data, rebuildable | MIT; no reuse proposed | First-party test: derived-data rebuild | Product Owner | Evidence established |
| AN-16 | Peek view / find in page / quicksearch | AFFiNE | `modules/{peek-view,find-in-page,quicksearch}` | `09-shared-desktop-experience.md` §command surface; [WP-10.02](../../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.02), [WP-19.01](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.01) | Reference Only | Evidence on the expected navigation surface | MIT; no reuse proposed | First-party keyboard-completion tests | Product Owner | Evidence established |
| AN-17 | Telemetry and track | AFFiNE | `modules/telemetry`, `packages/frontend/track` | `07-security-privacy-and-trust.md` §privacy; [WP-12.05](../../planning/work-packages/12-observability-foundation.md#rule-wp-12.05) | Reference Only | **Divergence recorded**: ArcForges desktop telemetry is minimal and opt-in, stricter than the reference | MIT; no reuse proposed | First-party test: nothing leaves the device without consent | Security and Privacy Owner | Evidence established |
| <a id="rule-an-18"></a>AN-18 | Server, cloud sync, realtime, storage | AFFiNE | `packages/backend/**`, `packages/common/{nbstore,realtime,s3-compat}` | `03-cloud-services-and-sync.md`; [WP-21](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21)–[WP-25](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) | **Reference Only — restricted** | `packages/backend/**` is **proprietary (EE)**; it must not be copied, translated or ported, and its expression was deliberately not read. `packages/common/{nbstore,realtime,s3-compat}` are MIT and supply sync-shape evidence only | Mixed: proprietary (backend) / MIT (common) | First-party three-device convergence proof ([WP-25.07](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.07)) | Architecture Owner | Evidence established |
| <a id="rule-an-19"></a>AN-19 | Native modules | AFFiNE | `packages/common/native`, `packages/frontend/native`, `packages/frontend/mobile-native` | `12-native-interop-and-media.md` §2 | **Reference Only — restricted** | `packages/common/native` is governed by the **proprietary** backend licence per the root split; no reuse in any form | Proprietary | — | Licensing and Provenance Owner | Evidence established |
| AN-20 | Notebook / box model | SiYuan | `kernel/model/{box,box_doc,mount}.go` | `products/arcnotes.md` §workspace and notebook | Reference Only | Evidence for a notebook-scoped document container distinct from workspace | AGPL-3.0; no reuse proposed | First-party tests in [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) | Product Owner | Evidence established |
| <a id="rule-an-21"></a>AN-21 | Attribute view (typed properties and views) | SiYuan | `kernel/av/**`, `kernel/model/attribute_view*.go` (7 files incl. tests) | `products/arcnotes.md` §properties (**[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** phase 2); [WP-28](../../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) | Reference Only | **Second independent confirmation** that views are projections over typed attributes, from a different technology stack | AGPL-3.0; no reuse proposed | First-party property lifecycle tests | Product Owner | Evidence established |
| AN-22 | Backlink and virtual reference | SiYuan | `kernel/model/{backlink,virutalref}.go` | `products/arcnotes.md` §backlinks; [WP-18.02](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.02) | Reference Only | Confirms backlinks are derived from an index, not stored in content | AGPL-3.0; no reuse proposed | First-party test: backlinks provably derived | Product Owner | Evidence established |
| <a id="rule-an-23"></a>AN-23 | Transaction and undo log | SiYuan | `kernel/model/{transaction,undolog}.go` + `transaction_test.go` | `13-data-formats-and-portability.md` §undo vs journal; [WP-07.00](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.00), [WP-18.05](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05) | Reference Only | **Directly supports [QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)**: the reference keeps a transaction path and an undo log as separate mechanisms | AGPL-3.0; no reuse proposed | First-party four-mechanism distinction matrix | Architecture Owner | Evidence established |
| AN-24 | History and repository snapshots | SiYuan | `kernel/model/{history,repository}.go` + `history_test.go` | `products/arcnotes.md` §history and checkpoint; [WP-18.05](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05) | Reference Only | Evidence that document history and snapshot repository are distinct from undo | AGPL-3.0; no reuse proposed | First-party checkpoint restore test | Product Owner | Evidence established |
| AN-25 | Sync and cloud service | SiYuan | `kernel/model/{sync,cloud_service}.go` | `03-cloud-services-and-sync.md`; [WP-25](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) | Reference Only | Evidence on sync conflict and device-set expectations | AGPL-3.0; no reuse proposed | Three-device convergence proof ([WP-25.07](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.07)) | Architecture Owner | Evidence established |
| AN-26 | Export, encrypted export, export merge | SiYuan | `kernel/model/{export,encrypted_export,export_merge}.go` + tests | `13-data-formats-and-portability.md` §export; [WP-19.05](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05) | Reference Only | **Migration evidence** on export completeness and encryption expectations | AGPL-3.0; no reuse proposed | Native round-trip equivalence ([WP-19.05](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05)) | Product Owner | Evidence established |
| AN-27 | Import including Obsidian | SiYuan | `kernel/model/{import,import_obsidian}.go` + tests | `13-data-formats-and-portability.md` §import; [WP-19.04](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.04) | Reference Only | Names a concrete third-party import target and its fixture needs. **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) narrows required import to Markdown and plain text**; DOCX and full-fidelity package import are excluded from delivery | AGPL-3.0; no reuse proposed | Format fixture per claimed version ([PG-07](../open-gates-register.md#rule-pg-07)) | Product Owner | Evidence established |
| AN-28 | Search, index, rerank, embedding | SiYuan | `kernel/search/**`, `kernel/model/{search,index,rerank,embedding}.go` | `06-knowledge-search-and-retrieval.md`; [WP-19.00](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.00), [WP-40](../../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) | Reference Only | Evidence that lexical search, index maintenance and reranking are separable stages | AGPL-3.0; no reuse proposed | First-party permission-at-query test | Product Owner | Evidence established |
| <a id="rule-an-29"></a>AN-29 | Plugin, widget, snippet, template, theme | SiYuan | `kernel/model/{plugin,widget,snippet,template,theme}.go`, `kernel/plugin/**` | `08-extensions-and-developer-platform.md`; [WP-41](../../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41) | Reference Only | **Divergence recorded**: in-process plugins and user-injected snippets are prohibited by the ArcForges extension architecture | AGPL-3.0; no reuse proposed | First-party test: no in-process third-party code | Architecture Owner | Evidence established |
| <a id="rule-an-30"></a>AN-30 | Bazaar (community marketplace) | SiYuan | `kernel/bazaar/**`, `kernel/model/bazaar.go` | `08-extensions-and-developer-platform.md` §catalog; [WP-41.05](../../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.05) | Reference Only | Evidence for a catalog that is distribution-only rather than a paid marketplace — matching the accepted V1 position | AGPL-3.0; no reuse proposed | First-party hostile-catalog tests | Architecture Owner | Evidence established |
| AN-31 | MCP and agent | SiYuan | `kernel/mcp/**`, `kernel/agent/**`, `kernel/model/ai.go` | `08-extensions-and-developer-platform.md` §MCP; **[V-02](../phase-1-official-verification.md#rule-v-02)**; [WP-41.07](../../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) | Reference Only | Second confirmation that MCP is an integration adapter in this product category | AGPL-3.0; no reuse proposed | Vocabulary mapping record ([VG-02](../open-gates-register.md#rule-vg-02)) | Architecture Owner | Evidence established |
| <a id="rule-an-32"></a>AN-32 | WebDAV / CalDAV / CardDAV | SiYuan | `kernel/model/{dav,caldav,carddav}.go` | **Accepted exclusion** — no ArcForges requirement | Drop | Calendar and contact protocol servers are outside the accepted ArcNotes scope | AGPL-3.0; no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-an-33"></a>AN-33 | Flashcard / spaced repetition | SiYuan | `kernel/model/flashcard.go` | **Accepted exclusion** — no ArcForges requirement | Drop | Spaced-repetition study is additional product scope not in **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** | AGPL-3.0; no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-an-34"></a>AN-34 | OCR | SiYuan | `kernel/model/ocr.go` | **Accepted exclusion** as a first-party V1 capability | Drop | Attachment text extraction is required ([AN-15](#rule-an-15)); bundled OCR is a heavier commitment not in the accepted scope | AGPL-3.0; no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-an-35"></a>AN-35 | Graph view | SiYuan | `kernel/model/graph.go` | **Accepted exclusion** — not in the accepted V1 scope | Drop | A relationship graph visualisation is additional scope beyond **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)**'s three phases | AGPL-3.0; no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-an-36"></a>AN-36 | Publish access | SiYuan | `kernel/model/{publish_access}.go` + test | **Accepted exclusion** — no public share links in V1 | Drop | Consistent with the accepted web position | AGPL-3.0; no reuse | — | Product Owner | Accepted exclusion |
| AN-37 | Crypto and encrypted operations | SiYuan | `kernel/model/{crypto,encrypted_ops}.go` + tests | `07-security-privacy-and-trust.md` §secrets; `13-data-formats-and-portability.md` | Reference Only | Evidence on at-rest encryption expectations for a local-first note product | AGPL-3.0; no reuse proposed | First-party secret-handling tests | Security and Privacy Owner | Evidence established |
| AN-38 | Raw path guard | SiYuan | `kernel/model/raw_path_guard.go` | `12-native-interop-and-media.md` §3.3; `07-security-privacy-and-trust.md` | Reference Only | **Security evidence**: confirms path traversal is a real attack surface in this product category, supporting the resource-identity-not-path rule | AGPL-3.0; no reuse proposed | First-party test: a reference cannot carry a path | Security and Privacy Owner | Evidence established |
| AN-39 | Updater | SiYuan | `kernel/model/updater.go` | `10-distribution-update-and-support.md` §3 | Reference Only | Evidence on in-product update expectations | AGPL-3.0; no reuse proposed | Update matrix ([WP-50.02](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02)) | Release Engineering Owner | Evidence established |
| AN-40 | Onboarding | SiYuan | `kernel/model/onboarding.go` + test | `09-shared-desktop-experience.md` §first run | Reference Only | Evidence that first-run content seeding is expected; ArcForges must not make **application launch** a sign-in gate ([ID-01](../../requirements/02-identity-account-and-workspace.md#rule-id-01) of the identity requirements), while **notebook enrolment does require Cloud sign-in** ([PR-02](../../requirements/products/arcnotes.md#rule-pr-02) of the ArcNotes requirements) | AGPL-3.0; no reuse proposed | First-party test: the application launches with no account, and an enrolled hydrated notebook stays editable and searchable through an outage ([WP-18](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18) gate 10) | Product Owner | Evidence established |
| AN-41 | Packaged release shape | Both | `StartArcForges/{AFFiNE,siyuan}`: `affine-0.27.2-stable-windows-x64.nsis.exe`, `Squirrel.exe`, `siyuan-3.7.3-win.exe`, `LICENSES.chromium.html`, `LICENSE.electron.txt` | `10-distribution-update-and-support.md`; `14-build-packaging-and-release.md` | Reference Only | **Packaging and NOTICE evidence**: both ship an installer plus bundled runtime licence files — the NOTICE obligation pattern ArcForges must also satisfy | Bundled notices | [WP-50.01](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01) NOTICE verification | Release Engineering Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 41 rows across all 8 areas |
| Every row carries all nine required fields | **Pass** |
| Every row carries a completeness state | **Pass** — 41 rows: 33 evidence established, 9 accepted exclusions, 0 unresolved. [AN-14](#rule-an-14) is the one compound row (sharing excluded, quota established) and is counted in both, so the two figures sum to 42 over 41 rows. **Recounted 2026-09-06 after [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**; [AN-03](#rule-an-03) moved to exclusion because Edgeless is no longer delivered |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** — no row creates a new requirement |
| Licence position determined below the repository root | **Pass, and materially so** — the AFFiNE split changed the position for two subtrees |
| Any row proposing reuse carries a provenance obligation | **Not applicable** — no row proposes reuse |
| **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** phase coverage — edgeless, views, slides | Edgeless [AN-03](#rule-an-03), views [AN-04](#rule-an-04)/[AN-21](#rule-an-21). **Slides: neither reference implements a presentation mode** — recorded in `§6` |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

| # | Finding | Effect |
|---|---|---|
| F-AN-1 | **AFFiNE's server subtree is proprietary**, not MIT as the root badge implies. | Confirms **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**'s "a repository-root licence must not be assumed to cover every file" is load-bearing. `packages/backend/**` and `packages/common/native/**` are permanently ineligible for reuse and were deliberately not read beyond their licence. **No design change**; the provenance rule already covers it. |
| F-AN-2 | **Neither reference implements slides or a presentation mode.** | **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** phase 3 ([WP-29](../../planning/work-packages/29-arcnotes-slides.md#rule-wp-29)) has **no reference evidence**. It is an original ArcForges capability. [WP-29](../../planning/work-packages/29-arcnotes-slides.md#rule-wp-29) must therefore rely on first-party requirements and oracles only, and its matrix row is an explicit absence rather than an omission. **Effect: [WP-29](../../planning/work-packages/29-arcnotes-slides.md#rule-wp-29)'s verification oracle set is first-party only** — recorded in that package. |
| F-AN-3 | **Both references independently converge on views-as-projections-over-typed-attributes** ([AN-04](#rule-an-04), [AN-21](#rule-an-21)), from different stacks. | Strong support for [WP-28](../../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28)'s ordering — properties and queries before views. No change needed. |
| F-AN-4 | **Both references implement in-process extension loading** ([AN-08](#rule-an-08), [AN-29](#rule-an-29)). | The ArcForges out-of-process decision diverges from both references. This is deliberate and already justified by **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**; recorded so the divergence is not mistaken for an oversight. |
| F-AN-5 | **SiYuan keeps transaction and undo log as separate mechanisms** ([AN-23](#rule-an-23)). | Independent support for [QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09). No change needed. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | Bound to AFFiNE `81df4751a3` and SiYuan `eef105683`. [WP-18](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18) re-checks both for drift and newly introduced material; it does not re-create this matrix. |
| <a id="rule-mt-02"></a>MT-02 | **The AFFiNE licence split is re-verified on every drift check**, because a subtree licence can change upstream. |
| MT-03 | A new upstream capability is assessed against **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)**'s accepted scope; it does not become a requirement by appearing. |
