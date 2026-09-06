# Phase 2 Specification Decisions

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Decisions
> Governing authority: **D-001** (conflict-resolution rule), **D-016** (deferred-decision ownership), **D-019** (sequence status)
> Companions: [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

Phase 1 froze twenty-three foundation decisions. **They are binding and are not reopened here.** This register records only what Phase 2 had to decide that is *not* derivable from them.

The bar for entry is deliberately high. A conclusion already stated in the preserved input corpus, or already implied by a Phase 1 decision, is implemented in the requirements, architecture or planning layers with a citation — it does not become a decision record. Five entries exist: four in force, and one withdrawn and retained as the record of a corrected error.

---

## Register conventions

| Field | Meaning |
|---|---|
| **Status** | `ADOPTED` — decided and in force · `DEFERRED` — deliberately left open with an owner, a trigger and a binding constraint · `WITHDRAWN` — recorded in error, normative content removed, entry retained so the correction is auditable |
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

## P2-002 — Sequence derivation under D-019 · `WITHDRAWN — SUPERSEDED BY P2-004`

> **This entry was wrong and is retained as the record of the error, not as authority.** Its normative content is withdrawn. The governing entry is `P2-004`.

**What it decided.** That the numbered work-package sequence would be derived **before** the per-product Reference Coverage Matrices and the item-level code inventory existed, with those audits scheduled inside the sequence and later packages rewritten if a finding invalidated them (`DC-01`–`DC-04`).

**Why it was wrong.** **D-019** states that the implementation plan *must be derived after* requirements, architecture, licence matrices and current-code reconciliation are complete. **D-012** states that every product must receive a Reference Coverage Matrix *before implementation planning for that product is finalized*. Both are `USER_CONFIRMED` and binding.

P2-002 substituted a different process — derive first, audit during implementation, rewrite after findings — and presented that substitution as satisfying **D-019**. It did not. A Phase 2 decision may not alter a Phase 1 decision's ordering requirement, and `RC-01` of this register already says so. The entry contradicted the rule under which it was recorded.

**What the substitution cost.** It was not a formality. Producing the prerequisite evidence afterwards surfaced findings that would have changed the plan:

| Finding | Where | What the sequence had assumed |
|---|---|---|
| Four of six accessible references are GPL-family, proprietary or AGPL; **no reuse is possible from any of them** | [`../assurance/reference-coverage/README.md`](../assurance/reference-coverage/README.md) `§Aggregate licence position` | That per-product licence audits might clear material for reuse, making `Copy`/`Port` dispositions plausible downstream |
| Neither ArcNotes reference implements slides | [`arcnotes-affine-siyuan.md`](../assurance/reference-coverage/arcnotes-affine-siyuan.md) `F-AN-2` | That `WP-29` would have reference oracles like its sibling packages |
| Serial-Studio's licence creates an **authorship boundary**, not only a reuse prohibition | [`arcscope-serial-studio.md`](../assurance/reference-coverage/arcscope-serial-studio.md) `F-AS-1` | That the whole reference was readable evidence |
| The implementation repository has **166 projects and 8,638 C# lines**, not 332 projects of substance | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) `§3` `C-01`, `C-02` | A materially different starting position |
| Four of six recorded conformance findings were false | there, `C-03`–`C-06` | `WP-02` and `WP-05` scoped larger than the evidence supports |
| The cloud three-role separation does not exist | there, `§5.5` | Not identified at all — a new priority-3 item |
| Olive was **not present** at the authorized location, which the plan had assumed | [`arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md) | That all registered ArcSlate references were available. **Resolved by `P2-005`**: the reference map is amended and ArcVideo plus ArcVideoFoundation are the baselines |

`DC-04` anticipated rewriting "a package"; the evidence in fact changed package scope, priority order and one open question requiring the user's decision. Deriving first did not make the dependency structure visible — it made a **provisional** structure look settled.

**Status of everything it produced.** The sequence derived under P2-002 was **provisional**, not a validly derived implementation plan. `P2-004` records its re-derivation from the completed evidence and the specific changes that followed.

**Withdrawn on.** 2026-09-05, during the Stage 2 repair and closure pass.

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

## P2-004 — Sequence derivation from completed prerequisite evidence · `ADOPTED`

**Decision.** The implementation sequence is derived from the completed prerequisite evidence, in the ordering **D-019** and **D-012** require. The prerequisite evidence is:

| Prerequisite | Artifact | State |
|---|---|---|
| Requirements | [`../requirements/`](../requirements/README.md) | Complete |
| Architecture | [`../architecture/`](../architecture/README.md) | Complete |
| Licence matrices — per product, per **D-012** | [`../assurance/reference-coverage/`](../assurance/reference-coverage/README.md) — five matrices, 145 item-level rows | **Complete.** The one unresolved determination it carried was closed by `P2-005` |
| Current-code reconciliation | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) — 166 projects, item-level | **Complete** |

**Ordering, stated plainly.** Requirements and architecture, then licence matrices and code reconciliation, **then** the plan. That is **D-019**'s ordering and it is now followed rather than substituted.

**Consequences.**

- `DD-01`: **The sequence is derived, not provisional.** Every package's scope rests on evidence that existed before it was written.
- `DD-02`: **The baseline matrices and the inventory are versioned planning inputs.** Implementation packages consume them. No implementation package re-creates a baseline audit.
- `DD-03`: **Implementation packages retain drift checks only** — source drift against the recorded commit, changed scope, and newly introduced material. Baseline creation and later maintenance are different obligations and are not conflated.
- `DD-04`: **Where evidence changed a package, the change is recorded** with its evidence, the affected statement, the correction, downstream consumers and the verification needed — in [`../planning/evidence-driven-revisions.md`](../planning/evidence-driven-revisions.md).
- `DD-05`: **No unresolved determination remains.** The one that existed — `OC-01`, the ArcSlate reference baseline — was closed by user decision on 2026-09-05 and is recorded as `P2-005`.
- `DD-06`: **`DC-01`–`DC-04` are withdrawn with P2-002.** They described the substituted process.

**Authority.** Product Owner, with the Architecture Owner and the Licensing and Provenance Owner.

**Consumed by.** [`../planning/implementation-sequence.md`](../planning/implementation-sequence.md) `§1.1`; [`../planning/work-packages/README.md`](../planning/work-packages/README.md); [`../planning/evidence-driven-revisions.md`](../planning/evidence-driven-revisions.md); every work package's Required Inputs.

**Reversal cost.** Not applicable — this is the ordering Phase 1 already confirmed. It is followed, not chosen.

---

## P2-005 — ArcSlate reference baseline: ArcVideo and ArcVideoFoundation · `ADOPTED`

**Decision (user, 2026-09-05).** **ArcSlate's direct reference repositories are ArcVideo and ArcVideoFoundation. There is no requirement to obtain or independently review an Olive repository.**

**Basis.** Olive could not be built in the user's environment. ArcVideo contains the modifications made to get that codebase building, and ArcVideo and ArcVideoFoundation are the intended concrete reference baselines. The concrete, buildable fork is the reference of record; the unbuildable upstream is not.

**Why this is a decision and not an inference.** **D-012** registered Olive explicitly. Dropping it is a scope decision that only the Product Owner can take — which is why the Stage 2 repair recorded it as `OC-01` and did not resolve it locally.

**Consequences.**

- `RB-01`: **D-012's reference map is amended.** The verbatim decision block is preserved per this register's supersession convention; the current effective ArcSlate line is *"ArcVideo and ArcVideoFoundation → ArcSlate references"* ([`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) §D-012 amendment; applied-disposition row 31).
- `RB-02`: **The Olive-direct audit scope is removed.** No obligation exists to obtain Olive's independent tests, fixtures, source or licence file. The missing-repository blocker is withdrawn.
- `RB-03`: **ArcSlate's reference coverage, planning and verification evidence rest on the actual ArcVideo and ArcVideoFoundation repositories**, at commits `caf5651` and `139eeca`.
- `RB-04`: **Olive-origin provenance is preserved, not erased.** ArcVideo is a documented fork of Olive. Its **GPL-3.0 obligations, upstream copyright and attribution run to the Olive authors**, and every notice, licence header and provenance record that inherited material requires is retained (**D-013**). Removing Olive as an independent reference does not authorise removing its provenance, and no row in any matrix does so.
- `RB-05`: **Preserved raw inputs are unchanged.** `I2 §II` and `I4 §Stage 20` still discuss Olive as historical evidence; this decision is recorded outside them and does not rewrite them.
- `RB-06`: **`OC-01` is closed.** No unresolved determination remains in the Phase 2 register.

