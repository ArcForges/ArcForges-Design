# Reference Coverage Matrix — ArcScope / Serial-Studio

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete**
> Governing authority: **D-012**, **D-013**, **D-002** (ArcScope is independently defined, not a rename of a superseded product)
> Consuming product: **ArcScope** — [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md)

---

## 1. Source identity

| Field | Value |
|---|---|
| Repository | `github.com/Serial-Studio/Serial-Studio` |
| Local path | `C:\MyFile\ArcForges\Serial-Studio` |
| Commit | `639daafb` |
| Commit date | 2026-07-13 |
| Reviewed on | 2026-09-05 |
| Reviewer | Architecture Owner (design stage) |

---

## 2. Licence and provenance position — the most restrictive in the programme

`LICENSE.md` is a **custom dual-licence agreement**, not a standard grant. Read in full:

| Element | Evidence | Finding |
|---|---|---|
| Model | `LICENSE.md` §1 | **Dual**: GPL-3.0-only for source, **Serial Studio Commercial License** for official binaries and any build including gated features |
| GPL scope | `LICENSE.md` §1, §2 | GPLv3 applies **only** to components explicitly marked as such and **excludes** the Pro modules |
| GPL conditions | `LICENSE.md` §2.1 | Must compile from source; must use a GPL-compliant Qt; **must not enable, link, replicate, simulate or include any Pro module** |
| Pro modules (commercial-only, excluded from GPL) | `LICENSE.md` §4 | Qt MQTT and Qt SerialBus modules; **MQTT support**; **XY plotting**; **3D visualization**; **activation/licensing systems** |
| Pro module status | `LICENSE.md` §4 | *"defined as separate works and not covered by GPLv3. Their source code, even if visible, does not confer any right to use, modify, compile, or distribute them"* |
| Binary trial | `LICENSE.md` §1.1 | Official binary is a 14-day single-use trial, then requires a paid licence |
| Licence file set | `LICENSES/GPL-3.0-only.txt`, `LICENSES/LicenseRef-SerialStudio-Commercial.txt` | Confirms the two-licence structure |

| # | Finding |
|---|---|
| LP-01 | **The GPL portion is GPL-3.0-only.** Under **D-013**, GPL-only material **must not be copied, translated or ported**. It may be used only as controlled behavioural reference. |
| LP-02 | **The Pro modules are commercial-only and are not open source at all.** Source visibility confers no rights. They are treated as an **authorship boundary**: their source was not read, and no ArcForges capability may be derived from their expression. |
| LP-03 | **The packaged binary in `StartArcForges/Serial-Studio` is trial-limited commercial software.** It was **not executed** — consistent with the instruction not to execute packaged-product binaries, and independently required here because execution would consume a licensed trial. |
| LP-04 | **Every row in this matrix is `Reference Only` or an accepted exclusion.** No reuse is possible from either portion. |

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| Licence agreement in full | `LICENSE.md`, `LICENSES/` |
| Acquisition and transport | `app/src/IO/**`, `app/src/IO/Drivers/**` |
| Frame and data model | `app/src/DataModel/**` |
| Session, recording, replay, export, reporting | `app/src/Sessions/**`, `app/src/CSV/**`, `app/src/MDF4/**` |
| Visualisation surface | `app/qml/Widgets/Dashboard/**`, `app/src/UI/**` |
| Console | `app/src/Console/**` |
| API surface | `app/src/API/**` |
| Miscellaneous services | `app/src/Misc/**` |
| Platform integration | `app/src/Platform/**` |
| Test approach | `tests/{integration,unit,performance,security,benchmarks,manual}/**` |
| Packaged release shape | `StartArcForges/Serial-Studio` — directory listing only, **not executed** |

**Not read, and why:** `app/src/MQTT/**`, `app/src/Licensing/**`, and the 3D/XY plotting implementations — **Pro modules under `LICENSE.md` §4**. Their expression is deliberately not read; their existence and stated purpose are recorded from the licence text and directory names alone. `app/src/ThirdParty/**` — vendored dependencies under their own licences, out of scope.

