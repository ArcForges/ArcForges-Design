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
    # A global MSBuild override can silently load tasks from a different SDK despite global.json.
    override = os.environ.get("MSBuildSDKsPath")
    if override:
        sdks = subprocess.run([dotnet_on_path, "--list-sdks"], capture_output=True, text=True, check=False)
        expected_paths = [Path(line.split("[", 1)[1].rstrip("]")) / expected_sdk / "Sdks"
                          for line in sdks.stdout.splitlines() if line.startswith(expected_sdk + " [")]
        if sdks.returncode or not any(Path(override).resolve() == path.resolve() for path in expected_paths):
            errors.append("MSBuildSDKsPath does not belong to the selected pinned SDK; remove the conflicting override")
    print(json.dumps({"python": current_python, "python_executable": sys.executable,
                      "path_python": python_on_path, "dotnet_executable": dotnet_on_path,
                      "sdk": sdk.stdout.strip(), "expected_python": expected_python,
                      "expected_sdk": expected_sdk,
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
