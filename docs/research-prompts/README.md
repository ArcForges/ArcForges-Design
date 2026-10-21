# Priority Research Prompts (PRP)

A Priority Research Prompt is a complete, ready-to-use prompt for research that the product owner wants performed later. It preserves the prompt exactly as the owner gave it, so the research can start from it without being specified again. A PRP is stored instructions, not a task, a decision or a roadmap row.

## Rules

- **Consideration priority.** When the owner asks for future research, the PRPs here are considered before ordinary deferred roadmap research (the `RM-*` and `EX-*` rows of the canonical [roadmap](https://github.com/ArcForges/Plan/blob/main/roadmap.md)).
- **Saving is not authorization.** A PRP is researched only when the owner explicitly requests it. Saving one authorizes neither its research nor any implementation.
- **No override.** A PRP does not supersede delivery authorization (the Plan's delivery graph and serial delivery, [AD-0014](../decisions/AD-0014-delivery-method.md)), accepted decisions, or the canonical roadmap and its governance ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §9). Saving a PRP does not by itself displace active implementation work.
- **Outcomes take the normal route.** Research results are recorded like any other study (a record under [research/](../README.md#research)); design changes, new decisions and roadmap changes go through reviewed Design and Plan PRs. Running a PRP never promotes a roadmap item.

## Naming

`PRP-NNNN-<topic>.md`: a four-digit number, assigned in sequence and never reused, and a short kebab-case topic, for example `PRP-0001-network-plugins-and-platform-positioning.md`.

Each file holds:
- **metadata:** the ID, the title, the date saved, who requested it, the related design material, and a status line (`Saved, not researched`, or `Researched` with a link to the research record);
- **the prompt:** the research instructions verbatim, enclosed in quotation marks in a text block.

The prompt is not edited after it is saved. A revised prompt is a new PRP that names the one it replaces.

## Using a saved prompt

1. The owner explicitly requests a PRP by its ID.
2. The agent copies the quoted prompt from the file and uses it as the research brief, together with this repository's [AGENTS.md](../../AGENTS.md).
3. The research is recorded and reviewed through the normal route above.
4. A reviewed PR sets the PRP's status line to `Researched` and links the research record. The prompt stays as saved.

## Index

| ID | Topic |
|---|---|
| [PRP-0001](PRP-0001-network-plugins-and-platform-positioning.md) | Network management, a general-purpose plugin ecosystem and product positioning |
