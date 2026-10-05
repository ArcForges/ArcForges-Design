# WP05 architecture and repository policy stage acceptance

Authority: [WP-05.90 and the parent completion gate](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.90), [staged producer integration](../planning/README.md#staged-artifact-integration), [producer responsibilities](../planning/producer-artifacts-and-integration.md) and [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). Task: [GOV.15](../planning/delivery/lanes/governance.md#task-gov-15). The [machine-readable receipt](wp05-stage-acceptance.json) lists exact sources and results; the [integration evidence](wp05-90-integration-evidence.md) records the cross-repository graph, its pinned inputs, fixtures and limits.

**Result: delivered, not accepted complete.** Every repository enforces its own boundary, the cross-repository graph passes over the pinned published metadata with zero findings, and each policy host runs in a pull-request-reachable workflow. The stage is not accepted as complete because [GOV.07](../planning/delivery/lanes/governance.md#task-gov-07) is itself delivered, not complete (its executable function-pointer deferral stands, now tracked by GOV.20), so the receipt cannot join ten completed results. WP06 and WP21 take this task as an external artifact prerequisite only after it reaches the state their edges require.

Labels: **ledger** is taken from the Plan ledger record of the preceding task without re-observation; **observed** was read by the GOV.15 claimant from the provider or the file during this task.

## Joined results of GOV.04-GOV.14

| Task | Repository | State (ledger) | Reviewed head and merge (ledger) | Result carried into this stage |
|---|---|---|---|---|
| [GOV.04](../planning/delivery/lanes/governance.md#task-gov-04) | DesktopPlatform | complete | PR 67 `2e180f7826ef9cae0b679db7d10459e51027d4b2` merge `8cb04f44116b5e77f7c3c54d58d89ac5b4ab78bc`; repair PR 72 merge `e769b626c559fab3ea1d0a7eb7c0e60ea159bce6` | shared AT-01..14/RP-01..10 engine; 24 rules each with a passing and a failing compiled fixture; DesktopPlatform enforcement over 20 real projects |
| [GOV.05](../planning/delivery/lanes/governance.md#task-gov-05) | Contracts | complete | PR 71 `24b36e6caf3e411309532da42934fb495e0f796f` merge `2b41656c52d4073e05923a189ef8dd4974b7dc39` | contract and serialization policy over the real graph; hosted gate; main run `37194938676` success |
| [GOV.06](../planning/delivery/lanes/governance.md#task-gov-06) | DesktopPlatform | complete | PR 138 `65abc363220989fc277504f5dd53f80e9d49afb1` merge `d6e3fabf4dea2112d9c594c5eb5ac7f679c8be20` | generated-source reconstruction and generated-type recognition |
| [GOV.07](../planning/delivery/lanes/governance.md#task-gov-07) | ArcScope | **delivered** | PR 23 `0a9c2c053c3c1066029a032a4481e85b949ddef8` merge `80dd7f24009a5259cf432551b26d70b634b7b746` | host and hosted gate run; executable is non-production for the banned-API scan and production-only layer rules (deferral) |
| [GOV.09](../planning/delivery/lanes/governance.md#task-gov-09) | Cloud | complete | PR 43 `1679749041988ed8181f21830bdcefd90f2b6a9a` merge `ea08736d571cf0f4b44e022117cb44652a392e66` | hosted architecture gate and naming scan; main run `37255090427` success |
| [GOV.10](../planning/delivery/lanes/governance.md#task-gov-10) | AI | complete | PR 28 `fbe27687b57b78a1c88431b883f821a64084ad22` merge `5421c3789240093b2fce36322c2eb7773325ec7b` | Node/TypeScript policy wired into `npm run check` |
| [GOV.11](../planning/delivery/lanes/governance.md#task-gov-11) | Web | complete | PR 20 `202483ae52513716325b382c1093bf0bd87bc951` merge `cd65b035c85532cd4c0467d31ac90e1006d8fa9a` | Web architecture and canonical naming policy |
| [GOV.12](../planning/delivery/lanes/governance.md#task-gov-12) | Mobile | complete | PR 17 `ec43fc0f6abccc98d58fc46b2e21acb9c342343c` merge `34c64e05fcfb9da81d41b999555090938263947e` | Gradle policy, 59 of 59 result rows |
| [GOV.13](../planning/delivery/lanes/governance.md#task-gov-13) | DesktopPlatform | complete | see ledger gov-13 | accounting report covers all 406 invariants: 0 enforced and passing, 0 enforced and failing, 406 not yet implemented ([PG-11](open-gates-register.md#rule-pg-11) stays open) |
| [GOV.14](../planning/delivery/lanes/governance.md#task-gov-14) | DesktopPlatform | complete | PR 68 `fdffa0ce6c57e1bf7acb4e43bdd9651e40939bf2` merge `357e8a56004ff08776767ff6a9e43e138071685e` | specification integrity and decision coverage over the Design corpus |

There is no GOV.08 task in the delivery graph; the eleven numbers GOV.04-GOV.14 name ten tasks.

## Stage conditions

| Condition | Evidence | Result |
|---|---|---|
| Each repository enforces its own boundary independently | the ten results above; SI-09 finds each host and its pull-request-reachable, unconditional gate in the pinned metadata of all seven repositories (**observed**) | holds, with the GOV.07 executable deferral |
| The integration graph detects a forbidden transitive edge without cloning | [integration evidence](wp05-90-integration-evidence.md): eleven rules over published metadata; transitive edges fail in synthetic fixtures through producer-declared and lock-declared dependencies | holds for the pinned metadata; fixtures are not real-repository observations |
| The architecture and specification-integrity suites run in the pull-request pipeline and a violation fails the build | DesktopPlatform architecture suite, accounting and design-policy; the new `stage-integration` job (hosted run `37262285837` passed on DesktopPlatform#142, **observed**); the other six repositories' hosts in pull-request-reachable workflows (**observed** in pinned workflow files) | holds |
| Exact artifacts and provider reality recorded | pinned heads and hosted main runs listed in the [receipt](wp05-stage-acceptance.json) (**observed**, job conclusions only) | recorded |

## Not covered

No runtime, device, GUI, browser, live-service, inference or installed-consumer test ran, and no macOS result is claimed. The graph evaluates declared metadata at a pin; it does not see later merges, does not execute any product, and does not close native isolation, Native AOT, Cloudflare or commercial gates. PG-11 and the GOV.07 deferral remain open items for their owners. No artifact was downloaded, hashed or republished to create this receipt.
