<a id="rule-wp-14"></a>

# WP-14 — ArcChat Hub and Minimal ArcNotes Cross-Process Slice

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `08`, `09`, `10`, `11`, `13` · Downstream: `15`, `16`, `18`

> **Goal.** Two genuinely Native AOT-published processes, talking over a real transport, with real registration, real capability discovery, real idempotency, real approval and real resource references — and ArcNotes still fully editable with ArcChat absent. This is where ArcForges stops being a design and becomes a platform.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcChat + ArcNotes. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The ArcChat Hub as a local coordination plane; a minimal ArcNotes provider exposing two or three real capabilities; the full registration, discovery, invocation, approval and artifact round trip between them; and the degradation behaviour in both directions.

**Out of scope.** ArcChat's conversation model (`15`) and execution engine (`16`). ArcNotes' document model beyond the minimum needed to prove the slice (`18`). Anything cloud.

**Why this package exists.** [SQ-04](../implementation-sequence.md#rule-sq-04) requires that the first cross-process slice be real. [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) permits AI and Cloud fixtures here; IPC, serialization and AOT must be real. It is the single highest-value risk retirement in the sequence.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [Local IPC AOT and fault-injection checks](../../architecture/03-local-ipc-and-process-model.md#11-aot-checklist) | The transport proof; this package’s implementation steps and completion gate define the complete cross-process verification list |
| [`../../architecture/03-local-ipc-and-process-model.md`](../../architecture/03-local-ipc-and-process-model.md) | Registration, routing, health and reconnection |
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | Capability descriptors, context freezing, resource references, artifacts |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | ArcChat is a control plane and never a mandatory data gateway |
| [WP-08](08-local-ipc-and-registration.md#rule-wp-08)–[WP-13](13-high-risk-technical-probes.md#rule-wp-13) output | Transport, capability model, shell, security and probe conclusions |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **ArcNotes remains fully editable and saveable with ArcChat absent** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). This is a hard gate, not a degradation nicety. |
| BR-02 | **The Hub is a coordinator, never a data relay** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). No document body traverses it. |
| BR-03 | **Both processes are Native AOT release publishes.** A debug-host demonstration does not satisfy this package. |
| BR-04 | **Generated proxies, generated type shapes and the protobuf framing are used** — no reflection-based marshalling. |
| BR-05 | **Every write carries a command identity and is idempotent under retry** ([WP-04.01](04-identity-error-and-versioning-primitives.md#rule-wp-04.01)). |
| BR-06 | **Approval crosses the process boundary** and is enforced owner-side, whatever the caller claimed. |
| BR-07 | **Re-registration after a Hub restart is automatic and idempotent** ([WP-08.02](08-local-ipc-and-registration.md#rule-wp-08.02)). |
| BR-08 | **The local UI and the RPC surface use the same application service.** Two paths into one behaviour is a defect. |
| BR-09 | **AI and Cloud may be mocked in this package**; IPC, serialization and AOT may not. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.LocalHub/` | The Hub: registry, routing, lifecycle, health aggregation |
| `src/ArcChat/ArcChat.Desktop/` | Minimal shell hosting the Hub and a capability browser |
| `src/ArcChat/ArcChat.LocalRpc/` | Hub-side contract hosting and consumption |
| `src/ArcNotes/ArcNotes.Domain/`, `.Application/` | Minimal document and block model sufficient for the slice |
| `src/ArcNotes/ArcNotes.LocalRpc/` | Provider registration and capability implementation |
| `src/ArcNotes/ArcNotes.Desktop/` | Minimal editor surface over the same application service |
| `tests/EndToEndTests/` | The cross-process slice suite |

**Major types introduced.** `HubRegistry`, `ProviderRegistration`, `CapabilityBrowser`, `NotesDocument`, `NotesBlock`, `CreateDocumentCommand`, `AppendBlocksCommand`, `ReadDocumentQuery`, `DocumentArtifact`.

---

## 5. Required implementation work

<a id="rule-wp-14.00"></a>

### WP-14.00 — Hub registry and lifecycle

**What must be fully done.** The Hub accepts registrations, maintains leases with heartbeats, aggregates health, routes invocations, and survives restart with automatic provider re-registration. It exposes no data-relay path.

**Testing requirements.** Restart-recovery, lease-expiry and duplicate-registration tests; a structural test asserting no relay endpoint exists.

**Completion gate.** Providers re-register automatically after a Hub restart, dead leases expire, and no data-relay path exists.

<a id="rule-wp-14.01"></a>

### WP-14.01 — Minimal ArcNotes provider

**What must be fully done.** ArcNotes exposes at least: a query capability (read a document), a create capability (create a document), and an authoring capability (append blocks). Each is a real capability descriptor with risk level, side-effect class and approval posture. Writes go through the single write path and the local store.

**Testing requirements.** Capability descriptor validation; write-path assertions; store round-trip.

**Completion gate.** Three real capabilities are registered, discoverable, and backed by durable state.

<a id="rule-wp-14.02"></a>

### WP-14.02 — Discovery and invocation round trip

**What must be fully done.** ArcChat discovers ArcNotes' capabilities through the registry, displays them, and invokes them. Context is frozen at invocation. Results return as typed outcomes. Failures map to the closed semantic error set.

**Testing requirements.** Discovery, invocation and error-mapping tests across success, refusal, unavailable-provider and version-mismatch cases.

**Completion gate.** Discovery and invocation work end to end between published AOT binaries, with every failure typed.

<a id="rule-wp-14.03"></a>

### WP-14.03 — Idempotency and revision

**What must be fully done.** Every write carries a command identity. A retried write produces one effect. An expected-revision mismatch produces a typed conflict rather than a lost update. The outcome carries the resulting revision.

**Testing requirements.** Retry-produces-one-effect; concurrent-write conflict; kill-between-send-and-acknowledge followed by retry.

**Completion gate.** One command yields one effect under retry, disconnection and concurrency, and conflicts are typed rather than silent.

<a id="rule-wp-14.04"></a>

### WP-14.04 — Approval across the boundary

**What must be fully done.** A capability with an approval posture produces an approval request surfaced in ArcChat, with the operation described in the user's terms. Approval is enforced owner-side in ArcNotes: a forged or absent approval is refused there, whatever ArcChat claimed. Approval state is durable across a restart of either process.

**Testing requirements.** Owner-side refusal with a forged approval; approval expiry; approval surviving a restart of each process.

**Completion gate.** ArcNotes refuses an unapproved high-risk operation regardless of what ArcChat asserts, and pending approval survives restart.

<a id="rule-wp-14.05"></a>

### WP-14.05 — Resource references and artifacts

**What must be fully done.** ArcNotes returns a document artifact reference rather than a document body. ArcChat resolves it through the resource path with permission re-checked at access. The Hub carries no body. A large payload uses the controlled transfer channel.

**Testing requirements.** A no-body assertion on the Hub path; permission re-check at resolution; a large-transfer test.

**Completion gate.** Artifacts cross as references, permission is re-checked at access, and the Hub demonstrably carries no body.

<a id="rule-wp-14.06"></a>

### WP-14.06 — Degradation in both directions

**What must be fully done.** ArcNotes starts, edits, saves and recovers with no Hub present, with ecosystem features shown as unavailable with a reason. ArcChat starts with no providers present and shows an empty, explained capability set. Neither blocks on the other.

**Testing requirements.** Hub-absent ArcNotes full workflow; provider-absent ArcChat start; provider crash mid-invocation producing a typed failure with correct effect certainty.

**Completion gate.** Each product is fully usable in its own right with the other absent, and a mid-invocation crash produces a typed outcome.

---

<a id="rule-wp-14.90"></a>
### WP-14.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement the real minimal provider slice with pinned proto/Platform packages; exercise Hub routing inside ArcChat, Notes ownership and degraded product combinations. No CF decision loop enters this slice.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Real independently built AOT executables cover discovery, idempotency, approval, references and ArcChat/Notes absence.

**Completion gate.** Real independently built AOT executables cover discovery, idempotency, approval, references and ArcChat/Notes absence. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The local store carries real document state for the first time |
| Protocol | The first real capability contracts and their versioning |
| UI | Capability browser, approval surface and unavailability reasons |
| Security | Owner-side final validation proven across a real boundary |
| Platform | Cross-process behaviour verified on every desktop platform |
| Migration | The first schema that later migrations must carry forward |
| Compatibility | The first contract version pair that must remain compatible |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Hub restart, lease and no-relay results | [WP-14.00](#rule-wp-14.00) |
| Capability descriptor and write-path results | [WP-14.01](#rule-wp-14.01) |
| Discovery, invocation and error-mapping matrix | [WP-14.02](#rule-wp-14.02) |
| Idempotency, conflict and disconnection results | [WP-14.03](#rule-wp-14.03) |
| Owner-side refusal, expiry and restart-survival results | [WP-14.04](#rule-wp-14.04) |
| Artifact reference, permission re-check and no-body assertions | [WP-14.05](#rule-wp-14.05) |
| Hub-absent and provider-absent workflow results | [WP-14.06](#rule-wp-14.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-14.90](#rule-wp-14.90) and all inherited domain-specific gates must pass on the same candidate closure. Real independently built AOT executables cover discovery, idempotency, approval, references and ArcChat/Notes absence.

**All of the following, between two genuinely Native AOT-published processes, with recorded evidence:**

1. Registration, lease, heartbeat and automatic re-registration after Hub restart all work.
2. Capability discovery and invocation succeed, with every failure mapped to the closed semantic error set.
3. One command produces one effect under retry, disconnection and concurrency; conflicts are typed.
4. ArcNotes refuses an unapproved high-risk operation regardless of ArcChat's assertion, and pending approval survives a restart of either process.
5. Artifacts cross as references with permission re-checked at access, and the Hub carries no payload body.
6. **ArcNotes starts, edits, saves and recovers fully with ArcChat absent**, and ArcChat starts cleanly with no providers present.
7. Generated proxies, generated type shapes and the protobuf framing are used throughout; no reflection-based marshalling exists on the path.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [08 local ipc and registration](08-local-ipc-and-registration.md#rule-wp-08)
- [09 capability contribution and resource model](09-capability-contribution-and-resource-model.md#rule-wp-09)
- [10 design system and desktop shell](10-design-system-and-desktop-shell.md#rule-wp-10)
- [11 security foundation](11-security-foundation.md#rule-wp-11)
- [13 high risk technical probes](13-high-risk-technical-probes.md#rule-wp-13)

**Downstream — consumers of these released outputs.**

- [15 arcchat conversation core](15-arcchat-conversation-core.md#rule-wp-15)
- [16 unified execution engine](16-unified-execution-engine.md#rule-wp-16)
- [18 arcnotes document core](18-arcnotes-document-core.md#rule-wp-18)

---
