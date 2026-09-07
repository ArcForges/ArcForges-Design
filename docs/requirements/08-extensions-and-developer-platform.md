# Extensions, Integrations and Developer Platform Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (AOT matrix), **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (Apache-2.0 SDK boundary), **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** (MCP `2026-07-28`)
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`05-ai-and-agent-execution.md`](05-ai-and-agent-execution.md), [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`../architecture/15-extension-platform-architecture.md`](../architecture/15-extension-platform-architecture.md)

The extensibility surface, in layers of increasing power and decreasing implicit trust:

```
Skill        declarative agent guidance             no code, no capability
Template     parameterised initial blueprint        no code, no capability
Workflow     reusable execution blueprint           orchestrates existing capabilities
MCP          external capability integration        adapter to an external server
Connector    long-lived external relationship       identity + data + capability
External Agent  excluded                           no delegation/ACP executor
Extension    installable executable component       out-of-process, adds new capability
Third-party App  standalone Arc application         its own product, own domain
```

---

## 1. Skill

**Skill = versionable, reusable agent methodology and working knowledge.**

| # | Requirement |
|---|---|
| SK-01 | **A Skill is never code** ([I-291](01-normative-glossary-and-invariants.md#rule-i-291)). It is declarative agent guidance, not a runtime plug-in. |
| SK-02 | **A Skill confers no capability** ([I-290](01-normative-glossary-and-invariants.md#rule-i-290)) and **grants no permission** ([I-264](01-normative-glossary-and-invariants.md#rule-i-264)). It may *refer to* capabilities; using them still requires the ordinary permission and approval path. |
| SK-03 | Skills are **versioned**. A skill update does not modify historical results; a completed Run keeps the skill version it executed under. |
| SK-04 | **Skill ≠ MCP** ([I-292](01-normative-glossary-and-invariants.md#rule-i-292)) and **MCP Prompt ≠ Skill** ([I-310](01-normative-glossary-and-invariants.md#rule-i-310)). An MCP prompt does not automatically become a Skill. |
| SK-05 | A user may **fork** a community skill; the fork becomes a user-owned skill with its own lifecycle. |
| SK-06 | A packaged skill's content is **read-only managed content**; customising it produces an independent user-owned resource rather than mutating the package. |

## 2. Template

**Template = a parameterisable initial blueprint used when creating a resource or configuration.**

| # | Requirement |
|---|---|
| TP-01 | **Template ≠ Skill** ([I-293](01-normative-glossary-and-invariants.md#rule-i-293)). A template shapes a created resource; a skill shapes agent behaviour. |
| TP-02 | **Templates materialise by default.** The created resource exists independently of the template. |
| TP-03 | **A template update must not silently change existing user documents** ([I-294](01-normative-glossary-and-invariants.md#rule-i-294)). A linked-template model, if ever offered, is an explicit opt-in with explicit update semantics. |
| TP-04 | Template parameters are **typed and declared**, not free-form substitution. |
| TP-05 | **Materialisation goes through the owning product's capability**, never a direct write into that product's store. |
| TP-06 | A template may declare **requirements**; unmet requirements are shown before use. |

## 3. Workflow

**Workflow = a reusable work execution blueprint.**

| # | Requirement |
|---|---|
| WF-01 | **Workflow ≠ Task** ([I-296](01-normative-glossary-and-invariants.md#rule-i-296)). Running a workflow creates a Task under the Stage-19 model; the workflow is the blueprint. |
| WF-02 | **Workflow ≠ Automation** ([I-295](01-normative-glossary-and-invariants.md#rule-i-295), [I-299](01-normative-glossary-and-invariants.md#rule-i-299)). A workflow says *how*; an automation says *when*. |
| WF-03 | **Workflow ≠ Agent Plan** ([I-297](01-normative-glossary-and-invariants.md#rule-i-297)). A workflow is authored and deterministic in structure; an agent plan is generated per run and revisable. |
| WF-04 | **A workflow update does not change a running Task.** Running Tasks keep their frozen execution snapshot. |
| WF-05 | **A workflow is not a second agent runtime.** It compiles into ordinary Steps in the one execution model. |
| WF-06 | **No scripting language is introduced** ([I-298](01-normative-glossary-and-invariants.md#rule-i-298)). Workflow steps are declared, typed and closed: invoke capability, branch on a declared condition, iterate a bounded collection, wait for approval, wait for a product job, produce an artifact. |
| WF-07 | **Unbounded looping is not a workflow capability.** Recurrence belongs to Automation triggers. |
| WF-08 | **A community workflow obtains no implicit permission** ([I-265](01-normative-glossary-and-invariants.md#rule-i-265)). Each step passes the full security pipeline. |
| WF-09 | A workflow may depend on **connector capabilities**; the resulting run is an ordinary root Task. |
| WF-10 | Missing requirements are surfaced at install time with a legible "why can't this run" explanation. |

## 4. Automation

Automation is specified in [`05-ai-and-agent-execution.md`](05-ai-and-agent-execution.md) §10. Here only the platform relationship is fixed: an automation may reference a workflow, a skill and a template; none of those grant it authority, and every triggered Task re-authorises.

---

## 5. MCP

**MCP = an external capability integration adapter.**

| # | Requirement |
|---|---|
| <a id="rule-mc-01"></a>MC-01 | **MCP never becomes the internal protocol of ArcForges** ([I-307](01-normative-glossary-and-invariants.md#rule-i-307)). Internal cross-product capability remains the native semantic capability model. MCP is an edge adapter. |
| <a id="rule-mc-02"></a>MC-02 | **An MCP tool maps to a capability** in the ArcForges model, carrying declared risk, permission requirements and provenance — it is not injected as a raw tool into the agent. |
| MC-03 | **An MCP resource is not an ArcForges resource** ([I-076](01-normative-glossary-and-invariants.md#rule-i-076), [I-309](01-normative-glossary-and-invariants.md#rule-i-309)). It is addressed by the server's own scheme and surfaced as an external source. |
| MC-04 | **MCP Definition ≠ MCP Connection** ([I-309](01-normative-glossary-and-invariants.md#rule-i-309)). The integration definition or package is distinct from a live connection instance. |
| MC-05 | **MCP ≠ Connector** ([I-308](01-normative-glossary-and-invariants.md#rule-i-308)). MCP may be used *inside* a connector; a connector is a higher-level relationship. |
| MC-06 | **MCP is not a marketplace package ABI.** An MCP server is reached through an integration package, not treated as ArcForges' extension binary format. |
| <a id="rule-mc-07"></a>MC-07 | **MCP tool descriptions, prompts and resource contents are untrusted data** ([I-262](01-normative-glossary-and-invariants.md#rule-i-262)), never instructions. |
| MC-08 | Per **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**: the `2026-07-28` revision is stable and the official C# SDK is stable. The protocol core is **stateless** — no `initialize` exchange, no session header, per-request capability negotiation — so **ArcForges must not build session identity on MCP transport state**. Server-to-client requests use multi round-trip requests, which is a transport mechanism and not an ArcForges execution concept. |
| MC-09 | **The exact MCP C# SDK version is pinned at first consumption**, and an explicit mapping between MCP extension concepts (its own `Task`, `Skill`) and the ArcForges execution vocabulary is recorded (see glossary §9). *Owner: Architecture Owner. Trigger: start of the MCP/extension work package.* |
| <a id="rule-mc-10"></a>MC-10 | An MCP server changing its tool set **re-enters permission review** ([TR-10](07-security-privacy-and-trust.md#rule-tr-10) in the security requirements). |

## 6. Connector

**Connector = an ArcForges integration with an external system that establishes a long-term identity, data and capability relationship.**

| # | Requirement |
|---|---|
| CN-01 | **Connector Definition ≠ Connection Instance** ([I-311](01-normative-glossary-and-invariants.md#rule-i-311)). One definition supports many connections. |
| CN-02 | A connection owns: its external identity binding, its credentials **by reference only**, its scope, its sync state, its health, and its audit trail. |
| CN-03 | **A secret never enters connector configuration** ([SE-01](07-security-privacy-and-trust.md#rule-se-01)). Configuration holds `SecretRef`; plaintext keys are never stored in it. |
| CN-04 | A connector may contribute capabilities, resources, knowledge sources and events. |
| CN-05 | **Live Connector ≠ Imported Resource** ([I-312](01-normative-glossary-and-invariants.md#rule-i-312)). Querying an external system live is different from importing, which creates a new owned resource in an owning product. |
| CN-06 | **A connector sync projection is not external authority.** It is a derived, replica-semantics projection. |
| CN-07 | A connector may use MCP internally, or a public API directly; either way it remains a connector. |
| CN-08 | **Connector content is data, never instruction** ([I-263](01-normative-glossary-and-invariants.md#rule-i-263)). |
| CN-09 | An OAuth scope expansion requires re-consent ([TR-11](07-security-privacy-and-trust.md#rule-tr-11)). |

## 7. External-agent exclusion

| # | Requirement |
|---|---|
| <a id="rule-ea-01"></a>EA-01 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): external-agent providers and profile-to-external-agent modes are excluded. |
| EA-02 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no ACP external-agent adapter. |
| EA-03 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no external-agent session mapping. |
| EA-04 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no delegation into another agent runtime or independently planning child Task. |
| <a id="rule-ea-05"></a>EA-05 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no external-agent delegation lease. Ordinary bounded tool leases retain security requirements. |
| <a id="rule-ea-06"></a>EA-06 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no external-agent result adapter; ordinary tool results use the accepted result contract. |
| <a id="rule-ea-07"></a>EA-07 | Hidden reasoning is never an extension result or audit requirement. |
| <a id="rule-ea-08"></a>EA-08 | A package/connector/MCP tool cannot bypass this exclusion by starting an autonomous delegated agent. No agent-team or external-agent contribution kind. |

The single Cloud Harness may call authorised tools concurrently within one budget. A tool has declared input/output, effect and timeout semantics; it does not own a model loop or a delegated work goal.

---

## 8. Extension

**Extension = an installable third-party component that adds execution capability to ArcForges or to a product.**

### 8.1 The core security decision

> **Third-party executable extensions run out-of-process by default.**

| # | Requirement |
|---|---|
| <a id="rule-ex-01"></a>EX-01 | **No runtime Avalonia plug-in DLL injection.** Loading arbitrary third-party assemblies into a product's main process is prohibited — it would break the Native AOT main path (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) and remove the isolation boundary at once. |
| <a id="rule-ex-02"></a>EX-02 | **Third-party native code does not enter the main process by default.** It runs inside the extension process. |
| <a id="rule-ex-03"></a>EX-03 | **First-party native adapters are the stated exception**: narrow, product-controlled P/Invoke inside the owning process (Technical Exception C in [`00-product-scope-and-portfolio.md`](00-product-scope-and-portfolio.md) §8.1). This never extends to arbitrary community native plug-ins. |
| <a id="rule-ex-04"></a>EX-04 | **An extension's own implementation is not required to be Native AOT.** The **ArcForges host stays a Native AOT deliverable**; the extension is a separate process with its own runtime. This is precisely what makes a dynamic ecosystem compatible with an AOT product. |
| <a id="rule-ex-05"></a>EX-05 | **Extension processes start on demand** by default and stop when idle. |
| <a id="rule-ex-06"></a>EX-06 | **Background execution must be explicitly declared** in the manifest and separately consented. Adding it in an update is a permission expansion requiring re-consent ([TR-08](07-security-privacy-and-trust.md#rule-tr-08)). |
| <a id="rule-ex-07"></a>EX-07 | **An extension never connects to a product database.** It calls capabilities. |
| <a id="rule-ex-08"></a>EX-08 | **Extension private state is not product canonical domain state** ([I-319](01-normative-glossary-and-invariants.md#rule-i-319)). It has its own store and its own `SchemaVersion`. |
| EX-09 | **An extension creating a professional resource goes through the owner's capability** ([EX-07](#rule-ex-07)), and the resource is owned by that product forever ([I-489](01-normative-glossary-and-invariants.md#rule-i-489) analogue). |
| EX-10 | **Extension isolation is not authorization** ([I-259](01-normative-glossary-and-invariants.md#rule-i-259)); **out-of-process is not automatically safe** ([I-260](01-normative-glossary-and-invariants.md#rule-i-260)). Capability-based access still governs everything. |
| <a id="rule-ex-11"></a>EX-11 | **An extension crash must not crash the owning application.** The product remains open; the affected capability degrades with a clear state. |
| <a id="rule-ex-12"></a>EX-12 | **Extension process identity is bound to the package installation.** A process cannot claim to be a different package, and cannot register a reserved official capability namespace. |
| <a id="rule-ex-13"></a>EX-13 | **Extension output is validated** against its declared schema before entering the product. |
| <a id="rule-ex-14"></a>EX-14 | **Extension process input is minimised** to what the current call requires — never an "ArcForges API full access object". |
| <a id="rule-ex-15"></a>EX-15 | **Extension invocations are traced** as ordinary capability invocations in the task trace and audit, not into a separate plug-in log system. |
| <a id="rule-ex-16"></a>EX-16 | Extension metrics and diagnostics require explicit declaration and consent. **Package analytics and extension telemetry are separate**, and nothing is reported to a publisher automatically. |

### 8.2 The dual capability boundary

The unresolved tension — a strongly typed AOT product versus unknown third-party capabilities — is resolved by **two levels**, not by weakening the core.

| Level | Mechanism | Used for |
|---|---|---|
| **1 — Known typed extension points** | A stable, compile-time typed contract per extension point | The best experience; the default route for anything ArcForges anticipated |
| **2 — Custom extension capability** | A **schema-described extension capability protocol** over a fixed, closed, AOT-safe structured value model | Capabilities ArcForges did not anticipate |

| # | Requirement |
|---|---|
| <a id="rule-db-01"></a>DB-01 | **The structured value model is closed**: null, boolean, integer, decimal/number, string, binary reference, date/time, `ResourceRef`, list, record — with an explicit schema. |
| <a id="rule-db-02"></a>DB-02 | **Prohibited across the extension boundary**: arbitrary CLR objects, runtime `Type`, assembly-qualified type names, native pointers. **`Dictionary<string, object>` is not the extension protocol** ([I-328](01-normative-glossary-and-invariants.md#rule-i-328)). |
| <a id="rule-db-03"></a>DB-03 | **C# developers still get a code-first experience**: C# records plus attributes → source generator → extension schema, serializer and client/server binding. Developers do not hand-maintain JSON Schema. |
| <a id="rule-db-04"></a>DB-04 | **The AOT host needs no knowledge of third-party CLR types.** This is what makes the boundary AOT-safe. |
| <a id="rule-db-05"></a>DB-05 | **The schema exception applies only at the dynamic third-party boundary** ([I-329](01-normative-glossary-and-invariants.md#rule-i-329)). It must never be back-propagated into ArcNotes, ArcScope or ArcSlate native capabilities, which stay compile-time typed. |
| <a id="rule-db-06"></a>DB-06 | **Large data never travels inside a structured extension value.** Large content crosses as a `ResourceRef` with controlled access. |

### 8.3 UI contribution

| # | Requirement |
|---|---|
| UI-01 | **Arbitrary embedding of third-party Avalonia controls is prohibited.** |
| <a id="rule-ui-02"></a>UI-02 | Extension UI contribution uses a **declarative panel protocol** and declarative settings schema. |
| <a id="rule-ui-03"></a>UI-03 | Complex third-party interfaces belong in a **standalone third-party Arc application**, not embedded in a first-party product's process. |
| <a id="rule-ui-04"></a>UI-04 | **A secret settings field returns a `SecretRef`.** Plaintext is never stored in extension configuration. |
| <a id="rule-ui-05"></a>UI-05 | **No general browser-extension WebView platform** is built. It is a large security surface with no corresponding product need. |

### 8.4 Third-party Arc App

| # | Requirement |
|---|---|
| TA-01 | **A third-party Arc App is a standalone complete application** with its own process, domain, storage and lifecycle — distinct from an Extension ([I-317](01-normative-glossary-and-invariants.md#rule-i-317)). |
| TA-02 | It participates through the cross-application contribution model, exactly as a first-party product does. |
| TA-03 | **It is not a first-party application.** Publisher and trust are distinct, and reserved official identifiers and namespaces cannot be claimed. |
| TA-04 | It may hold higher permission than an extension — because it is a peer application — and it is still governed by the same security pipeline. |

---

## 9. Package model

**Arc Package** is the single distribution unit.

| # | Requirement |
|---|---|
| PK-01 | **Package ≠ Contribution** ([I-300](01-normative-glossary-and-invariants.md#rule-i-300)). One package may carry several contributions: skills, templates, workflows, an integration, an extension. |
| PK-02 | A package declares a **primary category** in its manifest, so discovery and trust behave predictably. |
| <a id="rule-pk-03"></a>PK-03 | **`PackageId` never changes across versions**, and `PublisherId` is stable. |
| PK-04 | **Local sideload requires no cloud account.** Publishing to the official community catalog requires a publisher account with verification. |
| <a id="rule-pk-05"></a>PK-05 | **Package version uses semantic versioning** but **`PackageVersion` is not the compatibility mechanism** ([I-301](01-normative-glossary-and-invariants.md#rule-i-301), [I-302](01-normative-glossary-and-invariants.md#rule-i-302)). Package version, extension protocol version, contract version and host application version are four separate things and must never be conflated. |
| PK-06 | **A published version is immutable.** Files for a given version can never be overwritten. |
| PK-07 | **Yank ≠ Revoke** ([I-433](01-normative-glossary-and-invariants.md#rule-i-433), [I-330](01-normative-glossary-and-invariants.md#rule-i-330)). *Yank* removes it from new installation and recommendation; *Revoke* blocks or quarantines execution. *Deprecate* is neither — it signals a successor. |
| PK-08 | A manifest expresses at least: identity, publisher, version, category, contributions, declared permission surface, capability requirements, package dependencies, compatibility, platform targets, licence, security contact, and integrity metadata. |
| PK-09 | **A manifest never contains a secret.** |
| PK-10 | **The manifest must be readable before any extension code executes.** Trust, compatibility and permission decisions all precede execution. |
| PK-11 | **Compatibility is expressed richly**, not as a single "compatible" flag: per-contribution compatibility, allowing "partially usable" states. |
| PK-12 | **Compatibility is ultimately judged per contribution**, not per suite. There is no lockstep suite compatibility requirement. |
| PK-13 | A manifest compatibility check is a **preflight**; the runtime handshake is the ultimate fact. |
| PK-14 | **Platform targets are declared.** Content-only packages are usually cross-platform; executable packages are not assumed to be. |
| PK-15 | **Package dependency ≠ capability dependency** ([I-326](01-normative-glossary-and-invariants.md#rule-i-326)). Capability requirements are preferred because they are more portable; a package dependency binds to a specific package. |
| PK-16 | **No npm-style transitive dependency tree.** An executable package is self-contained as far as practical, with its runtime dependencies bundled at publish time. **Dependency hell must not appear on a user's machine.** |
| PK-17 | **Dependency cycles are rejected at validation.** |
| PK-18 | **A package must not execute arbitrary scripts at install time.** Installation is performed by the ArcForges installer under its own control. |
| PK-19 | Where a system dependency is genuinely required, it is declared and surfaced to the user, never silently installed. |
| <a id="rule-pk-20"></a>PK-20 | **Executable packages carry an SBOM**, signature and integrity metadata, verified before installation. The community package supply chain follows the same discipline as ArcForges' own release pipeline. |
| PK-21 | **Package licence is declared** and surfaced. Community packages are not required to be open source, but their licence must be stated. |
| PK-22 | **A package security contact is required** for executable packages. |

### 9.1 Package lifecycle

| Stage | Rules |
|---|---|
| **Discover** | From a catalog source |
| **Install** | Manifest read, integrity verified, trust evaluated, declared permission surface shown. **Install ≠ Enable** ([I-303](01-normative-glossary-and-invariants.md#rule-i-303)), **Install ≠ permission grant** ([I-304](01-normative-glossary-and-invariants.md#rule-i-304)) |
| **Enable** | Contributions become active |
| **Grant** | Permissions granted just-in-time or explicitly consented at install |
| **Update** | Never silent for a permission-expanding update; running Tasks freeze the version they started with |
| **Disable** | Stops execution, **keeps data and configuration** |
| **Uninstall** | Removes the package; asks about extension private data; **never cascades into professional resources** |
| **Revoke** | Blocks execution platform-wide; **never deletes user data** |

| # | Requirement |
|---|---|
| LC-01 | **A running Task freezes the package version it started with.** An update mid-task does not change the executing snapshot. |
| LC-02 | **Side-by-side versions are not supported.** One installed version per package per installation scope. |
| LC-03 | **Package rollback is a binary rollback, not a data rollback** ([I-208](01-normative-glossary-and-invariants.md#rule-i-208)). Extension private data carries its own `SchemaVersion` and its own migration story. |
| LC-04 | **A running extension cannot be uninstalled outright.** It is stopped or drained first. |
| <a id="rule-lc-05"></a>LC-05 | **Uninstall does not delete resources the extension created in professional products.** A document created through an extension remains an ArcNotes document. |
| <a id="rule-lc-06"></a>LC-06 | **A missing or revoked contribution degrades gracefully.** An ArcSlate project referencing a revoked effect still opens, states clearly what is unavailable, and preserves the state so it can be restored if the package returns. |
| <a id="rule-lc-07"></a>LC-07 | **Unknown package data is preserved, not executed.** Data for a contribution that is not currently installed is retained and clearly marked, never silently trusted or discarded. |
| LC-08 | **Package provenance flows into tasks and artifacts.** An artifact produced through a community workflow records which package and version produced it; the owning resource's owner is unchanged. |

---

## 10. Community Catalog

**Community Catalog = a package discovery and distribution catalog.**

| # | Requirement |
|---|---|
| CA-01 | **Catalog ≠ Marketplace** ([I-323](01-normative-glossary-and-invariants.md#rule-i-323)). It is not a paid marketplace in this baseline. |
| CA-02 | **Catalog ≠ runtime dependency** ([I-324](01-normative-glossary-and-invariants.md#rule-i-324)). Local products keep working with the catalog unreachable; installed non-AI native capabilities remain available offline; Cloud AI never falls back to local execution. |
| CA-03 | Three catalog source classes are supported: the **official** catalog, a **self-hosted** catalog, and **local/sideload**. |
| CA-04 | **A self-hosted realm must not be locked to the official catalog.** |
| CA-05 | A catalog package page shows: identity, publisher, trust state, review status, category, contributions, **declared permission surface**, compatibility, platform targets, licence, version history and security contact. |
| CA-06 | **Permissions are visible before installation** ([UX-02](07-security-privacy-and-trust.md#rule-ux-02)). |
| CA-07 | **Trust, review status and permission are three separate axes** ([I-305](01-normative-glossary-and-invariants.md#rule-i-305), [I-247](01-normative-glossary-and-invariants.md#rule-i-247), [I-248](01-normative-glossary-and-invariants.md#rule-i-248)). A signature proves origin, a review status describes process, neither implies safety, and none of them grants permission. |
| CA-08 | **Community packages are never automatically trusted** ([I-325](01-normative-glossary-and-invariants.md#rule-i-325)). |
| <a id="rule-ca-09"></a>CA-09 | **A recommendation never installs anything automatically** and never becomes advertising pressure. |
| CA-10 | **An agent must never auto-install or auto-trust a community package.** |
| CA-11 | **Community ratings and reviews are not runtime authority.** |
| CA-12 | A **realm or owner workspace policy** may restrict which catalogs, publishers, categories or trust levels are permitted (see [`11-policy-and-configuration.md`](11-policy-and-configuration.md)). |
| <a id="rule-ca-13"></a>CA-13 | **Package revocation reaches installed users** as an actionable Needs Attention state, coordinated with the security-advisory process, and never deletes user work. |

---

## 11. Public SDK and CLI

### 11.1 SDK boundary

| # | Requirement |
|---|---|
| SD-01 | **An internal interface does not automatically become SDK.** The public SDK is a deliberate, separately versioned, long-term-compatibility surface. |
| SD-02 | **Public SDK contract ≠ internal LocalRpc contract** ([I-327](01-normative-glossary-and-invariants.md#rule-i-327)). |
| SD-03 | The SDK lives in the **Apache-2.0 interoperability boundary** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**), together with public wire schemas, public DTOs, public clients and contract-level validators. |
| SD-04 | **SDK Foundation contains only genuinely stable types**: identity primitives, result and error primitives, `ResourceRef`, `ArtifactRef`, `TaskHandle`, capability descriptors, the structured value model and the schema attributes. |
| SD-05 | **The SDK major version is separate from the extension protocol version** ([PK-05](#rule-pk-05)). |
| SD-06 | **The extension protocol itself is versioned**, and the host supports a compatibility window across protocol versions. |
| SD-07 | **A source generator produces the mechanical protocol surface** — schema, serializer, client and server binding — from C# records and attributes. Developers do not maintain three parallel schema definitions. |
| SD-08 | **The manifest has a language-independent canonical representation** (a static document), but **the manifest schema is generated and validated from the SDK model** rather than maintained twice by hand. |
| SD-09 | **C# is the first-class SDK language.** Other languages may integrate through the documented wire protocol and manifest; the best developer experience is C#. |

### 11.2 CLI

The official CLI is part of the developer platform, not a side tool. Its long-term command surface includes at minimum:

| Command | Purpose |
|---|---|
| `new` | Scaffold a package from a template for a chosen contribution kind |
| `dev` | Run a package against a development host with hot iteration; the host itself remains an AOT product |
| `validate` | Validate the manifest, schema, declared permissions, compatibility, dependency graph and, for executables, the supply-chain requirements |
| `pack` | Produce an immutable package artifact |
| `publish` | Push to a catalog through the publish pipeline |
| `sign` | Sign a package |
| `test` | Run conformance tests against the extension test host |

| # | Requirement |
|---|---|
| CL-01 | **`validate` is a gate, not advice.** A package failing validation cannot be packed or published. |
| CL-02 | **Extension validation additionally checks** the declared permission surface against the actual contribution set, forbidden constructs at the boundary, background-execution declarations, and platform target consistency. |
| CL-03 | **A first-party C# extension runs through the same public SDK path**, and does not reference ArcForges internal assemblies. This keeps the public contract honest by making it the only route. |

### 11.3 Developer experience

| # | Requirement |
|---|---|
| DX-01 | **Developer Mode** exists, is user- or administrator-enabled only (never enabled by a package), is clearly visible in the interface, and permits running a local unsigned package. |
| DX-02 | **Developer Mode does not bypass permission, secret rules or workspace policy** ([I-271](01-normative-glossary-and-invariants.md#rule-i-271)). Its trust level is *lower*, not higher. |
| DX-03 | A **lightweight extension test host** is provided for fast iteration, and **integration tests must still run against the real product** — an ArcSlate contribution is tested in ArcSlate. |
| DX-04 | A **compatibility test matrix** is published: available host versions and contract fixtures a developer can test against. |
| DX-05 | **Certification is not compatibility** and neither is trust. A certified package may still be incompatible with a given host version. |
| DX-06 | Sample packages and a conformance test suite are published as part of the platform. |
| DX-07 | Developer documentation covers the contribution model, the security model, the schema model, the manifest, the lifecycle, the publish pipeline and the compatibility policy. |

---

## 12. Placement rules

| # | Requirement |
|---|---|
| <a id="rule-pl-01"></a>PL-01 | **Mobile and web never load executable extensions.** No community executable plug-in is loaded into the mobile or web client. |
| PL-02 | **Content packages may sync across devices** (skills, templates, workflows); executable packages are re-obtained and installed per platform. |
| PL-03 | **Cloud connector execution runs cloud-side** and **runs no third-party binaries** in the ArcForges cloud host by default; where a cloud-side extension ever exists it is isolated to the same standard as a cloud task ([RX-07](03-cloud-services-and-sync.md#rule-rx-07)). |
| PL-04 | **Extension installation scope and connection scope are separate.** Installation is per device; a connection may be per workspace. |
| PL-05 | **Package identity does not change with realm.** The same package identity is meaningful in an official and a self-hosted realm; installation and trust decisions are per realm. |
| PL-06 | **Package data scope is explicit**: which workspace's data a package may touch, honouring workspace isolation. |

---

## 13. Deliberate non-goals

| Non-goal | Reason |
|---|---|
| A general "run script" extension mechanism | Arbitrary shell execution is a high-risk capability, not a platform primitive. If a shell capability ever exists it is an explicit, high-risk, separately authorised capability. |
| A browser-extension-style WebView platform | Very large security surface, no corresponding product need |
| Reinventing a general-purpose language package manager | NuGet resolves at development and build time; Arc packages are built artifacts |
| Reinventing container orchestration | Out of scope; isolation is achieved by process boundary and capability scoping |
| MCP as the marketplace package ABI | MCP is an integration adapter, reached through a package |
| ACP as an ArcChat domain model | ACP is an adapter |
| Extensions redefining resource ownership | An ArcSlate resource is ArcSlate-owned forever; an extension may own its **own** new resource type |

---

## 14. Extension points

Extension points are typed and versioned per product. Not every point must open in V1 — but **the extension model must be able to carry them all** without redesign.

| Product | Representative extension point families |
|---|---|
| **ArcChat** | Agent tools, skills, context providers, artifact handlers, integrations, task step kinds |
| **ArcNotes** | Block types, importers, exporters, property types, view kinds, document commands |
| **ArcScope** | Source adapters, decoders, measurement kinds, analysis kinds, exporters, visualisation kinds |
| **ArcSlate** | Effects, transitions, importers, exporters, render presets, media adapters |
| **Cross-cutting** | Commands, panels, settings pages, deep-link handlers, knowledge sources, automation triggers |

| # | Requirement |
|---|---|
| EP-01 | **Extension points are versioned independently** of the host product version. |
| EP-02 | **Official reserved capability namespaces are protected** and cannot be registered by an extension ([EX-12](#rule-ex-12)). |
| EP-03 | **Outside a known extension point**, contribution goes through the level-2 schema-described capability protocol. |
| EP-04 | **Extension-generated knowledge sources are ordinary knowledge sources** subject to the current four-dimension policy model — declaring one does not mean AI indexes everything behind it. |
| <a id="rule-ep-05"></a>EP-05 | **Connector events feed ordinary automation triggers**, with mandatory throttling, `EventId` deduplication and causation, because a high-rate external event stream must not create a task storm ([LP-04](05-ai-and-agent-execution.md#rule-lp-04)). |
| <a id="rule-ep-06"></a>EP-06 | **Capability resolution must be deterministic** when several providers offer the same capability: an explicit preference, then a documented rule — never a random pick. |
| EP-07 | **A package cannot expand its permission through a dependency**. Authority belongs to the actual executor and is evaluated per invocation. |

---

## 15. Domain model

```
PackageId · PackageVersion · PublisherId · ArcPackage · PackageManifest
PackageCategory · PackageContribution · PackageDependency · CapabilityRequirement
PackageCompatibility · PlatformTarget · PackageSignature · PackageIntegrity
PackageTrust · PackageReviewStatus
PackageInstallation · PackageEnablement · PackageUpdate
SkillDefinition · SkillVersion
TemplateDefinition · TemplateParameter
WorkflowDefinition · WorkflowVersion · WorkflowStepTemplate
IntegrationDefinition · IntegrationInstance
McpIntegration · McpConnection
ConnectorDefinition · ConnectorConnection · ConnectorSyncState
ExtensionDefinition · ExtensionInstance · ExtensionHostSession
ExtensionCapabilityDescriptor · ExtensionSchema · StructuredExtensionValue
ExtensionPoint · ExtensionPointVersion
ThirdPartyAppDescriptor
CatalogSource · CatalogPackageEntry · CatalogVersionEntry
DeveloperMode
```

---

## 16. Unified surfaces

| Surface | Contents |
|---|---|
| **Integrations** | MCP connections and connectors in one management surface, with unified status: configured, connected, degraded, failing, unauthorised, revoked |
| **Library** | Skills, templates and workflows as first-class reusable objects — not buried in settings |
| **Extensions** | Installed packages, trust state, permissions, health, updates |

**Extension search is not knowledge search**. Finding a package is a catalog operation; finding user content is knowledge search. They are never the same box.

---

## 17. Acceptance scenarios

**Skill** — a community skill guides the agent, grants nothing, and its update does not alter completed run results.

**Skill permission** — a skill referencing a capability the user has not granted causes the ordinary permission prompt, not silent execution.

**Template** — materialisation creates an independent resource through the owner's capability; a later template change leaves it untouched.

**Workflow** — running a workflow creates an ordinary Task; a workflow update does not change a running Task; a community workflow's step is refused for lack of permission.

**Automation** — an automation referencing a workflow re-authorises at every trigger.

**MCP** — a tool maps to a capability with declared risk; a description attempting to instruct the agent has no effect; a tool-set change re-enters permission review.

**Connector** — a definition supports several connections; a secret is stored only by reference; a live query is distinguished from an import.

**Excluded executor** — packages, MCP connections and connectors cannot register an external-agent/ACP mode, start a sub-agent or bypass Cloud AI billing; ordinary bounded tools remain usable.

**Out-of-process extension** — an extension crash leaves the owning product running; the extension is restarted on demand; the affected capability shows a clear degraded state.

**Native extension** — third-party native code runs only in the extension process; no third-party assembly is loaded into the AOT host.

**AOT** — a non-AOT extension runs successfully against an AOT host, and the host's AOT publish remains clean.

**Schema code-first** — a C# record plus attributes produces schema, serializer and bindings; an attempt to pass an arbitrary CLR object across the boundary fails at compile time or validation.

**Package** — an immutable published version; a yank removes it from discovery without stopping installed use; a revoke stops execution without deleting user data.

**Permission expansion** — an update adding a permission or background execution requires explicit re-consent.

**Update during task** — an update mid-task leaves the running Task on its frozen version.

**Uninstall** — configuration and extension private data are handled explicitly; professional resources created through the extension survive.

**Missing contribution** — a project referencing an unavailable effect opens, explains, and preserves the state for later restoration.

**Catalog** — offline operation continues; a self-hosted catalog is usable; realm/owner policy restricts sources.

**Revocation** — an installed revoked package surfaces Needs Attention and stops executing.

**Self-host** — package identity is stable across realms; installation and trust are per realm.

**Third-party app** — participates through the contribution model; cannot claim a reserved official identity.

**Knowledge** — an extension-declared knowledge source obeys the full knowledge policy model rather than becoming implicitly AI-indexed.

**Automation event** — a high-rate connector event stream is throttled and deduplicated, and does not create a task storm.

**Workspace isolation** — a package cannot reach a workspace outside its declared data scope.

**Developer** — developer mode is visible, cannot be enabled by a package, and does not bypass permission.

**Publish** — validation gates packing; a published version cannot be overwritten; the SBOM and signature are present for executables.

---

## 18. Traceability

| Current document | Relationship |
|---|---|
| [Extension Platform Architecture](../architecture/15-extension-platform-architecture.md) | Implements contribution, package, extension, SDK and CLI requirements |
| [Content and Extension Isolation](../architecture/24-content-and-extension-isolation.md) | Defines the executable extension isolation profiles |
| [Security, Permission, Privacy and Trust Requirements](07-security-privacy-and-trust.md) | Owns permission, trust, lease and egress constraints |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | The AOT host constraint that makes out-of-process extensions structural rather than stylistic |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Public SDK contracts split by boundary, ownership and licence |
| **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | The public SDK surface sits inside the Apache-2.0 interoperability boundary |
| **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** | MCP `2026-07-28` stable status, statelessness, extension-framework vocabulary collision and the SDK version-pin gate |
