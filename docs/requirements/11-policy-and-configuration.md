# Dynamic Policy and Configuration Requirements

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Companions: [`04-commerce-entitlement-and-credits.md`](04-commerce-entitlement-and-credits.md), [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`09-shared-desktop-experience.md`](09-shared-desktop-experience.md), [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md)

The **Dynamic Configuration and Product Policy Control Plane** answers one question:

> How does ArcForges change *how the current product is allowed to run* — safely, explainably, and reversibly — without redistributing the client?

---

## 1. Four founding boundaries

| # | Boundary | Why it matters |
|---|---|---|
| BD-01 | **Policy ≠ Entitlement** (`I-341`) | "Temporarily unavailable" (policy), "upgrade required" (entitlement) and "not available here" (policy scope) are three different user messages with three different resolutions |
| BD-02 | **Policy ≠ Settings** (`I-340`) | A user preference is not an administrative constraint. A policy-disabled feature shows as disabled with its reason, not as an unchecked box |
| BD-03 | **Policy ≠ Runtime Health** (`I-343`) | "Not currently enforceable" (health) is not "not permitted" (policy) |
| BD-04 | **Policy Control Plane ≠ request Data Plane** (`I-345`) | A client-side policy decision is a user-experience optimisation. **Every cloud service performs its own server-side policy check on the actual request.** |

Additionally: **Policy ≠ Permission** (`I-342`) and **Policy ≠ Domain State** (`I-344`).

### 1.1 The layered decision

A capability is usable only when every layer independently permits it:

```
Binary contains the code path
  → Product policy allows the feature            (this document)
  → Entitlement permits this workspace           (commerce requirements)
  → Security authorises this actor and resource  (security requirements)
  → Runtime health permits execution now
  → User settings have it enabled
```

**A single boolean cannot express this.** Each layer produces its own decision with its own reason, and the composition is explicit.

---

## 2. Feature and Feature Flag

**Feature = a stable product capability identity.**
**Feature Flag = a dynamic gate stating whether a Feature may currently be activated.**

| # | Requirement |
|---|---|
| FT-01 | **Feature ≠ Feature Flag** (`I-347`). The feature is the capability; the flag is a temporary gate over it. |
| FT-02 | **`FeatureId` is stable and namespaced** by owning product. Renaming a user-facing label does not change the `FeatureId`. |
| FT-03 | **A feature flag is not a permanent architecture layer.** Every flag carries a lifecycle and an intended removal point; a mature feature has its rollout flag deleted. |
| FT-04 | **Feature lifecycle** is explicit: `InDevelopment → Internal → Preview → Rollout → GA → Deprecated → Removed`. Temporary code paths are removed as the lifecycle advances. |
| FT-05 | **A feature flag can never replace real version design** (`I-382`). It gates whether an already-compatible, already-secure capability is exposed. It cannot make an incompatible binary compatible. |
| FT-06 | **A feature flag must correspond to an existing code path.** A flag enabling something the installed binary cannot do resolves to `UnsupportedByBinary`, not to "on". |
| FT-07 | **Feature prerequisites** are declared, and the prerequisite graph must be acyclic; a cyclic definition is rejected at publish. |
| FT-08 | **A feature flag must not be used to hide a paywall** (`I-350`). Subscription logic disguised as a flag is prohibited — it produces a system where nobody can explain why a user cannot do something. |

---

## 3. Rollout

**Rollout = a release strategy in which a feature expands gradually from few subjects to many.**

| # | Requirement |
|---|---|
| RO-01 | **Rollout ≠ Experiment** (`I-349`). A rollout ends with the feature everywhere; an experiment compares variants. |
| RO-02 | **Percentage rollout must be deterministic.** The same subject resolves the same way on every evaluation. Random-per-request assignment is prohibited (`I-352`). |
| RO-03 | **The rollout subject is explicit**: User, Workspace, or Device/Installation. Which one is correct depends on the feature and must be declared. |
| RO-04 | **Email must never be the bucketing identity.** Email changes; identity must not. |
| RO-05 | **Assignment identities are never shared across realms.** An official-realm assignment does not apply in a self-hosted realm. |
| RO-06 | **Signed-out users** bucket on `InstallationId`, or are excluded from the rollout entirely — declared per rollout, never left implicit. |
| RO-07 | Allowlists and denylists are supported alongside percentage. |
| RO-08 | **Release channel and rollout are independent axes.** Being on a preview channel is not the same as being in a rollout cohort. |
| RO-09 | **A rollout must be haltable immediately** — hold at the current exposure, or roll exposure back. |
| RO-10 | **A rollout rollback must never destroy user data.** If a feature created data, disabling the feature leaves the data intact and legible. **Rollout cannot substitute for format compatibility** (`I-386`). |

