# ArcForges Design

This repository contains product requirements, system architecture, design decisions, and delivery planning for the ArcForges product family. It does not contain product implementation code.

Current work uses the formal requirements, architecture, planning and assurance under the effective accepted decisions. The original inputs have completed their role and are archived in [`docs/deprecated-inputs/`](docs/deprecated-inputs/README.md). They are **deprecated**, not current design authority or part of ongoing design-completeness audits. A missing current definition must be resolved in the formal design, not inferred from the archive.

## Repository Structure

- [`docs/requirements/`](docs/requirements/): Product requirements and scope specifications.
- [`docs/architecture/`](docs/architecture/): System architecture specifications, topology, and component boundaries.
- [`docs/decisions/`](docs/decisions/): Architecture Decision Records (ADRs) capturing significant technical and design choices.
- [`docs/planning/`](docs/planning/): Implementation delivery plans and work packages derived from accepted designs.
- [`docs/assurance/`](docs/assurance/): Design specifications covering quality, security, and acceptance criteria.
- [`docs/deprecated-inputs/`](docs/deprecated-inputs/README.md): Deprecated original inputs, retained only for historical provenance. Excluded from active design, planning and audit scope.

Historical `I1`–`I4` and input Stage citations identify the archived origin of a rule; they do not require reading or auditing those inputs again. Current definitions and accepted decisions stand on their own. Reference-source repositories and their review obligations are unaffected by this archival change.

## License

ArcForges Design is licensed under the GNU Affero General Public License v3.0. See [`LICENSE`](LICENSE).

## Current architecture amendment

[P2-009](docs/decisions/phase-2-specification-decisions.md#rule-p2-009) adopts independent repositories and versioned native/managed packages, handwritten proto business RPC, a Native AOT C# business host, Kotlin/Jetpack Compose Android mobile under [P2-010](docs/decisions/phase-2-specification-decisions.md#rule-p2-010), and a sole Cloudflare AI Harness with Workers AI and R2. Start implementation at the [planning entry](docs/planning/README.md); formal design decisions precede implementation and runtime proof.

[P2-010](docs/decisions/phase-2-specification-decisions.md#rule-p2-010) completes Android-only Kotlin/Compose planning, all Apache Contracts outputs including Maven, functional native ABI, full product/extension/policy behavior and cross-repository integration. [Producer stages](docs/planning/producer-artifacts-and-integration.md) and the [family completion review](docs/assurance/family-design-completion-review.md) distinguish document closure from actual product/runtime/commercial evidence.

Current producer and local gRPC amendment: [closure review](docs/assurance/producer-and-local-grpc-closure-review.md). Use its current graph/contract evidence; earlier dated reviews retain their historical baselines.

## Current design entry points

[P2-012](docs/decisions/phase-2-specification-decisions.md#rule-p2-012) defines Cloudflare hosting and independent embedded assistants. Start with [project/package directories](docs/architecture/27-platform-projects-and-application-assistants.md), [client UX](docs/experience/README.md), [D1](docs/architecture/data-model/04-d1-execution-profile.md), [history](docs/architecture/data-model/05-application-history.md), and [scope/streams](docs/architecture/contracts/10-application-scope-and-streams.md). Implementation is scheduled by the [delivery model](docs/planning/delivery/README.md) under [P2-018](docs/decisions/phase-2-specification-decisions.md#rule-p2-018): 51 active work packages are the obligation catalogue and the delivery graph schedules concurrent tasks; [cross-product collaboration](docs/future/cross-product-collaboration/README.md) is future only.

Current coordinated repair: [P2-014](docs/decisions/phase-2-specification-decisions.md#rule-p2-014); see [final findings verification](docs/assurance/final-findings-remediation-verification.md). Earlier dated reviews retain their evidence baselines; real runtime and commercial gates remain separate and open.
