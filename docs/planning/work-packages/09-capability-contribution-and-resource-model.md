<a id="rule-wp-09"></a>

# WP-09 — Capability, Contribution and Resource Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Implement the cross-application semantic model — App, Installation, Instance, Contribution, Capability, Action, Context, `ResourceRef`, Artifact, Deep Link, Event, Health and Invocation — so that every product, extension and agent describes and reaches every other through one vocabulary.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Contracts; Platform; products. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The capability registry and its selection pipeline; contribution registration; the six contribution kinds' registration paths; action availability; context providers and context freezing; resource and artifact reference resolution; deep links; the event model; health reporting; and the invocation pipeline with its fixed routing priority and semantic error set.

**Out of scope.** The agent runtime that consumes capabilities (`16`). Product-specific capability implementations. Extension hosting (`41`).

**Why this package exists.** Without one semantic model, each product invents its own, and every same-application feature becomes a bespoke integration. This is also the layer where the permission model attaches, so it must exist before security enforcement is wired.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


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
| <a id="rule-br-01"></a>BR-01 | **`App ≠ Installation ≠ Instance`.** Three distinct identities with three distinct lifecycles. |
| <a id="rule-br-02"></a>BR-02 | **`Capability ≠ Action`.** A capability is an invocable semantic operation; an action is a user-facing offer with availability. |
| <a id="rule-br-03"></a>BR-03 | **`ResourceRef` floats; `ResourceVersionRef` pins.** Choosing the wrong one is a semantic defect, not a style choice. |
| <a id="rule-br-04"></a>BR-04 | **A resource is owned by exactly one product forever.** Ownership does not transfer with a reference. |
| <a id="rule-br-05"></a>BR-05 | **Context is frozen at invocation.** A capability sees the context as it was when the invocation began, never a later mutation. |
| <a id="rule-br-06"></a>BR-06 | **Availability is computed, not assumed.** An action unavailable for a stated reason is shown as unavailable with that reason, never silently missing. |
| <a id="rule-br-07"></a>BR-07 | **Routing priority is fixed** and identical on every platform (`§10` of the contract architecture). |
| <a id="rule-br-08"></a>BR-08 | **The semantic error set is closed**, and every invocation failure maps to it. |
| <a id="rule-br-09"></a>BR-09 | **Health has five dimensions** — reachable, ready, healthy, degraded, capacity — used identically locally and in the cloud. |
| <a id="rule-br-10"></a>BR-10 | **A capability descriptor is richer than a tool description**: it carries risk level, trust requirement, side-effect class, reversibility and approval posture. |

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

### WP-09.00 — Application identity and in-process composition

**What must be fully done.** Bind the closed ProductId, device, installation and instance epoch to each application composition root. Companion product identity is independent of Android/Web platform. No running-product registry or shared desktop Hub.

**Testing requirements.** Two products on one device keep separate sessions/history/capabilities; forged/missing target refuses.

**Completion gate.** Every application owns an independent registry and typed owner handlers.

<a id="rule-wp-09.01"></a>

### WP-09.01 — Static contribution registration

**What must be fully done.** Register capability/context/artifact/lifecycle/deep-link handlers inside the owning process through generated descriptors and explicit composition. Child extension contributions pass the admitted host boundary and grants.

**Testing requirements.** Duplicate IDs, wrong owner, unavailable child, undeclared tool schema and cross-product registration refuse.

**Completion gate.** No product process discovery, peer heartbeat or central contribution host is required.

<a id="rule-wp-09.02"></a>

### WP-09.02 — Capability registry and selection

**What must be fully done.** Implement the wire CapabilityDescriptor/OperationBinding/effect/locus/context/cancellation schema and complete initial first-party binding matrix. Register exactly the product and Cloud tool methods declared by Contracts; validate per-operation risk and grant posture.

**Testing requirements.** Enumerate expected bindings; reject missing/extra methods, unsupported major, inconsistent pureRead/write classification, readiness mismatch and ambiguous target.

**Completion gate.** No implementer invents binding fields or capability behavior to join products.

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

### WP-09.06 — Own navigation, hints and health

**What must be fully done.** Route artifact opens and deep links to the owning application handler; bounded in-process state hints cause authoritative rereads. Private child events follow annex 09; Cloud application presence is WP26.

**Testing requirements.** Invalid ownership, missing content, expired child cursor, restart and duplicate hint recover without launching another product.

**Completion gate.** Own-app navigation and child recovery work while other products are closed or absent.

