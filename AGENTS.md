# AGENTS.md

Instructions for AI coding agents and contributors working in the ArcForges Design repository.

## Guidelines

- **Pure documentation repository**: This repository is strictly for documentation and design artifacts; it does not contain product source code.
- **Formal documentation in English**: All formal repository content, requirements, architecture, decisions, and planning must be written in English.
- **Current design authority**: Use current requirements, architecture, planning and assurance under the effective accepted decisions. Record missing current definitions in those layers; do not fill gaps by treating archived inputs as requirements.
- **Deprecated inputs**: `docs/deprecated-inputs/` has completed its role in producing the formal design. Its four `*-deprecated.md` files are historical provenance only, excluded from ongoing design, implementation planning and design-completeness audits. Do not reread, extract commitments from, remap or reconcile them as part of those tasks. Historical `I1`–`I4` and Stage citations do not create a new reading obligation. Keep the archived file bodies unchanged. Reference-source review obligations remain governed by the current design and reference-coverage documents.
- **No empty placeholder batches**: Do not create speculative or empty placeholder files without substantive content.
- **Work in worktree**: Always work inside `.worktree/` branches rather than checking out or modifying the primary checkout branch.
- **Planning changes**: Implementation scheduling follows the [delivery model](docs/planning/delivery/README.md). Edit `docs/planning/delivery/delivery-graph.json` in a retained Design worktree, regenerate the views with the Plan repository's tool, `python C:\MyFile\Projects\Plan-B\tools\delivery.py generate --plan <Plan worktree> --design <Design worktree>`, and require `check` with the same roots to pass ([DLV-33](docs/planning/delivery/README.md#rule-dlv-33)). Always name both roots: without them this tool uses the Plan and Design primary checkouts, whatever the current directory. Never run `generate` against a primary checkout, and never edit a primary checkout. Never edit generated views or generated section 9 blocks by hand.
- **Integration**: `CLAUDE.md` defers directly to this file.

## CI and validation restrictions

Follow [the accepted CI and local validation policy](docs/assurance/ci-and-local-validation-policy.md) for all planning and implementation. Never prescribe macOS CI, hosted device/emulator/GUI/browser/live-service/inference/installed-consumer tests, or routine post-publication downloads/hash/install checks. Retain necessary Windows/Linux builds, targeted offline checks, signatures, locks, licences and non-duplicated security. Local runtime checks are affected-scope, existing-environment opt-in and are not repeated after passing. No toolchain reinstall or hidden heavy Git hooks. Independent delivery tasks may run concurrently under atomic claims; serialize heavy local builds per workstation. Use normal networking and no wsl.exe wrappers; stop on a network failure. Post-merge verification is commit/job status and a clean fast-forward only. Historical receipts are not active testing mandates.

Documentation-only PRs in documentation repositories with no configured CI merge after review. Repositories with CI must pass all applicable required checks even for documentation-only changes. Do not add skip-CI directives, disable workflows or bypass required checks merely because a PR changes documentation. Documentation changes do not require additional ad-hoc local product builds or runtime tests.
