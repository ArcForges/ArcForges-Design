"""Require identical pinned Python and .NET selection locally and in CI."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def check() -> list[str]:
    errors = []
    expected_python = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
    expected_sdk = json.loads((ROOT / "global.json").read_text(encoding="utf-8"))["sdk"]["version"]
    current_python = platform.python_version()
    if current_python != expected_python:
        errors.append(f"Python {current_python} at {sys.executable}; expected {expected_python}")
    python_on_path = shutil.which("python")
    dotnet_on_path = shutil.which("dotnet")
    if not python_on_path or not dotnet_on_path:
        return errors + ["python and dotnet must both be on PATH"]
    selected = subprocess.run([python_on_path, "--version"], capture_output=True, text=True, check=False)
    if selected.returncode or selected.stdout.strip() != f"Python {expected_python}":
        errors.append(f"PATH python at {python_on_path} does not select {expected_python}")
    sdk = subprocess.run([dotnet_on_path, "--version"], cwd=ROOT, capture_output=True, text=True, check=False)
    if sdk.returncode or sdk.stdout.strip() != expected_sdk:
        errors.append(f"dotnet at {dotnet_on_path} does not select pinned SDK {expected_sdk}")
    # global.json selects the CLI SDK; evaluated projects must use that same installed SDK.
    sdks = subprocess.run([dotnet_on_path, "--list-sdks"], capture_output=True, text=True, check=False)
    sdk_roots = [Path(line.split("[", 1)[1].rstrip("]")) / expected_sdk
                 for line in sdks.stdout.splitlines() if line.startswith(expected_sdk + " [")]
    if sdks.returncode or not sdk_roots:
        errors.append("The selected dotnet does not report an installed root for the pinned SDK")
    effective = subprocess.run(
        [dotnet_on_path, "msbuild", "tools/proto-toolchain/ProtoToolchain.csproj", "-nologo", "-verbosity:quiet",
         "-getProperty:NETCoreSdkVersion,MSBuildToolsPath,MSBuildSDKsPath"],
        cwd=ROOT, capture_output=True, text=True, check=False)
    properties = {}
    try:
        if effective.returncode:
            raise ValueError("project evaluation failed")
        properties = json.loads(effective.stdout)["Properties"]
        if properties["NETCoreSdkVersion"] != expected_sdk:
            errors.append("Effective NETCoreSdkVersion differs from the pinned SDK")
        if not properties["MSBuildToolsPath"] or not properties["MSBuildSDKsPath"] or not any(
                Path(properties["MSBuildToolsPath"]).resolve() == root.resolve()
                and Path(properties["MSBuildSDKsPath"]).resolve() == (root / "Sdks").resolve()
                for root in sdk_roots):
            errors.append("Effective MSBuild tools/SDK roots differ from the selected installed SDK")
    except (ValueError, KeyError, TypeError):
        errors.append("Cannot evaluate the effective MSBuild SDK/root identity")
    # An explicit override also has to agree, even when a project resets its evaluated value.
    override = os.environ.get("MSBuildSDKsPath")
    if override:
        if not any(Path(override).resolve() == (root / "Sdks").resolve() for root in sdk_roots):
            errors.append("MSBuildSDKsPath does not belong to the selected pinned SDK; remove the conflicting override")
    print(json.dumps({"python": current_python, "python_executable": sys.executable,
                      "path_python": python_on_path, "dotnet_executable": dotnet_on_path,
                      "sdk": sdk.stdout.strip(), "expected_python": expected_python,
                      "expected_sdk": expected_sdk,
                      "installed_sdk_roots": [str(root) for root in sdk_roots],
                      "effective_msbuild": properties,
                      "lock_sha256": hashlib.sha256((ROOT / "tools/proto-toolchain/packages.lock.json").read_bytes()).hexdigest()},
                     ensure_ascii=True))
    return errors


def main() -> int:
    errors = check()
    for error in errors:
        print("toolchain mismatch: " + error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
