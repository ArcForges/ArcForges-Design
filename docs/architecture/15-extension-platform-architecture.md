# Extension Platform Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (the host stays Native AOT), **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (public SDK licence boundary), [extension requirements](../requirements/08-extensions-and-developer-platform.md)
> Companions: [`../requirements/08-extensions-and-developer-platform.md`](../requirements/08-extensions-and-developer-platform.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`08-security-architecture.md`](08-security-architecture.md), [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md)

The extension platform exists to resolve one tension: **ArcForges ships a strongly typed, Native AOT product, and must still host capabilities nobody anticipated.** The resolution is architectural, not a compromise on either side — a process boundary, and a dual capability boundary above it.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-ea-01"></a>EA-01 | **Third-party executable extensions run out-of-process by default** ([EX-01](../requirements/08-extensions-and-developer-platform.md#rule-ex-01) in the extension requirements). |
| <a id="rule-ea-02"></a>EA-02 | **No third-party assembly is loaded into a product's main process at runtime.** That would break the Native AOT main path (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) and remove the isolation boundary simultaneously ([EX-01](../requirements/08-extensions-and-developer-platform.md#rule-ex-01) there). |
| <a id="rule-ea-03"></a>EA-03 | **An extension's own implementation is not required to be Native AOT** ([EX-04](../requirements/08-extensions-and-developer-platform.md#rule-ex-04) there). The host stays AOT; the extension is a separate process with its own runtime. This is precisely what makes a dynamic ecosystem compatible with an AOT product. |
| <a id="rule-ea-04"></a>EA-04 | **Isolation is not authorization** ([I-259](../requirements/01-normative-glossary-and-invariants.md#rule-i-259)), and **out-of-process is not automatically safe** ([I-260](../requirements/01-normative-glossary-and-invariants.md#rule-i-260)). Every extension call passes the full security pipeline (`§7`). |
| <a id="rule-ea-05"></a>EA-05 | **An extension never touches a product store.** It calls capabilities ([EX-07](../requirements/08-extensions-and-developer-platform.md#rule-ex-07) there). |
| <a id="rule-ea-06"></a>EA-06 | **An extension crash must not crash the owning application** ([EX-11](../requirements/08-extensions-and-developer-platform.md#rule-ex-11) there). |
| <a id="rule-ea-07"></a>EA-07 | **The manifest is readable and verifiable before any extension code executes**. |
| <a id="rule-ea-08"></a>EA-08 | **The schema-described boundary applies only at the dynamic third-party edge** ([DB-05](../requirements/08-extensions-and-developer-platform.md#rule-db-05) there, [I-329](../requirements/01-normative-glossary-and-invariants.md#rule-i-329)). It is never back-propagated into first-party product capabilities. |

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
| <a id="rule-pr-01"></a>PR-01 | **One extension process per installed package instance**, started on demand and stopped when idle ([EX-05](../requirements/08-extensions-and-developer-platform.md#rule-ex-05) there). |
| <a id="rule-pr-02"></a>PR-02 | **Background residency must be declared in the manifest and separately consented** ([EX-06](../requirements/08-extensions-and-developer-platform.md#rule-ex-06) there). Adding it in an update is a permission expansion requiring re-consent (`§8`). |
| <a id="rule-pr-03"></a>PR-03 | **Process identity is bound to the package installation** ([EX-12](../requirements/08-extensions-and-developer-platform.md#rule-ex-12) there). The host verifies it; a process cannot claim to be a different package. |
| <a id="rule-pr-04"></a>PR-04 | **The host applies resource limits** — memory, CPU share, concurrent invocations, wall-clock per invocation — and enforces them by termination when exceeded, with a typed reason. |
| <a id="rule-pr-05"></a>PR-05 | **A crashed extension process is restarted with backoff**, and repeated crashes quarantine the extension with a visible state rather than looping (`§8`). |
| <a id="rule-pr-06"></a>PR-06 | **In-flight invocations of a crashed process fail with a typed, retryable-or-not classification**, never hang (`§5` of the agent runtime architecture). |
| <a id="rule-pr-07"></a>PR-07 | **Extension processes inherit no ambient credential.** They receive no environment secret, no session token, and no filesystem handle beyond what a granted capability provides. |
| <a id="rule-pr-08"></a>PR-08 | **Extension shutdown is graceful then forced**: a stop request, a bounded drain window, then termination. |
| <a id="rule-pr-09"></a>PR-09 | **A running extension cannot be uninstalled directly**. Stop, then uninstall. |
| <a id="rule-pr-10"></a>PR-10 | The [OS-enforced isolation profiles](24-content-and-extension-isolation.md) deny direct product-store, credential and ungranted network access. Same-user process separation plus an RPC grant check is insufficient. A missing profile refuses execution with `security.isolation_unavailable`; it never runs the extension in ambient full trust. |

### 3.2 Transport

| # | Rule |
|---|---|
| <a id="rule-tr-01"></a>TR-01 | **The extension protocol is authored proto and native gRPC over the same OS IPC as the rest of the product** — named pipe on Windows, Unix domain socket elsewhere (`§2` of the local IPC architecture). |
| <a id="rule-tr-02"></a>TR-02 | **The channel is per process and access-controlled to the current user**; it is never a network endpoint. |
| <a id="rule-tr-03"></a>TR-03 | **Payload size is bounded.** Large content crosses as a `ResourceRef` with controlled access ([DB-06](../requirements/08-extensions-and-developer-platform.md#rule-db-06) there). |
| <a id="rule-tr-04"></a>TR-04 | **Cancellation, timeout and backpressure are first-class protocol concerns**, not conventions. |
| <a id="rule-tr-05"></a>TR-05 | **The host never blocks its UI thread on an extension** (`§4` of the desktop architecture). |

[Local profile 09](contracts/09-local-grpc-and-sandbox.md) fixes both receiver directions, launch-bound credentials, generated services and restricted-stream hosting. Host Handshake/RenewLease and bidirectional Invoke/Stop roles never use an untyped symmetric channel.

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
| <a id="rule-hs-01"></a>HS-01 | **The handshake happens before any contribution is invoked**. |
| <a id="rule-hs-02"></a>HS-02 | **An extension process cannot claim to be another package**; a mismatch terminates the process. |
| <a id="rule-hs-03"></a>HS-03 | **An extension cannot register in a reserved official capability namespace**, except by implementing a known official extension point. |
| <a id="rule-hs-04"></a>HS-04 | **Version negotiation failure is a clean, explained refusal**, not a crash or a silent downgrade. |
| <a id="rule-hs-05"></a>HS-05 | **Manifest compatibility is a preflight check; the handshake is the ultimate fact**. A manifest that claims compatibility does not override a failed negotiation. |

---

## 4. The dual capability boundary

### 4.1 Level 1 — typed extension points

| # | Rule |
|---|---|
| <a id="rule-l1-01"></a>L1-01 | **A typed extension point is an ordinary versioned contract** in the contract layer (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**), with generated serialization and no reflection. |
| <a id="rule-l1-02"></a>L1-02 | **It is the default route** for anything ArcForges anticipated, and gives the best developer experience and the strongest validation. |
| <a id="rule-l1-03"></a>L1-03 | **Extension points are product-specific and enumerated** (`§14` of the extension requirements). Not every point is opened in V1, **but the model must be able to carry them**. |
| <a id="rule-l1-04"></a>L1-04 | **An internal interface does not automatically become a public extension point**. Promotion to the public SDK is a deliberate act with a compatibility commitment. |

### 4.2 Level 2 — the schema-described boundary

For capabilities ArcForges did not anticipate.

**The closed structured value model** ([DB-01](../requirements/08-extensions-and-developer-platform.md#rule-db-01) there):

```
null · boolean · integer · number · string · binary reference
date/time · ResourceRef · list<Value> · record<name, Value>
```

| # | Rule |
|---|---|
| <a id="rule-l2-01"></a>L2-01 | **The value model is closed and AOT-safe.** No arbitrary CLR object, no runtime `Type`, no assembly-qualified type name, no native pointer crosses the boundary ([DB-02](../requirements/08-extensions-and-developer-platform.md#rule-db-02) there). |
| <a id="rule-l2-02"></a>L2-02 | **`Dictionary<string, object>` is not the extension protocol** ([I-328](../requirements/01-normative-glossary-and-invariants.md#rule-i-328)). Every dynamic payload is described by a schema and validated against it. |
| <a id="rule-l2-03"></a>L2-03 | **The host requires no knowledge of third-party CLR types** ([DB-04](../requirements/08-extensions-and-developer-platform.md#rule-db-04) there). This is what makes the boundary AOT-safe: the host manipulates values, never foreign types. |
| <a id="rule-l2-04"></a>L2-04 | **Every dynamic payload is validated in both directions** — inbound to the host and outbound to the extension — before it reaches any product logic ([EX-13](../requirements/08-extensions-and-developer-platform.md#rule-ex-13) there). |
| <a id="rule-l2-05"></a>L2-05 | **Validation failure is a typed protocol error** attributed to the extension, never a host exception. |
| <a id="rule-l2-06"></a>L2-06 | **The schema exception never leaks inward** ([DB-05](../requirements/08-extensions-and-developer-platform.md#rule-db-05) there, [I-329](../requirements/01-normative-glossary-and-invariants.md#rule-i-329)). ArcNotes, ArcScope and ArcSlate native capabilities stay compile-time typed. A repository policy test asserts that the structured value type does not appear in a first-party domain or product contract. |
| <a id="rule-l2-09"></a>L2-09 | **Inward means past the decode step.** The boundary receives a structured value and immediately converts it to a generated typed request (`§3.1` of the local RPC contract); everything after that point is compile-time typed. The exception is a doorway, not a corridor. |
| <a id="rule-l2-07"></a>L2-07 | **Numeric, temporal and text semantics are specified exactly** — integer width, decimal precision, time zone handling, normalisation and length limits — so two implementations agree. |
| <a id="rule-l2-08"></a>L2-08 | **Unknown fields are rejected by default**, with an explicit forward-compatible mode where the schema declares it. |

### 4.3 Code-first for C# authors

| # | Rule |
|---|---|
| <a id="rule-cf-01"></a>CF-01 | C# attributed records feed only the declared extension parameter/settings schema and codec described by CF-02. Public service envelopes and method bindings are generated from authored Contracts proto. |
| <a id="rule-cf-02"></a>CF-02 | C# extension authors may generate their declared parameter/settings schema and codec from attributed records. The enclosing public extension service/messages remain the handwritten proto authority; this convenience never generates first-party business wire contracts from C#. |
| <a id="rule-cf-03"></a>CF-03 | **The manifest still has a language-independent canonical representation**, so non-C# authors and the host tooling are not excluded. |
| <a id="rule-cf-04"></a>CF-04 | **Generated artifacts are verified in CI against the committed baseline**, exactly as product contracts are (`§2.2` of the build architecture). |

---

## 5. Contribution kinds and their runtime treatment

| Contribution | Executes code | Runtime treatment |
|---|---|---|
| **Skill** | No | Declarative agent guidance; versioned; resolved by the agent runtime; confers no capability (`§1` of the extension requirements) |
| **Template** | No | Materialised through the owning product's capability, never written directly into a product store (`§2` there) |
| **Workflow** | No | A blueprint compiled into Plan and Step objects of the unified execution model; never a second agent runtime (`§3` there) |
| **MCP integration** | Out of process | An external capability adapter; MCP terms are disambiguated per **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** and never become the internal protocol (`§5` there) |
| **Connector** | Out of process | Definition and connection instance separated; secrets held as `SecretRef` only (`§6` there) |
| ~~External agent~~ | — | **Retired by P2-006.** External-agent providers, ACP adapters, session mapping, delegation leases and result adapters are excluded ([EA-01](../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-06](../requirements/08-extensions-and-developer-platform.md#rule-ea-06) of the extension requirements). **There is no external-agent contribution kind**, and a package, connector or MCP tool cannot start an autonomous delegated agent ([EA-08](../requirements/08-extensions-and-developer-platform.md#rule-ea-08) there). An integration contributes tools; it never contributes a planner |
| **Extension** | **Yes** | The extension process model of `§3` |
| **Third-party Arc App** | Future scope | Peer-application discovery/contribution is not registered in this release. Current third-party executable contributions use the admitted extension host and its permissions. |

| # | Rule |
|---|---|
| <a id="rule-ck-01"></a>CK-01 | **A content contribution never executes code**, and the runtime must make that structurally true — a skill, template or workflow package has no executable entry point. |
| <a id="rule-ck-02"></a>CK-02 | **A workflow's steps are limited to the declared step semantics.** No scripting language is introduced, and unbounded looping is not a workflow capability. |
| <a id="rule-ck-03"></a>CK-03 | **A community-provided contribution obtains no implicit permission**. |
| <a id="rule-ck-04"></a>CK-04 | **A running task freezes the package version it started with**; an update does not change a running execution. |
| <a id="rule-ck-05"></a>CK-05 | **Package provenance enters the task and artifact records**, and resource provenance is retained. |

---

## 6. UI contribution architecture

| # | Rule |
|---|---|
| <a id="rule-ui-01"></a>UI-01 | **No third-party Avalonia control is instantiated in a product process** ([`UI-01`](../requirements/08-extensions-and-developer-platform.md#rule-ui-01) there). |
| <a id="rule-ui-02"></a>UI-02 | **Panel contributions use a declarative panel protocol**: the extension sends a declaration tree from a closed element vocabulary; the host renders it with first-party controls and product theming. |
| <a id="rule-ui-03"></a>UI-03 | **The element vocabulary is closed and versioned**, with no raw markup, no styling escape hatch and no script. |
| <a id="rule-ui-04"></a>UI-04 | **Interaction is a message, not a callback into host internals.** A user action produces a typed event delivered to the extension process. |
| <a id="rule-ui-05"></a>UI-05 | **Settings UI is generated from a declarative settings schema** ([UI-02](../requirements/08-extensions-and-developer-platform.md#rule-ui-02) there). |
| <a id="rule-ui-06"></a>UI-06 | **A secret settings field yields a `SecretRef` only** ([UI-04](../requirements/08-extensions-and-developer-platform.md#rule-ui-04) there); plaintext is never stored in extension configuration and never returned to the extension. |
| <a id="rule-ui-07"></a>UI-07 | **Complex third-party interfaces belong in a standalone third-party Arc App** ([UI-03](../requirements/08-extensions-and-developer-platform.md#rule-ui-03) there), not embedded in a first-party process. |
| <a id="rule-ui-08"></a>UI-08 | **No general browser-extension or WebView platform is built** ([UI-05](../requirements/08-extensions-and-developer-platform.md#rule-ui-05) there). |
| <a id="rule-ui-09"></a>UI-09 | **Extension-contributed UI is visibly attributed** to its package, so a user always knows whose surface they are looking at. |

---

## 7. Security enforcement

| # | Rule |
|---|---|
| <a id="rule-se-01"></a>SE-01 | **Every extension invocation is an ordinary capability invocation** and passes the fourteen-step security decision pipeline (`§12` of the security requirements). |
| <a id="rule-se-02"></a>SE-02 | **Owner-side final validation always applies** (`§3` of the security architecture). The extension host is one enforcement point; the capability owner remains the last. |
| <a id="rule-se-03"></a>SE-03 | **Permissions are declared in the manifest, presented before installation, and granted explicitly**. Installation is not authorization. |
| <a id="rule-se-04"></a>SE-04 | **A tool invocation into an extension creates a capability lease** — scoped, expiring, revocable, and audited (`§10` of the security requirements). The lease bounds one bounded invocation; it never authorises an extension to plan or to run its own agent loop ([EA-05](../requirements/08-extensions-and-developer-platform.md#rule-ea-05), [EA-08](../requirements/08-extensions-and-developer-platform.md#rule-ea-08) there). |
| <a id="rule-se-05"></a>SE-05 | **Input to an extension is minimised to the current call** ([EX-14](../requirements/08-extensions-and-developer-platform.md#rule-ex-14) there). There is no full-access object. |
| <a id="rule-se-06"></a>SE-06 | **Extension output is untrusted input.** It is schema-validated ([L2-04](#rule-l2-04)), and any instruction-like content it carries is marked with untrusted provenance for the agent runtime (`§8` of the security architecture). |
| <a id="rule-se-07"></a>SE-07 | **Trust, permission, signature and review status are four separate things**: trust is a level, permission is a grant, a signature proves origin not safety, and review status is an independent assertion. |
| <a id="rule-se-08"></a>SE-08 | **Egress by an extension is a separate authorization** (`§7` of the security requirements). Holding a read capability never implies permission to send data out. |
| <a id="rule-se-09"></a>SE-09 | **Extension invocations appear in the ordinary task trace and audit** ([EX-15](../requirements/08-extensions-and-developer-platform.md#rule-ex-15) there), never in a separate plug-in log. |
| <a id="rule-se-10"></a>SE-10 | **Package analytics and extension telemetry are separate, declared and consented** ([EX-16](../requirements/08-extensions-and-developer-platform.md#rule-ex-16) there); nothing is reported to a publisher automatically. |
| <a id="rule-se-11"></a>SE-11 | **Developer Mode is user- or administrator-enabled only, never by a package**, is clearly visible while active, and does not bypass permission. |

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
| <a id="rule-pm-01"></a>PM-01 | **Integrity is verified before installation**, and an executable package should carry an SBOM. Community packages follow the same supply-chain discipline as ArcForges' own artifacts. |
| <a id="rule-pm-02"></a>PM-02 | **Installation never executes an arbitrary script**. Installation is performed by the ArcForges installer, not by package-provided code. |
| <a id="rule-pm-03"></a>PM-03 | **A published package version is immutable**; files of the same version are never overwritten. |
| <a id="rule-pm-04"></a>PM-04 | **Local sideload requires no cloud account**; publishing to the official catalog requires a verified publisher account. |
| <a id="rule-pm-05"></a>PM-05 | **Executable packages are as self-contained as practical**. Runtime dependencies are packaged at release so dependency resolution never happens on a user machine; no npm-style transitive dependency tree exists. |
| <a id="rule-pm-06"></a>PM-06 | **Arc Package dependencies express logical package relationships only**, and a dependency cycle fails validation. |
| <a id="rule-pm-07"></a>PM-07 | **System dependencies are declared, detected and reported** — never silently installed by the package. |

### 8.2 Update, disable, uninstall

| # | Rule |
|---|---|
| <a id="rule-pu-01"></a>PU-01 | **Automatic update is never silent**. |
| <a id="rule-pu-02"></a>PU-02 | **A new permission requirement forces re-consent**, and adding background execution is a permission expansion. |
| <a id="rule-pu-03"></a>PU-03 | **Side-by-side versions do not run**. One installed version is active. |
| <a id="rule-pu-04"></a>PU-04 | **Rollback is binary rollback, not data rollback**. Private data compatibility is governed by the extension's own `SchemaVersion` ([EX-08](../requirements/08-extensions-and-developer-platform.md#rule-ex-08)). |
| <a id="rule-pu-05"></a>PU-05 | **Disable and uninstall are separate**. Disable retains data and configuration. |
| <a id="rule-pu-06"></a>PU-06 | **Uninstall asks about extension private data by default**, and **never cascade-deletes professional resources the extension created** — those belong to the owning product forever. |
| <a id="rule-pu-07"></a>PU-07 | **Yank, deprecate and revoke are three different operations** ([I-433](../requirements/01-normative-glossary-and-invariants.md#rule-i-433), [I-330](../requirements/01-normative-glossary-and-invariants.md#rule-i-330)): yank removes from new installation and recommendation; deprecate signals a successor; revoke blocks or severely limits execution of an installed package. |
| <a id="rule-pu-08"></a>PU-08 | **Revocation reaches installed clients** through the policy control plane's kill-switch mechanism (`§4` of the policy requirements), with a stated reason surfaced to the user. |

### 8.3 Extension private state

| # | Rule |
|---|---|
| <a id="rule-ps-01"></a>PS-01 | **Private state lives in a per-installation store outside the product's canonical domain** ([EX-08](../requirements/08-extensions-and-developer-platform.md#rule-ex-08) there). |
| <a id="rule-ps-02"></a>PS-02 | **It carries its own `SchemaVersion`** and its own migration path. |
| <a id="rule-ps-03"></a>PS-03 | **It is included in device backup but is never treated as product authority**, and its loss degrades the extension without damaging product data. |
| <a id="rule-ps-04"></a>PS-04 | **It is size-bounded**, with pressure surfaced to the user rather than growing unchecked (`§14` of the data requirements). |

---

## 9. Catalog architecture

| # | Rule |
|---|---|
| <a id="rule-ca-01"></a>CA-01 | **The community catalog is a discovery and distribution catalog, not a marketplace**. There is no paid transaction in V1. |
| <a id="rule-ca-02"></a>CA-02 | **Three source classes are supported**: the official catalog, an additional configured catalog, and a local or direct source. |
| <a id="rule-ca-03"></a>CA-03 | **A self-hosted environment is never locked to the official catalog**. |
| <a id="rule-ca-04"></a>CA-04 | **A catalog is untrusted content.** Listing text, metadata and links are treated as data, sanitised for display, and never as instructions. |
| <a id="rule-ca-05"></a>CA-05 | **The package page shows what matters before install**: contributions, permissions, publisher, trust level, review status, version history, compatibility and provenance. |
| <a id="rule-ca-06"></a>CA-06 | **The catalog client does not execute anything it downloads** before the local verification pipeline of `§8.1` completes. |
| <a id="rule-ca-07"></a>CA-07 | **Catalog availability is not a runtime dependency.** An installed package continues to work when the catalog is unreachable. |

---

## 10. Versioning and compatibility

### 10.1 The separated axes

| Axis | Governs |
|---|---|
| `PackageVersion` | The package's own release identity — **not the compatibility mechanism** ([I-301](../requirements/01-normative-glossary-and-invariants.md#rule-i-301), [I-302](../requirements/01-normative-glossary-and-invariants.md#rule-i-302)) |
| `ExtensionProtocolVersion` | The host↔extension protocol itself |
| `ContractVersion` / `ContractSet` | The typed capability and extension-point contracts |
| `AppVersion` | The host product |
| Public SDK major version | The developer-facing API surface |

| # | Rule |
|---|---|
| <a id="rule-vc-01"></a>VC-01 | **These axes are never mixed** (`§14` of the quality contract). |
| <a id="rule-vc-02"></a>VC-02 | **The extension protocol is itself versioned and supports more than one version simultaneously** during a migration window. |
| <a id="rule-vc-03"></a>VC-03 | **The public SDK major version is separate from the protocol version**. |
| <a id="rule-vc-04"></a>VC-04 | **`PackageId` never changes across versions**, and `PublisherId` is stable ([PK-03](../requirements/08-extensions-and-developer-platform.md#rule-pk-03) there). |

### 10.2 Contribution-level compatibility

| # | Rule |
|---|---|
| <a id="rule-cc-01"></a>CC-01 | **Compatibility is judged per contribution, not per suite**. A package may be partially usable: three of its four contributions work, and the fourth is reported as incompatible with a reason. |
| <a id="rule-cc-02"></a>CC-02 | **Extension compatibility never forces the whole suite into lockstep**. |
| <a id="rule-cc-03"></a>CC-03 | **A compatibility manifest states real ranges, not a single number**, and partial compatibility is expressible. |
| <a id="rule-cc-04"></a>CC-04 | **Platform targets are declared**; content-only packages are usually cross-platform. |
| <a id="rule-cc-05"></a>CC-05 | **An incompatible contribution is visibly disabled with an explanation**, never silently missing. |

---

## 11. Public SDK and CLI

### 11.1 SDK

| # | Rule |
|---|---|
| <a id="rule-sd-01"></a>SD-01 | **The public SDK is separate from internal contracts**, and carries a long-term compatibility commitment that internal interfaces do not. |
| <a id="rule-sd-02"></a>SD-02 | **The SDK foundation holds only genuinely stable types**. |
| <a id="rule-sd-03"></a>SD-03 | **The public SDK sits on the Apache-2.0 side of the licence boundary** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**), together with public protocol specifications, wire schemas, DTOs, public clients and contract-level validators. |
| <a id="rule-sd-04"></a>SD-04 | **C# is the first-class SDK language**; other languages are served by the canonical manifest and protocol representations ([CF-03](#rule-cf-03)). |
| <a id="rule-sd-05"></a>SD-05 | **The SDK source generator produces mechanical protocol code only** — schema, codec, binding — never business behaviour. |
| <a id="rule-sd-06"></a>SD-06 | **An official first-party extension uses the public SDK**, not internal assemblies, so the public path is proven by first-party use. |

### 11.2 CLI

The `arcforge` CLI is part of the developer platform.

| Command | Responsibility |
|---|---|
| `new` | Scaffold a package from a template |
| `dev` | Run against a development host; the production host itself remains an AOT product |
| `validate` | Manifest, schema, permission declaration and executable-package checks |
| `pack` | Produce an immutable package artifact |
| `publish` | Submit to a catalog through the publish pipeline |

| # | Rule |
|---|---|
| <a id="rule-cl-01"></a>CL-01 | **`validate` runs the same checks the host runs at install time**, so a developer discovers a failure locally rather than at publication. |
| <a id="rule-cl-02"></a>CL-02 | **`pack` output is immutable and content-addressed**, and the same artifact is what publishes. |
| <a id="rule-cl-03"></a>CL-03 | **The CLI never requires a cloud account for local development.** |

---

## 12. Testing and gates

| # | Test obligation |
|---|---|
| <a id="rule-xt-01"></a>XT-01 | **Protocol conformance suite**: a reference extension exercising every contribution kind, every value-model type, and every error path. |
| <a id="rule-xt-02"></a>XT-02 | **Version negotiation matrix**: host and extension at differing protocol versions produce the specified outcome — negotiated, partially usable, or cleanly refused. |
| <a id="rule-xt-03"></a>XT-03 | **Isolation tests**: extension crash, hang, memory exhaustion, and infinite output each leave the host healthy with a typed failure ([EA-06](#rule-ea-06), [PR-04](#rule-pr-04)–[PR-06](#rule-pr-06)). |
| <a id="rule-xt-04"></a>XT-04 | **Security tests**: an extension attempting to exceed its grant, impersonate another package, claim a reserved namespace, read a secret, or egress data is refused and audited. |
| <a id="rule-xt-05"></a>XT-05 | **Schema-containment test**, scoped precisely: the structured value type is **absent** from every first-party domain, application and product-operation assembly, and **permitted only** in the boundary dispatch assembly that decodes it (`§3.1` of the local RPC contract, [DP-02](contracts/02-local-rpc-operations.md#rule-dp-02)). An unscoped test would fail against the boundary the design requires; a test that omitted the boundary's own assembly would let the exception leak inward. Enforced as a repository policy test. |
| <a id="rule-xt-06"></a>XT-06 | **AOT test**: the host publishes AOT with the extension platform present, and no reflection-based path is required ([EA-03](#rule-ea-03)). |
| <a id="rule-xt-07"></a>XT-07 | **Package lifecycle tests**: install, permission grant, update with new permissions, disable, enable, rollback, uninstall with and without private-data deletion, and revoke reaching an installed client. |
| <a id="rule-xt-08"></a>XT-08 | **Provenance tests**: a task and artifact produced through a community package carry that package's provenance ([CK-05](#rule-ck-05)). |
| <a id="rule-xt-09"></a>XT-09 | **Catalog-as-untrusted tests**: hostile listing content, oversized metadata and malformed manifests are rejected without executing anything. |
| <a id="rule-xt-10"></a>XT-10 | **Compatibility tests**: partial contribution availability is reported correctly and does not disable the whole package ([CC-01](#rule-cc-01)). |

---

## 13. Non-goals

The extension platform is **not**: an in-process plug-in system; a scripting language; a general WebView or browser-extension host; a paid marketplace in V1; a route by which third-party code reaches a product database; a second agent runtime; a reason to weaken the host's AOT posture; or a mechanism through which a dynamic value model spreads into first-party contracts.

---

## 14. Traceability

| Current document | Relationship |
|---|---|
| [Extensions, Integrations and Developer Platform Requirements](../requirements/08-extensions-and-developer-platform.md) | Owns contributions, package lifecycle, compatibility, SDK and CLI scope |
| [Security, Permission, Privacy and Trust Requirements](../requirements/07-security-privacy-and-trust.md) | Owns permissions, leases, trust and egress constraints |
| [Content and Extension Isolation](24-content-and-extension-isolation.md) | Defines OS-enforced executable extension boundaries |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | The host remains Native AOT; the extension does not have to be |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Extension points and capability contracts as versioned contracts |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | The public SDK on the Apache boundary |
| **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** | MCP term disambiguation wherever MCP appears in this platform |

## Selected extension protocol composition

The public IExtensionHost service, StructuredValue and typed extension message envelopes come from the Contracts proto registry. Code-first extension parameter schema generation above composes into that fixed envelope; it does not introduce a second first-party RPC protocol or expose foreign CLR types. MCP remains its explicitly accepted external standard and cannot choose the internal transport.

## Initial schemas and owner lifecycle

[Extension/policy profiles](contracts/08-extension-and-policy-profiles.md) fixes the six package contribution kinds, complete manifest, template/workflow/panel schemas, connector lifecycle and staged/drained update. Author those closed schemas in Contracts and generate validators before owner implementations. Dynamic schema generation is permitted only within the already declared extension-only argument boundary; it cannot replace handwritten business proto or invent first-party product operations. Catalog, signing, immutable package Resource hosting and existing owner/grant/policy validation are actual WP41 outputs, not a filesystem-only install demo.

## PackageCatalog producer and distribution

Cloud PackageCatalog owns the registry 04 catalog methods and model 01 publisher/package/version/review/revocation tables. WP41 implements submission/verification/scanning/review-state/index production and CLI consumer; WP45 adds operator review/revocation UI. CLI `publish` uploads immutable bytes through Resource, then calls catalog.submitVersion with a scoped publisher credential. It does not bypass review or publish directly to a public bucket.

Contracts WP03 specifies `catalog-index.v1` and `catalog-revocations.v1` as signed canonical JSON envelopes. Envelope fields: schemaVersion, realmId, channel, revision:uint64-string, issuedAt, expiresAt, keyId, bodyHash, body, signature. Ed25519 signs canonical envelope bytes excluding signature; bodyHash is SHA256 of canonical body. Index body entries contain packageId, publisherId, exact version, archiveHttpsUrl, sha256, manifestHash, minimumHostVersion and capabilitiesDigest. Revocation body entries contain packageId/version/digest, reason and revokedAt; revisions are monotonic, no removed revocation. Pagination uses immutable signed shards with count/hash in the root, max 1 MiB/shard and 1,000 entries. Clients pin realm/channel/signing trust and reject expired (max 24h), rollback or mismatched shards. Production keys use WP53 distribution custody; WP02/06 supply distinct fixture keys so WP41 is independently executable.

Serve immutable revisions and latest signed pointers at downloads.arcforges.com/catalog/v1/. Poll before new install/enable and at least every 24h when online. Known revoked code cannot launch; unreachable/expired metadata blocks new install/enable, reports attention and preserves existing data. Existing installed unrevoked packages follow their last verified admission and explicit offline policy; no network dependency is added to ordinary native editing. Self-host catalogs have separately accepted trust roots and cannot overwrite official publisher trust.

Extension RPC schemas are handwritten Contracts public proto; SDK/tool generators project descriptors, argument validation and bindings, never discover business schemas from C# reflection. Executable extensions use the parent/child gRPC profile. Local MCP stdio is behind an owned connector child; Cloud MCP uses only the AI Worker's admitted HTTP adapter. Browser/Android never run a local MCP subprocess. Third-party apps use scoped PAT APIs or explicit OS/file interchange, never undocumented product discovery or unrestricted Tool Invoke.
