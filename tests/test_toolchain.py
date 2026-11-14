"""Exercise version rejection with real installed tools and isolated selector inputs."""
import io
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eng"))
import check_toolchain as toolchain  # noqa: E402


class ToolchainSelection(unittest.TestCase):
    def check(self):
        with redirect_stdout(io.StringIO()):
            return toolchain.check()

    def test_actual_tools_match_repository_pins(self):
        self.assertEqual(self.check(), [])

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
