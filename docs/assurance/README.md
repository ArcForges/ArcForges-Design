# Assurance

This directory defines criteria and specifications for quality, safety, security, compatibility, and production readiness across ArcForges designs.

The [deprecated input archive](../deprecated-inputs/README.md) is excluded from ongoing design-completeness audits. Completed input-reading and extraction records are historical provenance, not a new audit denominator or an obligation to repeat input review. The current invariant catalogue, its design/implementation obligations and reference-source review remain in scope under the effective design.

## Current design review

[Cloudflare and application assistants](cloudflare-app-assistants-review.md) records the [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) closure matrix, final corrections, document validation and remaining real implementation gates. Earlier dated reviews retain their original evidence baselines.

## Phase 1 — foundation record

- [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md) — Historical Phase 1 input-reading coverage and topic inventory, with the deferred-gate register and Foundation Freeze status recorded at that baseline. It does not reopen review of the deprecated inputs.
- [`phase-1-official-verification.md`](phase-1-official-verification.md) — Phase 1 official verification record. Verifies the foundation-critical external claims that Phase 1 decisions depend on, against current official primary sources: regulatory applicability, protocol specification status, runtime and AOT posture, dependency AOT evidence, payment-provider role and capability, payout relationship, and mobile-storefront commerce rules. Findings [V-01](phase-1-official-verification.md#rule-v-01) to [V-09](phase-1-official-verification.md#rule-v-09), each with source, source date, verification date, result, architectural consequence, and any required implementation-time proof or go-live gate.

Prices, fees, quotas and rates are deliberately **not** verified in these artifacts; they are deferred under [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)'s first-consumption rule with a named owner and trigger.

## Phase 2 — assurance specifications

| Document | Covers |
|---|---|
| [ci-and-local-validation-policy.md](ci-and-local-validation-policy.md) | P2-017 execution authority: retained build/offline/security/signing checks, prohibited macOS/hosted runtime CI and redundant public verification, local opt-in coverage and bounded post-merge completion |
| [`testing-and-verification-strategy.md`](testing-and-verification-strategy.md) | The eighteen test families with their unique responsibility, placement and evidence; cross-cutting verification themes; the invariant-to-test obligation; test environments; fixtures and corpora; verification of the specification itself; and what each family may not substitute for |
| [`release-gates.md`](release-gates.md) | Every gate between work and users, consolidated: continuous, per-release, channel-promotion, product first-release, go-live (cloud, commercial, regional, mobile, extension) and deferred-gate closure — each with evidence and an accountable role |
| [open-gates-register.md](open-gates-register.md) | The authoritative current register of design closures, candidate-specific implementation evidence, remaining implementation obligations, retired/merged entries and owner determinations |
| [`reference-coverage-and-provenance.md`](reference-coverage-and-provenance.md) | **The method**: the reference map and what a reference repository is not; the matrix columns; the ten-field provenance record required by [D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013); the licence decision table; automated enforcement; and verification oracles. The completed matrices are in [`reference-coverage/`](reference-coverage/README.md) |
| [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) | **The completed item-level inventory**: historical166 projects at ede43db with measured content and dispositions, six corrections to earlier false conformance findings, per-shim native reconciliation, the effective build configuration, the measured test harness, and the revised priority order |
| [`traceability-matrix.md`](traceability-matrix.md) | Decision-to-document, verification-to-enforcement, requirement-to-architecture-to-test, and invariant coverage mappings |
| [`reference-coverage/`](reference-coverage/README.md) | **The five completed Reference Coverage Matrices** required by [D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012) — ArcChat/AionUi, ArcNotes/AFFiNE+SiYuan, ArcScope/Serial-Studio, ArcSlate/ArcVideo+ArcVideoFoundation, distribution/StartArcForges. 145 item-level rows, each with evidence location, source commit, requirement or exclusion, disposition, rationale, licence position, verification oracle and owner |
| [`invariant-coverage.md`](invariant-coverage.md) | The [D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018) obligations separated: completed historical input accounting (484 statements), current design traceability (**429 of 429** invariants mapped item-level), and implementation evidence (deliberately not claimed) |
| [`commercial-figure-status.md`](commercial-figure-status.md) | Evidence that no commercial figure has been consumed as an authoritative specification, and that no price, rate or tariff exists in the authoritative layers |
| [end-to-end-workflow-verification.md](end-to-end-workflow-verification.md) | Current success/failure traces across Notes, sync, migration, transactions, billing, provider effects, streams, isolation, media and real implementation prerequisites |
| [phase-2-design-closure-review.md](phase-2-design-closure-review.md) | Fourteen review groups, final mechanisms, owning work packages and the boundary between design closure and runtime proof |
| [design-repair-verification.md](design-repair-verification.md) | Reproducible standard-library design counterexamples and complete citation/dependency checks |
| [deprecated-input-independence-review.md](deprecated-input-independence-review.md) | Removal of active archived-input dependencies, necessary formal supplements, preserved historical boundaries and focused verification evidence |
| [final-design-review.md](final-design-review.md) | Historical independent post-amendment review of all 51 active packages and the accepted family; frozen repair groups, corrected authorities/producer gates, document verification and remaining runtime evidence |
| [producer-and-local-grpc-closure-review.md](producer-and-local-grpc-closure-review.md) | Current AF01–AF18 and local IPC closure: corrected source snapshots, 52-WP/161-edge graph, numbered gRPC/OS-stream design, bounded final review and reproducible document checks; runtime gates remain open |

## Conventions

- Every gate has an owner, a trigger, a statement of what it blocks, and a named evidence artifact. A gate that depends on someone remembering is not a gate.
- **Design-stage gates close on design evidence; implementation-stage gates never do.** Five are closed. The [closure review](phase-2-design-closure-review.md) and [reproducible checks](design-repair-verification.md) record the new citation closure; the register separately records the remaining runtime obligations.
- **Registering an open finding never closes a gate.** Where accounting and enforcement are both needed they are separate gates with separate evidence ([PG-06](open-gates-register.md#rule-pg-06) versus [PG-11](open-gates-register.md#rule-pg-11)).
- Citations use **D-nnn** for Phase 1 decisions, **V-nn** for verification findings, and **F-nnn** for deferred gates.


The [React/TypeScript Web redesign review](web-typescript-redesign-review.md) records the [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) migration, its contract/toolchain/session/visual scope and the current verification evidence.


The current [P2-009 amendment](../decisions/phase-2-specification-decisions.md#rule-p2-009) updates runtime/protocol/repository assumptions and activates the Cloud AOT gate. Prior review records are dated evidence; use the current requirements, contracts, planning and gate register for implementation. Product/runtime/commercial execution gates remain unclosed until their real evidence exists.

[Family design completion review](family-design-completion-review.md) records its dated 35-finding repair set, source snapshot, closure checks and self-contained validator. [VG-09](open-gates-register.md#rule-vg-09) is retired because iOS is outside current scope. Use the [current gate register](open-gates-register.md#7-register-summary) for the status of implementation obligations. Historical validation does not establish the current runtime, actual AOT/CF/device behavior or commercial readiness.

Current coordinated repair: [P2-013](../decisions/phase-2-specification-decisions.md#rule-p2-013); see [verification record](independent-review-remediation-verification.md). Runtime and commercial gates remain separate from design evidence.

Latest accepted implementation receipt: [WP03.02 — serialization posture](wp03-02-implementation-evidence.md), completed 2026-09-22 under its [approved profile](wp03-02-serialization-posture-profile.md) after [WP03.01](wp03-01-implementation-evidence.md), [WP03.00](wp03-00-implementation-evidence.md) and the accepted [WP02 stage](wp02-stage-acceptance.md). Its [machine-readable receipt](wp03-02-implementation-evidence.json) records reviewed source, passing PR/main checks including the Linux Native AOT probe, C#/TS vector coverage and all 22 normal package publications. [F-026](open-gates-register.md#rule-f-026) remains open for the generated-client AOT proof. Substep 03.03 has not started. Under [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018), new task completions are recorded in the Plan execution ledger and gate or package acceptance records are added here; the ordered execution steps inside dated profiles and receipts, such as advancing a Plan Current task, are historical records and not execution instructions. Later contract, runtime and commercial gates stay open; earlier receipts retain their historical scope and evidence.

Historical [WP00.03 — reuse and provenance](wp00-03-implementation-evidence.md), verified 2026-09-19, retains its original source, distribution and runtime evidence, including the candidate-specific [Android closure](open-gates-register.md#21-current-android-candidate-licence-evidence). Historical evidence does not require repeating the removed CI or post-publication checks.
