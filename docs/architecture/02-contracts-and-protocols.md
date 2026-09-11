# Contracts, Protocols and the Cross-Application Semantic Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (Apache interoperability boundary), **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)** (contract-authoring obligation), **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** (MCP)
> Companions: [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md), [`03-local-ipc-and-process-model.md`](03-local-ipc-and-process-model.md), [`../requirements/01-normative-glossary-and-invariants.md`](../requirements/01-normative-glossary-and-invariants.md)

> **What is shared across products is the semantic contract, not the domain model.**

ArcChat must be able to orchestrate ArcNotes, ArcScope and ArcSlate without referencing any of their domain entities, and each product must be able to evolve its domain freely without breaking the others.

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
| CM-01 | **Shared foundation is small and stable; product capability contracts are independently owned and versioned by their owning product** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| CM-02 | **An upgrade to one product must never force an unrelated product to recompile or re-release** ([I-032](../requirements/01-normative-glossary-and-invariants.md#rule-i-032) family). |
| CM-03 | **The foundation contract package holds only genuinely long-term stable types.** Product-specific concepts are prohibited in it. |
| CM-04 | **A cross-application envelope never contains `object`** ([I-328](../requirements/01-normative-glossary-and-invariants.md#rule-i-328)). Payloads are typed by the owning product's contract. |
| CM-05 | **Cross-application contracts are AOT-friendly by construction**: source-generated serialization, no runtime type resolution, no assembly-qualified type names on the wire. |
| CM-06 | **A small amount of extensible metadata is permitted and must not become a domain dumping ground.** |

---

## 2. Application, installation and instance

| Concept | Definition | Lifetime |
|---|---|---|
| **`AppId`** | A stable ArcForges product identity | Permanent |
| **`AppInstallation`** | One installed copy on one device | Until uninstalled |
| **`AppInstance`** | A running instance that can actually provide local capabilities | One process lifetime |

| # | Rule |
|---|---|
| AI-01 | **`AppId` is stable forever** and never encodes version, process or platform. |
| AI-02 | **`AppId ≠ ProductScope`** ([I-005](../requirements/01-normative-glossary-and-invariants.md#rule-i-005)). One is runtime identity; the other is a commercial scoping concept. |
| AI-03 | **`AppId ≠ Process`** ([I-006](../requirements/01-normative-glossary-and-invariants.md#rule-i-006)). **`AppId → unique process` must never be assumed** ([I-009](../requirements/01-normative-glossary-and-invariants.md#rule-i-009)). |
| AI-04 | **An installation exists independently of any running instance.** Static contribution metadata is readable before the product starts. |
| AI-05 | **An instance may host several window and document sessions**, and one product may have several concurrent instances. |
| AI-06 | **An instance restart produces a new `InstanceId`** ([I-008](../requirements/01-normative-glossary-and-invariants.md#rule-i-008)). |
| AI-07 | **Resource identity never depends on `InstanceId`**; **context identity may** (`§6.3`). |
| AI-08 | **Application information is not deleted when an instance dies.** The installation and its static contributions remain. |
| AI-09 | The term for a capability host in cross-application context is **App Instance**, never "provider" — "provider" is reserved for AI and external service providers ([I-115](../requirements/01-normative-glossary-and-invariants.md#rule-i-115), [I-116](../requirements/01-normative-glossary-and-invariants.md#rule-i-116)). |

---

## 3. Contribution model

A product declares what it offers through a **contribution manifest**, not by ArcChat hard-coding its behaviour.

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
| CB-01 | **ArcChat must never hard-code product behaviour.** A `switch (appId)` over product identities is prohibited. |
| CB-02 | **Contribution is description, not authority** ([I-042](../requirements/01-normative-glossary-and-invariants.md#rule-i-042)). Declaring a capability grants the caller nothing. |
| CB-03 | **Discovery reads contributions; it never scans a product's domain** (`§13`). |
| CB-04 | **Static contribution metadata exists before start-up**; a running instance's registration then **overrides runtime availability**. |
| CB-05 | **`Static Capability ≠ Runtime Capability Availability`** ([I-045](../requirements/01-normative-glossary-and-invariants.md#rule-i-045)). |
| CB-06 | **Adding a new product must not require changing ArcChat's domain**. |

---

## 4. Capability

**`Capability` = a stable semantic capability a product exposes for machine invocation.**

### 4.1 Identity

| # | Rule |
|---|---|
| CP-01 | **A capability has a stable, namespaced `CapabilityId`**, owned by the contributing product: `arcnotes.document.create`, `arcscope.session.compare`, `arcslate.timeline.move-clip`. |
| CP-02 | **The string is used only for discovery, display, policy, tool selection, routing and audit.** The actual call lands on a compiled, strongly typed interface method (**[AC-02](00-architecture-overview.md#rule-ac-02)**). |
| CP-03 | **A capability is business semantics, not a CRUD mapping.** `arcnotes.document.insert-block` is a capability; `arcnotes.table.row.update` is not. |
| CP-04 | **`Capability ≠ UI Command`** ([I-041](../requirements/01-normative-glossary-and-invariants.md#rule-i-041)). A local menu item is not automatically a cross-application capability; a capability is a domain behaviour with cross-application value. |
| CP-05 | **`Capability ≠ Action`** ([I-040](../requirements/01-normative-glossary-and-invariants.md#rule-i-040)), **`Capability ≠ Permission`** ([I-042](../requirements/01-normative-glossary-and-invariants.md#rule-i-042)), **`Capability ≠ Package`** ([I-044](../requirements/01-normative-glossary-and-invariants.md#rule-i-044)). |
| CP-06 | **One classification system, not three.** Read, write and long-running operations are all capabilities, differing by declared metadata — not by living in separate mechanisms. |
| CP-07 | **A `CapabilityId` is not changed for an additive change.** A breaking change produces a new capability identity or a new contract version (`§8`). |

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
| CD-01 | **Retry safety is declared by the owner, never guessed by the caller** ([FL-08](../requirements/05-ai-and-agent-execution.md#rule-fl-08) in the AI requirements). |
| CD-02 | **Capability metadata must not reveal internal implementation detail** — no type names, no storage structure, no internal paths. |
| CD-03 | **Every capability declares its risk baseline**; runtime modifiers may raise it and third-party metadata may never lower it ([RK-03](../requirements/07-security-privacy-and-trust.md#rule-rk-03)). |

---

## 5. Action

**`Action` = a context-sensitive executable entry displayed to a user.**

| # | Rule |
|---|---|
| AC-01 | **`Action ≠ Capability`** ([I-040](../requirements/01-normative-glossary-and-invariants.md#rule-i-040)) and **`Action ≠ Capability Invocation`** ([I-043](../requirements/01-normative-glossary-and-invariants.md#rule-i-043)). An action is user-experience semantics; a capability is execution semantics. |
| AC-02 | **Not every capability is surfaced as an action**, and **an action may map to several capabilities**. |
| AC-03 | An `ActionDescriptor` declares: identity, display, applicable context kinds, the capability or capabilities it invokes, and its availability rule. |
| <a id="rule-ac-04"></a>AC-04 | **Availability is a dynamic projection**, expressing at minimum: `Available`, `NotApplicableToContext`, `AppNotInstalled`, `AppNotRunning`, `IncompatibleVersion`, `PermissionRequired`, `EntitlementRequired`, `PolicyDisabled`, `TemporarilyUnavailable`. |
| AC-05 | **A permission-required action is not hidden forever.** It is shown and routes into the ordinary approval and permission flow ([UX-01](../requirements/07-security-privacy-and-trust.md#rule-ux-01)). |

---

## 6. Context

**`Context Provider` = a product exposing a read-only description of what the user is currently focused on.**

| # | Rule |
|---|---|
| CX-01 | **`Context Provider ≠ Resource Database`** ([I-048](../requirements/01-normative-glossary-and-invariants.md#rule-i-048)) and **≠ Search Engine** ([I-047](../requirements/01-normative-glossary-and-invariants.md#rule-i-047)). It answers *current, relevant, bounded*; querying and search are capabilities. |
| CX-02 | **A context provider supplies description and references, never bulk content** ([I-049](../requirements/01-normative-glossary-and-invariants.md#rule-i-049)). |
| CX-03 | **Context is either stable or ephemeral.** Stable context references durable resources; ephemeral context reflects transient selection. |
| CX-04 | **Ephemeral context is bound to an `InstanceId`** and carries **generation and expiry** semantics. |
| CX-05 | **Ephemeral context is frozen before a task is created** ([IB-01](../requirements/05-ai-and-agent-execution.md#rule-ib-01)). Once frozen, the task's input is fixed. |
| CX-06 | **Context freeze is not a copy of all data** ([I-049](../requirements/01-normative-glossary-and-invariants.md#rule-i-049)). It is stable references plus typed selection. |
| CX-07 | **Context that cannot be frozen must not be presented as persistent.** It is for immediate use only. |
| CX-08 | **A context provider grants no read permission** ([I-046](../requirements/01-normative-glossary-and-invariants.md#rule-i-046)). Reading the referenced content still goes through capability plus authorization. |
| CX-09 | **A context provider cannot silently expand scope** ([AS-05](../requirements/06-knowledge-search-and-retrieval.md#rule-as-05)). |
| CX-10 | **`Context ≠ Resource`** ([I-046](../requirements/01-normative-glossary-and-invariants.md#rule-i-046)), and **`Current Selection ≠ durable resource identity`** ([I-050](../requirements/01-normative-glossary-and-invariants.md#rule-i-050)). |

---

## 7. Resource and reference

**`Resource` = a stably identifiable business object or asset owned by exactly one authoritative owner product.**
**`ResourceRef` = a stable, lightweight, non-writable reference to a resource in its owner.**

### 7.1 `ResourceRef`

Carries: realm, workspace scope where applicable, owning `AppId`, namespaced `ResourceKind`, `ResourceId`, optional display hint, and an availability hint.

| # | Rule |
|---|---|
| <a id="rule-rr-01"></a>RR-01 | **`ResourceKind` is namespaced by owner**: `arcnotes.document`, `arcnotes.block`, `arcscope.session`, `arcslate.sequence`. |
| RR-02 | **A file path is never an identity** ([I-052](../requirements/01-normative-glossary-and-invariants.md#rule-i-052), [I-195](../requirements/01-normative-glossary-and-invariants.md#rule-i-195)). |
| RR-03 | **A `ResourceRef` never contains**: a file path, a native pointer, an internal database key, a connection handle, credentials, or the resource's content ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). |
| <a id="rule-rr-04"></a>RR-04 | **`ResourceId` is never reused** (`§2` of the glossary). |
| RR-05 | **Rename does not change the reference** ([SY-11](../requirements/03-cloud-services-and-sync.md#rule-sy-11)). **Move does not change the reference.** |
| RR-06 | **Deleting a resource does not degrade its reference to a plain string.** The reference remains valid as an identity, resolving to a deleted state; restoring the resource makes it resolvable again ([DE-03](../requirements/03-cloud-services-and-sync.md#rule-de-03)). |
| RR-07 | **Copy or import produces a new resource with a new `ResourceId`** (`§4.2` of the product scope). |
| RR-08 | **`ResourceRef` and `ResourceVersionRef` are different** (`§7.2`). |
| <a id="rule-rr-09"></a>RR-09 | **A reference is location-independent and works across devices.** The same logical object has one reference; **availability is separate from identity** ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). |
| RR-10 | **A local-only resource still has a reference**, with availability naming the device that holds it. |
| RR-11 | **A reference never expands visibility** ([I-054](../requirements/01-normative-glossary-and-invariants.md#rule-i-054)). Dereferencing an unauthorised reference returns a permission failure. |
| RR-12 | **`ResourceRef ≠ Capability Token`** ([I-053](../requirements/01-normative-glossary-and-invariants.md#rule-i-053)) and **≠ permission token** ([I-054](../requirements/01-normative-glossary-and-invariants.md#rule-i-054)). It is an address, not an authorization. |
| RR-13 | **Dereferencing is always controlled by the owner** ([I-055](../requirements/01-normative-glossary-and-invariants.md#rule-i-055)). |
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
| TS-01 | **A `ResourceRef` is not stuffed with sub-paths** ([I-055](../requirements/01-normative-glossary-and-invariants.md#rule-i-055)). |
| TS-02 | **No universal selection schema is created.** ArcNotes block ranges, ArcScope time and signal ranges, and ArcSlate timeline ranges are structurally different and are typed by their owners. |
| TS-03 | **`ResourceRef ≠ Resource Selection`** ([I-056](../requirements/01-normative-glossary-and-invariants.md#rule-i-056)). |

---

## 8. Artifact

**`Artifact` = a record of a result that has independent user value.**

| # | Rule |
|---|---|
| AR-01 | **`Artifact ≠ Resource`** ([I-058](../requirements/01-normative-glossary-and-invariants.md#rule-i-058)) and **`ArtifactRef ≠ ResourceRef`** ([I-059](../requirements/01-normative-glossary-and-invariants.md#rule-i-059)). |
| AR-02 | **An artifact record carries**: identity, namespaced `ArtifactKind`, producing task and run, actor chain, time, provenance, a reference to the underlying resource where one exists, and availability. |
| AR-03 | **A professional product's artifact is owned by that product**; ArcChat records the artifact relationship, not the content. |
| AR-04 | **An ArcChat-native artifact is owned by ArcChat**, which then owns the corresponding resource or payload. |
| AR-05 | **Deleting an artifact record never deletes the resource** ([I-060](../requirements/01-normative-glossary-and-invariants.md#rule-i-060)). Deleting the resource requires calling the owner's capability explicitly. |
| AR-06 | **`Artifact Handler` declares which artifact kinds a product can handle** and with which capabilities — open, preview, import, convert, edit. |
| AR-07 | **When several products can handle an artifact, resolution is deterministic** ([EP-06](../requirements/08-extensions-and-developer-platform.md#rule-ep-06)): explicit preference, then a documented rule, never a random pick. |
| AR-08 | **Artifact preview is a derived projection** ([I-060](../requirements/01-normative-glossary-and-invariants.md#rule-i-060)), never artifact content authority. |
| AR-09 | **`ArtifactRef` is not a permission token** ([I-054](../requirements/01-normative-glossary-and-invariants.md#rule-i-054) family). |

---

## 9. Deep link

**`Deep Link` = a navigation and handoff contract, not a remote command contract** ([I-062](../requirements/01-normative-glossary-and-invariants.md#rule-i-062)).

| # | Rule |
|---|---|
| DL-01 | **A deep link may**: open a product, navigate to a location, address a resource, or carry a handoff intent. |
| DL-02 | **A deep link may not, by default**: perform a side-effecting operation, bypass confirmation, or grant authority. It routes into the ordinary UI, capability and approval path. |
| DL-03 | **A deep link may carry intent; it never represents authorized execution.** |
| DL-04 | **Deep links address stable identity** — a `ResourceRef` or a logical route — never an absolute path (`DL-04` in the shared desktop requirements). |
| DL-05 | **Cloud objects use an HTTPS canonical link**; `arcforges://` is the desktop local routing scheme. Both resolve to the same logical object. |
| DL-06 | **A private HTTPS link is not a public share link** ([I-279](../requirements/01-normative-glossary-and-invariants.md#rule-i-279)). Permission is always checked at access. |
| DL-07 | **An externally originated deep link is always untrusted input** ([DL-02](../requirements/09-shared-desktop-experience.md#rule-dl-02) there). |
| DL-08 | **Secrets are prohibited in deep links** ([DL-03](../requirements/09-shared-desktop-experience.md#rule-dl-03) there). |
| DL-09 | **A deep link is not a capability token** ([I-063](../requirements/01-normative-glossary-and-invariants.md#rule-i-063)). |

---

## 10. Event

**`Event` = an observable fact that has already occurred.**

| # | Rule |
|---|---|
| EV-01 | **`Event ≠ Command`** ([I-064](../requirements/01-normative-glossary-and-invariants.md#rule-i-064)). A command requests; an event reports. |
| EV-02 | **An event is produced after the business fact is committed**. |
| EV-03 | **Every event carries a stable `EventId`**, because delivery is at-least-once; consumers deduplicate by `EventId`. |
| EV-04 | **Every event carries causation and correlation**, which is what makes automation loop detection possible ([LP-01](../requirements/05-ai-and-agent-execution.md#rule-lp-01)). |
| EV-05 | **An event references resources rather than copying large content** ([I-051](../requirements/01-normative-glossary-and-invariants.md#rule-i-051)). |
| EV-06 | **Durable integration events and ephemeral signals are distinguished** ([I-065](../requirements/01-normative-glossary-and-invariants.md#rule-i-065)). A durable event is a business fact; an ephemeral signal is a realtime experience. |
| <a id="rule-ev-07"></a>EV-07 | **Automation subscribes only to durable events by default.** A high-rate signal may be explicitly promoted into a durable event, with throttling. |
| EV-08 | **A generic `Changed` event is not exposed as the primary ecosystem contract.** Events are semantic. |
| <a id="rule-ev-09"></a>EV-09 | **There is no global ArcForges event sequence.** Ordering is per stream or per resource; a global absolute order is never implied. |
| <a id="rule-ev-10"></a>EV-10 | **Event loss must not destroy state** ([I-066](../requirements/01-normative-glossary-and-invariants.md#rule-i-066)). State is recoverable by query. |
| EV-11 | **An event grants no permission** (`§8` of the security requirements). |

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
| HL-01 | **These dimensions must never be merged into one flag.** |
| HL-02 | **`Health ≠ Trust`** ([I-070](../requirements/01-normative-glossary-and-invariants.md#rule-i-070)), **`Health ≠ Compatibility`** ([I-069](../requirements/01-normative-glossary-and-invariants.md#rule-i-069)), **`Health ≠ Capability Availability`** ([I-071](../requirements/01-normative-glossary-and-invariants.md#rule-i-071)), **`Presence ≠ Readiness`** ([I-068](../requirements/01-normative-glossary-and-invariants.md#rule-i-068)). |
| HL-03 | **A health snapshot is not a business state image.** It carries operational state only. |
| HL-04 | **Out-of-contact instances are evicted by lease**, not by guesswork (`§4.3` of the local IPC architecture). |

---

## 12. Compatibility and versioning

| # | Rule |
|---|---|
| <a id="rule-vc-01"></a>VC-01 | **Compatibility is negotiated per capability**, not per product version. |
| VC-02 | **App version is information, not the compatibility criterion** ([I-025](../requirements/01-normative-glossary-and-invariants.md#rule-i-025)). Contract and capability versions decide. |
| VC-03 | **Compatibility is layered**: foundation contract version, per-product contract set version, per-capability version, feature set. |
| VC-04 | **Not every version change affects the whole product.** Partial compatibility is expressible: some capabilities available, others not. |
| VC-05 | **A destructive contract change follows semantic versioning rules** and produces either a new capability identity or a coexisting `V2` interface with a stated migration window. |
| VC-06 | **A feature flag is not a capability version** ([I-072](../requirements/01-normative-glossary-and-invariants.md#rule-i-072)). One says whether a capability has been released; the other says what shape it has. |
| VC-07 | **Compatibility negotiation completes before invocation.** An incompatible call is refused with a specific reason, not attempted and failed. |
| VC-08 | **An owner's internal schema version is never the platform compatibility axis** (`§14` of the quality contract). |
| VC-09 | **Contract compatibility tests retain the previous stable client assembly, serialized golden vectors and AOT publish artifacts** ([CT-02](../requirements/12-quality-and-compatibility-contract.md#rule-ct-02) there). |
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

Fixed priority:

1. The invocation names an `InstanceId` explicitly
2. The target resource is already bound to an online instance (**resource affinity**)
3. The user's currently selected default instance for that product
4. The single healthy instance of that product
5. Otherwise → **`SelectionRequired`**

| # | Rule |
|---|---|
| RT-01 | **"The most recently started instance" is never a universal default.** |
| RT-02 | **Resource affinity is a routing hint, not an ownership migration.** |
| RT-03 | **If the product is installed but not running**, the caller may request a launch, subject to permission, and then retry. |
| RT-04 | **If the product is not installed**, the result is `NotInstalled`, with a route to obtain it. |
| RT-05 | **The Hub never picks silently at random when several candidates exist.** |

### 13.4 Authorization

| # | Rule |
|---|---|
| AU-01 | **Validation and authorization are separate.** Shape validity is not permission. |
| AU-02 | **The owner authorizes again at the final execution point** ([DP-02](../requirements/07-security-privacy-and-trust.md#rule-dp-02) in the security requirements). Steps performed in ArcChat, the Hub or Cloud never substitute for owner-side authorization. |
| AU-03 | **A capability invocation never carries a UI object**, a control, a view model, a native pointer or a `SafeHandle`. Input is semantic. |

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
| ER-01 | **"Failed" alone is prohibited.** The semantic error set includes at minimum: `NotFound`, `PermissionDenied`, `ApprovalRequired`, `ApprovalDenied`, `Conflict`, `PreconditionFailed`, `InvalidInput`, `Unsupported`, `IncompatibleVersion`, `NotInstalled`, `NotRunning`, `SelectionRequired`, `Busy`, `RateLimited`, `BudgetExceeded`, `EntitlementRequired`, `PolicyDisabled`, `ResourceUnavailable`, `Timeout`, `ExternalEffectUnknown`, `Internal`. |
| ER-02 | **`Conflict` is first-class platform semantics** ([I-092](../requirements/01-normative-glossary-and-invariants.md#rule-i-092) family). It reports the current revision, a disclosure-safe conflict summary, whether automatic replay is possible, and a recommended action. **Silent last-write-wins is prohibited.** |
| ER-03 | **A stable error code never changes with localisation** ([CT-03](../requirements/12-quality-and-compatibility-contract.md#rule-ct-03) in the quality contract). |
| ER-04 | **Health, compatibility and permission failures produce distinct user experiences** ([ER-08](../requirements/09-shared-desktop-experience.md#rule-er-08) in the shared desktop requirements). "ArcScope unavailable" must not stand in for "you lack permission". |
| ER-05 | **Provenance is carried end to end**: actor chain, caller instance, capability, invocation, command, task, run, step, approval — through to the owner's domain revision. |

---

## 14. Suggested tasks

| # | Rule |
|---|---|
| SG-01 | **A suggested task is a recommendation**, never automatically executed. |
| SG-02 | **A suggestion carries no additional permission.** |
| SG-03 | **Suggestions are contextual**, derived from the current context provider output, and are a discovery mechanism rather than a workflow engine. |

---

## 15. Relationship to adjacent systems

| Pair | Relationship |
|---|---|
| **Cross-application model ↔ Search** | A search result is a projection, not resource authority ([SR-03](../requirements/06-knowledge-search-and-retrieval.md#rule-sr-03)). |
| **Cross-application model ↔ Extensions** | Native products and third-party extensions may share semantics; **trust differs** (`§9` of the security requirements). |
| **Cross-application model ↔ MCP** | **MCP is an edge adapter, never the internal protocol** ([I-307](../requirements/01-normative-glossary-and-invariants.md#rule-i-307)). **`MCP Resource ≠ ArcForges Resource`** ([I-076](../requirements/01-normative-glossary-and-invariants.md#rule-i-076)). MCP's own `Task` and `Skill` never conflate with ArcForges' (**[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**, glossary §9). |
| **Cross-application model ↔ Cloud** | **Local RPC and the public API are not required to share one wire contract.** Each carries the appropriate versioned DTO for its boundary. |

**A universal protocol is not reinvented for the sake of a unified semantic model.** Three transports remain, each with its own DTOs.

---

## 16. Contract-authoring obligations

These are **hard authoring rules**, not optimisations. [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) replaces the historical local-RPC generator rules with the following proto rules.

| # | Obligation |
|---|---|
| <a id="rule-ca-01"></a>CA-01 | Author business wire services/messages in Contracts handwritten proto, using the complete field registry. |
| CA-02 | Generate C#/TS bindings and released descriptors from that source; never edit generated code. |
| <a id="rule-ca-03"></a>CA-03 | Explicitly register generated services/serializers; no runtime contract scanning. |
| CA-04 | Preserve per-owner service/package boundaries, independent versions and license closure. |
| CA-05 | Use explicit request/result messages; no overloaded wire method, CLR property or generic service. |
| CA-06 | Unary methods use bounded async generated clients and cancellation/deadline propagation. |
| CA-07 | Events are typed hints in EventService.Poll; owner snapshots/cursors decide state. |
| CA-08 | Dispose channels/leases on peer restart and rebuild authenticated bindings. |
| CA-09 | Writes carry CommandId, target identity and the exact owner revision kind. |
| CA-10 | No object/dynamic/Type/ORM/view model/native pointer crosses a wire boundary. |
| <a id="rule-ca-11"></a>CA-11 | C# and TS values follow the exact protobuf/JSON projection profile and independent vectors. |
| CA-12 | All 17 hint payloads are generated from the same event registry. |
| <a id="rule-ca-13"></a>CA-13 | C# uses generated gRPC, React generated gRPC-Web, RN the bounded unary adapter; HTTP exceptions are separately typed. |
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
