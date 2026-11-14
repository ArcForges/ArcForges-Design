"""Generator selection is a lockfile decision, independent of ambient cache/PATH order."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_design as design  # noqa: E402


class LockedGenerator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root / "packages"
        self.toolchain = self.root / "tools/proto-toolchain"
        self.toolchain.mkdir(parents=True)
        (self.toolchain / "packages.lock.json").write_text(json.dumps({"dependencies": {
            "net11.0": {"Grpc.Tools": {"resolved": "2.85.0"}}}}), encoding="utf-8")
        self.selected, self.include = self.package("2.85.0")
        self.foreign, self.foreign_include = self.package("99.0.0")
        self.addCleanup(patch.stopall)
        patch.object(design, "ROOT", self.root).start()
        patch.dict(os.environ, {"NUGET_PACKAGES": str(self.cache), "ARCFORGES_PROTOC": "",
                                "ARCFORGES_PROTOC_INCLUDE": "", "PATH": str(self.foreign.parent)}).start()

    def package(self, version, cache=None):
        package = (cache or self.cache) / "grpc.tools" / version
        exe = package / "tools" / ("windows_x64" if os.name == "nt" else "linux_x64") / ("protoc.exe" if os.name == "nt" else "protoc")
        exe.parent.mkdir(parents=True)
        exe.write_bytes(b"selection fixture; never executed")
        include = package / "build/native/include"
        include.mkdir(parents=True)
        return exe, include

    def test_other_cached_versions_and_path_do_not_override_the_lock(self):
        self.assertEqual(design.find_protoc(), (str(self.selected), str(self.include)))

    def test_explicit_foreign_generator_or_include_is_rejected(self):
        for variable, path in (("ARCFORGES_PROTOC", self.foreign),
                               ("ARCFORGES_PROTOC_INCLUDE", self.foreign_include)):
            with self.subTest(variable=variable), patch.dict(os.environ, {variable: str(path)}):
                with self.assertRaisesRegex(ValueError, "conflicts with locked Grpc.Tools"):
                    design.find_protoc()

    def test_missing_locked_package_does_not_fall_back_to_path_or_other_cache(self):
        self.selected.unlink()
        self.assertEqual(design.find_protoc(), (None, None))
        with patch.dict(os.environ, {"ARCFORGES_PROTOC": str(self.foreign)}):
            with self.assertRaisesRegex(ValueError, "overrides cannot replace it"):
                design.find_protoc()

    def test_restore_assets_select_the_actual_package_folder(self):
        cache = self.root / "restore-selected-cache"
        exe, include = self.package("2.85.0", cache)
        (self.toolchain / "obj").mkdir()
        (self.toolchain / "obj/project.assets.json").write_text(json.dumps({"packageFolders": {str(cache): {}}}), encoding="utf-8")
        self.assertEqual(design.find_protoc(), (str(exe), str(include)))
