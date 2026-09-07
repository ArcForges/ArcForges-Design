# AGENTS.md

Instructions for AI coding agents and contributors working in the ArcForges Design repository.

## Guidelines

- **Pure documentation repository**: This repository is strictly for documentation and design artifacts; it does not contain product source code.
- **Formal documentation in English**: All formal repository content, requirements, architecture, decisions, and planning must be written in English.
- **Current design authority**: Use current requirements, architecture, planning and assurance under the effective accepted decisions. Record missing current definitions in those layers; do not fill gaps by treating archived inputs as requirements.
- **Deprecated inputs**: `docs/deprecated-inputs/` has completed its role in producing the formal design. Its four `*-deprecated.md` files are historical provenance only, excluded from ongoing design, implementation planning and design-completeness audits. Do not reread, extract commitments from, remap or reconcile them as part of those tasks. Historical `I1`–`I4` and Stage citations do not create a new reading obligation. Keep the archived file bodies unchanged. Reference-source review obligations remain governed by the current design and reference-coverage documents.
- **No empty placeholder batches**: Do not create speculative or empty placeholder files without substantive content.
- **Work in worktree**: Always work inside `.worktree/` branches rather than checking out or modifying the primary checkout branch.
- **Integration**: `CLAUDE.md` defers directly to this file.
