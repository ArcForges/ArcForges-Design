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


class ErrorPairChecks(unittest.TestCase):
    HEADER = "| Category / code | Meaning | Retry advice | Effect | Details |\n|---|---|---|---|---|\n"

    def run_rows(self, rows: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "errors.md"
            path.write_text(self.HEADER + rows, encoding="utf-8")
            old = cd.ERRORS_MD
            cd.ERRORS_MD = path
            try:
                rep = cd.Report()
                cd.check_error_pairs(rep)
            finally:
                cd.ERRORS_MD = old
            return rep.errors

    def test_the_catalogue_passes(self):
        rep = cd.Report()
        cd.check_error_pairs(rep)
        self.assertEqual(rep.errors, [])

    def test_conditional_rows_pass(self):
        rows = (
            "| `STATE/peer_unreachable` | x | `AFTER_TIME` with `DID_NOT_HAPPEN`; with `UNKNOWN`, `RECONCILE` reading `PeerService.ListPeers` | `DID_NOT_HAPPEN` or `UNKNOWN` | — |\n"
            "| `INTERNAL/internal` | x | `NEVER` when the effect is `UNKNOWN`; `AFTER_TIME` once when it is `DID_NOT_HAPPEN` or `HAPPENED` | `UNKNOWN` unless known | — |\n"
            "| `STATE/in_use` | x | `AFTER_TIME` | `DID_NOT_HAPPEN` | — |\n"
        )
        self.assertEqual(self.run_rows(rows), [])

    def test_the_rows_before_the_amendment_fail(self):
        # The four rows of the catalogue at ArcForges-Design 44a86a9, which paired UNKNOWN with AFTER_TIME.
        for row in (
            "| `STATE/peer_unreachable` | x | `AFTER_TIME` | `DID_NOT_HAPPEN` or `UNKNOWN` | — |\n",
            "| `STATE/cloud_unreachable` | x | `AFTER_TIME` | `DID_NOT_HAPPEN` or `UNKNOWN` | — |\n",
            "| `EXECUTION/provider_error` | x | `AFTER_TIME` | `UNKNOWN` | — |\n",
            "| `INTERNAL/internal` | x | `AFTER_TIME` once | `UNKNOWN` unless known | — |\n",
        ):
            with self.subTest(row=row):
                errors = self.run_rows(row)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("advises AFTER_TIME", errors[0])

    def test_a_clause_naming_unknown_with_after_time_fails(self):
        row = "| `STATE/peer_unreachable` | x | `AFTER_TIME` with `DID_NOT_HAPPEN` or `UNKNOWN` | `DID_NOT_HAPPEN` or `UNKNOWN` | — |\n"
        self.assertEqual(len(self.run_rows(row)), 1)

    def test_a_qualified_first_cell_is_still_checked(self):
        row = "| `EXECUTION/provider_error` (Play) | x | `AFTER_TIME` | `UNKNOWN` | — |\n"
        self.assertTrue(any("advises AFTER_TIME" in e for e in self.run_rows(row)), self.run_rows(row))

    def test_names_without_backticks_are_still_checked(self):
        row = "| `EXECUTION/provider_error` | x | AFTER_TIME | unknown (the call may have committed) | — |\n"
        self.assertTrue(any("advises AFTER_TIME" in e for e in self.run_rows(row)), self.run_rows(row))

    def test_a_row_without_a_code_fails(self):
        row = "| EXECUTION/provider_error | x | `AFTER_TIME` | `UNKNOWN` | — |\n"
        self.assertTrue(any("does not start with" in e for e in self.run_rows(row)), self.run_rows(row))

    def test_after_time_in_another_case_or_with_a_space_is_still_checked(self):
        for retry in ("after_time", "After_Time", "AFTER TIME"):
            with self.subTest(retry=retry):
                row = f"| `EXECUTION/provider_error` | x | {retry} | `UNKNOWN` | — |\n"
                self.assertTrue(any("advises AFTER_TIME" in e for e in self.run_rows(row)), self.run_rows(row))

    def test_the_full_run_fails_on_a_pre_amendment_row(self):
        # The provider_error row of ArcForges-Design 44a86a9 inside a copy of the real catalogue: main() must exit 1, so removing
        # the gate's call from main() fails this test.
        old_row = "| `EXECUTION/provider_error` | A provider API (Google Play, Paddle) failed | `AFTER_TIME` | `UNKNOWN` | — |"
        text = cd.read(cd.ERRORS_MD)
        current = next(line for line in text.split("\n") if line.startswith("| `EXECUTION/provider_error` |"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "errors.md"
            path.write_text(text.replace(current, old_row), encoding="utf-8")
            saved = cd.ERRORS_MD
            cd.ERRORS_MD = path
            out = io.StringIO()
            try:
                with redirect_stdout(out):
                    status = cd.main([])
            finally:
                cd.ERRORS_MD = saved
        self.assertEqual(status, 1, out.getvalue())
        self.assertIn("EXECUTION/provider_error advises AFTER_TIME", out.getvalue())

    def test_a_row_with_another_cell_count_fails(self):
        row = "| `STATE/peer_unreachable` | x | `AFTER_TIME` with `DID_NOT_HAPPEN` | `UNKNOWN` |\n"
        self.assertTrue(any("expected 5" in e for e in self.run_rows(row)))


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

    def test_initial_guards_are_rendered_and_cover_the_initial_states(self):
        data = self.machine(initial_guards={"NEW": "kind = synthetic"})
        rep = cd.Report()
        cd.check_machines(rep, self.model, data)
        self.assertEqual(rep.errors, [])
        self.assertIn("Initial guard for `NEW`: kind = synthetic", cd.render_machines(data))

    def test_missing_or_extra_initial_guard_is_rejected(self):
        for guards in ({}, {"DONE": "not initial"}, {"NEW": "ok", "DONE": "extra"}):
            with self.subTest(guards=guards):
                rep = cd.Report()
                cd.check_machines(rep, self.model, self.machine(initial_guards=guards))
                self.assertTrue(any("cover exactly" in e for e in rep.errors), rep.errors)

    def test_empty_initial_guard_is_rejected(self):
        rep = cd.Report()
        cd.check_machines(rep, self.model, self.machine(initial_guards={"NEW": " "}))
        self.assertTrue(any("nonempty text" in e for e in rep.errors), rep.errors)

    def test_render_is_deterministic(self):
        data = self.machine()
        self.assertEqual(cd.render_machines(data), cd.render_machines(data))
        self.assertIn("stateDiagram-v2", cd.render_machines(data))

    def test_render_truncated_transition_labels_do_not_leave_trailing_whitespace(self):
        text = cd.render_machines(self.machine(transitions=[{"from": ["NEW"], "to": "DONE", "on": "a" * 59 + " tail"}]))
        edge = next(line for line in text.splitlines() if "NEW --> DONE" in line)
        self.assertEqual(edge, "  NEW --> DONE : " + "a" * 59)
        self.assertFalse(any(line.rstrip() != line for line in text.splitlines()))

    def stored_machine(self, **over):
        m = self.machine()["machines"][0]
        del m["enum"]
        m.update({"state_values": {"NEW": 1, "DONE": 3},
                  "state_source": {"repository": "example/Cloud", "commit": "a" * 40,
                                   "paths": ["center/schema.sql", "center/routed.go"]}})
        m.update(over)
        return {"machines": [m]}

    def test_stored_states_have_a_distinct_source_and_rendered_values(self):
        data = self.stored_machine()
        rep = cd.Report()
        cd.check_machines(rep, self.model, data)
        self.assertEqual(rep.errors, [])
        text = cd.render_machines(data)
        self.assertIn("non-wire stored states", text)
        self.assertIn("`NEW=1`", text)
        self.assertIn("`example/Cloud@" + "a" * 40 + "`", text)
        self.assertNotIn("Enum: `arcforges.node.v1.ThingState`", text)

    def test_stored_states_need_exactly_one_authority(self):
        for data in (self.stored_machine(enum="arcforges.node.v1.ThingState"), self.machine(state_values={"NEW": 1}),
                     self.machine(enum=None)):
            with self.subTest(data=data):
                rep = cd.Report()
                cd.check_machines(rep, self.model, data)
                self.assertNotEqual(rep.errors, [])
        data = self.machine()
        del data["machines"][0]["enum"]
        rep = cd.Report()
        cd.check_machines(rep, self.model, data)
        self.assertTrue(any("exactly one" in e for e in rep.errors), rep.errors)
        data = self.machine(state_source={"repository": "example/Cloud", "commit": "a" * 40, "paths": ["center/schema.sql"]})
        rep = cd.Report()
        cd.check_machines(rep, self.model, data)
        self.assertTrue(any("enum-backed machines cannot" in e for e in rep.errors), rep.errors)

    def test_stored_states_refuse_invalid_or_ambiguous_values(self):
        for values in ({}, {"NEW": 1, "DONE": 1}, {"NEW": True, "DONE": 3},
                       {"NEW": 0, "DONE": 3}, {"NEW": 32768, "DONE": 3}, {"New": 1, "DONE": 3}):
            with self.subTest(values=values):
                rep = cd.Report()
                cd.check_machines(rep, self.model, self.stored_machine(state_values=values))
                self.assertNotEqual(rep.errors, [])

    def test_stored_states_require_an_immutable_safe_source(self):
        source = {"repository": "example/Cloud", "commit": "a" * 40, "paths": ["center/schema.sql"]}
        invalid = [None, {}, {**source, "extra": "x"}, {**source, "commit": "a" * 12},
                   {**source, "repository": "../Cloud"}, {**source, "commit": "0" * 40}, {**source, "paths": []},
                   {**source, "paths": ["../schema.sql"]}, {**source, "paths": ["/absolute.sql"]},
                   {**source, "paths": ["center/x", "center/x"]}, {**source, "paths": [False]},
                   {**source, "commit": "A" * 40}]
        for value in invalid:
            with self.subTest(source=value):
                rep = cd.Report()
                cd.check_machines(rep, self.model, self.stored_machine(state_source=value))
                self.assertTrue(any("repository, full commit and safe source paths" in e for e in rep.errors), rep.errors)

    def test_stored_states_require_exact_coverage_and_reachability(self):
        cases = [
            (self.stored_machine(state_values={"NEW": 1, "DONE": 3, "MISSING": 8}), "never used"),
            (self.stored_machine(transitions=[{"from": ["NEW"], "to": "EXTRA", "on": "x"}], terminal=["EXTRA"]), "not in"),
            (self.stored_machine(state_values={"NEW": 1, "DONE": 3, "LOST": 8}, transitions=[
                {"from": ["NEW"], "to": "DONE", "on": "x"}, {"from": ["LOST"], "to": "DONE", "on": "x"}]), "unreachable"),
            (self.stored_machine(transitions=[{"from": ["NEW"], "to": "DONE", "on": "x"},
                                               {"from": ["DONE"], "to": "NEW", "on": "x"}]), "without reopen"),
        ]
        for data, message in cases:
            with self.subTest(message=message):
                rep = cd.Report()
                cd.check_machines(rep, self.model, data)
                self.assertTrue(any(message in e for e in rep.errors), rep.errors)

    def test_stored_states_cannot_use_enum_only_exemptions(self):
        for field in ("pseudo_states", "response_only"):
            rep = cd.Report()
            cd.check_machines(rep, self.model, self.stored_machine(**{field: ["OTHER"]}))
            self.assertTrue(any("enum-only" in e for e in rep.errors), rep.errors)


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
