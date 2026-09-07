# Architecture Decisions

This directory records Architecture Decision Records (ADRs) for significant structural, technology, and architectural choices across the ArcForges project.

## Active

- [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) — Phase 1 foundation decision register. Records every material issue found in the closed Phase 1 input corpus and the user decisions that resolve them. Only genuinely user-confirmed decisions are recorded as accepted. **[D-001](phase-1-foundation-decisions.md#rule-d-001) … [D-023](phase-1-foundation-decisions.md#rule-d-023) remain binding as explicitly amended by subsequent user direction; see [P2-006](phase-2-specification-decisions.md#rule-p2-006) and the Web amendment [P2-008](phase-2-specification-decisions.md#rule-p2-008) (2026-09-06).**
- [phase-2-specification-decisions.md](phase-2-specification-decisions.md) — Install/update baseline ([P2-001](phase-2-specification-decisions.md#rule-p2-001)), adopted browser cookie-session deployment ([P2-003](phase-2-specification-decisions.md#rule-p2-003)), sequence correction ([P2-004](phase-2-specification-decisions.md#rule-p2-004), superseding withdrawn [P2-002](phase-2-specification-decisions.md#rule-p2-002)), ArcSlate reference amendment ([P2-005](phase-2-specification-decisions.md#rule-p2-005)), and the current user-directed requirements revision ([P2-006](phase-2-specification-decisions.md#rule-p2-006)). Prior coverage/completion applies to its recorded baseline only.

## Conventions

- A conclusion already stated in the preserved input corpus, or already implied by a Phase 1 decision, is implemented in the requirements, architecture or planning layer **with a citation** — it does not become a decision record.
- A deferred decision carries an owner, a trigger and the constraint every permitted option must satisfy — never a bare "decide later" (**[D-016](phase-1-foundation-decisions.md#rule-d-016)**).
- A decision recorded here is cited inline wherever it is implemented, exactly as Phase 1 decisions are.
- Authors may not silently contradict Phase 1. Subsequent explicit user decisions take precedence under **[D-001](phase-1-foundation-decisions.md#rule-d-001)** and require a dated amendment; [P2-006](phase-2-specification-decisions.md#rule-p2-006) records the current requirements revision.

## Current requirements revision

[P2-006](phase-2-specification-decisions.md#rule-p2-006) governs the cloud subscription baseline. Its requirements and downstream reconciliation are recorded in the existing Stage 2 closure evidence; the subsequent Web amendment is governed by [P2-008](phase-2-specification-decisions.md#rule-p2-008) and the [Web redesign review](../assurance/web-typescript-redesign-review.md).


[P2-008](phase-2-specification-decisions.md#rule-p2-008) is the current Web decision: React/TypeScript with Node/npm, C#-generated OpenAPI/TS SDK, win.slnx/esproj and portable directory workflows. It supersedes the original [D-007](phase-1-foundation-decisions.md#rule-d-007) Web technology and resolves [P2-003](phase-2-specification-decisions.md#rule-p2-003); preserved inputs remain historical evidence.
