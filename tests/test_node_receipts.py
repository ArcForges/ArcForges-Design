"""Exercise real V2 SQLite specification constraints, not runtime or native-effect proof."""
import sqlite3
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "docs/data/node-store.sql"
EPOCH = bytes.fromhex("00112233445566778899aabbccddeeff")
CREATED = "2026-11-14T00:00:00Z"
EXPIRES = "2026-11-15T00:00:00Z"
COMPACTED = "2026-11-15T01:00:00Z"


class NodeReceiptConstraints(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript(SCHEMA.read_text(encoding="utf-8"))
        self.db.execute("""INSERT INTO owner_epoch
            (owner_id,owner_epoch,digest_key_ref,state,created_utc)
            VALUES (?,?,?,'ACTIVE',?)""", ("owner", EPOCH, "protected-key-reference", CREATED))

    def receipt(self, command="command-1", method="RunService.Start", state="SUCCEEDED", effect=2,
                epoch=EPOCH, aggregate_kind="run", aggregate_id="run-1", expires=EXPIRES, replace=False):
        known = state in {"SUCCEEDED", "FAILED"} and effect in {1, 2}
        verb = "INSERT OR REPLACE" if replace else "INSERT"
        self.db.execute(f"""{verb} INTO command_receipt
            (owner_id,owner_epoch,command_id,method,request_hmac_sha256,aggregate_kind,aggregate_id,
             state,effect_certainty,response_json,created_utc,updated_utc,resolved_utc,expires_utc)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            ("owner", epoch, command, method, "a" * 64, aggregate_kind, aggregate_id,
             state, effect, '{"safeResult":"original"}', CREATED, CREATED,
             CREATED if known else None, expires if known else None))

    def compact(self, command="command-1"):
        self.db.execute("""UPDATE command_receipt SET response_json=NULL,response_compacted_utc=?
            WHERE owner_id=? AND owner_epoch=? AND command_id=?""",
            (COMPACTED, "owner", EPOCH, command))

    def sandbox(self):
        self.db.execute("""INSERT INTO sandbox
            (sandbox_id,owner_id,display_name,normalized_name,revision,state,root_relative,
             root_identity,root_generation,created_utc,updated_utc)
            VALUES ('sandbox-1','owner','Sandbox','sandbox',1,2,'sandboxes/id','native-root',1,?,?)""",
            (CREATED, CREATED))
        self.db.execute("""INSERT INTO sandbox_config
            (sandbox_id,revision,profile_id,profile_version,config_json,config_sha256,created_utc)
            VALUES ('sandbox-1',1,'qualified-profile','1','{}',?,?)""", ("b" * 64, CREATED))

    def test_known_body_compacts_without_forgetting_identity_or_effect(self):
        self.receipt()
        self.compact()
        row = self.db.execute("""SELECT owner_id,owner_epoch,command_id,method,request_hmac_sha256,
            aggregate_kind,aggregate_id,state,effect_certainty,response_json,response_compacted_utc
            FROM command_receipt""").fetchone()
        self.assertEqual(row, ("owner", EPOCH, "command-1", "RunService.Start", "a" * 64,
                               "run", "run-1", "SUCCEEDED", 2, None, COMPACTED))
        with self.assertRaises(sqlite3.IntegrityError):
            self.receipt()  # A compacted key is still occupied.

    def test_active_epoch_identity_cannot_be_deleted(self):
        self.receipt()
        self.compact()
        with self.assertRaisesRegex(sqlite3.IntegrityError, "retains command identity"):
            self.db.execute("DELETE FROM command_receipt")
        with self.assertRaisesRegex(sqlite3.IntegrityError, "identity already exists"):
            self.receipt(method="RunService.Stop", replace=True)
        self.assertEqual(self.db.execute("SELECT count(*) FROM command_receipt").fetchone()[0], 1)

    def test_admitted_identity_fields_cannot_be_rekeyed(self):
        self.receipt()
        changes = {"owner_id": "different-owner", "owner_epoch": b"x" * 16,
                   "command_id": "replacement", "method": "RunService.Stop",
                   "request_hmac_sha256": "c" * 64, "aggregate_kind": "sandbox",
                   "aggregate_id": "different-run", "created_utc": EXPIRES}
        for column, value in changes.items():
            with self.subTest(column=column), self.assertRaisesRegex(sqlite3.IntegrityError, "identity is immutable"):
                self.db.execute(f"UPDATE command_receipt SET {column}=?", (value,))

    def test_settled_effect_cannot_be_reclassified(self):
        self.receipt()
        with self.assertRaisesRegex(sqlite3.IntegrityError, "outcome is immutable"):
            self.db.execute("UPDATE command_receipt SET state='FAILED',effect_certainty=1")

    def test_unknown_and_accepted_receipts_keep_their_full_body(self):
        for state in ("UNKNOWN", "ACCEPTED"):
            with self.subTest(state=state):
                self.receipt(command=state, state=state, effect=3)
                with self.assertRaises(sqlite3.IntegrityError):
                    self.compact(state)
                body = self.db.execute("SELECT response_json FROM command_receipt WHERE command_id=?", (state,)).fetchone()[0]
                self.assertIsNotNone(body)

    def test_body_cannot_disappear_without_compaction_metadata(self):
        self.receipt()
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE command_receipt SET response_json=NULL")

    def test_compaction_deadline_cannot_precede_twenty_four_hours(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.receipt(expires="2026-11-14T23:59:59Z")
        self.receipt()
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("""UPDATE command_receipt SET response_json=NULL,
                response_compacted_utc='2026-11-14T23:59:59Z'""")

    def test_epoch_must_be_exactly_sixteen_binary_bytes(self):
        for epoch in (b"x" * 15, b"x" * 17, "x" * 16):
            with self.subTest(epoch=epoch), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute("""INSERT INTO owner_epoch
                    (owner_id,owner_epoch,digest_key_ref,state,created_utc)
                    VALUES ('other',?,'key','ACTIVE',?)""", (epoch, CREATED))

    def test_owner_has_only_one_active_epoch(self):
        for verb in ("INSERT", "INSERT OR REPLACE"):
            with self.subTest(verb=verb), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute(f"""{verb} INTO owner_epoch
                    (owner_id,owner_epoch,digest_key_ref,state,created_utc)
                    VALUES ('owner',?,'new-key','ACTIVE',?)""", (b"n" * 16, CREATED))
        self.assertEqual(self.db.execute("SELECT owner_epoch FROM owner_epoch WHERE state='ACTIVE'").fetchone()[0], EPOCH)

    def test_epoch_identity_and_retirement_are_irreversible(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, "identity is immutable"):
            self.db.execute("UPDATE owner_epoch SET digest_key_ref='replacement-key'")
        self.db.execute("UPDATE owner_epoch SET state='RETIRED',retired_utc=?", (EXPIRES,))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "cannot be reactivated"):
            self.db.execute("UPDATE owner_epoch SET state='ACTIVE',retired_utc=NULL")
        with self.assertRaisesRegex(sqlite3.IntegrityError, "metadata is retained"):
            self.db.execute("DELETE FROM owner_epoch")
        with self.assertRaisesRegex(sqlite3.IntegrityError, "retired or unknown"):
            self.receipt()

    def test_a_different_store_epoch_cannot_admit_a_saved_request(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, "retired or unknown"):
            self.receipt(epoch=b"z" * 16)

    def test_terminal_commands_have_no_durable_receipt(self):
        for name in ("AcquireTerminal", "WriteTerminal", "ResizeTerminal", "DetachTerminal"):
            with self.subTest(method=name), self.assertRaises(sqlite3.IntegrityError):
                self.receipt(command=name, method="RunService." + name)

    def test_payload_start_values_match_canonical_enum_numbers(self):
        self.sandbox()
        sql = """INSERT INTO run
            (run_id,sandbox_id,sandbox_revision,revision,state,epoch,launch_sha256,
             snapshot_json,payload_started,created_utc,effect_certainty)
            VALUES (?,'sandbox-1',1,1,1,'supervisor-epoch',?,'{}',?,?,3)"""
        for value in (1, 2, 3):
            self.db.execute(sql, (f"valid-{value}", "d" * 64, value, CREATED))
        for value in (0, 4):
            with self.subTest(value=value), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute(sql, (f"invalid-{value}", "d" * 64, value, CREATED))

    def test_unresolved_transfer_blocks_body_compaction(self):
        self.sandbox()
        self.receipt(method="DataService.BeginImport", aggregate_kind="transfer", aggregate_id="transfer-1")
        self.db.execute("""INSERT INTO transfer
            (transfer_id,sandbox_id,owner_id,owner_epoch,command_id,direction,state,manifest_json,
             staging_identity,byte_length,verified_offset,expected_sha256,expires_utc,effect_certainty)
            VALUES ('transfer-1','sandbox-1','owner',?,'command-1','import',5,'{}',
                    'private-stage',0,0,?,?,3)""", (EPOCH, "e" * 64, EXPIRES))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "unresolved effect retains"):
            self.compact()

    def test_original_deletion_identity_and_unresolved_body_are_retained(self):
        self.sandbox()
        self.receipt(method="SandboxService.Delete", aggregate_kind="sandbox", aggregate_id="sandbox-1")
        self.db.execute("""INSERT INTO deletion_journal
            (deletion_id,sandbox_id,owner_id,owner_epoch,command_id,expected_revision,root_identity,
             phase,effect_certainty,updated_utc)
            VALUES ('delete-1','sandbox-1','owner',?,'command-1',1,'native-root','recovery_required',3,?)""",
            (EPOCH, CREATED))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "original deletion identity is immutable"):
            self.db.execute("UPDATE deletion_journal SET root_identity='foreign-root'")
        with self.assertRaisesRegex(sqlite3.IntegrityError, "original deletion journal already exists"):
            self.db.execute("""INSERT OR REPLACE INTO deletion_journal
                (deletion_id,sandbox_id,owner_id,owner_epoch,command_id,expected_revision,root_identity,
                 phase,effect_certainty,updated_utc)
                VALUES ('delete-1','sandbox-1','owner',?,'command-1',1,'foreign-root','planned',1,?)""",
                (EPOCH, CREATED))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "unresolved effect retains"):
            self.compact()


if __name__ == "__main__":
    unittest.main()