---

## 4. Kill switch

**Kill Switch = the highest-priority dynamic control, used to stop a new execution or a dangerous behaviour under abnormal conditions.**

| # | Requirement |
|---|---|
| KS-01 | **Kill Switch ≠ Feature Lifecycle** (`I-353`). It is emergency control, not a lifecycle stage. |
| KS-02 | **Stop semantics are declared**, from four modes: |

| Mode | Behaviour |
|---|---|
| **BlockNew** | New invocations are refused; existing work continues |
| **DrainExisting** | New invocations are refused; existing work completes normally |
| **StopAtSafePoint** | Cooperative cancellation at the next safe point |
| **ReadOnly** | Reads and saves continue; the affected mutation path is closed |

| # | Requirement |
|---|---|
| KS-03 | **A kill switch never deletes data** (`I-354`). |
| KS-04 | **A kill switch on a cloud capability is enforced server-side.** A client that has not received it is still refused at the service. |
| KS-05 | **A remote kill switch is not the remedy for a local security vulnerability.** A local security boundary is fixed by an application update; the kill switch reduces exposure in the interim (see the security-advisory process in [`10-distribution-update-and-support.md`](10-distribution-update-and-support.md)). |
| KS-06 | A kill switch **must not require a restart** to take effect. |
| KS-07 | Kill switches use the **fastest publication path**, distinct from ordinary policy publication. |

---

## 5. Remote configuration

**Remote Config = product parameters issued by the server and constrained by schema.**

| # | Requirement |
|---|---|
| RC-01 | **Remote Config is not a general JSON blob** (`I-356`). Every key has a definition, a type, a validation rule, an owner and a default. |
| RC-02 | **The value type set is closed**: null, boolean, integer, decimal, string, enumerated value, duration, list of these, and record of these. **Arbitrary CLR objects, runtime types and code are prohibited.** |
| RC-03 | **Every numeric config has validation** — range, unit, and monotonicity where relevant. |
| RC-04 | **A compiled hard limit always outranks remote config.** Remote config may tighten a limit; it can never exceed the built-in safety ceiling. An out-of-range value is rejected or clamped as invalid, and the rejection is recorded. |
| RC-05 | **Every remote config key has a safe compiled default**, so a client with no policy at all still behaves correctly. |
| RC-06 | **Remote Config ≠ User Setting** (`I-355`). A setting declares whether it is policy-controllable at all; some settings are never remotely forceable. |
| RC-07 | **Remote Config ≠ Project Format** (`I-357`) and **≠ transport selection** (`I-358`). Neither the persistent format nor the communication architecture is remotely configurable. |
| RC-08 | **Every policy key has an owning product.** Unowned keys accumulate into an unmaintainable surface and are rejected at publication. |
| RC-09 | Platform-level policy keys carry only genuinely cross-product semantics; everything else lives in a product namespace. |
| RC-10 | **No global key is exposed to a third-party extension.** An extension operates in its own namespace and **cannot set a platform kill switch**. |

---

## 6. Policy scope and resolution

| # | Requirement |
|---|---|
| PS-01 | **"More specific always wins" is not a valid universal rule.** Each policy definition declares its own permitted scopes and its own resolution rule. |
| PS-02 | Recommended scopes: **Realm**, **Platform**, **Product**, **Workspace**, **Cohort/Rollout**, **Device/Installation**. |
| PS-03 | **Policy Scope ≠ Entitlement Scope** (`I-346`). |
| PS-04 | **Realm is the top-level isolation boundary.** Official policy and self-hosted policy are separate authorities. |
| PS-05 | **A self-hosted realm has its own policy authority.** Where a self-hosted deployment consumes official managed AI, the official policy governs *that service*; it does not become the self-hosted product's control plane. |
| PS-06 | **Policy rules use a limited declarative predicate language.** Remote arbitrary script is prohibited. |
| PS-07 | **The policy engine is deterministic**: the same decision context yields the same decision, every time, on every surface. |
| PS-08 | **User content never enters the policy decision context.** A decision that depends on document content cannot be stably explained and is prohibited. |
| PS-09 | **A policy rule cannot be arbitrarily complex.** This is not a general business-rules engine. |

