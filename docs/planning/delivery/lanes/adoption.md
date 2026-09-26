# Adoption stage — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

One-time reconciliation of existing implementation with this graph; see the adoption stage document.

Tasks: 11 · Owning repositories: AI, ArcNotes, ArcScope, ArcSlate, Cloud, Contracts, Design, DesktopPlatform, Mobile, Plan, Web · Integration owner(s): AI integration owner, ArcNotes integration owner, ArcScope integration owner, ArcSlate integration owner, Cloud integration owner, Contracts integration owner, Design integration owner, DesktopPlatform integration owner, Mobile integration owner, Plan integration owner, Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [ADOPT.01](#task-adopt-01) | Freeze the adoption baseline | adoption | S | none | not-started |
| [ADOPT.02](#task-adopt-02) | Adopt DesktopPlatform | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.03](#task-adopt-03) | Adopt Contracts | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.04](#task-adopt-04) | Adopt ArcNotes | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.05](#task-adopt-05) | Adopt ArcScope | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.06](#task-adopt-06) | Adopt ArcSlate | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.07](#task-adopt-07) | Adopt Cloud | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.08](#task-adopt-08) | Adopt AI | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.09](#task-adopt-09) | Adopt Web | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.10](#task-adopt-10) | Adopt Mobile | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |
| [ADOPT.11](#task-adopt-11) | Reconcile Design and Plan documentation for adoption | adoption | S | [ADOPT.01](#task-adopt-01) (artifact) | not-started |

## Tasks

<a id="task-adopt-01"></a>

### ADOPT.01 — Freeze the adoption baseline

**Outcome.** The Plan ledger records, for every repository, the main head, open pull requests and branches and the latest published candidate per registry, so every adoption slice starts from the same frozen inputs. The baseline is complete through [WP-03.02](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02); [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) has not started.

| Field | Value |
|---|---|
| Owning repository | Plan (`C:\MyFile\Projects\Plan-B`); integration owner: Plan integration owner, the holder of `roles/integration-plan` |
| Claim, branch and ledger | `claims/adopt-01` and ledger record `ledger/tasks/adopt-01.md` in the Plan repository; task branch `task/adopt-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: baseline inputs |
| Provides | adoption baseline record; ledger skeleton |
| Start prerequisites | none |
| Completion prerequisites | none |
| Unblocks | [ADOPT.02](#task-adopt-02), [ADOPT.02.app-composition](#task-adopt-02-app-composition), [ADOPT.02.assistant](#task-adopt-02-assistant), [ADOPT.02.cloud](#task-adopt-02-cloud), [ADOPT.02.device-bridge](#task-adopt-02-device-bridge), [ADOPT.02.execution](#task-adopt-02-execution), [ADOPT.02.extensions](#task-adopt-02-extensions), [ADOPT.02.foundation](#task-adopt-02-foundation), [ADOPT.02.governance](#task-adopt-02-governance), [ADOPT.02.native](#task-adopt-02-native), [ADOPT.02.platform](#task-adopt-02-platform), [ADOPT.02.policy](#task-adopt-02-policy), [ADOPT.02.release](#task-adopt-02-release), [ADOPT.02.runtime-proofs](#task-adopt-02-runtime-proofs), [ADOPT.02.updater](#task-adopt-02-updater), [ADOPT.03](#task-adopt-03), [ADOPT.03.contracts](#task-adopt-03-contracts), [ADOPT.03.extensions](#task-adopt-03-extensions), [ADOPT.03.governance](#task-adopt-03-governance), [ADOPT.03.release](#task-adopt-03-release), [ADOPT.04](#task-adopt-04), [ADOPT.04.app-composition](#task-adopt-04-app-composition), [ADOPT.04.arcnotes](#task-adopt-04-arcnotes), [ADOPT.04.governance](#task-adopt-04-governance), [ADOPT.04.release](#task-adopt-04-release), [ADOPT.04.runtime-proofs](#task-adopt-04-runtime-proofs), [ADOPT.05](#task-adopt-05), [ADOPT.05.arcscope](#task-adopt-05-arcscope), [ADOPT.05.governance](#task-adopt-05-governance), [ADOPT.05.release](#task-adopt-05-release), [ADOPT.05.runtime-proofs](#task-adopt-05-runtime-proofs), [ADOPT.05.simulator](#task-adopt-05-simulator), [ADOPT.06](#task-adopt-06), [ADOPT.06.arcslate](#task-adopt-06-arcslate), [ADOPT.06.governance](#task-adopt-06-governance), [ADOPT.06.release](#task-adopt-06-release), [ADOPT.06.runtime-proofs](#task-adopt-06-runtime-proofs), [ADOPT.07](#task-adopt-07), [ADOPT.07.ai-routing](#task-adopt-07-ai-routing), [ADOPT.07.cloud](#task-adopt-07-cloud), [ADOPT.07.commerce](#task-adopt-07-commerce), [ADOPT.07.device-bridge](#task-adopt-07-device-bridge), [ADOPT.07.extensions](#task-adopt-07-extensions), [ADOPT.07.governance](#task-adopt-07-governance), [ADOPT.07.harness](#task-adopt-07-harness), [ADOPT.07.operations](#task-adopt-07-operations), [ADOPT.07.policy](#task-adopt-07-policy), [ADOPT.07.release](#task-adopt-07-release), [ADOPT.07.runtime-proofs](#task-adopt-07-runtime-proofs), [ADOPT.07.search](#task-adopt-07-search), [ADOPT.07.simulator](#task-adopt-07-simulator), [ADOPT.08](#task-adopt-08), [ADOPT.08.ai-routing](#task-adopt-08-ai-routing), [ADOPT.08.extensions](#task-adopt-08-extensions), [ADOPT.08.governance](#task-adopt-08-governance), [ADOPT.08.harness](#task-adopt-08-harness), [ADOPT.09](#task-adopt-09), [ADOPT.09.governance](#task-adopt-09-governance), [ADOPT.09.operations](#task-adopt-09-operations), [ADOPT.09.release](#task-adopt-09-release), [ADOPT.09.runtime-proofs](#task-adopt-09-runtime-proofs), [ADOPT.09.web](#task-adopt-09-web), [ADOPT.10](#task-adopt-10), [ADOPT.10.android](#task-adopt-10-android), [ADOPT.10.governance](#task-adopt-10-governance), [ADOPT.10.release](#task-adopt-10-release), [ADOPT.10.runtime-proofs](#task-adopt-10-runtime-proofs), [ADOPT.11](#task-adopt-11) |
| Write scope | `Plan:ledger/adoption/baseline.md`<br>`Plan:ledger/README.md` |
| Validation | Read-only inspection of repositories, pull requests and registry receipts already recorded; no builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Baseline record with exact commit identities per repository, open pull request list and latest candidate identities; reviewed and merged in the Plan repository. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-02"></a>

### ADOPT.02 — Adopt DesktopPlatform

**Outcome.** The repository-wide adoption facts for DesktopPlatform (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the DesktopPlatform classification table is complete when every adoption slice of the repository is complete. The governance slice schedules the replacement of the design-policy graph check that still validates the retired work-package graph.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/adopt-02` and ledger record `ledger/tasks/adopt-02.md` in the Plan repository; task branch `task/adopt-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: DesktopPlatform repository record |
| Provides | DesktopPlatform adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.02.app-composition](#task-adopt-02-app-composition) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.assistant](#task-adopt-02-assistant) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.cloud](#task-adopt-02-cloud) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.device-bridge](#task-adopt-02-device-bridge) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.execution](#task-adopt-02-execution) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.extensions](#task-adopt-02-extensions) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.foundation](#task-adopt-02-foundation) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.governance](#task-adopt-02-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.native](#task-adopt-02-native) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.platform](#task-adopt-02-platform) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.policy](#task-adopt-02-policy) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.release](#task-adopt-02-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.runtime-proofs](#task-adopt-02-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.02.updater](#task-adopt-02-updater) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/DesktopPlatform.md`<br>`Plan:ledger/tasks/adopt-02.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-03"></a>

### ADOPT.03 — Adopt Contracts

**Outcome.** The repository-wide adoption facts for Contracts (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the Contracts classification table is complete when every adoption slice of the repository is complete. The accepted [WP-03.00](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.00) to [WP-03.02](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02) receipts are recorded as inherited by the contracts slice; every later Contracts task, starting with the [WP-03.03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) closures, is open.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/adopt-03` and ledger record `ledger/tasks/adopt-03.md` in the Plan repository; task branch `task/adopt-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: Contracts repository record |
| Provides | Contracts adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.03.contracts](#task-adopt-03-contracts) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.03.extensions](#task-adopt-03-extensions) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.03.governance](#task-adopt-03-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.03.release](#task-adopt-03-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/Contracts.md`<br>`Plan:ledger/tasks/adopt-03.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-04"></a>

### ADOPT.04 — Adopt ArcNotes

**Outcome.** The repository-wide adoption facts for ArcNotes (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the ArcNotes classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | ArcNotes (`C:\MyFile\Projects\ArcForges\ArcNotes`); integration owner: ArcNotes integration owner, the holder of `roles/integration-arcnotes` |
| Claim, branch and ledger | `claims/adopt-04` and ledger record `ledger/tasks/adopt-04.md` in the Plan repository; task branch `task/adopt-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: ArcNotes repository record |
| Provides | ArcNotes adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.04.app-composition](#task-adopt-04-app-composition) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.04.arcnotes](#task-adopt-04-arcnotes) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.04.governance](#task-adopt-04-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.04.release](#task-adopt-04-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.04.runtime-proofs](#task-adopt-04-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/ArcNotes.md`<br>`Plan:ledger/tasks/adopt-04.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-05"></a>

### ADOPT.05 — Adopt ArcScope

**Outcome.** The repository-wide adoption facts for ArcScope (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the ArcScope classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/adopt-05` and ledger record `ledger/tasks/adopt-05.md` in the Plan repository; task branch `task/adopt-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: ArcScope repository record |
| Provides | ArcScope adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.05.arcscope](#task-adopt-05-arcscope) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.05.governance](#task-adopt-05-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.05.release](#task-adopt-05-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.05.runtime-proofs](#task-adopt-05-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.05.simulator](#task-adopt-05-simulator) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/ArcScope.md`<br>`Plan:ledger/tasks/adopt-05.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-06"></a>

### ADOPT.06 — Adopt ArcSlate

**Outcome.** The repository-wide adoption facts for ArcSlate (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the ArcSlate classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | ArcSlate (`C:\MyFile\Projects\ArcForges\ArcSlate`); integration owner: ArcSlate integration owner, the holder of `roles/integration-arcslate` |
| Claim, branch and ledger | `claims/adopt-06` and ledger record `ledger/tasks/adopt-06.md` in the Plan repository; task branch `task/adopt-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: ArcSlate repository record |
| Provides | ArcSlate adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.06.arcslate](#task-adopt-06-arcslate) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.06.governance](#task-adopt-06-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.06.release](#task-adopt-06-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.06.runtime-proofs](#task-adopt-06-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/ArcSlate.md`<br>`Plan:ledger/tasks/adopt-06.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-07"></a>

### ADOPT.07 — Adopt Cloud

**Outcome.** The repository-wide adoption facts for Cloud (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the Cloud classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/adopt-07` and ledger record `ledger/tasks/adopt-07.md` in the Plan repository; task branch `task/adopt-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: Cloud repository record |
| Provides | Cloud adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.07.ai-routing](#task-adopt-07-ai-routing) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.cloud](#task-adopt-07-cloud) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.commerce](#task-adopt-07-commerce) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.device-bridge](#task-adopt-07-device-bridge) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.extensions](#task-adopt-07-extensions) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.governance](#task-adopt-07-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.harness](#task-adopt-07-harness) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.operations](#task-adopt-07-operations) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.policy](#task-adopt-07-policy) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.release](#task-adopt-07-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.runtime-proofs](#task-adopt-07-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.search](#task-adopt-07-search) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.07.simulator](#task-adopt-07-simulator) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/Cloud.md`<br>`Plan:ledger/tasks/adopt-07.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-08"></a>

### ADOPT.08 — Adopt AI

**Outcome.** The repository-wide adoption facts for AI (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the AI classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/adopt-08` and ledger record `ledger/tasks/adopt-08.md` in the Plan repository; task branch `task/adopt-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: AI repository record |
| Provides | AI adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.08.ai-routing](#task-adopt-08-ai-routing) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.08.extensions](#task-adopt-08-extensions) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.08.governance](#task-adopt-08-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.08.harness](#task-adopt-08-harness) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/AI.md`<br>`Plan:ledger/tasks/adopt-08.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-09"></a>

### ADOPT.09 — Adopt Web

**Outcome.** The repository-wide adoption facts for Web (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the Web classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/adopt-09` and ledger record `ledger/tasks/adopt-09.md` in the Plan repository; task branch `task/adopt-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: Web repository record |
| Provides | Web adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.09.governance](#task-adopt-09-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.09.operations](#task-adopt-09-operations) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.09.release](#task-adopt-09-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.09.runtime-proofs](#task-adopt-09-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.09.web](#task-adopt-09-web) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/Web.md`<br>`Plan:ledger/tasks/adopt-09.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-10"></a>

### ADOPT.10 — Adopt Mobile

**Outcome.** The repository-wide adoption facts for Mobile (main head, retained CI workflow inventory under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), package identities and pins, shared roots and source inventory) are recorded once for its slices to cite, and the Mobile classification table is complete when every adoption slice of the repository is complete.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/adopt-10` and ledger record `ledger/tasks/adopt-10.md` in the Plan repository; task branch `task/adopt-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: Mobile repository record |
| Provides | Mobile adoption record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* repository-wide facts are recorded against the same frozen heads and receipts as every slice |
| Completion prerequisites | **integration** [ADOPT.10.android](#task-adopt-10-android) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.10.governance](#task-adopt-10-governance) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.10.release](#task-adopt-10-release) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository<br>**integration** [ADOPT.10.runtime-proofs](#task-adopt-10-runtime-proofs) — slice recorded. *Why:* the repository adoption record closes after every slice of the repository |
| Unblocks | none |
| Write scope | `Plan:ledger/adoption/Mobile.md`<br>`Plan:ledger/tasks/adopt-10.md` |
| Validation | Review of merged source, retained CI results and receipts only; no new builds, downloads or runtime checks ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Repository adoption record with the repository-wide facts, links to every slice record, the combined classification table and any conflicts raised under [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-adopt-11"></a>

### ADOPT.11 — Reconcile Design and Plan documentation for adoption

**Outcome.** Documentation findings that affect adoption decisions are resolved or scheduled (including the pre-existing corpus citation drift recorded in the adoption stage document), the generated views are confirmed current, and the ledger shows which adoption slices are complete.

| Field | Value |
|---|---|
| Owning repository | Design (`C:\MyFile\Projects\ArcForges-Design-B`); integration owner: Design integration owner, the holder of `roles/integration-design`; also touches Plan |
| Claim, branch and ledger | `claims/adopt-11` and ledger record `ledger/tasks/adopt-11.md` in the Plan repository; task branch `task/adopt-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | adoption / S |
| Obligations | [P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — adoption stage: documentation reconciliation |
| Provides | documentation reconciliation record |
| Start prerequisites | **artifact** [ADOPT.01](#task-adopt-01) — frozen baseline record. *Why:* reconciliation uses the frozen baseline |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `Design:docs/**`<br>`Plan:ledger/adoption/documentation.md` |
| Validation | Documentation consistency and link review, delivery graph check and the existing corpus integrity check; no product builds ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Reconciliation record with checker results and any planning-change pull requests. |
| Baseline (unreviewed unless accepted) | not-started |

## Adoption slices

Each slice classifies the tasks of one repository and lane against the frozen baseline and, when it is recorded, opens those tasks except the ones it classifies as inherited ([DLV-22](../README.md#rule-dlv-22)). Slices are claimed and recorded separately (claim `claims/adopt-NN-<lane>`, record `ledger/tasks/adopt-NN-<lane>.md`); one reviewed pull request may carry several. Every task a slice classifies as inherited, including each accepted-baseline task in its scope, also gets its own record `ledger/tasks/<key>.md` with `status: inherited` ([ledger records produced by adoption](../adoption.md#3-ledger-records-produced-by-adoption)) in the same pull request as the slice record, so it never becomes ready; a task inherited with adjustment opens with its remaining scope. The repository adoption task records the repository-wide facts and closes after all of its slices.

| Slice | Repository | Lane | Tasks it opens | Accepted baseline in scope | Repository record |
|---|---|---|---|---|---|
| <a id="task-adopt-02-app-composition"></a>ADOPT.02.app-composition | DesktopPlatform | [Application composition](app-composition.md) | 6 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-assistant"></a>ADOPT.02.assistant | DesktopPlatform | [Embedded assistant](assistant.md) | 22 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-cloud"></a>ADOPT.02.cloud | DesktopPlatform | [Cloud core](cloud.md) | 2 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-device-bridge"></a>ADOPT.02.device-bridge | DesktopPlatform | [Application presence and tool bridge](device-bridge.md) | 3 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-execution"></a>ADOPT.02.execution | DesktopPlatform | [Execution engine](execution.md) | 9 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-extensions"></a>ADOPT.02.extensions | DesktopPlatform | [Extension platform and integrations](extensions.md) | 7 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-foundation"></a>ADOPT.02.foundation | DesktopPlatform | [Foundation values](foundation.md) | 7 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-governance"></a>ADOPT.02.governance | DesktopPlatform | [Family governance and policy tests](governance.md) | 4 | [GOV.01](governance.md#task-gov-01), [GOV.02](governance.md#task-gov-02), [GOV.03](governance.md#task-gov-03) | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-native"></a>ADOPT.02.native | DesktopPlatform | [Native producers and probes](native.md) | 25 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-platform"></a>ADOPT.02.platform | DesktopPlatform | [Desktop platform mechanisms](platform.md) | 56 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-policy"></a>ADOPT.02.policy | DesktopPlatform | [Dynamic policy and configuration](policy.md) | 1 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-release"></a>ADOPT.02.release | DesktopPlatform | [Release readiness and family release](release.md) | 2 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-runtime-proofs"></a>ADOPT.02.runtime-proofs | DesktopPlatform | [Runtime proofs](runtime-proofs.md) | 4 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-02-updater"></a>ADOPT.02.updater | DesktopPlatform | [Desktop distribution and update](updater.md) | 8 | none | [ADOPT.02](#task-adopt-02) |
| <a id="task-adopt-03-contracts"></a>ADOPT.03.contracts | Contracts | [Contracts schema closures](contracts.md) | 22 | [CON.90](contracts.md#task-con-90), [CON.91](contracts.md#task-con-91), [CON.92](contracts.md#task-con-92) | [ADOPT.03](#task-adopt-03) |
| <a id="task-adopt-03-extensions"></a>ADOPT.03.extensions | Contracts | [Extension platform and integrations](extensions.md) | 3 | none | [ADOPT.03](#task-adopt-03) |
| <a id="task-adopt-03-governance"></a>ADOPT.03.governance | Contracts | [Family governance and policy tests](governance.md) | 2 | none | [ADOPT.03](#task-adopt-03) |
| <a id="task-adopt-03-release"></a>ADOPT.03.release | Contracts | [Release readiness and family release](release.md) | 1 | none | [ADOPT.03](#task-adopt-03) |
| <a id="task-adopt-04-app-composition"></a>ADOPT.04.app-composition | ArcNotes | [Application composition](app-composition.md) | 2 | none | [ADOPT.04](#task-adopt-04) |
| <a id="task-adopt-04-arcnotes"></a>ADOPT.04.arcnotes | ArcNotes | [ArcNotes](arcnotes.md) | 35 | none | [ADOPT.04](#task-adopt-04) |
| <a id="task-adopt-04-governance"></a>ADOPT.04.governance | ArcNotes | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.04](#task-adopt-04) |
| <a id="task-adopt-04-release"></a>ADOPT.04.release | ArcNotes | [Release readiness and family release](release.md) | 1 | none | [ADOPT.04](#task-adopt-04) |
| <a id="task-adopt-04-runtime-proofs"></a>ADOPT.04.runtime-proofs | ArcNotes | [Runtime proofs](runtime-proofs.md) | 1 | none | [ADOPT.04](#task-adopt-04) |
| <a id="task-adopt-05-arcscope"></a>ADOPT.05.arcscope | ArcScope | [ArcScope](arcscope.md) | 27 | none | [ADOPT.05](#task-adopt-05) |
| <a id="task-adopt-05-governance"></a>ADOPT.05.governance | ArcScope | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.05](#task-adopt-05) |
| <a id="task-adopt-05-release"></a>ADOPT.05.release | ArcScope | [Release readiness and family release](release.md) | 1 | none | [ADOPT.05](#task-adopt-05) |
| <a id="task-adopt-05-runtime-proofs"></a>ADOPT.05.runtime-proofs | ArcScope | [Runtime proofs](runtime-proofs.md) | 1 | none | [ADOPT.05](#task-adopt-05) |
| <a id="task-adopt-05-simulator"></a>ADOPT.05.simulator | ArcScope | [ArcScope Cloud simulator](simulator.md) | 1 | none | [ADOPT.05](#task-adopt-05) |
| <a id="task-adopt-06-arcslate"></a>ADOPT.06.arcslate | ArcSlate | [ArcSlate](arcslate.md) | 41 | none | [ADOPT.06](#task-adopt-06) |
| <a id="task-adopt-06-governance"></a>ADOPT.06.governance | ArcSlate | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.06](#task-adopt-06) |
| <a id="task-adopt-06-release"></a>ADOPT.06.release | ArcSlate | [Release readiness and family release](release.md) | 1 | none | [ADOPT.06](#task-adopt-06) |
| <a id="task-adopt-06-runtime-proofs"></a>ADOPT.06.runtime-proofs | ArcSlate | [Runtime proofs](runtime-proofs.md) | 1 | none | [ADOPT.06](#task-adopt-06) |
| <a id="task-adopt-07-ai-routing"></a>ADOPT.07.ai-routing | Cloud | [Workers AI routing and metering](ai-routing.md) | 6 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-cloud"></a>ADOPT.07.cloud | Cloud | [Cloud core](cloud.md) | 58 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-commerce"></a>ADOPT.07.commerce | Cloud | [Commerce, entitlement and credits](commerce.md) | 15 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-device-bridge"></a>ADOPT.07.device-bridge | Cloud | [Application presence and tool bridge](device-bridge.md) | 9 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-extensions"></a>ADOPT.07.extensions | Cloud | [Extension platform and integrations](extensions.md) | 1 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-governance"></a>ADOPT.07.governance | Cloud | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-harness"></a>ADOPT.07.harness | Cloud | [Cloud Harness](harness.md) | 2 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-operations"></a>ADOPT.07.operations | Cloud | [Operations, support and trust and safety](operations.md) | 9 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-policy"></a>ADOPT.07.policy | Cloud | [Dynamic policy and configuration](policy.md) | 10 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-release"></a>ADOPT.07.release | Cloud | [Release readiness and family release](release.md) | 3 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-runtime-proofs"></a>ADOPT.07.runtime-proofs | Cloud | [Runtime proofs](runtime-proofs.md) | 1 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-search"></a>ADOPT.07.search | Cloud | [Knowledge search and retrieval](search.md) | 8 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-07-simulator"></a>ADOPT.07.simulator | Cloud | [ArcScope Cloud simulator](simulator.md) | 9 | none | [ADOPT.07](#task-adopt-07) |
| <a id="task-adopt-08-ai-routing"></a>ADOPT.08.ai-routing | AI | [Workers AI routing and metering](ai-routing.md) | 5 | none | [ADOPT.08](#task-adopt-08) |
| <a id="task-adopt-08-extensions"></a>ADOPT.08.extensions | AI | [Extension platform and integrations](extensions.md) | 1 | none | [ADOPT.08](#task-adopt-08) |
| <a id="task-adopt-08-governance"></a>ADOPT.08.governance | AI | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.08](#task-adopt-08) |
| <a id="task-adopt-08-harness"></a>ADOPT.08.harness | AI | [Cloud Harness](harness.md) | 7 | none | [ADOPT.08](#task-adopt-08) |
| <a id="task-adopt-09-governance"></a>ADOPT.09.governance | Web | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.09](#task-adopt-09) |
| <a id="task-adopt-09-operations"></a>ADOPT.09.operations | Web | [Operations, support and trust and safety](operations.md) | 4 | none | [ADOPT.09](#task-adopt-09) |
| <a id="task-adopt-09-release"></a>ADOPT.09.release | Web | [Release readiness and family release](release.md) | 1 | none | [ADOPT.09](#task-adopt-09) |
| <a id="task-adopt-09-runtime-proofs"></a>ADOPT.09.runtime-proofs | Web | [Runtime proofs](runtime-proofs.md) | 1 | none | [ADOPT.09](#task-adopt-09) |
| <a id="task-adopt-09-web"></a>ADOPT.09.web | Web | [Web](web.md) | 31 | none | [ADOPT.09](#task-adopt-09) |
| <a id="task-adopt-10-android"></a>ADOPT.10.android | Mobile | [Android companion](android.md) | 26 | none | [ADOPT.10](#task-adopt-10) |
| <a id="task-adopt-10-governance"></a>ADOPT.10.governance | Mobile | [Family governance and policy tests](governance.md) | 1 | none | [ADOPT.10](#task-adopt-10) |
| <a id="task-adopt-10-release"></a>ADOPT.10.release | Mobile | [Release readiness and family release](release.md) | 1 | none | [ADOPT.10](#task-adopt-10) |
| <a id="task-adopt-10-runtime-proofs"></a>ADOPT.10.runtime-proofs | Mobile | [Runtime proofs](runtime-proofs.md) | 1 | none | [ADOPT.10](#task-adopt-10) |
