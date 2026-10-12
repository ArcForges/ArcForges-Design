-- ArcForges Cloud D1: new `fleet` module tables (specification; see cloud-store.md).
-- AF-CLD-01 expresses these as Physical/manifest/fleet.json in the Cloud repository; its generator then emits
-- the canonical constraints (full UUID GLOB checks, ck_/pk_/fk_/ix_/ux_ names) and the migration
-- `00xx_fleet__baseline.sql` (mode=expand). Column comments give the physical kind (Design D1 profile section 2).
-- Reused tables referenced here: identity_user, device_device, device_installation (unchanged keys).

CREATE TABLE "fleet_node" (
  "node_id" TEXT NOT NULL CHECK (length("node_id") = 36),                 -- id
  "user_id" TEXT NOT NULL CHECK (length("user_id") = 36),                 -- id
  "device_id" TEXT NOT NULL CHECK (length("device_id") = 36),             -- id
  "installation_id" TEXT NOT NULL CHECK (length("installation_id") = 36), -- id
  "display_name" TEXT NOT NULL CHECK (length("display_name") BETWEEN 1 AND 64), -- text
  "os" INTEGER NOT NULL CHECK ("os" IN (1, 2)),                           -- OsFamily
  "arch" INTEGER NOT NULL CHECK ("arch" IN (1, 2)),                       -- CpuArchitecture
  "role" INTEGER NOT NULL CHECK ("role" IN (1, 2)),                       -- NodeRole
  "host_node_id" TEXT CHECK ("host_node_id" IS NULL OR length("host_node_id") = 36), -- id
  "version" TEXT NOT NULL,                                                -- text (SemVer)
  "enrolled_at" INTEGER NOT NULL,                                         -- instant
  "last_seen_at" INTEGER NOT NULL,                                        -- instant
  "relay_enabled" INTEGER NOT NULL CHECK ("relay_enabled" IN (0, 1)),     -- bool
  "lan_endpoints" TEXT NOT NULL CHECK (json_valid("lan_endpoints") AND json_type("lan_endpoints") = 'array'), -- json array
  "lan_fingerprint" TEXT,                                                 -- text (hex SHA-256)
  "lan_reported_at" INTEGER,                                              -- instant
  "revoked_at" INTEGER,                                                   -- instant
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),                              -- rev
  CONSTRAINT "pk_fleet_node" PRIMARY KEY ("node_id"),
  CONSTRAINT "fk_fleet_node__user_id" FOREIGN KEY ("user_id") REFERENCES "identity_user" ("user_id") ON DELETE CASCADE,
  CONSTRAINT "fk_fleet_node__device_id" FOREIGN KEY ("device_id") REFERENCES "device_device" ("device_id") ON DELETE RESTRICT,
  CONSTRAINT "fk_fleet_node__installation_id" FOREIGN KEY ("installation_id") REFERENCES "device_installation" ("installation_id") ON DELETE RESTRICT,
  CONSTRAINT "fk_fleet_node__host_node_id" FOREIGN KEY ("host_node_id") REFERENCES "fleet_node" ("node_id") ON DELETE SET NULL,
  CONSTRAINT "ck_fleet_node__guest_has_host" CHECK ("role" <> 2 OR "host_node_id" IS NOT NULL)
) STRICT;
CREATE UNIQUE INDEX "ux_fleet_node__installation_id" ON "fleet_node" ("installation_id");
CREATE INDEX "ix_fleet_node__user_id_revoked_at" ON "fleet_node" ("user_id", "revoked_at");
CREATE INDEX "ix_fleet_node__host_node_id" ON "fleet_node" ("host_node_id");

