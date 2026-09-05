# Extension Platform Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **D-008** (the host stays Native AOT), **D-009** (contract granularity), **D-004**/**D-021** (public SDK licence boundary), `I4 §Stage 24`
> Companions: [`../requirements/08-extensions-and-developer-platform.md`](../requirements/08-extensions-and-developer-platform.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`08-security-architecture.md`](08-security-architecture.md), [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md)

The extension platform exists to resolve one tension: **ArcForges ships a strongly typed, Native AOT product, and must still host capabilities nobody anticipated.** The resolution is architectural, not a compromise on either side — a process boundary, and a dual capability boundary above it.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| EA-01 | **Third-party executable extensions run out-of-process by default** (`EX-01` in the extension requirements; `I4 §Stage 24 §53`). |
| EA-02 | **No third-party assembly is loaded into a product's main process at runtime.** That would break the Native AOT main path (**D-008**) and remove the isolation boundary simultaneously (`EX-01` there). |
| EA-03 | **An extension's own implementation is not required to be Native AOT** (`EX-04` there; `I4 §Stage 24 §152`). The host stays AOT; the extension is a separate process with its own runtime. This is precisely what makes a dynamic ecosystem compatible with an AOT product. |
| EA-04 | **Isolation is not authorization** (`I-259`), and **out-of-process is not automatically safe** (`I-260`). Every extension call passes the full security pipeline (`§7`). |
| EA-05 | **An extension never touches a product store.** It calls capabilities (`EX-07` there). |
| EA-06 | **An extension crash must not crash the owning application** (`EX-11` there). |
| EA-07 | **The manifest is readable and verifiable before any extension code executes** (`I4 §Stage 24 §90`). |
| EA-08 | **The schema-described boundary applies only at the dynamic third-party edge** (`DB-05` there, `I-329`). It is never back-propagated into first-party product capabilities. |

---

## 2. Component map

```
Product process (Native AOT)                     Extension process (any runtime)
┌──────────────────────────────────┐             ┌──────────────────────────────┐
│ Capability Registry              │             │ Extension entry point        │
│ Extension Point Registry (typed) │             │ SDK runtime                  │
│ Extension Host Manager           │◄──protocol─►│ Contribution implementations │
│  ├ lifecycle & supervision       │             │ Private state store          │
│  ├ handshake & negotiation       │             └──────────────────────────────┘
│  ├ permission & lease enforcement│
│  └ schema validation             │             Package Runtime
│ Declarative UI renderer          │             ┌──────────────────────────────┐
│ Structured value codec           │             │ install · verify · enable    │
└──────────────────────────────────┘             │ update · disable · uninstall │
                                                 │ integrity · provenance       │
                                                 └──────────────────────────────┘
```

| Component | Responsibility |
|---|---|
| **Extension Point Registry** | The set of typed extension points a product declares; compile-time contracts (`§4.1`) |
| **Extension Host Manager** | Starts, supervises, throttles and stops extension processes; owns the handshake and version negotiation |
| **Structured value codec** | Encodes and decodes the closed value model at the dynamic boundary (`§4.2`) |
| **Schema validator** | Validates every inbound and outbound dynamic payload against its declared schema |
| **Declarative UI renderer** | Renders panel and settings contributions from declarations; no third-party control is instantiated (`§6`) |
| **Package Runtime** | Manifest parsing, integrity verification, permission presentation, lifecycle, private-state schema versioning |
| **Catalog client** | Discovery, install source resolution, trust and review status presentation (`§9`) |

---

## 3. Process model and lifecycle

### 3.1 Supervision

| # | Rule |
|---|---|
| PR-01 | **One extension process per installed package instance**, started on demand and stopped when idle (`EX-05` there). |
| PR-02 | **Background residency must be declared in the manifest and separately consented** (`EX-06` there). Adding it in an update is a permission expansion requiring re-consent (`§8`). |
| PR-03 | **Process identity is bound to the package installation** (`EX-12` there). The host verifies it; a process cannot claim to be a different package. |
| PR-04 | **The host applies resource limits** — memory, CPU share, concurrent invocations, wall-clock per invocation — and enforces them by termination when exceeded, with a typed reason. |
| PR-05 | **A crashed extension process is restarted with backoff**, and repeated crashes quarantine the extension with a visible state rather than looping (`§8`). |
| PR-06 | **In-flight invocations of a crashed process fail with a typed, retryable-or-not classification**, never hang (`§5` of the agent runtime architecture). |
| PR-07 | **Extension processes inherit no ambient credential.** They receive no environment secret, no session token, and no filesystem handle beyond what a granted capability provides. |
| PR-08 | **Extension shutdown is graceful then forced**: a stop request, a bounded drain window, then termination. |
| PR-09 | **A running extension cannot be uninstalled directly** (`I4 §Stage 24 §141`). Stop, then uninstall. |

