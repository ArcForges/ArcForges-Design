# Node store and retention

[Target SQLite DDL](node-store.sql) specifies V2's normalized persistence and is executable for structural validation. It is not an upgrade script. Actual Node schema is version/min-reader **15** at the audited source. The future migration appends new steps; it never edits applied 0001–0015. See [migrations](migrations.md) and the [source audit](../research/runtime-audit.md).

| Table | Owner/invariants | Lifetime |
|---|---|---|
| `schema_version` | Single schema/min-reader/cohort/receipt row; readers refuse incompatible stores | Database lifetime |
| `sandbox` | Owner, normalized display-name uniqueness, relative root plus stable native identity, revision and six-state lifecycle | Tombstone after deletion; private payload bytes are separate |
| `sandbox_config` | Immutable versioned canonical config and digest; no plaintext secret environment | Retain while referenced by a Run; latest config always retained |
| `run` | One start and immutable redacted launch snapshot; seven-state Run enum, authoritative provenance for any exit | Configurable record retention after terminal and resolved effects |
| `supervisor_identity` | RunId+epoch+boot+process creation identity+boundary identity; never PID alone | Until Run finalized and cleanup proven |
| `command_receipt` | Unique owner+command ID; normalized method/payload hash; durable effect certainty | At least 24 h after known result; never expire UNKNOWN or an unresolved delete/transfer |
| `resource_policy` | Node/Sandbox/Run policy revision; no cloud entitlement in local policy | Scope lifetime |
| `limit_application` | Desired/applied/readback/time/state/reason per dimension and native boundary | Active Run plus last diagnostic state |
| `resource_sample` | Timestamp/epoch/unit/freshness and labeled memory semantics | 24 h raw by default, bounded configurable retention; long-term summaries only if enabled |
| `output_segment` | Immutable owned relative path, epoch and byte range; terminal versus piped streams | 64 MiB per Run default, bounded configurable; deletion/gap visible |
| `remote_grant` | Created/expanded locally; enrollment bound and versioned; either Sandbox scope or immutable provisioning-template scope; child records parent authority; ACTIVE/REVOKED/EXPIRED | Keep revocation receipt long enough to reject replay; check parent revocation/expiry at every new admission |
| `transfer` | Import/export manifest, exact staging identity, bounded size/hash/offset/expiry | One hour expiry for idle staging by default; unknown commit effects never blindly removed |
| `deletion_journal` | Preview revision and identity, quarantine phase, effect and reconciliation | Never purge unresolved entries |
| `event` | Monotonic sequence in Node epoch, redacted body and aggregate revision | Bounded retention; expired cursors explicitly produce a gap |
| `audit` | Append-only owner/origin/method/correlation/effect metadata; no raw secrets | Operator-configured retention; preserve unresolved operations and migration evidence |
| `migration_checkpoint` | Backup identity, source/target schema, cohort, unresolved count and receipt | Permanent migration history |

State integer mapping is exactly the corresponding protobuf enum: Sandbox 1 CREATING, 2 READY, 3 DELETING, 4 DELETED, 5 ERROR, 6 RECOVERY_REQUIRED; Run 1 STARTING, 2 RUNNING, 3 STOPPING, 4 DRAINING, 5 EXITED, 6 FAILED, 7 RECOVERY_REQUIRED. `payload_started` is 0 unknown, 1 not started, 2 confirmed. Foundation effect certainty is 1 DID_NOT_HAPPEN, 2 HAPPENED, 3 UNKNOWN. Wire state UNSPECIFIED is rejected on writes.

The Node is the sole metadata writer. All mutation/receipt/event updates share a transaction; native effects are coordinated by durable intent and post-effect reconciliation. Do not keep a SQLite write transaction open across a long network/native operation. Acquire the documented scope/ownership lease, persist intent, execute, then finalize or mark UNKNOWN. Concurrent starts and deletion take the same Sandbox gate.

Terminal writer leases are ephemeral supervisor authority, not durable permission: Node restart invalidates client leases and requires authenticated reacquisition, while output epoch/offset persists. This prevents a copied database from reviving terminal input authority.

Retention defaults are engineering safety limits, not subscription tiers. Disk-space admission reserves room for journals/audit before accepting a start or transfer. Exhaustion returns a bounded resource error and preserves existing evidence. Requested deletion accounts for managed active use; independently opened host file handles are outside the earlier owner's agreed protection scope, while ordinary OS access/identity failures still stop unsafe deletion.
