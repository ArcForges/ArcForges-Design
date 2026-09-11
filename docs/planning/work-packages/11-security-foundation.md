<a id="rule-wp-11"></a>

# WP-11 — Security Foundation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `04`, `08`, `09` · Downstream: `14`, `16`, `22`, `41`

> **Goal.** Implement the security model as mechanism rather than convention: principals and the actor chain, the R0–R4 risk model, the four enforcement points with owner-side final validation always last, approval and step-up, the secret broker, egress control, instruction provenance, capability leases and the append-only audit.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform/Cloud/AI adapters; Contracts public definitions. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The security decision pipeline and its enforcement points; the actor chain; risk classification and runtime modifiers; approval, step-up and local presence; the secret broker with `SecretRef` semantics; data egress as a separate authorization; instruction provenance marking; capability leases; typed trust evaluation; and the audit subsystem.

**Out of scope.** Cloud authentication and account lifecycle (`22`). Entitlement (`42`). Extension-specific enforcement (`41`), which attaches to this foundation.

**Why this package exists.** Security enforcement attaches to the invocation pipeline built in `09`. Attaching it later means every capability written in between has to be re-audited. [I-259](../../requirements/01-normative-glossary-and-invariants.md#rule-i-259) and [I-260](../../requirements/01-normative-glossary-and-invariants.md#rule-i-260) also make the point that isolation is not authorization — the enforcement must exist independently of process boundaries.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/08-security-architecture.md`](../../architecture/08-security-architecture.md) | Identity layering, four enforcement points, approval, secret broker, egress, trust, audit |
| [`../../requirements/07-security-privacy-and-trust.md`](../../requirements/07-security-privacy-and-trust.md) | The fourteen-step decision pipeline, R0–R4, reason codes, the security centre |
| **[V-01](../../assurance/phase-1-official-verification.md#rule-v-01)** | AI transparency obligations that attach to the same pipeline |
| [WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04) output | Typed identifiers, effect certainty and the reason-code registry |
| [WP-08](08-local-ipc-and-registration.md#rule-wp-08), [WP-09](09-capability-contribution-and-resource-model.md#rule-wp-09) output | The transport and the invocation pipeline enforcement attaches to |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Owner-side final validation always applies.** Whatever earlier enforcement point allowed a call, the capability owner validates again. |
| BR-02 | **Isolation is not authorization** ([I-259](../../requirements/01-normative-glossary-and-invariants.md#rule-i-259)); **out-of-process is not automatically safe** ([I-260](../../requirements/01-normative-glossary-and-invariants.md#rule-i-260)). |
| BR-03 | **Capability permission and resource authorization are separate.** Holding a capability grant never implies access to a specific resource. |
| <a id="rule-br-04"></a>BR-04 | **Use ≠ Reveal.** A `SecretRef` permits use of a secret without disclosing its value; no code path returns a plaintext secret to a caller that only needs to use it. |
| <a id="rule-br-05"></a>BR-05 | **Data egress is a separate authorization** from read access. |
| BR-06 | **Every input that can carry instructions is marked with its provenance**, and untrusted provenance never gains authority. |
| BR-07 | **A delegation creates a lease**: scoped, expiring, revocable and audited. |
| BR-08 | **Audit is append-only** and separate from observability ([OA-06](../../architecture/13-observability-and-operations.md#rule-oa-06) in the observability architecture). |
| BR-09 | **A refusal is explained with a registered reason code**, never a silent failure. |
| BR-10 | **Approval is not steering.** Approving an operation is a discrete authorization; steering adjusts a running operation and is not an authorization. |
| BR-11 | **Local presence is required for the highest risk class**, and a biometric app-unlock never substitutes for step-up ([I-277](../../requirements/01-normative-glossary-and-invariants.md#rule-i-277), [I-278](../../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Security/` | Reconciled and extended: principals, actor chain, risk model, decision pipeline, lease manager, trust evaluation |
| `src/BuildingBlocks/ArcForges.Security.Secrets/` | Created: the secret broker, `SecretRef` resolution, platform secure storage adapters |
| `src/BuildingBlocks/ArcForges.Security.Audit/` | Created: append-only audit writer, actor chain capture, export |
| `src/BuildingBlocks/ArcForges.Capabilities/` | Extended: the authorize step of the invocation pipeline |
| `tests/SecurityEnforcementTests/` | Created: refusal matrix, lease expiry, egress, provenance, audit completeness |

**Major types introduced.** `Principal`, `ActorChain`, `ActorKind`, `RiskLevel`, `RiskModifier`, `SecurityDecision`, `EnforcementPoint`, `ApprovalRequest`, `ApprovalOutcome`, `StepUpChallenge`, `LocalPresenceProof`, `SecretRef`, `SecretBroker`, `EgressRequest`, `InstructionProvenance`, `CapabilityLease`, `TrustLevel`, `AuditEvent`.

---

## 5. Required implementation work

<a id="rule-wp-11.00"></a>

### WP-11.00 — Principals and the actor chain

**What must be fully done.** Every operation carries a complete actor chain: the human principal, the device, the installation, the session, and any agent or extension acting on the principal's behalf. The chain is constructed once at the entry point and flows through every layer without reconstruction.

**Testing requirements.** A propagation test asserting the chain survives every hop including queue and process boundaries; a completeness test asserting no operation reaches an enforcement point without a chain.

**Completion gate.** No operation can reach an enforcement point without a complete actor chain.

<a id="rule-wp-11.01"></a>

### WP-11.01 — Risk model and classification

**What must be fully done.** R0–R4 with runtime modifiers. Every capability declares a base risk; modifiers raise it based on scope, target, reversibility, egress and actor kind. The effective risk is computed, explainable, and never lowered by a modifier.

**Testing requirements.** Classification tests across every modifier combination; a monotonicity test asserting a modifier can only raise risk.

**Completion gate.** Effective risk is computed, explainable and monotonic.

<a id="rule-wp-11.02"></a>

### WP-11.02 — The decision pipeline and enforcement points

**What must be fully done.** The fourteen-step decision pipeline implemented once, invoked at each of the four enforcement points, with owner-side validation always last. Each step produces a typed outcome, and a refusal names the failing step.

**Testing requirements.** A step-coverage test asserting every step runs; a refusal matrix producing a distinct reason code per failing step; a bypass test asserting no route reaches a capability without the pipeline.

**Completion gate.** The pipeline is unbypassable, every step is exercised, and every refusal names its step and reason code.

<a id="rule-wp-11.03"></a>

### WP-11.03 — Approval, steering and step-up

**What must be fully done.** Approval requests with a bounded lifetime, a durable pending state, and an explicit outcome. Steering is a separate mechanism that adjusts a running operation without granting authority. Step-up challenges for the enumerated sensitive operations. Local presence for the highest risk class, with biometric unlock explicitly not substituting for it.

**Testing requirements.** Approval expiry, duplicate-approval, and approval-after-cancel tests; a test asserting steering cannot escalate authority; a test asserting biometric unlock does not satisfy step-up.

**Completion gate.** Approval is durable and bounded, steering cannot escalate, and app-unlock never substitutes for step-up.

<a id="rule-wp-11.04"></a>

### WP-11.04 — Secret broker

**What must be fully done.** Secrets are stored in platform secure storage, referenced by `SecretRef`, and used through the broker. Use and reveal are separate operations with separate authorization. A secret-bearing type has no string representation and cannot be logged or serialized into a contract.

**Testing requirements.** A structural test that a secret type cannot be logged or serialized; a use-without-reveal test; a reveal-authorization test; a platform round-trip test per operating system.

**Completion gate.** A secret can be used without being revealed, and a secret type is structurally unloggable and unserializable.

<a id="rule-wp-11.05"></a>

### WP-11.05 — Egress control

**What must be fully done.** Every outbound data transfer is an egress decision with its own authorization, distinct from read access. The decision records what class of data, to what destination, under whose authority. A denied egress produces a typed refusal.

**Testing requirements.** A matrix asserting read access alone never authorizes egress; destination allowlist tests; a test asserting egress decisions are audited.

**Completion gate.** Read access never implies egress, and every egress is authorized and audited.

<a id="rule-wp-11.06"></a>

### WP-11.06 — Instruction provenance

**What must be fully done.** Every input that can carry instructions — model output, extension output, retrieved content, imported documents, deep links, catalog metadata — is marked with its provenance. Content of untrusted provenance can be processed but never gains authority to trigger an operation on its own.

**Testing requirements.** An injection corpus asserting that untrusted content cannot cause an unapproved operation; a marking-completeness test over every input path.

**Completion gate.** Every instruction-bearing input path is marked, and the injection corpus produces no unauthorized operation.

<a id="rule-wp-11.07"></a>

### WP-11.07 — Capability leases and trust

**What must be fully done.** A delegation creates a lease with scope, expiry and revocation. Lease expiry is enforced at use, not only at issue. Typed trust levels are evaluated at the defined points, and trust is separate from permission.

**Testing requirements.** Lease expiry-at-use, revocation-mid-operation and scope-escalation-attempt tests; a test asserting trust level alone never grants permission.

**Completion gate.** Leases expire at use and revoke mid-operation, and trust never substitutes for permission.

<a id="rule-wp-11.08"></a>

### WP-11.08 — Audit

**What must be fully done.** An append-only audit store, separate from telemetry, recording the enumerated security and business-state events with the full actor chain. No update or delete path exists. Audit access is itself audited.

**Testing requirements.** An immutability test asserting update and delete fail; a completeness test asserting every enumerated event is written; a separation test asserting no audit event lands in telemetry storage and no telemetry event lands in audit storage.

**Completion gate.** Audit is structurally append-only, complete for the enumerated event set, and provably separate from telemetry.

---

<a id="rule-wp-11.09"></a>

### WP-11.09 — Content helper and OS-enforced isolation

**What must be fully done.** Build the first-party C# Native AOT ContentSandbox, brokered bounded DTO/buffer protocol, parent-bound lifecycle and all RID profiles in [the isolation architecture](../../architecture/24-content-and-extension-isolation.md). Launch restrictions must apply before any parser/extension code runs. Add the signed helper/package inputs and typed isolation-unavailable result; the product retains all domain/agent authority.

**Testing requirements.** Publish and execute the real restricted helper on every supported RID. Attempt product-store/secret reads, loopback/external networking, process escape and descriptor abuse; inject native crash, hang, output overflow and parent death. Verify OS denial, resource bounds and cleanup. Test missing profile without an unsafe fallback.

**Completion gate.** Required first-party parser profiles demonstrably contain hostile parsing and deny access outside brokered resources. No mocked launcher or same-user unrestricted child satisfies this gate; [PG-22](../../assurance/open-gates-register.md#rule-pg-22) carries the runtime evidence.

---

<a id="rule-wp-11.90"></a>
### WP-11.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement fixed actor/owner, approval, secrets, egress and provenance rules across new boundaries. Package the signed, parent-bound content helper and OS broker with its native dependencies.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Cross-boundary owner refusal, stale approval/revocation, secrets/redaction and real OS-isolation tests; no hostile parser moved into a product process by package consolidation.

**Completion gate.** Cross-boundary owner refusal, stale approval/revocation, secrets/redaction and real OS-isolation tests; no hostile parser moved into a product process by package consolidation. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The audit store and its retention; secret metadata (never secret values) |
| Protocol | Actor chain and approval messages become live protocol |
| UI | Approval prompts, step-up flows, refusal messages and the security centre foundation |
| Security | This package *is* the security foundation |
| Platform | Platform secure storage and local presence per operating system |
| Migration | Audit retention outlives observability retention and constrains storage planning |
| Compatibility | Reason codes and refusal semantics become part of the client contract |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Actor chain propagation and completeness results | [WP-11.00](#rule-wp-11.00) |
| Risk classification and monotonicity matrix | [WP-11.01](#rule-wp-11.01) |
| Pipeline bypass, step-coverage and refusal matrix | [WP-11.02](#rule-wp-11.02) |
| Approval, steering and step-up results | [WP-11.03](#rule-wp-11.03) |
| Secret structural prohibitions and platform round-trip results | [WP-11.04](#rule-wp-11.04) |
| Egress authorization matrix and audit assertions | [WP-11.05](#rule-wp-11.05) |
| Injection corpus results and marking coverage | [WP-11.06](#rule-wp-11.06) |
| Lease expiry, revocation and trust-separation results | [WP-11.07](#rule-wp-11.07) |
| Audit immutability, completeness and separation results | [WP-11.08](#rule-wp-11.08) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-11.90](#rule-wp-11.90) and all inherited domain-specific gates must pass on the same candidate closure. Cross-boundary owner refusal, stale approval/revocation, secrets/redaction and real OS-isolation tests; no hostile parser moved into a product process by package consolidation.

**[PG-12](../../assurance/open-gates-register.md#rule-pg-12) evidence:** [WP-11.09](#rule-wp-11.09) — Packaged RID PDF parser containment, licence/binding and hostile-input proof; combine with Notes viewer integration. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. No operation reaches an enforcement point without a complete actor chain.
2. Effective risk is computed, explainable and can only be raised by a modifier.
3. The decision pipeline is unbypassable; every refusal names its failing step and a registered reason code; owner-side validation always runs last.
4. Approval is durable and bounded; steering cannot escalate authority; biometric app-unlock never satisfies step-up.
5. A secret can be used without being revealed, and secret types are structurally unloggable and unserializable.
6. Read access never implies egress; every egress is separately authorized and audited.
7. Every instruction-bearing input is provenance-marked, and the injection corpus produces no unauthorized operation.
8. Leases expire at use and revoke mid-operation; trust never substitutes for permission.
9. Audit is append-only, complete, and provably separate from telemetry.

The [WP-11.09](#rule-wp-11.09) helper and broker must additionally pass their packaged RID containment matrix, including native parser crash, prohibited file/network access, child escape, timeout and parent termination. Unsupported profiles fail closed; a process boundary alone cannot close [PG-22](../../assurance/open-gates-register.md#rule-pg-22).

---

## 9. Dependencies

**Upstream — all must be complete.**

- [04 identity error and versioning primitives](04-identity-error-and-versioning-primitives.md#rule-wp-04)
- [08 local ipc and registration](08-local-ipc-and-registration.md#rule-wp-08)
- [09 capability contribution and resource model](09-capability-contribution-and-resource-model.md#rule-wp-09)

**Downstream — consumers of these released outputs.**

- [14 hub and minimal provider slice](14-hub-and-minimal-provider-slice.md#rule-wp-14)
- [16 unified execution engine](16-unified-execution-engine.md#rule-wp-16)
- [22 identity workspace and device](22-identity-workspace-and-device.md#rule-wp-22)
- [41 extension platform and integrations](41-extension-platform-and-integrations.md#rule-wp-41)

---