-- Browser PKCE sign-in for nodes. The code, PKCE and attempt mechanics reuse identity_native_authorization
-- (same flow_id); this table adds the node being enrolled and the consent state.
CREATE TABLE "fleet_node_sign_in" (
  "flow_id" TEXT NOT NULL CHECK (length("flow_id") = 36),                 -- id (= identity_native_authorization.flow_id)
  "node_id" TEXT NOT NULL CHECK (length("node_id") = 36),                 -- id
  "installation_id" TEXT NOT NULL CHECK (length("installation_id") = 36), -- id (provisional until completion)
  "display_name" TEXT NOT NULL,                                           -- text
  "os" INTEGER NOT NULL CHECK ("os" IN (1, 2)),
  "arch" INTEGER NOT NULL CHECK ("arch" IN (1, 2)),
  "role" INTEGER NOT NULL CHECK ("role" IN (1, 2)),
  "host_node_id" TEXT,
  "version" TEXT NOT NULL,
  "state" INTEGER NOT NULL CHECK ("state" BETWEEN 1 AND 6),              -- NodeSignInState
  "user_id" TEXT CHECK ("user_id" IS NULL OR length("user_id") = 36),     -- id (approver)
  "created_at" INTEGER NOT NULL,
  "expires_at" INTEGER NOT NULL,
  "decided_at" INTEGER,
  "completed_at" INTEGER,
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),
  CONSTRAINT "pk_fleet_node_sign_in" PRIMARY KEY ("flow_id")
) STRICT;
CREATE INDEX "ix_fleet_node_sign_in__expires_at" ON "fleet_node_sign_in" ("expires_at");

CREATE TABLE "fleet_device_authorization" (
  "authorization_id" TEXT NOT NULL CHECK (length("authorization_id") = 36),  -- id
  "device_code_hash" BLOB NOT NULL CHECK (length("device_code_hash") = 32),  -- hash
  "user_code_hash" BLOB NOT NULL CHECK (length("user_code_hash") = 32),      -- hash (normalized code)
  "node_id" TEXT NOT NULL CHECK (length("node_id") = 36),
  "installation_id" TEXT NOT NULL CHECK (length("installation_id") = 36),
  "display_name" TEXT NOT NULL,
  "os" INTEGER NOT NULL CHECK ("os" IN (1, 2)),
  "arch" INTEGER NOT NULL CHECK ("arch" IN (1, 2)),
  "role" INTEGER NOT NULL CHECK ("role" IN (1, 2)),
  "host_node_id" TEXT,
  "version" TEXT NOT NULL,
  "state" INTEGER NOT NULL CHECK ("state" IN (1, 3, 4, 5, 6)),         -- DeviceAuthorizationState numbers (2 SLOW_DOWN is response-only)
  "user_id" TEXT CHECK ("user_id" IS NULL OR length("user_id") = 36),
  "interval_ms" INTEGER NOT NULL CHECK ("interval_ms" BETWEEN 5000 AND 60000),
  "last_poll_at" INTEGER,
  "entry_attempts" INTEGER NOT NULL CHECK ("entry_attempts" BETWEEN 0 AND 5),
  "created_at" INTEGER NOT NULL,
  "expires_at" INTEGER NOT NULL,
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),
  CONSTRAINT "pk_fleet_device_authorization" PRIMARY KEY ("authorization_id")
) STRICT;
CREATE UNIQUE INDEX "ux_fleet_device_authorization__device_code_hash" ON "fleet_device_authorization" ("device_code_hash");
CREATE UNIQUE INDEX "ux_fleet_device_authorization__user_code_hash_live" ON "fleet_device_authorization" ("user_code_hash") WHERE "state" = 1;
CREATE INDEX "ix_fleet_device_authorization__expires_at" ON "fleet_device_authorization" ("expires_at");

