# Reference Coverage Matrix — ArcChat / AionUi

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete**
> Governing authority: **D-012** (matrix required before ArcChat implementation planning is finalized), **D-013** (reuse and provenance)
> Consuming product: **ArcChat** — [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md)

---

## 1. Source identity

| Field | Value |
|---|---|
| Repository | `github.com/iOfficeAI/AionUi` |
| Local path | `C:\MyFile\ArcForges\AionUi` |
| Commit | `29c9271a5` |
| Commit date | 2026-07-14 |
| Reviewed on | 2026-09-05 |
| Reviewer | Architecture Owner (design stage) |

---

## 2. Licence and provenance position

| Scope | Evidence | Finding |
|---|---|---|
| Repository root | `LICENSE` — Apache License Version 2.0 header | **Apache-2.0** |
| Subtree exceptions | No differing `LICENSE` file found under `packages/`, `mobile/` or `docs/` | None found in the reviewed scope |
| Bundled third-party in packaged output | `StartArcForges/AionUi/LICENSE.electron.txt`, `LICENSES.chromium.html` | Electron and Chromium notices ship with the packaged product; they belong to the runtime, not to AionUi's own source |

**Position under D-013.** Apache-2.0 is permissive and compatible with **both** ArcForges licence boundaries. AionUi is therefore the **only** reference in the programme whose material could, after a per-file provenance record, enter the Apache-2.0 mobile and public-client boundary.

**This matrix nevertheless proposes no reuse.** Every row below is `Reference Only` or an accepted exclusion, for reasons stated per row — principally that AionUi is a TypeScript/Electron application and ArcForges is C#/Avalonia under Native AOT, so its expression is not transferable even where its licence would permit it.

| # | Rule |
|---|---|
| LP-01 | **File-level clearance is not inferred from the root licence.** Should any future row propose reuse, the specific files receive their own check and the ten-field record. |
| LP-02 | **Attribution obligation if ever reused**: Apache-2.0 §4 requires retaining copyright, patent, trademark and attribution notices, and stating modification. Recorded here so it is not discovered later. |

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| Product requirement documents | `docs/prds/{assistants,conversations,cron,pet,previews,remote,settings,teams,workspaces}` |
| Desktop application source | `packages/desktop/src/{common,process,preload,renderer}` |
| Conversation and agent model | `packages/desktop/src/common/chat/**`, `packages/desktop/src/common/types/agent/**` |
| Host bridges | `packages/desktop/src/process/bridge/**` |
| Update and distribution | `packages/desktop/src/process/services/{autoUpdaterService,updateFeed,cdnGenericProvider,installerLastFailure}.ts`, `common/update/**`, `electron-builder.yml` |
| Web surfaces | `packages/web-host/**`, `packages/web-cli/**` |
| Mobile surface | `mobile/**` |
| Guides | `docs/guides/{cdp,deploy-server,hub-testing,webui}.md`, `docs/guides/acp-image-output.zh-CN.md` |

**Not read, and why:** `node_modules`, lockfiles and build output — no design evidence. `patches/**` — upstream dependency patches, out of ArcForges scope. `homebrew/**` — a distribution channel ArcForges does not use (**D-014**).

---

## 4. Item-level matrix

Disposition vocabulary is **D-013**'s: Copy · Rewrite · Improve · Replace · Reference Only · Drop.

