# 12 — Distribution, updates and rollback

Ship Node, CLI, per-Run supervisor and the admitted official MXC runtime as a coherent signed Windows/Linux x64 cohort initially; architecture expansion requires its own real-host evidence. Native AOT publication uses locked dependency graphs and emits no unexplained trimming/AOT warnings. Blazor is a separate browser asset build; Go Center images include their own provenance and PostgreSQL migration version. No GUI/mobile app, Node.js product runtime, compiler adapter, cache daemon or C# Center is installed.

The MXC package/executor must match the admitted version, schema and CPU architecture. Preserve official signatures and notices; record SHA-256, package origin, redistribution permission/license, SBOM and transitive native dependencies. Do not call an arbitrary `wxc-exec` found on PATH. Installation checks OS backend prerequisites and reports exact unsupported builds or privileges; it does not silently modify security policy, enable WSL or fall back to plain processes.

## Upgrade protocol

1. Stage verified bytes beside the active version; validate signatures and integrity at the actual download/install handoff.
2. Probe compatibility with current Node schema/min-reader, MXC schema/profile and supervisor protocol. Save a backup consistent with SQLite WAL and the documented Center backup procedure.
3. Stop new admission; keep live supervisors on their original cohort until they exit, or explicitly drain/stop them before a hard incompatible upgrade. Do not replace a live process's native runtime in place.
4. Apply additive migrations transactionally, start the new Node, authenticate and reconcile old supported supervisor epochs, and run a bounded health check.
5. Switch the current version only after readiness. Record cohort and schema transition. A failed upgrade restores the old binary only if its minimum reader permits the store; otherwise restore the tested backup with explicit data-loss accounting.

Irreversible contract migrations require complete drain, an explicit rollback checkpoint and a tested restore path. Never lower `min_reader` to make an old process accept incompatible data. Retain a finite compatibility window for upgrading existing supervisors; remove it after the consumer cutover task. Do not preserve a permanent V1 Task runtime.

## Release gates and services

Self-host distribution includes Go Center, PostgreSQL configuration, origin/TLS guidance, Blazor assets, operator administration, backups and restore without official entitlement endpoints. Official hosting uses the existing guarded deployment scripts and dormant feature rollout; no direct Cloudflare mutations, worker previews or `workers.dev` activation. Package publication and production activation keep their existing user authorization and repository gates.

Final acceptance verifies fresh installation and upgrade from audited Node schema 15 and Center schema 10/11, same-cohort engine provenance, native interactive CLI, resource enforcement, offline operation, self-hosted remote control and official entitlement boundaries. Publishing a package alone proves none of those runtime behaviors.
