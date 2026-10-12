"""Tests for tools/check_design.py (standard library unittest)."""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_design as cd  # noqa: E402

FOUNDATION_STUB = '''syntax = "proto3";
package arcforges.foundation.v1;
message Id { optional bytes value = 1 [json_name = "value"]; }
message RequestMeta { Id command_id = 1 [json_name = "commandId"]; }
message ResponseMeta { optional string x = 1 [json_name = "x"]; }
message ArcError { optional string code = 1 [json_name = "code"]; }
message Receipt { Id command_id = 1 [json_name = "commandId"]; }
'''

GOOD = '''syntax = "proto3";
package arcforges.node.v1;
import "arcforges/foundation/v1/foundation.proto";

enum ThingState {
  THING_STATE_UNSPECIFIED = 0;
  THING_STATE_NEW = 1;
  THING_STATE_DONE = 2;
}

// Things.
service ThingService {
  // Make a thing.
  // auth: HUMAN=A SCRIPT=A AGENT=P REMOTE=-
  // idempotency: command_id
  // deadline: 5 s
  // stream: none
  // errors: STATE/not_found
  // locality: node
  rpc Make(ThingServiceMakeRequest) returns (ThingServiceMakeResponse);
}
message ThingServiceMakeRequest {
  arcforges.foundation.v1.RequestMeta meta = 1 [json_name = "meta"];
  reserved 2 to 9;
  optional string name = 10 [json_name = "name"]; // validate: 1..64 chars
}
message ThingServiceMakeResponse {
  arcforges.foundation.v1.ResponseMeta meta = 1 [json_name = "meta"];
  oneof outcome {
    ThingServiceMakeValue value = 2 [json_name = "value"];
    arcforges.foundation.v1.ArcError error = 3 [json_name = "error"];
  }
  reserved 4 to 9;
}
message ThingServiceMakeValue {
  optional ThingState state = 10 [json_name = "state"];
}
'''


class ProtoFixture:
    def __init__(self, text: str):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.proto_dir = base / "proto"
        (self.proto_dir / "arcforges/node/v1").mkdir(parents=True)
        (self.proto_dir / "arcforges/node/v1/thing.proto").write_text(text, encoding="utf-8")
        self.foundation = base / "ref/arcforges/foundation/v1/foundation.proto"
        self.foundation.parent.mkdir(parents=True)
        self.foundation.write_text(FOUNDATION_STUB, encoding="utf-8")
        self.errors = base / "errors.md"
        self.errors.write_text("| `STATE/not_found` | x | x | x | x |\n", encoding="utf-8")

    def model(self):
        model = cd.ProtoModel()
        files = sorted(self.proto_dir.rglob("*.proto"))
        for p in files:
            cd.parse_proto(p, p.relative_to(self.proto_dir).as_posix(), model)
        cd.parse_proto(self.foundation, "foundation", model)
        return model, files

    def check(self):
        model, files = self.model()
        rep = cd.Report()
        old = (cd.ERRORS_MD, cd.FOUNDATION, cd.FOUNDATION_SHA256)
        cd.ERRORS_MD, cd.FOUNDATION = self.errors, self.foundation
        cd.FOUNDATION_SHA256 = __import__("hashlib").sha256(cd.read(self.foundation).encode()).hexdigest()
        try:
            cd.check_protos(rep, model, files)
        finally:
            cd.ERRORS_MD, cd.FOUNDATION, cd.FOUNDATION_SHA256 = old
        return rep

    def close(self):
        self.tmp.cleanup()


class ProtoChecks(unittest.TestCase):
    def run_fixture(self, text):
        fx = ProtoFixture(text)
        try:
            return fx.check()
        finally:
            fx.close()

    def test_camel(self):
        self.assertEqual(cd.camel("mem_expected_bytes"), "memExpectedBytes")
        self.assertEqual(cd.camel("id"), "id")

    def test_good_fixture_passes(self):
        rep = self.run_fixture(GOOD)
        self.assertEqual(rep.errors, [])

    def test_parse_annotations(self):
        fx = ProtoFixture(GOOD)
        try:
            model, _ = fx.model()
        finally:
            fx.close()
        rpc = model.rpcs[0]
        self.assertEqual(rpc.ann["errors"], "STATE/not_found")
        self.assertEqual(rpc.doc, ["Make a thing."])
        self.assertIn("arcforges.node.v1.ThingState", model.enums)

    def test_missing_annotation(self):
        rep = self.run_fixture(GOOD.replace("  // locality: node\n", ""))
        self.assertTrue(any("lacks annotation 'locality'" in e for e in rep.errors))

    def test_unknown_error_code(self):
        rep = self.run_fixture(GOOD.replace("STATE/not_found", "STATE/nope"))
        self.assertTrue(any("STATE/nope" in e for e in rep.errors))

    def test_missing_json_name(self):
        rep = self.run_fixture(GOOD.replace(' [json_name = "name"]', ""))
        self.assertTrue(any("lacks json_name" in e for e in rep.errors))

    def test_missing_optional(self):
        rep = self.run_fixture(GOOD.replace("optional string name", "string name"))
        self.assertTrue(any("must be optional" in e for e in rep.errors))

    def test_missing_validate(self):
        rep = self.run_fixture(GOOD.replace(" // validate: 1..64 chars", ""))
        self.assertTrue(any("lacks a validate: rule" in e for e in rep.errors))

    def test_low_field_number(self):
        rep = self.run_fixture(GOOD.replace("optional string name = 10", "optional string name = 9"))
        self.assertTrue(any("numbered below 10" in e for e in rep.errors))