---

## 4. Item-level matrix

| # | Capability / behaviour | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|
| AS-01 | Connection and device management separation | `app/src/IO/{ConnectionManager,DeviceManager}.{h,cpp}` | `products/arcscope.md` `SD-01` (`Device ≠ DataSource`); `WP-33.00` | Reference Only | **Independent confirmation of `I-466`**: the reference separates connection management from device identity | GPL-3.0-only — no reuse permitted | First-party test: `Device ≠ DataSource` structurally | Product Owner | Evidence established |
| AS-02 | Transport drivers — serial, network, Bluetooth LE, HID, audio, process, CAN, Modbus | `app/src/IO/Drivers/{Network,BluetoothLE,HID,Audio,Process,CANBus,CanBackends,GsUsbCanBackend,Modbus}.{h,cpp}` | `products/arcscope.md` `SD-09` (V1 generic transports; device SDKs later); `WP-33.00` | Reference Only | Establishes the transport family a product in this category is expected to cover, and confirms ArcForges' V1 subset is a deliberate reduction rather than an omission | GPL-3.0-only — no reuse permitted | Per-adapter real-transport test (`WP-33.00`) | Product Owner | Evidence established |
| AS-03 | MQTT transport | `app/src/IO/Drivers/MQTT.{h,cpp}`, `app/src/MQTT/**` | **Accepted exclusion** — Pro module, and not in accepted V1 transports | Drop | `LICENSE.md` §4 lists MQTT as commercial-only; **its source was not read** | Commercial-only; no rights conferred | — | Licensing and Provenance Owner | Accepted exclusion |
| AS-04 | Circular / rolling buffer | `app/src/IO/CircularBuffer.h` | `products/arcscope.md` `SE-04` (live view vs capture); `WP-33.02` | Reference Only | Confirms the rolling-buffer/live-view separation and its role in pre-trigger windows | GPL-3.0-only — no reuse permitted | First-party test: pausing the view never stops recording | Product Owner | Evidence established |
| AS-05 | Frame reader, frame builder, frame config, checksum | `app/src/IO/{FrameReader,FrameBuilder,FrameConfig,Checksum}.*` | `products/arcscope.md` §decoders; `WP-34.03` | Reference Only | Evidence that framing and checksum validation are first-class and their failures must be visible | GPL-3.0-only — no reuse permitted | First-party test: checksum failures surfaced with counts and locations | Product Owner | Evidence established |
| AS-06 | Data table and frame consumer | `app/src/DataModel/{DataTable,Frame,FrameConsumer}.*` | `products/arcscope.md` §channel/signal/event model; `WP-33.03` | Reference Only | Evidence on the decoded-data model shape | GPL-3.0-only — no reuse permitted | First-party precision and alignment tests | Product Owner | Evidence established |
| AS-07 | Hot-path optimisation | `app/src/DataModel/HotpathOptimization.h`, `app/src/DSP.h` | `products/arcscope.md` §18 (throughput); `WP-13.02`, `WP-33.01` | Reference Only | **Performance evidence**: confirms that a dedicated hot path is required to sustain acquisition rates — supporting the probe in `WP-13.02` | GPL-3.0-only — no reuse permitted | Sustained-throughput measurement with bounded memory | Product Owner | Evidence established |
| AS-08 | Importers — DBC, Modbus map, Protobuf | `app/src/DataModel/Importers/{DBCImporter,ModbusMapImporter,ProtoImporter}.*` | **Accepted exclusion** for V1; retained as later-adapter evidence | Drop | Protocol-description import is beyond the accepted V1 decoder scope; recorded so it is a deliberate choice | GPL-3.0-only — no reuse permitted | — | Product Owner | Accepted exclusion |
| AS-09 | Session database and worker | `app/src/Sessions/{DatabaseManager,DatabaseWorker}.*` | `products/arcscope.md` `SE-14` (chunked verifiable store, not database blobs); `WP-33.04` | Reference Only | **Divergence recorded**: the reference stores session data in a database. ArcForges requires raw capture in a chunked verifiable store instead, because capture is evidence and must be independently verifiable | GPL-3.0-only — no reuse permitted | First-party test: crash yields a verifiable prefix with recorded loss | Architecture Owner | Evidence established |
| AS-10 | Player / replay | `app/src/Sessions/{Player,PlayerLoaderWorker}.*`, `app/src/CSV/Player.*`, `app/src/MDF4/Player.*` | `products/arcscope.md` `SD-10` (replay never impersonates a device); `WP-33.05` | Reference Only | Evidence that replay is a first-class source; ArcForges adds the labelling requirement the reference does not have | GPL-3.0-only — no reuse permitted | First-party test: replay always labelled, device-only fields absent | Product Owner | Evidence established |
| AS-11 | Export — CSV, MDF4, console, session | `app/src/{CSV,MDF4,Console}/Export.*`, `app/src/Sessions/Export.*` | `products/arcscope.md` §16 (export with precision warnings); `WP-35.04` | Reference Only | **Migration evidence**: names the interchange formats expected in this category, and confirms tabular export needs precision handling | GPL-3.0-only — no reuse permitted | Format fixture per claimed export version (`PG-07`) | Product Owner | Evidence established |
| AS-12 | HTML report and report data | `app/src/Sessions/{HtmlReport,ReportData}.*` | `products/arcscope.md` §12 (reports with source traceability); `WP-34.06` | Reference Only | Evidence on report composition; ArcForges additionally requires every element to trace to session, capture, configuration snapshot and analysis version | GPL-3.0-only — no reuse permitted | First-party test: report regeneration produces equivalent results | Product Owner | Evidence established |
| AS-13 | Dashboard widgets — plot, multi-plot, FFT, waterfall, bar, gauge, meter, compass, accelerometer, gyroscope, GPS, LED panel, data grid, terminal, clock, stopwatch | `app/qml/Widgets/Dashboard/*.qml` (24 files) | `products/arcscope.md` §5 visualisation; `WP-34.00` | Reference Only | **Establishes the expected visualisation vocabulary.** ArcForges' V1 set is a deliberate subset; this row is what makes that a choice rather than an oversight | GPL-3.0-only — no reuse permitted | First-party scope reference-signal tests | Product Owner | Evidence established |
| AS-14 | 3D plot and XY plot widgets | `app/qml/Widgets/Dashboard/Plot3D.qml` and the XY plotting implementation | **Accepted exclusion** — Pro modules | Drop | `LICENSE.md` §4 lists XY plotting and 3D visualization as commercial-only; **their implementations were not read** | Commercial-only; no rights conferred | — | Licensing and Provenance Owner | Accepted exclusion |
| AS-15 | Web engine / web view widgets | `app/qml/Widgets/Dashboard/{WebEngineSurface,WebView}.qml` | **Accepted exclusion** — no ArcForges requirement | Drop | An embedded browser surface in a professional acquisition product is outside the accepted scope and is a large security surface | GPL-3.0-only — no reuse | — | Security and Privacy Owner | Accepted exclusion |
| AS-16 | Alarm monitor | `app/src/UI/AlarmMonitor.*` | `products/arcscope.md` §7 triggers; `WP-34.01` | Reference Only | Evidence that threshold alarms are a distinct concept from capture triggers | GPL-3.0-only — no reuse permitted | First-party trigger window tests | Product Owner | Evidence established |
| AS-17 | Notification centre | `app/src/DataModel/NotificationCenter.*`, `app/qml/Widgets/Dashboard/NotificationLog.qml` | `09-shared-desktop-experience.md` §attention; `WP-10.04` | Reference Only | Evidence that acquisition products need a durable event log distinct from transient notifications | GPL-3.0-only — no reuse permitted | First-party durability test | Product Owner | Evidence established |
| AS-18 | Project editor | `app/qml/ProjectEditor/**` | `products/arcscope.md` §2 project model; `WP-33.00` | Reference Only | Evidence on configuring a data schema before acquisition; ArcForges records this as the effective configuration snapshot | GPL-3.0-only — no reuse permitted | First-party test: profile edit never rewrites a historical session | Product Owner | Evidence established |
| AS-19 | MCP handler and command protocol | `app/src/API/{MCPHandler,MCPProtocol,CommandHandler,CommandProtocol,CommandRegistry}.*` | `08-extensions-and-developer-platform.md` §MCP; **V-02**; `WP-35.00` | Reference Only | **Third independent confirmation** that MCP appears as an integration adapter in this product category | GPL-3.0-only — no reuse permitted | Vocabulary mapping record (`VG-02`) | Architecture Owner | Evidence established |
| AS-20 | gRPC API | `app/src/API/GRPC/**` | **Accepted exclusion** — prohibited by the technology constitution | Drop | The accepted constitution prohibits gRPC as a main RPC mechanism; recorded as a deliberate divergence | GPL-3.0-only — no reuse | — | Architecture Owner | Accepted exclusion |
| AS-21 | Path policy | `app/src/API/PathPolicy.*` | `products/arcscope.md` §14 (`AI-08`); `07-security-privacy-and-trust.md` | Reference Only | **Security evidence**: confirms an API that can touch files needs an explicit path policy — supporting ArcForges' resource-identity-not-path rule | GPL-3.0-only — no reuse permitted | First-party test: a reference cannot carry a path | Security and Privacy Owner | Evidence established |
| AS-22 | AI assistant with file sandbox and doc search | `app/src/AI/{Assistant,ChatStore,ContextBuilder,Conversation,DocSearch,FileSandbox,CommandRegistry}.*` | `products/arcscope.md` §14 (bounded structured context); `WP-35.01` | Reference Only | **Directly supports `I-182` and `AI-02`**: the reference sandboxes file access and builds bounded context rather than handing over raw data | GPL-3.0-only — no reuse permitted | First-party test: raw capture structurally cannot enter an AI context payload | Security and Privacy Owner | Evidence established |
| AS-23 | Extension manager | `app/src/Misc/ExtensionManager.*` | `08-extensions-and-developer-platform.md`; `WP-41` | Reference Only | Evidence of an extension surface in this category; ArcForges' out-of-process model diverges deliberately | GPL-3.0-only — no reuse permitted | First-party isolation tests | Architecture Owner | Evidence established |
| AS-24 | Crash tracker | `app/src/Misc/CrashTracker.*` | `12-native-interop-and-media.md` §6; `WP-12.05` | Reference Only | Evidence that native-heavy acquisition products need crash capture; ArcForges requires user approval before upload | GPL-3.0-only — no reuse permitted | First-party test: no report sent without approval | Security and Privacy Owner | Evidence established |
| AS-25 | Backup manager | `app/src/Misc/BackupManager.*` | `13-data-formats-and-portability.md`; `WP-46` | Reference Only | Evidence on local backup expectations | GPL-3.0-only — no reuse permitted | First-party restore proof | Operations Owner | Evidence established |
| AS-26 | CLI and console-only mode | `app/src/Misc/CLI.*`, `tests/integration/test_console_only_mode.py` | **Accepted exclusion** for V1 | Drop | A headless acquisition CLI is beyond the accepted V1 scope; recorded as a choice | GPL-3.0-only — no reuse | — | Product Owner | Accepted exclusion |
| AS-27 | Licensing / activation system | `app/src/Licensing/**` (CommercialToken, LemonSqueezy, MachineID, MonotonicClock, OfflineCertificate, OfflineLicense, GuardSelfTest) | **Accepted exclusion** — Pro module, and **directly contrary to D-022** | Drop | `LICENSE.md` §4 lists activation/licensing as commercial-only; **source not read**. Independently, a machine-bound offline licence key is exactly the unlock path **D-022** prohibits in ArcForges Mobile | Commercial-only; no rights conferred | Mobile commerce-prohibition check (`WP-32.03`) | Licensing and Provenance Owner | Accepted exclusion |
| AS-28 | Platform integration — client-side decorations, native window | `app/src/Platform/{AppPlatform,CSD,NativeWindow*}.*` | `09-shared-desktop-experience.md` §windows; `WP-10.01` | Reference Only | Evidence on per-platform window integration expectations | GPL-3.0-only — no reuse permitted | First-party per-platform window tests | Product Owner | Evidence established |
| AS-29 | Test approach — integration suite | `tests/integration/**` (~20+ named scenarios incl. `test_csv_player`, `test_device_write`, `test_audio_loopback`, `test_dataset_transforms`, `test_console_ansi_vt100`, `test_data_tables`) | `../testing-and-verification-strategy.md` F-05, F-11, F-18 | Reference Only | **Test evidence**: names the acquisition scenarios worth covering — device write, loopback, transforms, player — which ArcScope's suites must also cover | GPL-3.0-only — no reuse permitted | `WP-33`, `WP-34` scenario coverage | Quality Owner | Evidence established |
| AS-30 | Test approach — performance, security and benchmark suites | `tests/{performance,security,benchmarks,manual}/**` | `12-quality-and-compatibility-contract.md` §§7, 9, 15; `WP-13.02` | Reference Only | Confirms that this product category needs performance, security and manual hardware suites as separate families — matching the eighteen-family split | GPL-3.0-only — no reuse permitted | Hardware-lab inventory (`PG-08`) | Quality Owner | Evidence established |
| AS-31 | Packaged release shape | `StartArcForges/Serial-Studio`: `bin/`, `plugins/`, `qml/`, `resources/`, `translations/`, `run.cmd` — **no installer** | `10-distribution-update-and-support.md` §1.1; `14-build-packaging-and-release.md` §5 | Reference Only | **Packaging evidence**: the native Qt reference ships as a loose directory with a launcher script and no installer — the opposite of ArcForges' signed per-user installer requirement | Commercial binary; **not executed** | Update matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 31 rows across all 11 areas |
| Every row carries all nine required fields | **Pass** |
| Every row has exactly one completeness state | **Pass** — 24 evidence established, 7 accepted exclusions, 0 unresolved |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** |
| Pro-module boundary respected | **Pass** — 3 rows (`AS-03`, `AS-14`, `AS-27`) are excluded on licence grounds with their source deliberately unread |
| Packaged binary not executed | **Pass** — directory listing only |
| Any row proposing reuse carries a provenance obligation | **Not applicable** — no row proposes reuse |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

