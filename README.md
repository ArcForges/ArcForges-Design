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

## Effective architecture

Seven independent repositories integrate published NuGet packages and immutable artifacts. The only npm package kept is the internal `@arcforges/ai-internal` codec, and the Maven channels retire once their consumers migrate ([P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021)). Business and product logic is C# (.NET 10 LTS) on every surface: ArcScope, the one professional desktop application on Avalonia, which embeds its own application-owned assistant; the C# Native AOT Cloud host; Blazor WebAssembly Web profiles, with the public Site generated as static HTML by a C# generator; and .NET MAUI Android, Android only. TypeScript survives only as thin Cloudflare platform adapters that make no business decision. Every public business client uses authored-proto binary gRPC-Web; private child controls use generated gRPC over Named Pipe/UDS. Cloudflare Workers front the C# Native AOT Container, D1 authority, coordination DOs and R2. The AI Harness is C# on a D1 executor with Durable Object alarm wake, and Workers AI is reached through a thin binding adapter; no Cloudflare Workflow holds run state. ArcScope report export continues; in-app PDF preview and local PDF parsing are retired ([P2-022](docs/decisions/phase-2-specification-decisions.md#rule-p2-022)); macOS is out of scope ([P2-023](docs/decisions/phase-2-specification-decisions.md#rule-p2-023)). Cross-product collaboration is future-only.

## Current architecture amendment

[P2-009](docs/decisions/phase-2-specification-decisions.md#rule-p2-009) adopts independent repositories and versioned native/managed packages, handwritten proto business RPC, a Native AOT C# business host, and a sole Cloudflare AI Harness with Workers AI and R2. Its Kotlin/Jetpack Compose Android clause ([P2-010](docs/decisions/phase-2-specification-decisions.md#rule-p2-010)), its Workflow-only AI loop and its Kotlin, npm and Maven parts are superseded in part by [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021): Android is .NET MAUI, the Harness is C# with no Cloudflare Workflow holding run state, and `@arcforges/ai-internal` is the only npm package kept. Start implementation at the [planning entry](docs/planning/README.md); formal design decisions precede implementation and runtime proof.

[P2-010](docs/decisions/phase-2-specification-decisions.md#rule-p2-010) completes Android-only planning, all Apache Contracts outputs including Maven, functional native ABI (its PDF ABI is retired under [P2-022](docs/decisions/phase-2-specification-decisions.md#rule-p2-022)), full product/extension/policy behavior and cross-repository integration. Its Kotlin/Compose Android planning is superseded in part by [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021), and the Maven channels stop after their consumers migrate. [Producer stages](docs/planning/producer-artifacts-and-integration.md) and the [family completion review](docs/assurance/family-design-completion-review.md) distinguish document closure from actual product/runtime/commercial evidence.

Current producer and local gRPC amendment: [closure review](docs/assurance/producer-and-local-grpc-closure-review.md). Use its current graph/contract evidence; earlier dated reviews retain their historical baselines.

## Current design entry points

[P2-012](docs/decisions/phase-2-specification-decisions.md#rule-p2-012) defines Cloudflare hosting and independent embedded assistants. Start with [project/package directories](docs/architecture/27-platform-projects-and-application-assistants.md), [client UX](docs/experience/README.md), [D1](docs/architecture/data-model/04-d1-execution-profile.md), [history](docs/architecture/data-model/05-application-history.md), and [scope/streams](docs/architecture/contracts/10-application-scope-and-streams.md). Implementation is scheduled by the [delivery model](docs/planning/delivery/README.md) under [P2-018](docs/decisions/phase-2-specification-decisions.md#rule-p2-018): 51 active work packages are the obligation catalogue and the delivery graph schedules concurrent tasks.

## Related repositories

This Design repository and the [Plan repository](https://github.com/ArcForges/Plan) (`C:\MyFile\Projects\Plan`) are the documentation pair governing the ArcForges family, per [P2-019](docs/decisions/phase-2-specification-decisions.md#rule-p2-019). Seven independent implementation repositories consume their accepted decisions: DesktopPlatform, Contracts, ArcScope, Cloud, Web and Mobile, and AI (`ArcForges-AI`), a retired-runtime repository: its Harness role moves to Cloud and it remains read-only history after its last deployment is retired.

Current coordinated repair: [P2-014](docs/decisions/phase-2-specification-decisions.md#rule-p2-014); see [final findings verification](docs/assurance/final-findings-remediation-verification.md). The 2026-10-08 scope decisions [P2-021](docs/decisions/phase-2-specification-decisions.md#rule-p2-021) to [P2-025](docs/decisions/phase-2-specification-decisions.md#rule-p2-025) (C#-first stack, PDF preview retirement, macOS out of scope, WSL2 Linux checks and blocked-external inputs) supersede conflicting stack, PDF, macOS and WSL clauses in place; see the [decisions index](docs/decisions/README.md). Earlier dated reviews retain their evidence baselines; real runtime and commercial gates remain separate and open.