CREATE TABLE "fleet_phone_pairing" (
  "pairing_id" TEXT NOT NULL CHECK (length("pairing_id") = 36),
  "node_id" TEXT NOT NULL CHECK (length("node_id") = 36),
  "user_id" TEXT NOT NULL CHECK (length("user_id") = 36),
  "secret_hash" BLOB NOT NULL CHECK (length("secret_hash") = 32),
  "claim_token_hash" BLOB CHECK ("claim_token_hash" IS NULL OR length("claim_token_hash") = 32),
  "state" INTEGER NOT NULL CHECK ("state" BETWEEN 1 AND 7),              -- PhonePairingCloudState
  "phone_installation_id" TEXT CHECK ("phone_installation_id" IS NULL OR length("phone_installation_id") = 36),
  "phone_model" TEXT,
  "phone_os_version" TEXT,
  "phone_app_version" TEXT,
  "created_at" INTEGER NOT NULL,
  "expires_at" INTEGER NOT NULL,
  "claimed_at" INTEGER,
  "decided_at" INTEGER,
  "completed_at" INTEGER,
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),
  CONSTRAINT "pk_fleet_phone_pairing" PRIMARY KEY ("pairing_id"),
  CONSTRAINT "fk_fleet_phone_pairing__node_id" FOREIGN KEY ("node_id") REFERENCES "fleet_node" ("node_id") ON DELETE CASCADE,
  CONSTRAINT "fk_fleet_phone_pairing__user_id" FOREIGN KEY ("user_id") REFERENCES "identity_user" ("user_id") ON DELETE CASCADE
) STRICT;
CREATE INDEX "ix_fleet_phone_pairing__node_id_created_at" ON "fleet_phone_pairing" ("node_id", "created_at");

CREATE TABLE "fleet_node_certificate" (
  "serial" TEXT NOT NULL,                                                 -- key (hex serial)
  "node_id" TEXT NOT NULL CHECK (length("node_id") = 36),
  "public_key_hash" BLOB NOT NULL CHECK (length("public_key_hash") = 32),
  "issued_at" INTEGER NOT NULL,
  "expires_at" INTEGER NOT NULL,
  "revoked_at" INTEGER,
  CONSTRAINT "pk_fleet_node_certificate" PRIMARY KEY ("serial"),
  CONSTRAINT "fk_fleet_node_certificate__node_id" FOREIGN KEY ("node_id") REFERENCES "fleet_node" ("node_id") ON DELETE CASCADE
) STRICT;
CREATE INDEX "ix_fleet_node_certificate__node_id_expires_at" ON "fleet_node_certificate" ("node_id", "expires_at");

CREATE TABLE "fleet_remote_command" (
  "command_id" TEXT NOT NULL CHECK (length("command_id") = 36),
  "user_id" TEXT NOT NULL CHECK (length("user_id") = 36),
  "node_id" TEXT NOT NULL CHECK (length("node_id") = 36),
  "kind" INTEGER NOT NULL CHECK ("kind" BETWEEN 1 AND 11),               -- NodeCommandBody oneof field number
  "risk" INTEGER NOT NULL CHECK ("risk" IN (1, 2, 3)),                    -- RiskClass
  "state" INTEGER NOT NULL CHECK ("state" BETWEEN 1 AND 7),              -- enum RemoteCommandState
  "body" BLOB NOT NULL,                                                   -- proto arcforges.fleet.v1.NodeCommandBody
  "signed_envelope" BLOB NOT NULL,                                        -- proto arcforges.fleet.v1.SignedBlob
  "step_up_at" INTEGER,
  "session_id" TEXT NOT NULL CHECK (length("session_id") = 36),          -- issuing identity_session
  "created_at" INTEGER NOT NULL,
  "expires_at" INTEGER NOT NULL,
  "delivered_at" INTEGER,
  "completed_at" INTEGER,
  "result" BLOB,                                                          -- proto arcforges.fleet.v1.SignedBlob (NodeCommandResult)
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),
  CONSTRAINT "pk_fleet_remote_command" PRIMARY KEY ("command_id"),
  CONSTRAINT "fk_fleet_remote_command__node_id" FOREIGN KEY ("node_id") REFERENCES "fleet_node" ("node_id") ON DELETE CASCADE,
  CONSTRAINT "ck_fleet_remote_command__expiry" CHECK ("expires_at" > "created_at" AND "expires_at" - "created_at" <= 300000000)
) STRICT;
CREATE INDEX "ix_fleet_remote_command__node_id_created_at" ON "fleet_remote_command" ("node_id", "created_at");
CREATE INDEX "ix_fleet_remote_command__state_expires_at" ON "fleet_remote_command" ("state", "expires_at");
CREATE INDEX "ix_fleet_remote_command__user_id_created_at" ON "fleet_remote_command" ("user_id", "created_at");