### 6.1 Workspace policy

| # | Requirement |
|---|---|
| WP-01 | **Workspace Policy ≠ Workspace Permission** (`I-365`). Policy narrows what the product may do; permission decides what an actor may do. |
| WP-02 | **Workspace policy may only tighten a platform restriction, never loosen one.** Hard deny wins. |
| WP-03 | **A user cannot bypass workspace policy through local configuration.** |
| WP-04 | **Workspace policy cannot change local core ownership.** It cannot make ArcNotes depend on ArcChat, cannot relocate data ownership, and cannot override the architecture constitution. |

### 6.2 Product invariants beyond remote reach

Certain properties are **never** feature-flagged, remotely configured or policy-controlled:

- State ownership and the product topology
- Local-first operation and the ability to work with no account and no network
- Which product owns a protocol or a resource type
- The choice of transport for local IPC, public API or realtime
- Persistent format contracts
- Security boundaries and authorization requirements
- The two-boundary licensing model

---

## 7. Compatibility policy

**Compatibility Policy = whether the platform *allows* a client or capability to continue accessing online services, even where the technical protocol would still work.**

| # | Requirement |
|---|---|
| CO-01 | **Compatibility Policy ≠ Capability Negotiation** (`I-359`). Negotiation determines what two versions *can* do; policy determines what they are *permitted* to do. |
| CO-02 | Compatibility policy takes effect **per capability or service**, not as a blanket client block. |
| CO-03 | Version policy levels: **Recommended version**, **Minimum cloud version**, **Minimum version per capability**, **Blocked version range**. |
| CO-04 | **A blocked version range is distinct from a minimum version.** A specific bad build can be blocked while both older and newer builds remain allowed. |
| CO-05 | **A grace period applies before a minimum-version block takes effect**, with clear in-product notice. |
| CO-06 | **An emergency security block may skip the grace period** — an explicitly exceptional path, recorded as such. |
| CO-07 | **Minimum Cloud Version ≠ Minimum Local Data Version** (`I-360`). A client blocked from cloud sync must still open, edit, export and recover its local data. |
| CO-08 | **Compatibility policy can never make local user data inaccessible.** |
| CO-09 | **Compatibility policy cannot redefine a project format** (`RC-07`). |
| CO-10 | A blocked old client receives a specific, actionable message naming the required version and what remains available. |

---

## 8. Provider and model availability

| # | Requirement |
|---|---|
| PA-01 | **Provider catalog and provider availability are separate.** The catalog describes what exists; availability states what may currently be used for new executions. |
| PA-02 | **Provider Availability ≠ Provider Health** (`I-361`). Availability is policy; health is runtime fact. |
| PA-03 | Model lifecycle states: **Available**, **Preview**, **Limited**, **Deprecated**, **Retired**, **Suspended**. |
| PA-04 | **Model Availability ≠ Model Entitlement** (`I-362`) and **≠ Model Capability** (`I-363`). |
| PA-05 | **Silent substitution of a pinned model is prohibited** (`RT-08` in the AI requirements). If a user pinned a specific model and it becomes unavailable, the product says so and asks. |
| PA-06 | **Auto mode is different**: an auto class may route across its permitted set without asking, within its cost ceiling and policy. |
| PA-07 | **A Task or Run snapshots the model policy decision at start** (`TR-04`). Ordinary availability changes do not alter a running Run. |
| PA-08 | **An emergency model suspension may interrupt future invocations** inside a running Run — the one case where emergency policy outranks the run snapshot. |
| PA-09 | An already-dispatched provider request is allowed to complete or is cancelled per the kill-switch mode; it is never left in an undefined state. |
| PA-10 | **Model capability metadata is not fabricated by remote config.** It comes from the provider/model catalog definition. |
| PA-11 | **Provider and model policy never carry pricing** (`I-350` analogue). Pricing is the commercial layer (**D-020**). |
| PA-12 | **Model availability must not disguise a plan restriction.** "Not available" and "not included in your plan" are different messages produced by different layers. |
| PA-13 | **Model retirement must not silently rewrite history.** A historical task retains the model it used (`RT-13`). |
| PA-14 | If a pinned model retires, the user is prompted to choose a replacement; the system does not choose silently. |

