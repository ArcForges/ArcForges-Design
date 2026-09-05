# Requirements

This directory defines product requirements for the ArcForges family: product scope, user capabilities, behavior, constraints, and acceptance criteria.

All content here is **authoritative**. It is governed by the frozen Phase 1 decisions in [`../decisions/phase-1-foundation-decisions.md`](../decisions/phase-1-foundation-decisions.md) (D-001 … D-023) and by the verification record in [`../assurance/phase-1-official-verification.md`](../assurance/phase-1-official-verification.md) (V-01 … V-09). Where a requirement is governed by a decision, the decision is cited inline.

## Reading order

Read [`00-product-scope-and-portfolio.md`](00-product-scope-and-portfolio.md) and [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md) first. Everything else assumes both.

## Cross-cutting requirements

| Document | Covers |
|---|---|
| [`00-product-scope-and-portfolio.md`](00-product-scope-and-portfolio.md) | The frozen four-product baseline, commercial invariants, product independence, cross-product interaction, state ownership, data and control paths, the technology constitution, licensing scope, reference repositories, and the closed list of Architecture Baseline Changes |
| [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md) | **The D-018 gate.** One canonical definition per cross-product term, product namespacing, the full `X ≠ Y` invariant catalogue, term spaces, forbidden aliases and obsolete terms, and the V-02 MCP disambiguation |
| [`02-identity-account-and-workspace.md`](02-identity-account-and-workspace.md) | Realms, users and authentication identities, workspaces, devices, installations, instances and sessions, trust and remote access, step-up, API tokens, actors, account lifecycle and deletion, the account portal, and secret ownership |
| [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md) | The cloud capability bundle, data classification, sync scopes and change propagation, conflicts, deletion and tombstones, assets and immutable blobs, storage accounting, protection modes, cloud search, remote and cloud execution, automation in the cloud, notifications, the subscription lifecycle for cloud data, export and import, backup and disaster recovery, data health, and schema versioning |
| [`04-commerce-entitlement-and-credits.md`](04-commerce-entitlement-and-credits.md) | The Paddle Merchant-of-Record baseline with Payoneer payout, the product catalogue, pricing and tax posture, the purchase flow with event inbox and reconciliation, the subscription lifecycle, the grant-based entitlement model, quota and usage, the AI credit ledger, BYOK entitlement, refunds and disputes, mainland China, mobile commerce posture, and provider portability |
| [`05-ai-and-agent-execution.md`](05-ai-and-agent-execution.md) | The unified execution chain (Intent → Task → Run → Plan → Step → Attempt), lifecycle states, ownership and execution location, child tasks, checkpoints and compensation, approval and steering, budget, progress and trace, crash recovery, concurrency, automation, and the AI economics layer |
| [`06-knowledge-search-and-retrieval.md`](06-knowledge-search-and-retrieval.md) | Knowledge sources and scopes, indexes as derived projections, the five-dimension knowledge policy model, search versus retrieval, hybrid retrieval and budgets, permission and the index, evidence and citation, AI retrieval scope as the privacy boundary, and per-product knowledge responsibilities |
| [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md) | Principals and the actor chain, capability permission separated from resource authorization, the R0–R4 risk model, approval, step-up and local presence, secrets, data egress, instruction provenance, capability leases, typed trust, the fourteen-step security decision pipeline, audit, the security centre, privacy, and AI transparency obligations |
| [`08-extensions-and-developer-platform.md`](08-extensions-and-developer-platform.md) | Skills, templates, workflows, MCP, connectors, external agents, out-of-process extensions, the dual capability boundary, third-party apps, the Arc Package model, the community catalog, the public SDK and CLI, and placement rules |
| [`09-shared-desktop-experience.md`](09-shared-desktop-experience.md) | Design principles and the semantic token system, windows and panels, the command system, scoped settings, the attention model, errors, deep links, file associations, drag and drop, clipboard, lifecycle, menus, account surfaces, handoff, and the shared-foundation boundary |
| [`10-distribution-update-and-support.md`](10-distribution-update-and-support.md) | The distribution matrix and signing, release channels and records, update and rollback — and then support, operators, recovery, incidents, community reports, the enforcement ladder, appeals, and security advisories |
| [`11-policy-and-configuration.md`](11-policy-and-configuration.md) | The four boundaries separating policy from entitlement, settings, health and the data plane; features and flags; rollout; kill switches; remote config; scoped resolution; compatibility policy; provider and model availability; experiments; publication, staleness and explainability |
| [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md) | Two-tier thresholds, reference hardware, startup, memory, soak and background budgets, accessibility and localization contracts, units, the AOT gate, nine version axes, the compatibility matrix, migration and contract testing, crash and recovery, diagnostics, platform matrices, severity and waivers |
| [`13-data-formats-and-portability.md`](13-data-formats-and-portability.md) | The five-layer data separation, per-product storage strategy, working store versus portable package, format versioning, migration, save semantics, undo/revision/checkpoint/journal separation, external references, import and export, the portability constitution, Git friendliness, and backup |

## Product requirements

See [`products/README.md`](products/README.md).

## Conventions

- Every requirement carries a stable identifier (`AB-nn`) so architecture, assurance and work packages can cite it precisely.
- Every numeric commercial figure is **versioned commercial policy under D-020**, never a frozen commitment. Where a corpus-proposed default is recorded, it is labelled a proposal.
- Every `X ≠ Y` statement cites its invariant identifier from the glossary catalogue.
- Superseded product names (`ArcCanvas`, `ArcMusic`, `ArcImage`, `ArcVideo`) and the superseded payment provider never appear as current, per **D-002** and **D-005**.
