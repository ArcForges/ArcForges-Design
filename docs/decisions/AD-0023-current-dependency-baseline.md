# AD-0023 — Current dependency baseline and local/CI parity

- Status: Accepted owner direction; implementation and qualification remain pending.
- Date: 2026-11-14
- Decision owner: product owner, through the instruction to upgrade all dependencies and keep local and CI versions equal, after document review and merge.
- Scope: supplements AD-0022 delivery policy without changing its product boundaries or native acceptance gates.

## Decision and order

Finish independent review and required native verification of the paired Design/Plan amendment, merge Design, verify Plan against that actual Design main, then merge Plan. Only then execute AFV2-ENV-01 to upgrade the current development baseline before resuming the product tasks. Version discovery and installation are implementation work; selecting concrete version numbers is not a prerequisite to accepting this policy.

All seven repositories involved in delivery are covered: ArcForges, Cloud, Web, Contracts, DesktopPlatform, ArcForges-Design and Plan. Upgrade their SDKs/runtimes, language and package-manager tools, native build/code-generation/test/security tools, CI Actions and runner/build/container images, plus all direct and resolved transitive NuGet, npm, Go and other third-party dependencies. Shared producers are included even when they are not standalone V2 products. Independent Mobile, AI, ArcScope, ArcSlate and ArcNotes remain protected consumers, outside the blanket upgrade scope.

Use the latest upstream stable release available when the implementation candidate is locked, including stable major upgrades. Exclude previews, release candidates, deprecated and withdrawn releases; do not silently restrict selection to an older major or LTS channel. Record the lookup time, upstream source, exact version and artifact identity in a reviewed machine-readable inventory. A pinned candidate is reproducible: do not use floating `latest` tags or ranges as evidence. Recheck before final acceptance; a newly available stable release requires updating and reverifying the affected candidate. Dependency incompatibility is work to resolve, not permission to call an older pin current. If upstream constraints make the requested combination impossible, report the concrete blocker and leave the task unfinished until resolved or the owner changes scope.

Local execution on both designated MCP hosts and CI must select the same pinned versions and dependency graph for each repository. Record resolved executable paths, SDK/runtime and package-manager versions, lockfile hashes and platform-specific image/artifact digests. Windows and Linux binaries/digests may differ for the same upstream version; OS-specific tools remain explicitly platform-specific. Hosted runner OS images and native host OS images are distinct venues, not interchangeable machines. Keep a documented supported platform matrix and identical applicable tools/checks instead of claiming identical operating systems. Mismatched SDK roots, PATH overrides or unlocked restores fail preflight. Update current source/build integration and tests for new APIs/TFMs; never weaken analyzers, AOT, security, required checks or platform behavior to admit a version bump.

## Compatibility and immutable evidence

Upgrade shared DesktopPlatform/Contracts producers before admitting their new main-descended package cohorts into consumers. Preserve existing consumers through compatible packages or versioned migration; a newer dependency does not authorize removing a public API, repurposing a contract field or changing product scope. Record the producer commit, publication and each consumer admission. Never reuse a withdrawn first-party version or publish over an existing version.

Frozen history, published package bytes, applied SQL/checksums, captured acceptance receipts and historical bootstrap/security-bridge artifact identities remain immutable. They document what actually ran. Old tool versions needed solely to reproduce such artifacts may remain isolated and explicitly labeled historical; they cannot select the current build by default or count as latest-version acceptance. New dependency baselines get new evidence. No historical success proves MXC/native/runtime behavior for a changed cohort.

The owner has authorized the prerequisite local tool installations needed for this upgrade on the named Windows/Linux hosts. Preserve existing installations and in-flight work; use verified upstream artifacts and side-by-side installation where needed for rollback or historical reproduction. This authorization does not extend to proxy/network/security changes, host replacement, service deployment or public activation. The unchanged host reporting mechanism, independent review, serial execution and separate AFV2-PROD-01 activation approval continue to apply.

## Completion

AFV2-ENV-01 owns the full seven-repository inventory, upgrades, compatibility repairs, applicable publication/admission, local/CI parity evidence and rollback record. Every repository must have its reviewed latest candidate merged after its required exact-head native profiles pass. Resolve all current dependency entries, with explicit platform applicability and historical-only classification; a partial upgrade is not task completion. Subsequent tasks retain this policy for dependencies they add or change and requalify changed native components through their existing acceptance tasks.

This document records a requirement, not an installed-version, successful-build or product-delivery claim. Source research snapshots stay dated evidence; append new upgrade evidence without rewriting their observed facts.