---

## 9. Experiments

**Experiment = stable assignment of eligible subjects to variants, to test a product hypothesis.**

| # | Requirement |
|---|---|
| EX-01 | **Experiment ≠ Rollout** (`I-349`) and **Experiment ≠ Entitlement** (`I-350`). |
| EX-02 | An experiment declares: hypothesis, subject unit, eligibility, variants, allocation, duration, success metrics and exit criteria. |
| EX-03 | **Assignment is sticky.** Re-randomising per request destroys both the data and the user experience (`I-352`). |
| EX-04 | **A user-scoped experiment is consistent across the user's devices**; a device-specific experiment uses installation assignment; workspace-level behaviour uses workspace assignment. |
| EX-05 | **Session assignment is permitted only for a very small class of pure presentation experiments.** Anything with persistence, cost or workflow consequence cannot be session-randomised. |
| EX-06 | **Experiments must never weaken security** (`I-351`). There is no A/B test of a security control. |
| EX-07 | **Experiments must never modify entitlement.** Commercial experiments are designed explicitly in the entitlement system. |
| EX-08 | **Experiments must never change an incompatible persistent format.** Variants stay inside one compatibility contract. |
| EX-09 | **An experiment may change a default; it may never override an explicit user choice.** A user who selected a model is not reset to Auto at each launch. |
| EX-10 | **An experiment ends** by promoting a winner or the baseline, and the flag is removed. The assignment snapshot is retained for analysis. |
| EX-11 | **Mutually exclusive groups and holdouts are supported**, so overlapping experiments do not confound each other. |
| EX-12 | **Assignments must be consistent across surfaces** — desktop, web and mobile — or carry an explicit compatibility layer. A user must not see variant A on desktop and variant B on the web for the same behaviour. |
| EX-13 | **Assignment data is minimised**, and **experiment metrics are not part of the policy data** — they are an analytics concern with their own consent and retention rules, and never include user content. |

---

## 10. Publication, distribution and staleness

### 10.1 Publication

| # | Requirement |
|---|---|
| PB-01 | **Authoring and published runtime are separate.** A draft is not a policy; only a published revision is. |
| PB-02 | **A published policy revision is immutable** (`I-369`). Its content never changes after publication. |
| PB-03 | Policy is distributed as a **Policy Bundle** — a coherent set applied **atomically**. A partially applied bundle is prohibited. |
| PB-04 | **Publication requires validation**: schema conformance, key ownership, prerequisite acyclicity, experiment allocation validity, compatibility version-range validity, and provider/model references resolving to real catalog entries. |
| PB-05 | **Publication requires a dry run** with cohort impact evaluation, so the blast radius is known before publication. |
| PB-06 | **Policy rollback is a new revision, not a deleted one** (`I-370`). Revision 102 remains in history; revision 103 restores the earlier behaviour. |
| PB-07 | The **policy bundle schema is itself versioned**. An older client safely ignores unknown *additive* policy. |
| PB-08 | **An unknown *critical* policy must not default to enabled in an older client.** Where a client cannot understand a critical policy, the corresponding cloud capability is blocked rather than silently permitted. |
| PB-09 | **Remote config keys have a lifecycle** — introduced, active, deprecated, removed — so the surface does not accumulate thousands of unowned keys. |

### 10.2 Distribution and staleness

| # | Requirement |
|---|---|
| DS-01 | **A policy push is invalidation and acceleration, not authority** (`I-367`). A realtime event is not persistent truth. |
| DS-02 | **A client must not depend on a realtime connection to obtain policy.** Realtime speeds up refresh; the authoritative fetch is a normal request. |
| DS-03 | **Last Known Good** is a first-class concept: the last successfully validated policy snapshot, used when the control plane is unreachable. **LKG ≠ current cloud truth** (`I-368`). |
| DS-04 | **With no LKG at all, built-in safe compiled defaults apply.** |
| DS-05 | **Staleness strategy is per policy class, not one global rule.** A cosmetic rollout may tolerate long staleness; a compatibility block may not. The server re-decides on the actual request in either case. |
| DS-06 | **It is an accepted fact that an offline client cannot receive a new kill switch.** This is exactly why cloud-side enforcement is mandatory (`KS-04`) and why a local security fix requires an update (`KS-05`). |
| DS-07 | **Policy expiry must never brick a local application.** An expired snapshot degrades cloud-dependent features; local-first operation continues. |
| DS-08 | **Policy time uses stable server semantics.** The server decision is authoritative; client clock skew must not change eligibility. |
| DS-09 | **Policy fetch must never block local startup or exit** (`LF-06`). |