<a id="rule-wp-09.07"></a>

### WP-09.07 — Invocation pipeline

**What must be fully done.** The end-to-end invocation path: resolve → check availability → freeze context → authorize → invoke → validate result → record. Failures map to the closed semantic error set. The pipeline is the only route to a capability.

**Testing requirements.** A policy test asserting no bypass route exists; error-mapping tests for every semantic error; a tracing test asserting each invocation is observable.

**Completion gate.** The pipeline is the only route, every failure maps to the closed set, and every invocation is traced.

---

<a id="rule-wp-09.90"></a>
### WP-09.90 — Verify the owned artifact and real integration

**What must be fully done.** Consume generated capability/resource/contribution contracts. Preserve typed invocation, owner semantics, resource affinity/availability, preflight/compensation and large-artifact references. Generate AI tool projections from the same definitions.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

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

[Local gRPC closure](../../architecture/contracts/09-local-grpc-and-sandbox.md): Bind every capability/resource/context port to generated local gRPC and AZ04 eligibility/egress metadata; no model-callable infrastructure or untyped callback path.

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
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-09.90](#rule-wp-09.90) |

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

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [PLT.17](../delivery/lanes/platform.md#task-plt-17) | [WP-09.00](09-capability-contribution-and-resource-model.md#rule-wp-09.00) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [FND.01](../delivery/lanes/foundation.md#task-fnd-01) (artifact) |
| [PLT.18](../delivery/lanes/platform.md#task-plt-18) | [WP-09.01](09-capability-contribution-and-resource-model.md#rule-wp-09.01) (full)<br>[WP-09](09-capability-contribution-and-resource-model.md#rule-wp-09) Contribution/registration state durable across restarts (SS6 impacts) (package-level obligation contribution) | none |
| [PLT.19](../delivery/lanes/platform.md#task-plt-19) | [WP-09.02](09-capability-contribution-and-resource-model.md#rule-wp-09.02) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [PLT.20](../delivery/lanes/platform.md#task-plt-20) | [WP-09.03](09-capability-contribution-and-resource-model.md#rule-wp-09.03) (full) | none |
| [PLT.21](../delivery/lanes/platform.md#task-plt-21) | [WP-09.04](09-capability-contribution-and-resource-model.md#rule-wp-09.04) (full) | none |
| [PLT.22](../delivery/lanes/platform.md#task-plt-22) | [WP-09.05](09-capability-contribution-and-resource-model.md#rule-wp-09.05) (full) | [PLT.05](../delivery/lanes/platform.md#task-plt-05) (artifact) |
| [PLT.23](../delivery/lanes/platform.md#task-plt-23) | [WP-09.06](09-capability-contribution-and-resource-model.md#rule-wp-09.06) (full) | none |
| [PLT.24](../delivery/lanes/platform.md#task-plt-24) | [WP-09.07](09-capability-contribution-and-resource-model.md#rule-wp-09.07) (all work except the parts mapped to PLT.57) | none |
| [PLT.25](../delivery/lanes/platform.md#task-plt-25) | [WP-09.90](09-capability-contribution-and-resource-model.md#rule-wp-09.90) (full) | none |
| [PLT.57](../delivery/lanes/platform.md#task-plt-57) | [WP-09.07](09-capability-contribution-and-resource-model.md#rule-wp-09.07) (real authorize-step integration) | [PLT.38](../delivery/lanes/platform.md#task-plt-38) (artifact), [APP.01](../delivery/lanes/app-composition.md#task-app-01) (artifact) |

**Consumers outside this package:** [APP.01](../delivery/lanes/app-composition.md#task-app-01), [APP.02](../delivery/lanes/app-composition.md#task-app-02), [APP.06](../delivery/lanes/app-composition.md#task-app-06), [EXE.01](../delivery/lanes/execution.md#task-exe-01), [EXT.00](../delivery/lanes/extensions.md#task-ext-00), [NAT.01](../delivery/lanes/native.md#task-nat-01), [NOTES.12](../delivery/lanes/arcnotes.md#task-notes-12), [PLT.28](../delivery/lanes/platform.md#task-plt-28), [PLT.37](../delivery/lanes/platform.md#task-plt-37), [PLT.42](../delivery/lanes/platform.md#task-plt-42), [PLT.46](../delivery/lanes/platform.md#task-plt-46), [PLT.51](../delivery/lanes/platform.md#task-plt-51).

<!-- delivery-graph:end -->

