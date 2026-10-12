#!/usr/bin/env python3
"""Design repository checks for the ArcForges flagship design.

Usage:
  python tools/check_design.py                 # run all checks (protoc optional unless --require-protoc)
  python tools/check_design.py --write         # regenerate generated documents, then check
  python tools/check_design.py --plan <path>   # also cross-check task IDs against the Plan delivery graph
  python tools/check_design.py --compile       # also generate and build C# from the protos (needs dotnet)

Standard library only. Exit code 0 when every check passes, 1 otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PROTO_DIR = DOCS / "contracts" / "proto"
REF_DIR = DOCS / "contracts" / "reference" / "contracts-b774c322"
FOUNDATION = REF_DIR / "arcforges" / "foundation" / "v1" / "foundation.proto"
FOUNDATION_SHA256 = "e7e634103664dcca4c63383dd0eda5d90b408edb4786bfdf4a148856fed92736"
ERRORS_MD = DOCS / "contracts" / "errors.md"
CATALOGUE_MD = DOCS / "contracts" / "api-catalogue.md"
MACHINES_JSON = DOCS / "state-machines" / "machines.json"
MACHINES_MD = DOCS / "state-machines" / "README.md"
REQUIREMENTS_MD = DOCS / "product" / "requirements.md"
TRACE_JSON = DOCS / "traceability" / "model.json"
VERIFICATION_MD = DOCS / "verification" / "platform-capabilities.md"

ANN_REQUIRED = ["auth", "idempotency", "deadline", "stream", "errors", "locality"]
ANN_KEYS = ANN_REQUIRED + ["state"]
IMPLICIT_ERRORS = {"INTERNAL/internal", "RESOURCE/overloaded", "STATE/node_stopping",
                   "AUTHENTICATION/unauthenticated", "RESOURCE/rate_limited"}
SCALARS = {"string", "bytes", "bool", "int32", "int64", "uint32", "uint64", "sint32", "sint64",
           "fixed32", "fixed64", "sfixed32", "sfixed64", "double", "float"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


# --------------------------------------------------------------------------- proto model

@dataclass
class Field:
    label: str
    type: str
    name: str
    number: int
    options: str
    comment: str
    in_oneof: bool


@dataclass
class Message:
    name: str
    file: str
    fields: list[Field] = field(default_factory=list)
    reserved: list[str] = field(default_factory=list)
    oneofs: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class Rpc:
    service: str
    name: str
    request: str
    response: str
    stream: bool
    doc: list[str]
    ann: dict[str, str]
    file: str
    package: str


@dataclass
class ProtoModel:
    messages: dict[str, Message] = field(default_factory=dict)  # key: package.Name
    enums: dict[str, list[str]] = field(default_factory=dict)  # key: package.Name -> value names
    rpcs: list[Rpc] = field(default_factory=list)
    services: dict[str, tuple[str, str, list[str]]] = field(default_factory=dict)  # key -> (file, package, doc)


FIELD_RE = re.compile(r"^\s*(optional |repeated )?(map<[^>]+>|[\w.]+)\s+(\w+)\s*=\s*(\d+)\s*(\[[^\]]*\])?\s*;\s*(?://\s*(.*))?$")
RPC_RE = re.compile(r"^\s*rpc\s+(\w+)\((\w+)\)\s+returns\s+\((stream\s+)?(\w+)\);")


def parse_proto(path: Path, rel: str, model: ProtoModel) -> None:
    text = read(path)
    pkg = re.search(r"^package\s+([\w.]+);", text, re.M).group(1)
    lines = text.split("\n")
    stack: list[tuple[str, str]] = []  # (kind, name)
    pending_comments: list[str] = []
    current_service = None
    for line in lines:
        s = line.strip()
        if s.startswith("//"):
            pending_comments.append(s[2:].strip())
            continue
        m = re.match(r"^(message|enum|service|oneof)\s+(\w+)\s*\{$", s)
        if m:
            kind, name = m.groups()
            stack.append((kind, name))
            if kind == "message" and len([k for k, _ in stack if k == "message"]) == 1:
                model.messages[f"{pkg}.{name}"] = Message(name, rel)
            elif kind == "enum":
                model.enums[f"{pkg}.{name}"] = []
            elif kind == "service":
                current_service = name
                model.services[f"{pkg}.{name}"] = (rel, pkg, pending_comments[:])
            elif kind == "oneof":
                msg = top_message(stack, pkg, model)
                if msg:
                    msg.oneofs[name] = []
            pending_comments = []
            continue
        if s == "}":
            if stack:
                kind, _ = stack.pop()
                if kind == "service":
                    current_service = None
            pending_comments = []
            continue
        if not stack:
            pending_comments = []
            continue
        kind, name = stack[-1]
        if kind == "enum":
            em = re.match(r"^(\w+)\s*=\s*(\d+);", s)
            if em:
                model.enums[f"{pkg}.{name}"].append(em.group(1))
            pending_comments = []
            continue
        if kind == "service":
            rm = RPC_RE.match(line)
            if rm:
                ann: dict[str, str] = {}
                doc: list[str] = []
                for c in pending_comments:
                    km = re.match(r"^(\w+):\s*(.*)$", c)
                    if km and km.group(1) in ANN_KEYS:
                        ann[km.group(1)] = km.group(2)
                    else:
                        doc.append(c)
                model.rpcs.append(Rpc(current_service, rm.group(1), rm.group(2), rm.group(4), bool(rm.group(3)), doc, ann, rel, pkg))
            pending_comments = []
            continue
        if s.startswith("reserved"):
            msg = top_message(stack, pkg, model)
            if msg:
                msg.reserved.append(s)
            pending_comments = []
            continue
        fm = FIELD_RE.match(line)
        if fm and kind in ("message", "oneof"):
            msg = top_message(stack, pkg, model)
            if msg is not None and len([k for k, _ in stack if k == "message"]) == 1:
                f = Field((fm.group(1) or "").strip(), fm.group(2), fm.group(3), int(fm.group(4)), fm.group(5) or "", fm.group(6) or "", kind == "oneof")
                msg.fields.append(f)
                if kind == "oneof":
                    msg.oneofs[name].append(f.name)
        pending_comments = []


def top_message(stack, pkg, model):
    names = [n for k, n in stack if k == "message"]
    if not names:
        return None
    return model.messages.get(f"{pkg}.{names[0]}")


def load_protos() -> tuple[ProtoModel, list[Path]]:
    model = ProtoModel()
    files = sorted(PROTO_DIR.rglob("*.proto"))
    for p in files:
        parse_proto(p, p.relative_to(PROTO_DIR).as_posix(), model)
    parse_proto(FOUNDATION, "foundation", model)
    return model, files


def camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(x[:1].upper() + x[1:] for x in parts[1:])


def error_catalogue() -> set[str]:
    codes = set()
    for m in re.finditer(r"^\|\s*`([A-Z]+/[a-z_]+)`", read(ERRORS_MD), re.M):
        codes.add(m.group(1))
    return codes


def check_protos(rep: Report, model: ProtoModel, files: list[Path]) -> None:
    sha = hashlib.sha256(read(FOUNDATION).encode("utf-8")).hexdigest()
    if sha != FOUNDATION_SHA256:
        rep.error(f"pinned foundation.proto changed (sha256 {sha})")
    codes = error_catalogue()
    used: set[str] = set()
    for key, msg in model.messages.items():
        if msg.file == "foundation":
            continue
        for f in msg.fields:
            if f'json_name = "{camel(f.name)}"' not in f.options:
                rep.error(f"{msg.file}: {msg.name}.{f.name} lacks json_name \"{camel(f.name)}\"")
            base = f.type.split(".")[-1]
            singular_scalar = not f.label and not f.type.startswith("map<") and (f.type in SCALARS or any(k.endswith("." + base) for k in model.enums))
            if singular_scalar and not f.in_oneof:
                rep.error(f"{msg.file}: {msg.name}.{f.name} must be optional (explicit presence)")
    for rpc in model.rpcs:
        where = f"{rpc.file}: {rpc.service}.{rpc.name}"
        for k in ANN_REQUIRED:
            if not rpc.ann.get(k):
                rep.error(f"{where} lacks annotation '{k}'")
        if not rpc.doc:
            rep.error(f"{where} lacks a purpose comment")
        prefix = f"{rpc.service}{rpc.name}"
        if rpc.request != f"{prefix}Request":
            rep.error(f"{where}: request must be {prefix}Request")
        req = model.messages.get(f"{rpc.package}.{rpc.request}")
        if req is None:
            rep.error(f"{where}: request message missing")
        else:
            if not req.fields or req.fields[0].name != "meta" or req.fields[0].number != 1 or not req.fields[0].type.endswith("RequestMeta"):
                rep.error(f"{where}: request field 1 must be RequestMeta meta")
            if "reserved 2 to 9;" not in req.reserved:
                rep.error(f"{where}: request must reserve 2 to 9")
            for f in req.fields[1:]:
                if f.number < 10:
                    rep.error(f"{where}: request field {f.name} numbered below 10")
                needs_validate = f.label == "repeated" or f.type.startswith("map<") or f.type in ("string", "bytes") or f.type.endswith(".Id")
                if needs_validate and "validate:" not in f.comment:
                    rep.error(f"{where}: request field {f.name} lacks a validate: rule")
        if rpc.stream:
            if rpc.response != f"{prefix}Frame":
                rep.error(f"{where}: stream must return {prefix}Frame")
            fr = model.messages.get(f"{rpc.package}.{rpc.response}")
            if fr is None or "frame" not in fr.oneofs:
                rep.error(f"{where}: frame message must have oneof frame")
            elif not rpc.ann.get("stream", "").startswith("server"):
                rep.error(f"{where}: stream annotation must describe the server stream")
        else:
            if rpc.response != f"{prefix}Response":
                rep.error(f"{where}: response must be {prefix}Response")
            resp = model.messages.get(f"{rpc.package}.{rpc.response}")
            if resp is None or resp.oneofs.get("outcome") != ["value", "error"] or "reserved 4 to 9;" not in resp.reserved:
                rep.error(f"{where}: response must be meta=1, oneof outcome {{value=2; error=3}}, reserved 4 to 9")
            val = model.messages.get(f"{rpc.package}.{prefix}Value")
            if val is None:
                rep.error(f"{where}: value message missing")
            elif any(f.number < 10 for f in val.fields):
                rep.error(f"{where}: value fields must start at 10")
            if rpc.ann.get("stream") != "none":
                rep.error(f"{where}: unary method must have 'stream: none'")
        error_list = "" if rpc.ann.get("errors", "").startswith("none") else rpc.ann.get("errors", "")
        for code in [c.strip() for c in error_list.split(",") if c.strip()]:
            used.add(code)
            if code not in codes:
                rep.error(f"{where}: error code {code} is not in errors.md")
    unused = codes - used - IMPLICIT_ERRORS - {"INTERNAL/store_corrupt"}
    for code in sorted(unused):
        rep.note(f"error code {code} is catalogued but not named by any method")


def find_protoc() -> tuple[str | None, str | None]:
    exe = os.environ.get("ARCFORGES_PROTOC") or shutil.which("protoc")
    inc = os.environ.get("ARCFORGES_PROTOC_INCLUDE")
    if not exe:
        base = Path.home() / ".nuget" / "packages" / "grpc.tools"
        if base.is_dir():
            versions = sorted(base.iterdir(), key=lambda p: [int(x) for x in re.findall(r"\d+", p.name)])
            for v in reversed(versions):
                sub = "windows_x64" if os.name == "nt" else "linux_x64"
                cand = v / "tools" / sub / ("protoc.exe" if os.name == "nt" else "protoc")
                if cand.exists():
                    if os.name != "nt" and not os.access(cand, os.X_OK):
                        cand.chmod(0o755)  # NuGet extraction drops the execute bit
                    exe = str(cand)
                    inc = inc or str(v / "build" / "native" / "include")
                    break
    return exe, inc


def run_protoc(rep: Report, files: list[Path], require: bool, out_dir: Path | None = None) -> bool:
    exe, inc = find_protoc()
    if not exe:
        (rep.error if require else rep.note)("protoc not found (set ARCFORGES_PROTOC); proto compilation skipped")
        return False
    args = [exe, f"-I{PROTO_DIR}", f"-I{REF_DIR}"]
    if inc:
        args.append(f"-I{inc}")
    with tempfile.TemporaryDirectory() as tmp:
        args += [f"--descriptor_set_out={Path(tmp) / 'all.pb'}", "--include_imports"]
        if out_dir is not None:
            args += [f"--csharp_out={out_dir}"]
        args += [p.relative_to(PROTO_DIR).as_posix() for p in files]
        res = subprocess.run(args, cwd=PROTO_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        rep.error("protoc failed:\n" + res.stderr.strip())
        return False
    rep.note(f"protoc compiled {len(files)} files ({Path(exe).name})")
    return True


def compile_csharp(rep: Report, files: list[Path]) -> None:
    exe, inc = find_protoc()
    plugin = None
    if exe:
        cand = Path(exe).with_name("grpc_csharp_plugin.exe" if os.name == "nt" else "grpc_csharp_plugin")
        plugin = str(cand) if cand.exists() else None
    if not exe or not plugin or not shutil.which("dotnet"):
        rep.error("--compile needs protoc, grpc_csharp_plugin and dotnet")
        return
    with tempfile.TemporaryDirectory() as tmp:
        gen = Path(tmp) / "gen"
        gen.mkdir()
        base = [exe, f"-I{PROTO_DIR}", f"-I{REF_DIR}"] + ([f"-I{inc}"] if inc else [])
        res = subprocess.run(base + [f"--csharp_out={gen}", f"--grpc_out={gen}", f"--plugin=protoc-gen-grpc={plugin}"]
                             + [p.relative_to(PROTO_DIR).as_posix() for p in files], cwd=PROTO_DIR, capture_output=True, text=True)
        if res.returncode == 0:
            res = subprocess.run(base + [f"--csharp_out={gen}", "arcforges/foundation/v1/foundation.proto"], cwd=REF_DIR, capture_output=True, text=True)
        if res.returncode != 0:
            rep.error("C# generation failed: " + res.stderr.strip())
            return
        proj = Path(tmp) / "check.csproj"
        proj.write_text("""<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework>
