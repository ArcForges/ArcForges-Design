<a id="rule-wp-09"></a>

# WP-09 — Capability, Contribution and Resource Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `03`, `08` · Downstream: `11`, `14`, `16`, `41`

> **Goal.** Implement the cross-application semantic model — App, Installation, Instance, Contribution, Capability, Action, Context, `ResourceRef`, Artifact, Deep Link, Event, Health and Invocation — so that every product, extension and agent describes and reaches every other through one vocabulary.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Contracts; Platform; products. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The capability registry and its selection pipeline; contribution registration; the six contribution kinds' registration paths; action availability; context providers and context freezing; resource and artifact reference resolution; deep links; the event model; health reporting; and the invocation pipeline with its fixed routing priority and semantic error set.

**Out of scope.** The agent runtime that consumes capabilities (`16`). Product-specific capability implementations. Extension hosting (`41`).

**Why this package exists.** Without one semantic model, each product invents its own, and every cross-product feature becomes a bespoke integration. This is also the layer where the permission model attaches, so it must exist before security enforcement is wired.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | The full semantic model, `ResourceRef` rules, invocation pipeline and routing priority |
| [`../../requirements/08-extensions-and-developer-platform.md`](../../requirements/08-extensions-and-developer-platform.md) `§14` | The extension points the model must be able to carry |
| [`../../requirements/09-shared-desktop-experience.md`](../../requirements/09-shared-desktop-experience.md) | Deep links, handoff and command semantics |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) output | The descriptor contract types |
| [WP-08](08-local-ipc-and-registration.md#rule-wp-08) output | The transport that carries invocations |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **`App ≠ Installation ≠ Instance`.** Three distinct identities with three distinct lifecycles. |
| BR-02 | **`Capability ≠ Action`.** A capability is an invocable semantic operation; an action is a user-facing offer with availability. |
| BR-03 | **`ResourceRef` floats; `ResourceVersionRef` pins.** Choosing the wrong one is a semantic defect, not a style choice. |
| BR-04 | **A resource is owned by exactly one product forever.** Ownership does not transfer with a reference. |
| BR-05 | **Context is frozen at invocation.** A capability sees the context as it was when the invocation began, never a later mutation. |
| BR-06 | **Availability is computed, not assumed.** An action unavailable for a stated reason is shown as unavailable with that reason, never silently missing. |
| BR-07 | **Routing priority is fixed** and identical on every platform (`§10` of the contract architecture). |
| BR-08 | **The semantic error set is closed**, and every invocation failure maps to it. |
| BR-09 | **Health has five dimensions** — reachable, ready, healthy, degraded, capacity — used identically locally and in the cloud. |
| BR-10 | **A capability descriptor is richer than a tool description**: it carries risk level, trust requirement, side-effect class, reversibility and approval posture. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Capabilities/` | Created: registry, selection pipeline, invocation pipeline, availability evaluation |
| `src/BuildingBlocks/ArcForges.Contributions/` | Created: contribution registration and resolution |
| `src/Contracts/Public/ArcForges.Contracts.Capability/` | Extended with any descriptor field the implementation proves necessary, via the contract change process |
| `src/*/[Product].LocalRpc/` | Each product registers its contributions through this model |
| `tests/CapabilityModelTests/` | Created: registry, selection, availability, context freezing, routing priority |

**Major types introduced.** `AppIdentity`, `InstallationIdentity`, `InstanceIdentity`, `Contribution`, `CapabilityRegistry`, `CapabilityDescriptor`, `ActionDescriptor`, `AvailabilityResult`, `ContextProvider`, `FrozenContext`, `ResourceResolver`, `ArtifactHandler`, `DeepLinkRouter`, `EventBus`, `HealthDimension`, `InvocationRequest`, `InvocationOutcome`, `SemanticError`.

---

## 5. Required implementation work

<a id="rule-wp-09.00"></a>

### WP-09.00 — App, Installation and Instance identity

**What must be fully done.** The three identities with their lifecycles: an app is a stable product identity; an installation is that app installed on a device; an instance is a running process. Registration carries all three, and routing distinguishes "the app is installed" from "an instance is running".

**Testing requirements.** Lifecycle tests covering install without run, run without registration, multiple instances of one installation, and instance death.

**Completion gate.** The three identities are distinguishable at every decision point, with a test per confusion case.

<a id="rule-wp-09.01"></a>

### WP-09.01 — Contribution registration

**What must be fully done.** The six contribution kinds register through one path with a declared kind, identity, version and owner. Registration is idempotent, survives a Hub restart, and a contribution from an unknown or unverified source is refused.

**Testing requirements.** Registration idempotency; restart recovery; refusal of an unowned or reserved namespace claim.

**Completion gate.** Registration is idempotent and refuses reserved-namespace claims.

<a id="rule-wp-09.02"></a>

### WP-09.02 — Capability registry and selection

**What must be fully done.** The registry stores descriptors with their full field set. The selection pipeline resolves a requested capability to a concrete provider using the fixed routing priority, considering availability, health, version compatibility and placement. Selection is deterministic and explainable — the pipeline can state why it chose what it chose.

**Testing requirements.** Selection tests across every priority tier; an explainability test asserting a reason is produced; a determinism test.

**Completion gate.** Selection follows the fixed priority, is deterministic, and explains itself.

<a id="rule-wp-09.03"></a>

### WP-09.03 — Actions and availability

**What must be fully done.** Actions are computed from capabilities plus current context, with availability producing a typed reason when unavailable. Availability evaluation is cheap enough to run on UI enumeration and never performs a side effect.

**Testing requirements.** Availability tests across permission, entitlement, health, context and version reasons; a purity test asserting no side effect.

**Completion gate.** Every unavailability produces a typed reason, and evaluation is side-effect free.

<a id="rule-wp-09.04"></a>

### WP-09.04 — Context providers and freezing

**What must be fully done.** Context providers contribute typed context. At invocation, the context is frozen into an immutable snapshot carried with the invocation. A later change to the live context never affects an in-flight invocation.

**Testing requirements.** A mutation-during-invocation test asserting the frozen snapshot is used; a size-bounding test asserting oversized context is refused rather than truncated silently.

**Completion gate.** Context is provably frozen and oversized context is refused explicitly.

<a id="rule-wp-09.05"></a>

### WP-09.05 — Resources and artifacts

**What must be fully done.** Resource resolution from reference to access, honouring ownership and the floating-versus-pinned distinction. Artifact handlers register per artifact kind. A reference never carries a path, pointer or handle, and resolution always re-checks permission at access time.

**Testing requirements.** Resolution tests across owner-present, owner-absent, permission-denied and version-pinned cases; a structural test that a reference cannot carry a path.

**Completion gate.** Resolution re-checks permission at access, and a reference structurally cannot carry a path.

<a id="rule-wp-09.06"></a>

### WP-09.06 — Deep links, events and health

**What must be fully done.** A deep-link router mapping canonical links to surfaces, treating every link as untrusted input carrying no secret. An event model with typed events and bounded subscription. Health reporting across the five dimensions, aggregated per contribution and per instance.

**Testing requirements.** Deep-link tests including hostile input; event delivery and unsubscribe tests; health aggregation tests including a degraded provider.

**Completion gate.** Deep links reject hostile input, events cannot leak subscriptions, and health aggregation reflects a degraded provider correctly.

<a id="rule-wp-09.07"></a>

### WP-09.07 — Invocation pipeline

**What must be fully done.** The end-to-end invocation path: resolve → check availability → freeze context → authorize → invoke → validate result → record. Failures map to the closed semantic error set. The pipeline is the only route to a capability.

**Testing requirements.** A policy test asserting no bypass route exists; error-mapping tests for every semantic error; a tracing test asserting each invocation is observable.

**Completion gate.** The pipeline is the only route, every failure maps to the closed set, and every invocation is traced.

---

<a id="rule-wp-09.90"></a>
### WP-09.90 — Verify the owned artifact and real integration

**What must be fully done.** Consume generated capability/resource/contribution contracts. Preserve typed invocation, owner semantics, resource affinity/availability, preflight/compensation and large-artifact references. Generate AI tool projections from the same definitions.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Independent descriptor/argument/result checks; owner refuses invalid/stale invocations and opaque references do not grant access. No universal untyped business invocation replaces the catalogue.

**Completion gate.** Independent descriptor/argument/result checks; owner refuses invalid/stale invocations and opaque references do not grant access. No universal untyped business invocation replaces the catalogue. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Contribution and registration state is durable across restarts |
| Protocol | Descriptors and invocation messages become live protocol |
| UI | Actions, availability reasons and health states become surfaceable |
| Security | The invocation pipeline is where authorization attaches in `11` |
| Platform | Routing priority and placement rules become platform-uniform |
| Migration | Capability version compatibility begins to matter |
| Compatibility | Contribution-level compatibility, which the extension platform later depends on |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Identity lifecycle matrix | [WP-09.00](#rule-wp-09.00) |
| Registration idempotency and namespace refusal results | [WP-09.01](#rule-wp-09.01) |
| Selection priority, determinism and explainability results | [WP-09.02](#rule-wp-09.02) |
| Availability reason matrix and purity assertion | [WP-09.03](#rule-wp-09.03) |
| Context freezing and size-bound results | [WP-09.04](#rule-wp-09.04) |
| Resource resolution matrix and structural path prohibition | [WP-09.05](#rule-wp-09.05) |
| Deep-link hostile-input, event and health results | [WP-09.06](#rule-wp-09.06) |
| Pipeline bypass-prohibition, error-mapping and tracing results | [WP-09.07](#rule-wp-09.07) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-09.90](#rule-wp-09.90) and all inherited domain-specific gates must pass on the same candidate closure. Independent descriptor/argument/result checks; owner refuses invalid/stale invocations and opaque references do not grant access. No universal untyped business invocation replaces the catalogue.

**All of the following, with recorded evidence:**

1. App, installation and instance are distinguishable at every decision point.
2. Registration is idempotent, survives restart, and refuses reserved-namespace claims.
3. Capability selection follows the fixed routing priority, is deterministic, and explains its choice.
4. Every unavailability yields a typed reason, and availability evaluation has no side effects.
5. Context is frozen at invocation and oversized context is refused explicitly.
6. Resource resolution re-checks permission at access, and a reference structurally cannot carry a path, pointer or handle.
7. The invocation pipeline is the only route to a capability, every failure maps to the closed semantic error set, and every invocation is traced.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [03 contract foundation and licence split](03-contract-foundation-and-licence-split.md#rule-wp-03)
- [08 local ipc and registration](08-local-ipc-and-registration.md#rule-wp-08)

**Downstream — consumers of these released outputs.**

- [11 security foundation](11-security-foundation.md#rule-wp-11)
- [14 hub and minimal provider slice](14-hub-and-minimal-provider-slice.md#rule-wp-14)
- [16 unified execution engine](16-unified-execution-engine.md#rule-wp-16)
- [41 extension platform and integrations](41-extension-platform-and-integrations.md#rule-wp-41)

---
