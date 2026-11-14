# ArcForges V2 design authority

ArcForges is an open-source general CLI sandbox and intelligent resource-management platform. Local CLI operation and self-hosted Go Center are free. The official hosted Center and Blazor remote dashboard are subscription services.

**Current authority:** [AD-0022](docs/decisions/AD-0022-cli-sandbox-platform-pivot.md), [product definition](docs/product/product-definition.md), [requirements](docs/product/requirements.md), and the [V2 design index](docs/README.md). The [Plan](https://github.com/ArcForges/Plan) owns delivery tasks and execution records.

This is a design and migration specification, not a claim that V2 is implemented. The source audit distinguishes delivered V1 code from V2 targets and unproven MXC combinations. Read [verification](docs/verification/platform-capabilities.md) before making a platform support claim.

[AD-0023](docs/decisions/AD-0023-current-dependency-baseline.md) adds the owner-directed dependency upgrade: merge the reviewed policy documents first, then upgrade all current dependencies across the seven delivery repositories with local/CI parity before product implementation resumes.

All earlier product definitions, task contracts, AI/MCP routing, cache platforms, desktop/mobile applications, and Center-required local execution are superseded. Their unmodified evidence is frozen at `62172622550fff73a553135ca178f9b7117c9cbd` under [history/v1-20261114](history/v1-20261114-notice.md). Never execute a historical task from that archive.

## Contributing and validation

Work in `design/<topic>` worktrees. Update the schema and traceability together. Run `python tools/check_design.py --write` to generate the API catalogue and state-machine index; run `python tools/check_design.py --plan <Plan>/delivery-graph.json` to cross-check requirements. Required Windows/Linux host verification, independent review, and Design-before-Plan merge order remain in force; see [AGENTS.md](AGENTS.md). No product code belongs in this repository.
