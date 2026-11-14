# Contract, runtime and data migration

## Published contract versus runtime retirement

The audit records the actual consumers and pinned cohorts. New `arcforges.sandbox.v2` and `arcforges.management.v2` namespaces describe V2; the existing `arcforges.local.sandbox.v1` remains DesktopPlatform ContentSandbox. Never reuse a v1 message/field number for a different meaning or repurpose ContentSandbox as CLI Sandbox Core.

**Stop consuming:** migrate ArcForges and Go Center to explicit V2 APIs and remove their obsolete runtime route/client registrations. **Document retirement:** mark old source schemas as retired for ArcForges V2 with their replacement and last consumer inventory. **Incompatible source deletion:** only after the consumer inventory proves no retained independent product needs the schema; use an explicitly new major namespace/package surface when incompatibility is unavoidable. Already published versions remain downloadable and unchanged; no registry unpublish/deprecation/delete action is authorized. Continued old packages are immutable distribution history, not a maintained V1 execution path.

The consumer cutover inventory includes ArcForges, Go Center, old C# Cloud, Web, DesktopPlatform, Mobile, AI, ArcScope, ArcSlate and ArcNotes. Do not force unrelated products to implement V2. Keep only shared APIs they actually use, remove ArcForges-specific obsolete consumers and build dependencies, and verify independent product compile boundaries in the designated venues.

## Node upgrade from schema 15

1. Read schema history/checksums/min-reader and inventory actual installations. Stop new V1 task submission. Drain owned Task/Attempt processes, or request explicit stop; do not translate an executing Attempt into a V2 Run whose confinement was never established.
2. Resolve or preserve all unknown file-operation receipts, quarantine entries, held native identities, recovery-generation floors and pending audits. A new schema must not discard them. If an unsafe unresolved operation prevents contraction, keep the migration checkpoint blocked, not a permanent old service route.
3. Create a consistent backup and manifest of owned paths outside arbitrary host mounts. Append expand migrations with V2 tables and migration receipts. Historical V1 run/task records can be exported as read-only history with original IDs; they are never relabeled as V2 executions. Workspace roots are not auto-owned sandbox roots: offer explicit import/copy/adoption only after ownership/access review.
4. Start new Core against V2 tables with old execution APIs disabled. Test fresh install and schema15 upgrade. Preserve rollback to the pre-migration backup until acceptance; after irreversible contraction, binary downgrade alone is refused by min-reader.
5. Remove old Task/Attempt/queue/dependency/AI/cache/CAS/toolchain/LAN/mobile live tables and views through a forward contract migration, after receipts/journals are settled or copied to the retained reconciliation store and all runtime consumers removed. The 0001–0015 migration files remain immutable for upgrades/audit.

## Center schema 10 and 11

The last recorded deployment baseline is schema10 with narrow/Hello-only evidence; schema11 code includes the security-successor admission floor. The user's earlier external bootstrap/deployment remained deferred. **Appending 0012 is not itself a valid upgrade path.** Applied SQL checksums and 0011 safeguards cannot be deleted or edited. A dedicated V2 migration task must qualify source/runtime producer identities, the existing credential floor and restore safeguards, then supply a reviewed finite maintenance transition or an officially admitted successor that passes them.

Test three fixtures separately: fresh database, actually deployed schema10, and schema11 already applied. Document the source cohort, native/Go/Contracts compatibility, changed grants, backup, stale receipts, credential epoch, rollback/restore compatibility and exact migration order. An unproven provider authority boundary keeps activation blocked. No production data or credential is read by an agent as an expedient probe. See [Center store](cloud-store.md) for the target PostgreSQL model and exact migration constraints.

## Removal order and rollback

Retire disconnected desktop scaffolding and cancelled future configs first. Preserve the old critical executor only until both MXC profiles and resources are proven. Cut over new Core and local CLI, then the explicit Center methods and Web pages. Drain old consumers; remove old launchers, Task/Attempt/DAG/retry, file workspace routes, C# Center and dead dependencies. Finally contract live schemas and packaging inventories. Do not leave TODO implementations, disabled empty projects, a generic old dispatcher or a permanent feature-switched dual runtime.

Rollback before cutover restores the last accepted cohort and database backup without rewriting history. Rollback after irreversible deletion requires explicit restore and data-loss accounting; it never pretends newly created V2 data is readable by a V1 binary. A failed engine experiment blocks executor deletion. A failed data migration leaves service in maintenance and preserves backup/journal; it does not erase the database to make tests green.
