<a id="rule-wp-46"></a>

# WP-46 — Backup, Disaster Recovery and Data Health

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `25`, `45` · Downstream: `50`

> **Goal.** Make recovery a proven fact rather than a configured intention: five backup layers, cross-provider and cross-region copies, point-in-time restore, a rehearsed region rebuild, and continuous data-health detection — with a **green backup job never counting as a proven restore**.

---

## 1. Scope and purpose

**In scope.** The five backup layers; retention and cross-provider copies; point-in-time restore; blob restore; the region rebuild procedure; the disaster-recovery drill programme; data-health detection and repair; export and realm migration; and the user-facing recovery paths.

**Out of scope.** Local device backup responsibility, which belongs to the user's own system and is documented rather than implemented. Operational alerting itself (`45`).

**Why this package exists.** [L-13](../../assurance/release-gates.md#rule-l-13) in the release gates requires a **proven restore**, not merely a green backup job. [DR-04](../../requirements/products/arcforges-cloud.md#rule-dr-04) states plainly that a compressed archive is not a backup strategy. Neither is satisfiable without rehearsal.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/07-sync-conflict-and-backup.md`](../../architecture/07-sync-conflict-and-backup.md) | The five backup layers, data health and realm migration |
| [`../../requirements/products/arcforges-cloud.md`](../../requirements/products/arcforges-cloud.md) `§9.2` | Disaster recovery posture and recovery objectives |
| [`../../requirements/03-cloud-services-and-sync.md`](../../requirements/03-cloud-services-and-sync.md) | Backup, data health and export requirements |
| [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25), [WP-45](45-operations-support-and-trust-safety.md#rule-wp-45) output | Committed state as the backup subject, and the incident framework drills run inside |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **High durability is not backup.** Storage durability protects against hardware failure, not against deletion, corruption or a bad migration. |
| BR-02 | **A green backup job is not a proven restore.** Only an executed restore counts. |
| BR-03 | **Backups exist across providers and regions**, so a single provider incident cannot destroy every copy. |
| BR-04 | **Disaster recovery is single-primary-region plus zone redundancy plus cross-region and cross-provider backup plus a tested rebuild** — not active-active. |
| BR-05 | **A region rebuild is a tested procedure**, exercised in a full drill. |
| BR-06 | **Recovery objectives are internal engineering objectives** until a drill justifies publishing anything. |
| BR-07 | **Data health is continuous detection**, not an occasional audit, with a repair path per anomaly class. |
| <a id="rule-br-08"></a>BR-08 | **Export is a first-class product capability** and remains available regardless of subscription state where the data is the user's own. |
| BR-09 | **A restore never silently overwrites newer data**; a restore is an explicit, scoped, audited operation. |
| BR-10 | **Backup integrity is verified continuously**, not assumed from job success. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `deploy/backup/` | Backup configuration per layer, retention, cross-provider replication |
| `src/Cloud/ArcForges.Cloud.Modules.Operations/` | Data health detection, repair actions, restore orchestration, drill records |
| `src/Cloud/ArcForges.Cloud.Modules.Resource/` | Blob backup, verification and restore paths |
| `src/Cloud/ArcForges.Cloud.Migrations/` | Migration-failure recovery integrated with restore |
| `docs/runbooks/` in the implementation repository | Restore, rebuild, replay and repair runbooks with rehearsal records |
| `tests/CloudIntegrationTests/Recovery/` | Restore, corruption, orphan and drill-verification suites |

**Major types introduced.** `BackupLayer`, `BackupPolicy`, `BackupVerification`, `RestoreRequest`, `RestoreScope`, `PointInTimeTarget`, `RegionRebuildPlan`, `DisasterRecoveryDrill`, `DataHealthCheck`, `AnomalyClass`, `RepairAction`, `RealmMigration`.

---

## 5. Required implementation work

<a id="rule-wp-46.00"></a>

### WP-46.00 — The five backup layers

**What must be fully done.** Each layer implemented with its own scope, frequency, retention and verification: the transactional database, object storage, configuration and infrastructure definitions, secrets metadata, and the audit store. Cross-provider and cross-region copies for the layers that require them.

**Testing requirements.** Per-layer backup and verification runs; a cross-provider copy verification; a retention-enforcement test.

**Completion gate.** Every layer backs up, verifies and retains per policy, with cross-provider copies verified.

<a id="rule-wp-46.01"></a>

### WP-46.01 — Point-in-time and blob restore

**What must be fully done.** Account for logged stream rows in physical backup/WAL retention; purge restored presentation before traffic and reconcile unknown provider intents without repeating calls.  Point-in-time database restore to a chosen instant, and blob restore including cross-provider restore. A restore is scoped, explicit and audited, and never silently overwrites newer data.

**Testing requirements.** Restore while a stream/attempt is in flight and verify durable Task fallback, retained liability and no automatic dispatch.  A point-in-time restore to a chosen instant with verification; a cross-provider blob restore; a negative test asserting a restore cannot silently overwrite newer data.

**Completion gate.** TTL is not falsely presented as deletion from physical backups.  **A point-in-time restore and a cross-provider blob restore are both proven by execution**, and no restore silently overwrites newer data.

<a id="rule-wp-46.02"></a>

### WP-46.02 — Region rebuild

**What must be fully done.** A rebuild procedure from infrastructure definitions plus backups, producing a working environment. The procedure is documented as an executable runbook and rehearsed.

**Testing requirements.** A full rebuild rehearsal into a clean environment with functional verification afterwards.

**Completion gate.** A region rebuild from infrastructure definitions plus backups produces a verified working environment.

<a id="rule-wp-46.03"></a>

### WP-46.03 — Drill programme

**What must be fully done.** A recurring disaster-recovery drill programme covering database failover, point-in-time restore, blob restore, broker backlog and dead-letter replay, realtime outage, provider outage, deployment rollback, migration failure and region rebuild. Each drill produces a dated record and any runbook corrections it revealed.

**Testing requirements.** A completed drill cycle with dated records; a runbook-update assertion for every correction found.

**Completion gate.** A complete drill cycle is executed with dated records, and every correction found updated its runbook.

<a id="rule-wp-46.04"></a>

### WP-46.04 — Data health

**What must be fully done.** Continuous detection for divergence, missing blobs, orphan references, stale cursors, accounting mismatches and integrity failures, each with a repair action and an alert threshold. A health dashboard reflects real verification, not job success.

**Testing requirements.** Induced anomaly per class, each detected and repaired; a dashboard-truthfulness test asserting it reflects verification rather than job completion.

**Completion gate.** **Every anomaly class is detected and repaired**, and the health dashboard reflects verified state rather than job success.

<a id="rule-wp-46.05"></a>

### WP-46.05 — Export and realm migration

**What must be fully done.** Complete user-data export available regardless of subscription state where the data is the user's own, and realm migration moving a workspace's data with verification and no silent loss.

**Testing requirements.** Export completeness against every synced content kind; a subscription-lapsed export test; a realm migration with verification.

**Completion gate.** Export is complete and available with a lapsed subscription, and realm migration verifies its result.

<a id="rule-wp-46.06"></a>

### WP-46.06 — Backup health as a gate

**What must be fully done.** The backup health dashboard is green **with a proven restore**, and backup lag beyond objective is a page-worthy alert. The evidence for [L-13](../../assurance/release-gates.md#rule-l-13) is assembled.

**Testing requirements.** A lag-alert test; assembled evidence linking each backup layer to a dated restore proof.

**Completion gate.** The backup health gate is satisfied by dated restore proofs, not by job success — supplying the evidence for [L-13](../../assurance/release-gates.md#rule-l-13).

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Backup, restore and health-check state |
| Protocol | Export contracts |
| UI | Export, data health and account recovery surfaces |
| Security | Restore is a privileged, audited operation; backups carry the same protection as live data |
| Platform | Cross-provider and cross-region topology |
| Migration | Migration failure has a tested recovery path |
| Compatibility | Restored data must be readable by the current version |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Per-layer backup, verification and retention results | [WP-46.00](#rule-wp-46.00) |
| Point-in-time and cross-provider restore proofs | [WP-46.01](#rule-wp-46.01) |
| Region rebuild rehearsal record with functional verification | [WP-46.02](#rule-wp-46.02) |
| Dated drill cycle records and runbook corrections | [WP-46.03](#rule-wp-46.03) |
| Per-anomaly detection and repair results; dashboard truthfulness | [WP-46.04](#rule-wp-46.04) |
| Export completeness and realm migration verification | [WP-46.05](#rule-wp-46.05) |
| Backup lag alert and assembled restore-proof evidence | [WP-46.06](#rule-wp-46.06) |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Every backup layer backs up, verifies and retains per policy, with cross-provider copies verified.
2. **A point-in-time restore and a cross-provider blob restore are both proven by execution**; no restore silently overwrites newer data.
3. A region rebuild from infrastructure definitions plus backups produces a verified working environment.
4. A complete drill cycle is executed with dated records, and every correction found updated its runbook.
5. **Every data-health anomaly class is detected and repaired**, and the dashboard reflects verified state rather than job success.
6. Export is complete and available with a lapsed subscription; realm migration verifies its result.
7. **The backup health gate is satisfied by dated restore proofs**, supplying the evidence for [L-13](../../assurance/release-gates.md#rule-l-13).

---

## 9. Dependencies

**Upstream — all must be complete.**

- [25 — Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md)
- [45 — Operations, Support and Trust & Safety](45-operations-support-and-trust-safety.md)

**Downstream — these consume this package’s completed output.**

- [50 — Full-Platform Production Release](50-full-platform-production-release.md)