### 3.2 Transport

| # | Rule |
|---|---|
| TR-01 | **The extension protocol runs over the same local IPC transport as the rest of the product** — named pipe on Windows, Unix domain socket elsewhere (`§2` of the local IPC architecture). |
| TR-02 | **The channel is per process and access-controlled to the current user**; it is never a network endpoint. |
| TR-03 | **Payload size is bounded.** Large content crosses as a `ResourceRef` with controlled access (`DB-06` there, `I4 §Stage 24 §73`). |
| TR-04 | **Cancellation, timeout and backpressure are first-class protocol concerns**, not conventions. |
| TR-05 | **The host never blocks its UI thread on an extension** (`§4` of the desktop architecture). |

### 3.3 Handshake and negotiation

```
Host starts process with an installation-scoped identity token
  → Extension announces: package id, version, protocol version(s),
                          contributions it will serve
  → Host verifies identity against the installed manifest
  → Host negotiates the protocol version (§10)
  → Host resolves which contributions are usable (§10.2)
  → Ready; invocations may begin
```

| # | Rule |
|---|---|
| HS-01 | **The handshake happens before any contribution is invoked** (`I4 §Stage 24 §173`). |
| HS-02 | **An extension process cannot claim to be another package** (`I4 §Stage 24 §174`); a mismatch terminates the process. |
| HS-03 | **An extension cannot register in a reserved official capability namespace** (`I4 §Stage 24 §175`), except by implementing a known official extension point (`§176` there). |
| HS-04 | **Version negotiation failure is a clean, explained refusal**, not a crash or a silent downgrade. |
| HS-05 | **Manifest compatibility is a preflight check; the handshake is the ultimate fact** (`I4 §Stage 24 §170`). A manifest that claims compatibility does not override a failed negotiation. |

---

## 4. The dual capability boundary

### 4.1 Level 1 — typed extension points

| # | Rule |
|---|---|
| L1-01 | **A typed extension point is an ordinary versioned contract** in the contract layer (**D-009**), with generated serialization and no reflection. |
| L1-02 | **It is the default route** for anything ArcForges anticipated, and gives the best developer experience and the strongest validation. |
| L1-03 | **Extension points are product-specific and enumerated** (`§14` of the extension requirements). Not every point is opened in V1, **but the model must be able to carry them** (`I4 §Stage 24 §80`). |
| L1-04 | **An internal interface does not automatically become a public extension point** (`I4 §Stage 24 §81`). Promotion to the public SDK is a deliberate act with a compatibility commitment. |

### 4.2 Level 2 — the schema-described boundary

For capabilities ArcForges did not anticipate.

**The closed structured value model** (`DB-01` there):

```
null · boolean · integer · number · string · binary reference
date/time · ResourceRef · list<Value> · record<name, Value>
```

| # | Rule |
|---|---|
| L2-01 | **The value model is closed and AOT-safe.** No arbitrary CLR object, no runtime `Type`, no assembly-qualified type name, no native pointer crosses the boundary (`DB-02` there). |
| L2-02 | **`Dictionary<string, object>` is not the extension protocol** (`I-328`). Every dynamic payload is described by a schema and validated against it. |
| L2-03 | **The host requires no knowledge of third-party CLR types** (`DB-04` there). This is what makes the boundary AOT-safe: the host manipulates values, never foreign types. |
| L2-04 | **Every dynamic payload is validated in both directions** — inbound to the host and outbound to the extension — before it reaches any product logic (`EX-13` there). |
| L2-05 | **Validation failure is a typed protocol error** attributed to the extension, never a host exception. |
| L2-06 | **The schema exception never leaks inward** (`DB-05` there, `I-329`). ArcNotes, ArcScope and ArcSlate native capabilities stay compile-time typed. A repository policy test asserts that the structured value type does not appear in a first-party domain or product contract. |
| L2-07 | **Numeric, temporal and text semantics are specified exactly** — integer width, decimal precision, time zone handling, normalisation and length limits — so two implementations agree. |
| L2-08 | **Unknown fields are rejected by default**, with an explicit forward-compatible mode where the schema declares it. |

