<a id="rule-wp-41"></a>

# WP-41 — Extension Platform and Integrations

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Open the platform without weakening it: out-of-process extensions contributing **tools, never planners** ([EA-08](../../requirements/08-extensions-and-developer-platform.md#rule-ea-08)), the dual capability boundary with a closed AOT-safe value model, declarative UI contribution, the Arc Package runtime, the catalog, and the MCP, connector and artifact handoff and standard MCP integrations — all under the same security pipeline as first-party code.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Contracts public SDK/CLI; Platform host; ArcChat MCP; Cloud catalog. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The extension host and its supervision; the handshake and protocol versioning; the typed extension-point layer and the schema-described dynamic layer; declarative panel and settings contribution; the Arc Package model and lifecycle; the catalog client; the public SDK and CLI; and the integration kinds — MCP and connectors; external-agent delegation is excluded.

**Out of scope.** A paid marketplace, explicitly not in V1. A general WebView platform, explicitly a non-goal.

**Why this package exists.** The tension between a strongly typed AOT product and unknown third-party capability is the platform's hardest design problem. It is resolved architecturally, and this package is where the resolution is built and proven.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/15-extension-platform-architecture.md`](../../architecture/15-extension-platform-architecture.md) | The complete extension architecture |
| [`../../requirements/08-extensions-and-developer-platform.md`](../../requirements/08-extensions-and-developer-platform.md) | The layered model, package rules, catalog and SDK boundary |
| **[V-02](../../assurance/phase-1-official-verification.md#rule-v-02)** | MCP SDK pin and the vocabulary mapping gate |
| [WP-09](09-capability-contribution-and-resource-model.md#rule-wp-09), [WP-11](11-security-foundation.md#rule-wp-11), [WP-17](17-arcchat-independent-core.md#rule-wp-17) output | The capability model, the security pipeline and the capability hub |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Third-party executable extensions run out-of-process by default.** No third-party assembly loads into a product's main process. |
| <a id="rule-br-02"></a>BR-02 | **An extension's own implementation need not be AOT**; the host stays AOT. |
| <a id="rule-br-03"></a>BR-03 | **Isolation is not authorization** ([I-259](../../requirements/01-normative-glossary-and-invariants.md#rule-i-259)); every extension call passes the full security pipeline with owner-side validation last. |
| <a id="rule-br-04"></a>BR-04 | **The structured value model is closed and AOT-safe.** `Dictionary<string, object>` is not the protocol ([I-328](../../requirements/01-normative-glossary-and-invariants.md#rule-i-328)). |
| <a id="rule-br-05"></a>BR-05 | **The schema-described boundary never propagates inward** ([I-329](../../requirements/01-normative-glossary-and-invariants.md#rule-i-329)) into first-party product capabilities. |
| <a id="rule-br-06"></a>BR-06 | **No third-party control is instantiated in a product process.** UI contribution is declarative from a closed vocabulary. |
| <a id="rule-br-07"></a>BR-07 | **A secret settings field yields a reference only**; plaintext is never stored or returned. |
| <a id="rule-br-08"></a>BR-08 | **Installation is not authorization.** Permissions are presented before installation and granted explicitly; a new permission in an update forces re-consent. |
| <a id="rule-br-09"></a>BR-09 | **Yank, deprecate and revoke are three different operations** ([I-433](../../requirements/01-normative-glossary-and-invariants.md#rule-i-433), [I-330](../../requirements/01-normative-glossary-and-invariants.md#rule-i-330)). |
| <a id="rule-br-10"></a>BR-10 | **A running task freezes the package version it started with.** |
| <a id="rule-br-11"></a>BR-11 | **Uninstall never cascade-deletes professional resources the extension created.** |
| <a id="rule-br-12"></a>BR-12 | **MCP is an external capability adapter and never becomes the internal protocol** (**[V-02](../../assurance/phase-1-official-verification.md#rule-v-02)**). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Extensions/ArcForges.Extensions.Contracts/` | The extension protocol, value model and schema definitions |
| `src/Extensions/ArcForges.Extensions.Runtime/` | Host manager, supervision, handshake, validation, declarative UI rendering |
| `src/Extensions/ArcForges.Extensions.Registry/` | Contribution registration, compatibility resolution, catalog client |
| `src/Extensions/ArcForges.Extensions.Packaging/` | Package format, integrity, install, update, disable, uninstall |
| `src/SDK/ArcForges.SDK.*`, `src/SDK/ArcForges.Cli/` | Public SDK, source generators, testing helpers and the CLI |
| `DesktopPlatform/src/Communication/` + owning app integration | Parent-bound extension/connector and standardized MCP adapters; exact packages and bounded credentials |
| `tests/McpAotTests/`, `tests/ExtensionPlatformTests/` | Conformance, isolation, security, lifecycle and catalog suites |

**Major types introduced.** `ExtensionHost`, `ExtensionProcess`, `Handshake`, `ProtocolVersion`, `StructuredValue`, `ValueSchema`, `SchemaValidator`, `PanelDeclaration`, `SettingsSchema`, `ArcPackage`, `PackageManifest`, `PackageInstallation`, `PackageState`, `CatalogClient`, `TrustLevel`, `ReviewStatus`, `McpAdapter`, `ConnectorDefinition`, `ConnectionInstance`.

---

## 5. Required implementation work

<a id="rule-wp-41.00"></a>

### WP-41.00 — Extension host and supervision

**What must be fully done.** Enforce the package-specific OS profile from Content and Extension Isolation; broker grants do not protect against direct system calls by an unrestricted child.  Per-installation extension processes started on demand and stopped when idle, with resource limits enforced by termination, backoff restart, quarantine after repeated crashes, and typed failure for in-flight invocations. No ambient credential is inherited.

**Testing requirements.** Run a malicious package against product DB/token paths, network, sibling package and process APIs; revoke permission during an invocation and test unsupported profiles.  Crash, hang, memory exhaustion and unbounded output tests; quarantine behaviour; a credential-absence assertion.

**Completion gate.** [PG-22](../../assurance/open-gates-register.md#rule-pg-22) requires actual packaged-RID isolation; no same-user full-trust fallback is accepted.  Every hostile process behaviour leaves the host healthy with a typed failure, and no ambient credential is inherited.

<a id="rule-wp-41.01"></a>

### WP-41.01 — Handshake and protocol versioning

**What must be fully done.** Identity verification against the installed manifest before any contribution is invoked; protocol version negotiation supporting more than one version during a migration window; refusal that is clean and explained. A process cannot claim another package's identity or a reserved namespace.

**Testing requirements.** Impersonation and reserved-namespace negative tests; a version negotiation matrix including refusal.

**Completion gate.** Impersonation and reserved-namespace claims are refused, and version mismatch produces a clean explanation.

<a id="rule-wp-41.02"></a>

### WP-41.02 — The dual capability boundary

**What must be fully done.** The typed extension-point layer as ordinary versioned contracts, and the dynamic layer over the closed structured value model with schema validation in both directions. A repository policy test asserts the structured value type never appears in a first-party domain or product contract.

**Testing requirements.** Value-model coverage per type; bidirectional validation tests; the containment policy test with a negative fixture; an AOT publish with the platform present.

**Completion gate.** Both layers work, validation is bidirectional, **the value model provably never leaks inward**, and the host still publishes AOT cleanly.

<a id="rule-wp-41.03"></a>

### WP-41.03 — Declarative UI contribution

**What must be fully done.** Panel declarations from a closed, versioned element vocabulary rendered with first-party controls; declarative settings schemas; secret fields yielding references only; visible attribution of extension-contributed surfaces.

**Testing requirements.** Vocabulary coverage; a negative test asserting raw markup or script is rejected; a secret-field test; an attribution test.

**Completion gate.** No third-party control is instantiated, raw markup is rejected, and secret fields never yield plaintext.

<a id="rule-wp-41.04"></a>

### WP-41.04 — Package runtime

**What must be fully done.** Implement manifest.v1/workflow.v1/panel.v1 validators from published Contracts, all six families and immutable staged install/update/drain/migration/revocation/rollback states in annex 08.

**Testing requirements.** Archive traversal/size/signature, DAG bounds, increased permissions, active old job, private-state rollback incompatibility and unknown-effect tests.

**Completion gate.** No second autonomous planner, arbitrary UI/code eval, or update that resets effect fences.

<a id="rule-wp-41.05"></a>

### WP-41.05 — PackageCatalog producer and consumers

**What must be fully done.** Build Cloud PackageCatalog, DNS publisher verification, immutable submissions, review-state/revocation authority and signed static index producer, plus desktop/CLI consumers under arch 15/registry 04/model 01. Use WP03 fixture keys; production distribution keys are later WP53.

**Testing requirements.** Owner/PAT/operator separation, duplicate version conflict, invalid archive, review/revoke replay, signed-index rollback/expiry and offline installed-package behavior.

**Completion gate.** Real Cloud producer and package consumer integrate; WP45 can build review UI against existing methods, with no unowned catalog service.

<a id="rule-wp-41.06"></a>

### WP-41.06 — Public SDK and CLI

**What must be fully done.** Generate SDK/validators/tool payload projections from authored public proto. CLI uses eligible publisher PAT and catalog/resource methods. Third-party apps use approved public APIs or OS/file interchange.

**Testing requirements.** Independent SDK consumer, manifest/tag compatibility, PAT scopes and no generated schema inferred from C# reflection.

**Completion gate.** CLI publish submits for review and never uploads directly into public catalog visibility.

<a id="rule-wp-41.07"></a>

### WP-41.07 — MCP placement and connectors

**What must be fully done.** Implement local MCP stdio behind the owned connector child and Cloud MCP HTTP through the AI Worker adapter. Preserve MCP standard protocol; only the owned child boundary speaks ArcForges gRPC.

**Testing requirements.** Origin/scope changes invalidate consent, no browser/Android local subprocess, no unrestricted AI fetch, child crash/lease recovery.

**Completion gate.** Each MCP connection has one placement/secret owner and exact failure/egress behavior.

<a id="rule-wp-41.90"></a>
### WP-41.90 — Verify the owned artifact and real integration

**What must be fully done.** Split SDK/protocol, desktop host/runtime and Cloud registry ownership. Preserve standard MCP transports and out-of-process extensions. Remove the old external-agent integration wording rather than expanding accepted scope.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** SDK licence/protocol compatibility, capability checks, hostile-extension/process isolation and owner execution; no external-agent delegation or in-process third-party plugin.

**Completion gate.** SDK licence/protocol compatibility, capability checks, hostile-extension/process isolation and owner execution; no external-agent delegation or in-process third-party plugin. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**PackageCatalog ownership.** Cloud catalog tables, publication and review/revocation handlers live in `src/Modules/PackageCatalog/PackageCatalog.{Domain,Application,Infrastructure}`. OperatorService authenticates the operator and calls this owner; neither the Extensions implementation nor the console writes its tables. Verify owner references against the 21-module schema map.

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

Acceptance includes every amended §5 producer/consumer and [WP-41.90](#rule-wp-41.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

[Local gRPC closure](../../architecture/contracts/09-local-grpc-and-sandbox.md): Run real extension host↔child generated gRPC roles and ConnectorBroker consent/secret rotation/revocation; deny forged first-party identity and direct SSO/control access. No custom symmetric-event protocol.

| Evidence | Produced by |
|---|---|
| Hostile-process behaviour and credential-absence results | [WP-41.00](#rule-wp-41.00) |
| Impersonation, namespace and negotiation results | [WP-41.01](#rule-wp-41.01) |
| Value-model, validation, containment and AOT results | [WP-41.02](#rule-wp-41.02) |
| Vocabulary, markup-rejection, secret and attribution results | [WP-41.03](#rule-wp-41.03) |
| Lifecycle matrix, re-consent, uninstall and revoke results | [WP-41.04](#rule-wp-41.04) |
| Hostile catalog and unreachable-catalog results | [WP-41.05](#rule-wp-41.05) |
| Generator, validate-parity and first-party build results | [WP-41.06](#rule-wp-41.06) |
| MCP mapping record, connector secret and no-delegation structural results | [WP-41.07](#rule-wp-41.07) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-41.90](#rule-wp-41.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-41.90](#rule-wp-41.90) and all inherited domain-specific gates must pass on the same candidate closure. SDK licence/protocol compatibility, capability checks, hostile-extension/process isolation and owner execution; no external-agent delegation or in-process third-party plugin.

**[PG-22](../../assurance/open-gates-register.md#rule-pg-22) evidence:** [WP-41.00](#rule-wp-41.00) — Executable-extension OS profile denies store/credential/network/process escape and cleans up after parent death; combine with the platform broker proof. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Identity boundary evidence.** Apply the [owner/deployment identity chain](../../architecture/08-security-architecture.md#1-identity-layering). Automation loses authorization when its owner loses permission/service eligibility even with a valid process credential; no customer service-principal or Organization authority is introduced.

**All of the following, with recorded evidence:**

1. Every hostile extension-process behaviour leaves the host healthy with a typed failure; no ambient credential is inherited.
2. Impersonation and reserved-namespace claims are refused; version mismatch produces a clean explanation.
3. Both capability layers work with bidirectional validation; **the structured value model provably never appears in a first-party domain or contract**; the host still publishes AOT with zero diagnostics.
4. No third-party control is instantiated; raw markup is rejected; secret fields never yield plaintext.
5. The full package lifecycle works; new permissions force re-consent; uninstall never cascade-deletes professional resources; revoke reaches installed clients.
6. Hostile catalog content is rejected without executing anything; catalog unavailability never disables installed packages.
7. The SDK generates all protocol code; `validate` matches host install checks; a first-party extension is built through the public SDK.
8. **MCP concepts are explicitly mapped to the ArcForges vocabulary with the SDK version pinned** — satisfying [VG-02](../../assurance/open-gates-register.md#rule-vg-02); **no external-agent delegation path exists**; connectors hold secrets only as references.
9. The extension protocol conformance suite passes — satisfying [PG-09](../../assurance/open-gates-register.md#rule-pg-09).

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [EXT.00](../delivery/lanes/extensions.md#task-ext-00) | [WP-41.00](41-extension-platform-and-integrations.md#rule-wp-41.00) (full) | [PLT.45](../delivery/lanes/platform.md#task-plt-45) (artifact), [PLT.19](../delivery/lanes/platform.md#task-plt-19) (contract) |
| [EXT.01](../delivery/lanes/extensions.md#task-ext-01) | [WP-41.01](41-extension-platform-and-integrations.md#rule-wp-41.01) (full) | none |
| [EXT.02](../delivery/lanes/extensions.md#task-ext-02) | [WP-41.02](41-extension-platform-and-integrations.md#rule-wp-41.02) (full) | [CON.05](../delivery/lanes/contracts.md#task-con-05) (contract) |
| [EXT.03](../delivery/lanes/extensions.md#task-ext-03) | [WP-41.03](41-extension-platform-and-integrations.md#rule-wp-41.03) (full) | none |
| [EXT.04](../delivery/lanes/extensions.md#task-ext-04) | [WP-41.04](41-extension-platform-and-integrations.md#rule-wp-41.04) (manifest.v1/workflow.v1/panel.v1 validators and the immutable staged install/update/drain/migration/revocation/rollback state machine) | [CON.16](../delivery/lanes/contracts.md#task-con-16) (artifact) |
| [EXT.05](../delivery/lanes/extensions.md#task-ext-05) | [WP-41.04](41-extension-platform-and-integrations.md#rule-wp-41.04) (the six package contribution kinds (skill/template/workflow/mcp/connector/extension) runtime registration and execution wiring) | none |
| [EXT.06](../delivery/lanes/extensions.md#task-ext-06) | [WP-41.05](41-extension-platform-and-integrations.md#rule-wp-41.05) (Cloud PackageCatalog producer: DNS publisher verification, immutable submissions, review-state/revocation authority, signed static index)<br>[WP-41](41-extension-platform-and-integrations.md#rule-wp-41) PackageCatalog ownership paragraph (Sec.5-6 boundary): OperatorService is sole authenticator/caller; neither Extensions Runtime nor console writes PackageCatalog tables (package-level obligation contribution) | [CLOUD.16](../delivery/lanes/cloud.md#task-cloud-16) (artifact), [CLOUD.42](../delivery/lanes/cloud.md#task-cloud-42) (artifact), [CON.16](../delivery/lanes/contracts.md#task-con-16) (artifact) |
| [EXT.07](../delivery/lanes/extensions.md#task-ext-07) | [WP-41.05](41-extension-platform-and-integrations.md#rule-wp-41.05) (desktop/CLI catalog consumers) | none |
| [EXT.08](../delivery/lanes/extensions.md#task-ext-08) | [WP-41.06](41-extension-platform-and-integrations.md#rule-wp-41.06) (full)<br>[WP-41](41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 8: MCP vocabulary mapping + SDK version pin -- [VG-02](../../assurance/open-gates-register.md#rule-vg-02) (package-level obligation contribution) | [CLOUD.16](../delivery/lanes/cloud.md#task-cloud-16) (artifact) |
| [EXT.09](../delivery/lanes/extensions.md#task-ext-09) | [WP-41.07](41-extension-platform-and-integrations.md#rule-wp-41.07) (local MCP stdio placement behind the owned connector child process)<br>[WP-41](41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 8: MCP vocabulary mapping + SDK version pin -- [VG-02](../../assurance/open-gates-register.md#rule-vg-02) (package-level obligation contribution) | none |
| [EXT.10](../delivery/lanes/extensions.md#task-ext-10) | [WP-41.07](41-extension-platform-and-integrations.md#rule-wp-41.07) (Cloud MCP HTTP placement through the AI Worker adapter)<br>[WP-41](41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 8: MCP vocabulary mapping + SDK version pin -- [VG-02](../../assurance/open-gates-register.md#rule-vg-02) (package-level obligation contribution) | [CON.15](../delivery/lanes/contracts.md#task-con-15) (contract) |
| [EXT.90](../delivery/lanes/extensions.md#task-ext-90) | [WP-41.90](41-extension-platform-and-integrations.md#rule-wp-41.90) (full)<br>[WP-41](41-extension-platform-and-integrations.md#rule-wp-41) Sec.8 gate item 9: extension protocol conformance suite -- [PG-09](../../assurance/open-gates-register.md#rule-pg-09) (package-level obligation contribution) | none |

**Consumers outside this package:** [OPS.11](../delivery/lanes/operations.md#task-ops-11), [REL.06](../delivery/lanes/release.md#task-rel-06), [SCOPE.25](../delivery/lanes/arcscope.md#task-scope-25).

<!-- delivery-graph:end -->