<Nullable>disable</Nullable><ImplicitUsings>disable</ImplicitUsings><IsAotCompatible>true</IsAotCompatible>
<TreatWarningsAsErrors>true</TreatWarningsAsErrors><NoWarn>CS1591</NoWarn></PropertyGroup>
<ItemGroup><PackageReference Include="Google.Protobuf" Version="3.36.1" /><PackageReference Include="Grpc.Core.Api" Version="2.84.0" /></ItemGroup></Project>""", encoding="utf-8")
        res = subprocess.run(["dotnet", "build", str(proj), "-c", "Release", "-nologo", "-v", "q"], capture_output=True, text=True)
        if res.returncode != 0:
            rep.error("generated C# failed to build:\n" + (res.stdout + res.stderr)[-4000:])
        else:
            rep.note("generated C# built with zero warnings under IsAotCompatible")


def render_catalogue(model: ProtoModel) -> str:
    out = ["# API catalogue", "",
           "Generated by `tools/check_design.py --write` from the protos in [proto/](proto/). Do not edit by hand.",
           "Conventions and the annotation keys: [README.md](README.md). Error codes: [errors.md](errors.md).", ""]
    by_service: dict[str, list[Rpc]] = {}
    for r in model.rpcs:
        by_service.setdefault(f"{r.package}.{r.service}", []).append(r)
    total = sum(len(v) for v in by_service.values())
    out.append(f"{len(by_service)} services, {total} methods.")
    out.append("")
    out.append("| Service | Package | File | Methods |")
    out.append("|---|---|---|---|")
    for key in sorted(by_service, key=lambda k: (k.split(".")[1], k)):
        file, pkg, _ = model.services[key]
        name = key.split(".")[-1]
        out.append(f"| [{name}](#{(pkg.replace('.', '') + name).lower()}) | `{pkg}` | [{file}](proto/{file}) | {len(by_service[key])} |")
    for key in sorted(by_service, key=lambda k: (k.split(".")[1], k)):
        file, pkg, doc = model.services[key]
        name = key.split(".")[-1]
        out += ["", f'<a id="{(pkg.replace(".", "") + name).lower()}"></a>', "", f"## {pkg}.{name}", ""]
        if doc:
            out.append(" ".join(doc))
            out.append("")
        out.append("| Method | Purpose | Auth | Idempotency | Deadline | Stream | Errors | Locality | State |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        for r in by_service[key]:
            cells = [f"`{r.name}`", " ".join(r.doc)] + [r.ann.get(k, "") for k in ANN_KEYS]
            out.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------- state machines

def render_machines(data: dict) -> str:
    out = ["# State machines", "",
           "Generated by `tools/check_design.py --write` from [machines.json](machines.json). Do not edit by hand.",
           "States equal the named proto enum values (without the enum prefix); pseudo-states are marked.", ""]
    out.append("| ID | Machine | Enum | Persisted | Owner |")
    out.append("|---|---|---|---|---|")
    for m in data["machines"]:
        out.append(f"| [{m['id']}](#{m['id'].lower()}) | {m['title']} | `{m['enum']}` | {m['persisted']} | {m['owner']} |")
    for m in data["machines"]:
        out += ["", f'<a id="{m["id"].lower()}"></a>', "", f"## {m['id']} — {m['title']}", ""]
        out.append(f"- Enum: `{m['enum']}`; persisted: {m['persisted']}; owner: {m['owner']}.")
        out.append(f"- Initial: {', '.join('`' + s + '`' for s in m['initial'])}. Terminal: {', '.join('`' + s + '`' for s in m['terminal']) or 'none (long-lived)'}.")
        if m.get("pseudo_states"):
            out.append(f"- Pseudo-states (not in the enum): {', '.join(m['pseudo_states'])}.")
        if m.get("response_only"):
            out.append(f"- Response-only enum values (never stored): {', '.join(m['response_only'])}.")
        out += ["", "```mermaid", "stateDiagram-v2"]
        for s in m["initial"]:
            out.append(f"  [*] --> {s}")
        for t in m["transitions"]:
            label = t["on"].split(";")[0].replace(":", " ")[:60]
            for f in t["from"]:
                out.append(f"  {f} --> {t['to']} : {label}")
        for s in m["terminal"]:
            out.append(f"  {s} --> [*]")
        out += ["```", "", "| From | To | Trigger | Guard | Effect |", "|---|---|---|---|---|"]
        for t in m["transitions"]:
            cells = [", ".join(t["from"]), t["to"] + (" (reopen)" if t.get("reopen") else ""), t["on"], t.get("guard", ""), t.get("effect", "")]
            out.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    return "\n".join(out) + "\n"


def check_machines(rep: Report, model: ProtoModel, data: dict) -> None:
    ids = set()
    for m in data["machines"]:
        mid = m["id"]
        if mid in ids:
            rep.error(f"duplicate machine {mid}")
        ids.add(mid)
        enum = model.enums.get(m["enum"])
        if enum is None:
            rep.error(f"{mid}: enum {m['enum']} not found in protos")
            continue
        prefix = re.sub(r"(?<!^)([A-Z])", r"_\1", m["enum"].split(".")[-1]).upper() + "_"
        enum_states = {v[len(prefix):] for v in enum if v.startswith(prefix) and not v.endswith("_UNSPECIFIED")}
        pseudo = set(m.get("pseudo_states", []))
        response_only = set(m.get("response_only", []))
        states = set()
        for t in m["transitions"]:
            states.update(t["from"])
            states.add(t["to"])
        states |= set(m["initial"]) | set(m["terminal"])
        expected = enum_states - response_only
        missing = expected - states
        extra = states - expected - pseudo
        if missing:
            rep.error(f"{mid}: enum states never used: {sorted(missing)}")
        if extra:
            rep.error(f"{mid}: states not in {m['enum']}: {sorted(extra)}")
        reach = set(m["initial"])
        changed = True
        while changed:
            changed = False
            for t in m["transitions"]:
                if any(f in reach for f in t["from"]) and t["to"] not in reach:
                    reach.add(t["to"])
                    changed = True
        unreachable = states - reach
        if unreachable:
            rep.error(f"{mid}: unreachable states {sorted(unreachable)}")
        for t in m["transitions"]:
            if any(f in m["terminal"] for f in t["from"]) and not t.get("reopen"):
                rep.error(f"{mid}: transition {t['from']} -> {t['to']} leaves a terminal state without reopen")
        for s in states - set(m["terminal"]):
            if not any(s in t["from"] for t in m["transitions"]) and m["terminal"]:
                rep.error(f"{mid}: non-terminal state {s} has no outgoing transition")


# ---------------------------------------------------------------------------- SQL

def check_sql(rep: Report) -> None:
    node = DOCS / "data" / "node-store.sql"
    cloud = DOCS / "data" / "cloud-store.sql"
    for path, prelude in ((node, ""), (cloud, "CREATE TABLE identity_user(user_id TEXT PRIMARY KEY) STRICT;"
                                              "CREATE TABLE device_device(device_id TEXT PRIMARY KEY) STRICT;"
                                              "CREATE TABLE device_installation(installation_id TEXT PRIMARY KEY) STRICT;")):
        con = sqlite3.connect(":memory:")
        try:
            con.execute("PRAGMA foreign_keys = ON")
            if prelude:
                con.executescript(prelude)
            con.executescript(read(path))
            if con.execute("PRAGMA foreign_key_check").fetchall():
                rep.error(f"{path.name}: foreign_key_check failed")
            if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                rep.error(f"{path.name}: integrity_check failed")
            n = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
            rep.note(f"{path.name}: {n} tables loaded")
        except sqlite3.Error as e:
            rep.error(f"{path.name}: {e}")
        finally:
            con.close()
    # every table documented in node-store.md
    md = read(DOCS / "data" / "node-store.md")
    con = sqlite3.connect(":memory:")
    con.executescript(read(node))
    for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        if f"`{name}`" not in md:
            rep.error(f"node-store.md does not document table {name}")
    con.close()


# ------------------------------------------------------------------------- markdown

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def check_links(rep: Report) -> None:
    for md in sorted(list(DOCS.rglob("*.md")) + [ROOT / "README.md", ROOT / "AGENTS.md"]):
        if not md.exists():
            continue
        text = read(md)
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            resolved = (md.parent / path).resolve()
            if not resolved.exists():
                rep.error(f"{md.relative_to(ROOT).as_posix()}: broken link {target}")


def requirement_ids() -> set[str]:
    return set(re.findall(r"^\|\s*(R-[A-Z]+-\d{3})\s*\|", read(REQUIREMENTS_MD), re.M))


def check_references(rep: Report) -> None:
    reqs = requirement_ids()
    if not reqs:
        rep.error("no requirements found")
    for md in DOCS.rglob("*.md"):
        text = read(md)
        for rid in set(re.findall(r"\bR-[A-Z]+-\d+\b", text)):
            if rid not in reqs:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown requirement {rid}")
    ver_ids = set(re.findall(r"^\|\s*([VLAF]-[A-Z]?\d{2}|[VAF]-[A-Z]\d{2})\s*\|", read(VERIFICATION_MD), re.M))
    for md in DOCS.rglob("*.md"):
        text = read(md)
        for vid in set(re.findall(r"\b([VAF]-[WLNACT]\d{2}|L-\d{2})\b", text)):
            if vid not in ver_ids:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown verification ID {vid}")
    sm_ids = {m["id"] for m in json.loads(read(MACHINES_JSON))["machines"]}
    for md in DOCS.rglob("*.md"):
        for sid in set(re.findall(r"\bSM-[A-Z-]*[A-Z]\b", read(md))):
            if sid not in sm_ids:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown state machine {sid}")
    adrs = {p.name[:7] for p in (DOCS / "decisions").glob("AD-*.md")}
    for p in (DOCS / "decisions").glob("AD-*.md"):
        if "- Status:" not in read(p):
            rep.error(f"{p.name}: missing Status line")
    for md in DOCS.rglob("*.md"):
        for aid in set(re.findall(r"\bAD-\d{4}\b", read(md))):
            if aid not in adrs:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown decision {aid}")


def task_ids_in_design() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for md in list(DOCS.rglob("*.md")) + list(DOCS.rglob("*.json")):
        for tid in re.findall(r"\bAF-[A-Z]+-\d{2}\b", read(md)):
            found.setdefault(tid, set()).add(md.relative_to(ROOT).as_posix())
    return found


def check_traceability(rep: Report, plan: Path | None) -> None:
    if not TRACE_JSON.exists():
        rep.error("docs/traceability/model.json missing")
        return
    model = json.loads(read(TRACE_JSON))
    reqs = requirement_ids()
    covered = set()
    for entry in model.get("requirements", []):
        rid = entry["id"]
        if rid not in reqs:
            rep.error(f"traceability: unknown requirement {rid}")
        covered.add(rid)
        if not entry.get("design"):
            rep.error(f"traceability: {rid} has no design reference")
        if not entry.get("tasks"):
            rep.error(f"traceability: {rid} has no delivery task")
        for ref in entry.get("design", []):
            if not (ROOT / ref.split("#")[0]).exists():
                rep.error(f"traceability: {rid} references missing {ref}")
    for rid in sorted(reqs - covered):
        rep.error(f"traceability: requirement {rid} not traced")
    if plan:
        check_plan_consistency(rep, model, json.loads(read(plan)))


def check_plan_consistency(rep: Report, model: dict, graph: dict) -> None:
    """The traceability model and the Plan delivery graph must name the same tasks per requirement."""
    tasks = {t["id"] for t in graph["tasks"]}
    for tid, where in sorted(task_ids_in_design().items()):
        if tid not in tasks:
            rep.error(f"task {tid} referenced in {sorted(where)} is not in the delivery graph")
    by_req: dict[str, set[str]] = {}
    for t in graph["tasks"]:
        for r in t.get("requirements", []):
            by_req.setdefault(r, set()).add(t["id"])
    for entry in model.get("requirements", []):
        have = set(entry.get("tasks", []))
        for tid in sorted(have - tasks):
            rep.error(f"traceability: {entry['id']} names unknown task {tid}")
        want = by_req.get(entry["id"], set())
        if have != want:
            rep.error(f"traceability: {entry['id']} lists tasks {sorted(have)} but the delivery graph has {sorted(want)}")


# ----------------------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="regenerate generated documents")
    ap.add_argument("--plan", type=Path, help="path to the Plan delivery-graph.json")
    ap.add_argument("--require-protoc", action="store_true")
    ap.add_argument("--compile", action="store_true", help="generate and build C# from the protos")
    args = ap.parse_args(argv)
    rep = Report()
    model, files = load_protos()
    machines = json.loads(read(MACHINES_JSON))
    generated = {CATALOGUE_MD: render_catalogue(model), MACHINES_MD: render_machines(machines)}
    for path, content in generated.items():
        if args.write:
            path.write_text(content, encoding="utf-8", newline="\n")
        elif not path.exists() or read(path) != content:
            rep.error(f"{path.relative_to(ROOT).as_posix()} is out of date (run --write)")
    check_protos(rep, model, files)
    run_protoc(rep, files, args.require_protoc)
    if args.compile:
        compile_csharp(rep, files)
    check_machines(rep, model, machines)
    check_sql(rep)
    check_links(rep)
    check_references(rep)
    check_traceability(rep, args.plan)
    for n in rep.notes:
        print(f"note: {n}")
    for e in rep.errors:
        print(f"ERROR: {e}")
    print(f"{len(rep.errors)} error(s), {len(rep.notes)} note(s); {len(model.rpcs)} methods, {len(machines['machines'])} state machines")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