### 4.3 Code-first for C# authors

| # | Rule |
|---|---|
| CF-01 | **Developers write C# records with attributes**; a source generator produces the schema, the codec and the client and server binding (`DB-03` there, `I4 §Stage 24 §86`). |
| CF-02 | **Developers never hand-maintain three schemas** (`I4 §Stage 24 §87`). The C# model is the source; manifest schema and wire schema are generated and verified from it (`§89` there). |
| CF-03 | **The manifest still has a language-independent canonical representation** (`I4 §Stage 24 §88`), so non-C# authors and the host tooling are not excluded. |
| CF-04 | **Generated artifacts are verified in CI against the committed baseline**, exactly as product contracts are (`§2.2` of the build architecture). |

---

## 5. Contribution kinds and their runtime treatment

| Contribution | Executes code | Runtime treatment |
|---|---|---|
| **Skill** | No | Declarative agent guidance; versioned; resolved by the agent runtime; confers no capability (`§1` of the extension requirements) |
| **Template** | No | Materialised through the owning product's capability, never written directly into a product store (`§2` there) |
| **Workflow** | No | A blueprint compiled into Plan and Step objects of the unified execution model; never a second agent runtime (`§3` there) |
| **MCP integration** | Out of process | An external capability adapter; MCP terms are disambiguated per **V-02** and never become the internal protocol (`§5` there) |
| **Connector** | Out of process | Definition and connection instance separated; secrets held as `SecretRef` only (`§6` there) |
| **External agent** | Out of process | Delegated work mapped onto the unified Task model with a capability lease per delegation (`§7` there) |
| **Extension** | **Yes** | The extension process model of `§3` |
| **Third-party Arc App** | Yes, as a peer app | Participates through the cross-application contribution model, not through the extension host (`§8.4` there) |

| # | Rule |
|---|---|
| CK-01 | **A content contribution never executes code**, and the runtime must make that structurally true — a skill, template or workflow package has no executable entry point. |
| CK-02 | **A workflow's steps are limited to the declared step semantics.** No scripting language is introduced (`I4 §Stage 24 §22`), and unbounded looping is not a workflow capability (`§23` there). |
| CK-03 | **A community-provided contribution obtains no implicit permission** (`I4 §Stage 24 §25`). |
| CK-04 | **A running task freezes the package version it started with** (`I4 §Stage 24 §133`); an update does not change a running execution. |
| CK-05 | **Package provenance enters the task and artifact records** (`I4 §Stage 24 §164`), and resource provenance is retained (`§165` there). |

---

## 6. UI contribution architecture

| # | Rule |
|---|---|
| UI-01 | **No third-party Avalonia control is instantiated in a product process** (`UI-01` there, `I4 §Stage 24 §75`). |
| UI-02 | **Panel contributions use a declarative panel protocol**: the extension sends a declaration tree from a closed element vocabulary; the host renders it with first-party controls and product theming. |
| UI-03 | **The element vocabulary is closed and versioned**, with no raw markup, no styling escape hatch and no script. |
| UI-04 | **Interaction is a message, not a callback into host internals.** A user action produces a typed event delivered to the extension process. |
| UI-05 | **Settings UI is generated from a declarative settings schema** (`UI-02` there, `I4 §Stage 24 §77`). |
| UI-06 | **A secret settings field yields a `SecretRef` only** (`UI-04` there, `I4 §Stage 24 §78`); plaintext is never stored in extension configuration and never returned to the extension. |
| UI-07 | **Complex third-party interfaces belong in a standalone third-party Arc App** (`UI-03` there), not embedded in a first-party process. |
| UI-08 | **No general browser-extension or WebView platform is built** (`UI-05` there). |
| UI-09 | **Extension-contributed UI is visibly attributed** to its package, so a user always knows whose surface they are looking at. |

