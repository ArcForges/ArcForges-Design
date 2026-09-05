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
| [`open-gates-register.md`](open-gates-register.md) | The single register of open gates: the three deferred gates carried from Phase 1, the twelve created by the official verification record, and the ten created by Phase 2 — each with owner, trigger, what it blocks, and the work package that must satisfy it |
| [`reference-coverage-and-provenance.md`](reference-coverage-and-provenance.md) | The reference map and what a reference repository is not; the per-product Reference Coverage Matrix and its columns; the ten-field provenance record required by D-013; the licence decision table; automated enforcement; verification oracles; and the F-013 gate |
| [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) | The reconciliation method and dispositions; the observed first-pass inventory of the existing monorepo; conformance findings against this specification; priority order; the rules that constrain outcomes; and the gate that must pass before restructuring begins |
| [`traceability-matrix.md`](traceability-matrix.md) | Decision-to-document, verification-to-enforcement, requirement-to-architecture-to-test, and invariant coverage mappings |

## Conventions

- Every gate has an owner, a trigger, a statement of what it blocks, and a named evidence artifact. A gate that depends on someone remembering is not a gate.
- **Phase 2 schedules gates; it does not close them.** No gate in [`open-gates-register.md`](open-gates-register.md) is marked closed by a specification document.
- Citations use **D-nnn** for Phase 1 decisions, **V-nn** for verification findings, and **F-nnn** for deferred gates.
