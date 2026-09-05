# Phase 2 Specification Decisions

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Decisions
> Governing authority: **D-001** (conflict-resolution rule), **D-016** (deferred-decision ownership), **D-019** (sequence status)
> Companions: [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

Phase 1 froze twenty-three foundation decisions. **They are binding and are not reopened here.** This register records only what Phase 2 had to decide that is *not* derivable from them.

The bar for entry is deliberately high. A conclusion already stated in the preserved input corpus, or already implied by a Phase 1 decision, is implemented in the requirements, architecture or planning layers with a citation — it does not become a decision record. Three items met the bar.

---

## Register conventions

| Field | Meaning |
|---|---|
| **Status** | `ADOPTED` — decided and in force · `DEFERRED` — deliberately left open with an owner, a trigger and a binding constraint |
| **Authority** | Who may change it |
| **Consumed by** | Where it is implemented and enforced |

| # | Rule |
|---|---|
| RC-01 | **A Phase 2 decision may not contradict a Phase 1 decision.** Where it appears to, the Phase 1 decision governs and the Phase 2 text is a defect (**D-001**). |
| RC-02 | **A decision recorded here is cited inline wherever it is implemented**, exactly as Phase 1 decisions are. |
| RC-03 | **A deferred decision carries an owner, a trigger and the constraint every permitted option must satisfy** — never a bare "decide later". |
| RC-04 | **Adding to this register requires the same discipline as Phase 1**: a real decision, a stated consequence, and a named enforcement mechanism. |

---

## P2-001 — Install and update infrastructure baseline · `ADOPTED`

**Decision.** A single cross-platform install and update framework is the baseline for the four desktop products on Windows, macOS and Linux. The preserved corpus records this choice explicitly (`I4 §Stage 5 §4`), and Phase 2 adopts it as the implementation baseline with three qualifications:

1. **It sits behind a thin build-script and integration boundary.** Product code never references the framework's types outside one update-integration component, so the framework can be replaced without touching product code.
2. **The product's own update system remains authoritative across every distribution channel.** A platform store or package manager delivers the same signed installer; it does not become the update mechanism.
3. **It consumes the publish output directory and requires no machine-installed runtime.** This is what makes it compatible with the Native AOT desktop posture (**D-008**).

**Why this is a Phase 2 decision.** Phase 1 decided the runtime matrix (**D-008**), the distribution surfaces (**D-014**) and the mobile commerce posture (**D-022**), but never the desktop install and update mechanism. Implementation cannot proceed without it, and the choice constrains packaging, signing, the update feed, delta updates, channel switching and rollback across three platforms.

**Consequences.**

- Windows uses a per-user installer requiring no elevation; a machine-wide package may be added later for enterprise need.
- A store listing carries the **same signed installer**, not a repackaged container.
- Linux ships **one** self-contained portable format first; multiple packaging formats are not maintained simultaneously in the first stage.
- Delta updates, three release channels, self-hosted update sources and downgrade are available from the framework rather than built.

**Authority.** Architecture Owner, with the Release Engineering Owner.

**Consumed by.** [`../architecture/14-build-packaging-and-release.md`](../architecture/14-build-packaging-and-release.md) `§5`; [`../requirements/10-distribution-update-and-support.md`](../requirements/10-distribution-update-and-support.md) `§1`–`§3`; work packages `02`, `50`.

**Reversal cost.** Moderate before the first public release, high afterwards — an installed base's update path is not easily migrated. The abstraction boundary in qualification 1 exists specifically to keep this cost bounded.

---

## P2-002 — Sequence derivation under D-019 · `ADOPTED`

**Decision.** The numbered work-package sequence is derived **now**, with the packages that produce the per-product licence matrices and the item-level code inventory placed at the front of the sequence, gating every downstream product package.

**Why this is a Phase 2 decision.** **D-019** requires the implementation plan to be derived *after* requirements, architecture, licence matrices and current-code reconciliation are complete. Requirements and architecture are complete; the licence matrices and the item-level inventory are not, because producing them means reading reference repositories and several hundred project files item by item — implementation-planning work, not specification work.

Two readings were possible: withhold the sequence until those audits exist, or derive it now with the audits scheduled inside it. Phase 2 chose the second, because the first would leave the dependency structure invisible and the audits themselves unscheduled — the precise failure **D-019** exists to prevent.

**Consequences.**

- `DC-01`: the audit-producing packages (`00`, `01`, and each product's reference audit) sit at the front and their gates block downstream work.
- `DC-02`: no product implementation package begins before its Reference Coverage Matrix and licence audit are complete (**D-012**, **D-013**).
- `DC-03`: no restructuring begins before the item-level inventory exists.
- `DC-04`: **if a matrix or the inventory produces a finding that invalidates a later package's scope, that package is rewritten before work continues on it** (**D-001**). The sequence is derived, not frozen against evidence not yet gathered.

**Authority.** Product Owner, with the Architecture Owner.

**Consumed by.** [`../planning/implementation-sequence.md`](../planning/implementation-sequence.md) `§1.1`; [`../planning/work-packages/README.md`](../planning/work-packages/README.md); work packages `00`, `01`.

**Reversal cost.** Low. Rewriting a package before it starts is cheap; `DC-04` makes that the expected path rather than an exception.

---

## P2-003 — Browser token-handling deployment · `DEFERRED`

**Decision.** The concrete browser token-handling deployment — a cookie-based backend-for-frontend versus in-memory access tokens with a short lifetime — is **deliberately not decided in Phase 2**. It is deferred to implementation with a binding constraint that every permitted option must satisfy.

**The binding constraint.** **A long-lived access token is never held in storage readable by arbitrary scripts.** Whichever deployment is chosen must satisfy this, together with: short-lived access tokens with refresh rotation and revocation; serialised refresh so concurrent requests never storm; per-origin cookie, cross-origin and request-forgery posture with **no broad parent-domain authentication cookie** (**D-015**); and a web session that is shorter-lived and less trusted than a desktop session.

**Why this is deferred rather than decided.** Both options satisfy the security requirement, and the choice between them turns on operational facts that do not exist yet — the edge and hosting topology, the cost of an additional server-side component per origin, and measured refresh behaviour under real load. Deciding it now would be a guess presented as an architecture.

**Why it is recorded rather than left silent.** An undecided item that is not written down becomes an accidental decision made by whoever writes the code first. **D-016** requires deferred decisions to carry an owner and a trigger; this one does.

**Owner.** Architecture Owner, with the Security and Privacy Owner.

**Trigger.** Before the account portal's authentication implementation begins — work package `48`, sub-step `48.01`.

**Blocks.** `WP-48.01`. The package cannot complete its gate without the decision being made and recorded.

**Consumed by.** [`../architecture/10-web-architecture.md`](../architecture/10-web-architecture.md) `§5` (`AU-02`, `AU-03`); work package `48`.

**On resolution.** The chosen deployment is recorded as an amendment to this entry with its status changed to `ADOPTED`, and the constraint above becomes a test in `WP-48.01`.

---

## What was considered and deliberately not recorded

Recording a non-decision as a decision is as harmful as leaving a decision unrecorded. These were considered and rejected for entry, with the reason:

| Considered | Why it is not a Phase 2 decision |
|---|---|
| The dual capability boundary for extensions | Stated in the preserved corpus (`I4 §Stage 24 §67`–`§73`); implemented in [`../architecture/15-extension-platform-architecture.md`](../architecture/15-extension-platform-architecture.md) `§4` with citations |
| Three cloud runtime roles | Derivable from the modular monolith and isolated-job requirements; implemented in [`../architecture/05-cloud-architecture.md`](../architecture/05-cloud-architecture.md) `§2` |
| The eighteen test families | A design output of the quality contract, not a choice between alternatives |
| Native shims beyond the architecture's illustrative two | Governed by the permitted-surface rule (`NP-01`) and resolved per shim in `WP-01.03`; not a global decision |
| An isolated extension host | Already governed by **D-016** and the closed technical exception list; raising one is a future decision, not a present one |
| The eleven-phase reading structure of the sequence | Presentation of a dependency graph, not a decision |
| Cloud module count reconciliation | A reconciliation finding for `WP-21.02`, resolved with evidence rather than by decree |

---

## Open material conflicts requiring a user decision

**None.**

Phase 2 encountered four tensions that could have required a user decision. Each was resolvable within the authority Phase 1 already granted, and each resolution is recorded where it applies rather than escalated:

| Tension | Resolution | Recorded in |
|---|---|---|
| **D-019** requires the plan to follow audits that do not yet exist | Derive the sequence now with the audits scheduled at its front and `DC-04` permitting rewrite on finding | `P2-002` above |
| The existing monorepo is substantially more advanced than a greenfield sequence assumes | Reconciliation with per-item dispositions including `Keep`; the sequence adapts to what exists rather than discarding it | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) |
| The existing native surface is broader than the architecture's illustration | Permitted-surface decision per shim, with licence review, in `WP-01.03` | [`../architecture/12-native-interop-and-media.md`](../architecture/12-native-interop-and-media.md) `§2` |
| Every commercial figure in the corpus is a proposal, not a commitment | Recorded as versioned commercial policy with corpus defaults labelled proposals (**D-020**) | [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md) |

Should implementation surface a genuine material conflict, **D-001** governs: the work stops, the conflict is registered, and it is returned for decision rather than resolved locally.