---

## 7. Security enforcement

| # | Rule |
|---|---|
| SE-01 | **Every extension invocation is an ordinary capability invocation** and passes the fourteen-step security decision pipeline (`§12` of the security requirements). |
| SE-02 | **Owner-side final validation always applies** (`§3` of the security architecture). The extension host is one enforcement point; the capability owner remains the last. |
| SE-03 | **Permissions are declared in the manifest, presented before installation, and granted explicitly** (`I4 §Stage 24 §121`, `§122`). Installation is not authorization. |
| SE-04 | **A delegation to an extension creates a capability lease** — scoped, expiring, revocable, and audited (`§10` of the security requirements). |
| SE-05 | **Input to an extension is minimised to the current call** (`EX-14` there). There is no full-access object. |
| SE-06 | **Extension output is untrusted input.** It is schema-validated (`L2-04`), and any instruction-like content it carries is marked with untrusted provenance for the agent runtime (`§8` of the security architecture). |
| SE-07 | **Trust, permission, signature and review status are four separate things** (`I4 §Stage 24 §123`–`§126`): trust is a level, permission is a grant, a signature proves origin not safety, and review status is an independent assertion. |
| SE-08 | **Egress by an extension is a separate authorization** (`§7` of the security requirements). Holding a read capability never implies permission to send data out. |
| SE-09 | **Extension invocations appear in the ordinary task trace and audit** (`EX-15` there), never in a separate plug-in log. |
| SE-10 | **Package analytics and extension telemetry are separate, declared and consented** (`EX-16` there); nothing is reported to a publisher automatically. |
| SE-11 | **Developer Mode is user- or administrator-enabled only, never by a package** (`I4 §Stage 24 §145`), is clearly visible while active (`§144`), and does not bypass permission (`§146`). |

---

## 8. Package runtime

### 8.1 Install and verify

```
Acquire (.arcpkg from catalog, URL or local file)
 → verify integrity: hash, signature, publisher identity
 → parse manifest (before any code runs)
 → resolve compatibility: host version, contract set, protocol version, platform
 → present permissions and contributions to the user
 → user grants
 → install into a per-installation directory with private state initialised
 → enable
```

| # | Rule |
|---|---|
| PM-01 | **Integrity is verified before installation** (`I4 §Stage 24 §127`), and an executable package should carry an SBOM (`§129` there). Community packages follow the same supply-chain discipline as ArcForges' own artifacts (`§128` there). |
| PM-02 | **Installation never executes an arbitrary script** (`I4 §Stage 24 §158`). Installation is performed by the ArcForges installer, not by package-provided code. |
| PM-03 | **A published package version is immutable** (`I4 §Stage 24 §102`); files of the same version are never overwritten. |
| PM-04 | **Local sideload requires no cloud account** (`I4 §Stage 24 §98`); publishing to the official catalog requires a verified publisher account (`§99` there). |
| PM-05 | **Executable packages are as self-contained as practical** (`I4 §Stage 24 §111`, `§112`). Runtime dependencies are packaged at release so dependency resolution never happens on a user machine; no npm-style transitive dependency tree exists. |
| PM-06 | **Arc Package dependencies express logical package relationships only**, and a dependency cycle fails validation (`I4 §Stage 24 §113`, `§114`). |
| PM-07 | **System dependencies are declared, detected and reported** — never silently installed by the package (`I4 §Stage 24 §159`). |

### 8.2 Update, disable, uninstall

| # | Rule |
|---|---|
| PU-01 | **Automatic update is never silent** (`I4 §Stage 24 §130`). |
| PU-02 | **A new permission requirement forces re-consent** (`I4 §Stage 24 §131`), and adding background execution is a permission expansion (`§132` there). |
| PU-03 | **Side-by-side versions do not run** (`I4 §Stage 24 §134`). One installed version is active. |
| PU-04 | **Rollback is binary rollback, not data rollback** (`I4 §Stage 24 §135`). Private data compatibility is governed by the extension's own `SchemaVersion` (`§136` there, `EX-08`). |
| PU-05 | **Disable and uninstall are separate** (`I4 §Stage 24 §137`). Disable retains data and configuration (`§138`). |
| PU-06 | **Uninstall asks about extension private data by default** (`I4 §Stage 24 §139`), and **never cascade-deletes professional resources the extension created** (`§140`) — those belong to the owning product forever. |
| PU-07 | **Yank, deprecate and revoke are three different operations** (`I-433`, `I-330`; `I4 §Stage 24 §103`, `§163`): yank removes from new installation and recommendation; deprecate signals a successor; revoke blocks or severely limits execution of an installed package. |
| PU-08 | **Revocation reaches installed clients** through the policy control plane's kill-switch mechanism (`§4` of the policy requirements), with a stated reason surfaced to the user. |

