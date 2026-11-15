# AD-0023 — Current toolchain baseline and local/CI parity

- Status: Accepted owner direction; implementation verification remains pending.
- Date: 2026-11-14
- Amendment: 2026-11-15; the owner's latest scope clarification supersedes the earlier all-transitive-latest requirement and special Contracts Go qualification procedure.
- Decision owner: product owner, through the direction to preserve completed upgrades and finish the necessary mainstream toolchains with local/CI parity.
- Scope: supplements AD-0022 without changing product boundaries or ordinary native acceptance gates.

## Decision and order

Preserve all upgrades already completed across ArcForges, Cloud, Web, Contracts, DesktopPlatform, ArcForges-Design and Plan. Finish AFV2-ENV-01 around the necessary .NET/C#, Go and TypeScript toolchains and their applicable Node/npm, Python, native build and CI support. Adapt the current source/build integration and keep the selected versions consistent between local execution and CI. Independent Mobile, AI, ArcScope, ArcSlate and ArcNotes remain protected consumers outside this implementation scope.

Use explicit supported tool selections, normal locked dependency resolution and actual executable/SDK roots. Keep existing version, source, checksum and licence evidence; completed detailed inventories remain useful and are not discarded. Windows/Linux artifacts and hosted/native operating-system venues remain explicitly distinct. A mismatched selected SDK, PATH override or unlocked restore still fails the existing preflight controls.

Completion does not require upgrading every direct or transitive dependency to its individually newest upstream version, proving stable tags for all upstream metadata, researching untagged modules, or obtaining separate per-version review or owner approval. Compatible existing locked dependencies, including ordinary fixed Go pseudo-versions, may remain under the existing compilation, tests, security, checksum and source/provenance controls. No repository-specific exception process is needed merely to retain that compatible resolution. Newly published upstream versions do not automatically invalidate an otherwise compatible verified candidate.

The earlier Contracts-only named-metadata and two-module qualification procedure is no longer an additional ENV acceptance requirement. Preserve its already collected source observations and measured results as dated evidence; do not turn them into invented passes or erase ordinary Go module verification, tidy-drift, vulnerability, analyzer, build or owned-test checks.

## Compatibility, publication and immutable evidence

Retain completed tool and dependency upgrades. Repair actual compatibility failures caused by the selected necessary toolchains while keeping warnings, AOT/trim, security and platform behavior checks intact. Use an already published compatible shared-producer cohort when it satisfies the consumer. A new producer version is required only for a real source/API/package change or compatibility need, not merely because a language toolchain was upgraded. When a new cohort is needed, use the ordinary producer-before-consumer publication and admission order.

Preserve public APIs, contract fields, independent consumers, published package bytes, applied SQL/checksums, historical receipts and frozen source audits. Never publish over an existing version or reuse a withdrawn first-party version. Historical tools may remain isolated for reproduction; they must not unexpectedly select the current build. Changed native/runtime components retain their existing relevant qualification tasks; an old success is not evidence for changed behavior.

The already authorized prerequisite installations on the designated Windows/Linux hosts may continue with verified artifacts and rollback-safe side-by-side selection. Preserve previous installations and in-flight work. Proxy/network/security changes, host replacement, service deployment and public activation remain outside this authorization.

## Completion

AFV2-ENV-01 completes when the seven repositories' necessary selected toolchains and local/CI versions are aligned, compatible current source and locked resolution pass the normal required compilation/tests/security/source checks and exact-head host profiles, and applicable ordinary publication/admission is recorded. Keep the existing normal delivery review and reporting rules; do not add a new dependency-by-dependency approval loop. Merge this scope clarification Design first, then verify Plan against that Design main.

The task remains active until those actual results exist. This clarification does not report an installation, successful build, accepted dependency cohort or product delivery. Preserve completed work and record real remaining failures without restarting upstream-version research.
