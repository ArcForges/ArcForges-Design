# Product Requirements

Per-product requirements for the ArcForges family. Each document assumes [`../00-product-scope-and-portfolio.md`](../00-product-scope-and-portfolio.md) and [`../01-normative-glossary-and-invariants.md`](../01-normative-glossary-and-invariants.md), and consumes the cross-cutting requirements rather than restating them.

The current [P2-006 amendment](../../decisions/phase-2-specification-decisions.md#rule-p2-006) governs scope. Architecture/planning/assurance references still require reconciliation; these requirements do not certify implementation or Stage 2 closure.

## Desktop products

The frozen baseline is exactly four desktop products (**[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)**).

| Document | Product | Positioning |
|---|---|---|
| [`arcchat.md`](arcchat.md) | **ArcChat** (`arcchat`) | Native Cloud AI/task surface, local capability/authorization bridge and thin previews |
| [`arcnotes.md`](arcnotes.md) | **ArcNotes** (`arcnotes`) | Cloud-synchronized native notes: rich documents, references, basic properties/table/list views and durable cached work; no whiteboard, slides or collaboration (**[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**) |
| [`arcscope.md`](arcscope.md) | **ArcScope** (`arcscope`) | Local-first Observation, Acquisition & Telemetry Analysis authority — independently defined, **not** a continuation of any prior product (**[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)**) |
| [`arcslate.md`](arcslate.md) | **ArcSlate** (`arcslate`) | Local-first Professional Non-linear Video Editing authority, rebuilt in C#/Avalonia with ArcVideo and ArcVideoFoundation as product references only |

## Platform and companion surfaces

| Document | Surface | Positioning |
|---|---|---|
| [`arcforges-cloud.md`](arcforges-cloud.md) | **ArcForges Cloud** | The continuity and remote-execution platform: an ASP.NET Core **JIT modular monolith** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**), one deployment host with bounded internal work, dependency posture, environments, deployment, operations, resilience and go-live threshold |
| [`arcforges-web.md`](arcforges-web.md) | **ArcForges Web** | The twelve-surface web presence: static public pages plus one React/TypeScript application (**[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**, **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**, **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**) |
| [`arcchat-mobile-and-web.md`](arcchat-mobile-and-web.md) | **ArcChat Mobile / ArcChat Web** | Cloud continuity and remote-agent companion — Apache-2.0 mobile boundary (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**), Android on Mono AOT with iOS build-deferred (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**), consumption-only commerce (**[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**) |

## Rules that apply to every product document

1. **Product independence** — native editors do not require ArcChat for ordinary use. Cloud accounts/service govern synchronized notes and AI; cached editing/search and native capture/render retain their explicit offline contracts. ArcChat bridges AI access to local tools.
2. **State ownership** — each document states what its product owns authoritatively and what it must never own.
3. **Reference posture** — where a reference repository exists (**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**), the document records that it is a source of features, behaviour, tests and possibly reusable material, never an architecture authority or a parity commitment, and that reuse is licence- and provenance-gated (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**).
4. **V1 scope** — each document separates the complete product model from what the first release must actually deliver, so "complete specification" is never mistaken for "complete first version".
5. **Acceptance scenarios** — each document ends with the scenarios that must pass, including failure behaviour, not only the happy path.
