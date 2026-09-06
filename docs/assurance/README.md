# Assurance

This directory defines criteria and specifications for quality, safety, security, compatibility, and production readiness across ArcForges designs.

## Phase 1 — foundation record

- [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md) — Phase 1 complete-reading coverage and topic-inventory ledger for the closed design-input corpus, with the deferred-gate register and Foundation Freeze gate status.
- [`phase-1-official-verification.md`](phase-1-official-verification.md) — Phase 1 official verification record. Verifies the foundation-critical external claims that Phase 1 decisions depend on, against current official primary sources: regulatory applicability, protocol specification status, runtime and AOT posture, dependency AOT evidence, payment-provider role and capability, payout relationship, and mobile-storefront commerce rules. Findings V-01 to V-09, each with source, source date, verification date, result, architectural consequence, and any required implementation-time proof or go-live gate.

Prices, fees, quotas and rates are deliberately **not** verified in these artifacts; they are deferred under D-003's first-consumption rule with a named owner and trigger.

## Phase 2 — assurance specifications

| Document | Covers |
|---|---|
| [`testing-and-verification-strategy.md`](testing-and-verification-strategy.md) | The eighteen test families with their unique responsibility, placement and evidence; cross-cutting verification themes; the invariant-to-test obligation; test environments; fixtures and corpora; verification of the specification itself; and what each family may not substitute for |
| [`release-gates.md`](release-gates.md) | Every gate between work and users, consolidated: continuous, per-release, channel-promotion, product first-release, go-live (cloud, commercial, regional, mobile, extension) and deferred-gate closure — each with evidence and an accountable role |
| [`open-gates-register.md`](open-gates-register.md) | The single gate register, separated into design-stage and implementation-stage classes: three deferred gates from Phase 1, twelve from the official verification record, eleven from Phase 2 — each with owner, trigger, what it blocks and its satisfying package. Four are closed by design evidence; the rest are legitimate future obligations. Also carries the one unresolved determination |
| [`reference-coverage-and-provenance.md`](reference-coverage-and-provenance.md) | **The method**: the reference map and what a reference repository is not; the matrix columns; the ten-field provenance record required by D-013; the licence decision table; automated enforcement; and verification oracles. The completed matrices are in [`reference-coverage/`](reference-coverage/README.md) |
| [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) | **The completed item-level inventory**: 166 projects with measured content and dispositions, six corrections to earlier false conformance findings, per-shim native reconciliation, the effective build configuration, the measured test harness, and the revised priority order |
| [`traceability-matrix.md`](traceability-matrix.md) | Decision-to-document, verification-to-enforcement, requirement-to-architecture-to-test, and invariant coverage mappings |
| [`reference-coverage/`](reference-coverage/README.md) | **The five completed Reference Coverage Matrices** required by D-012 — ArcChat/AionUi, ArcNotes/AFFiNE+SiYuan, ArcScope/Serial-Studio, ArcSlate/ArcVideo+ArcVideoFoundation, distribution/StartArcForges. 145 item-level rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, verification oracle and owner |
| [`invariant-coverage.md`](invariant-coverage.md) | The D-018 obligations separated: design completeness (484 of 484 corpus statements accounted for), design traceability (421 of 421 invariants mapped item-level), and implementation evidence (deliberately not claimed) |
| [`commercial-figure-status.md`](commercial-figure-status.md) | Evidence that no commercial figure has been consumed as an authoritative specification, and that no price, rate or tariff exists in the authoritative layers |
| [`end-to-end-workflow-verification.md`](end-to-end-workflow-verification.md) | **Five boundary-crossing workflows traced step by step** — remote agent edit from mobile, purchase then immediate use, offline edits on two devices, budget exhausted mid-turn, and a PDF that will not render — each followed to a terminal state on both the success and the failure path, with every step resolved against a named operation, schema or rule. Three findings, all closed |

## Conventions

- Every gate has an owner, a trigger, a statement of what it blocks, and a named evidence artifact. A gate that depends on someone remembering is not a gate.
- **Design-stage gates close on design evidence; implementation-stage gates never do.** Four gates — `F-013`, `PG-01`, `PG-02`, `PG-06` — are closed by artifacts in this directory. The remaining twenty-two require execution evidence and are scheduled, not closed.
- **Registering an open finding never closes a gate.** Where accounting and enforcement are both needed they are separate gates with separate evidence (`PG-06` versus `PG-11`).
- Citations use **D-nnn** for Phase 1 decisions, **V-nn** for verification findings, and **F-nnn** for deferred gates.
