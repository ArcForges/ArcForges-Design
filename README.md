# ArcForges Design

This repository contains product requirements, system architecture, design decisions, and delivery planning for the ArcForges product family. It does not contain product implementation code.

Current work uses the formal requirements, architecture, planning and assurance under the effective accepted decisions. The original inputs completed their role; under [P2-019](docs/decisions/phase-2-specification-decisions.md#rule-p2-019) their bodies are not carried into this repository, and [`docs/deprecated-inputs/README.md`](docs/deprecated-inputs/README.md) identifies where they remain archived. They are **deprecated**, not current design authority or part of ongoing design-completeness audits. A missing current definition must be resolved in the formal design, not inferred from the archive.

## Repository Structure

- [`docs/requirements/`](docs/requirements/): Product requirements and scope specifications.
- [`docs/architecture/`](docs/architecture/): System architecture specifications, topology, and component boundaries.
- [`docs/decisions/`](docs/decisions/): Architecture Decision Records (ADRs) capturing significant technical and design choices.
- [`docs/planning/`](docs/planning/): Implementation delivery plans and work packages derived from accepted designs.
- [`docs/assurance/`](docs/assurance/): Design specifications covering quality, security, and acceptance criteria.
- [`docs/deprecated-inputs/`](docs/deprecated-inputs/README.md): Records where the deprecated original inputs are archived; their bodies are not carried into this repository. Excluded from active design, planning and audit scope.

Historical `I1`–`I4` and input Stage citations identify the archived origin of a rule; they do not require reading or auditing those inputs again. Current definitions and accepted decisions stand on their own. Reference-source repositories and their review obligations are unaffected by this archival change.

## License

ArcForges Design is licensed under the GNU Affero General Public License v3.0. See [`LICENSE`](LICENSE).

## Current architecture amendment

The effective architecture summary is kept in the [decisions index](docs/decisions/README.md); this file records the amendments to the stack sentences in place.

[P2-009](docs/decisions/phase-2-specification-decisions.md#rule-p2-009) adopts independent repositories and versioned native/managed packages, handwritten proto business RPC, a Native AOT C# business host, and a sole Cloudflare AI Harness with Workers AI and R2. Its React Native Mobile, React Web, generated TypeScript client, sole Cloudflare Workflow AI loop and AI repository clauses are superseded in part (2026-10-08) by [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021), as are the Kotlin/Jetpack Compose Android clause of [P2-010](docs/decisions/phase-2-specification-decisions.md#rule-p2-010) and its Maven Java and Kotlin-lite SDK clause: Android is .NET MAUI, the Harness is C# with no Cloudflare Workflow holding run state, the ArcForges-AI Harness role ends when HAR.40 replaces its Hello slice in Cloud, and `@arcforges/ai-internal` is the only npm package kept. The other npm channels and the Maven channels stop only after their consumers migrate; published versions stay immutable and resolvable, and nothing is unpublished, deleted or deprecated without explicit user approval. Start implementation at the [planning entry](docs/planning/README.md); formal design decisions precede implementation and runtime proof.

[P2-010](docs/decisions/phase-2-specification-decisions.md#rule-p2-010) completes Android-only planning, all Apache Contracts outputs including Maven, functional native ABI (its PDF ABI is retired under [P2-022](docs/decisions/phase-2-specification-decisions.md#rule-p2-022)), full product/extension/policy behavior and cross-repository integration. Its Kotlin/Compose Android planning is superseded in part (2026-10-08) by [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021), and the Maven channels stop after their consumers migrate; published Maven versions stay immutable and resolvable, and none is unpublished, deleted or deprecated without explicit user approval. [Producer stages](docs/planning/producer-artifacts-and-integration.md) and the [family completion review](docs/assurance/family-design-completion-review.md) distinguish document closure from actual product/runtime/commercial evidence.

Current producer and local gRPC amendment: [closure review](docs/assurance/producer-and-local-grpc-closure-review.md). Use its current graph/contract evidence; earlier dated reviews retain their historical baselines.

## Current design entry points

[P2-012](docs/decisions/phase-2-specification-decisions.md#rule-p2-012) defines Cloudflare hosting and independent embedded assistants (superseded in part, 2026-10-08, by [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021) for the Workflow Harness and the Kotlin Android clause). Start with [project/package directories](docs/architecture/27-platform-projects-and-application-assistants.md), [client UX](docs/experience/README.md), [D1](docs/architecture/data-model/04-d1-execution-profile.md), [history](docs/architecture/data-model/05-application-history.md), and [scope/streams](docs/architecture/contracts/10-application-scope-and-streams.md). Implementation is scheduled by the [delivery model](docs/planning/delivery/README.md) under [P2-018](docs/decisions/phase-2-specification-decisions.md#rule-p2-018): 51 active work packages are the obligation catalogue and the delivery graph schedules concurrent tasks.

## Related repositories

This Design repository and the [Plan repository](https://github.com/ArcForges/Plan) (`C:\MyFile\Projects\Plan`) are the documentation pair governing the ArcForges family, per [P2-019](docs/decisions/phase-2-specification-decisions.md#rule-p2-019). Seven independent implementation repositories consume their accepted decisions: DesktopPlatform, Contracts, ArcScope, Cloud, Web and Mobile, and AI (`ArcForges-AI`). Under [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021) its Harness runtime role ends when HAR.40 replaces its Hello slice in Cloud, and HAR.40 retires its deployment; the deployed `arcforges-ai` Worker stays live until then, deleting it requires explicit user confirmation, and the repository is kept as read-only history afterwards.

Current coordinated repair: [P2-014](docs/decisions/phase-2-specification-decisions.md#rule-p2-014); see [final findings verification](docs/assurance/final-findings-remediation-verification.md). The 2026-10-08 scope decisions [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021) to [P2-024](docs/decisions/phase-2-specification-decisions.md#rule-p2-024) supersede conflicting stack, PDF, macOS and WSL clauses in place: the C#-first stack; the retirement of native in-app PDF preview and local PDF parsing, with generic PDF attachments kept as opaque attachments, image support and ArcScope report export kept, and report PDFs presented only through the platform's own viewer or as a download; macOS out of scope; and WSL2 Linux checks. [P2-025](docs/decisions/phase-2-specification-decisions.md#rule-p2-025) records the blocked-external inputs (Postmark/SES, the second Windows account and a second Linux uid) with acceptance preserved, never removed or passed. See the [decisions index](docs/decisions/README.md). Earlier dated reviews retain their evidence baselines; real runtime and commercial gates remain separate and open.