**What does not change.** ArcSlate remains an **original implementation**. Both references are **GPL-3.0-only**, so **D-013** still prohibits copying, translating or porting from either; every matrix row remains `Reference Only` or an accepted exclusion. Removing Olive narrows the *audit* scope, not the *reuse* prohibition.

**Authority.** Product Owner (this decision), with the Licensing and Provenance Owner for `RB-04`.

**Consumed by.** [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) §D-012 amendment; [`../assurance/reference-coverage/arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md); [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md) §1.1, §2.2, §7; [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md) §6; [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md) §1; [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md) §9; `WP-36`.

**Reversal cost.** Low. Should an Olive checkout later become available and be wanted, it is added to the reference map and the ArcSlate matrix is extended; nothing built on this decision would need to be undone.

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

### OC-01 — ArcSlate reference baseline · `CLOSED 2026-09-05`

| Field | Position |
|---|---|
| **Was** | **D-012** registered Olive as an ArcSlate reference; no Olive repository existed at the authorized reference-map location |
| **Resolution** | **User decision, 2026-09-05**: ArcSlate's direct reference repositories are **ArcVideo and ArcVideoFoundation**; there is no requirement to obtain or independently review an Olive repository. Recorded as `P2-005`, and applied to **D-012** as a dated amendment |
| **Effect** | The Olive-direct audit scope and the missing-repository blocker are removed. ArcSlate's evidence rests on the two actual repositories at commits `caf5651` and `139eeca` |
| **Not removed** | **Olive-origin provenance.** ArcVideo is a documented fork; GPL-3.0 obligations, upstream copyright and attribution to the Olive authors are preserved wherever inherited material requires them (`RB-04`) |
| **State** | **Closed.** No unresolved determination remains in the Phase 2 register |

---

### Tensions resolved without escalation

Four further tensions were resolvable within the authority Phase 1 already granted. Each resolution is recorded where it applies:

| Tension | Resolution | Recorded in |
|---|---|---|
| **D-019** requires the plan to follow audits that did not exist | **Not resolvable by substitution** — the earlier attempt is withdrawn. The audits were produced, then the plan was re-derived | `P2-002` (withdrawn) and `P2-004` above |
| The existing monorepo's state differs materially from any assumption | Item-level reconciliation with per-project dispositions; the plan adapts to measured evidence | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) |
| Two native shims may fall outside the permitted native surface | `Fence` with a scheduled substitute analysis per shim, rather than a global judgement | there, `§5.2` `NS-07`, `NS-08` |
| Every commercial figure in the corpus is a proposal, not a commitment | Recorded as versioned commercial policy with corpus defaults labelled proposals (**D-020**); no figure has been consumed as an authoritative specification | [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md); [`../assurance/commercial-figure-status.md`](../assurance/commercial-figure-status.md) |

Should implementation surface a further material conflict, **D-001** governs: the work stops, the conflict is registered, and it is returned for decision rather than resolved locally.
