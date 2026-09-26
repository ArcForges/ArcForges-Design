# Operations, support and trust and safety — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Service levels, incidents, runbooks, status, operator console, support, trust and safety, mail and push delivery, package review.

Tasks: 13 · Owning repositories: Cloud, Web · Integration owner(s): Cloud integration owner, Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [OPS.01](#task-ops-01) | Service levels and alerting | service | M | none | not-started |
| [OPS.02](#task-ops-02) | Incident process | service | M | [OPS.01](#task-ops-01) (artifact) | not-started |
| [OPS.03](#task-ops-03) | Runbooks and rehearsal | service | M | [OPS.02](#task-ops-02) (artifact) | not-started |
| [OPS.04](#task-ops-04) | Status page | service | M | [OPS.01](#task-ops-01) (artifact) | not-started |
| [OPS.05](#task-ops-05) | Operator console and support access | service | XL | [CON.14](contracts.md#task-con-14) (contract), [POL.05](policy.md#task-pol-05) (artifact) | not-started |
| [OPS.06](#task-ops-06) | Break-glass | service | M | [OPS.05](#task-ops-05) (artifact) | not-started |
| [OPS.07](#task-ops-07) | Support cases and in-product reporting | service | M | [OPS.05](#task-ops-05) (artifact), [CON.22](contracts.md#task-con-22) (contract) | not-started |
| [OPS.08](#task-ops-08) | Trust and safety | service | L | [OPS.07](#task-ops-07) (artifact), [OPS.05](#task-ops-05) (artifact) | not-started |
| [OPS.09](#task-ops-09) | Operational mail and provider drills | service | M | [CLOUD.12](cloud.md#task-cloud-12) (artifact), [OPS.02](#task-ops-02) (artifact) | not-started |
| [OPS.10](#task-ops-10) | Customer push delivery and registration lifecycle | service | L | [OPS.09](#task-ops-09) (artifact), [CON.22](contracts.md#task-con-22) (contract) | not-started |
| [OPS.11](#task-ops-11) | Package review and revocation console | service | M | [EXT.06](extensions.md#task-ext-06) (artifact), [CON.14](contracts.md#task-con-14) (contract), [OPS.05](#task-ops-05) (artifact) | not-started |
| [OPS.12](#task-ops-12) | Owned-artifact receipt | service | S | [OPS.11](#task-ops-11) (artifact), [AND.26](android.md#task-and-26) (artifact), [OPS.01](#task-ops-01) (artifact), [OPS.02](#task-ops-02) (artifact), [OPS.03](#task-ops-03) (artifact), [OPS.04](#task-ops-04) (artifact), [OPS.06](#task-ops-06) (artifact), [OPS.07](#task-ops-07) (artifact), [OPS.08](#task-ops-08) (artifact), [OPS.09](#task-ops-09) (artifact), [OPS.10](#task-ops-10) (artifact) | not-started |
| [OPS.13](#task-ops-13) | Operator console exercises real financial-owner and kill-switch RPCs end to end | integration | M | [COM.13](commerce.md#task-com-13) (artifact), [POL.05](policy.md#task-pol-05) (artifact), [OPS.05](#task-ops-05) (artifact), [CON.14](contracts.md#task-con-14) (artifact), [OPS.11](#task-ops-11) (artifact) | not-started |

## Tasks

<a id="task-ops-01"></a>

### OPS.01 — Service levels and alerting

**Outcome.** Service-level indicators measure user-visible success per capability group with realtime/managed-AI computed independently, error budgets are visible, and every deployed alert routes correctly and names an existing runbook.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-01` and ledger record `ledger/tasks/ops-01.md` in the Plan repository; task branch `task/ops-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.00](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.00) — full |
| Provides | slo-sli-definitions; alert-routing |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.02](#task-ops-02), [OPS.04](#task-ops-04), [OPS.12](#task-ops-12) |
| Write scope | `Cloud:deploy/monitoring/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Offline tests: indicator correctness against synthetic failures, dependency-attribution, alert-routing, alert-to-runbook completeness assertion. |
| Completion evidence | Alert-to-runbook completeness assertion (every deployed alert names an existing runbook). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-02"></a>

### OPS.02 — Incident process

**Outcome.** A shared four-severity ladder drives incident state tracked independently of production, a possible personal-data breach classifies automatically at the highest severity with the statutory notification clock as a hard deadline, and post-incident review produces runbook updates.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-02` and ledger record `ledger/tasks/ops-02.md` in the Plan repository; task branch `task/ops-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.01](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.01) — full |
| Provides | incident-severity-ladder; incident-state-system |
| Start prerequisites | **artifact** [OPS.01](#task-ops-01) — alert routing to trigger incidents from. *Why:* the incident process consumes paging alerts as its primary trigger |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.03](#task-ops-03), [OPS.09](#task-ops-09), [OPS.12](#task-ops-12) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Support/**/Incidents/**` |
| Validation | Offline tests: severity-classification exercise, independence assertion for the incident system, breach-classification test. |
| Completion evidence | Breach-classification-automatic-highest-severity test result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-03"></a>

### OPS.03 — Runbooks and rehearsal

**Outcome.** Every required runbook is written with preconditions, decision points, exact steps, verification and rollback, and every runbook for an implemented owner carries at least one dated rehearsal record.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-03` and ledger record `ledger/tasks/ops-03.md` in the Plan repository; task branch `task/ops-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.02](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.02) — full |
| Provides | runbook-set; rehearsal-records |
| Start prerequisites | **artifact** [OPS.02](#task-ops-02) — the incident process the runbooks are executed within. *Why:* a runbook is 'executable in an incident'; the incident system must exist to rehearse against |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.51](cloud.md#task-cloud-51) — the DR drill programme's runbooks. *Why:* recovery runbooks depend on [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) (backup/recovery, out of this package's scope) to have something to rehearse<br>**integration** [HAR.04](harness.md#task-har-04) — Cloud Harness provider-failure/effect-certainty procedures. *Why:* CF-related runbook cases are explicitly named as awaiting [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46)/[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) and remain pending until WP50 joins them per [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)'s own completion gate text |
| Unblocks | [OPS.12](#task-ops-12) |
| Write scope | `Cloud:docs/runbooks/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Completeness check against the required runbook set (docs/requirements/products/arcforges-cloud.md §9.1); a dated rehearsal record per runbook, executed under existing environment per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no new infra spun up for the rehearsal itself). |
| Completion evidence | Completeness check result; dated rehearsal record per implemented-owner runbook; explicit pending markers for DR/CF cases awaiting [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46)/[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52). |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Contributes to [PG-04](../../../assurance/open-gates-register.md#rule-pg-04) (runbook rehearsal, Operations Owner, currently OPEN per open-gates-register.md). |

<a id="task-ops-04"></a>

### OPS.04 — Status page

**Outcome.** An independently hosted status page publishes only user-facing capability components with an explicit reviewed health-to-component mapping, survives a full Cloud outage, and publishes its emergency alternate URL in at least three places.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/ops-04` and ledger record `ledger/tasks/ops-04.md` in the Plan repository; task branch `task/ops-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.03](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.03) — full<br>[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) browser matrix acceptance; status page supported/degraded/blocked browser behavior, static no-JS readability — browser matrix acceptance; status page supported/degraded/blocked browser behavior, static no-JS readability<br>[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) Browser matrix acceptance (browser-support.v1 supported/degraded/blocked) — package-level obligation contribution |
| Provides | status-page; capability-health-mapping |
| Start prerequisites | **artifact** [OPS.01](#task-ops-01) — capability health signals to map from. *Why:* the published component state is a reviewed mapping from internal capability health, which OPS.01 is the source of |
| Entry condition | [ADOPT.09.operations](adoption.md#task-adopt-09-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.12](#task-ops-12) |
| Write scope | `Web:apps/site/**/status/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Offline/staged tests: full-cloud-outage availability, per-capability mapping, vendor-name-absence scan; static no-JS readability check per browser-support.v1. |
| Completion evidence | Full-cloud-outage availability test; vendor-name-absence scan (zero hits). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Web repo HEAD 120f2097 has apps/site and apps/app present but essentially empty (bootstrap only). |

<a id="task-ops-05"></a>

### OPS.05 — Operator console and support access

**Outcome.** The operator console runs on a separate origin with a separate identity system, never in public navigation; support access is explicit, scoped, time-bounded, consented and audited; a destructive action needs a second authorised operator; and no parallel unversioned admin API exists.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/ops-05` and ledger record `ledger/tasks/ops-05.md` in the Plan repository; task branch `task/ops-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / XL · early risk proof |
| Obligations | [WP-45.04](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.04) — all work except the parts mapped to OPS.13<br>[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) Operator contract closure — the real console join — operator contract closure; the real console join — wiring every generated role/method pair into the console UI<br>[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) browser matrix acceptance; supported/degraded/blocked browser behavior for the operator console's own flows — browser matrix acceptance; supported/degraded/blocked browser behavior for the operator console's own flows<br>[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) Browser matrix acceptance (browser-support.v1 supported/degraded/blocked) — package-level obligation contribution |
| Provides | operator-console; support-access-grant-model |
| Start prerequisites | **contract** [CON.14](contracts.md#task-con-14) — the OperatorService full RPC surface. *Why:* same gap noted at COM.13/POL.05 — the console has nothing to call until the operator RPCs are generated<br>**artifact** [POL.05](policy.md#task-pol-05) — the kill-switch RPC implementation. *Why:* the console must exercise kill-switch activation per the same generated role/method matrix |
| Entry condition | [ADOPT.09.operations](adoption.md#task-adopt-09-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [COM.13](commerce.md#task-com-13) — the financial-owner RPC implementations. *Why:* the console must exercise grant/revoke/issueCredit/adjustCredit/refund end to end per [WP-45.04](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.04)'s testing requirement |
| Unblocks | [CLOUD.64](cloud.md#task-cloud-64), [OPS.06](#task-ops-06), [OPS.07](#task-ops-07), [OPS.08](#task-ops-08), [OPS.11](#task-ops-11), [OPS.13](#task-ops-13), [WEB.31](web.md#task-web-31) |
| Write scope | `Web:apps/app/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append), [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append) |
| Validation | Offline/staged tests: silent-impersonation negative, scope/expiry, two-operator requirement, audit-completeness, parallel-admin-API-absence assertion, every generated role/method pair (allowed and refused), double-execution-of-one-approval negative; browser-support.v1 supported/degraded/blocked behavior per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no live E2E browser matrix in routine CI). |
| Completion evidence | Silent-impersonation negative result; two-operator requirement result; full role/method matrix exercised (allowed and refused). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Web apps/app has essentially one file at HEAD 120f2097 — no operator/admin/console code observed. |
| Notes | [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) ('an operator never silently becomes a user') is a headline security invariant for the whole package; the silent-impersonation negative test is worth proving early against a minimal console skeleton before building every case-type UI on top. |

<a id="task-ops-06"></a>

### OPS.06 — Break-glass

**Outcome.** A distinct, alarmed emergency-access path requires justification, expires automatically, alerts immediately, requires mandatory post-hoc review, and is visible to the affected account owner.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-06` and ledger record `ledger/tasks/ops-06.md` in the Plan repository; task branch `task/ops-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.05](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.05) — full |
| Provides | break-glass-path |
| Start prerequisites | **artifact** [OPS.05](#task-ops-05) — the operator identity/audit infrastructure. *Why:* break-glass is a distinct path alongside normal operator access and reuses the same audit system ([BR-08](../../../architecture/14-build-packaging-and-release.md#rule-br-08)) |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.12](#task-ops-12) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Support/**/BreakGlass/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Offline tests: activation alerting, expiry enforcement, review-requirement, owner-visibility. |
| Completion evidence | Expiry-enforcement test; owner-visibility test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-07"></a>

### OPS.07 — Support cases and in-product reporting

**Outcome.** In-product problem reporting produces a support reference without attaching user data by default, support cases link to diagnostic references rather than content, and the case lifecycle carries defined response expectations.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-07` and ledger record `ledger/tasks/ops-07.md` in the Plan repository; task branch `task/ops-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.06](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.06) — full |
| Provides | support-case-model |
| Start prerequisites | **artifact** [OPS.05](#task-ops-05) — operator case-handling surface. *Why:* support cases are worked by operators through the console's case model<br>**contract** [CON.22](contracts.md#task-con-22) — published support operations. *Why:* support cases implement the generated service |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.08](#task-ops-08), [OPS.12](#task-ops-12) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Support/**/Cases/**` |
| Validation | Offline tests: no-data-by-default assertion, reference-resolution, lifecycle. |
| Completion evidence | No-data-by-default assertion result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-08"></a>

### OPS.08 — Trust and safety

**Outcome.** Community report intake drives a proportionate enforcement ladder with every action recorded and communicated, account enforcement states integrate with the account model, and appeals have a defined path and response expectation.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-08` and ledger record `ledger/tasks/ops-08.md` in the Plan repository; task branch `task/ops-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-45.07](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.07) — full |
| Provides | enforcement-ladder; appeal-process |
| Start prerequisites | **artifact** [OPS.07](#task-ops-07) — the support case/reference model. *Why:* community reports are worked as a case type reusing OPS.07's reference-resolution model<br>**artifact** [OPS.05](#task-ops-05) — operator audit infrastructure. *Why:* every enforcement action must be recorded to the audit system operators use |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.12](#task-ops-12) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.TrustSafety/**` |
| Validation | Offline tests: ladder-progression, communication-completeness, appeal-path, enforcement-audit. |
| Completion evidence | Ladder-progression test; appeal-path test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-09"></a>

### OPS.09 — Operational mail and provider drills

**Outcome.** Transactional/broadcast email use the real [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) Postmark/SES adapters with separated streams; outage and reconciliation drills are rehearsed under a prepared secondary path; and the private security-advisory intake-through-publication process is complete with in-product containment/revocation attention.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-09` and ledger record `ledger/tasks/ops-09.md` in the Plan repository; task branch `task/ops-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.08](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.08) — full<br>[WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) Producer prerequisites (WP45.08 must consume real WP22 mail, no fixture) — producer prerequisites; consuming [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) real mail artifacts without deferring [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22)'s own gate; package-level obligation contribution |
| Provides | operational-mail-drills; security-advisory-process |
| Start prerequisites | **artifact** [CLOUD.12](cloud.md#task-cloud-12) — native/browser authentication's real Postmark/SES adapters. *Why:* [WP-45.08](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.08) text is explicit: 'Use WP22 real Postmark/SES adapters'; runtime mail fixtures are explicitly absent for this task per [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)'s own 'Producer prerequisites' note<br>**artifact** [OPS.02](#task-ops-02) — the incident process. *Why:* outage/reconciliation drills are rehearsed as incidents |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.10](#task-ops-10), [OPS.12](#task-ops-12) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Notification/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.TrustSafety/**/Advisories/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Offline tests where possible (spoofed/replayed callback, bounced/complained suppression, content-redaction) plus recorded live-provider drill evidence (unknown send, DNS readiness, independent status/incident during a real Cloud outage) kept outside routine CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Live operational evidence and rollback-contact record; signed advisory authenticity and affected-version-matching results; no disclosure before approved publication. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | This task cannot use a mail substitute — [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) explicitly states runtime mail fixtures are absent and that [WP-45.08](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.08) 'is not the first email producer,' i.e. it must consume [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22)'s real adapters from day one. |

<a id="task-ops-10"></a>

### OPS.10 — Customer push delivery and registration lifecycle

**Outcome.** Notification.IPushSender sends through a typed FCM HTTP v1 credential adapter with a unique delivery-intent outbox, generation/revocation checks and the exact push.v1 profile, working against an actual isolated Firebase project with bounded, fenced recovery.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-10` and ledger record `ledger/tasks/ops-10.md` in the Plan repository; task branch `task/ops-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-45.09](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.09) — all work except the parts mapped to AND.26 |
| Provides | fcm-push-sender |
| Start prerequisites | **artifact** [OPS.09](#task-ops-09) — the Notification module's adapter pattern and outbox convention. *Why:* IPushSender is expected to follow the same adapter/outbox shape the mail adapters establish in the same Notification module<br>**contract** [CON.22](contracts.md#task-con-22) — published notification operations including push registration. *Why:* push registration and delivery acknowledgement use the generated operations |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.26](android.md#task-and-26) — physical Android device receipt, no-GMS and permission evidence. *Why:* [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) explicitly remains open until [WP-32](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) supplies physical-device evidence; this task proves provider acceptance only, labelled separately from device delivery |
| Unblocks | [AND.26](android.md#task-and-26), [OPS.12](#task-ops-12) |
| Permitted substitutes | [SUB-fcm-recorded-responses](../substitutes.md#sub-fcm-recorded-responses) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Notification/**/Push/**` |
| Validation | Live isolated Firebase project send (kept outside routine CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), real service) plus offline tests for token-rotation race, crash-after-acceptance duplicates, TTL expiry, revoke-before-send, no-secret-logging. |
| Completion evidence | Recorded invalid-token/payload/project/rate-limit responses; no-secret-logging scan. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Named as required-real-early scaffolding in implementation-sequence §3.1 (recorded FCM WP45.09 to WP32 proves device receipt) — unlike payment/mail, no fixture stands in for the server-side send itself; it is real against an isolated Firebase project from the start. |

<a id="task-ops-11"></a>

### OPS.11 — Package review and revocation console

**Outcome.** The operator console integrates [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41) PackageCatalog operator methods (catalogReview/catalogRevoke) with independent operator authentication, step-up/evidence and audit, and review/revocation decisions visibly affect real signed catalog consumers.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/ops-11` and ledger record `ledger/tasks/ops-11.md` in the Plan repository; task branch `task/ops-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-45.10](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.10) — all work except the parts mapped to OPS.13 |
| Provides | package-review-console |
| Start prerequisites | **artifact** [EXT.06](extensions.md#task-ext-06) — the PackageCatalog producer's operator methods (GetCatalogSubmission etc.). *Why:* producer-artifacts-and-integration.md records an explicit WP41.05 to WP45.10 edge; this task integrates [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41)'s methods rather than reimplementing catalog review logic<br>**contract** [CON.14](contracts.md#task-con-14) — the catalogReview/catalogRevoke operator RPC shapes. *Why:* same operator-proto gap as COM.13/POL.05/OPS.05<br>**artifact** [OPS.05](#task-ops-05) — the operator console's identity/step-up/audit shell. *Why:* [WP-45.10](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.10) explicitly reuses 'independent operator authentication, step-up/evidence and audit' from the console rather than building a second one |
| Entry condition | [ADOPT.09.operations](adoption.md#task-adopt-09-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.12](#task-ops-12), [OPS.13](#task-ops-13) |
| Write scope | `Web:apps/app/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append), [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append) |
| Validation | Offline tests: customer/PAT denial, changed-proposal-hash, replay, revoked-package, failed-index-publication/retry. |
| Completion evidence | Revocation affecting a real signed catalog consumer, with recorded operator evidence. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-12"></a>

### OPS.12 — Owned-artifact receipt

**Outcome.** The package-level owned-artifact/real-integration receipt is recorded confirming actual role/redaction/status/support-case behavior and actionable CF/R2 failure diagnostics, with no second Node/operations business host.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/ops-12` and ledger record `ledger/tasks/ops-12.md` in the Plan repository; task branch `task/ops-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Package acceptance | Records the [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-45.90](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.90) — full |
| Provides | wp45-closure-receipt |
| Start prerequisites | **artifact** [OPS.11](#task-ops-11) — the last domain producer's evidence to attach. *Why:* the receipt aggregates every amended §5 producer/consumer result<br>**artifact** [AND.26](android.md#task-and-26) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.01](#task-ops-01) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.02](#task-ops-02) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.03](#task-ops-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.04](#task-ops-04) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.06](#task-ops-06) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.07](#task-ops-07) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.08](#task-ops-08) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.09](#task-ops-09) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [OPS.10](#task-ops-10) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.operations](adoption.md#task-adopt-07-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.06](release.md#task-rel-06), [REL.09](release.md#task-rel-09) |
| Write scope | `Cloud:eng/provenance/records/**` |
| Validation | Aggregation of OPS.01-11 evidence; no-second-host architecture assertion. |
| Completion evidence | The owned-artifact/real-integration receipt; no-second-Node-host assertion. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ops-13"></a>

### OPS.13 — Operator console exercises real financial-owner and kill-switch RPCs end to end

**Outcome.** an authorised operator can actually grant/revoke/issueCredit/adjustCredit/refund and activate a kill switch through the console UI, not just via direct RPC test calls

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/ops-13` and ledger record `ledger/tasks/ops-13.md` in the Plan repository; task branch `task/ops-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-45.04](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.04) — exercise every generated role/method pair via the actual console UI<br>[WP-45.10](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.10) — real operator console join |
| Start prerequisites | **artifact** [COM.13](commerce.md#task-com-13) — real, delivered outcome of COM.13 (Operator financial-owner proposal/approval operations). *Why:* this integration exercises the real operator financial-owner proposal/approval operations instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [POL.05](policy.md#task-pol-05) — real, delivered outcome of POL.05 (Kill switches). *Why:* this integration exercises the real kill switches instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [OPS.05](#task-ops-05) — real, delivered outcome of OPS.05 (Operator console and support access). *Why:* this integration exercises the real operator console and support access instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CON.14](contracts.md#task-con-14) — real, delivered outcome of CON.14 (Operator control service (OperatorService, full §9/9.1/9.2 protocol)). *Why:* this integration exercises the real operator control service (OperatorService, full §9/9.1/9.2 protocol) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [OPS.11](#task-ops-11) — real, delivered outcome of OPS.11 (Package review and revocation console). *Why:* this integration exercises the real package review and revocation console instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.09.operations](adoption.md#task-adopt-09-operations) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.13](commerce.md#task-com-13) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | an authorised operator can actually grant/revoke/issueCredit/adjustCredit/refund and activate a kill switch through the console UI, not just via direct RPC test calls |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as CON.98. |
