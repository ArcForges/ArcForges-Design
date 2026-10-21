# ArcForges design

Authoritative design of ArcForges, the flagship product: a cross-platform resource-control and execution platform for AI and automation ([AD-0001](decisions/AD-0001-flagship-pivot.md)). The delivery plan lives in [ArcForges/Plan](https://github.com/ArcForges/Plan).

## Read in this order

1. [Product definition](product/product-definition.md) and [requirements](product/requirements.md)
2. [Decisions](#decisions) AD-0001 … AD-0018
3. [Architecture](#architecture) chapters 01–18
4. [Contracts](contracts/README.md), [API catalogue](contracts/api-catalogue.md), [errors](contracts/errors.md)
5. [Data](#data), [state machines](state-machines/README.md), [experience](experience/README.md)
6. [Reuse and conflicts](#reuse), [verification register](verification/platform-capabilities.md), [traceability](traceability/model.json), [research records](#research)

## Product

- [product-definition.md](product/product-definition.md)
- Release 1 scope and supported operations: [product definition](product/product-definition.md) §9; the canonical [roadmap](https://github.com/ArcForges/Plan/blob/main/roadmap.md) (committed delivery, accepted future work, exploratory ideas) lives in ArcForges/Plan
- [requirements.md](product/requirements.md) (R-EXE … R-TEST, 141 requirements)

## Decisions

| ID | Decision |
|---|---|
| [AD-0001](decisions/AD-0001-flagship-pivot.md) | ArcForges becomes the flagship; new authoritative repositories |
| [AD-0002](decisions/AD-0002-platform-scope.md) | Platform scope: Windows and Linux now; macOS an accepted future execution target (AD-0017, roadmap RM-15), outside the current scope until RM-15 is promoted |
| [AD-0003](decisions/AD-0003-architecture-and-runtimes.md) | Components, runtimes and binaries (C#-first) |
| [AD-0004](decisions/AD-0004-contracts-and-state.md) | Contracts and authoritative state |
| [AD-0005](decisions/AD-0005-resource-enforcement.md) | Resource enforcement and privileges (WSL model superseded by AD-0018) |
| [AD-0006](decisions/AD-0006-execution-semantics.md) | Execution semantics: durability, retries, pause, caching |
| [AD-0007](decisions/AD-0007-ai-integration.md) | AI client integration |
| [AD-0008](decisions/AD-0008-lan-trust-and-placement.md) | LAN trust and placement |
| [AD-0009](decisions/AD-0009-cloud-relay-and-cost-controls.md) | Cloud relay, remote control, push and cost controls |
| [AD-0010](decisions/AD-0010-commerce-and-entitlements.md) | Commerce and entitlements |
| [AD-0011](decisions/AD-0011-identity-and-login.md) | Identity and login |
| [AD-0012](decisions/AD-0012-distribution-and-updates.md) | Distribution, signing, updates and rollback |
| [AD-0013](decisions/AD-0013-reuse-and-supersession.md) | Reuse, adaptation, retention and supersession |
| [AD-0014](decisions/AD-0014-delivery-method.md) | Delivery method: serial, distinct evidence, honest acceptance |
| [AD-0015](decisions/AD-0015-direction-editions-roadmap.md) | Product direction, editions (local and LAN free) and roadmap governance |
| [AD-0016](decisions/AD-0016-local-first-verification.md) | Local-first verification, owner-only lightweight CI and testing techniques |
| [AD-0017](decisions/AD-0017-delegated-execution-direction.md) | Long-term direction: application and workload control with verified contracts (principles only; the model is proposed in chapters 17 and 18) |
| [AD-0018](decisions/AD-0018-native-platforms-without-wsl-integration.md) | Native Windows and native Linux, without dedicated WSL integration; local-first verification on native legs |

## Architecture

| Chapter | Topic |
|---|---|
| [01](architecture/01-system-overview.md) | System overview, topologies, boundaries, repository map |
| [02](architecture/02-node-service.md) | Node service: structure, lifecycle, endpoint, configuration |
| [03](architecture/03-resource-control.md) | Observation, budgets, admission, enforcement, pressure |
| [04](architecture/04-execution.md) | Task specification, launch, output, attach, cancellation, recovery |
| [05](architecture/05-toolchains-caches.md) | Toolchains, adapters, caches, compiler servers, LAN cache sharing |
| [06](architecture/06-storage-workspaces.md) | Managed storage, workspaces, analysis, two-phase cleanup |
| [07](architecture/07-records-diagnosis-memory.md) | Records, diagnosis, findings, operational memory |
| [08](architecture/08-ai-integration.md) | AI clients: MCP adapter, hooks, sessions, routing, coverage |
| [09](architecture/09-lan.md) | LAN discovery, pairing, placement, transfer |
| [10](architecture/10-cloud.md) | Cloud: relay, flows, Durable Object, limits |
| [11](architecture/11-security-privacy.md) | Security and privacy: origins, permissions, threats, retention |
| [12](architecture/12-client-applications.md) | Client applications: shared client, Desktop, CLI, web, Android |
| [13](architecture/13-distribution-updates.md) | Distribution, installation, updates, store migrations |
| [14](architecture/14-commercial-operations.md) | Commercial operations: plans, lifecycle, support, costs, legal |
| [15](architecture/15-performance-targets.md) | Performance and footprint targets |
| [16](architecture/16-testing-strategy.md) | Testing strategy |
| [17](architecture/17-delegated-execution.md) | Verified contracts: access, confinement and lifecycle (ROADMAP, proposed): the access and confinement model, the single truth model, the fourteen fields of its rows, rejected alternatives, owner decisions |
| [18](architecture/18-application-workload-control.md) | Application and workload control (ROADMAP, proposed): the positioning in the owner's words, owner-directed and cooperative resource control, placement, the per-application record, third-party and first-party applications, the interactive guard, the fourteen fields of EX-24, EX-25, EX-26 and RM-09, owner decisions |

## Contracts

- [README](contracts/README.md): conventions, annotations, compatibility
- [api-catalogue.md](contracts/api-catalogue.md): generated, 30 services, 225 methods
- [errors.md](contracts/errors.md)
- [reuse-map.md](contracts/reuse-map.md)
- [proto/](contracts/proto/): `node/v1` (20 files), `peer/v1`, `fleet/v1`, `relay/v1`
- [reference/contracts-b774c322](contracts/reference/contracts-b774c322/README.md): pinned foundation contract

## Data

- [node-store.md](data/node-store.md) and [node-store.sql](data/node-store.sql)
- [cloud-store.md](data/cloud-store.md) and [cloud-store.sql](data/cloud-store.sql)

## State machines

- [README](state-machines/README.md) (generated) from [machines.json](state-machines/machines.json): 19 machines, one of them (the WSL guest link) retired by AD-0018 and kept as history

## Experience

- [README](experience/README.md): template, standard states, accessibility
- [desktop.md](experience/desktop.md), [cli.md](experience/cli.md), [mcp.md](experience/mcp.md), [web.md](experience/web.md), [android.md](experience/android.md), [journeys.md](experience/journeys.md)

## Reuse

- [inventory-and-classification.md](reuse/inventory-and-classification.md)
- [conflicts.md](reuse/conflicts.md)
- [desktopplatform-refactor.md](reuse/desktopplatform-refactor.md)

## Research

- [research/2026-10-18-delegated-execution/](research/2026-10-18-delegated-execution/README.md): the curated evidence record and lab register of the 2026-10-18 delegated-execution study, behind AD-0017 and chapter 17; roadmap evidence only, not verification-register facts
- [research/2026-10-19-application-workload-control/](research/2026-10-19-application-workload-control/README.md): the curated evidence record and lab register of the 2026-10-19 vision-correction study, behind AD-0017 as amended and chapters 17 and 18; roadmap evidence only, not verification-register facts

## Verification and traceability

- [verification/platform-capabilities.md](verification/platform-capabilities.md): verified facts, local probes, assumptions and future validations
- [traceability/model.json](traceability/model.json): requirement → design → task → verification