### 8.3 Extension private state

| # | Rule |
|---|---|
| PS-01 | **Private state lives in a per-installation store outside the product's canonical domain** (`EX-08` there). |
| PS-02 | **It carries its own `SchemaVersion`** and its own migration path. |
| PS-03 | **It is included in device backup but is never treated as product authority**, and its loss degrades the extension without damaging product data. |
| PS-04 | **It is size-bounded**, with pressure surfaced to the user rather than growing unchecked (`§14` of the data requirements). |

---

## 9. Catalog architecture

| # | Rule |
|---|---|
| CA-01 | **The community catalog is a discovery and distribution catalog, not a marketplace** (`I4 §Stage 24 §115`, `§116`). There is no paid transaction in V1. |
| CA-02 | **Three source classes are supported** (`I4 §Stage 24 §117`): the official catalog, an additional configured catalog, and a local or direct source. |
| CA-03 | **A self-hosted environment is never locked to the official catalog** (`I4 §Stage 24 §118`). |
| CA-04 | **A catalog is untrusted content.** Listing text, metadata and links are treated as data, sanitised for display, and never as instructions. |
| CA-05 | **The package page shows what matters before install** (`I4 §Stage 24 §120`, `§121`): contributions, permissions, publisher, trust level, review status, version history, compatibility and provenance. |
| CA-06 | **The catalog client does not execute anything it downloads** before the local verification pipeline of `§8.1` completes. |
| CA-07 | **Catalog availability is not a runtime dependency.** An installed package continues to work when the catalog is unreachable. |

---

## 10. Versioning and compatibility

### 10.1 The separated axes

| Axis | Governs |
|---|---|
| `PackageVersion` | The package's own release identity — **not the compatibility mechanism** (`I-301`, `I-302`) |
| `ExtensionProtocolVersion` | The host↔extension protocol itself |
| `ContractVersion` / `ContractSet` | The typed capability and extension-point contracts |
| `AppVersion` | The host product |
| Public SDK major version | The developer-facing API surface |

| # | Rule |
|---|---|
| VC-01 | **These axes are never mixed** (`I4 §Stage 24 §101`; `§14` of the quality contract). |
| VC-02 | **The extension protocol is itself versioned and supports more than one version simultaneously** during a migration window (`I4 §Stage 24 §171`). |
| VC-03 | **The public SDK major version is separate from the protocol version** (`I4 §Stage 24 §172`). |
| VC-04 | **`PackageId` never changes across versions**, and `PublisherId` is stable (`PK-03` there). |

### 10.2 Contribution-level compatibility

| # | Rule |
|---|---|
| CC-01 | **Compatibility is judged per contribution, not per suite** (`I4 §Stage 24 §167`, `§168`). A package may be partially usable: three of its four contributions work, and the fourth is reported as incompatible with a reason. |
| CC-02 | **Extension compatibility never forces the whole suite into lockstep** (`I4 §Stage 24 §167`). |
| CC-03 | **A compatibility manifest states real ranges, not a single number** (`I4 §Stage 24 §106`, `§107`), and partial compatibility is expressible. |
| CC-04 | **Platform targets are declared** (`I4 §Stage 24 §108`); content-only packages are usually cross-platform (`§109`). |
| CC-05 | **An incompatible contribution is visibly disabled with an explanation**, never silently missing. |

---

## 11. Public SDK and CLI

### 11.1 SDK

