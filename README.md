# ArcForges-Design

The authoritative design of **ArcForges**: a cross-platform resource-control and execution platform for AI and automation, local and across a LAN ([AD-0001](docs/decisions/AD-0001-flagship-pivot.md)). It contains no implementation; the implementation lives in `ArcForges/ArcForges`, `Contracts`, `DesktopPlatform`, `Cloud`, `Web` and `Mobile`.

- **Start here:** [docs/README.md](docs/README.md)
- **Delivery plan:** [ArcForges/Plan](https://github.com/ArcForges/Plan)
- **History:** the earlier product-family design is frozen in `ArcForges/ArcForges-Design-Parallel` (main `64173614`). It is cited by commit, never edited.

## Checks

The checks need Python 3.14 (`.python-version`) and the .NET SDK (`global.json`), which supplies the pinned protoc.

```bash
dotnet restore tools/proto-toolchain/ProtoToolchain.csproj --locked-mode
python tools/check_design.py --require-protoc
python -m unittest discover -s tests -v
```

`tools/check_design.py` verifies:
- the protos compile and follow the Contracts conventions (envelopes, `json_name`, explicit presence, method annotations, error codes against [errors.md](docs/contracts/errors.md));
- the generated [API catalogue](docs/contracts/api-catalogue.md) and [state-machine pages](docs/state-machines/README.md) are current (`--write` regenerates them);
- state machines match their proto enums and are reachable;
- both SQL schemas load in SQLite;
- every relative link resolves;
- requirement, verification, decision and state-machine IDs exist;
- every requirement is traced to design and tasks (`--plan <delivery-graph.json>` also checks the task IDs).

`--compile` also builds the generated C#, warning-free under `IsAotCompatible`.

## Licence

Documentation © ArcForges. Proto specifications are Apache-2.0, as in the Contracts repository.
