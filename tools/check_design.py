#!/usr/bin/env python3
"""Design repository checks for the ArcForges V2 Sandbox design.

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
HISTORY_DIR = ROOT / "history" / "v1-20261114"
HISTORY_SOURCE_COMMIT = "62172622550fff73a553135ca178f9b7117c9cbd"
HISTORY_MANIFEST_SHA256 = "69fe138cb803bb368ca0b09a4669604842f145b20cfa8f6fc8579765e436c79d"
TASK_ID_RE = re.compile(r"\bAFV2-[A-Z]+-\d{2}\b")
OBSOLETE_TASK_ID_RE = re.compile(r"\bAF-[A-Z]+-\d{2}\b")
VERIFICATION_ID = r"[VLAF]-(?:[A-Z][A-Z0-9]*-)?[A-Z]?\d{2}"

ANN_REQUIRED = ["auth", "idempotency", "deadline", "stream", "errors", "locality"]
ANN_KEYS = ANN_REQUIRED + ["state"]
IMPLICIT_ERRORS = {"INTERNAL/internal", "RESOURCE/overloaded", "STATE/node_stopping",
                   "AUTHENTICATION/unauthenticated", "RESOURCE/rate_limited", "STATE/not_activated"}
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


def active_documents(suffixes: tuple[str, ...] = (".md", ".json", ".proto", ".sql")) -> list[Path]:
    """The frozen archive and pinned Contracts reference are not executable V2 authority."""
    return sorted(p for p in DOCS.rglob("*")
                  if p.is_file() and p.suffix in suffixes and not p.is_relative_to(REF_DIR))


def check_history(rep: Report) -> None:
    """Verify the frozen manifest itself and every byte it identifies, without rewriting history."""
    manifest = HISTORY_DIR / "snapshot.json"
    if not manifest.is_file() or manifest.is_symlink():
        rep.error("V1 archive: snapshot.json is missing or is a symlink")
        return
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != HISTORY_MANIFEST_SHA256:
        rep.error("V1 archive: snapshot.json SHA-256 changed; the archive cannot be rebaselined")
    try:
        data = json.loads(read(manifest))
    except (ValueError, OSError) as exc:
        rep.error(f"V1 archive: unreadable snapshot.json: {exc}")
        return
    if (data.get("source_repository") != "ArcForges/ArcForges-Design"
            or data.get("source_commit") != HISTORY_SOURCE_COMMIT):
        rep.error("V1 archive: source repository/commit differs from the frozen baseline")
    entries = data.get("files")
    if not isinstance(entries, list) or not entries:
        rep.error("V1 archive: files must be a nonempty manifest")
        return
    listed: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            rep.error("V1 archive: invalid file entry")
            continue
        name, digest = entry.get("path"), entry.get("sha256")
        if (not isinstance(name, str) or not name or "\\" in name or ":" in name or name.startswith("/")
                or any(part in {"", ".", ".."} for part in name.split("/"))
                or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            rep.error(f"V1 archive: unsafe path or invalid digest: {name!r}")
            continue
        if name in listed:
            rep.error(f"V1 archive: duplicate path {name}")
        listed.add(name)
        path = HISTORY_DIR / name
        components = name.split("/")
        if (not path.is_file() or any(HISTORY_DIR.joinpath(*components[:n]).is_symlink()
                                    for n in range(1, len(components) + 1))):
            rep.error(f"V1 archive: missing or symlinked file {name}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            rep.error(f"V1 archive: SHA-256 mismatch for {name}")
    actual = {p.relative_to(HISTORY_DIR).as_posix() for p in HISTORY_DIR.rglob("*") if p.is_file()}
    extras = actual - listed - {"snapshot.json"}
    if extras:
        rep.error(f"V1 archive: unmanifested files {sorted(extras)}")
    rep.note(f"V1 archive: checked {len(listed)} frozen file identities")


def check_obsolete_task_references(rep: Report) -> None:
    for path in active_documents():
        if path.is_relative_to(DOCS / "research"):
            continue  # Historical source/ledger citations are evidence, not active task assignments.
        for task in sorted(set(OBSOLETE_TASK_ID_RE.findall(read(path)))):
            rep.error(f"{path.relative_to(ROOT).as_posix()}: obsolete executable task ID {task}; "
                      "move historical evidence to research and use an AFV2 task for current work")


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


CATALOGUE_HEADER = "| Category / code | Meaning | Retry advice | Effect | Details |"


def check_error_pairs(rep: Report) -> None:
    """A catalogue row whose effect can be UNKNOWN advises AFTER_TIME only in a clause that names a known effect.

    The Contracts rule `arcError` rejects an ArcError with effect UNKNOWN and retry AFTER_TIME (errors.md, "UNKNOWN never pairs
    with AFTER_TIME"). Every row of the catalogue table is read (a row that cannot be read is an error, never skipped); the retry
    cell is read clause by clause (split at ';'): a clause that names AFTER_TIME must name DID_NOT_HAPPEN or HAPPENED and must not
    name UNKNOWN. Names are matched as words, with or without backticks; AFTER_TIME and UNKNOWN in any case (AFTER_TIME also with a
    space), the known effects only as the enum names.
    """
    lines = read(ERRORS_MD).split("\n")
    if lines.count(CATALOGUE_HEADER) != 1:
        rep.error("errors.md: the error catalogue table header is missing or repeated")
        return
    start = lines.index(CATALOGUE_HEADER) + 2
    checked = set()
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        m = re.match(r"^\|\s*`([A-Z]+/[a-z_]+)`", line)
        if not m:
            rep.error(f"errors.md: a catalogue row does not start with a `CATEGORY/code` cell: {line[:60]!r}")
            continue
        checked.add(m.group(1))
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            rep.error(f"errors.md: {m.group(1)} has {len(cells)} cells, expected 5")
            continue
        retry, effect = cells[2], cells[3]
        if not re.search(r"\bUNKNOWN\b", effect, re.I):
            continue
        for clause in retry.split(";"):
            known = re.search(r"\b(DID_NOT_HAPPEN|HAPPENED)\b", clause)
            if re.search(r"\bAFTER[ _]TIME\b", clause, re.I) and (re.search(r"\bUNKNOWN\b", clause, re.I) or not known):
                rep.error(f"errors.md: {m.group(1)} advises AFTER_TIME in a clause that does not name a known effect, "
                          "while its effect can be UNKNOWN (Contracts rule arcError)")
    missed = error_catalogue() - checked
    if missed:
        rep.error(f"errors.md: catalogue codes outside the catalogue table were not checked: {sorted(missed)}")


def check_protos(rep: Report, model: ProtoModel, files: list[Path]) -> None:
    sha = hashlib.sha256(read(FOUNDATION).encode("utf-8")).hexdigest()
    if sha != FOUNDATION_SHA256:
        rep.error(f"pinned foundation.proto changed (sha256 {sha})")
    codes = error_catalogue()
    used: set[str] = set()
    for key, msg in model.messages.items():
        if msg.file == "foundation":
            continue
        field_names: set[str] = set()
        for f in msg.fields:
            if f.name in field_names:
                rep.error(f"{msg.file}: {msg.name} has duplicate field name {f.name}")
            field_names.add(f.name)
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


def check_v2_namespaces(rep: Report, files: list[Path]) -> None:
    """V1 specifications stay frozen; only the immutable foundation is shared by V2."""
    if not files:
        rep.error("no active V2 protobuf specifications found")
    for path in files:
        text = read(path)
        package = re.search(r"^package\s+([\w.]+);", text, re.M)
        if not package or not re.fullmatch(r"arcforges\.[a-z][a-z0-9_]*\.v2", package.group(1)):
            rep.error(f"{path.name}: active contract package must be an arcforges V2 namespace")
        elif path.parent.relative_to(PROTO_DIR).as_posix() != package.group(1).replace(".", "/"):
            rep.error(f"{path.name}: proto path does not match its V2 package")
        for imported in re.findall(r'^import\s+"([^"]+)";', text, re.M):
            if imported.startswith("arcforges/") and "/v1/" in imported and imported != "arcforges/foundation/v1/foundation.proto":
                rep.error(f"{path.name}: active contract imports obsolete V1 surface {imported}")


def find_protoc() -> tuple[str | None, str | None]:
    toolchain = ROOT / "tools" / "proto-toolchain"
    lock = json.loads(read(toolchain / "packages.lock.json"))
    versions = {packages["Grpc.Tools"]["resolved"] for packages in lock["dependencies"].values()
                if "Grpc.Tools" in packages}
    if len(versions) != 1:
        raise ValueError("proto lockfile must resolve exactly one Grpc.Tools version")
    version = versions.pop()
    assets = toolchain / "obj" / "project.assets.json"
    roots = list(json.loads(read(assets)).get("packageFolders", {})) if assets.is_file() else []
    if not roots:
        roots = [os.environ.get("NUGET_PACKAGES", str(Path.home() / ".nuget" / "packages"))]
    sub = "windows_x64" if os.name == "nt" else "linux_x64"
    for root in roots:
        package = Path(root) / "grpc.tools" / version
        exe = package / "tools" / sub / ("protoc.exe" if os.name == "nt" else "protoc")
        inc = package / "build" / "native" / "include"
        if not exe.is_file() or not inc.is_dir():
            continue
        for variable, expected in (("ARCFORGES_PROTOC", exe), ("ARCFORGES_PROTOC_INCLUDE", inc)):
            override = os.environ.get(variable)
            if override and Path(override).resolve() != expected.resolve():
                raise ValueError(f"{variable} conflicts with locked Grpc.Tools {version}; remove the override")
        if os.name != "nt" and not os.access(exe, os.X_OK):
            exe.chmod(0o755)  # NuGet extraction drops the execute bit
        # PATH and other cached versions never select the generator; the plugin is its locked sibling.
        return str(exe), str(inc)
    if os.environ.get("ARCFORGES_PROTOC") or os.environ.get("ARCFORGES_PROTOC_INCLUDE"):
        raise ValueError(f"locked Grpc.Tools {version} is missing; overrides cannot replace it")
    return None, None


def run_protoc(rep: Report, files: list[Path], require: bool, out_dir: Path | None = None) -> bool:
    try:
        exe, inc = find_protoc()
    except ValueError as error:
        rep.error(str(error))
        return False
    if not exe:
        (rep.error if require else rep.note)("locked protoc not found; restore tools/proto-toolchain/ProtoToolchain.csproj --locked-mode")
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
    rep.note(f"locked protoc compiled {len(files)} files ({exe})")
    return True


def compile_csharp(rep: Report, files: list[Path]) -> None:
    try:
        exe, inc = find_protoc()
    except ValueError as error:
        rep.error(str(error))
        return
    plugin = None
    if exe:
        cand = Path(exe).with_name("grpc_csharp_plugin.exe" if os.name == "nt" else "grpc_csharp_plugin")
        plugin = str(cand) if cand.exists() else None
        if plugin and os.name != "nt" and not os.access(cand, os.X_OK):
            cand.chmod(0o755)  # Same locked NuGet payload as protoc.
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
        proj.write_text("""<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net11.0</TargetFramework>
<Nullable>disable</Nullable><ImplicitUsings>disable</ImplicitUsings><IsAotCompatible>true</IsAotCompatible>
<TreatWarningsAsErrors>true</TreatWarningsAsErrors><NoWarn>CS1591</NoWarn></PropertyGroup>
<ItemGroup><PackageReference Include="Google.Protobuf" Version="3.36.2" /><PackageReference Include="Grpc.Core.Api" Version="2.85.0" /></ItemGroup></Project>""", encoding="utf-8")
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
           "States equal the named proto enum values (without the enum prefix), or an explicitly sourced non-wire stored state map; pseudo-states are marked.", ""]
    out.append("| ID | Machine | State authority | Persisted | Owner |")
    out.append("|---|---|---|---|---|")
    for m in data["machines"]:
        authority = f"`{m['enum']}`" if "enum" in m else "non-wire stored states"
        out.append(f"| [{m['id']}](#{m['id'].lower()}) | {m['title']} | {authority} | {m['persisted']} | {m['owner']} |")
    for m in data["machines"]:
        out += ["", f'<a id="{m["id"].lower()}"></a>', "", f"## {m['id']} — {m['title']}", ""]
        if "enum" in m:
            out.append(f"- Enum: `{m['enum']}`; persisted: {m['persisted']}; owner: {m['owner']}.")
            if "storage" in m:
                storage = m["storage"]
                out.append(f"- SQLite storage: `{storage['table']}.{storage['column']}`; encoding: `{storage['encoding']}`; checked against the enum and closed SQL state set.")
        else:
            source = m.get("state_source")
            source_text = (f"`{source.get('repository', '?')}@{source.get('commit', '?')}`: "
                           + ", ".join(f"`{path}`" for path in source.get("paths", []))) if isinstance(source, dict) and isinstance(source.get("paths", []), list) else "invalid source"
            values = m.get("state_values")
            values_text = ", ".join(f"`{name}={value}`" for name, value in values.items()) if isinstance(values, dict) else "invalid values"
            out.append(f"- Non-wire stored states: {values_text}; source: {source_text}; persisted: {m['persisted']}; owner: {m['owner']}.")
        out.append(f"- Initial: {', '.join('`' + s + '`' for s in m['initial'])}. Terminal: {', '.join('`' + s + '`' for s in m['terminal']) or 'none (long-lived)'}.")
        for state, guard in m.get("initial_guards", {}).items():
            out.append(f"- Initial guard for `{state}`: {guard}.")
        if m.get("pseudo_states"):
            out.append(f"- Pseudo-states (not in the enum): {', '.join(m['pseudo_states'])}.")
        if m.get("response_only"):
            out.append(f"- Response-only enum values (never stored): {', '.join(m['response_only'])}.")
        out += ["", "```mermaid", "stateDiagram-v2"]
        for s in m["initial"]:
            out.append(f"  [*] --> {s}")
        for t in m["transitions"]:
            label = t["on"].split(";")[0].replace(":", " ")[:60].rstrip()
            for f in t["from"]:
                out.append(f"  {f} --> {t['to']} : {label}")
        for s in m["terminal"]:
            out.append(f"  {s} --> [*]")
        out += ["```", "", "| From | To | Trigger | Guard | Effect |", "|---|---|---|---|---|"]
        for t in m["transitions"]:
            cells = [", ".join(t["from"]), t["to"] + (" (reopen)" if t.get("reopen") else ""), t["on"], t.get("guard", ""), t.get("effect", "")]
            out.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    return "\n".join(out) + "\n"


def valid_state_source(source: object) -> bool:
    """A non-wire state map names immutable repository source, not an invented protobuf enum.

    This validates the reference's shape; independent review must still compare the map with the named source bytes.
    """
    if not isinstance(source, dict) or set(source) != {"repository", "commit", "paths"}:
        return False
    repository, commit, paths = source["repository"], source["commit"], source["paths"]
    if (not isinstance(repository, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
            or any(part in {".", ".."} for part in repository.split("/"))):
        return False
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit) or commit == "0" * 40:
        return False
    if not isinstance(paths, list) or not paths or any(not isinstance(path, str) for path in paths):
        return False
    if len(set(paths)) != len(paths):
        return False
    return all(path and all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) and part not in {".", ".."}
                            for part in path.split("/")) for path in paths)


def check_machines(rep: Report, model: ProtoModel, data: dict) -> None:
    ids = set()
    for m in data["machines"]:
        mid = m["id"]
        if mid in ids:
            rep.error(f"duplicate machine {mid}")
        ids.add(mid)
        has_enum, has_values = "enum" in m, "state_values" in m
        if has_enum == has_values:
            rep.error(f"{mid}: choose exactly one of enum or state_values")
            continue
        if has_enum:
            if "state_source" in m:
                rep.error(f"{mid}: enum-backed machines cannot name a stored-state source")
            enum_name = m["enum"]
            enum = model.enums.get(enum_name) if isinstance(enum_name, str) else None
            if enum is None:
                rep.error(f"{mid}: enum {enum_name} not found in protos")
                continue
            prefix = re.sub(r"(?<!^)([A-Z])", r"_\1", enum_name.split(".")[-1]).upper() + "_"
            enum_states = {v[len(prefix):] for v in enum if v.startswith(prefix) and not v.endswith("_UNSPECIFIED")}
            if "storage" in m:
                check_machine_storage(rep, m, enum_states)
            pseudo = set(m.get("pseudo_states", []))
            response_only = set(m.get("response_only", []))
            expected = enum_states - response_only
            authority = enum_name
            missing_label = "enum states"
        else:
            values = m["state_values"]
            if not isinstance(values, dict) or not values or any(
                not isinstance(name, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", name)
                or type(value) is not int or not 1 <= value <= 32767 for name, value in values.items()
            ):
                rep.error(f"{mid}: state_values must map uppercase names to positive smallint values")
                continue
            if len(set(values.values())) != len(values):
                rep.error(f"{mid}: stored state values must be unique")
            source = m.get("state_source")
            if not valid_state_source(source):
                rep.error(f"{mid}: stored states require a repository, full commit and safe source paths")
            if "pseudo_states" in m or "response_only" in m:
                rep.error(f"{mid}: stored states cannot use enum-only pseudo_states or response_only")
            expected = set(values)
            pseudo = set()
            authority = "declared stored states"
            missing_label = "declared states"
        states = set()
        for t in m["transitions"]:
            states.update(t["from"])
            states.add(t["to"])
        states |= set(m["initial"]) | set(m["terminal"])
        missing = expected - states
        extra = states - expected - pseudo
        if missing:
            rep.error(f"{mid}: {missing_label} never used: {sorted(missing)}")
        if extra:
            rep.error(f"{mid}: states not in {authority}: {sorted(extra)}")
        initial_guards = m.get("initial_guards", {})
        if "initial_guards" in m and set(initial_guards) != set(m["initial"]):
            rep.error(f"{mid}: initial_guards must cover exactly the initial states")
        if any(not isinstance(guard, str) or not guard.strip() for guard in initial_guards.values()):
            rep.error(f"{mid}: initial guard must be nonempty text")
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

def check_machine_storage(rep: Report, machine: dict, states: set[str]) -> None:
    """Check an explicitly mapped enum against the SQLite column's closed state set."""
    mid = machine["id"]
    storage = machine.get("storage")
    if machine.get("persisted") is not True:
        rep.error(f"{mid}: a stored state machine must declare persisted=true")
    if not isinstance(storage, dict) or storage.get("encoding") != "lowercase_enum":
        rep.error(f"{mid}: unsupported state storage encoding")
        return
    table, column = storage.get("table"), storage.get("column")
    if any(not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", value)
           for value in (table, column)):
        rep.error(f"{mid}: state storage requires safe table and column names")
        return
    sql = sql_without_comments(read(DOCS / "data" / "node-store.sql"))
    match = re.search(r"\bCREATE\s+TABLE\s+" + re.escape(table) + r"\s*\((.*?)\)\s*STRICT\s*;", sql, re.I | re.S)
    if not match:
        rep.error(f"{mid}: stored state table {table} not found")
        return
    definitions = split_sql_top_level(match.group(1))
    definition = next((item for item in definitions
                       if re.match(re.escape(column) + r"\s", item, re.I)), "")
    check = re.search(r"\bCHECK\s*\(\s*" + re.escape(column) + r"\s+IN\s*\(([^)]*)\)\s*\)", definition, re.I)
    if not check:
        rep.error(f"{mid}: stored state column {table}.{column} needs a closed IN check")
        return
    literals = split_sql_top_level(check.group(1))
    if any(not re.fullmatch(r"'[a-z][a-z0-9_]*'", value) for value in literals):
        rep.error(f"{mid}: stored state check must contain simple lowercase state literals")
        return
    actual = {value[1:-1] for value in literals}
    expected = {state.lower() for state in states}
    if actual != expected or len(literals) != len(actual):
        rep.error(f"{mid}: stored states disagree with enum: expected {sorted(expected)}, got {sorted(actual)}")

PG_TYPES = {"uuid", "text", "smallint", "integer", "bigint", "bytea", "timestamptz", "boolean", "numeric"}
# Retained Cloud schema at 6df33c525fcbc20495e46c9c4c011086146da796.
# This map is not a substitute for executing the retained migration chain.
PG_RETAINED_COLUMNS = {
    "identity.user": {"user_id": "uuid"},
    "fleet.node": {"enrollment_id": "uuid", "node_id": "uuid", "user_id": "uuid"},
}
PG_RETAINED_SCHEMAS = {"identity", "fleet", "device", "entitlement", "audit", "platform"}


def sql_without_comments(text: str) -> str:
    return re.sub(r"'(?:''|[^'])*'|--[^\n]*|/\*.*?\*/",
                  lambda m: m.group(0) if m.group(0).startswith("'") else "", text, flags=re.S)


def split_sql_top_level(text: str, separator: str = ",") -> list[str]:
    """Split documented DDL while respecting strings and nested CHECK expressions."""
    out, start, depth, quoted, i = [], 0, 0, False, 0
    while i < len(text):
        c = text[i]
        if c == "'":
            if quoted and i + 1 < len(text) and text[i + 1] == "'":
                i += 2
                continue
            quoted = not quoted
        elif not quoted:
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth < 0:
                    raise ValueError("unbalanced closing parenthesis")
            elif c == separator and depth == 0:
                out.append(text[start:i].strip())
                start = i + 1
        i += 1
    if quoted or depth:
        raise ValueError("unterminated SQL string or parentheses")
    if text[start:].strip():
        out.append(text[start:].strip())
    return out


def check_postgres_structure(rep: Report, path: Path, documentation: Path) -> None:
    """Check PostgreSQL DDL structure only; never execute it in SQLite or claim runtime proof."""
    sql, doc = sql_without_comments(read(path)), read(documentation)
    if re.search(r"\b(PRAGMA|AUTOINCREMENT|STRICT)\b", sql, re.I):
        rep.error(f"{path.name}: SQLite syntax is invalid in the PostgreSQL specification")
    try:
        statements = split_sql_top_level(sql, ";")
    except ValueError as exc:
        rep.error(f"{path.name}: {exc}")
        return
    if sql.rstrip() and not sql.rstrip().endswith(";"):
        rep.error(f"{path.name}: final DDL statement lacks a semicolon")
    schemas: set[str] = set()
    tables: dict[str, dict[str, str]] = {}
    definitions: dict[str, list[str]] = {}
    indexes: list[tuple[str, str]] = []
    alterations: list[tuple[str, str]] = []
    ident = r"[a-z_][a-z0-9_]*"
    qualified = rf"{ident}\.{ident}"
    for statement in statements:
        schema = re.fullmatch(rf"CREATE\s+SCHEMA\s+({ident})", statement, re.I)
        table = re.fullmatch(rf"CREATE\s+TABLE\s+({qualified})\s*\((.*)\)", statement, re.I | re.S)
        index = re.fullmatch(rf"CREATE\s+(?:UNIQUE\s+)?INDEX\s+{ident}\s+ON\s+({qualified})\s*\(([^)]+)\)(?:\s+WHERE\s+.+)?", statement, re.I | re.S)
        alteration = re.fullmatch(rf"ALTER\s+TABLE\s+({qualified})\s+ADD\s+CONSTRAINT\s+{ident}\s+UNIQUE\s*\(([^)]+)\)", statement, re.I | re.S)
        if schema:
            name = schema.group(1).lower()
            if name in schemas:
                rep.error(f"{path.name}: duplicate schema {name}")
            schemas.add(name)
        elif table:
            name, body = table.group(1).lower(), table.group(2)
            if name in tables:
                rep.error(f"{path.name}: duplicate table {name}")
            columns: dict[str, str] = {}
            definitions[name] = split_sql_top_level(body)
            for definition in definitions[name]:
                if re.match(r"^(?:PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CHECK|CONSTRAINT)\b", definition, re.I):
                    continue
                column = re.match(rf"^({ident})\s+({ident})\b", definition, re.I)
                if not column:
                    rep.error(f"{path.name}: unreadable column in {name}: {definition[:70]}")
                    continue
                column_name, column_type = (part.lower() for part in column.groups())
                if column_name in columns:
                    rep.error(f"{path.name}: duplicate column {name}.{column_name}")
                columns[column_name] = column_type
                if column_type not in PG_TYPES:
                    rep.error(f"{path.name}: unsupported declared PostgreSQL type {column_type} for {name}.{column_name}")
                if column_type == "numeric" and not re.match(rf"^{ident}\s+numeric\s*\(\s*\d+\s*,\s*\d+\s*\)", definition, re.I):
                    rep.error(f"{path.name}: numeric type must declare precision/scale for {name}.{column_name}")
            if not columns:
                rep.error(f"{path.name}: table {name} has no parsed columns")
            tables[name] = columns
        elif index:
            indexes.append((index.group(1).lower(), index.group(2)))
        elif alteration:
            alterations.append((alteration.group(1).lower(), alteration.group(2)))
        else:
            rep.error(f"{path.name}: DDL statement outside the structurally checked subset: {statement[:90]}")
    if not tables:
        rep.error(f"{path.name}: no schema-qualified PostgreSQL tables found")
    known_columns = {**PG_RETAINED_COLUMNS, **tables}
    for name, columns in tables.items():
        if name.split(".")[0] not in schemas | PG_RETAINED_SCHEMAS:
            rep.error(f"{path.name}: {name} has no declared schema")
        if name in PG_RETAINED_COLUMNS:
            rep.error(f"{path.name}: cannot recreate retained table {name}")
        if f"`{name}`" not in doc:
            rep.error(f"{documentation.name} does not document table {name}")
        for definition in definitions[name]:
            ref = re.search(rf"\bREFERENCES\s+({qualified})\s*\(([^)]+)\)", definition, re.I)
            if not ref:
                if re.search(r"\bREFERENCES\b", definition, re.I):
                    rep.error(f"{path.name}: foreign key in {name} requires a qualified table and explicit columns")
                continue
            target = ref.group(1).lower()
            target_names = [c.strip().lower() for c in ref.group(2).split(",")]
            fk = re.search(r"FOREIGN\s+KEY\s*\(([^)]+)\)", definition, re.I)
            source_names = ([c.strip().lower() for c in fk.group(1).split(",")] if fk else [definition.split()[0].lower()])
            if target not in known_columns:
                rep.error(f"{path.name}: {name} references unknown table {target}")
                continue
            if len(source_names) != len(target_names):
                rep.error(f"{path.name}: foreign-key arity differs for {name} -> {target}")
            for source_column, target_column in zip(source_names, target_names):
                if source_column not in columns or target_column not in known_columns[target]:
                    rep.error(f"{path.name}: unknown foreign-key column {name}.{source_column} -> {target}.{target_column}")
                elif columns[source_column] != known_columns[target][target_column]:
                    rep.error(f"{path.name}: foreign-key type mismatch {name}.{source_column} -> {target}.{target_column}")
    for name, index_columns in indexes:
        if name not in tables:
            rep.error(f"{path.name}: index targets unknown table {name}")
            continue
        for column in [c.strip().lower() for c in index_columns.split(",")]:
            if column not in tables[name]:
                rep.error(f"{path.name}: index references unknown column {name}.{column}")
    for name, altered_columns in alterations:
        if name not in PG_RETAINED_COLUMNS:
            rep.error(f"{path.name}: ALTER targets an undeclared retained table {name}")
        elif any(c.strip().lower() not in PG_RETAINED_COLUMNS[name] for c in altered_columns.split(",")):
            rep.error(f"{path.name}: ALTER references unknown retained column in {name}")
    for requirement in ("postgresql", "migration", "checksum", "backup", "restore", "least-privilege", "afv2-center-01"):
        if requirement not in doc.lower():
            rep.error(f"{documentation.name}: missing migration protocol topic {requirement}")
    rep.note(f"{path.name}: structural PostgreSQL check of {len(tables)} tables only; "
             "NOT PostgreSQL execution/migration proof (AFV2-CENTER-01)")


def check_sql(rep: Report) -> None:
    node = DOCS / "data" / "node-store.sql"
    cloud = DOCS / "data" / "cloud-store.sql"
    con = sqlite3.connect(":memory:")
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(read(node))
        if con.execute("PRAGMA foreign_key_check").fetchall():
            rep.error(f"{node.name}: foreign_key_check failed")
        if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            rep.error(f"{node.name}: integrity_check failed")
        tables = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        md = read(DOCS / "data" / "node-store.md")
        for (name,) in tables:
            if f"`{name}`" not in md:
                rep.error(f"node-store.md does not document table {name}")
        rep.note(f"{node.name}: {len(tables)} SQLite tables loaded; integrity and foreign keys checked")
    except sqlite3.Error as exc:
        rep.error(f"{node.name}: {exc}")
    finally:
        con.close()
    check_postgres_structure(rep, cloud, DOCS / "data" / "cloud-store.md")


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
    for md in active_documents((".md",)):
        text = read(md)
        for rid in set(re.findall(r"\bR-[A-Z]+-\d+\b", text)):
            if rid not in reqs:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown requirement {rid}")
    ver_ids = set(re.findall(rf"^\|\s*({VERIFICATION_ID})\s*\|", read(VERIFICATION_MD), re.M))
    if not ver_ids:
        rep.error("no platform verification IDs found")
    for md in active_documents((".md",)):
        text = read(md)
        for vid in set(re.findall(rf"\b({VERIFICATION_ID})\b", text)):
            if vid not in ver_ids:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown verification ID {vid}")
    sm_ids = {m["id"] for m in json.loads(read(MACHINES_JSON))["machines"]}
    for md in active_documents((".md",)):
        for sid in set(re.findall(r"\bSM-[A-Z-]*[A-Z]\b", read(md))):
            if sid not in sm_ids:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown state machine {sid}")
    adrs = {p.name[:7] for p in (DOCS / "decisions").glob("AD-*.md")}
    for p in (DOCS / "decisions").glob("AD-*.md"):
        if "- Status:" not in read(p):
            rep.error(f"{p.name}: missing Status line")
    for md in active_documents((".md",)):
        for aid in set(re.findall(r"\bAD-\d{4}\b", read(md))):
            if aid not in adrs:
                rep.error(f"{md.relative_to(ROOT).as_posix()}: unknown decision {aid}")


def task_ids_in_design() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for md in active_documents():
        for tid in TASK_ID_RE.findall(read(md)):
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
        if rid in covered:
            rep.error(f"traceability: duplicate requirement {rid}")
        covered.add(rid)
        if not entry.get("design"):
            rep.error(f"traceability: {rid} has no design reference")
        if not entry.get("tasks"):
            rep.error(f"traceability: {rid} has no delivery task")
        for task in entry.get("tasks", []):
            if not isinstance(task, str) or not TASK_ID_RE.fullmatch(task):
                rep.error(f"traceability: {rid} has obsolete or malformed task ID {task!r}")
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
    for task in sorted(tasks):
        if not TASK_ID_RE.fullmatch(task):
            rep.error(f"delivery graph contains obsolete or malformed active task ID {task}")
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
    check_history(rep)
    check_obsolete_task_references(rep)
    model, files = load_protos()
    machines = json.loads(read(MACHINES_JSON))
    generated = {CATALOGUE_MD: render_catalogue(model), MACHINES_MD: render_machines(machines)}
    for path, content in generated.items():
        if args.write:
            path.write_text(content, encoding="utf-8", newline="\n")
        elif not path.exists() or read(path) != content:
            rep.error(f"{path.relative_to(ROOT).as_posix()} is out of date (run --write)")
    check_protos(rep, model, files)
    check_v2_namespaces(rep, files)
    check_error_pairs(rep)
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