| # | Finding | Effect |
|---|---|---|
| F-AS-1 | **Serial-Studio's licence excludes named features from GPL and reserves them commercially**, and states that source visibility confers no rights. | This is the strictest position in the programme. It creates an **authorship boundary**, not merely a reuse prohibition: three capability areas were deliberately not read. Recorded so a later reader does not mistake the gap for incomplete review. |
| F-AS-2 | **The reference's activation system is a machine-bound offline licence key** (`AS-27`). | Independent confirmation that **D-022**'s prohibition on a licence-key unlock path targets a real, common pattern — and that `MC-05` is correctly identified as the prohibition most likely to be violated by accident. **No design change**; the build check in `WP-32.03` already covers it. |
| F-AS-3 | **The reference stores session data in a database** (`AS-09`). | ArcForges diverges deliberately: raw capture goes to a chunked verifiable store because it is evidence. Recorded so the divergence is visible as a decision. |
| F-AS-4 | **The reference sandboxes AI file access and builds bounded context** (`AS-22`). | Independent support for `I-182` and `AI-02`. No change needed. |
| F-AS-5 | **The native Qt reference ships with no installer** (`AS-31`). | Contrast evidence for `P2-001`: ArcForges' signed per-user installer requirement is a deliberate improvement over the category norm for native products. No change needed. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | Bound to commit `639daafb`. `WP-33` re-checks for drift and newly introduced material; it does not re-create this matrix. |
| MT-02 | **The Pro-module list in `LICENSE.md` §4 is re-read on every drift check.** A feature moving into or out of that list changes the authorship boundary. |
| MT-03 | The packaged binary is never executed, at any stage. |
