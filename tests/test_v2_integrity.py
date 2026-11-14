"""V2 authority boundaries and PostgreSQL structural checks; no native runtime qualification."""
import hashlib
import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_design as cd  # noqa: E402


class StateStorageChecks(unittest.TestCase):
    """A persisted wire-state model must agree with the SQL states it can write."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.docs = Path(self.tmp.name)
        (self.docs / "data").mkdir()
        self.sql = self.docs / "data/node-store.sql"
        self.sql.write_text("CREATE TABLE limit_application (state TEXT NOT NULL CHECK(state IN ('pending','effective'))) STRICT;", encoding="utf-8")
        self.machine = {"id": "SM-EXAMPLE", "persisted": True,
                        "storage": {"table": "limit_application", "column": "state", "encoding": "lowercase_enum"}}

    def check(self, machine=None):
        rep = cd.Report()
        with patch.object(cd, "DOCS", self.docs):
            cd.check_machine_storage(rep, machine or self.machine, {"PENDING", "EFFECTIVE"})
        return rep.errors

    def test_matching_storage_passes(self):
        self.assertEqual(self.check(), [])

    def test_nonpersisted_claim_fails_for_stored_state(self):
        machine = copy.deepcopy(self.machine)
        machine["persisted"] = False
        self.assertTrue(any("persisted=true" in error for error in self.check(machine)))

    def test_sql_state_addition_or_omission_fails(self):
        for states in ("'pending'", "'pending','effective','unknown'"):
            with self.subTest(states=states):
                self.sql.write_text(f"CREATE TABLE limit_application (state TEXT NOT NULL CHECK(state IN ({states}))) STRICT;", encoding="utf-8")
                self.assertTrue(any("disagree with enum" in error for error in self.check()))

    def test_missing_closed_constraint_and_unsafe_location_fail(self):
        self.sql.write_text("CREATE TABLE limit_application (state TEXT NOT NULL) STRICT;", encoding="utf-8")
        self.assertTrue(any("closed IN check" in error for error in self.check()))
        machine = copy.deepcopy(self.machine)
        machine["storage"]["table"] = "../other"
        self.assertTrue(any("safe table and column" in error for error in self.check(machine)))


class ArchiveChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.archive = Path(self.tmp.name) / "history"
        self.archive.mkdir()
        (self.archive / "README.md").write_bytes(b"Frozen original\n")
        self.manifest = {
            "source_repository": "ArcForges/ArcForges-Design",
            "source_commit": cd.HISTORY_SOURCE_COMMIT,
            "files": [{"path": "README.md", "sha256": hashlib.sha256(b"Frozen original\n").hexdigest()}],
        }
        self.write_manifest()
        self.pin = hashlib.sha256((self.archive / "snapshot.json").read_bytes()).hexdigest()

    def write_manifest(self):
        (self.archive / "snapshot.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def check(self):
        rep = cd.Report()
        with patch.multiple(cd, HISTORY_DIR=self.archive, HISTORY_MANIFEST_SHA256=self.pin):
            cd.check_history(rep)
        return rep

    def test_frozen_bytes_pass(self):
        self.assertEqual(self.check().errors, [])

    def test_changed_archive_bytes_fail(self):
        (self.archive / "README.md").write_bytes(b"Rewritten product authority\n")
        self.assertTrue(any("SHA-256 mismatch for README.md" in e for e in self.check().errors))

    def test_rebaselining_manifest_does_not_hide_tampering(self):
        (self.archive / "README.md").write_bytes(b"Rewritten\n")
        self.manifest["files"][0]["sha256"] = hashlib.sha256(b"Rewritten\n").hexdigest()
        self.write_manifest()
        self.assertTrue(any("snapshot.json SHA-256 changed" in e for e in self.check().errors))

    def test_missing_file_and_unmanifested_file_fail(self):
        (self.archive / "README.md").unlink()
        (self.archive / "new-active-task.md").write_text("Do new work", encoding="utf-8")
        errors = self.check().errors
        self.assertTrue(any("missing or symlinked file README.md" in e for e in errors), errors)
        self.assertTrue(any("unmanifested files" in e for e in errors), errors)

    def test_unsafe_manifest_path_fails_without_reading_outside(self):
        self.manifest["files"][0]["path"] = "../outside.md"
        self.write_manifest()
        self.assertTrue(any("unsafe path" in e for e in self.check().errors))

    def test_main_retains_archive_gate(self):
        (self.archive / "README.md").write_bytes(b"Tampered\n")
        output = io.StringIO()
        with patch.multiple(cd, HISTORY_DIR=self.archive, HISTORY_MANIFEST_SHA256=self.pin), redirect_stdout(output):
            status = cd.main([])
        self.assertEqual(status, 1, output.getvalue())
        self.assertIn("SHA-256 mismatch for README.md", output.getvalue())


class AuthorityChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.docs = self.root / "docs"
        self.docs.mkdir()
        self.ref = self.docs / "contracts/reference/pinned"
        self.ref.mkdir(parents=True)
        self.patch = patch.multiple(cd, ROOT=self.root, DOCS=self.docs, REF_DIR=self.ref)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def put(self, relative, text):
        path = self.docs / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_historical_task_citations_do_not_become_active_assignments(self):
        self.put("research/audit.md", "Historical AF-EXEC-01. Replacement AFV2-MXC-02.")
        self.put("contracts/reference/pinned/README.md", "Immutable AF-CON-01 reference.")
        self.put("architecture/runtime.md", "Delivery owner AFV2-CORE-02.")
        rep = cd.Report()
        cd.check_obsolete_task_references(rep)
        self.assertEqual(rep.errors, [])
        self.assertEqual(set(cd.task_ids_in_design()), {"AFV2-MXC-02", "AFV2-CORE-02"})

    def test_obsolete_task_in_normative_document_fails(self):
        self.put("architecture/runtime.md", "Next execute AF-CTR-07.")
        rep = cd.Report()
        cd.check_obsolete_task_references(rep)
        self.assertTrue(any("obsolete executable task ID AF-CTR-07" in e for e in rep.errors), rep.errors)

    def test_obsolete_task_in_traceability_fails(self):
        req = self.put("product/requirements.md", "| R-RUN-001 | Run |\n")
        trace = self.put("traceability/model.json", json.dumps({"requirements": [
            {"id": "R-RUN-001", "tasks": ["AF-EXEC-01"], "design": ["docs/product/requirements.md"]},
        ]}))
        rep = cd.Report()
        with patch.multiple(cd, REQUIREMENTS_MD=req, TRACE_JSON=trace):
            cd.check_traceability(rep, None)
        self.assertTrue(any("obsolete or malformed task ID 'AF-EXEC-01'" in e for e in rep.errors), rep.errors)

    def test_extended_verification_ids_are_checked(self):
        req = self.put("product/requirements.md", "| R-MXC-001 | MXC |\n")
        ver = self.put("verification/platform-capabilities.md",
                       "| V-MXC-01 | source |\n| A-MXC-01 | assumption |\n| F-AOT-01 | future |\n")
        machines = self.put("state-machines/machines.json", '{"machines": []}')
        target = self.put("architecture/backend.md", "V-MXC-01, A-MXC-01 and F-AOT-01.")
        with patch.multiple(cd, REQUIREMENTS_MD=req, VERIFICATION_MD=ver, MACHINES_JSON=machines):
            good = cd.Report()
            cd.check_references(good)
            self.assertEqual(good.errors, [])
            target.write_text("V-MXC-99", encoding="utf-8")
            bad = cd.Report()
            cd.check_references(bad)
        self.assertTrue(any("unknown verification ID V-MXC-99" in e for e in bad.errors), bad.errors)

    def test_active_namespace_and_import_boundaries(self):
        proto_root = self.docs / "contracts/proto"
        path = self.put("contracts/proto/arcforges/sandbox/v2/test.proto",
                        'package arcforges.sandbox.v2;\nimport "arcforges/foundation/v1/foundation.proto";\n')
        with patch.object(cd, "PROTO_DIR", proto_root):
            good = cd.Report()
            cd.check_v2_namespaces(good, [path])
            self.assertEqual(good.errors, [])
            path.write_text('package arcforges.node.v1;\nimport "arcforges/node/v1/tasks.proto";\n', encoding="utf-8")
            bad = cd.Report()
            cd.check_v2_namespaces(bad, [path])
        self.assertTrue(any("must be an arcforges V2 namespace" in e for e in bad.errors), bad.errors)
        self.assertTrue(any("imports obsolete V1 surface" in e for e in bad.errors), bad.errors)


class PostgresStructureChecks(unittest.TestCase):
    SQL = """CREATE SCHEMA management;