| # | Capability / behaviour | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|
| AC-01 | Conversation, message and streaming assembly | `common/chat/chatLib.ts`, `docs/prds/conversations` | `products/arcchat.md` §conversation model; `WP-15.00` | Reference Only | Behavioural evidence for streaming interruption and message identity; ArcForges' immutability-on-commit rule is stricter than the reference | Apache-2.0; no reuse proposed | Reference behaviour observation, then first-party tests | Product Owner | Evidence established |
| AC-02 | Slash commands and availability | `common/chat/slash/{types,availability,mergeSlashCommands,guidSlashCommands}.ts` | `products/arcchat.md` §command surface; `WP-15.00`, `WP-31.01` | Reference Only | Confirms that command availability must be computed, not static — ArcForges routes this through the capability model instead | Apache-2.0; no reuse proposed | First-party test: availability agrees with capability availability (`WP-10.02`) | Product Owner | Evidence established |
| AC-03 | `@`-mention context binding | `common/chat/atCommandParser.ts` | `06-knowledge-search-and-retrieval.md` §context; `WP-20.00` | Reference Only | Evidence that context selection is explicit user action; ArcForges additionally bounds and freezes context | Apache-2.0; no reuse proposed | First-party test: context frozen at invocation | Architecture Owner | Evidence established |
| AC-04 | Tool-call normalisation | `common/chat/normalizeToolCall.ts` + `normalizeToolCall.test.ts` | `05-ai-and-agent-execution.md` §invocation; `WP-16.00` | Reference Only | Evidence that heterogeneous provider tool-call shapes need normalisation at the boundary; ArcForges normalises into the typed capability model | Apache-2.0; no reuse proposed | First-party test: every provider shape maps to one invocation record | Architecture Owner | Evidence established |
| AC-05 | Approval store | `common/chat/approval/ApprovalStore.ts` | `07-security-privacy-and-trust.md` §approval; `WP-11.03` | Reference Only | Evidence that approval needs durable state; ArcForges requires owner-side enforcement, which the reference does not have | Apache-2.0; no reuse proposed | First-party test: owner-side refusal regardless of caller claim (`WP-14.04`) | Security and Privacy Owner | Evidence established |
| AC-06 | ACP agent integration | `common/chat/acpToolCallOutput.ts`, `common/chat/slash/acpMapping.ts`, `common/types/agent/remoteAgentTypes.ts` | **Accepted exclusion** — external-agent integration is excluded by **P2-006** (`EA-01`–`EA-06`) | Drop | The ACP adapter shape was previously retained as evidence for an external-agent adapter. That capability is now excluded outright, so the row carries no design obligation | Apache-2.0; no reuse proposed | First-party test: external agent work produces ArcForges Tasks with leases | Architecture Owner | Accepted exclusion |
| AC-07 | MCP client and built-in MCP server | `renderer/hooks/mcp/**`, `process/resources/builtinMcp/{constants,imageGenServer}.ts` | `08-extensions-and-developer-platform.md` §MCP; `WP-41.07`; **V-02** | Reference Only | Evidence that MCP is an integration adapter, not an internal protocol — consistent with **V-02**'s vocabulary-collision finding | Apache-2.0; no reuse proposed | Vocabulary mapping record (`VG-02`) | Architecture Owner | Evidence established |
| AC-08 | Agent detection and hub types | `common/types/agent/{detectedAgent,hub}.ts` | `products/arcchat.md` §capability hub; `WP-17.00` | Reference Only | Confirms a hub/registry concept is needed; ArcForges' registry is contract-typed and lease-based, which the reference is not | Apache-2.0; no reuse proposed | First-party test: registration, lease and re-registration (`WP-08.02`) | Architecture Owner | Evidence established |
| AC-09 | Assistant / agent profile | `docs/prds/assistants`, `common/types/agent/assistantTypes.ts` | `products/arcchat.md` §agent profile; `WP-15.03` | Reference Only | Evidence that model, mode and behaviour bundle into a reusable profile | Apache-2.0; no reuse proposed | First-party lifecycle tests | Product Owner | Evidence established |
| AC-10 | Workspaces | `docs/prds/workspaces`, `common/adapter/workspaceMapper.ts` | `02-identity-account-and-workspace.md` §workspace | Reference Only | ArcForges' workspace is an entitlement and data scope from day one (**D-002**-era decision), a stronger concept than the reference's | Apache-2.0; no reuse proposed | First-party tests in `WP-22.00` | Product Owner | Evidence established |
| AC-11 | Teams / multi-agent | `docs/prds/teams`, `common/adapter/teamMapper.ts`, `renderer/pages/team` | **Accepted exclusion** — agent teams and sub-agents are excluded by **P2-006** (`EA-08`) | Drop | Previously excluded as beyond first launch; now excluded outright. There is no agent-team interface and no sub-agent execution model | Apache-2.0; no reuse | — | Product Owner | Accepted exclusion |
| AC-12 | Cron / scheduled tasks | `docs/prds/cron`, `renderer/pages/cron` | `05-ai-and-agent-execution.md` §automation; `WP-17.04` | Reference Only | Evidence that scheduled execution is a distinct concept from a task; ArcForges separates Automation (when) from Plan (how) | Apache-2.0; no reuse proposed | First-party test: automation never gains implicit permission | Product Owner | Evidence established |
| AC-13 | Remote access / WebUI | `docs/prds/remote`, `packages/web-host/**`, `docs/guides/webui.md`, `process/bridge/webuiBridge.ts` | `products/arcchat-mobile-and-web.md`; `WP-26`, `WP-49` | Reference Only | **Material divergence recorded**: the reference exposes a host-side web server. **D-010** forbids that shape for ArcForges — remote reaches a desktop only through Cloud and a durable tool request | Apache-2.0; no reuse proposed | First-party test: no cloud-initiated local connection, no local listener (`WP-26.01`, `WP-31.06`) | Architecture Owner | Evidence established |
| AC-14 | Previews | `docs/prds/previews` | `09-shared-desktop-experience.md` §preview and handoff; `WP-17.06` | Reference Only | Evidence for thin preview; ArcForges adds rich handoff to the owning product | Apache-2.0; no reuse proposed | First-party handoff tests | Product Owner | Evidence established |
| AC-15 | Desktop pet | `docs/prds/pet`, `process/pet/**`, `renderer/pet/**` | **Accepted exclusion** — no ArcForges requirement | Drop | An ambient companion surface is outside the accepted ArcChat scope and would create unrequested product scope | Apache-2.0; no reuse | — | Product Owner | Accepted exclusion |
| AC-16 | Settings | `docs/prds/settings`, `renderer/pages/settings`, `process/bridge/systemSettingsBridge.ts` | `09-shared-desktop-experience.md` §scoped settings; `WP-10.03` | Reference Only | ArcForges settings are scope-resolved and explainable, which the reference's flat model is not | Apache-2.0; no reuse proposed | First-party test: effective value explainable to its source scope | Product Owner | Evidence established |
| AC-17 | Auto-update and update feed | `process/services/{autoUpdaterService,updateFeed,cdnGenericProvider}.ts`, `common/update/**` | `10-distribution-update-and-support.md` §3; `WP-02`, `WP-50.02` | Reference Only | **Migration evidence**: a generic CDN provider plus a self-hosted feed is the same shape ArcForges adopts under `P2-001`; the reference's Electron updater is not transferable | Apache-2.0; no reuse proposed | Update matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |
| AC-18 | Update failure diagnostics | `process/services/{autoUpdateDiagnostics,installerLastFailure}.ts` | `10-distribution-update-and-support.md` §3; `WP-50.02` | Reference Only | Evidence that installer failure needs its own persisted diagnostic path — a case ArcForges' update matrix must cover | Apache-2.0; no reuse proposed | First-party test: interrupted install recovery | Release Engineering Owner | Evidence established |
| AC-19 | Notification bridge | `process/bridge/notificationBridge.ts` | `09-shared-desktop-experience.md` §attention; `WP-10.04` | Reference Only | ArcForges classifies attention by durability, which the reference does not | Apache-2.0; no reuse proposed | First-party test: missed transient notification loses no durable item | Product Owner | Evidence established |
| AC-20 | Theming | `common/theme/**`, `renderer/theme/**`, `docs/theming` | `09-shared-desktop-experience.md` §tokens; `WP-10.00` | Reference Only | Evidence that theming must be tokenised; ArcForges additionally forbids raw literals in components | Apache-2.0; no reuse proposed | Policy test: no raw colour literal | Product Owner | Evidence established |
| AC-21 | Crash and feedback | `process/feedback/**`, `process/bridge/feedbackBridge.ts` | `10-distribution-update-and-support.md` §7.1; `WP-12.05` | Reference Only | ArcForges requires generate → show → approve → send, stricter than the reference | Apache-2.0; no reuse proposed | First-party test: no report sent without approval | Security and Privacy Owner | Evidence established |
| AC-22 | Search adapter | `common/adapter/searchMapper.ts` | `06-knowledge-search-and-retrieval.md`; `WP-15.05` | Reference Only | ArcForges applies permission during query evaluation, which the reference does not | Apache-2.0; no reuse proposed | First-party test: refused content invisible in results and counts | Product Owner | Evidence established |
| AC-23 | Mobile companion | `mobile/**` (React Native / Expo) | `products/arcchat-mobile-and-web.md`; `WP-30`, `WP-31` | Reference Only | **Technology divergence recorded**: the reference's mobile stack is React Native; ArcForges is .NET MAUI under **D-008**. Behavioural evidence only | Apache-2.0; no reuse proposed — and any reuse would be prohibited by the Apache-boundary rule only if it were GPL-family, which it is not; the barrier here is technical, not licensing | First-party mobile tests (`WP-31`) | Product Owner | Evidence established |
| AC-24 | Web CLI / admin password bootstrap | `packages/web-cli/{index,ensureAdminPassword,browser}.ts` | **Accepted exclusion** — ArcForges has no host-side admin password model | Drop | Contradicts **D-015** and the identity model: ArcForges uses passkey-first cloud identity, not a locally bootstrapped admin credential | Apache-2.0; no reuse | — | Security and Privacy Owner | Accepted exclusion |
| AC-25 | CDP / browser automation guide | `docs/guides/cdp.md` | **Accepted exclusion** — no ArcForges requirement in the accepted scope | Drop | Browser automation as a first-party capability is not in the accepted ArcChat scope | Apache-2.0; no reuse | — | Product Owner | Accepted exclusion |
| AC-26 | Self-hosted server deployment | `docs/guides/deploy-server.md` | `products/arcforges-cloud.md` §self-host; `WP-45` | Reference Only | Evidence about self-host expectations; ArcForges' self-host boundary is defined by its own cloud requirements | Apache-2.0; no reuse proposed | First-party self-host boundary tests | Operations Owner | Evidence established |
| AC-27 | Image generation via MCP | `common/chat/imageGenCore.ts`, `common/config/imageGenerationMcpEnv.ts`, `process/resources/builtinMcp/imageGenServer.ts` | **Accepted exclusion** as a first-party capability; retained as evidence for `08-extensions-and-developer-platform.md` §MCP | Drop as capability; Reference Only as integration evidence | Image generation is not in the accepted four-product scope (**D-002**); the MCP integration shape is separately useful evidence | Apache-2.0; no reuse | Vocabulary mapping record (`VG-02`) | Product Owner | Accepted exclusion |
| AC-28 | Document handling in chat | `common/chat/document/**` | `products/arcchat.md` §attachments; `WP-15.02` | Reference Only | ArcForges stores attachments by reference with integrity verification and never embeds bodies | Apache-2.0; no reuse proposed | First-party test: no attachment body embedded in message storage | Product Owner | Evidence established |
| AC-29 | Packaging configuration | `packages/desktop/electron-builder.yml`, `entitlements.plist` | `14-build-packaging-and-release.md`; `WP-50.02` | Reference Only | Packaging evidence for signing entitlements and per-platform targets; the toolchain differs entirely | Apache-2.0; no reuse proposed | Release matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |
| AC-30 | Hub testing guide | `docs/guides/hub-testing.md` | `03-local-ipc-and-process-model.md`; `WP-14` | Reference Only | **Test evidence**: names the hub scenarios worth covering — registration, restart, reconnection — which ArcForges' first-slice suite must also cover | Apache-2.0; no reuse proposed | `WP-14.00`, `WP-14.06` scenario coverage | Architecture Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 30 rows across all 8 areas |
| Every row carries all nine required fields | **Pass** |
| Every row has exactly one completeness state | **Pass** — 30 rows: 24 evidence established, 6 accepted exclusions (`AC-06`, `AC-11`, `AC-15`, `AC-24`, `AC-25`, `AC-27`), 0 unresolved. **Recounted 2026-09-06 after P2-006**; `AC-06` moved to exclusion because external-agent integration is no longer a design obligation |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** — no row creates a new requirement |
| Every `Drop` row states why it is excluded | **Pass** |
| Any row proposing reuse carries a provenance-record obligation | **Not applicable** — no row proposes reuse |
| Licence position determined below the repository root | **Pass** — subtrees checked; none differ |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

Three items produced material evidence rather than confirmation. None creates a new requirement; each confirms or sharpens an existing one.

| # | Finding | Effect |
|---|---|---|
| F-AC-1 | The reference exposes remote control by running a **web server on the user's machine** (`AC-13`). | **Confirms D-010's prohibition is load-bearing, not theoretical.** The nearest real-world implementation of this product category does exactly what ArcForges forbids. `WP-26` and `WP-31` already assert the prohibition structurally; no change needed. |
| F-AC-2 | Update delivery uses a **generic CDN provider plus a self-hosted feed** (`AC-17`). | Independent confirmation of the shape `P2-001` adopts — the product's own feed remains authoritative and storage is replaceable. No change needed. |
| F-AC-3 | The reference's mobile companion is a **separate technology stack** from its desktop (`AC-23`). | Confirms **D-021**'s no-shared-ViewModel position is the normal outcome rather than a restriction. No change needed. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | This matrix is bound to commit `29c9271a5`. `WP-15` re-checks the reference for drift against that commit and for newly introduced material; it does not re-create the matrix. |
| MT-02 | A new capability appearing upstream is assessed against the accepted ArcChat scope; it does not become a requirement by appearing. |
| MT-03 | A disposition change is recorded here with its reason and its date. |