| # | Rule |
|---|---|
| SD-01 | **The public SDK is separate from internal contracts** (`I4 §Stage 24 §82`), and carries a long-term compatibility commitment that internal interfaces do not (`§83`). |
| SD-02 | **The SDK foundation holds only genuinely stable types** (`I4 §Stage 24 §85`). |
| SD-03 | **The public SDK sits on the Apache-2.0 side of the licence boundary** (**D-004**, **D-021**), together with public protocol specifications, wire schemas, DTOs, public clients and contract-level validators. |
| SD-04 | **C# is the first-class SDK language** (`I4 §Stage 24 §153`); other languages are served by the canonical manifest and protocol representations (`CF-03`). |
| SD-05 | **The SDK source generator produces mechanical protocol code only** (`I4 §Stage 24 §86`) — schema, codec, binding — never business behaviour. |
| SD-06 | **An official first-party extension uses the public SDK**, not internal assemblies (`I4 §Stage 24 §156`), so the public path is proven by first-party use. |

### 11.2 CLI

The `arcforge` CLI is part of the developer platform (`I4 §Stage 24 §148`, `§149`).

| Command | Responsibility |
|---|---|
| `new` | Scaffold a package from a template (`I4 §Stage 24 §150`) |
| `dev` | Run against a development host; the production host itself remains an AOT product (`§151` there) |
| `validate` | Manifest, schema, permission declaration and executable-package checks (`§154`, `§155` there) |
| `pack` | Produce an immutable package artifact (`§157` there) |
| `publish` | Submit to a catalog through the publish pipeline (`§160`, `§161` there) |

| # | Rule |
|---|---|
| CL-01 | **`validate` runs the same checks the host runs at install time**, so a developer discovers a failure locally rather than at publication. |
| CL-02 | **`pack` output is immutable and content-addressed**, and the same artifact is what publishes. |
| CL-03 | **The CLI never requires a cloud account for local development.** |

---

## 12. Testing and gates

| # | Test obligation |
|---|---|
| XT-01 | **Protocol conformance suite**: a reference extension exercising every contribution kind, every value-model type, and every error path. |
| XT-02 | **Version negotiation matrix**: host and extension at differing protocol versions produce the specified outcome — negotiated, partially usable, or cleanly refused. |
| XT-03 | **Isolation tests**: extension crash, hang, memory exhaustion, and infinite output each leave the host healthy with a typed failure (`EA-06`, `PR-04`–`PR-06`). |
| XT-04 | **Security tests**: an extension attempting to exceed its grant, impersonate another package, claim a reserved namespace, read a secret, or egress data is refused and audited. |
| XT-05 | **Schema-containment test**: the structured value type does not appear in any first-party domain or product contract (`L2-06`), enforced as a repository policy test. |
| XT-06 | **AOT test**: the host publishes AOT with the extension platform present, and no reflection-based path is required (`EA-03`). |
| XT-07 | **Package lifecycle tests**: install, permission grant, update with new permissions, disable, enable, rollback, uninstall with and without private-data deletion, and revoke reaching an installed client. |
| XT-08 | **Provenance tests**: a task and artifact produced through a community package carry that package's provenance (`CK-05`). |
| XT-09 | **Catalog-as-untrusted tests**: hostile listing content, oversized metadata and malformed manifests are rejected without executing anything. |
| XT-10 | **Compatibility tests**: partial contribution availability is reported correctly and does not disable the whole package (`CC-01`). |

---

## 13. Non-goals

The extension platform is **not**: an in-process plug-in system; a scripting language; a general WebView or browser-extension host; a paid marketplace in V1; a route by which third-party code reaches a product database; a second agent runtime; a reason to weaken the host's AOT posture; or a mechanism through which a dynamic value model spreads into first-party contracts.

---

## 14. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 24 §1`–`§185` | The layered developer-platform model, the out-of-process security decision, the dual capability boundary and closed value model, UI contribution limits, the Arc Package model and lifecycle, catalog positioning and trust layering, versioning separation, contribution-level compatibility, handshake rules, and the SDK and CLI structure |
| `I4 §Stage 21` | The contribution model third-party Arc Apps participate in |
| `I3 §8` | Capabilities as semantic interfaces, and agents as non-superusers |
| **D-008** | The host remains Native AOT; the extension does not have to be |
| **D-009** | Extension points and capability contracts as versioned contracts |
| **D-004**, **D-021** | The public SDK on the Apache boundary |
| **V-02** | MCP term disambiguation wherever MCP appears in this platform |