### 10.3 Application timing

Every policy declares when a change takes effect:

| Timing | Meaning |
|---|---|
| **Immediate / Emergency** | Applies at once, including inside running work where the mode says so |
| **Next Invocation** | Applies to the next API or AI invocation |
| **Next Task / Run** | Running Tasks keep their snapshot |
| **Next Session** | Applies on the next authenticated session |
| **Next App Launch** | Applies on the next start |
| **Restart Required** | Explicitly requires a restart — and a kill switch may never be of this kind (`KS-06`) |

Configuration additionally declares **hot-change safety**: whether a value may change in place, or requires a drain of dependent work first.

### 10.4 Relationship to the task model

| # | Requirement |
|---|---|
| TS-01 | A Run **freezes the decision snapshot that actually affects it**, not the entire global policy object. |
| TS-02 | **Ordinary rollout changes do not affect started Tasks.** |
| TS-03 | **Emergency policy may override a run snapshot** — the single documented exception. |
| TS-04 | **Experiment assignment is snapshotted the same way**: a Run assigned variant B continues as B. |
| TS-05 | **A feature disabled while a Task is running** follows the kill-switch mode; the Task is not silently corrupted. |
| TS-06 | **An automation referencing a now-unavailable feature or model** enters Needs Attention with a specific reason; existing automations are not deleted, and may resume when availability returns. |

---

## 11. Explainability

| # | Requirement |
|---|---|
| EP-01 | **Every policy decision is explainable**: not merely "disabled", but which layer decided, which revision, and why. |
| EP-02 | **The user-visible reason is separate from developer diagnostics.** Internal rule expressions are never shown to users. |
| EP-03 | Reason categories are **unified and stable**, including at minimum: `Available`, `NotEnabledYet`, `TemporarilyUnavailable`, `DisabledByWorkspacePolicy`, `RequiresNewerVersion`, `BlockedVersion`, `UnsupportedByBinary`, `UnsupportedPlatform`, `PrerequisiteMissing`, `ProviderUnavailable`, `ModelRetired`, `EmergencyDisabled`. |
| EP-04 | **Policy reasons, entitlement reasons and security reasons are three separate vocabularies** (`SR-03`). |
| EP-05 | **An unavailable feature must be presented correctly, not merely hidden.** Where a user has existing data or history produced by a now-unavailable feature, that history stays legible. |
| EP-06 | **Hiding an entry point and disabling a capability are separate decisions.** Hiding the entry alone is not enforcement; enforcement is server-side. |
| EP-07 | **Catalog visibility is independent of availability.** A model may be visible-but-unavailable, or hidden-but-still-honoured for existing pins. |
| EP-08 | **Remote config must not rewrite the explanation of past user actions.** A task that ran variant A is forever recorded as A. |
| EP-09 | **A policy decision records the participating revisions** — every source that contributed — so any decision can be reconstructed later. |
| EP-10 | An effective decision may be **cached**, and the cache is invalidated on policy change. Cached decisions never survive a kill switch. |
| EP-11 | **The effective feature decision is a structured value**, not a compressed boolean: state, reason, source revision, applicable scope, and any grace deadline. |
| EP-12 | If a policy change invalidates the user's current selection, the product states what changed and what it will do — it does not silently substitute. |

---

## 12. Boundaries with other systems

| # | Statement |
|---|---|
| BN-01 | **Dynamic policy is not a general escape hatch from releasing code** (`I-372`). Code release is still required. Policy chooses among already-compiled, already-safe behaviours. |
| BN-02 | **This is a hard requirement under Native AOT** (**D-008**). The control plane distributes **data, never code**. There is no dynamic code loading, no remote script, and no runtime code generation on the policy path. |
| BN-03 | **Dynamic policy is not the architecture constitution** (`I-371`). |
| BN-04 | **Policy is not permission and not trust.** Extension trust authority and malicious-package handling belong to the security and trust-and-safety systems; policy may set an extension protocol minimum version and may restrict community feature availability, but it is not the extension trust database. |
| BN-05 | **A user's own document-level "Exclude from AI" is not a remote policy.** It is user/resource knowledge policy. A workspace product policy may add a restriction on top; the two combine restrictively, never permissively. |
| BN-06 | **Policy may set a minimum version for cloud search**, and local keyword search continues regardless. |
| BN-07 | The control plane is a **module of the cloud modular monolith** (**D-008**), not a microservice-first design, and it is **not on the critical path of ordinary business requests** — services evaluate against a cached published snapshot with atomic refresh. |

