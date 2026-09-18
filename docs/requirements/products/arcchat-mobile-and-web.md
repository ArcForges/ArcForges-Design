# Android companion and Web companion — Product Requirements

[P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012) current implementation authorities: [Complete Android experience](../../experience/02-android-companion.md); [One-application targeting and transport](../../architecture/contracts/10-application-scope-and-streams.md).
> Effective scope: [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012) and [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) amend the technology and application ownership below. **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Product identities: `companion`, `chat.arcforges.com`
> Governing authority: **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** (Apache-2.0 mobile boundary), **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)** (web technology), **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Android Kotlin/Jetpack Compose; iOS outside scope), **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**/**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** (surfaces), **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**/**[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)** (consumption-only)
> Companions: [`arcchat.md`](arcchat.md), [`arcforges-web.md`](arcforges-web.md), [`../03-cloud-services-and-sync.md`](../03-cloud-services-and-sync.md), [`../05-ai-and-agent-execution.md`](../05-ai-and-agent-execution.md)

> **Android companion and Web companion are the Cloud Continuity and Remote Agent Companion for ArcChat.**

The companion loop:

```
See → Approve → Steer → Continue → Start remote work → Receive results
```

---

## 1. Identity and boundaries

| # | Requirement |
|---|---|
| <a id="rule-id-01"></a>ID-01 | **Mobile and Web are companion surfaces, not mobile or web editions of the three professional desktop products** ([I-027](../01-normative-glossary-and-invariants.md#rule-i-027)). There is no ArcNotes Mobile editor, no ArcScope Mobile editor and no ArcSlate Mobile editor. |
| <a id="rule-id-02"></a>ID-02 | **Mobile and Web are not one responsive product.** They share domain semantics and contracts; their information architecture, interaction model and capability set differ deliberately. |
| <a id="rule-id-03"></a>ID-03 | **Mobile and Web connect only to Cloud** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). They must never scan a LAN, discover a desktop application runtime, or address a named pipe or domain socket. |
| <a id="rule-id-04"></a>ID-04 | **`Companion ≠ thin remote controller`** (`§20`). Both surfaces are useful with no desktop online, through cloud chat, cloud tasks, projects, search, automation and continuity. |
| <a id="rule-id-05"></a>ID-05 | **A `Remote Task` is not remote desktop** ([I-120](../01-normative-glossary-and-invariants.md#rule-i-120)). ArcForges provides a **semantic remote agent**, never a general screen-and-input remote tool. |
| <a id="rule-id-06"></a>ID-06 | **Android companion is Apache-2.0** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**), together with the mobile-only libraries, the ArcForges-owned public protocol specifications required for its interoperability, and their wire schemas, DTOs and client libraries. It must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation, directly or transitively. |
| <a id="rule-id-07"></a>ID-07 | **Base ViewModel patterns are not shared between Avalonia desktop and Kotlin Android mobile** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). Each UI stack owns its implementation. |
| <a id="rule-id-08"></a>ID-08 | Android production uses Kotlin/Jetpack Compose on Android ART. iOS and multiplatform sharing are outside the current scope under P2-010. |
| <a id="rule-id-09"></a>ID-09 | **Web companion is a deployment of the single `ArcForges.Web.App` React/TypeScript codebase** (**[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**, **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**), served at `chat.arcforges.com`. |

### 1.1 Responsibility split

| Surface | Responsibility |
|---|---|
| **Desktop** | Native product surface, cached projections/drafts, local tool execution and the application runtime; Cloud owns AI execution |
| **Mobile** | Attention, approval, remote control, result consumption — with cloud chat and tasks in their own right |
| **Web** | Cloud chat, tasks, projects, search, automation, continuity — closer to desktop in depth, without local capability |

---

## 2. Object model on the companion

| # | Requirement |
|---|---|
| <a id="rule-om-01"></a>OM-01 | **The core objects on Mobile and Web are still ArcChat objects**: conversations, tasks, projects, artifacts, approvals, automations. |
| <a id="rule-om-02"></a>OM-02 | **Professional product objects appear through reference and preview only.** A companion surface never holds a complete writable copy of an ArcScope session, an ArcNotes document or an ArcSlate project ([I-060](../01-normative-glossary-and-invariants.md#rule-i-060)). |
| <a id="rule-om-03"></a>OM-03 | The full execution semantics are those of [`../05-ai-and-agent-execution.md`](../05-ai-and-agent-execution.md); the companion is a surface, never a second model. |

---

## 3. Information architecture

| Surface | Home |
|---|---|
| **Mobile** | **"What needs me now?"** — attention first: approvals, waiting tasks, results, notifications |
| **Web** | Closer to desktop: composer, recent, tasks, projects, artifacts |

| # | Requirement |
|---|---|
| <a id="rule-ia-01"></a>IA-01 | **Mobile must not open as a large chat composer.** Chat must not occupy the entire home surface; attention leads. |
| <a id="rule-ia-02"></a>IA-02 | Mobile navigation prioritises: Home/Attention, Tasks, Chats, Artifacts, Devices, Settings. |
| <a id="rule-ia-03"></a>IA-03 | **Approval is reachable directly from Home attention**, in one step. |
| <a id="rule-ia-04"></a>IA-04 | Web navigation may approach the desktop layout: Home, Chats, Tasks, Artifacts, Projects, Automations, Search, Settings. |

---

## 4. Device presence and remote availability

| # | Requirement |
|---|---|
| <a id="rule-dp-01"></a>DP-01 | **Device Presence is a core companion foundation**: which desktops exist, which are online, when last seen, product version, and per-product readiness. |
| <a id="rule-dp-02"></a>DP-02 | **`Device Presence ≠ Device Trust`** ([I-250](../01-normative-glossary-and-invariants.md#rule-i-250)), and **`Device Online ≠ Remote Agent Enabled`** ([I-251](../01-normative-glossary-and-invariants.md#rule-i-251)). |
| <a id="rule-dp-03"></a>DP-03 | **Presence is not a per-second heartbeat display.** It is a coarse, honest, low-noise state, and never presented as more precise than it is. |
| <a id="rule-dp-04"></a>DP-04 | Show per-device application installations with product, running state, compatibility, instance epoch and available capabilities. Presence never grants access. |
| <a id="rule-dp-05"></a>DP-05 | **Remote availability is finer-grained than "device online"**: remote enabled, capability permitted, product installed, product running, workspace matching. |
| <a id="rule-dp-06"></a>DP-06 | **The device selector must not expose underlying network detail.** It presents devices, not transports or addresses. |
| <a id="rule-dp-07"></a>DP-07 | **Remote agent enablement must be performed on the desktop the first time** ([TR-04](../02-identity-account-and-workspace.md#rule-tr-04)). It cannot be enabled remotely. |
| <a id="rule-dp-08"></a>DP-08 | **When remote agent is disabled**, desktop capabilities become unavailable with a clear reason; existing cloud capability is unaffected. |

---

## 5. Remote tasks

**Remote Task** is a Cloud agent task initiated from a companion, optionally using authorized desktop tools. Desktop/Cloud/Hybrid labels describe tool locality, never multiple agent runtimes.

| # | Requirement |
|---|---|
| <a id="rule-rt-01"></a>RT-01 | A task fixes either Cloud-only work or one explicit product/device/installation target. The agent loop always runs in Cloud; every device step uses that same product target. |
| <a id="rule-rt-02"></a>RT-02 | Require explicit application-target confirmation. A single eligible installation may be preselected but is never silently selected or substituted. |
| <a id="rule-rt-03"></a>RT-03 | The application target and realm/workspace profile are durable task attributes, not a transient UI selection. |
| <a id="rule-rt-04"></a>RT-04 | Cloud-only work can proceed without a desktop; desktop-required work uses TaskState=waiting with reasonFacet=device until that application is available. |
| <a id="rule-rt-05"></a>RT-05 | **Local-only data must never be uploaded to Cloud merely because the desktop is offline** ([OW-08](../05-ai-and-agent-execution.md#rule-ow-08)). The task waits. |
| <a id="rule-rt-06"></a>RT-06 | **A remote task is durable by default** ([EX-02](../05-ai-and-agent-execution.md#rule-ex-02)). It never depends on the mobile session's lifetime. |
| <a id="rule-rt-07"></a>RT-07 | **A created remote task enters the Task Center immediately**, before any execution begins. |
| <a id="rule-rt-08"></a>RT-08 | Task presentation distinguishes Cloud-only work from work waiting for or using desktop tools. Tool location never implies a desktop agent runtime. |
| <a id="rule-rt-09"></a>RT-09 | **Cloud tasks can be created with no desktop at all** (`§9` of the cloud requirements). |
| <a id="rule-rt-10"></a>RT-10 | **Hybrid task presentation must be clear**: which steps ran in Cloud, which require a device, and what is currently blocking. |

---

## 6. Approval

**Approval is a first-class mobile surface**, not a notification with a button.

| # | Requirement |
|---|---|
| <a id="rule-ap-01"></a>AP-01 | An approval card shows at minimum: what will happen, to which resource at which revision, the effective risk, the execution location and device, the requesting task and actor chain, the expiry, and the consequences. |
| <a id="rule-ap-02"></a>AP-02 | **An approval must never be an abstract tool name.** "Allow `notes.write`?" is prohibited; the concrete effect is described. |
| <a id="rule-ap-03"></a>AP-03 | Risk handling follows [`../07-security-privacy-and-trust.md`](../07-security-privacy-and-trust.md) §4: R0/R1 generally proceed inside an authorised scope; R2 requires a clear preview and confirmation; R3 requires explicit approval and often remote step-up; **R4 requires local confirmation on a trusted device by default** ([LP-02](../07-security-privacy-and-trust.md#rule-lp-02), [TR-06](../07-security-privacy-and-trust.md#rule-tr-06)). |
| <a id="rule-ap-04"></a>AP-04 | **R4 local confirmation is a hard boundary.** Mobile and Web may only prompt the user to return to a trusted device. |
| <a id="rule-ap-05"></a>AP-05 | **Step-up authentication is required for high-risk approval**; an already-open ordinary session is insufficient. |
| <a id="rule-ap-06"></a>AP-06 | **Every approval expires** ([AP-07](../07-security-privacy-and-trust.md#rule-ap-07) in the security requirements). |
| <a id="rule-ap-07"></a>AP-07 | **A resource revision change invalidates the approval** for that exact effect; the action is rebased, the preview regenerated, and approval re-requested ([AP-06](../07-security-privacy-and-trust.md#rule-ap-06) there). |
| <a id="rule-ap-08"></a>AP-08 | **A rejected approval does not necessarily fail the task** ([AP-10](../07-security-privacy-and-trust.md#rule-ap-10) there). The agent may take an alternative, skip an optional step, or ask. |
| <a id="rule-ap-09"></a>AP-09 | **A processed approval must never continue to appear as actionable.** |

---

## 7. Steering

| # | Requirement |
|---|---|
| <a id="rule-st-01"></a>ST-01 | **Steering and approval are separate** ([I-098](../01-normative-glossary-and-invariants.md#rule-i-098)). |
| <a id="rule-st-02"></a>ST-02 | **Steering is not an ordinary conversation message** ([I-099](../01-normative-glossary-and-invariants.md#rule-i-099)). It is bound to a task. |
| <a id="rule-st-03"></a>ST-03 | Task detail provides a **dedicated steering composer**. |
| <a id="rule-st-04"></a>ST-04 | **Steering does not rewrite task history** ([SG-02](../05-ai-and-agent-execution.md#rule-sg-02), [SG-03](../05-ai-and-agent-execution.md#rule-sg-03)). It produces an immutable steering event; the original intent is retained. |
| <a id="rule-st-05"></a>ST-05 | **Steering does not guarantee immediate effect** ([SG-05](../05-ai-and-agent-execution.md#rule-sg-05)). Its application timing — applied, queued to a safe point, or not applicable — is shown. |
| <a id="rule-st-06"></a>ST-06 | **Cancel is expressed accurately** ([CN-01](../05-ai-and-agent-execution.md#rule-cn-01)): `CancelRequested`, then `Canceling`, then `Canceled`, with completed effects listed. |
| <a id="rule-st-07"></a>ST-07 | **Steering that expands scope may affect budget**, and the budget impact is shown before it takes effect ([BG-06](../05-ai-and-agent-execution.md#rule-bg-06)). |

---

## 8. Notifications

Five categories, with different default behaviour:

| Category | Default |
|---|---|
| **Needs approval** | Push |
| **Task completed** | Push, if the user asked for it or the task was long |
| **Task failed / needs attention** | Push |
| **Security event** | **Always** — cannot be disabled |
| **Informational / marketing** | Off by default, separately opt-in |

| # | Requirement |
|---|---|
| <a id="rule-nt-01"></a>NT-01 | **Ordinary chat replies do not push every message by default.** |
| <a id="rule-nt-02"></a>NT-02 | **Task progress is never pushed incrementally.** Progress is pulled in-app. |
| <a id="rule-nt-03"></a>NT-03 | **Lock-screen content is not sensitive by default** ([`NT-03`](../03-cloud-services-and-sync.md#rule-nt-03) in the cloud requirements). Full content requires an explicit preview opt-in. |
| <a id="rule-nt-04"></a>NT-04 | **Security notifications cannot be fully disabled** ([SN-02](../02-identity-account-and-workspace.md#rule-sn-02)). |
| <a id="rule-nt-05"></a>NT-05 | **Notification actions are safe**: an action opens the corresponding surface. **A push button is never an authorization token** ([AD-01](../07-security-privacy-and-trust.md#rule-ad-01)). |
| <a id="rule-nt-06"></a>NT-06 | **Notifications deduplicate**: one condition updates one item ([AT-03](../09-shared-desktop-experience.md#rule-at-03)). |
| <a id="rule-nt-07"></a>NT-07 | An in-app **Notification Center / Attention Inbox** holds the durable state. **A push notification is not durable attention state** ([NT-04](../03-cloud-services-and-sync.md#rule-nt-04) in the cloud requirements) — missing a push never loses a pending approval. |

---

## 9. Artifacts and result consumption

**Artifacts are the most important result-consumption object on the companion.**

Three preview layers:

| Layer | Meaning |
|---|---|
| **Summary** | Title, kind, owner, provenance, size, availability |
| **Light preview** | Text excerpt, image, small document render, transcript snippet |
| **Full access** | Download, or handoff to the owning desktop product |

| # | Requirement |
|---|---|
| <a id="rule-ar-01"></a>AR-01 | **Mobile must not attempt to fully edit an ArcNotes document.** No complete block editor on mobile. |
| <a id="rule-ar-02"></a>AR-02 | **Web companion must not quietly become an ArcNotes Web editor.** Its role is preview, continuity and agent. |
| <a id="rule-ar-03"></a>AR-03 | **Artifact availability is shown truthfully**: available in cloud, on a device only, requires download, requires the owning product, or unavailable. |
| <a id="rule-ar-04"></a>AR-04 | An assistant-generated artifact belongs to its frozen application/Cloud execution scope and existing resource owner. Shared UI does not create a separate ArcChat owner or another product's write permission. |
| <a id="rule-ar-05"></a>AR-05 | **Remote result delivery prefers small results with large source data kept local.** A summary, a report, a rendered excerpt — not the whole source. |
| <a id="rule-ar-06"></a>AR-06 | Open an available Cloud artifact in the companion's bounded preview or show its owning desktop target. Current scope has no generic cross-product handoff command. |
| <a id="rule-ar-07"></a>AR-07 | A device-only artifact is visibly unavailable until an explicitly approved own-application upload tool produces a verified Cloud resource. Do not invent a generic transfer Task or report upload completion before verification. |
| <a id="rule-ar-08"></a>AR-08 | **A large artifact prompts before transfer**, with size and estimated cost. |
| <a id="rule-ar-09"></a>AR-09 | **A cellular policy exists**: download over cellular, large transfers on Wi-Fi only, and a hard size threshold ([SY-36](../03-cloud-services-and-sync.md#rule-sy-36)). |
| <a id="rule-ar-10"></a>AR-10 | **Mobile artifact preview cache is bounded and evictable** (`§11`). |
| <a id="rule-ar-11"></a>AR-11 | **Cloud task results and remote desktop task results share one artifact experience**, differing only in source and availability. |

---

## 10. Continuity

> **Continuity ≠ mirroring the interface** ([I-125](../01-normative-glossary-and-invariants.md#rule-i-125)).

| # | Requirement |
|---|---|
| <a id="rule-cn-01"></a>CN-01 | Conversation continuity uses Cloud-acknowledged history in the selected owner workspace. |
| <a id="rule-cn-02"></a>CN-02 | Unsent desktop drafts and unsynchronized local tool/file content do not become visible on a phone merely because the account matches. |
| <a id="rule-cn-03"></a>CN-03 | Task visibility follows Cloud task authorization; it does not disclose unselected local tool inputs or device files. Local-only conversation execution is not a separate supported mode. |
| <a id="rule-cn-04"></a>CN-04 | **Task continuity is by identity**: one `TaskId` observed and steered from desktop, web and mobile — not three sessions ([SN-01](../05-ai-and-agent-execution.md#rule-sn-01)). |
| <a id="rule-cn-05"></a>CN-05 | **Task detail may be simplified per device** without becoming a different object. |
| <a id="rule-cn-06"></a>CN-06 | **Draft continuity is optional and explicit**: cloud draft sync is a user choice, not a default. |
| <a id="rule-cn-07"></a>CN-07 | Project continuity uses the same Cloud project identities, references and tasks. Native pending drafts are not advertised as acknowledged content. |

---

## 11. Search on the companion

| # | Requirement |
|---|---|
| <a id="rule-se-01"></a>SE-01 | **Cloud search searches only what Cloud can access** ([SR-08](../06-knowledge-search-and-retrieval.md#rule-sr-08) in the knowledge requirements). |
| <a id="rule-se-02"></a>SE-02 | **Search results show availability** — cloud, device-only, unavailable. |
| <a id="rule-se-03"></a>SE-03 | **Finding a local resource must never automatically wake the desktop.** Reaching it is an explicit remote search or remote task ([SR-11](../06-knowledge-search-and-retrieval.md#rule-sr-11) there). |
| <a id="rule-se-04"></a>SE-04 | **Search and Ask remain strictly separated** ([I-147](../01-normative-glossary-and-invariants.md#rule-i-147)). |
| <a id="rule-se-05"></a>SE-05 | A cloud search result **may be added to chat context**, and doing so is an explicit act that defines the AI processing scope. |

---

## 12. AI on the companion

| # | Requirement |
|---|---|
| <a id="rule-ai-01"></a>AI-01 | No device supplies a local model. Mobile, Web and Desktop invoke the same Cloud AI service; only authorized native tools depend on a desktop being online. |
| <a id="rule-ai-02"></a>AI-02 | Cloud AI requires the selected service realm and its service eligibility; Cloud-only work requires no desktop. |
| <a id="rule-ai-03"></a>AI-03 | No customer provider-key submission or BYOK mode exists on any surface. Operator provider credentials remain server-side deployment secrets. |
| <a id="rule-ai-04"></a>AI-04 | The selected service realm, model policy and actual tool targets are visible consistently across surfaces. |
| <a id="rule-ai-05"></a>AI-05 | A conversational turn and a durable agent task both use Cloud AI; neither transfers a model loop to the desktop. |
| <a id="rule-ai-06"></a>AI-06 | **A quick remote instruction is supported** — a short "do this on my desktop" — and if it produces durable context, it becomes a proper task rather than an orphan. |
| <a id="rule-ai-07"></a>AI-07 | Mobile and Web show replenishing included capacity, recovery timing, purchased credits separately, and actual per-task consumption. Extra-credit consent and limits apply across all clients. |
| <a id="rule-ai-08"></a>AI-08 | **An automation exhausting its budget produces Needs Attention** ([LP-05](../05-ai-and-agent-execution.md#rule-lp-05)), visible on the companion. |
| <a id="rule-ai-09"></a>AI-09 | **A remote surface must never silently break through a task budget** ([BG-07](../05-ai-and-agent-execution.md#rule-bg-07)). Raising it requires approval with a stated estimate. |

---

## 13. Automation on the companion

| # | Requirement |
|---|---|
| <a id="rule-au-01"></a>AU-01 | Mobile supports viewing automations, enabling and disabling them, running now, and simple creation. |
| <a id="rule-au-02"></a>AU-02 | **Advanced trigger, concurrency and missed-run configuration lives on Desktop and Web.** |
| <a id="rule-au-03"></a>AU-03 | **Web automation management may be more complete**, including batch task and automation management. |
| <a id="rule-au-04"></a>AU-04 | **`Run Now` creates a new task run** and does not shift the schedule ([AU-07](../05-ai-and-agent-execution.md#rule-au-07)). |
| <a id="rule-au-05"></a>AU-05 | **Disabling an automation does not cancel a running task** ([`AU-05`](../05-ai-and-agent-execution.md#rule-au-05)). |

---

## 14. Devices surface

| # | Requirement |
|---|---|
| <a id="rule-dv-01"></a>DV-01 | **Devices is a first-class management surface** on Mobile and Web: list, presence, trust state, remote enablement, per-capability grants, last seen, and revoke. |
| <a id="rule-dv-02"></a>DV-02 | **Revoking a device is a safe, step-up-protected operation** (`§6` of the identity requirements) that takes effect immediately. |
| <a id="rule-dv-03"></a>DV-03 | Revocation stops sync, remote and cloud access for that device, and **does not delete its local data** ([I-438](../01-normative-glossary-and-invariants.md#rule-i-438)). |

---

## 15. Workspace and realm

| # | Requirement |
|---|---|
| <a id="rule-wr-01"></a>WR-01 | **Workspace switching is an explicit action** with a visible active workspace ([AC-03](../09-shared-desktop-experience.md#rule-ac-03)). |
| <a id="rule-wr-02"></a>WR-02 | **Composer context does not survive a workspace switch.** Context bound to the previous workspace is removed or invalidated, never silently carried across. |
| <a id="rule-wr-03"></a>WR-03 | **The relationship between a remote device and a workspace is verified**: workspace, realm and permission must all match before a remote task targets a device. |
| <a id="rule-wr-04"></a>WR-04 | A desktop may hold several realm/workspace profiles. Remote commands freeze the authorized realm, workspace and application installation; switching the phone's profile never retargets an existing execution. |
| <a id="rule-wr-05"></a>WR-05 | **Cross-realm operation is prohibited** ([RW-02](../07-security-privacy-and-trust.md#rule-rw-02)). Realm is part of the mobile and web login session, selected by server profile. |

---

## 16. Offline and session security

| # | Requirement |
|---|---|
| <a id="rule-of-01"></a>OF-01 | **Mobile offline caching is very restrained**: recent task state, recent conversation summaries, pending attention items and small previews — bounded and evictable. |
| <a id="rule-of-02"></a>OF-02 | **An offline draft is queued**, and **a high-risk agent task is never automatically executed when the network returns.** |
| <a id="rule-of-03"></a>OF-03 | **An ordinary chat draft may send automatically** on reconnection. |
| <a id="rule-of-04"></a>OF-04 | **An offline-submitted agent task carries an explicit pending state** and requires confirmation on reconnection if its risk warrants. |
| <a id="rule-of-05"></a>OF-05 | **Web offline is minimal**: the application states it is offline and preserves unsent input; it does not pretend to work. |
| <a id="rule-of-06"></a>OF-06 | **Mobile App Lock is UI access protection, not account authentication** ([I-277](../01-normative-glossary-and-invariants.md#rule-i-277)). Biometric unlock **never** substitutes for step-up on a high-risk operation ([I-278](../01-normative-glossary-and-invariants.md#rule-i-278)). |
| <a id="rule-of-07"></a>OF-07 | **Web sessions are more conservative than desktop sessions** — shorter lifetime, not treated as strong long-term trust by default. |
| <a id="rule-of-08"></a>OF-08 | **An unknown browser does not immediately hold R3 approval capability.** Elevation requires additional verification. |

---

## 17. Web and Account Portal separation

| # | Requirement |
|---|---|
| <a id="rule-wp-01"></a>WP-01 | **Web companion and the Account Portal are strictly separate products** (**[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**, **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). `chat.arcforges.com` is the ArcChat surface; `account.arcforges.com` is the account, billing and security control centre. |
| <a id="rule-wp-02"></a>WP-02 | Web companion may **link** to the account portal; it does not embed it. |
| <a id="rule-wp-03"></a>WP-03 | **The mobile account surface is likewise a link-out**, showing identity, workspace, storage and usage, with management performed in the portal (`§12` of the identity requirements) — subject to the mobile commerce prohibitions in **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**. |

---

## 18. Links and URLs

| # | Requirement |
|---|---|
| <a id="rule-ln-01"></a>LN-01 | **A push deep link is safe**: it opens the corresponding surface — for example an approval — and **never carries an authorization token** ([AD-02](../07-security-privacy-and-trust.md#rule-ad-02)). |
| <a id="rule-ln-02"></a>LN-02 | Universal/app links are supported so an HTTPS canonical URL opens the installed application where present. |
| <a id="rule-ln-03"></a>LN-03 | **`arcforges://` remains the local desktop deep-link scheme**; **HTTPS canonical URLs are the cloud-addressable form** ([DL-04](../09-shared-desktop-experience.md#rule-dl-04)). |
| <a id="rule-ln-04"></a>LN-04 | **A cloud resource URL always verifies permission** at access time; an unauthorised request is denied, and the denial does not disclose the resource's existence where that would leak ([SR-02](../07-security-privacy-and-trust.md#rule-sr-02) in the security requirements). |
| <a id="rule-ln-05"></a>LN-05 | **There is no public share by default** (`§18` of the cloud requirements). Links are authenticated private links ([I-279](../01-normative-glossary-and-invariants.md#rule-i-279)). |

---

## 19. Commerce posture

Governed entirely by **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**, confirmed by **[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)**.

| Android companion may | Android companion must not |
|---|---|
| Sign in | Sell subscriptions, cloud access or AI credits in-app |
| Display current plan and entitlement state | Embed provider checkout |
| Consume cloud capabilities and credits acquired elsewhere | Integrate store billing for the initial release |
| Display tasks, runs, approvals, notifications and results | Display an external purchase button, link or call to action |
| Manage non-commercial account and security settings permitted by store policy | **Unlock functionality from a locally entered licence key or purchase token** |

**The same conservative behaviour applies on every storefront**, even where a regional programme permits external links. The entitlement architecture stays capable of accepting a future store-originated grant without implementing one.

---

## 20. Non-goals

Mobile and Web are **not**: a complete knowledge editing workbench; an ArcScope or ArcSlate editor; a general screen-and-input remote desktop; a route that bypasses the ArcChat trust model to reach professional products directly; a way to perform R4 operations without local presence; a place where desktop-local secrets are held; or a commerce surface.

---

## 21. Domain model

```
DevicePresence · RemoteAgentAvailability · RemoteDeviceCapability
RemoteTaskRequest · ExecutionTarget · ExecutionLocation · RemoteTaskReference
ContinuityState
ApprovalRequest · ApprovalPresentation · ApprovalExpiry
SteeringInstruction · SteeringStatus
Notification · NotificationPreference · AttentionItem · PushRegistration
ArtifactAvailability · ArtifactPreview · RemoteArtifactTransfer
CloudTaskReference · RemoteHandoff
WorkspaceDeviceContext · RemoteSession · OfflineCachePolicy
```

---

## 22. Platform requirements

| # | Requirement |
|---|---|
| <a id="rule-pf-01"></a>PF-01 | Android arm64 is the delivered mobile platform, using the pinned Kotlin/Jetpack Compose release build. x64 is emulator-only. No MAUI/Mono runtime flag enters this project. |
| <a id="rule-pf-02"></a>PF-02 | **Android only.** No iOS architecture, implementation, build or store deliverable is required under P2-010. A future target needs its own scope decision. |
| <a id="rule-pf-03"></a>PF-03 | **Mobile and Web never load executable extensions** ([PL-01](../08-extensions-and-developer-platform.md#rule-pl-01) in the extension requirements). |
| <a id="rule-pf-04"></a>PF-04 | Mobile secure storage holds authorized session material. Model-provider credentials and private deployment policy never reach the phone. |
| <a id="rule-pf-05"></a>PF-05 | **Weak-network behaviour is a release gate** ([PM-03](../12-quality-and-compatibility-contract.md#rule-pm-03) in the quality contract): background resume, reconnection with sequence backfill, and offline queueing all verified on real devices. |
| <a id="rule-pf-06"></a>PF-06 | Web uses React/TypeScript static profiles; Mobile uses Kotlin/Jetpack Compose. Both consume Apache generated proto SDKs, current Cloud authorization and the same CF presentation/recovery semantics through their selected adapters. |
| <a id="rule-pf-07"></a>PF-07 | **The mobile provenance and dependency-closure audit ([F-023](../../assurance/open-gates-register.md#rule-f-023)) must pass before the first mobile artifact is produced** ([PL-06](../10-distribution-update-and-support.md#rule-pl-06) in the distribution requirements). |
| <a id="rule-pf-08"></a>PF-08 | **Automated architecture and dependency checks prevent GPL-family or AGPL-only source, project references, packages, generated artifacts and transitive dependencies from entering the mobile distributable** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |

---

## 23. Acceptance scenarios

**Presence** — a desktop appears online with its per-product readiness; disabling remote agent on the desktop makes desktop capabilities unavailable while cloud capability continues.

**Remote task** — a task created from mobile with a desktop target and the desktop offline enters `WaitingForDevice`, not `Failed`; a cloud-executable task runs with the machine fully powered off; a hybrid task states which step is blocking.

**Local-only data** — a task requiring an 80 GB local capture waits for the device; nothing is uploaded.

**Durability** — a remote task survives closing the mobile application and killing it; it is found in the Task Center on return.

**Approval** — the card names the concrete effect and resource revision; a revision change invalidates it; an R4 operation is refused remotely and directed to a trusted device; a processed approval no longer appears actionable.

**Steering** — a steering instruction is bound to the task, recorded immutably, and reports whether it applied immediately, queued, or could not apply.

**Notifications** — an approval pushes; task progress does not; a security notification cannot be disabled; a lock-screen notification reveals nothing sensitive by default; tapping opens the surface and grants nothing.

**Artifacts** — a device-only artifact shows as requiring a transfer; requesting it creates a visible transfer task; a large transfer prompts and respects the cellular policy; handoff opens the owning desktop product.

**Continuity** — acknowledged history and one Cloud TaskId are observed across all surfaces; unsent drafts and unselected device files remain private to their current location.

**Search** — cloud search finds only cloud-accessible content; a local resource is not fetched by waking the desktop implicitly.

**AI** — Cloud-only work runs with desktops off; local tools wait for an authorized device; no local model or BYOK path exists; shared usage and extra-credit limits hold across simultaneous clients.

**Workspace** — switching workspace clears composer context; a remote task targeting a device verifies workspace, realm and permission.

**Security** — app lock does not substitute for step-up; a new browser cannot immediately perform an R3 approval; revoking a device takes effect immediately and deletes no local data.

**Commerce** — no purchase surface, no external purchase call to action, and no licence-key unlock path exists in any build; an entitlement purchased on the web is consumed normally.

---

## 24. Traceability

| Current document | Relationship |
|---|---|
| [Mobile Architecture](../../architecture/11-mobile-architecture.md) | Implements Kotlin Android companion scope, networking and device security |
| [Web Architecture](../../architecture/10-web-architecture.md) | Implements the browser companion with the current Web stack |
| [Realtime Events and the Durable Bridge](../../architecture/contracts/03-realtime-and-bridge.md) | Defines durable remote requests, results and realtime recovery |
| **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**, **[F-023](../../assurance/open-gates-register.md#rule-f-023)** | Apache-2.0 mobile boundary, no shared ViewModels, pre-distribution provenance gate |
| **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**, **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../../assurance/phase-1-official-verification.md#rule-v-04)** | Web technology; Android Kotlin/Jetpack Compose; iOS outside scope |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud never reaches local IPC; the desktop re-authorises every remote request |
| **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**, **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Surface inventory; Web companion separate from the account portal |
| **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)** | Consumption-only commerce posture and its traceable prohibitions |