CREATE TABLE "fleet_play_purchase" (
  "purchase_token_hash" BLOB NOT NULL CHECK (length("purchase_token_hash") = 32),
  "encrypted_purchase_token" BLOB NOT NULL,                               -- bytes (encrypted at rest; needed for API re-reads)
  "user_id" TEXT CHECK ("user_id" IS NULL OR length("user_id") = 36),     -- NULL while NEEDS_CONFIRMATION
  "subscription_id" TEXT,                                                 -- commerce_subscription link once granted
  "product_id" TEXT NOT NULL,
  "base_plan_id" TEXT NOT NULL,
  "obfuscated_account_id" TEXT,
  "link_state" INTEGER NOT NULL CHECK ("link_state" BETWEEN 1 AND 5),    -- enum PlayLinkState
  "play_state" TEXT NOT NULL,                                             -- last subscriptionsv2 subscriptionState
  "acknowledged_at" INTEGER,
  "acknowledge_due_at" INTEGER NOT NULL,                                  -- purchase time + 24 h (alert), Google window 3 days
  "expires_at" INTEGER,
  "last_verified_at" INTEGER NOT NULL,
  "created_at" INTEGER NOT NULL,
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),
  CONSTRAINT "pk_fleet_play_purchase" PRIMARY KEY ("purchase_token_hash")
) STRICT;
CREATE INDEX "ix_fleet_play_purchase__user_id" ON "fleet_play_purchase" ("user_id");
CREATE INDEX "ix_fleet_play_purchase__ack_pending" ON "fleet_play_purchase" ("acknowledge_due_at") WHERE "acknowledged_at" IS NULL;

CREATE TABLE "fleet_play_notification" (
  "message_id" TEXT NOT NULL,                                             -- Pub/Sub message ID (dedup)
  "received_at" INTEGER NOT NULL,
  "purchase_token_hash" BLOB,
  "notification_type" INTEGER,
  "payload" BLOB NOT NULL,                                                -- bytes (decoded RTDN JSON, encrypted)
  "processed_at" INTEGER,
  "attempts" INTEGER NOT NULL CHECK ("attempts" >= 0),
  CONSTRAINT "pk_fleet_play_notification" PRIMARY KEY ("message_id")
) STRICT;
CREATE INDEX "ix_fleet_play_notification__unprocessed" ON "fleet_play_notification" ("received_at") WHERE "processed_at" IS NULL;

CREATE TABLE "fleet_signing_key" (
  "kid" TEXT NOT NULL,                                                    -- key
  "purpose" INTEGER NOT NULL CHECK ("purpose" IN (1, 2, 3)),             -- enum: command_signing, entitlement_token, relay_hmac
  "algorithm" TEXT NOT NULL,
  "public_key" BLOB,                                                      -- NULL for HMAC keys
  "secret_ref" TEXT NOT NULL,                                             -- name of the platform secret binding; never the key
  "not_before" INTEGER NOT NULL,
  "not_after" INTEGER NOT NULL,
  "retired_at" INTEGER,
  CONSTRAINT "pk_fleet_signing_key" PRIMARY KEY ("kid")
) STRICT;

CREATE TABLE "fleet_push_preference" (
  "user_id" TEXT NOT NULL CHECK (length("user_id") = 36),
  "kind" TEXT NOT NULL CHECK ("kind" IN ('node.task_failed', 'node.task_finished', 'node.approval_needed', 'node.offline', 'node.finding')),
  "node_scope" TEXT NOT NULL,                                             -- node_id, or '*' for all nodes
  "enabled" INTEGER NOT NULL CHECK ("enabled" IN (0, 1)),
  "updated_at" INTEGER NOT NULL,
  "rev" INTEGER NOT NULL CHECK ("rev" >= 0),                              -- per-user revision (max over rows)
  CONSTRAINT "pk_fleet_push_preference" PRIMARY KEY ("user_id", "kind", "node_scope"),
  CONSTRAINT "fk_fleet_push_preference__user_id" FOREIGN KEY ("user_id") REFERENCES "identity_user" ("user_id") ON DELETE CASCADE
) STRICT;