---

## 13. Domain model

```
FeatureId · FeatureDefinition · FeatureLifecycle · FeaturePrerequisite
FeatureAvailability · FeatureGate
RolloutDefinition · RolloutRule · RolloutSubject · RolloutAssignment
KillSwitch · KillSwitchMode
RemoteConfigKey · RemoteConfigDefinition · RemoteConfigValue
PolicyScope · PolicyRule · PolicyResolver · PolicyConstraint
PolicyDecision · PolicyReason · DecisionContext
PolicyBundle · PolicyBundleRevision · PolicySchemaVersion
PolicySnapshot · LastKnownGoodPolicy
CompatibilityPolicy · MinimumVersionPolicy · BlockedVersionRange · GracePeriod
ProviderAvailabilityPolicy · ModelAvailabilityPolicy · ModelLifecycleState
ExperimentDefinition · ExperimentVariant · ExperimentAssignment · ExperimentGroup · AssignmentUnit
PolicyApplicationTiming · PolicyStalenessMode
```

---

## 14. Acceptance scenarios

**Feature rollout** — a percentage rollout assigns deterministically; the same user resolves identically on every device and every evaluation.

**Workspace rollout** — a workspace-scoped rollout applies to every member consistently.

**Kill switch** — each mode behaves as declared: new invocations blocked, existing drained, stopped at a safe point, or reduced to read-only; no data is deleted; no restart is required; the cloud enforces it regardless of client state.

**Policy server failure** — the client uses Last Known Good; the product continues; cloud requests are still decided server-side.

**First offline start** — with no policy at all, built-in safe defaults apply and the product is fully usable locally.

**Remote config validation** — an out-of-range value is rejected or clamped, never applied; the compiled hard limit wins.

**User setting** — a policy-controllable setting shows as locked with its reason; a non-controllable setting cannot be remotely forced.

**Workspace constraint** — a workspace restriction cannot be bypassed locally, and cannot re-enable something the platform denies.

**Entitlement separation** — a plan-limited capability reports an entitlement reason, never a policy reason.

**Temporary availability** — a temporarily disabled capability reports `TemporarilyUnavailable`, distinct from `RequiresNewerVersion`.

**Runtime health** — an unreachable dependency reports a health reason, not a policy reason.

**Minimum version** — a below-minimum client is warned during the grace period, then blocked from the specific capability while local work continues.

**Blocked bad version** — one specific build is blocked while both neighbours are allowed.

**Cloud sync blocked** — the client can still open, edit, export and recover locally, with an actionable message.

**Model pinning** — a pinned model is never silently substituted; on retirement the user is asked.

**Auto model** — auto routes inside its class and cost ceiling.

**Emergency model suspension** — future invocations inside a running Run are interrupted per the declared mode.

**Experiment** — sticky assignment across devices; ending promotes a winner and removes the flag.

**Prohibited experiments** — a security experiment and an incompatible-format experiment are both rejected at publication validation.

**Policy rollback** — restoring earlier behaviour creates a new revision; history shows both.

**Partial capability policy** — one capability is disabled while the rest of the product continues.

**Existing feature data** — data created by a now-disabled feature remains readable and exportable.

**Automation** — an automation blocked by policy enters Needs Attention with a specific reason and is not deleted.

**Self-host** — a self-hosted realm applies its own policy authority and is not governed by official product policy.

---

## 15. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 25` | The entire control plane: the four boundaries, feature and flag model, rollout, kill switch, remote config, policy scope and resolution, workspace policy, compatibility policy, provider and model availability, experiments, publication and staleness, application timing, explainability, and the non-goals |
| `I4 §Stage 27` | Version and compatibility vocabulary shared with the quality contract |
| `I4 §Stage 19` | Run snapshot semantics for policy and experiment assignment |
| `I4 §Stage 8` | Model and provider catalogue relationship; pricing stays in the commercial layer |
| **D-008** | The control plane distributes data, never code — required by the Native AOT desktop main path |
| **D-020** | Pricing is versioned commercial policy, not remote product policy |
