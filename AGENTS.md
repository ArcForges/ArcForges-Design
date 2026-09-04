# AGENTS.md

This file is the primary instruction source for humans and AI coding agents working in the ArcForges Design repository. `CLAUDE.md` defers to this file.

## Repository purpose

This is a design-only repository. It owns product requirements, architecture specifications, architecture decision records, delivery planning, and assurance criteria. It does not contain ArcForges product implementation.

An accepted document proves only that the document has been reviewed and accepted. It does not prove that code exists, builds pass, tests pass, performance targets are met, or a release has shipped.

## Working rules

- Work in a Git worktree under `.worktree/`; never switch the user's primary checkout.
- Use focused branches with the `codex/` prefix unless the user specifies another name.
- Preserve user changes and never use destructive reset or checkout commands.
- Use one serial execution context. Do not delegate, hand off, or parallelize the design program.
- Write all canonical repository content in English. Informative source material under `docs/inputs` may retain its original language.
- Use stable, responsibility-based names. Do not name canonical files or directories after "future", "rewrite", "latest", a temporary migration, or a vendor.
- Do not create empty batches of speculative documents. A directory may contain only a `README.md` until real content is approved.
- Do not invent an implementation sequence before its requirements and architecture are accepted.
- Keep source material under `docs/inputs` informative. Promote a statement into a canonical document only through explicit review.

## Authority by concern

There is no single global file-precedence rule. Authority depends on the concern:

- `docs/requirements` owns product scope, user-visible behavior, and quality requirements.
- `docs/architecture` owns boundaries, topology, data ownership, interfaces, and technical constraints.
- `docs/decisions` records why significant choices were made. An accepted decision must be reflected in every affected canonical document; it does not silently override them.
- `docs/planning` owns dependency order and delivery gates only after upstream requirements and architecture are accepted.
- `docs/assurance` owns traceability, review methods, risks, acceptance criteria, and evidence obligations.
- `docs/inputs` provides provenance and context only. It is never normative.

If canonical documents conflict, stop and reconcile the conflict explicitly. Do not choose a convenient interpretation and continue.

## Document lifecycle

Canonical documents use `draft`, `proposed`, `accepted`, `superseded`, or `retired`. Input documents use `informative`. Accepted architecture decision records are immutable in meaning; create a new decision record to supersede one.

## Review expectations

Before pushing:

1. Review the complete diff.
2. Check links, naming, Markdown structure, and English-only canonical content.
3. Confirm that informative inputs are not described as authority.
4. Confirm that no implementation or verification claim lacks evidence.
5. Confirm that the pull request remains focused.
