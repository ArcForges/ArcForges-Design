<a id="rule-wp-14"></a>
# WP-14 — Independent Application Composition and Typed Host Ports

> Status: Authoritative — P2-012
> Upstream: `08` · `09` · `10` · `11` · `13` · Downstream: `15` · `16` · `18`
> Repositories: DesktopPlatform + ArcNotes. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.

<a id="rule-br-01"></a>

## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-14.00"></a>
### WP-14.00 — Application scope and host ports

**What must be fully done.** Publish Assistant.Abstractions with architecture 27 host port signatures, product/profile identity and lifetime. The minimal sample uses real capabilities/shell/store; full AssistantHost UI is produced at 17.

**Testing requirements.** Two independent application identities cannot share stores/registration; no future 15/17 implementation dependency.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.01"></a>
### WP-14.01 — Minimal ArcNotes application services

**What must be fully done.** Implement real read/create/append document commands through typed application handlers and local persistence. Professional document completion remains 18.

**Testing requirements.** Descriptor/risk/context validation and one write path for UI and own-app capability.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.02"></a>
### WP-14.02 — Package consumer composition

**What must be fully done.** Build a clean Native AOT Notes consumer using exact Platform/Contracts packages and in-process typed host ports; no source reference or local RPC product loop.

**Testing requirements.** Package-only restore, publish/run, command/cancel/result and owner refusal.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.03"></a>
### WP-14.03 — Idempotency and revision

**What must be fully done.** Exercise command receipt and expected local revision against real store; preserve draft/conflict behavior and unknown outcome classification.

**Testing requirements.** Duplicate command, stale revision and process kill around commit.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.04"></a>
### WP-14.04 — Approval at the owner

**What must be fully done.** Render a real local approval and enforce it again in the product handler; authorization belongs to the app, not a shared coordinator.

**Testing requirements.** Expiry/modified input/revocation cannot bypass owner checks.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.05"></a>
### WP-14.05 — Context and artifact integration

**What must be fully done.** Freeze own-app resource references, open preview through product port, enforce egress separately and preserve provenance.

**Testing requirements.** Selection changes after freeze, missing resource, denied export and bounded artifact.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.06"></a>
### WP-14.06 — Independent lifecycle

**What must be fully done.** Launch/save with Cloud unavailable and assistant view closed; dispose views independently from services. Professional app shutdown handles local work honestly.

**Testing requirements.** Two windows/different drafts, independent app crash, no loss of canonical data.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-14.90"></a>
### WP-14.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Application scope and host ports: Two independent application identities cannot share stores/registration; no future 15/17 implementation dependency. | [WP-14.00](#rule-wp-14.00) |
| Minimal ArcNotes application services: Descriptor/risk/context validation and one write path for UI and own-app capability. | [WP-14.01](#rule-wp-14.01) |
| Package consumer composition: Package-only restore, publish/run, command/cancel/result and owner refusal. | [WP-14.02](#rule-wp-14.02) |
| Idempotency and revision: Duplicate command, stale revision and process kill around commit. | [WP-14.03](#rule-wp-14.03) |
| Approval at the owner: Expiry/modified input/revocation cannot bypass owner checks. | [WP-14.04](#rule-wp-14.04) |
| Context and artifact integration: Selection changes after freeze, missing resource, denied export and bounded artifact. | [WP-14.05](#rule-wp-14.05) |
| Independent lifecycle: Two windows/different drafts, independent app crash, no loss of canonical data. | [WP-14.06](#rule-wp-14.06) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-14.90](#rule-wp-14.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

**Upstream:** `08` · `09` · `10` · `11` · `13`. Consume completed stage outputs.

**Downstream:** `15` · `16` · `18`. Consumers use exact released artifacts.
