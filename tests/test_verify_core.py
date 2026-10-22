# SPDX-License-Identifier: Apache-2.0
"""Tests of the shared verification core (eng/verify.py, the same file in every ArcForges repository).

Each test builds a throwaway repository with its own origin and step table and drives eng/verify.py as a verification
host does. The origin's configured URL is a github.com URL rewritten to the local bare repository (url.<base>.insteadOf),
and a fake `gh` on PATH records the commit statuses that `run-and-report` posts. Only the Linux host runs here; the
tests are skipped on other operating systems.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

CORE = Path(__file__).resolve().parent.parent / "eng" / "verify.py"

TABLE = '''REPOSITORY = "CoreTest-{name}"
FINGERPRINT = {{"linux": {{"bash": "bash --version | head -n 1", "token": "echo [$ARCFORGES_STATUS_TOKEN]"}}}}
def select_profile(changed): {profile}
STEPS = [
{steps}
]
'''

# Records each call (one line of arguments, and whether the expected token reached it, never its value) and fails like
# GitHub when GH_FAIL is set, or only for the state named by GH_FAIL_STATE.
FAKE_GH = """#!/bin/sh
printf '%s\\n' "$*" >> "$GH_LOG"
if [ -n "$EXPECT_TOKEN" ] && [ "$GH_TOKEN" = "$EXPECT_TOKEN" ]; then echo "token-match" >> "$GH_LOG"; fi
if [ -n "$GH_FAIL" ]; then echo "gh: No commit found for SHA: x (HTTP 422)" >&2; exit 1; fi
case "$*" in *"state=$GH_FAIL_STATE "*) if [ -n "$GH_FAIL_STATE" ]; then echo "gh: (HTTP 502)" >&2; exit 1; fi;; esac
exit 0
"""


def run(argv: list[str], cwd: Path, stdin: str = "", env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=300,
                          env=dict(os.environ, **(env or {})))


@unittest.skipUnless(sys.platform.startswith("linux") and shutil.which("setsid") and shutil.which("timeout"),
                     "the Linux host of the verification core")
class VerifyCore(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="verify-core-"))
        self.home = self.root / "home"
        self.home.mkdir()
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(FAKE_GH, encoding="utf-8")
        (bin_dir / "gh").chmod(0o755)
        self.gh_log = self.root / "gh.log"
        self.env = {"HOME": str(self.home), "GIT_CONFIG_GLOBAL": str(self.root / "gitconfig"),
                    "GIT_CONFIG_NOSYSTEM": "1", "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                    "GH_LOG": str(self.gh_log)}
        (self.root / "gitconfig").write_text("[user]\n\temail = t@example.invalid\n\tname = t\n"
                                             "[init]\n\tdefaultBranch = main\n", encoding="utf-8")
        self.counter = 0

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def git(self, cwd: Path, *args: str) -> str:
        result = run(["git", *args], cwd, env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def repository(self, steps: str, name: str = "a", profile: str = 'return "full"') -> Path:
        """A clone with an origin whose main holds the core and the table, and a feature commit on top."""
        self.counter += 1
        origin = self.root / f"origin-{name}-{self.counter}.git"
        self.git(self.root, "init", "-q", "--bare", str(origin))
        work = self.root / f"work-{name}-{self.counter}"
        self.git(self.root, "clone", "-q", str(origin), str(work))
        # Reports go to github.com/ArcForges/CoreTest-<name>; fetches of that URL reach the local origin.
        url = f"https://github.com/ArcForges/CoreTest-{name}.git"
        self.git(work, "remote", "set-url", "origin", url)
        self.git(work, "config", f"url.{origin}.insteadOf", url)
        (work / "eng").mkdir()
        shutil.copy(CORE, work / "eng" / "verify.py")
        (work / "eng" / "verify_steps.py").write_text(TABLE.format(name=name, steps=steps, profile=profile),
                                                     encoding="utf-8")
        (work / "a.txt").write_text("base\n", encoding="utf-8")
        self.git(work, "add", "-A")
        self.git(work, "commit", "-qm", "base")
        self.git(work, "push", "-q", "origin", "HEAD:main")
        self.git(work, "checkout", "-q", "-b", "feature")
        (work / "a.txt").write_text("change\n", encoding="utf-8")
        self.git(work, "commit", "-qam", "change")
        return work

    def verify(self, work: Path, *args: str, stdin: str = "", env: dict[str, str] | None = None
               ) -> subprocess.CompletedProcess:
        return run([sys.executable, "eng/verify.py", *args], work, stdin=stdin, env=dict(self.env, **(env or {})))

    def statuses(self) -> list[dict[str, str]]:
        """The statuses the fake gh was asked to post, in order."""
        posted = []
        lines = self.gh_log.read_text(encoding="utf-8").splitlines() if self.gh_log.exists() else []
        for line in lines:
            if line.startswith("token-"):
                continue
            fields = dict(part.split("=", 1) for part in line.split(" -f ")[1:])
            fields["endpoint"] = line.split()[5]
            posted.append(fields)
        return posted

    def test_the_linux_leg_runs_natively_in_its_own_clone(self) -> None:
        work = self.repository('Step("linux-a", "linux", "test \\"$PWD\\" = \\"$HOME/.cache/arcforges-verify/CoreTest-a\\" '
                               '&& test \\"$(git rev-parse HEAD)\\" = {sha} && test -z \\"$(git status --porcelain)\\" '
                               '&& echo $ARCFORGES_VERIFY-$X", timeout=60, env={"X": "y"})')
        result = self.verify(work, "run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("arcforges-verify: LEG PASS", result.stdout)
        self.assertIn("arcforges-verify: PASS", result.stdout)
        [summary] = (work / ".git" / "arcforges-verify" / "logs").glob("*-linux/summary.json")
        data = json.loads(summary.read_text(encoding="utf-8"))
        self.assertTrue(data["ok"])
        self.assertEqual(data["sha"], self.git(work, "rev-parse", "HEAD"))
        self.assertIn("1-y", (summary.parent / "linux-a.log").read_text(encoding="utf-8"))
        self.assertTrue(data["results"][0]["log_sha256"])
        self.assertTrue((self.home / ".cache" / "arcforges-verify" / "CoreTest-a" / ".git").is_dir())
        self.assertEqual(self.statuses(), [], "run reports nothing")

    def test_run_and_report_posts_pending_then_success_for_the_exact_commit(self) -> None:
        work = self.repository('Step("linux-a", "linux", "true", timeout=60),\n'
                               'Step("linux-b", "linux", "true", timeout=60, lane="other")')
        sha = self.git(work, "rev-parse", "HEAD")
        result = self.verify(work, "run-and-report")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        posted = self.statuses()
        self.assertEqual([s["state"] for s in posted], ["pending", "success"])
        for status in posted:
            self.assertEqual(status["endpoint"], f"repos/ArcForges/CoreTest-a/statuses/{sha}")
            self.assertEqual(status["context"], "arcforges/linux")
        self.assertIn("2 steps passed", posted[1]["description"])

    def test_a_failed_step_reports_failure_and_fails_the_command(self) -> None:
        work = self.repository('Step("linux-ok", "linux", "true", timeout=60),\n'
                               'Step("linux-bad", "linux", "echo broken; exit 3", timeout=60, lane="other")')
        result = self.verify(work, "run-and-report")
        self.assertEqual(result.returncode, 1)
        self.assertIn("linux-bad (exit code 3)", result.stderr)
        self.assertIn("broken", result.stdout)
        posted = self.statuses()
        self.assertEqual([s["state"] for s in posted], ["pending", "failure"])
        self.assertIn("linux-bad (exit code 3)", posted[1]["description"])
        self.assertLessEqual(len(posted[1]["description"]), 140)

    def test_a_leg_that_cannot_complete_reports_error(self) -> None:
        work = self.repository('Step("linux-a", "linux", "true", timeout=60)',
                               profile='raise RuntimeError("broken table")')
        result = self.verify(work, "run-and-report")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("broken table", result.stderr)
        self.assertEqual([s["state"] for s in self.statuses()], ["pending", "error"])

    def test_an_unpushed_commit_is_refused_before_any_step_runs(self) -> None:
        marker = self.root / "ran"
        work = self.repository(f'Step("linux-a", "linux", "touch {marker}", timeout=60)')
        result = self.verify(work, "run-and-report", env={"GH_FAIL": "1"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("HTTP 422", result.stderr)
        self.assertIn("Is the commit pushed to GitHub", result.stderr)
        self.assertFalse(marker.exists(), "a step ran although the status could not be reported")

    def test_a_host_without_steps_reports_success_saying_so(self) -> None:
        work = self.repository('Step("win-a", "win", ["cmd", "/c", "exit 0"], timeout=60)')
        result = self.verify(work, "run-and-report")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        posted = self.statuses()
        self.assertEqual([s["state"] for s in posted], ["pending", "success"])
        self.assertIn("no Linux steps apply", posted[1]["description"])

    def test_the_status_token_reaches_gh_and_never_a_step(self) -> None:
        secret = "token-for-test-only-0f9e"
        # The login profile of the host exports a token again; the step must still not see it.
        (self.home / ".profile").write_text(f"export ARCFORGES_STATUS_TOKEN={secret}-profile\nexport GH_TOKEN=ambient\n",
                                            encoding="utf-8")
        work = self.repository('Step("linux-a", "linux", "echo \\"[$ARCFORGES_STATUS_TOKEN][$GH_TOKEN][$GITHUB_TOKEN]\\"", '
                               'timeout=60)')
        result = self.verify(work, "run-and-report", env={"ARCFORGES_STATUS_TOKEN": secret, "GITHUB_TOKEN": "ambient",
                                                          "EXPECT_TOKEN": secret})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn(secret, result.stdout + result.stderr)
        [log] = (work / ".git" / "arcforges-verify" / "logs").glob("*-linux/linux-a.log")
        text = log.read_text(encoding="utf-8")
        self.assertIn("\n[][][]\n", text)
        self.assertNotIn(secret, text)
        [summary] = log.parent.glob("summary.json")
        self.assertEqual(json.loads(summary.read_text(encoding="utf-8"))["tools"]["linux:token"], "[]")
        self.assertIn("token-match", self.gh_log.read_text(encoding="utf-8"))

    def test_an_ambient_github_token_reaches_gh_but_no_step(self) -> None:
        work = self.repository('Step("linux-a", "linux", "echo \\"[$GH_TOKEN]\\"", timeout=60)')
        result = self.verify(work, "run-and-report", env={"GH_TOKEN": "ambient-0f9e", "EXPECT_TOKEN": "ambient-0f9e"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        [log] = (work / ".git" / "arcforges-verify" / "logs").glob("*-linux/linux-a.log")
        self.assertIn("\n[]\n", log.read_text(encoding="utf-8"))
        self.assertIn("token-match", self.gh_log.read_text(encoding="utf-8"))

    def test_a_terminated_run_reports_error(self) -> None:
        started = self.root / "started"
        marker = self.root / "slow.pid"
        work = self.repository(f'Step("linux-slow", "linux", "sleep 60 & echo $! > {marker}; touch {started}; wait", '
                               'timeout=120)')
        running = subprocess.Popen([sys.executable, "eng/verify.py", "run-and-report"], cwd=work, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, env=dict(os.environ, **self.env))
        deadline = time.monotonic() + 120
        while not started.exists() and running.poll() is None and time.monotonic() < deadline:
            time.sleep(0.1)
        running.terminate()
        output, _ = running.communicate(timeout=120)
        self.assertEqual(running.returncode, 2, output)
        self.assertEqual([s["state"] for s in self.statuses()], ["pending", "error"])
        child = int(marker.read_text().strip())
        time.sleep(1)
        self.assertFalse(Path(f"/proc/{child}").exists() and "sleep" in Path(f"/proc/{child}/cmdline").read_text(errors="replace"),
                         "the interrupted step's process is still running")

    def test_a_success_that_cannot_be_reported_fails_the_command(self) -> None:
        work = self.repository('Step("linux-a", "linux", "true", timeout=60)')
        result = self.verify(work, "run-and-report", env={"GH_FAIL_STATE": "success"})
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cannot report arcforges/linux success", result.stderr)
        self.assertNotIn("arcforges-verify: PASS", result.stdout)

    def test_keep_going_runs_every_step_and_still_fails(self) -> None:
        marker = self.root / "second"
        work = self.repository(f'Step("linux-bad", "linux", "exit 3", timeout=60),\n'
                               f'Step("linux-after", "linux", "touch {marker}", timeout=60)')
        result = self.verify(work, "run-and-report", "--keep-going")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertTrue(marker.exists(), "--keep-going stopped after the first failure")
        self.assertEqual([s["state"] for s in self.statuses()], ["pending", "failure"])

    def test_the_retired_pre_push_hook_lets_the_push_through(self) -> None:
        work = self.repository('Step("linux-a", "linux", "false", timeout=60)')
        sha = self.git(work, "rev-parse", "HEAD")
        result = self.verify(work, "pre-push", "origin", stdin=f"refs/heads/feature {sha} refs/heads/feature {'0' * 40}\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("verification runs after the push", result.stderr)
        self.assertEqual(self.statuses(), [])

    def test_a_timed_out_step_is_stopped_with_its_children(self) -> None:
        marker = self.root / "child.pid"
        work = self.repository(f'Step("linux-slow", "linux", "sleep 300 & echo $! > {marker}; wait", timeout=3)')
        started = time.monotonic()
        result = self.verify(work, "run")
        self.assertEqual(result.returncode, 1)
        self.assertIn("timed out after 3s", result.stderr)
        self.assertLess(time.monotonic() - started, 120)
        child = int(marker.read_text().strip())
        time.sleep(1)
        self.assertFalse(Path(f"/proc/{child}").exists() and "sleep" in Path(f"/proc/{child}/cmdline").read_text(errors="replace"),
                         "the step's child process survived the timeout")

    def test_a_shallow_clone_is_refused(self) -> None:
        work = self.repository('Step("linux-a", "linux", "true", timeout=60)')
        shallow = self.root / "shallow"
        self.git(self.root, "clone", "-q", "--depth", "1", f"file://{work}", str(shallow))
        result = self.verify(shallow, "run")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("git fetch --unshallow", result.stderr)

    def test_an_incomplete_linux_clone_is_made_again(self) -> None:
        work = self.repository('Step("linux-a", "linux", "test \\"$(git rev-list --count HEAD)\\" = 3", timeout=60)')
        # History below the merge base: main gets a second commit and the feature moves onto it.
        root = self.git(work, "rev-parse", "main")
        self.git(work, "checkout", "-q", "main")
        (work / "b.txt").write_text("b\n", encoding="utf-8")
        self.git(work, "add", "b.txt")
        self.git(work, "commit", "-qm", "main two")
        self.git(work, "push", "-q", "origin", "main")
        self.git(work, "checkout", "-q", "feature")
        self.git(work, "rebase", "-q", "main")
        clone = self.home / ".cache" / "arcforges-verify" / "CoreTest-a"
        first = self.verify(work, "run")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        # Lose the root commit below the merge base, as a fetch from a shallow source leaves the clone.
        objects = clone / ".git" / "objects"
        for pack in sorted((objects / "pack").glob("*.pack")):
            moved = self.root / pack.name
            pack.rename(moved)
            pack.with_suffix(".idx").unlink()
            subprocess.run(["git", "unpack-objects", "-q"], cwd=clone, stdin=moved.open("rb"), check=True,
                           env=dict(os.environ, **self.env))
        (objects / root[:2] / root[2:]).unlink()
        self.assertNotEqual(run(["git", "rev-list", "--count", "HEAD"], clone, env=self.env).returncode, 0)
        # The commit and the base are both still there, so a fetch alone would bring nothing and leave the hole.
        second = self.verify(work, "run")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertIn("making it again", second.stdout)
        self.assertIn("arcforges-verify: LEG PASS", second.stdout)

    def test_a_shallow_linux_clone_is_made_again(self) -> None:
        work = self.repository('Step("linux-a", "linux", "test \\"$(git rev-list --count HEAD)\\" = 2", timeout=60)')
        clone = self.home / ".cache" / "arcforges-verify" / "CoreTest-a"
        first = self.verify(work, "run")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        # A shallow boundary at the commit itself: rev-list walks from it and from the base without an error.
        sha = self.git(work, "rev-parse", "HEAD")
        (clone / ".git" / "shallow").write_text(sha + "\n", encoding="utf-8")
        self.assertEqual(run(["git", "rev-list", "--quiet", sha, self.git(work, "rev-parse", "main")], clone,
                             env=self.env).returncode, 0)
        second = self.verify(work, "run")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertIn("making it again", second.stdout)
        self.assertIn("arcforges-verify: LEG PASS", second.stdout)
        self.assertEqual(self.git(clone, "rev-parse", "--is-shallow-repository"), "false")

    def test_two_clones_of_a_repository_never_run_linux_legs_at_once(self) -> None:
        started, release = self.root / "started", self.root / "release"
        steps = (f'Step("linux-a", "linux", "touch {started}; while [ ! -e {release} ]; do sleep 0.1; done; '
                 'test \\"$(git rev-parse HEAD)\\" = {sha}", timeout=60)')
        first = self.repository(steps, name="shared")
        second = self.root / "second"
        origin = next(self.root.glob("origin-shared-*.git"))
        self.git(self.root, "clone", "-q", str(origin), str(second))
        self.git(second, "remote", "set-url", "origin", "https://github.com/ArcForges/CoreTest-shared.git")
        self.git(second, "config", f"url.{origin}.insteadOf", "https://github.com/ArcForges/CoreTest-shared.git")
        (second / "b.txt").write_text("other\n", encoding="utf-8")
        self.git(second, "add", "b.txt")
        self.git(second, "commit", "-qm", "other")
        running = subprocess.Popen([sys.executable, "eng/verify.py", "run"], cwd=first, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, env=dict(os.environ, **self.env))
        try:
            deadline = time.monotonic() + 120
            while not started.exists() and running.poll() is None and time.monotonic() < deadline:
                time.sleep(0.1)
            self.assertTrue(started.exists(), "the first clone's step did not start")
            # The second clone shares the Linux-native clone and pid files; its leg must not touch the running one.
            refused = self.verify(second, "run")
            self.assertEqual(refused.returncode, 2, refused.stdout + refused.stderr)
            self.assertIn("another clone's Linux leg of this repository", refused.stderr)
            release.touch()
            output, _ = running.communicate(timeout=120)
        finally:
            release.touch()
            if running.poll() is None:
                running.kill()
        self.assertEqual(running.returncode, 0, output)
        self.assertIn("arcforges-verify: LEG PASS", output)
        started.unlink()
        after = self.verify(second, "run")
        self.assertEqual(after.returncode, 0, after.stdout + after.stderr)
        self.assertIn("arcforges-verify: LEG PASS", after.stdout)


class GitHubRepository(unittest.TestCase):
    """The remote URL forms run-and-report accepts, and the ones it refuses without printing a credential."""

    def parse(self, url: str) -> str:
        spec = importlib.util.spec_from_file_location("arcforges_verify_core", CORE)
        core = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = core
        spec.loader.exec_module(core)
        with mock.patch.object(core, "git", return_value=url):
            return core.github_repository("origin")

    def test_accepted_forms(self) -> None:
        for url in ("https://github.com/ArcForges/Plan.git", "https://github.com/ArcForges/Plan",
                    "https://x-access-token:abc@github.com/ArcForges/Plan.git", "https://github.com/ArcForges/Plan/",
                    "ssh://git@github.com/ArcForges/Plan.git", "git@github.com:ArcForges/Plan.git"):
            self.assertEqual(self.parse(url), "ArcForges/Plan", url)
        self.assertEqual(self.parse("https://github.com/ArcForges/ArcForges-Design.git"), "ArcForges/ArcForges-Design")

    def test_refused_forms_never_print_a_credential(self) -> None:
        for url in ("https://user:ghp_SECRET@github.com/ArcForges/Plan/pulls", "https://example.com/ArcForges/Plan.git",
                    "git@github-alias:ArcForges/Plan.git", "https://github.com/ArcForges/..", "/srv/git/plan.git"):
            with self.assertRaises(Exception) as caught:
                self.parse(url)
            self.assertIn("not a github.com repository", str(caught.exception), url)
            self.assertNotIn("SECRET", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
