# Architecture Decisions

This directory records Architecture Decision Records (ADRs) for significant structural, technology, and architectural choices across the ArcForges project.

## Active

- [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) — Phase 1 foundation decision register. Records every material issue found in the closed Phase 1 input corpus and the user decisions that resolve them. Only genuinely user-confirmed decisions are recorded as accepted. **D-001 … D-023 are binding and are not reopened.**
- [`phase-2-specification-decisions.md`](phase-2-specification-decisions.md) — Phase 2 specification decisions. Records only what Phase 2 had to decide that is not derivable from Phase 1: the desktop install and update infrastructure baseline (`P2-001`), the sequence derivation under D-019 (`P2-002`), and the deliberately deferred browser token-handling deployment with its binding constraint (`P2-003`). It also records what was considered and deliberately *not* recorded, and states that no open material conflict requires a user decision.

## Conventions

- A conclusion already stated in the preserved input corpus, or already implied by a Phase 1 decision, is implemented in the requirements, architecture or planning layer **with a citation** — it does not become a decision record.
- A deferred decision carries an owner, a trigger and the constraint every permitted option must satisfy — never a bare "decide later" (**D-016**).
- A decision recorded here is cited inline wherever it is implemented, exactly as Phase 1 decisions are.
- No Phase 2 decision may contradict a Phase 1 decision. Where one appears to, the Phase 1 decision governs and the Phase 2 text is a defect (**D-001**).
