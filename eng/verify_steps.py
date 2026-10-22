# SPDX-License-Identifier: Apache-2.0
"""Local verification steps of ArcForges-Design, loaded by eng/verify.py (which injects `Step`).

The steps are exactly what .github/workflows/design.yml runs for external PRs: the locked restore of the pinned proto
toolchain, the design checks with protoc and the warning-free build of the generated C#, and the tool tests. Markdown is
this repository's source, so every change runs the full profile: the Windows leg on native Windows (where authors run
the checks) and the Linux leg on native Linux (as the Ubuntu runner), each on its own host after the push and reported
to GitHub as the commit statuses arcforges/windows and arcforges/linux (eng/verify.py; AGENTS.md rule 8). actionlint
runs only when a workflow changed.
"""

REPOSITORY = "ArcForges-Design"

# Tool versions recorded in each leg's summary (the python running eng/verify.py is added by the core).
FINGERPRINT = {
    "win": {"python": ["python", "--version"], "dotnet": ["dotnet", "--version"]},
    "linux": {"python": "python --version", "dotnet": "dotnet --version"},
}

# The environment of design.yml.
ENV = {"CI": "true", "DOTNET_NOLOGO": "true", "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "PYTHONUTF8": "1"}

RESTORE = "dotnet restore tools/proto-toolchain/ProtoToolchain.csproj --locked-mode"
CHECK = "python tools/check_design.py --require-protoc --compile"
TESTS = "python -m unittest discover -s tests -v"

# actionlint as pinned in the product repositories' CI, cached once on the Linux host; the archive is checked on every
# run.
ACTIONLINT = (
    "set -euo pipefail; v=1.7.12; "
    "sum=8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8; "
    "d=\"$HOME/.cache/arcforges-verify/tools\"; t=\"$d/actionlint_${v}_linux_amd64.tar.gz\"; mkdir -p \"$d\"; "
    "if [ ! -f \"$t\" ]; then "
    "curl --fail --silent --show-error --location --output \"$t.part\" "
    "\"https://github.com/rhysd/actionlint/releases/download/v${v}/actionlint_${v}_linux_amd64.tar.gz\"; "
    "echo \"$sum  $t.part\" | sha256sum --check --quiet; mv \"$t.part\" \"$t\"; fi; "
    "echo \"$sum  $t\" | sha256sum --check --quiet; "
    "mkdir -p \"$d/actionlint-$v\"; tar -xzf \"$t\" -C \"$d/actionlint-$v\" actionlint; "
    "\"$d/actionlint-$v/actionlint\""
)


def workflows_changed(changed: list[str]) -> bool:
    return any(path.startswith(".github/workflows/") for path in changed)


def select_profile(changed: list[str]) -> str:
    return "full"


STEPS = [
    Step("win-restore", "win", RESTORE.split(), timeout=600, env=ENV),
    Step("win-design-check", "win", CHECK.split(), timeout=1200, env=ENV),
    Step("win-tool-tests", "win", TESTS.split(), timeout=600, env=ENV),
    Step("linux-restore", "linux", RESTORE, timeout=600, env=ENV),
    Step("linux-design-check", "linux", CHECK, timeout=1200, env=ENV),
    Step("linux-tool-tests", "linux", TESTS, timeout=600, env=ENV),
    Step("actionlint", "linux", ACTIONLINT, timeout=300, lane="actionlint", when=workflows_changed),
]