CREATE TABLE management.item (
    item_id uuid PRIMARY KEY,
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    state smallint NOT NULL CHECK (state IN (1, 2)),
    note text CHECK (note <> 'a,;--b''c')
);
CREATE INDEX item_account ON management.item (account_id);
"""
    DOC = """PostgreSQL structural specification: `management.item`.
Numbered migration, checksum, backup, restore and least-privilege requirements.
AFV2-CENTER-01 executes real PostgreSQL; structural checks do not prove runtime behavior.
"""

    def check(self, sql=None, doc=None):
        with tempfile.TemporaryDirectory() as tmp:
            path, documentation = Path(tmp) / "cloud-store.sql", Path(tmp) / "cloud-store.md"
            path.write_text(self.SQL if sql is None else sql, encoding="utf-8")
            documentation.write_text(self.DOC if doc is None else doc, encoding="utf-8")
            rep = cd.Report()
            with patch.object(cd.sqlite3, "connect", side_effect=AssertionError("PostgreSQL cannot be checked as SQLite")):
                cd.check_postgres_structure(rep, path, documentation)
            return rep

    def test_structural_success_is_not_runtime_proof(self):
        rep = self.check()
        self.assertEqual(rep.errors, [])
        self.assertTrue(any("NOT PostgreSQL execution/migration proof" in n for n in rep.notes), rep.notes)

    def test_foreign_key_wrong_type_fails(self):
        rep = self.check(self.SQL.replace("account_id uuid", "account_id text"))
        self.assertTrue(any("foreign-key type mismatch" in e for e in rep.errors), rep.errors)

    def test_unknown_reference_and_sqlite_type_fail(self):
        rep = self.check(self.SQL.replace("identity.user", "identity.missing").replace("note text", "note BLOB"))
        self.assertTrue(any("unknown table identity.missing" in e for e in rep.errors), rep.errors)
        self.assertTrue(any("PostgreSQL type blob" in e for e in rep.errors), rep.errors)

    def test_undocumented_table_and_missing_migration_protocol_fail(self):
        rep = self.check(doc="PostgreSQL")
        self.assertTrue(any("does not document table management.item" in e for e in rep.errors), rep.errors)
        self.assertTrue(any("missing migration protocol topic checksum" in e for e in rep.errors), rep.errors)

    def test_unknown_index_column_and_unbalanced_ddl_fail(self):
        bad_index = self.check(self.SQL.replace("ON management.item (account_id)", "ON management.item (missing)"))
        self.assertTrue(any("index references unknown column" in e for e in bad_index.errors), bad_index.errors)
        bad_syntax = self.check(self.SQL.replace("state IN (1, 2)", "state IN (1, 2"))
        self.assertTrue(any("unterminated SQL string or parentheses" in e for e in bad_syntax.errors), bad_syntax.errors)


if __name__ == "__main__":
    unittest.main()