class MachineChecks(unittest.TestCase):
    def setUp(self):
        fx = ProtoFixture(GOOD)
        self.model, _ = fx.model()
        fx.close()

    def machine(self, **over):
        m = {"id": "SM-THING", "title": "Thing", "enum": "arcforges.node.v1.ThingState", "persisted": "-", "owner": "-",
             "initial": ["NEW"], "terminal": ["DONE"],
             "transitions": [{"from": ["NEW"], "to": "DONE", "on": "Make"}]}
        m.update(over)
        return {"machines": [m]}

    def test_valid(self):
        rep = cd.Report()
        cd.check_machines(rep, self.model, self.machine())
        self.assertEqual(rep.errors, [])

    def test_state_not_in_enum(self):
        rep = cd.Report()
        cd.check_machines(rep, self.model, self.machine(transitions=[{"from": ["NEW"], "to": "GONE", "on": "x"}], terminal=["GONE"]))
        self.assertTrue(any("not in" in e for e in rep.errors))
        self.assertTrue(any("never used" in e for e in rep.errors))

    def test_terminal_exit_needs_reopen(self):
        rep = cd.Report()
        data = self.machine(transitions=[{"from": ["NEW"], "to": "DONE", "on": "x"}, {"from": ["DONE"], "to": "NEW", "on": "again"}])
        cd.check_machines(rep, self.model, data)
        self.assertTrue(any("without reopen" in e for e in rep.errors))
        data["machines"][0]["transitions"][1]["reopen"] = True
        rep = cd.Report()
        cd.check_machines(rep, self.model, data)
        self.assertEqual(rep.errors, [])

    def test_render_is_deterministic(self):
        data = self.machine()
        self.assertEqual(cd.render_machines(data), cd.render_machines(data))
        self.assertIn("stateDiagram-v2", cd.render_machines(data))


class RepositoryState(unittest.TestCase):
    def test_repository_checks_pass(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cd.main([])
        self.assertEqual(code, 0, buf.getvalue())

    def test_traceability_covers_every_requirement(self):
        model = json.loads(cd.read(cd.TRACE_JSON))
        self.assertEqual({r["id"] for r in model["requirements"]}, cd.requirement_ids())


class PlanConsistency(unittest.TestCase):
    def model_and_graph(self):
        model = {"requirements": [{"id": "R-EXE-001", "tasks": ["AF-NODE-02"]}]}
        graph = {"tasks": [{"id": tid, "requirements": ["R-EXE-001"] if tid == "AF-NODE-02" else []}
                           for tid in sorted(cd.task_ids_in_design())]}
        return model, graph

    def test_matching_mappings_pass(self):
        model, graph = self.model_and_graph()
        rep = cd.Report()
        cd.check_plan_consistency(rep, model, graph)
        self.assertEqual(rep.errors, [])

    def test_disagreeing_mappings_fail(self):
        model, graph = self.model_and_graph()
        next(t for t in graph["tasks"] if t["id"] == "AF-EXEC-01")["requirements"] = ["R-EXE-001"]
        rep = cd.Report()
        cd.check_plan_consistency(rep, model, graph)
        self.assertTrue(any("R-EXE-001 lists tasks" in e for e in rep.errors), rep.errors)

    def test_unknown_task_fails(self):
        model, graph = self.model_and_graph()
        model["requirements"][0]["tasks"].append("AF-NOPE-01")
        rep = cd.Report()
        cd.check_plan_consistency(rep, model, graph)
        self.assertTrue(any("unknown task AF-NOPE-01" in e for e in rep.errors), rep.errors)


if __name__ == "__main__":
    unittest.main()
