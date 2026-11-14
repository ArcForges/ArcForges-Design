-- ArcForges V2 target SQLite schema specification; not an executable upgrade of V1.
-- Applied V1 schema steps 0001..0015 remain byte-immutable; see migrations.md.
PRAGMA foreign_keys = ON;
CREATE TABLE schema_version (
 singleton INTEGER PRIMARY KEY CHECK (singleton=1), version INTEGER NOT NULL,
 min_reader INTEGER NOT NULL, cohort TEXT NOT NULL, migration_receipt TEXT NOT NULL
) STRICT;
CREATE TABLE sandbox (
 sandbox_id TEXT PRIMARY KEY, owner_id TEXT NOT NULL, display_name TEXT NOT NULL,
 normalized_name TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>0),
 state INTEGER NOT NULL CHECK(state BETWEEN 1 AND 6), root_relative TEXT NOT NULL UNIQUE,
 root_identity TEXT NOT NULL, root_generation INTEGER NOT NULL CHECK(root_generation>0),
 created_utc TEXT NOT NULL, updated_utc TEXT NOT NULL,
 UNIQUE(owner_id, normalized_name)
) STRICT;
CREATE TABLE sandbox_config (
 sandbox_id TEXT NOT NULL REFERENCES sandbox(sandbox_id), revision INTEGER NOT NULL,
 profile_id TEXT NOT NULL, profile_version TEXT NOT NULL, config_json TEXT NOT NULL CHECK(json_valid(config_json)),
 config_sha256 TEXT NOT NULL CHECK(length(config_sha256)=64), created_utc TEXT NOT NULL,
 PRIMARY KEY(sandbox_id, revision)
) STRICT;
CREATE TABLE run (
 run_id TEXT PRIMARY KEY, sandbox_id TEXT NOT NULL REFERENCES sandbox(sandbox_id),
 sandbox_revision INTEGER NOT NULL, revision INTEGER NOT NULL CHECK(revision>0),
 state INTEGER NOT NULL CHECK(state BETWEEN 1 AND 7), epoch TEXT NOT NULL,
 launch_sha256 TEXT NOT NULL CHECK(length(launch_sha256)=64), snapshot_json TEXT NOT NULL CHECK(json_valid(snapshot_json)),
 payload_started INTEGER NOT NULL CHECK(payload_started BETWEEN 0 AND 2),
 created_utc TEXT NOT NULL, started_utc TEXT, ended_utc TEXT,
 raw_exit_code INTEGER, exit_source TEXT, termination_reason TEXT,
 effect_certainty INTEGER NOT NULL CHECK(effect_certainty BETWEEN 1 AND 3),
 FOREIGN KEY(sandbox_id,sandbox_revision) REFERENCES sandbox_config(sandbox_id,revision)
) STRICT;
CREATE INDEX run_by_sandbox_state ON run(sandbox_id,state,created_utc);
CREATE TABLE supervisor_identity (
 run_id TEXT PRIMARY KEY REFERENCES run(run_id), instance_id TEXT NOT NULL, boot_id TEXT NOT NULL,
 process_id INTEGER NOT NULL, creation_identity TEXT NOT NULL, endpoint TEXT NOT NULL,
 boundary_identity TEXT NOT NULL, backend_id TEXT NOT NULL, cohort TEXT NOT NULL,
 lease_epoch TEXT NOT NULL, last_seen_utc TEXT NOT NULL
) STRICT;
CREATE TABLE command_receipt (
 owner_id TEXT NOT NULL, command_id TEXT NOT NULL, method TEXT NOT NULL,
 request_sha256 TEXT NOT NULL CHECK(length(request_sha256)=64), aggregate_id TEXT,
 state TEXT NOT NULL CHECK(state IN ('ACCEPTED','SUCCEEDED','FAILED','UNKNOWN')),
 effect_certainty INTEGER NOT NULL CHECK(effect_certainty BETWEEN 1 AND 3),
 response_json TEXT CHECK(response_json IS NULL OR json_valid(response_json)),
 created_utc TEXT NOT NULL, updated_utc TEXT NOT NULL, expires_utc TEXT,
 PRIMARY KEY(owner_id,command_id)
) STRICT;
CREATE TABLE resource_policy (
 scope_kind TEXT NOT NULL CHECK(scope_kind IN ('node','sandbox','run')), scope_id TEXT NOT NULL,
 revision INTEGER NOT NULL CHECK(revision>0), policy_json TEXT NOT NULL CHECK(json_valid(policy_json)),
 PRIMARY KEY(scope_kind,scope_id)
) STRICT;
CREATE TABLE limit_application (
 run_id TEXT NOT NULL REFERENCES run(run_id), dimension TEXT NOT NULL, unit TEXT NOT NULL,
 desired_revision INTEGER NOT NULL, desired_value TEXT NOT NULL, applied_value TEXT, readback_value TEXT,
 applied_utc TEXT, readback_utc TEXT, state TEXT NOT NULL CHECK(state IN ('pending','effective','degraded','failed','unsupported')),
 reason TEXT NOT NULL, boundary_identity TEXT NOT NULL, PRIMARY KEY(run_id,dimension)
) STRICT;
CREATE TABLE resource_sample (
 scope_kind TEXT NOT NULL, scope_id TEXT NOT NULL, observed_utc TEXT NOT NULL,
 epoch TEXT NOT NULL, sample_json TEXT NOT NULL CHECK(json_valid(sample_json)),
 PRIMARY KEY(scope_kind,scope_id,observed_utc)
) STRICT;
CREATE TABLE output_segment (
 run_id TEXT NOT NULL REFERENCES run(run_id), epoch TEXT NOT NULL,
 offset_start INTEGER NOT NULL CHECK(offset_start>=0), length_bytes INTEGER NOT NULL CHECK(length_bytes>=0),
 relative_path TEXT NOT NULL, stream_kind TEXT NOT NULL CHECK(stream_kind IN ('terminal','stdout','stderr')),
 created_utc TEXT NOT NULL, PRIMARY KEY(run_id,epoch,offset_start,stream_kind)
) STRICT;
CREATE TABLE remote_grant (
 grant_id TEXT PRIMARY KEY, sandbox_id TEXT REFERENCES sandbox(sandbox_id),
 scope_kind TEXT NOT NULL CHECK(scope_kind IN ('sandbox','provision')), parent_grant_id TEXT REFERENCES remote_grant(grant_id),
 template_revision INTEGER, creation_template_json TEXT CHECK(creation_template_json IS NULL OR json_valid(creation_template_json)),
 enrollment_id TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>0),
 state INTEGER NOT NULL CHECK(state BETWEEN 1 AND 3), policy_json TEXT NOT NULL CHECK(json_valid(policy_json)),
 created_local_utc TEXT NOT NULL, expires_utc TEXT, revoked_utc TEXT,
 CHECK((scope_kind='sandbox' AND sandbox_id IS NOT NULL) OR (scope_kind='provision' AND sandbox_id IS NULL AND creation_template_json IS NOT NULL AND template_revision>0))
) STRICT;
CREATE TABLE transfer (
 transfer_id TEXT PRIMARY KEY, sandbox_id TEXT NOT NULL REFERENCES sandbox(sandbox_id),
 command_id TEXT NOT NULL, direction TEXT NOT NULL CHECK(direction IN ('import','export')),
 state INTEGER NOT NULL CHECK(state BETWEEN 1 AND 5), manifest_json TEXT NOT NULL CHECK(json_valid(manifest_json)),
 staging_identity TEXT NOT NULL, byte_length INTEGER NOT NULL CHECK(byte_length>=0),
 verified_offset INTEGER NOT NULL CHECK(verified_offset>=0), expected_sha256 TEXT NOT NULL,
 expires_utc TEXT NOT NULL, effect_certainty INTEGER NOT NULL CHECK(effect_certainty BETWEEN 1 AND 3)
) STRICT;
CREATE TABLE deletion_journal (
 deletion_id TEXT PRIMARY KEY, sandbox_id TEXT NOT NULL REFERENCES sandbox(sandbox_id),
 command_id TEXT NOT NULL, expected_revision INTEGER NOT NULL, root_identity TEXT NOT NULL,
 quarantine_identity TEXT, phase TEXT NOT NULL CHECK(phase IN ('planned','locked','quarantined','removing','complete','recovery_required')),
 effect_certainty INTEGER NOT NULL CHECK(effect_certainty BETWEEN 1 AND 3), updated_utc TEXT NOT NULL
) STRICT;
CREATE TABLE event (
 sequence INTEGER PRIMARY KEY AUTOINCREMENT, epoch TEXT NOT NULL, kind TEXT NOT NULL,
 aggregate_id TEXT NOT NULL, revision INTEGER NOT NULL, created_utc TEXT NOT NULL,
 body_json TEXT NOT NULL CHECK(json_valid(body_json))
) STRICT;
CREATE TABLE audit (
 sequence INTEGER PRIMARY KEY AUTOINCREMENT, actor_id TEXT NOT NULL, origin TEXT NOT NULL,
 command_id TEXT, method TEXT NOT NULL, aggregate_id TEXT, effect_certainty INTEGER NOT NULL,
 reason_code TEXT NOT NULL, created_utc TEXT NOT NULL, metadata_json TEXT NOT NULL CHECK(json_valid(metadata_json))
) STRICT;
CREATE TABLE migration_checkpoint (
 migration_id TEXT PRIMARY KEY, source_schema INTEGER NOT NULL, target_schema INTEGER NOT NULL,
 backup_identity TEXT NOT NULL, state TEXT NOT NULL, cohort TEXT NOT NULL,
 unresolved_count INTEGER NOT NULL CHECK(unresolved_count>=0), receipt_sha256 TEXT NOT NULL,
 created_utc TEXT NOT NULL
) STRICT;
