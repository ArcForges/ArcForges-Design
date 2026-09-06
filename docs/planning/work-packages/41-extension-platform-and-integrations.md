# WP-41 — Extension Platform and Integrations

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `09`, `11`, `17` · Downstream: `50`

> **Goal.** Open the platform without weakening it: out-of-process extensions contributing **tools, never planners** (`EA-08`), the dual capability boundary with a closed AOT-safe value model, declarative UI contribution, the Arc Package runtime, the catalog, and the MCP, connector and external-agent integrations — all under the same security pipeline as first-party code.

---

## 1. Scope and purpose

**In scope.** The extension host and its supervision; the handshake and protocol versioning; the typed extension-point layer and the schema-described dynamic layer; declarative panel and settings contribution; the Arc Package model and lifecycle; the catalog client; the public SDK and CLI; and the integration kinds — MCP, connectors and external agents.

**Out of scope.** A paid marketplace, explicitly not in V1. A general WebView platform, explicitly a non-goal.

**Why this package exists.** The tension between a strongly typed AOT product and unknown third-party capability is the platform's hardest design problem. It is resolved architecturally, and this package is where the resolution is built and proven.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/15-extension-platform-architecture.md`](../../architecture/15-extension-platform-architecture.md) | The complete extension architecture |
| [`../../requirements/08-extensions-and-developer-platform.md`](../../requirements/08-extensions-and-developer-platform.md) | The layered model, package rules, catalog and SDK boundary |
| **V-02** | MCP SDK pin and the vocabulary mapping gate |
| `WP-09`, `WP-11`, `WP-17` output | The capability model, the security pipeline and the capability hub |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Third-party executable extensions run out-of-process by default.** No third-party assembly loads into a product's main process. |
| BR-02 | **An extension's own implementation need not be AOT**; the host stays AOT. |
| BR-03 | **Isolation is not authorization** (`I-259`); every extension call passes the full security pipeline with owner-side validation last. |
| BR-04 | **The structured value model is closed and AOT-safe.** `Dictionary<string, object>` is not the protocol (`I-328`). |
| BR-05 | **The schema-described boundary never propagates inward** (`I-329`) into first-party product capabilities. |
| BR-06 | **No third-party control is instantiated in a product process.** UI contribution is declarative from a closed vocabulary. |
| BR-07 | **A secret settings field yields a reference only**; plaintext is never stored or returned. |
| BR-08 | **Installation is not authorization.** Permissions are presented before installation and granted explicitly; a new permission in an update forces re-consent. |
| BR-09 | **Yank, deprecate and revoke are three different operations** (`I-433`, `I-330`). |
| BR-10 | **A running task freezes the package version it started with.** |
| BR-11 | **Uninstall never cascade-deletes professional resources the extension created.** |
| BR-12 | **MCP is an external capability adapter and never becomes the internal protocol** (**V-02**). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Extensions/ArcForges.Extensions.Contracts/` | The extension protocol, value model and schema definitions |
| `src/Extensions/ArcForges.Extensions.Runtime/` | Host manager, supervision, handshake, validation, declarative UI rendering |
| `src/Extensions/ArcForges.Extensions.Registry/` | Contribution registration, compatibility resolution, catalog client |
| `src/Extensions/ArcForges.Extensions.Packaging/` | Package format, integrity, install, update, disable, uninstall |
| `src/SDK/ArcForges.SDK.*`, `src/SDK/ArcForges.Cli/` | Public SDK, source generators, testing helpers and the CLI |
| `src/ArcChat/ArcChat.McpClient/` | MCP integration with the vocabulary mapping |
| `tests/McpAotTests/`, `tests/ExtensionPlatformTests/` | Conformance, isolation, security, lifecycle and catalog suites |

**Major types introduced.** `ExtensionHost`, `ExtensionProcess`, `Handshake`, `ProtocolVersion`, `StructuredValue`, `ValueSchema`, `SchemaValidator`, `PanelDeclaration`, `SettingsSchema`, `ArcPackage`, `PackageManifest`, `PackageInstallation`, `PackageState`, `CatalogClient`, `TrustLevel`, `ReviewStatus`, `McpAdapter`, `ConnectorDefinition`, `ConnectionInstance`, `ExternalAgentAdapter`.

---

## 5. Required implementation work

### WP-41.00 — Extension host and supervision

**What must be fully done.** Per-installation extension processes started on demand and stopped when idle, with resource limits enforced by termination, backoff restart, quarantine after repeated crashes, and typed failure for in-flight invocations. No ambient credential is inherited.

**Testing requirements.** Crash, hang, memory exhaustion and unbounded output tests; quarantine behaviour; a credential-absence assertion.

**Completion gate.** Every hostile process behaviour leaves the host healthy with a typed failure, and no ambient credential is inherited.

### WP-41.01 — Handshake and protocol versioning

**What must be fully done.** Identity verification against the installed manifest before any contribution is invoked; protocol version negotiation supporting more than one version during a migration window; refusal that is clean and explained. A process cannot claim another package's identity or a reserved namespace.

**Testing requirements.** Impersonation and reserved-namespace negative tests; a version negotiation matrix including refusal.

**Completion gate.** Impersonation and reserved-namespace claims are refused, and version mismatch produces a clean explanation.

### WP-41.02 — The dual capability boundary

**What must be fully done.** The typed extension-point layer as ordinary versioned contracts, and the dynamic layer over the closed structured value model with schema validation in both directions. A repository policy test asserts the structured value type never appears in a first-party domain or product contract.

**Testing requirements.** Value-model coverage per type; bidirectional validation tests; the containment policy test with a negative fixture; an AOT publish with the platform present.

**Completion gate.** Both layers work, validation is bidirectional, **the value model provably never leaks inward**, and the host still publishes AOT cleanly.

### WP-41.03 — Declarative UI contribution

**What must be fully done.** Panel declarations from a closed, versioned element vocabulary rendered with first-party controls; declarative settings schemas; secret fields yielding references only; visible attribution of extension-contributed surfaces.

**Testing requirements.** Vocabulary coverage; a negative test asserting raw markup or script is rejected; a secret-field test; an attribution test.

**Completion gate.** No third-party control is instantiated, raw markup is rejected, and secret fields never yield plaintext.

### WP-41.04 — Package runtime

**What must be fully done.** Integrity verification, manifest parsing before any code runs, compatibility resolution, permission presentation and grant, install, enable, update with re-consent, disable, uninstall with a private-data prompt, rollback, yank, deprecate and revoke. Installation never executes package-provided scripts.

**Testing requirements.** Full lifecycle matrix; a re-consent test on new permissions; an uninstall test asserting professional resources survive; a revoke test reaching an installed client.

**Completion gate.** The full lifecycle works, new permissions force re-consent, uninstall never cascade-deletes professional resources, and revoke reaches an installed client.

### WP-41.05 — Catalog

**What must be fully done.** A catalog client supporting the official catalog, additional configured catalogs and local sources. Catalog content is untrusted: sanitised for display and never treated as instructions. The package page shows contributions, permissions, publisher, trust, review status, version history, compatibility and provenance before install.

**Testing requirements.** Hostile listing content; oversized metadata; malformed manifest; a catalog-unreachable test asserting installed packages keep working.

**Completion gate.** Hostile catalog content is rejected without executing anything, and catalog unavailability never disables installed packages.

### WP-41.06 — Public SDK and CLI

**What must be fully done.** The Apache-2.0 public SDK with source generators producing schema, codec and binding from C# records. The CLI with scaffold, development host, validate, pack and publish. `validate` runs the same checks the host runs at install. A first-party extension is built through the public SDK to prove the path.

**Testing requirements.** Generator output tests; a validate-parity test against host install checks; a first-party-extension build through the public path.

**Completion gate.** The SDK generates all protocol code, `validate` matches host install checks, and a first-party extension is built through the public SDK.

### WP-41.07 — MCP, connectors and external agents

**What must be fully done.** MCP as an external capability adapter with the SDK version pinned and an explicit mapping between MCP extension concepts and the ArcForges execution vocabulary. Connectors with definition and connection instance separated and secrets held as references. External agents mapped onto the unified Task model with a capability lease per delegation, and their hidden reasoning excluded from the product model.

**Testing requirements.** MCP tool and resource mapping tests; a vocabulary-mapping record; connector secret-handling tests; an external-agent lease expiry test; a hidden-reasoning exclusion assertion.

**Completion gate.** MCP terms are explicitly mapped and the SDK version pinned — **satisfying `VG-02`** — connectors never store plaintext secrets, and external agent work maps onto ArcForges Tasks with leases.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Package installations, grants and extension private state |
| Protocol | The extension protocol and its independent version axis |
| UI | Declarative panels, settings, catalog and permission surfaces |
| Security | The largest new attack surface, contained by the pipeline and the boundary |
| Platform | Extension process behaviour per platform |
| Migration | Extension private state schema versioning |
| Compatibility | Contribution-level compatibility rather than suite lockstep |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Hostile-process behaviour and credential-absence results | `WP-41.00` |
| Impersonation, namespace and negotiation results | `WP-41.01` |
| Value-model, validation, containment and AOT results | `WP-41.02` |
| Vocabulary, markup-rejection, secret and attribution results | `WP-41.03` |
| Lifecycle matrix, re-consent, uninstall and revoke results | `WP-41.04` |
| Hostile catalog and unreachable-catalog results | `WP-41.05` |
| Generator, validate-parity and first-party build results | `WP-41.06` |
| MCP mapping record, connector secret and lease results | `WP-41.07` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Every hostile extension-process behaviour leaves the host healthy with a typed failure; no ambient credential is inherited.
2. Impersonation and reserved-namespace claims are refused; version mismatch produces a clean explanation.
3. Both capability layers work with bidirectional validation; **the structured value model provably never appears in a first-party domain or contract**; the host still publishes AOT with zero diagnostics.
4. No third-party control is instantiated; raw markup is rejected; secret fields never yield plaintext.
5. The full package lifecycle works; new permissions force re-consent; uninstall never cascade-deletes professional resources; revoke reaches installed clients.
6. Hostile catalog content is rejected without executing anything; catalog unavailability never disables installed packages.
7. The SDK generates all protocol code; `validate` matches host install checks; a first-party extension is built through the public SDK.
8. **MCP concepts are explicitly mapped to the ArcForges vocabulary with the SDK version pinned** — satisfying `VG-02`; connectors hold secrets only as references; external agent work maps onto Tasks with leases.
9. The extension protocol conformance suite passes — satisfying `PG-09`.

---

## 9. Dependencies

**Upstream.** `09` (capability model), `11` (security), `17` (the capability hub).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `50` — Production release | The extension platform as a shippable capability |
