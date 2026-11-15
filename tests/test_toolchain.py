"""Exercise version rejection with real installed tools and isolated selector inputs."""
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager, redirect_stdout
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eng"))
import check_toolchain as toolchain  # noqa: E402


class ToolchainSelection(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in (".python-version", "global.json", "tools/proto-toolchain/ProtoToolchain.csproj",
                             "tools/proto-toolchain/packages.lock.json"):
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, destination)
            with patch.object(toolchain, "ROOT", root):
                yield root

    def check(self):
        with redirect_stdout(io.StringIO()):
            return toolchain.check()

    def test_actual_tools_match_repository_pins(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(toolchain.check(), [])
        evidence = json.loads(output.getvalue())
        properties = evidence["effective_msbuild"]
        self.assertEqual(properties["NETCoreSdkVersion"], evidence["expected_sdk"])
        self.assertIn(Path(properties["MSBuildToolsPath"]).resolve(),
                      [Path(root).resolve() for root in evidence["installed_sdk_roots"]])
        self.assertEqual(Path(properties["MSBuildSDKsPath"]).resolve(),
                         (Path(properties["MSBuildToolsPath"]) / "Sdks").resolve())

    def test_project_effective_sdk_version_is_checked_even_when_cli_matches(self):
        with self.fixture() as root:
            (root / "Directory.Build.targets").write_text(
                "<Project><PropertyGroup><NETCoreSdkVersion>0.0.0</NETCoreSdkVersion></PropertyGroup></Project>",
                encoding="utf-8")
            self.assertTrue(any("Effective NETCoreSdkVersion" in error for error in self.check()))

    def test_project_sdk_root_is_checked_without_an_environment_override(self):
        with self.fixture() as root:
            (root / "Directory.Build.targets").write_text(
                f"<Project><PropertyGroup><MSBuildSDKsPath>{root / 'wrong-sdk'}</MSBuildSDKsPath>"
                "</PropertyGroup></Project>", encoding="utf-8")
            with patch.dict(os.environ):
                os.environ.pop("MSBuildSDKsPath", None)
                self.assertTrue(any("Effective MSBuild tools/SDK roots" in error for error in self.check()))

    def test_conflicting_sdk_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"MSBuildSDKsPath": tmp}):
                self.assertTrue(any("MSBuildSDKsPath" in error for error in self.check()))

    def test_both_running_and_path_python_must_match_the_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            (fixture / ".python-version").write_text("0.0.0\n", encoding="utf-8")
            shutil.copyfile(ROOT / "global.json", fixture / "global.json")
            (fixture / "tools/proto-toolchain").mkdir(parents=True)
            shutil.copyfile(ROOT / "tools/proto-toolchain/packages.lock.json",
                            fixture / "tools/proto-toolchain/packages.lock.json")
            with patch.object(toolchain, "ROOT", fixture):
                errors = self.check()
            self.assertTrue(any(error.startswith("Python ") for error in errors))
            self.assertTrue(any(error.startswith("PATH python ") for error in errors))


if __name__ == "__main__":
    unittest.main()
