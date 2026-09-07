# Product Implementation Maps

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Desktop is a Native AOT deliverable), **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** (target monorepo), **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** (reference coverage), **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** (provenance)
> Companions: [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md), [`../assurance/reference-coverage/README.md`](../assurance/reference-coverage/README.md)

The project layout says which projects exist. The reference coverage matrices say which reference capabilities were reviewed and how they were disposed. **Neither says where each accepted capability actually lives in ArcForges.** This document closes that gap for the four desktop products, and verifies the claim that matters most: that every reference capability ArcForges accepted has a real home, and that every one it declined is declined on the record rather than by omission.

---

## 1. What this document is

| It is | It is not |
|---|---|
| A capability-to-component map per product | A class design or a file listing |
| A verification that each accepted reference capability has a named owner and package | A re-derivation of the coverage matrices |
| A statement of what each product does **not** build | A scope change — nothing here adds a requirement |

| # | Rule |
|---|---|
| PM-01 | **No row here creates a requirement** ([RC-03](../assurance/reference-coverage/README.md#rule-rc-03) of the coverage README). A capability appears because a requirement establishes it. |
| <a id="rule-pm-02"></a>PM-02 | **No row here authorizes reuse.** Across all five matrices — **145 rows** — every disposition is `Reference Only` or `Drop`; **not one proposes `Copy`, `Rewrite`, `Improve` or `Replace`** ([ND-02](../assurance/reference-coverage/README.md#rule-nd-02) there). ArcForges is a first-party implementation informed by behavioural evidence. |
| PM-03 | **A component named here is a project or a bounded area within one**, from [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md). Adding a project is a layout change, not a map change. |
| <a id="rule-pm-04"></a>PM-04 | **A capability with no component and no accepted exclusion is a defect**, and `§7` asserts there are none. |

---

## 2. The shared component pattern

Every desktop product uses the same five-layer shape, which is why a capability's home is predictable rather than negotiated.

| Layer | Holds | Never holds |
|---|---|---|
| `*.Domain` | Entities, value objects, invariants, domain services | Persistence, RPC, UI, provider clients |
| `*.Application` | Use cases, orchestration, policy application, the single write path | Storage mechanics, transport |
| `*.Infrastructure` | Persistence, file formats, external clients, native wrappers | Domain rules |
| `*.LocalRpc` | Contract hosting and consumption, capability descriptors | Business logic — it delegates (`§4` of the local RPC contract) |
| `*.Desktop` | Avalonia host, views, view models, shell composition | Any authoritative state |

Plus per-product specialisations: `ArcChat.Hub` and `ArcChat.Agent`; `ArcScope.Acquisition`; `ArcSlate.Media`.

| # | Rule |
|---|---|
| CP-01 | **A capability's owner-side validation lives in `*.Application`**, never in `*.LocalRpc` and never in the caller (`§2` of the local RPC contract). |
| <a id="rule-cp-02"></a>CP-02 | **A native wrapper lives in `*.Infrastructure`** and is the only project referencing a P/Invoke class ([PI-03](12-native-interop-and-media.md#rule-pi-03), [PI-04](12-native-interop-and-media.md#rule-pi-04) of the native interop architecture). |
| CP-03 | **The Desktop project holds no authoritative state**, which is what makes headless testing of every product possible. |

---

## 3. ArcChat

### 3.1 Capability map

| Capability | Component | Package |
|---|---|---|
| Conversation, message, branch, part model | `ArcChat.Domain` | [WP-15.00](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.00), [WP-15.01](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.01) |
| Attachments by reference | `ArcChat.Domain` + `ArcChat.Infrastructure` | [WP-15.02](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.02) |
| Projects, agent profiles, skills | `ArcChat.Domain` + `ArcChat.Application` | [WP-15.03](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.03), [WP-15.04](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.04) |
| Local search over conversations | `ArcChat.Infrastructure` (derived store) | [WP-15.05](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.05) |
| **The turn loop, batching, compaction** | **`ArcForges.Cloud.AgentRuntime`** — Cloud, not the desktop ([LS-02](17-agent-harness.md#rule-ls-02)) | [WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00), [WP-52.01](../planning/work-packages/52-cloud-harness.md#rule-wp-52.01) |
| Context assembly and packing | **`ArcForges.Cloud.AgentRuntime`** | [WP-40.03](../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.03) |
| Capability registry and selection | Cloud registry + `ArcChat.Hub` for device-local capabilities | [WP-17.00](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.00) |
| Execution engine — task, run, plan, step, attempt | **`ArcForges.Cloud.Modules.Agent`** ([TO-01](data-model/00-data-model-overview.md#rule-to-01)) | [WP-16.00](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.00)–[WP-16.07](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.07) |
| Permission, approval, audit surfaces | `ArcChat.Application` + `ArcChat.Desktop` | [WP-17.02](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.02) |
| Task centre | `ArcChat.Application` + `ArcChat.Desktop` | [WP-17.03](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.03) |
| Automation | `ArcChat.Application` | [WP-17.04](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.04) |
| Cloud AI client — submit a turn, read task state, surface admission reasons | `ArcChat.CloudClient` | [WP-17.05](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.05) |
| Hub registration, routing, health | `ArcChat.Hub` | [WP-14.00](../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00)–[WP-14.06](../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.06) |
| Thin preview and handoff | `ArcChat.Desktop` (`§8.1` of the editing architecture) | [WP-17.06](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.06) |
| Cloud client, sync, bridge consumption | `ArcChat.CloudClient` | [WP-25](../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25), [WP-26](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) |
| First-party local capabilities and the ToolRequest executor | `ArcChat.LocalTools` | [WP-17.00](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.00), [WP-26.02](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02) |

### 3.2 AionUI reference verification

The matrix records 30 items at commit `29c9271a5` — **25 evidence established, 5 accepted exclusions, 0 unresolved** — all `Reference Only` or `Drop`. This table verifies the consequence: every non-excluded item has an ArcForges home, and every excluded item is excluded deliberately.

| # | Reference capability | ArcForges position | Where |
|---|---|---|---|
| <a id="rule-ac-01"></a>AC-01 | Conversation, message, streaming assembly | Present, and **stricter** — a message is immutable on commit and an interrupted stream is stored as `interrupted`, never as complete | `ArcChat.Domain`; [WP-15.00](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.00), [ST-01](17-agent-harness.md#rule-st-01) of the harness |
| AC-02 | Slash commands and availability | Present, and **routed through the capability registry** rather than a static list, so availability is computed with a reason | `ArcChat.Hub`; [WP-17.00](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.00), [MK-05](18-editing-and-rich-content.md#rule-mk-05) of the editing architecture |
| AC-03 | `@`-mention context binding | Present, and **bounded, frozen and permission-filtered** at assembly | `ArcChat.Agent`; `§4` of the harness, [WP-40.03](../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.03) |
| AC-04 | Tool-call normalisation | Present as the resolve-and-validate step of the turn loop, normalising into the typed capability model | `ArcChat.Agent`; `§2` of the harness, [MR-01](17-agent-harness.md#rule-mr-01) |
| <a id="rule-ac-05"></a>AC-05 | Approval store | Present, and **owner-side enforced** — an approval is a durable object, and a cloud approval never substitutes for local re-authorization | `ArcChat.Application`; `§5` of the harness, [BR-01](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-br-01)–[BR-03](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-br-03) |
| AC-06 | ACP external-agent integration | **Excluded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** ([EA-01](../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-06](../requirements/08-extensions-and-developer-platform.md#rule-ea-06)). An integration contributes tools, never a planner | `§9` of the harness; [XA-01](17-agent-harness.md#rule-xa-01), [XA-03](17-agent-harness.md#rule-xa-03) of the harness |
| AC-07 | MCP client and built-in MCP server | Present as an **edge adapter**, never the internal protocol (**[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**). A built-in MCP **server** is not built | [WP-41.07](../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07); [XA-06](17-agent-harness.md#rule-xa-06), [XA-07](17-agent-harness.md#rule-xa-07) |
| AC-08 | Agent detection and hub types | Present, and **contract-typed and lease-based** rather than discovered | `ArcChat.Hub`; [WP-17.00](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.00) |
| AC-09 | Assistant / agent profile | Present, **Cloud-owned** (`§5` of the product scope); clients edit authorised configuration | `ArcForges.Cloud.Modules.Agent`; [WP-15.03](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.03) |
| AC-10 | Workspaces | Present, and **an entitlement and data scope from day one** | `ArcForges.Cloud.Modules.Workspace`; [WP-22](../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22) |
| AC-11 | Teams / multi-agent | **Excluded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** ([EA-08](../requirements/08-extensions-and-developer-platform.md#rule-ea-08) of the extension requirements). Bounded parallel Steps and product Job references stay inside the one Harness; no child agent Tasks | `§12` of the harness; [XA-02](17-agent-harness.md#rule-xa-02) |
| AC-12 | Cron / scheduled tasks | Present as Automation, **kept distinct from a Plan**: automation decides *when*, a plan decides *how* | `ArcChat.Application`; [WP-17.04](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.04), [BR-05](../planning/work-packages/17-arcchat-independent-core.md#rule-br-05) of [WP-17](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17) |
| <a id="rule-ac-13"></a>AC-13 | Remote access via a host-side web server | **Refused by design.** The bridge is pull-and-answer; Cloud never connects to a device (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**) | `§5` of the realtime and bridge contract; [WP-26](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26), [RV-05](contracts/03-realtime-and-bridge.md#rule-rv-05) there |
| AC-14 | Previews | Present as the three honest levels, with rich handoff added | `§8.1` of the editing architecture; [WP-17.06](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.06) |
| AC-15 | Desktop pet | **Accepted exclusion** — no requirement establishes an ambient companion surface | Matrix `AC-15` |
| AC-16 | Settings | Present, and **scope-resolved and explainable** rather than flat | [WP-10.03](../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.03) |
| <a id="rule-ac-17"></a>AC-17 | Auto-update and update feed | Present — the product's own feed is authoritative, storage is replaceable | `§7` of the build architecture; [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) |
| AC-18 | Update failure diagnostics | Present as a persisted installer-failure path in the update matrix | [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) |
| AC-19 | Notification bridge | Present, and **classified by durability** — a missed transient notification loses no durable attention state | [WP-10.04](../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.04); [PD-02](11-mobile-architecture.md#rule-pd-02) of the mobile architecture, [I-405](../requirements/01-normative-glossary-and-invariants.md#rule-i-405) |
| AC-20 | Theming | Present as design tokens, with **no raw colour literal permitted in a component** | [WP-10.00](../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.00); repository policy test |
| AC-21 | Crash and feedback | Present, and **stricter** — generate, show, approve, then send | [WP-12.05](../planning/work-packages/12-observability-foundation.md#rule-wp-12.05) |
| <a id="rule-ac-22"></a>AC-22 | Search adapter | Present, with **permission applied during query evaluation**, so refused content is invisible in results and in counts | [WP-15.05](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.05), [WP-40.03](../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.03) |
| <a id="rule-ac-23"></a>AC-23 | Mobile companion on a separate stack | Present as MAUI under **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**; the separate-stack outcome **confirms [D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** rather than contradicting it | `ArcChat.Mobile`; [WP-30](../planning/work-packages/30-mobile-shared-architecture.md#rule-wp-30), [WP-31](../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31) |
| AC-24 | Web CLI admin-password bootstrap | **Accepted exclusion** — contradicts the passkey-first identity model | Matrix `AC-24` |
| AC-25 | CDP browser automation | **Accepted exclusion** — not a first-party capability in the accepted scope | Matrix `AC-25` |
| AC-26 | Self-hosted server deployment | Present, bounded by ArcForges' own self-host boundary | [WP-45](../planning/work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) |
| AC-27 | First-party image generation via MCP | **Accepted exclusion as a capability**; retained as MCP evidence | Matrix `AC-27` |
| AC-28 | Document handling in chat | Present, **by reference with integrity verification** and never an embedded body | [WP-15.02](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.02); [AT-03](../requirements/products/arcnotes.md#rule-at-03) of the ArcNotes requirements applies the same rule product-wide |
| AC-29 | Packaging configuration | Present; the toolchain differs entirely | `§4` of the build architecture; [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) |
| AC-30 | Hub testing scenarios | Present as the first-slice hub suite — registration, restart, reconnection | [WP-14.00](../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.00)–[WP-14.06](../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.06) |

| # | Result |
|---|---|
| VC-01 | **25 evidence-established rows, 5 accepted exclusions, 0 unresolved.** Every non-excluded row above names an ArcForges component and a work package. |
| VC-02 | **Three rows record ArcForges being deliberately stricter than the reference**: [AC-01](#rule-ac-01) immutability, [AC-05](#rule-ac-05) owner-side approval, [AC-22](#rule-ac-22) permission during query evaluation. |
| VC-03 | **One row records a direct architectural contradiction resolved in ArcForges' favour**: [AC-13](#rule-ac-13). The nearest real-world implementation of this product category runs a web server on the user's machine, which **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** forbids. That the reference does it is evidence the prohibition is load-bearing (`F-AC-1`). |
| VC-04 | **No AionUI code is copied, translated or ported.** Every disposition is `Reference Only` or `Drop`, so there is no attribution obligation beyond the matrix's own record — and [LP-02](../assurance/reference-coverage/arcchat-aionui.md#rule-lp-02) there states what the obligation would be if that ever changed. |

---

## 4. ArcNotes

### 4.1 Capability map

| Capability | Component | Package |
|---|---|---|
| Notebook, folder, document, block tree | `ArcNotes.Domain` | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| **Inline content model, edit transactions, undo** | `ArcNotes.Domain` + `ArcNotes.Application` (`§2`–`§3` of the editing architecture) | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00), [WP-18.05](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05) |
| Editor interaction, caret, IME, layout | `ArcNotes.Desktop` (`§4`–`§5` there) | [WP-18.01](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) |
| Links, backlinks, outline | `ArcNotes.Application` + derived index | [WP-18.02](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.02) |
| Properties, tags, saved views | `ArcNotes.Domain` + `ArcNotes.Application` | [WP-18.03](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.03), [WP-28](../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) |
| Attachments, preview levels, PDF viewer | `ArcNotes.Infrastructure` + `ArcNotes.Desktop` | [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04); **[PG-12](../assurance/open-gates-register.md#rule-pg-12)** |
| History, checkpoint, trash, recovery | `ArcNotes.Application` + `ArcNotes.Infrastructure` | [WP-18.05](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05), [WP-18.06](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.06) |
| Search and portability | `ArcNotes.Infrastructure` | [WP-19](../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19) |
| ~~Edgeless canvas~~ | **Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded from delivery, no future hook | — |
| ~~Slides~~ | **Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** — excluded from delivery, no future hook | — |
| Saved list and table views over bounded scalar properties | `ArcNotes.Domain` + `ArcNotes.Desktop` | [WP-28](../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) |
| Capability surface | `ArcNotes.LocalRpc` + `ArcNotes.Application` | [WP-18.07](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.07) |

### 4.2 AFFiNE and SiYuan reference verification

41 items across two references — **34 evidence established, 8 accepted exclusions, 0 unresolved**; [AN-14](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-14) is the one compound row, its sharing half excluded and its quota half established. The licence position is the material fact:

| # | Result |
|---|---|
| VN-01 | **AFFiNE's licence is split, and the split is load-bearing.** `packages/backend/**` and `packages/common/native/**` are governed by the Enterprise Edition licence, not MIT ([LP-01](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-lp-01) there). Those subtrees are **permanently ineligible and deliberately unread** — recorded as finding `F-AN-1`. |
| VN-02 | **This is exactly the case [D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013) anticipates**: a repository-root licence does not cover every file. The matrix is the evidence that the rule was applied rather than assumed. |
| VN-03 | **SiYuan is AGPL-3.0.** Under **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**, AGPL material could only ever live inside the AGPL boundary and is **prohibited in the Apache-2.0 mobile, public-client and SDK projects**. No row proposes reuse, so the question stays hypothetical. |
| VN-04 | **`F-AN-2` is now moot.** Neither reference implemented slides, and [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) excludes slides from delivery, so the missing-oracle finding closes by scope rather than by evidence. The same applies to canvas criteria are first-party only. This is stated rather than discovered during implementation. |
| VN-05 | The eight exclusions are recorded individually: journal as a distinct model ([AN-12](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-12)), comments ([AN-13](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-13)), public sharing ([AN-14](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-14)), WebDAV/CalDAV/CardDAV ([AN-32](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-32)), flashcards ([AN-33](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-33)), OCR ([AN-34](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-34)), graph view ([AN-35](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-35)) and publish access ([AN-36](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-36)). Each states its reason rather than being left unmentioned. |
| VN-06 | **The block model, transaction and undo log rows ([AN-01](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-01), [AN-07](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-07), [AN-23](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-23)) are behavioural evidence for `§2`–`§3` of the editing architecture**, which is a first-party design; the correspondence is conceptual, not derived. |

---

## 5. ArcScope

### 5.1 Capability map

| Capability | Component | Package |
|---|---|---|
| Device, connection and transport lifecycle | `ArcScope.Acquisition` | [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) |
| High-rate acquisition, hardware timestamps | `ArcScope.Acquisition` + native primitives (`§2` of the native interop architecture) | [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) |
| Session, capture lifecycle, trigger semantics | `ArcScope.Domain` + `ArcScope.Application` — **managed, never native** | [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) |
| Chunked capture store, honest end marker | `ArcScope.Infrastructure` (`§4` of the desktop data model) | [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) |
| Analysis definitions and evaluation | `ArcScope.Domain` + `ArcScope.Application` | [WP-34](../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) |
| Reporting and evidence | `ArcScope.Application` + `ArcScope.Desktop` | [WP-34](../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) |
| Dashboard and visualisation | `ArcScope.Desktop` | [WP-34](../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) |
| Integration, sync and capability surface | `ArcScope.LocalRpc` + `ArcScope.CloudClient` | [WP-35](../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35) |

### 5.2 Serial-Studio reference verification

31 items — **24 evidence established, 7 accepted exclusions, 0 unresolved**. The licence position dominates:

| # | Result |
|---|---|
| VS-01 | **Serial-Studio is dual GPL-3.0-only / commercial, and its §4 Pro modules are excluded from the GPL grant** ([LP-01](../assurance/reference-coverage/arcscope-serial-studio.md#rule-lp-01), [LP-02](../assurance/reference-coverage/arcscope-serial-studio.md#rule-lp-02) there) — Qt MQTT and SerialBus, MQTT, XY plotting, 3D visualization, and the activation and licensing system. Those are **commercial-only and not open source at all**. |
| VS-02 | **Under [D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013), GPL-only material must not be copied, translated or ported.** Every row is `Reference Only` or an accepted exclusion ([LP-04](../assurance/reference-coverage/arcscope-serial-studio.md#rule-lp-04) there); **no reuse is proposed anywhere in the matrix.** |
| VS-03 | **The transport, framing and buffering rows are behavioural evidence** for what an acquisition pipeline must handle — checksum framing, rolling buffers, hot-path pressure — not a source of implementation. |
| VS-04 | **Seven capabilities are excluded on the record**: MQTT transport ([AS-03](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-03)), the DBC/Modbus/Protobuf importers ([AS-08](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-08)), 3D and XY plot widgets ([AS-14](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-14)), web-engine widgets ([AS-15](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-15)), the gRPC API ([AS-20](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-20)), CLI console-only mode ([AS-26](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-26)) and the licensing and activation system ([AS-27](../assurance/reference-coverage/arcscope-serial-studio.md#rule-as-27)). Four of those — MQTT, XY plotting, 3D visualization and activation — are exactly the **§4 Pro modules excluded from the GPL grant**, so excluding them is a licence necessity as well as a scope decision. |
| VS-05 | **The packaged binary in the reference tree is never executed**, at any stage ([LP-03](../assurance/reference-coverage/arcscope-serial-studio.md#rule-lp-03) there, [MT-04](../assurance/reference-coverage/arcslate-arcvideo.md#rule-mt-04) of the ArcSlate matrix). |

---

## 6. ArcSlate

### 6.1 Capability map

| Capability | Component | Package |
|---|---|---|
| Project, sequence, timeline, clip model | `ArcSlate.Domain` — **exact rational frame rates, no float column** | [WP-36](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) |
| Edit decisions, ripple, markers, undo | `ArcSlate.Domain` + `ArcSlate.Application` | [WP-36](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) |
| Processing graph and parameter model | `ArcSlate.Domain` | [WP-37](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) |
| Playback, audio clock, proxy and cache management | `ArcSlate.Media` + `ArcSlate.Application` | [WP-37](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37) |
| Demux, decode, encode, colour conversion, scaling, resampling | **Native, behind the C ABI** (`§2`–`§3` of the native interop architecture) | [WP-37](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37), [WP-38](../planning/work-packages/38-arcslate-render-and-colour.md#rule-wp-38) |
| Render orchestration and the render queue | `ArcSlate.Application` — **managed; the native pipeline receives an immutable plan** | [WP-38](../planning/work-packages/38-arcslate-render-and-colour.md#rule-wp-38) |
| Colour management and transforms | `ArcSlate.Media` + native colour pipeline | [WP-38](../planning/work-packages/38-arcslate-render-and-colour.md#rule-wp-38) |
| Integration, portability, interchange | `ArcSlate.LocalRpc` + `ArcSlate.Infrastructure` | [WP-39](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) |

### 6.2 ArcVideo and ArcVideoFoundation reference verification

31 items — **29 evidence established, 2 accepted exclusions, 0 unresolved** — the highest evidence ratio of the four, because the reference is closest in domain.

| # | Result |
|---|---|
| VL-01 | **Both references are GPL-3.0-only** ([LP-01](../assurance/reference-coverage/arcslate-arcvideo.md#rule-lp-01) there). **GPL-3.0 → AGPL-3.0-only is not a permitted reuse direction** ([LP-04](../assurance/reference-coverage/arcslate-arcvideo.md#rule-lp-04) there), so no row proposes reuse despite the domain proximity. |
| VL-02 | **ArcForges owning the reference repository does not change its licence** ([LP-03](../assurance/reference-coverage/arcslate-arcvideo.md#rule-lp-03) there). ArcVideo is a documented Olive fork and **the copyright is not solely ArcForges'** ([LP-02](../assurance/reference-coverage/arcslate-arcvideo.md#rule-lp-02) there). |
| VL-03 | **Olive provenance is preserved.** Removing Olive as an independent reference ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005), [OC-01](../assurance/open-gates-register.md#rule-oc-01)) removed an audit obligation, not a provenance obligation: upstream copyright, licence notices and attribution to the Olive authors are retained wherever inherited material requires them ([UD-01](../assurance/open-gates-register.md#rule-ud-01) of the open-gates register). 25 rows are labelled *(upstream-derived)* for exactly this reason. |
| VL-04 | **The two exclusions are multicam ([AL-23](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-23)) and node-based compositing as the user-facing paradigm ([AL-24](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-24)).** ArcSlate's processing graph is an internal model; the reference's editing paradigm is not adopted. |
| VL-05 | **[AL-30](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-30) records ArcVideoFoundation's actual extraction state** and is re-checked on drift ([MT-02](../assurance/reference-coverage/arcslate-arcvideo.md#rule-mt-02) there) — the one row whose value is a fact about the reference rather than about a capability. |
| VL-06 | **The rational-arithmetic and timeline-coordinate rows ([AL-01](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-01), [AL-02](../assurance/reference-coverage/arcslate-arcvideo.md#rule-al-02)) are why the schema stores `frame_rate_num`/`frame_rate_den`** and forbids a float column. The reference is evidence that float frame rates are a defect class, not a style preference. |

---

## 7. Completeness

| Check | Result |
|---|---|
| Every product has a capability map naming components and packages | **Pass** — four products, `§3.1`, `§4.1`, `§5.1`, `§6.1` |
| Every non-excluded reference row has an ArcForges home | **Pass** — all 30 ArcChat rows verified individually in `§3.2`; the remaining 115 rows verified by capability area in `§4.2`, `§5.2`, `§6.2` against the maps in `§4.1`, `§5.1`, `§6.1` |
| Every excluded reference row is excluded on the record | **Pass** — **22 accepted exclusions** across 145 rows (ArcChat 5, ArcNotes 8, ArcScope 7, ArcSlate 2, distribution 1), each with a stated reason |
| Any row proposing reuse carries a provenance record | **Not applicable** — **no row in any matrix proposes reuse** ([PM-02](#rule-pm-02)) |
| Unresolved determinations | **Zero** across all 145 rows; [OC-01](../assurance/open-gates-register.md#rule-oc-01), the one that existed, was closed by user decision ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)) |
| A capability with neither a component nor an exclusion | **None found** ([PM-04](#rule-pm-04)) |

---

## 8. What no product builds

| Not built | Rule |
|---|---|
| A second agent runtime in any product | [CT-06](../requirements/05-ai-and-agent-execution.md#rule-ct-06) of the AI requirements; ArcScope and ArcSlate reach AI through the capability model |
| A product-local approval or permission model | `§2` of the local RPC contract; one security pipeline, owner-side |
| A product-local update or telemetry channel | `§7` of the build architecture; `§2` of the observability architecture |
| A product-local marketplace | [AN-30](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-30) accepted exclusion; the extension catalog is platform-level |
| A host-side web server for remote control | **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**; [AC-13](#rule-ac-13) |
| Any UI shared between Avalonia desktop and MAUI mobile | **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**; [AC-23](#rule-ac-23) |

---

## 9. Verification

| # | Obligation | Where |
|---|---|---|
| PV-01 | Each product's drift check compares its reference against the bound commit and assesses newly introduced material against accepted scope — it does not re-create the matrix | [WP-15.07](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.07), [WP-18.08](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.08), [WP-35](../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35), [WP-39](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) |
| PV-02 | A repository policy test asserts no project references a P/Invoke class outside its owning infrastructure project | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [DR-02](12-native-interop-and-media.md#rule-dr-02) |
| <a id="rule-pv-03"></a>PV-03 | A repository policy test asserts no AGPL-boundary assembly is referenced from an Apache-2.0 project | [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| PV-04 | **Launching any product requires no account** ([ID-01](../requirements/02-identity-account-and-workspace.md#rule-id-01) of the identity requirements), and no product requires ArcChat. **Cloud dependence then differs by product and must be verified as it actually is**: ArcScope capture/analysis and ArcSlate editing/render are native and run without Cloud; ArcNotes and ArcChat are Cloud-authoritative, so what is verified is that an **enrolled, hydrated** workspace stays editable and searchable through an outage with pending edits durably recoverable ([PR-02](../requirements/products/arcnotes.md#rule-pr-02) and [CL-05](../requirements/products/arcnotes.md#rule-cl-05) of the ArcNotes requirements). Verifying "no account" against ArcNotes or ArcChat *content* would be verifying a product that was not specified | [WP-18](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18) gate 10, [WP-15.05](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.05), [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33), [WP-36](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36) completion gates |
| PV-05 | The AFFiNE Enterprise-Edition subtrees remain unread and unreferenced across every drift check | [WP-18.08](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.08) |
| PV-06 | No packaged reference binary is executed at any stage | Matrix [MT-04](../assurance/reference-coverage/arcslate-arcvideo.md#rule-mt-04); the reference-coverage README |
