# Contracts, Protocols and Shared Semantics

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (Apache interoperability boundary), **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)** (contract-authoring obligation), **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** (MCP)
> Companions: [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md), [`03-local-ipc-and-process-model.md`](03-local-ipc-and-process-model.md), [`../requirements/01-normative-glossary-and-invariants.md`](../requirements/01-normative-glossary-and-invariants.md)

> **What is shared across products is the semantic contract, not the domain model.**

Each professional application composes the Platform assistant with its own typed handlers. Shared packages do not reference product domain entities. Cloud may invoke the explicitly selected application installation through the device bridge; there is no desktop-to-desktop orchestration or local peer discovery. [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../decisions/phase-2-specification-decisions.md#rule-p2-013) and annex 10 govern the current scope.

---

## 1. The two-layer contract model

```
Shared semantic primitives          small, stable, rarely changed, Apache-2.0
        +
Owner-specific strongly typed contracts   independently owned and versioned per product
```

**This is not a universal dynamic RPC.** A generic `Invoke(string capability, object payload)` would defeat contracts, permissions, versioning, AOT safety and testability simultaneously.

| # | Rule |
|---|---|
| <a id="rule-cm-01"></a>CM-01 | **Shared foundation is small and stable; product capability contracts are independently owned and versioned by their owning product** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| <a id="rule-cm-02"></a>CM-02 | **An upgrade to one product must never force an unrelated product to recompile or re-release** ([I-032](../requirements/01-normative-glossary-and-invariants.md#rule-i-032) family). |
| <a id="rule-cm-03"></a>CM-03 | **The foundation contract package holds only genuinely long-term stable types.** Product-specific concepts are prohibited in it. |
| <a id="rule-cm-04"></a>CM-04 | A process-boundary envelope never contains object. Payloads use the owning contract; in-process application calls use the same typed semantics without introducing a listener. |
| <a id="rule-cm-05"></a>CM-05 | Process-boundary contracts are AOT-friendly: authored proto/generated bindings, no runtime type resolution or assembly-qualified type names. |
| <a id="rule-cm-06"></a>CM-06 | **A small amount of extensible metadata is permitted and must not become a domain dumping ground.** |

---

## 2. Application, installation and instance

| Concept | Definition | Lifetime |
|---|---|---|
| **`AppId`** | A stable ArcForges product identity | Permanent |
| **`AppInstallation`** | One installed copy on one device | Until uninstalled |
| **`AppInstance`** | A running instance that can actually provide local capabilities | One process lifetime |

| # | Rule |
|---|---|
| <a id="rule-ai-01"></a>AI-01 | **`AppId` is stable forever** and never encodes version, process or platform. |
| <a id="rule-ai-02"></a>AI-02 | **`AppId ≠ ProductScope`** ([I-005](../requirements/01-normative-glossary-and-invariants.md#rule-i-005)). One is runtime identity; the other is a commercial scoping concept. |
| <a id="rule-ai-03"></a>AI-03 | **`AppId ≠ Process`** ([I-006](../requirements/01-normative-glossary-and-invariants.md#rule-i-006)). **`AppId → unique process` must never be assumed** ([I-009](../requirements/01-normative-glossary-and-invariants.md#rule-i-009)). |
| <a id="rule-ai-04"></a>AI-04 | **An installation exists independently of any running instance.** Static contribution metadata is readable before the product starts. |
| <a id="rule-ai-05"></a>AI-05 | **An instance may host several window and document sessions**, and one product may have several concurrent instances. |
| <a id="rule-ai-06"></a>AI-06 | **An instance restart produces a new `InstanceId`** ([I-008](../requirements/01-normative-glossary-and-invariants.md#rule-i-008)). |
| <a id="rule-ai-07"></a>AI-07 | **Resource identity never depends on `InstanceId`**; **context identity may** (`§6.3`). |
| <a id="rule-ai-08"></a>AI-08 | **Application information is not deleted when an instance dies.** The installation and its static contributions remain. |
| <a id="rule-ai-09"></a>AI-09 | App Instance names an application execution identity; provider remains reserved for AI/external service providers. Its presence is a Cloud projection, not a local discovery record. |

---

## 3. Contribution model

A host application composes its own signed contribution descriptors and admitted extensions. Shared assistant UI consumes these typed in-process registrations; it does not scan other installations or hard-code product behavior.

Six contribution kinds:

| Kind | Meaning |
|---|---|
| **Capability** | A machine-callable semantic operation |
| **Action** | A context-sensitive executable entry shown to a user |
| **Context Provider** | A read-only source of "what the user is focused on" |
| **Artifact Handler** | A declaration of which artifact kinds this product can handle |
| **Suggested Task** | A context-derived suggestion of useful work |
| **Deep Link / Open Target** | A navigable address this product can resolve |

| # | Rule |
|---|---|
| <a id="rule-cb-01"></a>CB-01 | Shared assistant packages must not hard-code product behavior. The host supplies typed contribution bindings; product-specific behavior stays in its domain/application package. |
| <a id="rule-cb-02"></a>CB-02 | **Contribution is description, not authority** ([I-042](../requirements/01-normative-glossary-and-invariants.md#rule-i-042)). Declaring a capability grants the caller nothing. |
| <a id="rule-cb-03"></a>CB-03 | The own-application registry reads explicit contributions, never another product database or local discovery directory. |
| <a id="rule-cb-04"></a>CB-04 | Static metadata is part of the host package inventory. Runtime availability is evaluated inside that application and projected to Cloud through application.heartbeat when signed in. |
| <a id="rule-cb-05"></a>CB-05 | **`Static Capability ≠ Runtime Capability Availability`** ([I-045](../requirements/01-normative-glossary-and-invariants.md#rule-i-045)). |
| <a id="rule-cb-06"></a>CB-06 | Adding a host application does not require product switches in shared assistant packages. |

---

## 4. Capability

**`Capability` = a stable semantic capability a product exposes for machine invocation.**

### 4.1 Identity

| # | Rule |
|---|---|
| <a id="rule-cp-01"></a>CP-01 | **A capability has a stable, namespaced `CapabilityId`**, owned by the contributing product: `arcnotes.document.create`, `arcscope.session.compare`, `arcslate.timeline.move-clip`. |
| <a id="rule-cp-02"></a>CP-02 | **The string is used only for discovery, display, policy, tool selection, routing and audit.** The actual call lands on a compiled, strongly typed interface method (**[AC-02](00-architecture-overview.md#rule-ac-02)**). |
| <a id="rule-cp-03"></a>CP-03 | **A capability is business semantics, not a CRUD mapping.** `arcnotes.document.insert-block` is a capability; `arcnotes.table.row.update` is not. |
| <a id="rule-cp-04"></a>CP-04 | Capability and UI Command are distinct: a menu item is not automatically machine callable. Only explicit capability descriptors can enter an own-app assistant or authorized Cloud invocation. |
| <a id="rule-cp-05"></a>CP-05 | **`Capability ≠ Action`** ([I-040](../requirements/01-normative-glossary-and-invariants.md#rule-i-040)), **`Capability ≠ Permission`** ([I-042](../requirements/01-normative-glossary-and-invariants.md#rule-i-042)), **`Capability ≠ Package`** ([I-044](../requirements/01-normative-glossary-and-invariants.md#rule-i-044)). |
| <a id="rule-cp-06"></a>CP-06 | **One classification system, not three.** Read, write and long-running operations are all capabilities, differing by declared metadata — not by living in separate mechanisms. |
| <a id="rule-cp-07"></a>CP-07 | **A `CapabilityId` is not changed for an additive change.** A breaking change produces a new capability identity or a new contract version (`§8`). |

### 4.2 Descriptor

`CapabilityDescriptor` declares, at minimum:

| Field group | Contents |
|---|---|
| Identity | `CapabilityId`, display metadata, owning `AppId`, contract version, feature flags |
| Typing | The typed service and method identity it binds to |
| Shape | Input and output summary; whether it writes state |
| **Execution shape** | Immediate result, or long-running returning a `TaskHandle` |
| **Effect semantics** | `Reversible`, `Compensatable`, `Irreversible` |
| **Retry semantics** | `Idempotent`, `RetrySafe`, `RequiresReconciliation` |
| **Cancellation semantics** | `Cancelable`, `CancelableAtSafePoint`, `NotCancelableOnceStarted` |
| **Preview / preflight** | Whether an impact preview can be produced without executing |
| **Checkpoint support** | Whether the owner can produce a domain checkpoint first |
| **Compensation support** | Whether and how the effect can be compensated |
| Authorization | Required scope, risk level, whether confirmation is mandatory |
| Limits | Resource size, expected duration, concurrency limits |

| # | Rule |
|---|---|
| <a id="rule-cd-01"></a>CD-01 | **Retry safety is declared by the owner, never guessed by the caller** ([FL-08](../requirements/05-ai-and-agent-execution.md#rule-fl-08) in the AI requirements). |
| <a id="rule-cd-02"></a>CD-02 | **Capability metadata must not reveal internal implementation detail** — no type names, no storage structure, no internal paths. |
| <a id="rule-cd-03"></a>CD-03 | **Every capability declares its risk baseline**; runtime modifiers may raise it and third-party metadata may never lower it ([RK-03](../requirements/07-security-privacy-and-trust.md#rule-rk-03)). |

---

## 5. Action

**`Action` = a context-sensitive executable entry displayed to a user.**

| # | Rule |
|---|---|
| <a id="rule-ac-01"></a>AC-01 | **`Action ≠ Capability`** ([I-040](../requirements/01-normative-glossary-and-invariants.md#rule-i-040)) and **`Action ≠ Capability Invocation`** ([I-043](../requirements/01-normative-glossary-and-invariants.md#rule-i-043)). An action is user-experience semantics; a capability is execution semantics. |
| <a id="rule-ac-02"></a>AC-02 | **Not every capability is surfaced as an action**, and **an action may map to several capabilities**. |
| <a id="rule-ac-03"></a>AC-03 | An `ActionDescriptor` declares: identity, display, applicable context kinds, the capability or capabilities it invokes, and its availability rule. |
| <a id="rule-ac-04"></a>AC-04 | **Availability is a dynamic projection**, expressing at minimum: `Available`, `NotApplicableToContext`, `AppNotInstalled`, `AppNotRunning`, `IncompatibleVersion`, `PermissionRequired`, `EntitlementRequired`, `PolicyDisabled`, `TemporarilyUnavailable`. |
| <a id="rule-ac-05"></a>AC-05 | **A permission-required action is not hidden forever.** It is shown and routes into the ordinary approval and permission flow ([UX-01](../requirements/07-security-privacy-and-trust.md#rule-ux-01)). |

---

## 6. Context

**`Context Provider` = a product exposing a read-only description of what the user is currently focused on.**

| # | Rule |
|---|---|
| <a id="rule-cx-01"></a>CX-01 | **`Context Provider ≠ Resource Database`** ([I-048](../requirements/01-normative-glossary-and-invariants.md#rule-i-048)) and **≠ Search Engine** ([I-047](../requirements/01-normative-glossary-and-invariants.md#rule-i-047)). It answers *current, relevant, bounded*; querying and search are capabilities. |
| <a id="rule-cx-02"></a>CX-02 | **A context provider supplies description and references, never bulk content** ([I-049](../requirements/01-normative-glossary-and-invariants.md#rule-i-049)). |
| <a id="rule-cx-03"></a>CX-03 | **Context is either stable or ephemeral.** Stable context references durable resources; ephemeral context reflects transient selection. |
| <a id="rule-cx-04"></a>CX-04 | **Ephemeral context is bound to an `InstanceId`** and carries **generation and expiry** semantics. |
| <a id="rule-cx-05"></a>CX-05 | **Ephemeral context is frozen before a task is created** ([IB-01](../requirements/05-ai-and-agent-execution.md#rule-ib-01)). Once frozen, the task's input is fixed. |
| <a id="rule-cx-06"></a>CX-06 | **Context freeze is not a copy of all data** ([I-049](../requirements/01-normative-glossary-and-invariants.md#rule-i-049)). It is stable references plus typed selection. |
| <a id="rule-cx-07"></a>CX-07 | **Context that cannot be frozen must not be presented as persistent.** It is for immediate use only. |
| <a id="rule-cx-08"></a>CX-08 | **A context provider grants no read permission** ([I-046](../requirements/01-normative-glossary-and-invariants.md#rule-i-046)). Reading the referenced content still goes through capability plus authorization. |
| <a id="rule-cx-09"></a>CX-09 | **A context provider cannot silently expand scope** ([AS-05](../requirements/06-knowledge-search-and-retrieval.md#rule-as-05)). |
| <a id="rule-cx-10"></a>CX-10 | **`Context ≠ Resource`** ([I-046](../requirements/01-normative-glossary-and-invariants.md#rule-i-046)), and **`Current Selection ≠ durable resource identity`** ([I-050](../requirements/01-normative-glossary-and-invariants.md#rule-i-050)). |

---

## 7. Resource and reference

**`Resource` = a stably identifiable business object or asset owned by exactly one authoritative owner product.**
**`ResourceRef` = a stable, lightweight, non-writable reference to a resource in its owner.**

### 7.1 `ResourceRef`

Carries: realm, workspace scope where applicable, owning `AppId`, namespaced `ResourceKind`, `ResourceId`, optional display hint, and an availability hint.

| # | Rule |
|---|---|
| <a id="rule-rr-01"></a>RR-01 | **`ResourceKind` is namespaced by owner**: `arcnotes.document`, `arcnotes.block`, `arcscope.session`, `arcslate.sequence`. |
| <a id="rule-rr-02"></a>RR-02 | **A file path is never an identity** ([I-052](../requirements/01-normative-glossary-and-invariants.md#rule-i-052), [I-195](../requirements/01-normative-glossary-and-invariants.md#rule-i-195)). |
| <a id="rule-rr-03"></a>RR-03 | **A `ResourceRef` never contains**: a file path, a native pointer, an internal database key, a connection handle, credentials, or the resource's content ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). |
| <a id="rule-rr-04"></a>RR-04 | **`ResourceId` is never reused** (`§2` of the glossary). |
| <a id="rule-rr-05"></a>RR-05 | **Rename does not change the reference** ([SY-11](../requirements/03-cloud-services-and-sync.md#rule-sy-11)). **Move does not change the reference.** |
| <a id="rule-rr-06"></a>RR-06 | **Deleting a resource does not degrade its reference to a plain string.** The reference remains valid as an identity, resolving to a deleted state; restoring the resource makes it resolvable again ([DE-03](../requirements/03-cloud-services-and-sync.md#rule-de-03)). |
| <a id="rule-rr-07"></a>RR-07 | **Copy or import produces a new resource with a new `ResourceId`** (`§4.2` of the product scope). |
| <a id="rule-rr-08"></a>RR-08 | **`ResourceRef` and `ResourceVersionRef` are different** (`§7.2`). |
| <a id="rule-rr-09"></a>RR-09 | **A reference is location-independent and works across devices.** The same logical object has one reference; **availability is separate from identity** ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). |
| <a id="rule-rr-10"></a>RR-10 | **A local-only resource still has a reference**, with availability naming the device that holds it. |
| <a id="rule-rr-11"></a>RR-11 | **A reference never expands visibility** ([I-054](../requirements/01-normative-glossary-and-invariants.md#rule-i-054)). Dereferencing an unauthorised reference returns a permission failure. |
| <a id="rule-rr-12"></a>RR-12 | **`ResourceRef ≠ Capability Token`** ([I-053](../requirements/01-normative-glossary-and-invariants.md#rule-i-053)) and **≠ permission token** ([I-054](../requirements/01-normative-glossary-and-invariants.md#rule-i-054)). It is an address, not an authorization. |
| <a id="rule-rr-13"></a>RR-13 | **Dereferencing is always controlled by the owner** ([I-055](../requirements/01-normative-glossary-and-invariants.md#rule-i-055)). |
| <a id="rule-rr-14"></a>RR-14 | **`ResourceRef` standardises identity, not content** ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). It is a bridge, never a universal domain model. |

### 7.2 Floating and pinned references

| Form | Meaning |
|---|---|
| **`ResourceRef`** (floating) | "This resource, as it currently is" |
| **`ResourceVersionRef`** (pinned) | "This resource at this revision" |

**The two must never be conflated** ([I-165](../requirements/01-normative-glossary-and-invariants.md#rule-i-165) family). A citation pins; a working reference floats.

### 7.3 Typed resource selection

Partial selection — a block range, a time range, a clip set — uses a **common envelope plus a per-product typed selector** defined by the owner's contract.

| # | Rule |
|---|---|
| <a id="rule-ts-01"></a>TS-01 | **A `ResourceRef` is not stuffed with sub-paths** ([I-055](../requirements/01-normative-glossary-and-invariants.md#rule-i-055)). |
| <a id="rule-ts-02"></a>TS-02 | **No universal selection schema is created.** ArcNotes block ranges, ArcScope time and signal ranges, and ArcSlate timeline ranges are structurally different and are typed by their owners. |
| <a id="rule-ts-03"></a>TS-03 | **`ResourceRef ≠ Resource Selection`** ([I-056](../requirements/01-normative-glossary-and-invariants.md#rule-i-056)). |

---

## 8. Artifact

**`Artifact` = a record of a result that has independent user value.**

| # | Rule |
|---|---|
| <a id="rule-ar-01"></a>AR-01 | **`Artifact ≠ Resource`** ([I-058](../requirements/01-normative-glossary-and-invariants.md#rule-i-058)) and **`ArtifactRef ≠ ResourceRef`** ([I-059](../requirements/01-normative-glossary-and-invariants.md#rule-i-059)). |
| <a id="rule-ar-02"></a>AR-02 | **An artifact record carries**: identity, namespaced `ArtifactKind`, producing task and run, actor chain, time, provenance, a reference to the underlying resource where one exists, and availability. |
| <a id="rule-ar-03"></a>AR-03 | A professional product owns its artifacts. Its embedded assistant records relationships within that scope; it does not own another product corpus. |
| <a id="rule-ar-04"></a>AR-04 | An assistant-generated artifact belongs to its frozen application/Cloud execution scope and existing resource owner. Shared UI does not create a separate ArcChat owner or another product's write permission. |
| <a id="rule-ar-05"></a>AR-05 | **Deleting an artifact record never deletes the resource** ([I-060](../requirements/01-normative-glossary-and-invariants.md#rule-i-060)). Deleting the resource requires calling the owner's capability explicitly. |
| <a id="rule-ar-06"></a>AR-06 | **`Artifact Handler` declares which artifact kinds a product can handle** and with which capabilities — open, preview, import, convert, edit. |
| <a id="rule-ar-07"></a>AR-07 | The host resolves its admitted artifact handlers deterministically by explicit preference then descriptor priority. Another product is never discovered or launched for resolution; cross-product handoff is future scope. |
| <a id="rule-ar-08"></a>AR-08 | **Artifact preview is a derived projection** ([I-060](../requirements/01-normative-glossary-and-invariants.md#rule-i-060)), never artifact content authority. |
| <a id="rule-ar-09"></a>AR-09 | **`ArtifactRef` is not a permission token** ([I-054](../requirements/01-normative-glossary-and-invariants.md#rule-i-054) family). |

---

## 9. Deep link

**`Deep Link` = a navigation contract, not a remote command contract** ([I-062](../requirements/01-normative-glossary-and-invariants.md#rule-i-062)).

| # | Rule |
|---|---|
| <a id="rule-dl-01"></a>DL-01 | A deep link may open its addressed application and navigate to its own resource or route. Cross-product handoff payloads are deferred; native sign-in callbacks are governed separately by contracts 07. |
| <a id="rule-dl-02"></a>DL-02 | **A deep link may not, by default**: perform a side-effecting operation, bypass confirmation, or grant authority. It routes into the ordinary UI, capability and approval path. |
| <a id="rule-dl-03"></a>DL-03 | **A deep link may carry intent; it never represents authorized execution.** |
| <a id="rule-dl-04"></a>DL-04 | **Deep links address stable identity** — a `ResourceRef` or a logical route — never an absolute path ([`DL-04`](../requirements/09-shared-desktop-experience.md#rule-dl-04) in the shared desktop requirements). |
| <a id="rule-dl-05"></a>DL-05 | **Cloud objects use an HTTPS canonical link**; `arcforges://` is the desktop local routing scheme. Both resolve to the same logical object. |
| <a id="rule-dl-06"></a>DL-06 | **A private HTTPS link is not a public share link** ([I-279](../requirements/01-normative-glossary-and-invariants.md#rule-i-279)). Permission is always checked at access. |
| <a id="rule-dl-07"></a>DL-07 | **An externally originated deep link is always untrusted input** ([DL-02](../requirements/09-shared-desktop-experience.md#rule-dl-02) there). |
| <a id="rule-dl-08"></a>DL-08 | **Secrets are prohibited in deep links** ([DL-03](../requirements/09-shared-desktop-experience.md#rule-dl-03) there). |
| <a id="rule-dl-09"></a>DL-09 | **A deep link is not a capability token** ([I-063](../requirements/01-normative-glossary-and-invariants.md#rule-i-063)). |

---

## 10. Event

**`Event` = an observable fact that has already occurred.**

| # | Rule |
|---|---|
| <a id="rule-ev-01"></a>EV-01 | **`Event ≠ Command`** ([I-064](../requirements/01-normative-glossary-and-invariants.md#rule-i-064)). A command requests; an event reports. |
| <a id="rule-ev-02"></a>EV-02 | **An event is produced after the business fact is committed**. |
| <a id="rule-ev-03"></a>EV-03 | **Every event carries a stable `EventId`**, because delivery is at-least-once; consumers deduplicate by `EventId`. |
| <a id="rule-ev-04"></a>EV-04 | **Every event carries causation and correlation**, which is what makes automation loop detection possible ([LP-01](../requirements/05-ai-and-agent-execution.md#rule-lp-01)). |
| <a id="rule-ev-05"></a>EV-05 | **An event references resources rather than copying large content** ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). |
| <a id="rule-ev-06"></a>EV-06 | **Durable integration events and ephemeral signals are distinguished** ([I-065](../requirements/01-normative-glossary-and-invariants.md#rule-i-065)). A durable event is a business fact; an ephemeral signal is a realtime experience. |
| <a id="rule-ev-07"></a>EV-07 | **Automation subscribes only to durable events by default.** A high-rate signal may be explicitly promoted into a durable event, with throttling. |
| <a id="rule-ev-08"></a>EV-08 | **A generic `Changed` event is not exposed as the primary ecosystem contract.** Events are semantic. |
| <a id="rule-ev-09"></a>EV-09 | **There is no global ArcForges event sequence.** Ordering is per stream or per resource; a global absolute order is never implied. |
| <a id="rule-ev-10"></a>EV-10 | **Event loss must not destroy state** ([I-066](../requirements/01-normative-glossary-and-invariants.md#rule-i-066)). State is recoverable by query. |
| <a id="rule-ev-11"></a>EV-11 | **An event grants no permission** (`§8` of the security requirements). |

---

## 11. Health, presence, readiness and compatibility

**Five separate dimensions. A single green dot is insufficient** ([I-067](../requirements/01-normative-glossary-and-invariants.md#rule-i-067)–[I-071](../requirements/01-normative-glossary-and-invariants.md#rule-i-071)).

| Dimension | Question |
|---|---|
| **Installation** | Is the product installed on this device? |
| **Presence** | Is an instance currently connected? |
| **Health** | Is the instance functioning — `Ready`, `Busy`, `Degraded`, `Draining`? |
| **Readiness** | Can it accept work right now? |
| **Compatibility** | Can this caller and this instance actually interoperate? |

| # | Rule |
|---|---|
| <a id="rule-hl-01"></a>HL-01 | **These dimensions must never be merged into one flag.** |
| <a id="rule-hl-02"></a>HL-02 | **`Health ≠ Trust`** ([I-070](../requirements/01-normative-glossary-and-invariants.md#rule-i-070)), **`Health ≠ Compatibility`** ([I-069](../requirements/01-normative-glossary-and-invariants.md#rule-i-069)), **`Health ≠ Capability Availability`** ([I-071](../requirements/01-normative-glossary-and-invariants.md#rule-i-071)), **`Presence ≠ Readiness`** ([I-068](../requirements/01-normative-glossary-and-invariants.md#rule-i-068)). |
| <a id="rule-hl-03"></a>HL-03 | **A health snapshot is not a business state image.** It carries operational state only. |
| <a id="rule-hl-04"></a>HL-04 | Cloud application presence expires after 30 seconds without the 10-second heartbeat, as specified by annex 10. A private helper lease is launch-bound under annex 09; neither mechanism discovers another product. |

---

## 12. Compatibility and versioning

| # | Rule |
|---|---|
| <a id="rule-vc-01"></a>VC-01 | **Compatibility is negotiated per capability**, not per product version. |
| <a id="rule-vc-02"></a>VC-02 | **App version is information, not the compatibility criterion** ([I-025](../requirements/01-normative-glossary-and-invariants.md#rule-i-025)). Contract and capability versions decide. |
| <a id="rule-vc-03"></a>VC-03 | **Compatibility is layered**: foundation contract version, per-product contract set version, per-capability version, feature set. |
| <a id="rule-vc-04"></a>VC-04 | **Not every version change affects the whole product.** Partial compatibility is expressible: some capabilities available, others not. |
| <a id="rule-vc-05"></a>VC-05 | **A destructive contract change follows semantic versioning rules** and produces either a new capability identity or a coexisting `V2` interface with a stated migration window. |
| <a id="rule-vc-06"></a>VC-06 | **A feature flag is not a capability version** ([I-072](../requirements/01-normative-glossary-and-invariants.md#rule-i-072)). One says whether a capability has been released; the other says what shape it has. |
| <a id="rule-vc-07"></a>VC-07 | **Compatibility negotiation completes before invocation.** An incompatible call is refused with a specific reason, not attempted and failed. |
| <a id="rule-vc-08"></a>VC-08 | **An owner's internal schema version is never the platform compatibility axis** (`§14` of the quality contract). |
| <a id="rule-vc-09"></a>VC-09 | **Contract compatibility tests retain the previous stable client assembly, serialized golden vectors and AOT publish artifacts** ([CT-02](../requirements/12-quality-and-compatibility-contract.md#rule-ct-02) there). |
| <a id="rule-vc-10"></a>VC-10 | **A failure to generate an AOT proxy is a CI blocker**; falling back to a dynamic proxy in production is prohibited. |

---

## 13. Invocation

**`Invocation` = one complete semantic request to execute a capability.**

An invocation logically carries: `InvocationId`, target (capability identity plus resolution input), typed request, actor chain, workspace and realm, correlation and causation, approval reference where applicable, `CommandId` for a write, `ExpectedRevision` where applicable, and a cancellation token.

### 13.1 Identity separation

| Identity | Meaning |
|---|---|
| **`CommandId`** | This logical write action |
| **`InvocationId`** | This actual call |
| **`AttemptId`** | This execution try of a task step |
| **`StepId`** | This unit of work in a run |

**`InvocationId ≠ CommandId`** ([I-073](../requirements/01-normative-glossary-and-invariants.md#rule-i-073)); **`Invocation ≠ Step`** ([I-074](../requirements/01-normative-glossary-and-invariants.md#rule-i-074)); **`AttemptId ≠ CommandId`** ([I-085](../requirements/01-normative-glossary-and-invariants.md#rule-i-085)).

### 13.2 The invocation pipeline

```
Resolve target → Negotiate compatibility → Validate input
  → Authorize (caller side) → Route → Owner validates → Owner authorizes (final)
  → Execute → Result or TaskHandle → Record provenance → Emit events
```

### 13.3 Routing

Inside an application, the compiled capability binding invokes that host's handler directly. Remote device tools bind the exact ApplicationTarget from annex 10: product, device, installation and delivery epoch. The client may select an eligible own-product target; a Task, conversation or approval retains the target it captured. An absent/offline target waits or refuses with a typed reason; it never launches a desktop or silently chooses another installation.

| # | Rule |
|---|---|
| <a id="rule-rt-01"></a>RT-01 | Process start order is never a routing default. |
| <a id="rule-rt-02"></a>RT-02 | Resource affinity cannot migrate ownership or expand product scope. |
| <a id="rule-rt-03"></a>RT-03 | A stopped/offline target is unavailable until the user independently starts/connects it; no remote or peer launch-on-demand. |
| <a id="rule-rt-04"></a>RT-04 | Missing installation produces a stated unavailable/install action in the companion; it does not search the local machine. |
| <a id="rule-rt-05"></a>RT-05 | Multiple eligible targets require explicit selection; existing execution identities are not retargeted. |

### 13.4 Authorization

| # | Rule |
|---|---|
| <a id="rule-au-01"></a>AU-01 | **Validation and authorization are separate.** Shape validity is not permission. |
| <a id="rule-au-02"></a>AU-02 | The executing owner reauthorizes current actor, scope, revision, policy and approval. An assistant UI, Cloud route or descriptor cannot substitute for owner-side checks. |
| <a id="rule-au-03"></a>AU-03 | **A capability invocation never carries a UI object**, a control, a view model, a native pointer or a `SafeHandle`. Input is semantic. |

### 13.5 Results

Two success shapes:

| Shape | Use |
|---|---|
| **Immediate result** | The operation completed; the response carries the outcome and the new revision |
| **`TaskHandle`** | The operation is long-running; the caller observes the task |

**A long-running RPC connection held open for hours is prohibited**.

### 13.6 Errors

Business failures use `ArcResult<T>` / `ArcError` with a **stable semantic code**, a message key, optional details and a correlation identifier. Callers branch on the code, never on human-readable text.

| # | Rule |
|---|---|
| <a id="rule-er-01"></a>ER-01 | **"Failed" alone is prohibited.** The semantic error set includes at minimum: `NotFound`, `PermissionDenied`, `ApprovalRequired`, `ApprovalDenied`, `Conflict`, `PreconditionFailed`, `InvalidInput`, `Unsupported`, `IncompatibleVersion`, `NotInstalled`, `NotRunning`, `SelectionRequired`, `Busy`, `RateLimited`, `BudgetExceeded`, `EntitlementRequired`, `PolicyDisabled`, `ResourceUnavailable`, `Timeout`, `ExternalEffectUnknown`, `Internal`. |
| <a id="rule-er-02"></a>ER-02 | **`Conflict` is first-class platform semantics** ([I-092](../requirements/01-normative-glossary-and-invariants.md#rule-i-092) family). It reports the current revision, a disclosure-safe conflict summary, whether automatic replay is possible, and a recommended action. **Silent last-write-wins is prohibited.** |
| <a id="rule-er-03"></a>ER-03 | **A stable error code never changes with localisation** ([CT-03](../requirements/12-quality-and-compatibility-contract.md#rule-ct-03) in the quality contract). |
| <a id="rule-er-04"></a>ER-04 | **Health, compatibility and permission failures produce distinct user experiences** ([ER-08](../requirements/09-shared-desktop-experience.md#rule-er-08) in the shared desktop requirements). "ArcScope unavailable" must not stand in for "you lack permission". |
| <a id="rule-er-05"></a>ER-05 | **Provenance is carried end to end**: actor chain, caller instance, capability, invocation, command, task, run, step, approval — through to the owner's domain revision. |

---

## 14. Suggested tasks

| # | Rule |
|---|---|
| <a id="rule-sg-01"></a>SG-01 | **A suggested task is a recommendation**, never automatically executed. |
| <a id="rule-sg-02"></a>SG-02 | **A suggestion carries no additional permission.** |
| <a id="rule-sg-03"></a>SG-03 | **Suggestions are contextual**, derived from the current context provider output, and are a discovery mechanism rather than a workflow engine. |

---

## 15. Relationship to adjacent systems

| Pair | Relationship |
|---|---|
| **Shared semantics ↔ Search** | A search result is a projection, not resource authority ([SR-03](../requirements/06-knowledge-search-and-retrieval.md#rule-sr-03)). |
| **Shared semantics ↔ Extensions** | Native products and third-party extensions may share semantics; **trust differs** (`§9` of the security requirements). |
| **Shared semantics ↔ MCP** | **MCP is an edge adapter, never the internal protocol** ([I-307](../requirements/01-normative-glossary-and-invariants.md#rule-i-307)). **`MCP Resource ≠ ArcForges Resource`** ([I-076](../requirements/01-normative-glossary-and-invariants.md#rule-i-076)). MCP's own `Task` and `Skill` never conflate with ArcForges' (**[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**, glossary §9). |
| **Application ↔ Cloud** | Every first-party client uses authored public proto over binary gRPC-Web. Only isolated child boundaries use private helper proto over Named Pipe/UDS; same-process handlers need no wire transport. |

[Registry 04](contracts/04-protobuf-wire-registry.md) owns generated public/private messages and named standard-protocol exceptions; there is no second business DTO authority.

---

## 16. Contract-authoring obligations

These are **hard authoring rules**, not optimisations. [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) replaces the historical local-RPC generator rules with the following proto rules.

| # | Obligation |
|---|---|
| <a id="rule-ca-01"></a>CA-01 | Author business wire services/messages in Contracts handwritten proto, using the complete field registry. |
| <a id="rule-ca-02"></a>CA-02 | Generate C#/TS bindings and released descriptors from that source; never edit generated code. |
| <a id="rule-ca-03"></a>CA-03 | Explicitly register generated services/serializers; no runtime contract scanning. |
| <a id="rule-ca-04"></a>CA-04 | Preserve per-owner service/package boundaries, independent versions and license closure. |
| <a id="rule-ca-05"></a>CA-05 | Use explicit request/result messages; no overloaded wire method, CLR property or generic service. |
| <a id="rule-ca-06"></a>CA-06 | Unary methods use bounded async generated clients and cancellation/deadline propagation. |
| <a id="rule-ca-07"></a>CA-07 | Events are typed hints in EventService.Poll; owner snapshots/cursors decide state. |
| <a id="rule-ca-08"></a>CA-08 | Dispose channels/leases on peer restart and rebuild authenticated bindings. |
| <a id="rule-ca-09"></a>CA-09 | Writes carry CommandId, target identity and the exact owner revision kind. |
| <a id="rule-ca-10"></a>CA-10 | No object/dynamic/Type/ORM/view model/native pointer crosses a wire boundary. |
| <a id="rule-ca-11"></a>CA-11 | C# and TS values follow the exact protobuf/JSON projection profile and independent vectors. |
| <a id="rule-ca-12"></a>CA-12 | All 17 hint payloads are generated from the same event registry. |
| <a id="rule-ca-13"></a>CA-13 | C# uses generated gRPC-Web, React generated gRPC-Web, Kotlin Android generated gRPC-Web; HTTP exceptions are separately typed. |
| <a id="rule-ca-14"></a>CA-14 | Published service, method, field names/numbers are permanent; reserve removals and check previous/current compatibility. |

**A repository-policy test asserts [CA-01](#rule-ca-01) through [CA-03](#rule-ca-03) and [CA-11](#rule-ca-11) through [CA-13](#rule-ca-13) mechanically** (`§7.2` of the layout architecture).

---

### 16.1 TypeScript consumers and exact JSON values

[P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) selects handwritten proto and generated C#/TS packages in [the wire registry](contracts/04-protobuf-wire-registry.md). Native/TS binary values and their JSON-exception projections follow that exact-value profile. SDK generation is followed by real client tests of auth, idempotency, streaming and compatibility against the same operation catalogue.

---

## 17. Domain model

```
AppId · AppInstallation · AppInstance · AppContribution
CapabilityId · CapabilityDescriptor · CapabilityVersion · CapabilityAvailability
Action · ActionDescriptor
ContextProvider · ContextDescriptor · ContextBinding · ContextSnapshot
ResourceRef · ResourceKind · ResourceVersionRef · TypedResourceSelection
Artifact · ArtifactRef · ArtifactKind · ArtifactHandler
DeepLink · DeepLinkRoute
IntegrationEvent · EventType · EventId · EventSequence
HealthSnapshot · InstancePresence · InstanceHealth · InstanceReadiness
CompatibilityDescriptor · ContractVersion · FeatureSet
Invocation · InvocationId · InvocationTarget · InvocationResult · SemanticError
SuggestedTask · CorrelationId · CausationId
```

---

## 18. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Normative Glossary and Invariant Catalogue](../requirements/01-normative-glossary-and-invariants.md) | Owns the semantic vocabulary and distinctions |
| [ArcForges Product Scope and Portfolio](../requirements/00-product-scope-and-portfolio.md) | Owns product interaction, ownership and routing boundaries |
| [Operation Catalogue](contracts/00-operation-catalogue.md) | Defines common operation envelopes, errors, idempotency and compatibility |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Contract granularity and generated compatibility artifacts |
| **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | The Apache interoperability boundary for schemas, DTOs, clients and contract validators |
| **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)** | The contract-authoring obligation that makes proxies AOT- and trim-safe |
| **[V-05c](../assurance/phase-1-official-verification.md#rule-v-05c)**, **[F-026](../assurance/open-gates-register.md#rule-f-026)** | The typed-HTTP-client entry point and reflection-package prohibition |
| **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** | MCP statelessness and the vocabulary disambiguation requirement |
