# Current V2 specification

Read this index and [AD-0022](decisions/AD-0022-cli-sandbox-platform-pivot.md) first. Only the files below and their explicit normative references define the current product. Research proves source facts; future-experiment records never prove runtime behavior.

| Area | Authority |
|---|---|
| Product and boundaries | [Definition](product/product-definition.md), [requirements](product/requirements.md), [non-goals](product/non-goals.md) |
| System and objects | [01 System](architecture/01-system-overview.md), [03 Sandbox and Run](architecture/03-sandbox-run-model.md) |
| Official engine | [02 MXC integration](architecture/02-mxc-integration.md), [research](research/mxc-research.md), [experiments](verification/mxc-experiments.md) |
| Local management | [04 Resources](architecture/04-resource-management.md), [05 Files and data](architecture/05-filesystem-data.md), [06 Node and CLI](architecture/06-local-node-cli.md), [07 Recovery](architecture/07-lifecycle-recovery.md) |
| Security | [08 Trust](architecture/08-security-trust.md) |
| Remote product | [09 Go Center](architecture/09-go-center.md), [10 Blazor](architecture/10-blazor-dashboard.md), [11 Identity and commerce](architecture/11-identity-commerce.md) |
| Delivery | [12 Distribution](architecture/12-distribution-updates.md), [verification](verification/platform-capabilities.md), [acceptance](verification/acceptance.md) |
| Wire and storage | [API conventions](contracts/README.md), [catalogue](contracts/api-catalogue.md), [errors](contracts/errors.md), [Node store](data/node-store.md), [Center store](data/cloud-store.md), [migrations](data/migrations.md), [state machines](state-machines/README.md) |
| Migration evidence | [Baseline](research/baseline.md), [local audit](research/runtime-audit.md), [cloud audit](research/cloud-audit.md), [disposition](reuse/disposition.md), [traceability](traceability/model.json) |

V2's Plan uses only `AFV2-*` task IDs. The complete V1 corpus is outside `docs/`, in the frozen history snapshot. The retained delivery/verification ADRs preserve their gates; product ADRs AD-0001–AD-0021 have an explicit disposition beside AD-0022.
